@lab.Title

## Overview

In this lab, you give AI agents context with Microsoft IQ: Web IQ for the web, Fabric IQ for structured business data, Work IQ for your Microsoft 365 work, and Foundry IQ for your documents. For each IQ, you call it from a Python notebook, and then you add it as an MCP server in the GitHub Copilot app so you can ask it questions from a chat.

The scenario is Caldova, a fictional pharmaceutical company, where you work as a procurement analyst looking into supplier issues: cold-chain guidance on the web, supplier and product data in Fabric, CALD-201 emails in your mailbox, and purchasing policies and agreements in Azure AI Search. Along the way, you check each answer against the source it came from.

## Sign in to Windows

Sign in to the virtual machine with these credentials:

- **User name**: +++@lab.VirtualMachine(ILL344:Win11).Username+++
- **Password**: +++@lab.VirtualMachine(ILL344:Win11).Password+++

## Set up Visual Studio Code

### Open the lab folder

1. Open Visual Studio Code.
2. Select **File > Open Folder**, go to **Desktop**, select the **aitour-ILL344** folder, and then select **Select Folder**.
3. When prompted whether to trust the authors of the files, select **Yes, I trust the authors**.

### Check the environment setup

Your Azure resources, search indexes, Fabric items, Work IQ app registration, and sample emails are already created for you.

1. In Visual Studio Code, select **Terminal > New Terminal**.
2. Wait a few seconds for the Python virtual environment to be activated in the terminal.
3. Run this command to show the MCP server URLs that setup saved for you:

    +++Get-Content .env | Select-String "MCP_URL"+++

    You should see three lines: **FOUNDRY_IQ_MCP_URL**, **FABRIC_ONTOLOGY_MCP_URL**, and **FABRIC_DATA_AGENT_MCP_URL**. If any are missing, let a proctor know.

### Sign in to the Azure portal

1. Open the browser and go to +++https://portal.azure.com+++.
2. Sign in with your lab credentials:
   - **Username**: +++@lab.CloudPortalCredential(User1).Username+++
   - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++
3. If the **Stay signed in?** prompt appears, select **Yes**.

Keep the browser open. The next sign-ins reuse this session.

## Sign in to GitHub

1. In the browser, sign in to the GitHub enterprise organization for Skillable:

    +++https://github.com/enterprises/skillable-events/sso+++

You will be signed into a special account created for the lab environment, not your actual GitHub account.

## Set up the GitHub Copilot app

In the exercises, you will connect the GitHub Copilot app to each IQ so you can query it from a chat.

1. Open the **GitHub Copilot** app from the desktop shortcut.
2. Select **Sign in to GitHub**. If an installation process starts, wait for it to complete before continuing.
3. When the browser opens, select the lab GitHub account.
4. Paste the 8-digit code from the app screen.
5. Select **Authorize GitHub**.
6. Return to the **GitHub Copilot** app. On the next screen, leave the folder selection empty and select **Continue**. You will use the app for chat and VS Code for working with the lab folder.
7. Send a message to the agent in the chat box, such as:

    +++Write a short haiku about a supply chain that runs on time.+++

Select **Next** to start **Exercise 1: Web IQ**.

===
# Exercise 1: Web IQ

Web IQ grounds answers in current web content.

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

In the notebook, select **Select Kernel > Python Environments**, and choose the **.venv** environment with the path **.venv\Scripts\python.exe**. Use this same environment in every notebook in the lab.

1. In Visual Studio Code, open **src > notebooks > part1-web-iq.ipynb**.
2. Follow the notebook's instructions **from top to bottom** and run **Steps 1 to 5** in sequence. Wait for each cell to finish before starting the next. You list the Web IQ tools, then search web pages, images, and videos.

> [!Hint] **Troubleshooting:** If code cells get stuck and keep spinning, try these remediation steps:
>
> 1. Select **Restart** from the notebook toolbar at the top. If that doesn't work:
> 2. Select **Developer: Reload Window** from the VS Code command palette. If that doesn't work:
> 3. Close VS Code completely and restart it. Reopen the lab folder and notebook. If cells still get stuck, let a proctor know.

## Verify the evidence

1. In the Step 3 results, pick a result from a peer-reviewed journal or a regulator. Open its URL in the browser and find the passage on the page.
2. Note which questions about the shipment the web cannot answer, such as what happened to these 4,800 units. You will answer them from Caldova's own evidence in Exercise 4.

