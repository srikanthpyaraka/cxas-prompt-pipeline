STAGE 1 — INGEST

```artifact:NORMALIZED_BRIEF
| Field | Value |
|-------|-------|
| Business goal | Self-serve shopping assistant for Cymbal Home & Garden; larger baskets via upsell |
| Success metrics | ❓UNKNOWN — no KPI stated (propose: task-completion, add-to-cart rate, upsell attach) |
| Users / channels | Cymbal web + app shoppers; chat + image upload (multimodal) |
| Languages / volume | ❓UNKNOWN (assume en-US) |
| In-scope journeys | Product selection; plant ID from image; cart mgmt/checkout; upsell; manager discount |
| Out of scope | Non-shopping topics → dedicated out-of-scope sub-agent |
| Backend systems | OpenAPI catalog/cart endpoints; Google Search; customer profile store |
| Data / safety | Prompt guards, blocklists, safety outcomes required; ❓UNKNOWN PII policy |
| Variables | customer_profile (schema); image_uploaded (bool); manager_discount_approved (bool) |
| Environment | GCP; cxas-scrapi; ❓UNKNOWN project_id / location |
```

```json
[
 {"id":"R1","text":"Browse/select products from the Cymbal catalog","type":"functional","priority":"P0","status":"known","source":"PRD 1"},
 {"id":"R2","text":"Identify a plant from an uploaded image; recommend care/products","type":"functional","priority":"P0","status":"known","source":"PRD 2"},
 {"id":"R3","text":"Manage cart: add/remove/checkout","type":"functional","priority":"P0","status":"known","source":"PRD 3"},
 {"id":"R4","text":"Upsell relevant items without being pushy","type":"functional","priority":"P1","status":"known","source":"PRD 4"},
 {"id":"R5","text":"Route non-shopping topics to an out-of-scope handler","type":"functional","priority":"P0","status":"known","source":"PRD out-of-scope"},
 {"id":"R6","text":"Support manager discount approval flow","type":"functional","priority":"P1","status":"known","source":"PRD 5"},
 {"id":"R7","text":"Personalize using customer_profile variable","type":"functional","priority":"P1","status":"known","source":"PRD goals + variables"},
 {"id":"R8","text":"Guardrails: prompt guards, blocklists, safety outcomes","type":"guardrail","priority":"P0","status":"known","source":"PRD constraints"},
 {"id":"R9","text":"Ground answers via OpenAPI catalog + Google Search (no free-generated stock/price)","type":"guardrail","priority":"P0","status":"known","source":"PRD systems"},
 {"id":"R10","text":"Clean session end (end_session system tool)","type":"nonfunctional","priority":"P1","status":"assumed","source":"inferred from sample"}
]
```

Summary: 10 requirements (P0: 6, P1: 4). UNKNOWNs: KPIs, language, volume, PII policy, env.
Top risk: no success metric defined — evals need targets.

SELF-CHECK: pass. DECIDED: 10 requirements. ASSUMED: en-US, R10. NEED NEXT: interview on KPIs + env.
