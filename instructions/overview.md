@lab.Title
## Before you begin

<details>
<summary><strong>🔑 Lab credentials (click to expand when you need to sign in)</strong></summary>

At any point during the lab, if you need to sign in to the virtual machine (Windows) or any Azure or Microsoft 365 apps, use the credentials provided below. Use the lab account, not your personal or work account.

### Sign into virtual machine (Windows)

If you need to sign in the virtual machine, use the following credentials:

- **User name**: +++@lab.VirtualMachine(ILL344:Win11).Username+++
- **Password**: +++@lab.VirtualMachine(ILL344:Win11).Password+++

### Sign into Azure & Microsoft 365

If you need to sign in to any Azure or Microsoft 365 apps, use the following credentials:

- **Username**: +++@lab.CloudPortalCredential(User1).Username+++  
- **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++

</details>

## Overview

You are a procurement analyst at **Caldova**, a fictional pharmaceutical company. Your team needs to investigate supplier issues and prepare a supply-chain briefing. The answers are spread across the public web, structured supplier data, recent email, purchasing policy, supplier records, and approved agreements.

Your job is not just to get an answer. It is to show **which evidence supports each claim**. An email about a possible delay is not an amended purchase order. A web article about cold-chain guidance is not Caldova's investigation report.

Through four exercises, you will give agents context with Microsoft IQ: **Web IQ** for the web, **Fabric IQ** for structured business data, **Work IQ** for your Microsoft 365 work, and a **Foundry IQ** knowledge base over Caldova's documents. You will call each one from a Python notebook, most of them through Model Context Protocol (MCP).

### How to work through the lab

For each exercise, **inspect the source in the browser, run the notebook, and compare the answer with the source**. Keep this guide open alongside Visual Studio Code.

The browser makes the source data and created resources visible. The notebooks create resources and make authenticated calls. **You do not need to recreate resources in the portals.**

## Getting started

Follow the steps below to set up your environment and begin the lab.

### Sign into Windows

In the virtual machine, sign into Windows using the following credentials:

- **User name**: +++@lab.VirtualMachine(ILL344:Win11).Username+++
- **Password**: +++@lab.VirtualMachine(ILL344:Win11).Password+++

### Access the lab repository

Once signed in to the Skillable environment, you'll find the lab repository already cloned on your desktop under the folder: **Desktop > aitour-ILL344**.

> This folder contains all the code, notebooks, and resources you'll need for the lab.

### Open the project folder in Visual Studio Code

Open Visual Studio Code and select **File > Open Folder**. Then navigate to Desktop and select the **aitour-ILL344** folder and then **Select Folder**.

> [!TIP]
>
> When prompted whether to trust the authors of the files, select **Yes, I trust the authors**.

### Verify the environment setup

All required Azure services, Fabric items, and sample emails have already been provisioned for you.

<details>
<summary><strong>📋 What's pre-configured (click to expand for details)</strong></summary>

- **Web IQ** - A Web IQ account in your resource group. You create its API key in Exercise 1.
- **Microsoft Fabric** - A workspace with the **CaldovaSupplierAnalytics** lakehouse and the **CaldovaMedicinalProductOntology** ontology
- **Work IQ** - A Microsoft Entra app registration with admin consent to call Work IQ as you, and three sample CALD-201 emails in your mailbox
- **Foundry IQ (Azure AI Search)** - Two pre-created indexes
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
   - *FABRIC_ONTOLOGY_MCP_URL*
   - *WORK_IQ_ENTRA_APP_ID*
   - *WORK_IQ_ENTRA_TENANT_ID*

You will add **WEB_IQ_KEY** yourself in Exercise 1. If any other variable is missing, ask a proctor before continuing.

Keep keys and tokens private. Do not paste `.env` contents into chat, screenshots, or shared notes.

#### Sign in to the Azure portal

1. Open a web browser and navigate to the +++https://portal.azure.com+++.
2. Sign in using your lab credentials:
    - **Username**: +++@lab.CloudPortalCredential(User1).Username+++  
    - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++
3. If the **Stay signed in?** prompt appears, select **Yes**.

Keep the browser open. The next sign-ins reuse this session.