## Use Web IQ in the GitHub Copilot app

1. In the GitHub Copilot app, select **Customize**, and then select **Add > MCP Server...**.
2. Enter these values:
    - **Server name**: +++web-iq+++
    - **Server type**: HTTP
    - **URL**: +++https://api.microsoft.ai/v3/mcp+++
3. Select **Add header**, and enter the name +++x-apikey+++. Switch to Visual Studio Code, copy the **WEB_IQ_KEY** value from **.env**, and then switch back to the app and paste it as the header value.
4. Select **Add server**, and then switch to the **Installed** tab. Under **MCP Servers**, confirm that **web-iq** is toggled on and has a green check mark.

Then select **New** and ask:

+++Use Web IQ to find current guidance on what to check when a pharmaceutical shipment has a temperature excursion. Cite your sources.+++

Once you have completed the notebook, select **Next** to continue to **Exercise 2: Fabric IQ**.

===
# Exercise 2: Fabric IQ

Fabric IQ gives agents structured business data from Microsoft Fabric. Your Fabric workspace has a Caldova lakehouse, an ontology over medicinal products, active substances, and manufacturers, and a published Fabric data agent over supplier performance.

Caldova's procurement team has found Meridian API Works invoice and quality evidence for lot **AUR-API-7**, which contains Caldovexine (**SUB-001**). The team needs two kinds of structured answers: which products and manufacturers are related to the substance, and how Meridian API Works' delivery performance is trending. You will query the Fabric IQ ontology and a Fabric data agent through MCP.

## Explore the Fabric data

Before calling Fabric IQ from code, explore the data and relationships in the Fabric portal. These items are already created for you. You don't need to create or edit them.

1. In the browser, go to +++https://app.fabric.microsoft.com+++ and sign in with your lab account.
2. Select **Workspaces** and open the workspace whose name starts with **CaldovaSupplyChain-**. If several are listed, match its workspace ID in the browser URL to **FABRIC_WORKSPACE_ID** in **.env**.
3. Open **CaldovaSupplierAnalytics**, then expand **Schemas > dbo > Tables**. Preview **ActiveSubstance**, **MedicinalProduct**, and **ProductActiveSubstance**. Find **SUB-001** in the substance table and follow its ID through the linking table to a product.
4. Preview **DimSupplier** and **SupplierPerformance**. Find the **SupplierID** for Meridian API Works and look at a few of its weekly rows. Notice the **OTIF12moPct** and **BatchRejectionRatePct** columns.
5. Return to the workspace and open **CaldovaMedicinalProductOntology**. Inspect **MedicinalProduct**, **ActiveSubstance**, and **Manufacturer**, and the **contains** and **manufactures** relationships. The ontology gives business meaning to the table relationships.
6. Return to the workspace and open **CaldovaSupplierDataAgent**. In the **Explorer** pane, expand **CaldovaSupplierAnalytics** and see which tables are selected. Open the agent's instructions to see how it should join the tables and present the metrics. The data agent answers analytical questions over these tables in natural language.

**Trace the relationship:** Use **ProductActiveSubstance** to connect **SUB-001** to a medicinal product. Keep that relationship and Meridian API Works' rows available to compare with the notebook's answers.

## Call Fabric IQ from the notebook

In the notebook, select **Select Kernel > Python Environments**, and choose the **.venv** environment with the path **.venv\Scripts\python.exe**.

Open **src/notebooks/part2-fabric-iq.ipynb** and run **Steps 1 to 6** in order, signing in with the same lab account when prompted.

> [!Help] **Sign-in window:** If the sign-in window is hidden, minimize the other windows **inside the lab virtual machine** until you find it. Keep the outer browser hosting the Skillable lab open.

- **Steps 2 and 3** call the ontology's MCP endpoint. The **ask_ontology** answer takes 30 to 60 seconds.
- **Steps 4 to 6** call the data agent's MCP endpoint with ranking and trend questions.

> [!Hint] **Troubleshooting:** If code cells get stuck and keep spinning, try these remediation steps:
>
> 1. Select **Restart** from the notebook toolbar at the top. If that doesn't work:
> 2. Select **Developer: Reload Window** from the VS Code command palette. If that doesn't work:
> 3. Close VS Code completely and restart it. Reopen the lab folder and notebook. If cells still get stuck, let a proctor know.

