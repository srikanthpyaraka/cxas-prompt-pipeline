STAGE 3 — DESIGN & ARCHITECTURE

```artifact:ARCHITECTURE
App: orderbot (1 app)

Router pattern — 1 router + 3 focused sub-agents. Rationale: the three journeys have
distinct tools and risk profiles (returns writes data; FAQ is read-only KB). Splitting
keeps each agent's instructions tight and lets evals target them independently. A single
mega-agent was rejected: mixing a write-capable returns flow with open FAQ raises blast
radius and muddies grounding.

           ┌────────────┐
   user ──▶│  router     │  classifies intent, routes; handles small talk
           └─┬────┬────┬─┘
             ▼    ▼    ▼
   order_status  returns  faq        ── each: goal + instructions + tools + examples
             └────┴────┴──▶ human handoff (out-of-scope / 2 failed attempts / after-hours)

Agents
- order_status_agent — Goal: resolve tracking questions. Tool: get_order_status (OMS read).
  Fallback: no match after 2 turns → handoff. [R1]
- returns_agent — Goal: start an eligible return. Tool: create_return (Returns write).
  Relays API eligibility verbatim; never decides eligibility itself. [R2]
- faq_agent — Goal: answer policy/hours. Tool: search_kb (grounded; no free-generation). [R3]

Tools
- get_order_status(order_id) → {status, eta, carrier}. Auth: OAuth SA. Idempotent (read).
- create_return(order_id, reason) → {rma_id, label_url | ineligible_reason}. Write; needs
  confirmation turn; not retried automatically on ambiguous failure.
- search_kb(query) → top-k passages with sources; answers must cite a passage. [R3]

Guardrails (attached to all agents)
- pii_redaction — redact card#, email, phone in logs; keep order id. [R5]
- pci_block — never echo/store full PAN; mask to last-4. [R6]
- off_topic_refusal — decline out-of-scope, offer handoff. [R4]

Handoff: tier-1 queue 6am–10pm; after-hours → ticket + expectation. [R4]
Non-functionals: p95 ≤ 3s [R8]; en-US, web/mobile-web chat [R9]; KPIs containment ≥ 0.45,
CSAT ≥ 4.2 [R7].
```

```artifact:TRACEABILITY_MATRIX
| Req | Design element(s) | Planned eval type(s) |
|-----|-------------------|----------------------|
| R1 | order_status_agent + get_order_status | Tool Test, Turn Eval, Platform Golden |
| R2 | returns_agent + create_return (confirm turn) | Tool Test (incl. ineligible path), Local Simulation |
| R3 | faq_agent + search_kb (grounded) | Platform Golden, Turn Eval (cited answer) |
| R4 | router + off_topic_refusal + handoff | Local Simulation (out-of-scope), Turn Eval |
| R5 | pii_redaction guardrail | Callback Test, Turn Eval (no PII leak) |
| R6 | pci_block guardrail | Turn Eval (adversarial card#), Callback Test |
| R7 | KPIs on goldens/sims | Platform Golden aggregate (containment, CSAT proxy) |
| R8 | latency budget | latency metric on all eval runs |
| R9 | channel/lang constraint | Local Simulation (locale) |
Coverage: 9/9 = 100%. Gaps: none.
```

Trade-offs: router+sub-agents (chosen) vs. single agent (simpler, higher blast radius) vs.
4 separate apps (over-split, harder to share context). Recommend the router pattern.

SELF-CHECK: pass — every Rn mapped; returns write-path isolated. PAUSE for confirmation.
DECIDED: router + 3 sub-agents. ASSUMED: none new. NEED NEXT: confirm → Stage-4 build.
