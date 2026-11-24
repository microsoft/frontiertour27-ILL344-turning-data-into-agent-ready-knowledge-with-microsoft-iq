# Deploy to Your Own Azure Subscription

This folder contains resources for deploying the ILL344 knowledge base infrastructure to your own Azure subscription.

## Prerequisites

- **Azure subscription** with sufficient permissions to create resources
- **Azure Developer CLI (azd)** installed ([Install guide](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd))
- **Azure CLI** installed and configured ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.10+** installed
- **Git** (to clone this repository)
- **VS Code** or **GitHub Codespaces** with Jupyter extension (recommended)

### Required Azure Permissions

You'll need permissions to:

- Create resource groups
- Deploy Bicep templates
- Create and manage:
  - Foundry IQ (Azure AI Search) services
  - Microsoft Foundry projects
  - Azure OpenAI model deployments
  - Microsoft Fabric capacities
  - Web IQ accounts (`Microsoft.WebIQ/accounts`)
- Assign Azure RBAC roles

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/microsoft/frontiertour27-ILL344-turning-data-into-agent-ready-knowledge-with-microsoft-iq.git
cd frontiertour27-ILL344-turning-data-into-agent-ready-knowledge-with-microsoft-iq
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Deploy with azd

```bash
azd auth login
azd up
```

This will:

- Provision all Azure resources (AI Search, Foundry project, OpenAI models, Fabric capacity, Web IQ account)
- Fetch API keys and write a `.env` file with all required variables
- Create search indexes and upload sample data
- Set up the `CaldovaSupplierAnalytics` lakehouse, `CaldovaMedicinalProductOntology`, the `SupplierSM` semantic model, and `CaldovaSupplierDataAgent`

To skip the Web IQ account, run `azd env set DEPLOY_WEB_IQ false` before `azd up` and skip Part 1.

> **Note:** Email seeding (used in the hosted Skillable lab for Part 3 - Work IQ) requires a service principal with the `Mail.ReadWrite` application permission (emails are created directly in the user's Inbox; `Mail.Send` is only a fallback) and is **not run** during self-deploy. Part 3 will use your own mailbox data instead.

> **Work IQ prerequisites (Part 3):** Work IQ requires (1) a usage-based billing plan (Copilot credits) for Work IQ configured in Copilot Studio, with each user assigned to it, (2) a Microsoft Entra Global Administrator enabling the Work IQ API in the tenant, and (3) an identity running `azd up` with the Cloud Application Administrator role (or the Microsoft Graph application permissions `Application.ReadWrite.All`, `DelegatedPermissionGrant.ReadWrite.All`, and `Directory.Read.All`), so `infra/create-workiq-entra.py` can create the Work IQ Entra app and grant `WorkIQAgent.Ask` admin consent. Part 3's write steps also require a tenant policy that allows Work IQ create, update, delete, and action requests. The provisioning hook is non-fatal, so the other parts still deploy when Work IQ setup is unavailable. See the [Work IQ MCP tool reference](https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/mcp/tool-reference).

### 4. Create your Web IQ API key (Part 1)

Web IQ API keys are created in the Web IQ portal, not by Azure. Go to [Web IQ profile management](https://webiq.microsoft.ai/profiles), connect the `ill344-webiq-...` account in your resource group, create an API key under **Authentication > API Keys**, and add it to `.env` as `WEB_IQ_KEY`.

`azd up` also creates and publishes the `CaldovaSupplierDataAgent` Fabric data agent used in Part 2, with `SupplierSM` and the ontology as its data sources, and writes all three MCP URLs (`FOUNDRY_IQ_MCP_URL`, `FABRIC_ONTOLOGY_MCP_URL`, `FABRIC_DATA_AGENT_MCP_URL`) to `.env`.

### 5. Start the Lab

Open the [notebooks](src/notebooks) folder in VS Code and **start with `part1-web-iq.ipynb`**.

## Cleanup

To delete all resources and avoid ongoing charges:

```bash
azd down
```

## Additional Resources

- [Foundry IQ (Azure AI Search) Documentation](https://learn.microsoft.com/azure/search/)
- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure Bicep Documentation](https://learn.microsoft.com/azure/azure-resource-manager/bicep/)
- [Microsoft Foundry Community Discord](https://aka.ms/AIFoundryDiscord-Ignite25)
