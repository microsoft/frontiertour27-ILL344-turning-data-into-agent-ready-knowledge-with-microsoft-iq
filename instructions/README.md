
# ILL344: Turning data into agent-ready knowledge with Microsoft IQ

These instructions are for participants of the **instructor-led lab** **ILL344: Turning data into agent-ready knowledge with Microsoft IQ** at Microsoft AI Tour.

## Lab overview

You are a Caldova procurement analyst investigating supplier risk. Give agents context with Microsoft IQ: find public guidance with Web IQ, query structured supplier data with Fabric IQ, read and act on your Microsoft 365 work with Work IQ, and build a Foundry IQ knowledge base over policy and document evidence. At every stage, verify which source supports the answer.

Follow the [guided lab instructions](overview.md). Each exercise follows **inspect in the browser > run the notebook > verify the evidence**, then adds the same IQ to the GitHub Copilot app as an MCP server. The browser activities are part of the lab, not just environment setup.

## Prerequisites

To get the most out of this lab, you should have a basic understanding of the following:

- **Python and Jupyter Notebooks** – You will write and run code cells directly inside a Jupyter environment.  
- **Azure Fundamentals** – Familiarity with Azure services and concepts such as resource groups, storage accounts, and authentication.  
- **Retrieval-Augmented Generation (RAG)** – A general understanding of how LLMs use external data for grounding will help you better follow the agentic retrieval flow.  
- **Foundry IQ (Azure AI Search) and OpenAI** – Basic knowledge of what these services do (indexing, querying, embeddings, completions) is helpful but not required.

> [!NOTE]  
> You do **not** need to provision any Azure services or deploy infrastructure manually for this lab. All required resources including Foundry IQ (Azure AI Search), OpenAI deployments, and data sources — are pre-created and ready to use.

## Get started

Start with the [environment setup](overview.md#sign-in-to-windows), then keep the guide open alongside Visual Studio Code:

| Exercise | Browser activity | Notebook |
| --- | --- | --- |
| [1. Web IQ](overview.md#exercise-1-ground-answers-in-the-web-with-web-iq) | Create a Web IQ API key and check a cited web passage on its source page | [part1-web-iq.ipynb](../src/notebooks/part1-web-iq.ipynb) |
| [2. Fabric IQ](overview.md#exercise-2-query-structured-data-with-fabric-iq) | Explore lakehouse tables, the Fabric ontology, and the data agent | [part2-fabric-iq.ipynb](../src/notebooks/part2-fabric-iq.ipynb) |
| [3. Work IQ](overview.md#exercise-3-bring-in-work-context-with-work-iq) | Read the seeded Outlook emails and the approved purchase order, then check each write in Outlook | [part3-work-iq.ipynb](../src/notebooks/part3-work-iq.ipynb) |
| [4. Foundry IQ](overview.md#exercise-4-build-a-knowledge-base-with-foundry-iq) | Inspect PDFs, Search explorer results, and created knowledge bases | [part4-foundry-iq.ipynb](../src/notebooks/part4-foundry-iq.ipynb) |

Each notebook stands on its own, but the exercises follow one Caldova investigation, so run them in order. After all four exercises, continue to the [summary](summary.md).

## Publishing to Skillable

Use **overview.md** for setup and the four exercises, followed by **summary.md** for the wrap-up. Preserve the `===` separators, which start new sidebar pages, and the existing lab credential tokens. The notebooks link back to the same guide for learners outside Skillable.

## Discussions

If you’d like to contribute, raise an issue, or provide feedback, please open an issue in this repo.

If you enjoyed this workshop, consider giving the repository a ⭐ on GitHub and sharing it with your peers or community.

## Source Code

The source code for this session is available in the [notebooks folder](../src/notebooks) of this repository.  
You can use it as a reference for future projects, extend it with additional capabilities, or integrate it into your own solutions built on Foundry IQ (Azure AI Search) and agentic retrieval.