### Optional: Set up the GitHub Copilot app

Each exercise ends with an optional activity that adds the same IQ to the **GitHub Copilot** app as an MCP server, so you can query it from a chat. If you want to try those activities, set up the app now. Otherwise, skip this section.

1. In the browser, sign in through +++https://github.com/enterprises/skillable-events/sso+++. This uses the special GitHub account created for your lab environment, not your personal GitHub account.
2. Open the **GitHub Copilot** app from the desktop shortcut.
3. Select **Sign in to GitHub**. If an installation process starts, wait for it to complete before continuing with the GitHub sign-in process.
4. When the browser opens, use the lab GitHub account, paste the device code from the app, and select **Authorize GitHub**.
5. Return to the app. You do not need to connect a repository. Select **Continue** on the repository selection screen and **Finish** on the preferences screen.

Select **Next** to start **Exercise 1: Ground answers in the web with Web IQ**.

===
# Exercise 1: Ground answers in the web with Web IQ

Shipment **SHIP-VC-1026-BOS-FRA** ran above its labelled temperature range. Before the distribution team reviews Caldova's own records, it wants current public guidance on handling temperature excursions. You will call Web IQ through MCP to find that guidance as citable passages.

## Get your Web IQ key

A Web IQ account was created for you in your resource group. Create an API key for it in the Web IQ portal:

1. In the browser, go to +++https://webiq.microsoft.ai/profiles+++.
2. In the sign-in prompt, select your lab account.
3. In **Select an Azure Resource**, select your lab subscription for **Azure subscription**, and then select the resource that starts with **ill344-webiq-** for **Resource**. Select **Finish**.
4. If a dialog invites you to try Web IQ in a playground, select **Skip**.
5. On the profile management page, scroll to the bottom. Under **Authentication > API Keys**, select **Create API key**, enter any name, and select **Create**. Copy the new key.

Then save the key so the notebook can use it:

1. In Visual Studio Code, open the **.env** file in the lab folder.
2. Add a new line at the end of the file with **WEB_IQ_KEY=**, and paste the key after the equals sign. For example: **WEB_IQ_KEY=your-key**.
3. Save the file.

## Call Web IQ from the notebook

1. In Visual Studio Code, open **src > notebooks > part1-web-iq.ipynb**.
2. Select **Select Kernel > Python Environments**, then choose the environment at **.venv\Scripts\python.exe**. Use this same Python environment in the remaining exercises.
3. Follow the notebook's instructions **from top to bottom** and run **Steps 1 to 5** in sequence. Wait for each cell to finish before starting the next.

You list the Web IQ tools, then search web pages, images, and videos.

## Verify the evidence

1. In the Step 3 results, pick a result from a peer-reviewed journal or a regulator. Open its URL in the browser and find the passage on the page.
2. Note which questions about the shipment the web cannot answer, such as what happened to these 4,800 units. You will answer them from Caldova's own evidence in Exercise 4.

## Optional: Use Web IQ in the GitHub Copilot app

1. In the GitHub Copilot app, select **Customize**, and then select **Add > MCP Server...**.
2. Enter these values:
    - **Server name**: +++web-iq+++
    - **Server type**: **HTTP**, not Local/SSE
    - **URL**: +++https://api.microsoft.ai/v3/mcp+++
3. Select **Add header**, and enter the name +++x-apikey+++. Switch to Visual Studio Code, copy the **WEB_IQ_KEY** value from **.env**, and then switch back to the app and paste it as the header value.
4. Select **Add server**. Then select the **Installed** tab and confirm that **web-iq** is toggled on and has a green check mark.
5. Start a new chat by selecting **+** next to **Chats** in the sidebar and ask:

    +++Use Web IQ to find current guidance on handling temperature excursions during pharmaceutical shipments. Cite your sources.+++

Once you have completed the notebook, select **Next** to continue to **Exercise 2: Query structured data with Fabric IQ**.

===
# Exercise 2: Query structured data with Fabric IQ