## Verify the answers

1. Open a deep link from the data agent's answer, inspect the generated query, and compare Meridian API Works' latest values with the **SupplierPerformance** rows you previewed.
2. Compare the ontology's product answer with the **SUB-001** relationship you traced in the lakehouse.

## Use Fabric IQ in the GitHub Copilot app

Add two MCP servers, one for the ontology and one for the data agent. Both sign you in with your Microsoft Entra account, so they don't need headers.

In Visual Studio Code, open the **.env** file in the lab folder and find **FABRIC_ONTOLOGY_MCP_URL** and **FABRIC_DATA_AGENT_MCP_URL**. Keep the file open so you can switch back to it when each URL is needed.

1. In the GitHub Copilot app, select **Customize**, and then select **Add > MCP Server...**.
2. Enter these values, and then select **Add server**:
    - **Server name**: +++fabric-iq-ontology+++
    - **Server type**: HTTP
    - **URL**: switch to Visual Studio Code, copy the complete **FABRIC_ONTOLOGY_MCP_URL** value from **.env**, and switch back to the app to paste it. Copy only the URL after the first **=**, without surrounding quotes.
3. Select **Add > MCP Server...** again, enter these values, and then select **Add server**:
    - **Server name**: +++fabric-iq-data-agent+++
    - **Server type**: HTTP
    - **URL**: switch to Visual Studio Code, copy the complete **FABRIC_DATA_AGENT_MCP_URL** value from **.env**, and switch back to the app to paste it. Copy only the URL after the first **=**, without surrounding quotes.
4. Switch to the **Installed** tab. Under **MCP Servers**, find **fabric-iq-ontology** and select **Sign in**. A Microsoft Entra sign-in page opens in the browser. Sign in with:

    - **Username**: +++@lab.CloudPortalCredential(User1).Username+++
    - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++

    At the **Enter Temporary Access Pass** screen, enter the pass above and select **Sign in**. Then return to the GitHub Copilot app.

5. On the **Installed** tab, find **fabric-iq-data-agent**, select **Sign in**, and complete the sign-in in the browser the same way.
6. Confirm that both servers are toggled on and each has a green check mark. If sign-in still fails, let a proctor know.

Then select **New** and ask:

+++Which Caldova medicinal products contain Caldovexine, and which manufacturers make it?+++

+++How has Meridian API Works' OTIF changed over the last four weekly snapshots?+++

Once you have completed the notebook, select **Next** to continue to **Exercise 3: Work IQ**.

===
# Exercise 3: Work IQ

Work IQ gives agents your Microsoft 365 work context: email, meetings, files, chats, and people. It always uses your own permissions.

Caldova's supply team has recent emails about Summit Dose equipment mapping, subcontractor approval, and delivery planning for **CALD-201**. You will use Work IQ to read that context as you, compare it with the approved purchase order, schedule the delivery decision, and send a follow-up.

## Read the source emails first

Your mailbox has three emails about CALD-201. Read them before asking Work IQ about them.

1. In the browser, go to +++https://outlook.office.com+++ and sign in with your lab credentials if prompted.
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

In the notebook, select **Select Kernel > Python Environments**, and choose the **.venv** environment with the path **.venv\Scripts\python.exe**.

Open **src/notebooks/part3-work-iq.ipynb**. Run **Steps 1 to 8**, signing in with the lab account when prompted. These steps only read data.

> [!Help] **Sign-in window:** If the sign-in window is hidden, minimize the other windows **inside the lab virtual machine** until you find it. Keep the outer browser hosting the Skillable lab open.

- **Step 3** uses **ask** for a synthesized answer and a follow-up in the same conversation. Allow 30 to 60 seconds for each answer.
- **Step 4** uses **retrieve** for the cited passages behind that answer.
- **Steps 5 to 8** use **discover**, **search_paths**, **get_schema**, **fetch**, and **list_agents**.

## Act on your behalf

The remaining cells **change real data in your lab mailbox and calendar without input prompts**. Run them one at a time and check the result in Outlook after each:

