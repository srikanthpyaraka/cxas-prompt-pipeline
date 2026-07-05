# PRD — Cymbal Home & Garden retail assistant

_Reverse-engineered from CX Agent Studio's default **sample agent** (`cymbal_retail_agent`,
"Cymbal Home & Garden"), so the pipeline can be tried against a real, known-good Studio
build. Source: CX Agent Studio → Build → Sample agents (as of Nov 2025)._

## Background
Cymbal Home & Garden is a fictional retailer. We want a customer-facing web/app assistant
that helps shoppers find products, identify plants from photos they upload, and complete a
purchase — while upselling tastefully and handing off anything off-topic.

## Goals
- Help customers browse and select products from the Cymbal catalog.
- Identify a plant from a customer-uploaded image and recommend care/products.
- Manage the shopping cart end to end (add, remove, checkout).
- Increase basket size via relevant upsell — without being pushy.
- Personalize using the customer's profile.

## In scope
1. Product selection / browsing.  2. Plant identification from an uploaded image.
3. Cart management + checkout.     4. Upsell suggestions.  5. Manager discount approval.

## Out of scope
- Anything not retail-shopping related → a dedicated out-of-scope handler.

## Systems / data
- Product catalog + cart via OpenAPI endpoints. General lookups via Google Search.
- Customer profile (structured). Flags for "image uploaded" and "manager discount approved."

## Constraints
- Multimodal (image upload). Safety: prompt guards, blocklists, safety outcomes required.
- Launch on GCP; build/test with cxas-scrapi.
