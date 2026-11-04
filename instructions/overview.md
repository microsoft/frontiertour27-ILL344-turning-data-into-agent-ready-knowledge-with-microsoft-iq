@lab.Title
## Before you begin

<details>
<summary><strong>🔑 Lab credentials (click to expand when you need to sign in)</strong></summary>

At any point during the lab, if you need to sign in to the virtual machine (Windows) or any Azure or Microsoft 365 apps, use the credentials provided below. Use the lab account, not your personal or work account.

### Sign into virtual machine (Windows)

If you need to sign in the virtual machine, use the following credentials:

- **User name**: +++@lab.VirtualMachine(Win11-Pro-Base).Username+++  
- **Password**: +++@lab.VirtualMachine(Win11-Pro-Base).Password+++

### Sign into Azure & Microsoft 365

If you need to sign in to any Azure or Microsoft 365 apps, use the following credentials:

- **Username**: +++@lab.CloudPortalCredential(User1).Username+++  
- **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++

</details>

## Overview

You are a procurement analyst at **Caldova**, a fictional pharmaceutical company. Your team needs to investigate supplier issues and prepare a supply-chain briefing. The answers are spread across purchasing policy, supplier records, approved agreements, structured product relationships, and recent email.

Your job is not just to get an answer. It is to show **which evidence supports each claim**. An email about a possible delay is not an amended purchase order. A supplier mentioned in a document is not automatically a manufacturer in the ontology.

Through five exercises, you will build Foundry IQ knowledge bases in Azure AI Search, add Fabric IQ and Work IQ, and connect an agent through Model Context Protocol (MCP).

### How to work through the lab

For each exercise, **inspect the source in the browser, run the notebook, and compare the answer with the source**. Keep this guide open alongside Visual Studio Code. Do not select **Run All** and skip the checkpoints.

The browser makes the source data and created resources visible. The notebooks create the knowledge sources and knowledge bases and make authenticated retrieval calls. **You do not need to recreate resources in the portals.**

> [!NOTE]
> These instructions describe the hosted Skillable environment. If you deployed to your own subscription, use the [self-deployment guide](../deploy_yourself.md) for setup, then follow the exercises below using your repository location instead of **Desktop > aitour-ILL344**. Sample emails are seeded only in the hosted lab. Your own mailbox will not necessarily contain the Caldova messages.

## Getting started

Follow the steps below to set up your environment and begin the lab.

### Sign into Windows

In the virtual machine, sign into Windows using the following credentials:

- **User name**: +++@lab.VirtualMachine(Win11-Pro-Base).Username+++  
- **Password**: +++@lab.VirtualMachine(Win11-Pro-Base).Password+++

### Access the lab repository

Once signed in to the Skillable environment, you'll find the lab repository already cloned on your desktop under the folder: **Desktop > aitour-ILL344**.

> This folder contains all the code, notebooks, and resources you'll need for the lab.

### Open the project folder in Visual Studio Code

Open Visual Studio Code and select **File > Open Folder**. Then navigate to Desktop and select the **aitour-ILL344** folder and then **Select Folder**.

> [!TIP]
>
> When prompted whether to trust the authors of the files, select **Yes, I trust the authors**.

### Verify the environment setup

All required Azure services including **Foundry IQ (Azure AI Search) with pre-indexed data** and **Azure OpenAI deployments** have already been provisioned for you.

<details>
<summary><strong>📋 What's pre-configured (click to expand for details)</strong></summary>

- **Foundry IQ (Azure AI Search)** - Standard tier with two pre-created indexes
- **supplier-evidence:** Supplier invoices, shipment evidence, and quality records
- **sourcing-documents:** RFP responses, agreements, purchase orders, and sourcing diagrams
- **Azure OpenAI** - Deployed models **gpt-5.4** for chat completion and answer synthesis and **text-embedding-3-large** for vector embeddings
- **Pre-computed vectors** - All Caldova document chunks are already vectorized and indexed

</details>

#### Verify environment variables