Caldova's procurement team has found Meridian API Works invoice and quality evidence for lot **AUR-API-7**, which contains Caldovexine (**SUB-001**). The team needs two kinds of structured answers: which products and manufacturers are related to the substance, and how Meridian API Works' delivery performance is trending. You will query the Fabric IQ ontology through MCP, then create and publish a Fabric data agent for the trend questions.

## Explore the Fabric data

1. In the browser, go to +++https://app.fabric.microsoft.com+++ and sign in with your lab account.
2. Select **Workspaces** and open the workspace whose name starts with **CaldovaSupplyChain-**. If several are listed, match its workspace ID in the browser URL to **FABRIC_WORKSPACE_ID** in `.env`.
3. Open **CaldovaSupplierAnalytics**, then expand **Schemas > dbo > Tables**. Preview **ActiveSubstance**, **MedicinalProduct**, and **ProductActiveSubstance**. Find **SUB-001** in the substance table and follow its ID through the linking table to a product.
4. Preview **DimSupplier** and **SupplierPerformance**. Find the **SupplierID** for Meridian API Works and look at a few of its weekly rows. Notice the **OTIF12moPct** and **BatchRejectionRatePct** columns.
5. Return to the workspace and open **CaldovaMedicinalProductOntology**. Inspect **MedicinalProduct**, **ActiveSubstance**, and **Manufacturer**, and the **contains** and **manufactures** relationships. The ontology gives business meaning to the table relationships.

**Trace the relationship:** Use **ProductActiveSubstance** to connect **SUB-001** to a medicinal product. Keep that relationship and Meridian API Works' rows available to compare with the notebook's answers.

## Call Fabric IQ from the notebook

Open **src/notebooks/part2-fabric-iq.ipynb** and run **Steps 1 to 8** in order, signing in with the same lab account when prompted.

If the browser sign-in window is hidden, minimize other windows **inside the virtual machine**. Keep the outer browser hosting Skillable open.

- **Steps 2 and 3** call the ontology's MCP endpoint. The `ask_ontology` answer takes 30 to 60 seconds.
- **Steps 4 to 6** create **CaldovaSupplierDataAgent** with the Fabric REST API, select the supplier analytics tables, add instructions, and publish it.
- **Steps 7 and 8** call the published data agent's MCP endpoint with ranking and trend questions.

## Verify what you built

1. Return to your Fabric workspace and refresh it. Open **CaldovaSupplierDataAgent**.
2. In the **Explorer** pane, expand **CaldovaSupplierAnalytics** and confirm that only the supplier analytics tables are selected. Open the agent's instructions and compare them with the notebook.
3. Open a deep link from the notebook's answer, inspect the generated query, and compare Meridian API Works' latest values with the **SupplierPerformance** rows you previewed.
4. Compare the ontology's product answer with the **SUB-001** relationship you traced in the lakehouse.

## Optional: Use Fabric IQ in the GitHub Copilot app

Add two MCP servers, one for the ontology and one for the data agent. Both sign you in with your Microsoft Entra account, so they don't need headers.

In Visual Studio Code, open the **.env** file and find **FABRIC_ONTOLOGY_MCP_URL** and **FABRIC_DATA_AGENT_MCP_URL**. The notebook added the second one in Step 6.

1. In the GitHub Copilot app, select **Customize**, and then select **Add > MCP Server...**.
2. Enter these values, and then select **Add server**:
    - **Server name**: +++fabric-iq-ontology+++
    - **Server type**: **HTTP**
    - **URL**: the complete **FABRIC_ONTOLOGY_MCP_URL** value from **.env**. Copy only the URL after the first **=**.
3. Select **Add > MCP Server...** again, enter these values, and then select **Add server**:
    - **Server name**: +++fabric-iq-data-agent+++
    - **Server type**: **HTTP**
    - **URL**: the complete **FABRIC_DATA_AGENT_MCP_URL** value from **.env**. Copy only the URL after the first **=**.
4. Switch to the **Installed** tab. For each server, select **Sign in** and complete the Microsoft Entra sign-in in the browser with your lab account:
    - **Username**: +++@lab.CloudPortalCredential(User1).Username+++
    - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++
5. Confirm that both servers are toggled on and each has a green check mark. Then start a new chat and ask:

    +++Which Caldova medicinal products contain Caldovexine, and how has Meridian API Works' OTIF changed over the last four weeks?+++

