"""Create or update the Caldova SupplierSM Direct Lake semantic model."""

import base64
import os
import time
import warnings
from pathlib import Path

from azure.core.credentials import TokenCredential
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from dotenv import load_dotenv, set_key

warnings.filterwarnings("ignore", category=SyntaxWarning, module=r"microsoft_fabric_api\..*")

from microsoft_fabric_api import FabricClient
from microsoft_fabric_api.generated.semanticmodel.models import (
    CreateSemanticModelRequest,
    SemanticModelDefinition,
    SemanticModelDefinitionPart,
    UpdateSemanticModelDefinitionRequest,
)

REPO_ROOT = Path(__file__).parents[1]
ENV_PATH = REPO_ROOT / ".env"
DEFINITION_ROOT = REPO_ROOT / "data" / "caldova" / "semantic-model" / "SupplierSM"
LAKEHOUSE_NAME = "CaldovaSupplierAnalytics"
SEMANTIC_MODEL_NAME = "SupplierSM"
PORTAL_BASE_URL = "https://app.fabric.microsoft.com"
SQL_ENDPOINT_TIMEOUT_SECONDS = 300


def require_env(name: str) -> str:
    """Return a required environment setting."""
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required to create the semantic model.")
    return value


def create_credential(tenant_id: str) -> TokenCredential:
    """Use a service principal in Skillable and azd credentials for local setup."""
    if os.getenv("AZURE_CLIENT_ID") and os.getenv("AZURE_CLIENT_SECRET"):
        return DefaultAzureCredential()
    return AzureDeveloperCliCredential(tenant_id=tenant_id)


def find_lakehouse(client: FabricClient, workspace_id: str):
    """Find the supplier analytics lakehouse by display name."""
    return next(
        (item for item in client.lakehouse.items.list_lakehouses(workspace_id) if item.display_name == LAKEHOUSE_NAME),
        None,
    )


def wait_for_sql_endpoint(client: FabricClient, workspace_id: str, lakehouse_id: str):
    """Wait until the lakehouse SQL analytics endpoint is ready."""
    deadline = time.monotonic() + SQL_ENDPOINT_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        lakehouse = client.lakehouse.items.get_lakehouse(workspace_id, lakehouse_id)
        endpoint = lakehouse.properties.sql_endpoint_properties
        if endpoint.provisioning_status == "Success":
            if not endpoint.id or not endpoint.connection_string:
                raise RuntimeError("The SQL endpoint is ready but has no identity.")
            return endpoint
        if endpoint.provisioning_status == "Failed":
            raise RuntimeError("The lakehouse SQL endpoint failed to provision.")
        time.sleep(5)
    raise TimeoutError("Timed out waiting for the lakehouse SQL endpoint.")


def definition_part(path: Path, replacements: dict[str, str]) -> SemanticModelDefinitionPart:
    """Encode one TMDL definition part after resolving the SQL endpoint markers."""
    relative_path = path.relative_to(DEFINITION_ROOT).as_posix()
    content = path.read_text(encoding="utf-8")
    for marker, value in replacements.items():
        content = content.replace(marker, value)
    if "{{" in content or "}}" in content:
        raise ValueError(f"Unresolved definition marker in {relative_path}.")
    return SemanticModelDefinitionPart(
        path=relative_path,
        payload=base64.b64encode(content.encode("utf-8")).decode("ascii"),
        payload_type="InlineBase64",
    )


def build_definition(sql_endpoint: str, sql_database: str) -> SemanticModelDefinition:
    """Build the source-controlled TMDL definition bound to the lakehouse SQL endpoint."""
    files = sorted(path for path in DEFINITION_ROOT.rglob("*") if path.is_file())
    if not files or not (DEFINITION_ROOT / "definition.pbism").exists():
        raise RuntimeError("The SupplierSM TMDL definition is incomplete.")
    replacements = {"{{SQL_ENDPOINT}}": sql_endpoint, "{{SQL_DATABASE}}": sql_database}
    return SemanticModelDefinition(format="TMDL", parts=[definition_part(path, replacements) for path in files])


def run_fabric_operation(operation) -> None:
    """Run a Fabric long-running operation, tolerating the SDK's KeyError('status') bug.

    microsoft-fabric-api can raise KeyError('status') from its result callback even though the
    operation finishes server-side, so treat that specific error as success.
    """
    try:
        operation()
    except KeyError:
        print("Fabric long-running operation returned no status; treating as complete.")


def find_semantic_model(client: FabricClient, workspace_id: str):
    """Find SupplierSM by display name."""
    return next(
        (
            item
            for item in client.semanticmodel.items.list_semantic_models(workspace_id)
            if item.display_name == SEMANTIC_MODEL_NAME
        ),
        None,
    )


def main() -> None:
    """Create or update SupplierSM and save its ID to .env."""
    load_dotenv(ENV_PATH, override=False)
    tenant_id = os.getenv("FABRIC_TENANT_ID") or require_env("AZURE_TENANT_ID")
    workspace_id = require_env("FABRIC_WORKSPACE_ID")
    credential = create_credential(tenant_id)
    try:
        client = FabricClient(credential)
        lakehouse = find_lakehouse(client, workspace_id)
        if lakehouse is None:
            raise RuntimeError(f"Lakehouse '{LAKEHOUSE_NAME}' does not exist in workspace {workspace_id}.")
        endpoint = wait_for_sql_endpoint(client, workspace_id, lakehouse.id)
        definition = build_definition(endpoint.connection_string, endpoint.id)
        semantic_model = find_semantic_model(client, workspace_id)
        if semantic_model is None:
            print(f"Creating semantic model '{SEMANTIC_MODEL_NAME}'...")
            run_fabric_operation(
                lambda: client.semanticmodel.items.create_semantic_model(
                    workspace_id,
                    CreateSemanticModelRequest(
                        display_name=SEMANTIC_MODEL_NAME,
                        description="Synthetic supplier performance analytics for Caldova.",
                        definition=definition,
                    ),
                )
            )
            semantic_model = find_semantic_model(client, workspace_id)
            if semantic_model is None:
                raise RuntimeError(f"Semantic model '{SEMANTIC_MODEL_NAME}' was created but could not be found.")
        else:
            print(f"Updating semantic model '{SEMANTIC_MODEL_NAME}'...")
            run_fabric_operation(
                lambda: client.semanticmodel.items.update_semantic_model_definition(
                    workspace_id,
                    semantic_model.id,
                    UpdateSemanticModelDefinitionRequest(definition=definition),
                )
            )
    finally:
        close = getattr(credential, "close", None)
        if close:
            close()

    ENV_PATH.touch()
    set_key(ENV_PATH, "FABRIC_SEMANTIC_MODEL_ID", semantic_model.id, quote_mode="never")
    print(f"Semantic model: {SEMANTIC_MODEL_NAME} ({semantic_model.id})")
    print(f"Fabric UI: {PORTAL_BASE_URL}/groups/{workspace_id}/datasets/{semantic_model.id}/details")


if __name__ == "__main__":
    main()
