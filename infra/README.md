# Infrastructure

Normal attendee deployment restores the committed `supplier-evidence` and `sourcing-documents` snapshots by running `create-knowledge.py`. It does not require Blob Storage or Content Understanding.

When Fabric is configured, `create-caldova-lakehouse.py` loads the synchronized Caldova JSON into `CaldovaSupplierAnalytics`, and `create-caldova-ontology.py` creates or updates `CaldovaMedicinalProductOntology`. An existing `FABRIC_WORKSPACE_ID` is reused. Otherwise, deployment creates a workspace on `FABRIC_CAPACITY_ID` and grants the Skillable attendee access. `create-caldova-data-agent.py` then creates and publishes `CaldovaSupplierDataAgent` over the supplier analytics tables and writes `FABRIC_DATA_AGENT_MCP_URL`. Setup also writes `FOUNDRY_IQ_MCP_URL` for `caldova-supply-chain-knowledge-base`, which attendees create in Part 4.

`main.bicep` also deploys a Web IQ account (`Microsoft.WebIQ/accounts`) for Part 1. It is defined inline, not as a module, because the Skillable validation step expects exactly one deployment in the resource group. Its API key comes from the [Web IQ portal](https://webiq.microsoft.ai/profiles), not from Azure, so attendees create it and add it to `.env` as `WEB_IQ_KEY`. Set the `deployWebIq` parameter to `false` to skip the account.

## Refresh the index snapshots

Maintainers can reproduce the snapshots as follows:

1. Run `python3 scripts/sync-caldova-data.py ../aitour27-caldova-data` from the repository root.
2. Set `DEPLOY_INDEXING_STORAGE=true` and provision the infrastructure.
3. Run `python3 infra/create-index-snapshots.py` with the deployment outputs in the environment.
4. Run `python3 scripts/export-search-index.py`.
5. Run `python3 scripts/validate-index-snapshots.py`.
6. Review and commit the synchronized PDFs, Fabric JSON, manifests, index definitions, and JSONL snapshots together.

The indexing storage account is maintainer-only. Attendee deployments leave `DEPLOY_INDEXING_STORAGE=false`.