Once you have completed the notebook, select **Next** to continue to **Exercise 3: Bring in work context with Work IQ**.

===
# Exercise 3: Bring in work context with Work IQ

Caldova's supply team has recent emails about Summit Dose equipment mapping, subcontractor approval, and delivery planning for **CALD-201**. You will use Work IQ to read that context as you, compare it with the approved purchase order, schedule the delivery decision, and send a follow-up.

## Read the source emails first

1. In the browser, go to +++https://outlook.office.com+++ and sign in with your lab account.
2. Open **Inbox** and search for +++CALD-201+++. Read these three sample emails:
   - **CALD-201 transfer checkpoint - equipment mapping approval needed**
   - **CALD-201 testing subcontractor - Piedmont evidence incomplete**
   - **Decision Friday: protect the CALD-201 April delivery**
3. Identify an action owner, a deadline, and a decision that is still open. Keep the emails available for comparison with the answer.
4. In File Explorer, open **Desktop > aitour-ILL344 > data > caldova > pdfs**. Open **PO-CAL-SUM-2026-1108.pdf** in Microsoft Edge and compare its delivery commitment with the delivery email.

**Compare the dates:** Locate the proposed **12 May** release in the email and the approved **30 April** delivery commitment in the purchase order. Keep the two records available to check how the answers describe their different roles.

> [!NOTE]
> These are fictional scenario dates, not deadlines relative to today's date. If the hosted mailbox is empty or the messages are missing, ask a proctor. Do not seed messages yourself or switch to your personal mailbox. If you self-deployed, use relevant messages you are authorized to access and adapt the questions.

## Ask, retrieve, and discover

Open **src/notebooks/part3-work-iq.ipynb**. Run **Steps 1 to 8**, signing in with the lab account when prompted. These steps only read data.

- **Step 3** uses `ask` for a synthesized answer and a follow-up in the same conversation. Allow 30 to 60 seconds for each answer.
- **Step 4** uses `retrieve` for the cited passages behind that answer.
- **Steps 5 to 8** use `discover`, `search_paths`, `get_schema`, `fetch`, and `list_agents`.

## Act on your behalf

The remaining cells **change real data in your lab mailbox and calendar without input prompts**. Run them one at a time and check the result in Outlook after each:

1. Run **Step 9** to create the decision meeting. In Outlook, open **Calendar** and go to tomorrow. Find **CALD-201: decide on the weekend coating slot**, a 30-minute event at 15:00 UTC (Outlook shows it in your local time zone), and open it to see the agenda.
2. Run **Step 10** to update the meeting and check your reminders. Refresh the calendar and confirm that the subject now ends with **and change control** and that the event is 45 minutes long.
3. Run **Step 11** to send the follow-up. In Outlook, open your **Inbox** and find **CALD-201 follow-up: weekend coating slot decision** with the purchase order attached. It can take a minute to arrive. You can also find it in **Sent Items**.
4. Run **Step 12** to download the attachment from Sent Items with `fetch_blob` and confirm that it matches the file on disk.
5. Run **Step 13** to delete the meeting. Refresh the calendar and confirm that the event is gone.

When resuming after a kernel restart, run **Steps 1 and 2** to sign in again, then check Outlook to see which actions have completed before continuing. If a write fails with a policy error, ask a proctor.

## Verify against your mailbox

1. Pick an owner or deadline from the Step 3 answer. Find a passage that supports it in the Step 4 results, then open the original email in Outlook and compare.
2. In your follow-up email, find the statement that comes from the purchase order rather than the emails. Check that it matches **PO-CAL-SUM-2026-1108.pdf**.

## Optional: Use Work IQ in the GitHub Copilot app

Work IQ is available as a plugin, so you install it instead of adding the MCP server yourself.

1. In the GitHub Copilot app, select **Customize**, and then select **Browse**.
2. Search for +++workiq+++.
3. Under **Plugins**, find **WorkIQ** from Microsoft, and select **Install**.
4. Start a new chat and ask:

    +++Check my recent emails about CALD-201. Summarize the open actions, owners, and deadlines.+++