1. Open the **.env** file under the main project folder.  
2. Verify that it includes these environment variables:
   - *AZURE_SEARCH_SERVICE_ENDPOINT*
   - *AZURE_SEARCH_ADMIN_KEY*
   - *AZURE_OPENAI_ENDPOINT*
   - *AZURE_OPENAI_KEY*
   - *AZURE_OPENAI_CHATGPT_DEPLOYMENT*
   - *AZURE_OPENAI_CHATGPT_MODEL_NAME*
   - *AZURE_OPENAI_EMBEDDING_DEPLOYMENT*
   - *AZURE_TENANT_ID*
   - *FABRIC_WORKSPACE_ID*
   - *FABRIC_ONTOLOGY_ID*

If these variables are present, proceed to verify the indexes in Azure Portal.

Keep keys and tokens private. Do not paste `.env` contents into chat, screenshots, or shared notes.

#### Verify indexes in Azure Portal

Confirm that the search indexes have been created successfully:

1. Open a web browser and navigate to the +++https://portal.azure.com+++.
2. Sign in using your lab credentials:
    - **Username**: +++@lab.CloudPortalCredential(User1).Username+++  
    - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++
3. If the **Stay signed in?** prompt appears, select **Yes**.
4. In the Azure Portal search bar at the top, search for +++ill344-search+++ and select your AI Search service (it will look like *ill344-search-.....*).
5. In the left navigation menu, select **Search management** > **Indexes**.
6. You should see two indexes:
   - **supplier-evidence** - Should show a nonzero document count
   - **sourcing-documents** - Should show a nonzero document count

If your indexes are present and populated, keep this browser tab open. You will inspect their contents in Exercise 1. If either index is missing or empty, ask a proctor before continuing.

Select **Next** to start **Exercise 1: Build Foundry IQ knowledge bases with agentic retrieval**. Outside Skillable, continue to the exercise below.

===
# Exercise 1: Build Foundry IQ knowledge bases with agentic retrieval

Caldova's distribution team needs to decide whether goods can be distributed after a temperature excursion, a period of high temperature during shipment. You will query a Foundry IQ knowledge base with indexed documents to investigate what happened and find the final distribution decision.

## Inspect the documents before running code

1. In your Azure portal tab, return to **Search management > Indexes** and open **supplier-evidence**.
2. Open **Search explorer**. In the search text box, enter +++SHIP-VC-1026-BOS-FRA+++ and select **Search**. Inspect a result's **chunk**, **title**, **blob_path**, and page-number fields.
3. In File Explorer, open **Desktop > aitour-ILL344 > data > caldova > pdfs**. Open **TL-VCL-1026.pdf** and **EXC-VC-1026-04.pdf** in Microsoft Edge. Find the temperature record and the disposition evidence.
4. Finally, open **CAL-POL-PUR-001.pdf** from the same folder and find an approval or escalation rule. Unlike the shipment records, this policy is not in either pre-created index. The notebook will introduce a file knowledge source and upload the policy directly.

**Compare the records:** Follow the shipment identifier from the temperature logger to the investigation report. Find both the initial quarantine status and the final disposition. Keep these records open to check whether the generated answer distinguishes the two stages.

## Build and query the knowledge bases

1. In Visual Studio Code, open **src > notebooks > part1-standard-foundry-iq-kb.ipynb**.
2. Select **Select Kernel > Python Environments**, then choose the environment at **.venv\Scripts\python.exe**. Use this same Python environment in the remaining exercises.
3. Follow the notebook's instructions **from top to bottom** and run the corresponding code cells **in sequence**. Wait for each cell to finish before starting the next.

Work through **Steps 1 to 5** to upload the policy and query the policy-only knowledge base. Allow about 40 seconds for file ingestion.

Then work through **Steps 6 to 9** to connect both existing indexes and create **caldova-supply-chain-knowledge-base**. Run the shipment query, then the **activity log**, **references**, and **Source Hunt** sections.

## Verify what you built in the browser

