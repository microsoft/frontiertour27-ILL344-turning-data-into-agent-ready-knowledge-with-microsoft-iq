"""Create and publish the Caldova Fabric data agent over SupplierSM and the medicinal-product ontology."""

import base64
import json
import os
import re
import time
from pathlib import Path

import httpx
from azure.core.credentials import TokenCredential
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from dotenv import load_dotenv, set_key

REPO_ROOT = Path(__file__).parents[1]
ENV_PATH = REPO_ROOT / ".env"
FABRIC_API_URL = "https://api.fabric.microsoft.com"
FABRIC_SCOPE = f"{FABRIC_API_URL}/.default"
SEMANTIC_MODEL_NAME = "SupplierSM"
DATA_AGENT_NAME = "CaldovaSupplierDataAgent"
OPERATION_TIMEOUT_SECONDS = 300
SEMANTIC_MODEL_TABLES = {
    "DimAuditResult",
    "DimDate",
    "DimFinancialRating",
    "DimInspectionResult",
    "DimLocation",
    "DimSupplier",
    "SupplierPerformance",
}

AI_INSTRUCTIONS = """Use SupplierSM for Caldova supplier performance: suppliers, service categories,
locations, capacity, quality, regulatory status, commercial metrics, and weekly performance trends.
Use the latest and four-week change measures for current status and recent movement. Report
percentage metrics as percentages. Performance metrics are synthetic analytics, not facts extracted
from invoices, and null manufacturing metrics mean not applicable, never zero.
Use CaldovaMedicinalProductOntology for medicinal products, active substances, manufacturers,
marketing authorizations, regulatory agencies, and the relationships among them.
For questions that span both sources, join Manufacturer.manufacturerId from the ontology to
DimSupplier.SupplierID in SupplierSM, and combine the results by that exact ID.
When querying the ontology, generate Fabric Ontology GQL. Use FILTER after MATCH for predicates,
never WHERE. Entity types are MedicinalProduct, ActiveSubstance, Manufacturer, MarketingAuthorization,
and RegulatoryAgency. Relationships are contains, manufactures, hasAuthorization, and issuedBy."""


def require_env(name: str) -> str:
    """Return a required environment setting."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required to create the Fabric data agent.")
    return value


def create_credential(tenant_id: str) -> TokenCredential:
    """Use a service principal in Skillable and azd credentials for local setup."""
    if os.getenv("AZURE_CLIENT_ID") and os.getenv("AZURE_CLIENT_SECRET"):
        return DefaultAzureCredential()
    return AzureDeveloperCliCredential(tenant_id=tenant_id)


class Fabric:
    """Minimal Fabric REST client that waits for long-running operations."""

    def __init__(self, token: str) -> None:
        self.client = httpx.Client(
            base_url=FABRIC_API_URL,
            headers={"Authorization": f"Bearer {token}"},
            timeout=60,
        )

    def wait(self, response: httpx.Response) -> httpx.Response:
        if response.status_code != httpx.codes.ACCEPTED or "Location" not in response.headers:
            return response
        location = response.headers["Location"]
        deadline = time.monotonic() + OPERATION_TIMEOUT_SECONDS
        while time.monotonic() < deadline:
            operation = self.client.get(location)
            operation.raise_for_status()
            payload = operation.json()
            status = payload.get("status")
            if status == "Succeeded":
                return response
            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Fabric operation {status.lower()}: {payload.get('error')}")
            time.sleep(min(max(float(operation.headers.get("Retry-After", "2")), 1), 10))
        raise TimeoutError(f"Timed out waiting for the Fabric operation at {location}.")

    def call(self, method: str, url: str, **kwargs) -> httpx.Response:
        response = self.client.request(method, url, **kwargs)
        response.raise_for_status()
        return self.wait(response)

    def list_items(self, url: str, **params) -> list[dict]:
        page = self.call("GET", url, params=params).json()
        values = list(page.get("value", []))
        while page.get("continuationUri"):
            page = self.call("GET", page["continuationUri"]).json()
            values.extend(page.get("value", []))
        return values

    def get_definition(self, item_url: str) -> list[dict]:
        """Return a Fabric item's definition parts, waiting for the operation if needed."""
        response = self.client.post(f"{item_url}/getDefinition")
        response.raise_for_status()
        if response.status_code == httpx.codes.ACCEPTED:
            self.wait(response)
            response = self.call("GET", f"{response.headers['Location']}/result")
        return response.json()["definition"]["parts"]

    def close(self) -> None:
        self.client.close()


