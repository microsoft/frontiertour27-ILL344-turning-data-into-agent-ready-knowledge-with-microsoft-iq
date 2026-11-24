<a name="start-building"></a>

<p align="center">
<img src="img/banner-frontier-tour-27.png" alt="Microsoft Frontier Tour 2027" width="100%"/>
</p>

# [Microsoft Frontier Tour 2027](https://aitour.microsoft.com)

## 🔥 ILL344: Turning data into agent-ready knowledge with Microsoft IQ

### Session description

Give agents context with Microsoft IQ. Use Web IQ to ground answers in current web content, Fabric IQ to query structured data in OneLake through an ontology and a data agent, and Work IQ to read and act on Microsoft 365 work context. Then build a Foundry IQ knowledge base with agentic retrieval over enterprise documents. At every step, check which source supports each claim.

### 🚀 Getting started

#### In a guided session

If you're following along during a live session:

1. Open the lab environment and sign in with the provided credentials.
2. Follow the setup guidance in [`instructions/overview.md`](instructions/overview.md).
3. Keep the [guided exercises](instructions/overview.md#exercise-1-ground-answers-in-the-web-with-web-iq) open alongside [`src/notebooks/`](src/notebooks/). In each exercise, inspect the source in the browser, run the notebook, and verify the evidence before continuing.

#### On your own

If you're learning at your own pace:

1. Clone this repository.
2. Provision the required resources by following the [self-deployment guide](deploy_yourself.md).
3. Follow the exercises in [`instructions/overview.md`](instructions/overview.md#exercise-1-ground-answers-in-the-web-with-web-iq) alongside all four notebooks in [`src/notebooks/`](src/notebooks/). Use your own deployment settings and note the differences for sample emails in the guide.

### 🎯 Learning outcomes

By the end of this session, you will be able to:

- Ground answers in current web content by calling Web IQ through Model Context Protocol (MCP).
- Query structured business data with a Fabric IQ ontology, and create and publish a Fabric data agent for analytical questions.
- Use Work IQ tools to ask, retrieve, discover, read, and act on Microsoft 365 work context as the signed-in user.
- Build a multi-source knowledge base over indexed enterprise content using Foundry IQ (Azure AI Search) agentic retrieval.

### 💻 Technologies used

- Microsoft Web IQ
- Microsoft Fabric IQ (ontology and data agent)
- Work IQ
- Foundry IQ (Azure AI Search)
- Azure OpenAI (`gpt-5.4` and `text-embedding-3-large`)
- Model Context Protocol (MCP)
- Python and Jupyter Notebooks

### 📚 Continue your learning

Pick your next step based on your learning style:

| Resource | What you'll get |
|----------|-----------------|
| **[Session Recording](https://aka.ms/ft27/ill344/youtube)** | A recording of session ILL344 by the session creator |
| **[English](https://aka.ms/ft27/ill344/slides/en)** \| **[Spanish](https://aka.ms/ft27/ill344/slides/es)** | Session slides for ILL344 |
| **[Foundry IQ (Azure AI Search) documentation](https://learn.microsoft.com/azure/search/)** | Explore the full capabilities of Foundry IQ (Azure AI Search) |
| **[Create a knowledge base](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base)** | Follow the steps to create and configure a knowledge base |
| **[Design an index for agentic retrieval](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-index)** | Learn best practices for structuring data for agentic retrieval |
| **[Microsoft Learn](https://learn.microsoft.com)** | Official documentation and guided learning paths on these topics |
| **[Frontier Tour 2027 Resource Center](https://aka.ms/FrontierTour27)** | Additional session repos and materials from Frontier Tour 2027 |
| **[Microsoft Foundry Community](https://aka.ms/MicrosoftFoundryDiscord-ft27)** | Connect with other learners and experts in our Discord community |

### 🌟 Microsoft Learn MCP Server

<!-- Remove this section if the Microsoft Learn MCP Server is not relevant to the session. -->

The Microsoft Learn MCP Server gives your AI agent direct access to Microsoft's official documentation — grounded, up-to-date answers about the topics in this session.

**GitHub Copilot CLI** — Install with:

```shell
copilot plugin install microsoftdocs/mcp
```

**VS Code** — One-click install:  
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Learn_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft-learn&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D)

For more information, visit the [Learn MCP Server repo](https://aka.ms/learnmcp).

### 👥 Content owners

<table>
<tr>
    <td align="center"><a href="https://github.com/pamelafox">
        <img src="https://github.com/pamelafox.png" width="100px;" alt="Pamela Fox"/><br />
        <sub><b>Pamela Fox</b></sub></a><br />
            <a href="https://github.com/pamelafox" title="talk">📢</a>
    </td>
    <td align="center"><a href="https://github.com/aycabas">
        <img src="https://github.com/aycabas.png" width="100px;" alt="Ayca Bas"/><br />
        <sub><b>Ayca Bas</b></sub></a><br />
            <a href="https://github.com/aycabas" title="talk">📢</a>
    </td>
</tr></table>

### Deliver this session

Presenters and re-delivery partners can find the deck, recordings, presenter
notes, and delivery guidance in [`delivery-resources/`](delivery-resources/README.md).

### ⚖️ Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.

Any use of third-party trademarks or logos are subject to those third-party's policies.