1. Return to your Azure AI Search service. Select **Agentic retrieval > Knowledge bases** and refresh the list.
2. Find **caldova-policy-knowledge-base** and **caldova-supply-chain-knowledge-base**. Inspect their knowledge sources. The first uses the policy file. The second uses that file plus **supplier-evidence-knowledge-source** and **sourcing-documents-knowledge-source**.
3. Compare one cited shipment claim with the PDF you opened. Use the reference's title and page numbers to find the evidence. A `blob_path` is citation metadata and might not be a directly accessible link.

**Checkpoint:** In the notebook answer, find the distribution conclusion and its supporting reference. Use the reference's title and page numbers to locate the final disposition in the investigation PDF. Check that the answer distinguishes the initial quarantine from the final decision.

## Optional: Query the knowledge base in the GitHub Copilot app

After completing the checkpoint, you can query the same knowledge base from a chat client instead of Python. The notebook provides the MCP URL. Follow the app instructions here, not in the notebook.

### Get the MCP URL

In **part1-standard-foundry-iq-kb.ipynb**, run the cell under **Optional: Get the knowledge base MCP URL**. Keep the printed URL available.

### Sign in to GitHub and open the app

1. In the browser, sign in through +++https://github.com/enterprises/skillable-events/sso+++. This uses the special GitHub account created for your lab environment, not your personal GitHub account.
2. Open the **GitHub Copilot** app from the desktop shortcut.
3. Select **Sign in to GitHub**. If an installation process starts, wait for it to complete before continuing with the GitHub sign-in process.
4. When the browser opens, use the lab GitHub account, paste the device code from the app, and select **Authorize GitHub**.
5. Return to the app. You do not need to connect a repository. Select **Continue** on the repository selection screen and **Finish** on the preferences screen.

### Add the knowledge base MCP server

1. Select **Customize** in the sidebar, then select the **MCP** tab.
2. Open the **Add** menu and select **MCP server**.
3. Enter these values:
   - **Server name**: +++caldova-kb+++
   - **Server type**: **HTTP**, not Local/SSE
   - **URL**: the complete URL printed by the notebook
   - **Header name**: +++api-key+++
   - **Header value**: the value of **AZURE_SEARCH_ADMIN_KEY** from your lab `.env` file
4. Select **Add server** and confirm that **caldova-kb** appears in the server list.
5. Start a new chat by selecting **+** next to **Chats** in the sidebar and ask:

   +++Compare Summit Dose's documented CALD-201 commitments across its Caldova RFP response, agreement amendment, and purchase order.+++

Whether you try the optional activity or skip it, select **Next** to continue to **Exercise 2: Add structured data from Fabric IQ** once you have completed the notebook and checkpoint.

===
# Exercise 2: Add structured data from Fabric IQ

Caldova's procurement team has found Meridian API Works invoice and quality evidence for lot **AUR-API-7**. The documents identify the lot and its active substance, but the team also needs to find which medicinal product uses that substance. You will add a Fabric IQ ontology knowledge source to connect those document facts with structured product relationships.

## Explore the Fabric data

1. In the browser, go to +++https://app.fabric.microsoft.com+++ and sign in with your lab account.
2. Select **Workspaces** and open the workspace whose name starts with **CaldovaSupplyChain-**. If several are listed, match its workspace ID in the browser URL to **FABRIC_WORKSPACE_ID** in `.env`.
3. Open **CaldovaSupplierAnalytics**. Under **Tables**, preview **ActiveSubstance**, **MedicinalProduct**, and **ProductActiveSubstance**. Find **SUB-001** in the substance table and follow its ID through the linking table to a product.
4. Return to the workspace and open **CaldovaMedicinalProductOntology**. Inspect **MedicinalProduct**, **ActiveSubstance**, and **Manufacturer**, and the **contains** and **manufactures** relationships. The ontology gives business meaning to the table relationships.

**Trace the relationship:** Use **ProductActiveSubstance** to connect **SUB-001** to a medicinal product. Keep that relationship available to compare with the retrieval result.