def find_by_name(items: list[dict], name: str) -> dict | None:
    return next((item for item in items if item.get("displayName") == name), None)


def decode_part(part: dict) -> str:
    return base64.b64decode(part["payload"]).decode("utf-8")


def get_or_create_data_agent(fabric: Fabric, workspace_url: str) -> dict:
    """Return the data agent, creating it when it doesn't exist yet."""
    data_agent = find_by_name(fabric.list_items(f"{workspace_url}/dataAgents"), DATA_AGENT_NAME)
    if data_agent:
        print(f"Reusing Fabric data agent '{DATA_AGENT_NAME}'.")
        return data_agent
    fabric.call("POST", f"{workspace_url}/dataAgents", json={"displayName": DATA_AGENT_NAME})
    for _ in range(30):
        data_agent = find_by_name(fabric.list_items(f"{workspace_url}/dataAgents"), DATA_AGENT_NAME)
        if data_agent:
            print(f"Created Fabric data agent '{DATA_AGENT_NAME}'.")
            return data_agent
        time.sleep(2)
    raise RuntimeError(f"Fabric data agent '{DATA_AGENT_NAME}' was created but could not be found.")


def get_or_add_datasource(fabric: Fabric, agent_url: str, workspace_id: str, item_id: str) -> str:
    """Return the staging data source ID for a Fabric item, adding the item when needed."""

    def find() -> dict | None:
        return next(
            (
                source
                for source in fabric.list_items(f"{agent_url}/staging/datasources")
                if source.get("itemReference", {}).get("itemId") == item_id
            ),
            None,
        )

    datasource = find()
    if datasource is None:
        fabric.call(
            "POST",
            f"{agent_url}/staging/datasources",
            json={
                "type": "FabricItem",
                "itemReference": {"referenceType": "ById", "itemId": item_id, "workspaceId": workspace_id},
            },
        )
        datasource = find()
    if datasource is None:
        raise RuntimeError(f"Fabric item {item_id} was added but is not a data source.")
    return datasource["id"]


def select_semantic_model_tables(fabric: Fabric, elements_url: str) -> None:
    """Select every SupplierSM table."""
    tables = {element["displayName"]: element for element in fabric.list_items(elements_url) if element.get("type") == "Table"}
    if set(tables) != SEMANTIC_MODEL_TABLES:
        raise RuntimeError(
            f"{SEMANTIC_MODEL_NAME} tables differ. Expected {sorted(SEMANTIC_MODEL_TABLES)}, found {sorted(tables)}."
        )
    for name, table in sorted(tables.items()):
        if not table.get("isSelected"):
            fabric.call("PATCH", elements_url, params={"id": table["id"]}, json={"isSelected": True})
    print(f"Selected {SEMANTIC_MODEL_NAME} tables: {', '.join(sorted(tables))}")


def get_ontology_entities(fabric: Fabric, workspace_url: str, ontology_id: str) -> dict[str, list[str]]:
    """Return each ontology entity's property names from its TMDL definition."""
    entities = {}
    for part in fabric.get_definition(f"{workspace_url}/ontologies/{ontology_id}"):
        if not part["path"].startswith("entities/"):
            continue
        text = decode_part(part)
        entity = re.search(r"^entity (\S+)", text, re.MULTILINE)
        if entity:
            entities[entity.group(1)] = re.findall(r"^\tproperty (\S+)", text, re.MULTILINE)
    if not entities:
        raise RuntimeError(f"Ontology {ontology_id} has no TMDL entities.")
    return entities