5. If the chat shows that the **workiq** MCP server needs you to sign in, select **Sign in** and complete the Microsoft Entra sign-in in the browser with your lab account. Then send the same question again.

Once you have completed the notebook, select **Next** to continue to **Exercise 4: Build a knowledge base with Foundry IQ**.

===
# Exercise 4: Build a knowledge base with Foundry IQ

Caldova's distribution team needs to decide whether goods can be distributed after the temperature excursion on shipment **SHIP-VC-1026-BOS-FRA**. In Exercise 1, you found public guidance. Now you will query a Foundry IQ knowledge base over Caldova's own documents to investigate what happened and find the final distribution decision.

## Inspect the documents before running code

1. In the Azure portal, search for +++ill344-search+++ in the top search bar and select your AI Search service (it will look like *ill344-search-.....*).
2. Select **Search management > Indexes**. Confirm that **supplier-evidence** and **sourcing-documents** both show a nonzero document count. If either index is missing or empty, ask a proctor before continuing.
3. Open **supplier-evidence**, then open **Search explorer**. In the search text box, enter +++SHIP-VC-1026-BOS-FRA+++ and select **Search**. Inspect a result's **chunk**, **title**, **blob_path**, and page-number fields.
4. In File Explorer, open **Desktop > aitour-ILL344 > data > caldova > pdfs**. Open **TL-VCL-1026.pdf** and **EXC-VC-1026-04.pdf** in Microsoft Edge. Find the temperature record and the disposition evidence.
5. Finally, open **CAL-POL-PUR-001.pdf** from the same folder and find an approval or escalation rule. Unlike the shipment records, this policy is not in either pre-created index. The notebook will introduce a file knowledge source and upload the policy directly.

**Compare the records:** Follow the shipment identifier from the temperature logger to the investigation report. Find both the initial quarantine status and the final disposition. Keep these records open to check whether the generated answer distinguishes the two stages.

## Build and query the knowledge bases

Open **src/notebooks/part4-foundry-iq.ipynb** and follow the notebook **from top to bottom**, running the code cells **in sequence**.

Work through **Steps 1 to 5** to upload the policy and query the policy-only knowledge base. Allow about 40 seconds for file ingestion.

Then work through **Steps 6 to 9** to connect both existing indexes and create **caldova-supply-chain-knowledge-base**. Run the shipment query, then the **activity log** and **references** cells.

## Verify what you built in the browser

1. Return to your Azure AI Search service. Select **Agentic retrieval > Knowledge bases** and refresh the list.
2. Find **caldova-policy-knowledge-base** and **caldova-supply-chain-knowledge-base**. Inspect their knowledge sources. The first uses the policy file. The second uses that file plus **supplier-evidence-knowledge-source** and **sourcing-documents-knowledge-source**.
3. Compare one cited shipment claim with the PDF you opened. Use the reference's title and page numbers to find the evidence. A `blob_path` is citation metadata and might not be a directly accessible link.

## Optional: Query the knowledge base in the GitHub Copilot app

You can also query the same knowledge base from the GitHub Copilot app instead of Python. The notebook provides the MCP URL. Follow the app instructions here, not in the notebook.

1. In **part4-foundry-iq.ipynb**, run the cell under **Optional: Get the knowledge base MCP URL**. Keep the printed URL available.
2. In the GitHub Copilot app, select **Customize**, then select **Add > MCP Server...**.
3. Enter these values:
   - **Server name**: +++caldova-kb+++
   - **Server type**: **HTTP**, not Local/SSE
   - **URL**: the complete URL printed by the notebook
   - **Header name**: +++api-key+++
   - **Header value**: the value of **AZURE_SEARCH_ADMIN_KEY** from your lab `.env` file
4. Select **Add server**. Then select the **Installed** tab and confirm that **caldova-kb** appears under **MCP Servers**.
5. Start a new chat and ask:

   +++Compare Summit Dose's documented CALD-201 commitments across its Caldova RFP response, agreement amendment, and purchase order.+++

Once you have completed all four notebooks, select **Next** in Skillable to review the summary and next steps.