1. Run **Step 9** to create the decision meeting. In Outlook, open **Calendar** and go to tomorrow. Find **CALD-201: decide on the weekend coating slot**, a 30-minute event at 15:00 UTC (Outlook shows it in your local time zone), and open it to see the agenda.
2. Run **Step 10** to update the meeting and check your reminders. Refresh the calendar and confirm that the subject now ends with **and change control** and that the event is 45 minutes long.
3. Run **Step 11** to send the follow-up. In Outlook, open your **Inbox** and find **CALD-201 follow-up: weekend coating slot decision** with the purchase order attached. It can take a minute to arrive. You can also find it in **Sent Items**.
4. Run **Step 12** to download the attachment from Sent Items with **fetch_blob** and confirm that it matches the file on disk.
5. Run **Step 13** to delete the meeting. Refresh the calendar and confirm that the event is gone.

When resuming after a kernel restart, run **Steps 1 and 2** to sign in again, then check Outlook to see which actions have completed before continuing. A proctor can help if an action needs state from before the restart, or if a write fails with a policy error.

> [!Hint] **Troubleshooting:** If code cells get stuck and keep spinning, try these remediation steps:
>
> 1. Select **Restart** from the notebook toolbar at the top. If that doesn't work:
> 2. Select **Developer: Reload Window** from the VS Code command palette. If that doesn't work:
> 3. Close VS Code completely and restart it. Reopen the lab folder and notebook. If cells still get stuck, let a proctor know.

## Verify against your mailbox

1. Pick an owner or deadline from the Step 3 answer. Find a passage that supports it in the Step 4 results, then open the original email in Outlook and compare.
2. In your follow-up email, find the statement that comes from the purchase order rather than the emails. Check that it matches **PO-CAL-SUM-2026-1108.pdf**.

## Use Work IQ in the GitHub Copilot app

Work IQ is available as a plugin, so you install it instead of adding the MCP server yourself.

1. In the GitHub Copilot app, select **Customize**, and then select **Browse**.
2. Search for +++workiq+++.
3. Under **Plugins**, find **WorkIQ** from Microsoft ("Find answers across Microsoft 365 emails, meetings, documents, and Teams messages"), and select **Install**.
4. Select **New** and ask:

    +++Check my recent emails about CALD-201. Summarize the open actions, who owns them, and the deadlines.+++

5. If the chat shows **Extension "workiq" needs you to sign in to MCP server "workiq"**, select **Sign in**. Before you sign in, the agent may answer that it can't check your emails. That's expected.
6. A Microsoft Entra sign-in page opens in the browser. Sign in with:

    - **Username**: +++@lab.CloudPortalCredential(User1).Username+++
    - **Temporary Access Pass**: +++@lab.CloudPortalCredential(User1).AccessToken+++

    At the **Enter Temporary Access Pass** screen, enter the pass above and select **Sign in**.

7. Return to the GitHub Copilot app and send the same question again:

    +++Check my recent emails about CALD-201. Summarize the open actions, who owns them, and the deadlines.+++

    Confirm that Work IQ returns a summary of the sample emails. If sign-in still fails or the chat reports that the MCP server is not configured, let a proctor know.

Once you have completed the notebook, select **Next** to continue to **Exercise 4: Foundry IQ**.

===
# Exercise 4: Foundry IQ

Foundry IQ knowledge bases combine knowledge sources, such as search indexes and uploaded files, and use agentic retrieval to plan queries across them and return grounded answers with citations.

Caldova's distribution team needs to decide whether goods can be distributed after the temperature excursion on shipment **SHIP-VC-1026-BOS-FRA**. In Exercise 1, you found public guidance. Now you will query a Foundry IQ knowledge base over Caldova's own documents to investigate what happened and find the final distribution decision.

## Inspect the documents before running code

Foundry IQ knowledge bases run on Azure AI Search. Your search service already has two indexes of Caldova supplier and sourcing documents. Look at what's indexed and compare it with the original files before you build knowledge bases over them.