def attach_ontology(fabric: Fabric, workspace_id: str, agent_url: str, ontology_id: str) -> None:
    """Attach the ontology through the data agent definition, since the datasources API blocks ontologies."""
    workspace_url = f"/v1/workspaces/{workspace_id}"
    parts = fabric.get_definition(agent_url)
    draft_prefix = "Files/Config/draft/ontologies/"
    draft_ontologies = [part for part in parts if part["path"].startswith(draft_prefix)]

    ontology = fabric.call("GET", f"{workspace_url}/ontologies/{ontology_id}").json()
    entities = get_ontology_entities(fabric, workspace_url, ontology_id)
    ontology_config = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/dataAgent/definition/ontology/1.0.0/schema.json",
        "artifactId": ontology_id,
        "workspaceId": workspace_id,
        "displayName": ontology["displayName"],
        "elements": [
            {
                "id": name,
                "is_selected": True,
                "display_name": name,
                "type": "ontology.entity",
                "description": ",".join(properties),
                "children": [],
            }
            for name, properties in entities.items()
        ],
        "entitiesWithUserAuthoredDescriptions": list(entities),
    }
    ontology_path = f"{draft_prefix}{ontology['displayName']}/ontology.json"
    if [(part["path"], json.loads(decode_part(part))) for part in draft_ontologies] == [(ontology_path, ontology_config)]:
        print(f"Reusing ontology '{ontology['displayName']}'.")
        return

    print(f"Attaching ontology '{ontology['displayName']}'...")
    parts = [part for part in parts if part not in draft_ontologies] + [
        {
            "path": ontology_path,
            "payload": base64.b64encode(json.dumps(ontology_config, indent=2).encode("utf-8")).decode("ascii"),
            "payloadType": "InlineBase64",
        }
    ]
    fabric.call("POST", f"{agent_url}/updateDefinition", json={"definition": {"parts": parts}})


def main() -> None:
    """Create or update the data agent, publish it, and save its MCP URL to .env."""
    load_dotenv(ENV_PATH, override=False)
    tenant_id = os.getenv("FABRIC_TENANT_ID") or require_env("AZURE_TENANT_ID")
    workspace_id = require_env("FABRIC_WORKSPACE_ID")
    ontology_id = os.getenv("FABRIC_ONTOLOGY_ID", "").strip()
    workspace_url = f"/v1/workspaces/{workspace_id}"

    credential = create_credential(tenant_id)
    try:
        token = credential.get_token(FABRIC_SCOPE).token
    finally:
        close = getattr(credential, "close", None)
        if close:
            close()

    fabric = Fabric(token)
    try:
        semantic_model = find_by_name(fabric.list_items(f"{workspace_url}/semanticModels"), SEMANTIC_MODEL_NAME)
        if semantic_model is None:
            raise RuntimeError(f"Semantic model '{SEMANTIC_MODEL_NAME}' does not exist in workspace {workspace_id}.")

        data_agent = get_or_create_data_agent(fabric, workspace_url)
        agent_url = f"{workspace_url}/dataAgents/{data_agent['id']}"
        fabric.call("PATCH", f"{agent_url}/staging/settings", json={"aiInstructions": AI_INSTRUCTIONS})

        datasource_id = get_or_add_datasource(fabric, agent_url, workspace_id, semantic_model["id"])
        select_semantic_model_tables(fabric, f"{agent_url}/staging/datasources/{datasource_id}/elements")

        if ontology_id:
            attach_ontology(fabric, workspace_id, agent_url, ontology_id)
        else:
            print("WARNING: FABRIC_ONTOLOGY_ID is not set, so the ontology was not attached to the data agent.")

        fabric.call(
            "POST",
            f"{agent_url}/staging/publish",
            json={"publishedDescription": "Caldova supplier performance and medicinal-product relationships"},
        )
    finally:
        fabric.close()

    mcp_url = f"{FABRIC_API_URL}/v1/mcp/workspaces/{workspace_id}/dataagents/{data_agent['id']}/agent"
    ENV_PATH.touch()
    set_key(ENV_PATH, "FABRIC_DATA_AGENT_ID", data_agent["id"], quote_mode="never")
    set_key(ENV_PATH, "FABRIC_DATA_AGENT_MCP_URL", mcp_url, quote_mode="never")
    print(f"Published Fabric data agent: {DATA_AGENT_NAME} ({data_agent['id']})")
    print(f"Data agent MCP: {mcp_url}")


if __name__ == "__main__":
    main()
