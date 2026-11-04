===
# Summary

Across five exercises, you investigated Caldova supplier questions with Foundry IQ, added Fabric IQ and Work IQ, and connected a Microsoft Agent Framework agent through MCP. You inspected the original data, not just generated answers.

## What changed at each step

| Part | What you built | How you checked it |
| --- | --- | --- |
| 1 | A policy file source, two indexed sources, and knowledge bases with answer synthesis | Compared a shipment claim with its PDF and citation metadata |
| 2 | A knowledge base adding Fabric IQ to the Part 1 sources | Traced a substance-to-product relationship through Fabric tables and `fabricRawData` |
| 3 | A knowledge base adding Work IQ to the Part 1 sources | Compared recent Outlook messages with approved sourcing commitments |
| 4 | A five-source briefing knowledge base | Matched claims to sources and challenged an unsupported relationship |
| 5 | An extractive knowledge base over the Part 1 sources and an agent using MCP | Inspected the retrieval tool call and compared the agent's conclusion with the original evidence |

## Review your results

Before you finish, revisit these results:

1. In Part 1, find the index connected by each indexed knowledge source and the knowledge base that brings those sources together.
2. Compare the delivery email with the purchase order and check that your answer preserves their different roles.
3. Trace the substance-to-product relationship in Fabric and match it to the returned structured evidence.
4. Compare the answer-synthesis knowledge base in Part 1 with the extractive knowledge base and agent model in Part 5.

If you cannot point to supporting evidence, treat the claim as unverified. A knowledge base having a source configured is not proof that the source supported a particular answer.

## Continue learning

- [Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/) - Explore the full capabilities of Foundry IQ (Azure AI Search) and how it integrates with other Azure services.
- [Design an index for agentic retrieval in Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/search-agentic-retrieval-how-to-index) - Best practices for structuring your data for agentic retrieval.
- [Create a knowledge base in Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/search-agentic-retrieval-how-to-create?tabs=rbac%2Cpython-get-agents%2Cpython-create-agent%2Cpython-query-agent%2Cpython-delete-agent) - Step-by-step guide to creating and configuring knowledge bases.
- [Create a knowledge source](https://learn.microsoft.com/azure/search/search-knowledge-source-overview) - Understand how to create and configure different data sources.
- [Use answer synthesis for citation-backed responses in Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/search-agentic-retrieval-how-to-synthesize) - Learn how to generate grounded answers with citations using answer synthesis.

## Next steps

Here are some ways to apply what you've learned:

**Query from more MCP clients** - Connect the knowledge base MCP endpoint to compatible clients such as GitHub Copilot CLI.

**Customize retrieval behavior** - Adjust reasoning effort levels, configure custom retrieval and answer instructions for specific sources.

**Integrate with your data** - Replace the sample Caldova policy and procurement records with enterprise content you are authorized to use.

**Build a conversational interface** - Extend the notebook's Microsoft Agent Framework agent with additional tools and a chat UI for end users.

The patterns you explored in this lab form the foundation for building custom copilots, enterprise assistants, and intelligent knowledge applications that combine indexed enterprise data with structured and workplace context.