## Add Fabric IQ and query

Open **src/notebooks/part2-fabric-iq-to-kb.ipynb**. Run **Steps 1 to 5**, signing in with the same lab account when prompted. This creates **caldova-fabric-knowledge-base** over the Part 1 sources plus Fabric IQ.

If the browser sign-in window is hidden, minimize other windows **inside the virtual machine**. Keep the outer browser hosting Skillable open.

Allow about 40 seconds for retrieval. Run the activity and reference cells, then complete **Source Hunt**.

## Verify the relationship

1. Find a `searchIndex` reference for the **AUR-API-7** lot evidence and a `fabricOntology` reference for the substance-to-product relationship.
2. Compare the product in `fabricRawData` with the **SUB-001** relationship you inspected in Fabric.

**Checkpoint:** Match the lot claim to its indexed document reference, then match the product claim to `fabricRawData` and the table relationship you inspected. Flag any claimed relationship that the structured results do not contain.

Once you have completed the notebook and checkpoint, select **Next** to continue to **Exercise 3: Add workplace context from Work IQ**.

===
# Exercise 3: Add workplace context from Work IQ

Caldova's supply team has recent emails about Summit Dose equipment mapping, subcontractor approval, and delivery planning for **CALD-201**. You will add a Work IQ knowledge source to compare these updates with approved sourcing commitments, using the signed-in user's Microsoft 365 permissions.

## Read the source emails first

1. In the browser, go to +++https://outlook.office.com+++ and sign in with your lab account.
2. Open **Inbox** and search for +++CALD-201+++. Read these three sample emails:
   - **CALD-201 transfer checkpoint - equipment mapping approval needed**
   - **CALD-201 testing subcontractor - Piedmont evidence incomplete**
   - **Decision Friday: protect the CALD-201 April delivery**
3. Identify an action owner, a deadline, and a decision that is still open. Keep the emails available for comparison with the answer.
4. From the lab's PDF folder, open **PO-CAL-SUM-2026-1108.pdf** and compare its delivery commitment with the delivery email.

**Compare the dates:** Locate the proposed **12 May** release in the email and the approved **30 April** delivery commitment in the purchase order. Keep the two records available to check how the answer describes their different roles.

> [!NOTE]
> These are fictional scenario dates, not deadlines relative to today's date. If the hosted mailbox is empty or the messages are missing, ask a proctor. Do not seed messages yourself or switch to your personal mailbox. If you self-deployed, use relevant messages you are authorized to access and adapt the question. You will not be able to verify these three sample messages unless they have been seeded.

## Add Work IQ and query

Open **src/notebooks/part3-work-iq-to-kb.ipynb**. Run **Steps 1 to 5**, signing in with the lab account when prompted. This creates **caldova-workiq-knowledge-base** over the Part 1 sources plus Work IQ, not the Fabric source.

Allow 1 to 2 minutes for retrieval. While waiting, compare the emails with the purchase order. Do not submit the query again while the cell is running.

## Verify against your mailbox

1. Run the activity and reference cells and complete **Source Hunt**.
2. In a `workIQ` reference, find a supporting link in the text or a citation's `targetLink`. Open it in the browser and compare an owner, deadline, or decision with the original email. If a link cannot open, find the message by subject in Outlook.
3. Find a separate `searchIndex` reference supporting an approved sourcing commitment.

**Checkpoint:** Check that the answer labels the email as a planning update and preserves the purchase order's approved commitment. Match each date to its supporting reference. Work IQ is querying accessible workplace context at runtime, not uploading your entire mailbox to either document index.

Once you have completed the notebook and checkpoint, select **Next** to continue to **Exercise 4: Combine Work IQ and Fabric IQ**.

===
# Exercise 4: Combine Work IQ and Fabric IQ

Caldova's executive team needs one **CALD-201** supply-chain briefing that brings together purchasing controls, approved Summit Dose commitments, current actions, and active-substance manufacturers. You will combine the existing document sources with Work IQ and Fabric IQ in one knowledge base, then check which source supports each part of the briefing.