1. In the Azure portal, search for +++ill344-search+++ in the top search bar and select your AI Search service (it will look like *ill344-search-.....*).
2. Select **Search management > Indexes**. Note the two indexes, **supplier-evidence** and **sourcing-documents**, and their document counts. Each document is a chunk of a source file. If either index is missing or empty, ask a proctor before continuing.
3. Open **supplier-evidence**, then open **Search explorer**. In the search text box, enter +++SHIP-VC-1026-BOS-FRA+++ and select **Search**. Inspect a result's **chunk**, **title**, **blob_path**, and page-number fields.
4. In File Explorer, open **Desktop > aitour-ILL344 > data > caldova > pdfs**. Open **TL-VCL-1026.pdf** and **EXC-VC-1026-04.pdf** in Microsoft Edge. Find the temperature record and the disposition evidence.
5. Finally, open **CAL-POL-PUR-001.pdf** from the same folder and find an approval or escalation rule. Unlike the shipment records, this policy is not in either pre-created index. The notebook will introduce a file knowledge source and upload the policy directly.

**Compare the records:** Follow the shipment identifier from the temperature logger to the investigation report. Find both the initial quarantine status and the final disposition. Keep these records open to check whether the generated answer distinguishes the two stages.

## Build and query the knowledge bases

In the notebook, select **Select Kernel > Python Environments**, and choose the **.venv** environment with the path **.venv\Scripts\python.exe**.

Open **src/notebooks/part4-foundry-iq.ipynb** and follow the notebook **from top to bottom**, running the code cells **in sequence**.

Work through **Steps 1 to 5** to upload the policy and query the policy-only knowledge base. Allow about 40 seconds for file ingestion.

Then work through **Steps 6 to 9** to connect both existing indexes and create **caldova-supply-chain-knowledge-base**. Run the shipment query, then the **activity log** and **references** cells.

> [!Hint] **Troubleshooting:** If code cells get stuck and keep spinning, try these remediation steps:
>
> 1. Select **Restart** from the notebook toolbar at the top. If that doesn't work:
> 2. Select **Developer: Reload Window** from the VS Code command palette. If that doesn't work:
> 3. Close VS Code completely and restart it. Reopen the lab folder and notebook. If cells still get stuck, let a proctor know.

## Verify what you built in the browser

1. Return to your Azure AI Search service. Select **Agentic retrieval > Knowledge bases** and refresh the list.
2. Find **caldova-policy-knowledge-base** and **caldova-supply-chain-knowledge-base**. Inspect their knowledge sources. The first uses the policy file. The second uses that file plus **supplier-evidence-knowledge-source** and **sourcing-documents-knowledge-source**.
3. Select **Agentic retrieval > Knowledge sources**. Compare **file-docs-knowledge-source**, which the service indexed for you from the uploaded policy file, with **supplier-evidence-knowledge-source**, which points to the index you inspected earlier.
4. Compare one cited shipment claim with the PDF you opened. Use the reference's title and page numbers to find the evidence. A **blob_path** is citation metadata and might not be a directly accessible link.

## Use Foundry IQ in the GitHub Copilot app

The knowledge base MCP endpoint uses a Search query key. First find the key in the Azure portal:

1. Go back to the Azure portal in the browser.
2. Search for +++ill344-search+++ in the top search bar, and open the Azure AI Search service in your resource group.
3. Select **Security + networking > Keys**, and locate a key under **Manage query keys**. Keep this page open.

In Visual Studio Code, open the **.env** file in the lab folder and find **FOUNDRY_IQ_MCP_URL**. It points to **caldova-supply-chain-knowledge-base**, which you created in the notebook. Keep the file open. You will switch between the app, Visual Studio Code, and the portal to copy and paste each value when it is needed.

Then add the MCP server:

1. In the GitHub Copilot app, select **Customize**, and then select **Add > MCP Server...**.
2. Enter these values:
    - **Server name**: +++foundry-iq+++
    - **Server type**: HTTP
    - **URL**: switch to Visual Studio Code, copy the complete **FOUNDRY_IQ_MCP_URL** value from **.env**, and switch back to the app to paste it. Copy only the URL after the first **=**, without surrounding quotes.
3. Select **Add header**, and enter the name +++api-key+++. Switch to the Azure portal's **Keys** page, copy a key under **Manage query keys**, and switch back to the app to paste it as the header value.
4. Select **Add server**, and then switch to the **Installed** tab. Under **MCP Servers**, confirm that the server is toggled on and has a green check mark.

Then select **New** and ask:

+++Compare Summit Dose's documented CALD-201 commitments across its Caldova RFP response, agreement amendment, and purchase order.+++

Once you have completed all four notebooks, select **Next** in Skillable to review the summary and next steps.
