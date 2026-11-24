===
# Summary

Across four exercises, you gave agents Caldova context with Microsoft IQ: Web IQ for public guidance, Fabric IQ for structured supplier data, Work IQ for your Microsoft 365 work, and a Foundry IQ knowledge base over Caldova's documents. You inspected the original data, not just generated answers.

## What changed at each step

| Part | What you built | What you explored |
| --- | --- | --- |
| 1 | An MCP session to Web IQ with web, image, and video search | Compared a cited web passage with its source page and noted what the web cannot answer |
| 2 | An ontology query over MCP and a Fabric data agent that you created and published | Traced a substance-to-product relationship and compared a supplier trend with the lakehouse rows |
| 3 | Work IQ reads, evidence retrieval, a decision meeting, and a follow-up with the approved purchase order | Matched synthesized claims to retrieved passages and kept email updates distinct from the purchase order |
| 4 | A policy file source, two indexed sources, and knowledge bases with answer synthesis | Compared a shipment claim with its PDF and citation metadata |

## Continue learning

- [Microsoft Web IQ documentation](https://learn.microsoft.com/web-iq/) - Learn about the Web IQ APIs, passages, and the MCP server.
- [What is Fabric IQ?](https://learn.microsoft.com/fabric/iq/overview) - Explore ontologies, data agents, and the other Fabric IQ capabilities.
- [Work IQ MCP tool reference](https://learn.microsoft.com/microsoft-365/copilot/extensibility/work-iq/mcp/tool-reference) - Review every Work IQ tool, including `retrieve`, `discover`, and `fetch_blob`.
- [Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/) - Explore the full capabilities of Foundry IQ (Azure AI Search) and how it integrates with other Azure services.
- [Create a knowledge base in Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/agentic-retrieval-how-to-create-knowledge-base) - Step-by-step guide to creating and configuring knowledge bases.
- [Create a knowledge source](https://learn.microsoft.com/azure/search/search-knowledge-source-overview) - Understand how to create and configure different data sources, including Fabric IQ, Work IQ, and Web IQ knowledge sources.
- [Use answer synthesis for citation-backed responses in Foundry IQ (Azure AI Search)](https://learn.microsoft.com/azure/search/search-agentic-retrieval-how-to-synthesize) - Learn how to generate grounded answers with citations using answer synthesis.

## Next steps

Here are some ways to apply what you've learned:

**Combine the IQs in one knowledge base** - Add Fabric IQ, Work IQ, and Web IQ as knowledge sources alongside the indexed documents, so agentic retrieval can plan across all of them.

**Query from more MCP clients** - Connect the Web IQ, Fabric IQ, Work IQ, and knowledge base MCP endpoints to compatible clients such as GitHub Copilot CLI.

**Customize retrieval behavior** - Adjust reasoning effort levels and configure custom retrieval and answer instructions for specific sources.

**Integrate with your data** - Replace the sample Caldova policy, procurement records, and supplier analytics with enterprise content you are authorized to use.

The patterns you explored in this lab form the foundation for building agents that combine public web content, structured business data, workplace context, and indexed enterprise documents.