## Match briefing claims to sources

Use this table to track the role of each source. After retrieval, add a reference identifier or source title from your own result in your notes.

| Briefing claim | Expected source | Evidence you found |
| --- | --- | --- |
| Purchasing approval or escalation rule | Policy file | |
| Approved Summit Dose commitment | Sourcing documents index | |
| Current equipment-mapping or delivery action | Work IQ | |
| Manufacturers of Caldovexine, SUB-001 | Fabric IQ | |

The **supplier-evidence** index is also available for operational evidence. Having five configured sources does not mean every question needs results from all five.

## Combine the sources

Open **src/notebooks/part4-work-iq-fabric-iq-to-kb.ipynb**. Run **Steps 1 to 5** to create **caldova-supply-chain-briefing-knowledge-base** and request the briefing. This notebook obtains separate authorization for Fabric IQ and Work IQ.

Allow 1 to 2 minutes for retrieval. Run the activity and reference cells and complete **Source Hunt**.

## Inspect and verify

1. Return to **Agentic retrieval > Knowledge bases** in the Azure portal and refresh. Inspect **caldova-supply-chain-briefing-knowledge-base** and its five configured sources.
2. Complete the evidence column above from the returned references, not from memory. If a claim or its supporting reference is absent, mark it **not returned** rather than filling it in from expectation.
3. Reopen one supporting email in Outlook and compare one structured claim with the Fabric tables. Check that the briefing preserves the different roles of these sources.

**Checkpoint:** Compare any claim that Summit Dose manufactures Caldovexine with the returned ontology evidence. If that relationship is absent, mark the claim as unsupported. Mentioning a supplier in an email is not evidence of a manufacturing relationship in Fabric.

Once you have completed the notebook and checkpoint, select **Next** to continue to **Exercise 5: Build an agent with Microsoft Agent Framework**.

===
# Exercise 5: Build an agent with Microsoft Agent Framework

Caldova's supply-chain team wants an agent that can use retrieved evidence to answer the shipment question from Part 1. You will connect Microsoft Agent Framework to an extractive knowledge base through MCP. Unlike Parts 1 to 4, the knowledge base will return evidence without synthesizing an answer, and the agent's model will produce the response.

## Compare the configurations

Open **src/notebooks/part5-agent-framework-mcp.ipynb** and compare **Step 3: Create an extractive knowledge base** with Part 1's knowledge base definition.

Look for **EXTRACTIVE_DATA**, **minimal** reasoning effort, and the absence of an attached knowledge base model. This uses the **three Part 1 sources**, not the five-source briefing knowledge base. The agent still has its own model.

## Build and run the agent

Run **Steps 1 to 7** in order. You create **caldova-supply-chain-minimal-knowledge-base**, connect it through MCP, run **CaldovaSupplyChainAgent**, and display the tool-call table.

This agent runs inside the notebook. You do not deploy a Foundry Hosted Agent or need a Microsoft Foundry playground for this exercise.

## Verify the agent's work

1. In the Azure portal, refresh **Agentic retrieval > Knowledge bases** and find **caldova-supply-chain-minimal-knowledge-base**. Compare its sources and output mode with **caldova-supply-chain-knowledge-base** from Part 1.
2. In the notebook's tool-call table, find the retrieval call and inspect the query arguments. If no retrieval call is shown, do not assume the answer used the knowledge base.
3. Compare the answer's shipment conclusion with Part 1 and with **EXC-VC-1026-04.pdf** in the browser. Wording may differ. The evidence and distribution conclusion should agree.

**Checkpoint:** Follow the retrieval query in the tool-call table back to the three configured document sources, then check the agent's distribution conclusion against the investigation PDF. Compare the extractive knowledge base definition with the agent's model configuration to see where answer generation now happens.

Once you have completed all five notebooks and checkpoints, select **Next** in Skillable to review the summary and next steps. Outside Skillable, open the [lab summary](summary.md).
