"""Create and publish the Caldova supplier performance Fabric data agent."""

import os
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
LAKEHOUSE_NAME = "CaldovaSupplierAnalytics"
DATA_AGENT_NAME = "CaldovaSupplierDataAgent"
OPERATION_TIMEOUT_SECONDS = 300

# The ontology covers product and substance relationships, so the data agent only sees the
# supplier performance star schema.
SUPPLIER_ANALYTICS_TABLES = {
    "SupplierPerformance",
    "DimSupplier",
    "DimDate",
    "DimLocation",
    "DimInspectionResult",
    "DimAuditResult",
    "DimFinancialRating",
}

AI_INSTRUCTIONS = """Answer Caldova supplier performance questions from the selected lakehouse tables.
Report OTIF12moPct, BatchRejectionRatePct, RightFirstTimePct, and CurrentUtilizationPct as percentages, since they are stored as fractions.
Performance metrics are synthetic analytics, not facts extracted from invoices. Treat null metrics as not applicable, never as zero.
Do not answer product, active-substance, or manufacturer relationship questions. Those come from the Caldova ontology."""

DATASOURCE_INSTRUCTIONS = """SupplierPerformance holds one weekly snapshot per supplier, keyed by SupplierID and DateKey.
Join DimSupplier on SupplierID for supplier names and DimDate on DateKey for snapshot dates.
Use the latest DateKey for current values, and order by DateKey for trends."""


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

    def call(self, method: str, url: str, **kwargs) -> httpx.Response:
        response = self.client.request(method, url, **kwargs)
        response.raise_for_status()
        if response.status_code == httpx.codes.ACCEPTED and "Location" in response.headers:
            deadline = time.monotonic() + OPERATION_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                operation = self.client.get(response.headers["Location"])
                operation.raise_for_status()
                payload = operation.json()
                status = payload.get("status")
                if status == "Succeeded":
                    return response
                if status in ("Failed", "Cancelled"):
                    raise RuntimeError(f"Fabric operation {status.lower()}: {payload.get('error')}")
                time.sleep(min(max(float(operation.headers.get("Retry-After", "2")), 1), 10))
            raise TimeoutError(f"Timed out waiting for {method} {url}.")
        return response

    def list(self, url: str, **params) -> list[dict]:
        page = self.call("GET", url, params=params).json()
        values = list(page.get("value", []))
        while page.get("continuationUri"):
            page = self.call("GET", page["continuationUri"]).json()
            values.extend(page.get("value", []))
        return values

    def close(self) -> None:
        self.client.close()


def find_by_name(items: list[dict], name: str) -> dict | None:
    return next((item for item in items if item.get("displayName") == name), None)


def get_or_create_data_agent(fabric: Fabric, workspace_url: str) -> dict:
    """Return the data agent, creating it when it doesn't exist yet."""
    data_agent = find_by_name(fabric.list(f"{workspace_url}/dataAgents"), DATA_AGENT_NAME)
    if data_agent:
        print(f"Reusing Fabric data agent '{DATA_AGENT_NAME}'.")
        return data_agent
    fabric.call("POST", f"{workspace_url}/dataAgents", json={"displayName": DATA_AGENT_NAME})
    for _ in range(30):
        data_agent = find_by_name(fabric.list(f"{workspace_url}/dataAgents"), DATA_AGENT_NAME)
        if data_agent:
            print(f"Created Fabric data agent '{DATA_AGENT_NAME}'.")
            return data_agent
        time.sleep(2)
    raise RuntimeError(f"Fabric data agent '{DATA_AGENT_NAME}' was created but could not be found.")


def get_or_add_lakehouse_datasource(fabric: Fabric, agent_url: str, workspace_id: str, lakehouse_id: str) -> str:
    """Return the lakehouse data source ID, adding the lakehouse to the draft when needed."""

    def find() -> dict | None:
        return next(
            (
                source
                for source in fabric.list(f"{agent_url}/staging/datasources")
                if source.get("itemReference", {}).get("itemId") == lakehouse_id
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
                "itemReference": {"referenceType": "ById", "itemId": lakehouse_id, "workspaceId": workspace_id},
            },
        )
        datasource = find()
    if datasource is None:
        raise RuntimeError(f"Lakehouse '{LAKEHOUSE_NAME}' was added but is not a data source.")
    return datasource["id"]


def select_tables(fabric: Fabric, elements_url: str) -> None:
    """Select the supplier analytics tables and clear every other table."""
    tables = {
        element["displayName"]: element
        for element in fabric.list(elements_url, recursive="true")
        if element["type"] == "Table"
    }
    missing = SUPPLIER_ANALYTICS_TABLES - tables.keys()
    if missing:
        raise RuntimeError(f"Lakehouse '{LAKEHOUSE_NAME}' is missing tables: {sorted(missing)}")
    for name, table in sorted(tables.items()):
        selected = name in SUPPLIER_ANALYTICS_TABLES
        if table["isSelected"] != selected:
            fabric.call("PATCH", elements_url, params={"id": table["id"]}, json={"isSelected": selected})
    print(f"Selected tables: {', '.join(sorted(SUPPLIER_ANALYTICS_TABLES))}")


def main() -> None:
    """Create or update the data agent, publish it, and save its MCP URL to .env."""
    load_dotenv(ENV_PATH, override=False)
    tenant_id = os.getenv("FABRIC_TENANT_ID") or require_env("AZURE_TENANT_ID")
    workspace_id = require_env("FABRIC_WORKSPACE_ID")
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
        lakehouse = find_by_name(fabric.list(f"{workspace_url}/lakehouses"), LAKEHOUSE_NAME)
        if lakehouse is None:
            raise RuntimeError(f"Lakehouse '{LAKEHOUSE_NAME}' does not exist in workspace {workspace_id}.")

        data_agent = get_or_create_data_agent(fabric, workspace_url)
        agent_url = f"{workspace_url}/dataAgents/{data_agent['id']}"
        datasource_id = get_or_add_lakehouse_datasource(fabric, agent_url, workspace_id, lakehouse["id"])
        select_tables(fabric, f"{agent_url}/staging/datasources/{datasource_id}/elements")

        fabric.call("PATCH", f"{agent_url}/staging/settings", json={"aiInstructions": AI_INSTRUCTIONS})
        fabric.call(
            "PATCH",
            f"{agent_url}/staging/datasources/{datasource_id}",
            json={"description": "Caldova supplier performance star schema", "instructions": DATASOURCE_INSTRUCTIONS},
        )
        fabric.call(
            "POST",
            f"{agent_url}/staging/publish",
            json={"publishedDescription": "Caldova supplier performance analytics"},
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
