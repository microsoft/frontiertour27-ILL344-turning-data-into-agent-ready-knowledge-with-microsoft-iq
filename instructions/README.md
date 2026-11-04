
# ILL344: Turning data into agent-ready knowledge with Microsoft IQ

These instructions are for participants of the **instructor-led lab** **ILL344: Turning data into agent-ready knowledge with Microsoft IQ** at Microsoft AI Tour.

## Lab overview

You are a Caldova procurement analyst investigating supplier risk. Build Foundry IQ knowledge bases over policy and document evidence, add Fabric IQ relationships and Work IQ workplace context, then connect a Microsoft Agent Framework agent. At every stage, verify which source supports the answer.

Follow the [guided lab instructions](overview.md). Each exercise follows **inspect in the browser > run the notebook > verify the evidence**. The browser activities are part of the lab, not just environment setup.

## Prerequisites

To get the most out of this lab, you should have a basic understanding of the following:

- **Python and Jupyter Notebooks** – You will write and run code cells directly inside a Jupyter environment.  
- **Azure Fundamentals** – Familiarity with Azure services and concepts such as resource groups, storage accounts, and authentication.  
- **Retrieval-Augmented Generation (RAG)** – A general understanding of how LLMs use external data for grounding will help you better follow the agentic retrieval flow.  
- **Foundry IQ (Azure AI Search) and OpenAI** – Basic knowledge of what these services do (indexing, querying, embeddings, completions) is helpful but not required.

> [!NOTE]  
> You do **not** need to provision any Azure services or deploy infrastructure manually for this lab. All required resources including Foundry IQ (Azure AI Search), OpenAI deployments, and data sources — are pre-created and ready to use.

## Get started

Start with the [environment setup](overview.md#getting-started), then keep the guide open alongside Visual Studio Code:

| Exercise | Browser activity | Notebook |
| --- | --- | --- |
| [1. Foundry IQ knowledge bases](overview.md#exercise-1-build-foundry-iq-knowledge-bases-with-agentic-retrieval) | Inspect PDFs, Search explorer results, and created knowledge bases | [part1-standard-foundry-iq-kb.ipynb](../src/notebooks/part1-standard-foundry-iq-kb.ipynb) |
| [2. Fabric IQ](overview.md#exercise-2-add-structured-data-from-fabric-iq) | Explore lakehouse tables and the Fabric ontology | [part2-fabric-iq-to-kb.ipynb](../src/notebooks/part2-fabric-iq-to-kb.ipynb) |
| [3. Work IQ](overview.md#exercise-3-add-workplace-context-from-work-iq) | Read the seeded Outlook emails and an approved purchase order | [part3-work-iq-to-kb.ipynb](../src/notebooks/part3-work-iq-to-kb.ipynb) |
| [4. Work IQ and Fabric IQ](overview.md#exercise-4-combine-work-iq-and-fabric-iq) | Inspect the combined knowledge base and verify claims in source systems | [part4-work-iq-fabric-iq-to-kb.ipynb](../src/notebooks/part4-work-iq-fabric-iq-to-kb.ipynb) |
| [5. Microsoft Agent Framework](overview.md#exercise-5-build-an-agent-with-microsoft-agent-framework) | Compare knowledge base configurations and check the shipment evidence | [part5-agent-framework-mcp.ipynb](../src/notebooks/part5-agent-framework-mcp.ipynb) |

Complete Part 1 before the later notebooks, which reuse its policy file source. After all five exercises, continue to the [summary](summary.md).

## Publishing to Skillable

Use **overview.md** for setup and the five exercises, followed by **summary.md** for the wrap-up. Preserve the `===` separators, which start new sidebar pages, and the existing lab credential tokens. The notebooks link back to the same guide for learners outside Skillable.

## Discussions

If you’d like to contribute, raise an issue, or provide feedback, please open an issue in this repo.

If you enjoyed this workshop, consider giving the repository a ⭐ on GitHub and sharing it with your peers or community.

## Source Code

The source code for this session is available in the [notebooks folder](../src/notebooks) of this repository.  
You can use it as a reference for future projects, extend it with additional capabilities, or integrate it into your own solutions built on Foundry IQ (Azure AI Search) and agentic retrieval.
