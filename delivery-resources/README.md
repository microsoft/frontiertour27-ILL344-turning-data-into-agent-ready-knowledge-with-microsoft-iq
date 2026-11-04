# Delivery resources

Presenter, re-delivery, and train-the-trainer materials for this session.

## Core materials

| Item | Link | Notes |
|---|---|---|
| Delivery deck | [English](https://aka.ms/ft27/ill344/slides/en) \| [Spanish](https://aka.ms/ft27/ill344/slides/es) | Session slides |
| Session recording | [ILL334 Recording](https://aka.ms/ft27/ill344/youtube) | Video of presenation|
| Attendee landing page | [Session README](../README.md) | Public starting point |
| Workshop/lab instructions | [Instructions](../instructions/README.md) | Remove this row when not applicable |

## Delivery checklist

- Review the session README
- Review the attendee instructions
- Open the deck
- Review the presenter guidance below
- Review live demo reproducibility guidance
- Validate any required environment or setup

## Session preparation

- Review the attendee entry point from the root README.
- Review the delivery deck.
- Validate the required environment and setup.

## Run of show

This flow was used for Frontier Tour Singapore and is planned for Frontier Tour London. Customize it for your own session while preserving time for attendees to work through the lab.

Use this proposed pacing for a 60-minute session. Rehearse it in the event environment before delivery. Sign-in and retrieval latency can reduce working time.

| Minutes | Activity | Understanding check |
| --- | --- | --- |
| 0 to 8 | Introduce the Caldova decision and draw the roles of documents, Fabric IQ, and Work IQ | Ask which system can prove an approved commitment versus a current action |
| 8 to 13 | Sign in, open **Desktop > aitour-ILL344**, choose the notebook kernel, and verify the indexes | Everyone can find the data they will query |
| 13 to 26 | Exercise 1, including PDFs, Search explorer, and the first knowledge bases | Attendees point to evidence for their shipment conclusion |
| 26 to 35 | Exercise 2, including the Fabric tables and ontology | Attendees distinguish a document fact from a structured relationship |
| 35 to 44 | Exercise 3, including the three Outlook messages | Attendees distinguish the planning update from the purchase order |
| 44 to 51 | Exercise 4 and the claim-to-source table | Attendees challenge the unsupported Summit Dose manufacturing link |
| 51 to 57 | Exercise 5 and the retrieval tool-call table | Attendees explain whether the knowledge base or the agent synthesizes the answer |
| 57 to 60 | Teach-back and wrap-up | Use the four questions in the [summary](../instructions/summary.md#explain-it-back) |

Keep the GitHub Copilot app bonus and extra questions optional. If the group falls behind, walk through the remaining exercises together and leave their individual completion for self-paced follow-up. Do not skip Part 1's source creation or describe a walkthrough as completed hands-on work.

## Facilitation guidance

Use the PREL42 pattern of exploring the source in a browser before querying it. In this lab, pair that exploration with a prediction and a concrete evidence check.

- **Show one complete loop before independent work.** Open a shipment PDF, inspect its indexed chunk, run a query, and trace a claim to its reference. Explain what each surface contributes.
- **Pause at the exercise checkpoints.** Ask attendees to explain the result to a neighbor or name the supporting source. Avoid asking only whether their cells ran successfully.
- **Use wait time for investigation.** While Fabric IQ or Work IQ retrieves, have attendees inspect the table relationship or compare the email with the purchase order. Do not encourage repeated query submissions.
- **Make source boundaries visible.** Keep the four-row claim-to-source table from Exercise 4 on screen. Distinguish a missing source result from an unsupported model conclusion.
- **Keep the browser work read-only.** Learners inspect existing Fabric items and notebook-created knowledge bases. They do not edit the ontology, recreate resources, or deploy an agent.

Before the session, verify the hosted account can open Search explorer, the **CaldovaSupplyChain-** workspace, **CaldovaSupplierAnalytics**, **CaldovaMedicinalProductOntology**, and the three **CALD-201** emails in Outlook. Confirm the notebook-created knowledge bases can be inspected in the portal. Preview source or model configuration might not render in the portal, so rehearse the notebook-definition fallback in Exercise 1.

The lab's fifth exercise runs an agent inside a notebook over the three Part 1 sources. It does not deploy a Foundry Hosted Agent and does not use the combined five-source knowledge base.

## Demo reproducibility

If the session includes live demos, link to or include the steps, code, setup,
and notes required to reproduce them.

## Setup notes

At the tech check the day before your session, the event team will provide the location-specific link attendees need to start the lab. Add a slide to your presentation showing that link, and display it when transitioning to the Skillable environment.

Use the [lab instructions](../instructions/overview.md) for sign-in guidance, environment pre-checks, and the notebook sequence.

## Support

Content owner or contact:
