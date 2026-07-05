# PRD — "OrderBot" (AcmeShop customer support agent)

_Sample input. Deliberately imperfect: some things are specified, some are vague — that's
what the Ingest + Interview stages are for._

## Background
AcmeShop is a mid-size online retailer. Tier-1 support is overwhelmed by repetitive
"where's my order" and "how do I return this" contacts. We want a chat agent, "OrderBot,"
on the website to handle these and hand off everything else to a human.

## Goals
- Deflect a large share of tier-1 contacts (target ~45%).
- Faster answers than the current 8-minute average wait.
- Don't make customers angrier — escalate cleanly when the bot can't help.

## In scope
1. Order status ("where is my order", tracking).
2. Returns and refunds — start a return for an eligible order.
3. Store/policy FAQs (hours, return window, shipping fees).

## Out of scope
- Payment changes, account/password issues, anything not above → human.

## Systems we have
- OMS REST API (read order + tracking). Returns/RMA API (can create a return).
- A help-center knowledge base for FAQs.

## Constraints / notes
- Web chat, English (US). Mobile web matters.
- We're in retail — cards are involved. Legal says don't mishandle card data.
- Should be fast.
- Launch on GCP. Someone mentioned "cxas-scrapi" for building/testing.
