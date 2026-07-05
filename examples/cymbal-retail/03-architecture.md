STAGE 3 — DESIGN & ARCHITECTURE

_Mirrors the real Studio sample's structure so the build is verifiable against it._

```artifact:ARCHITECTURE
App: cymbal_retail (1 app)

Multi-agent (root + 2 sub-agents) — matches the sample:
           ┌───────────────────────┐
   user ──▶│ cymbal_retail_agent   │  root: browse, plant ID, cart, personalization
           └───┬───────────────┬───┘
               ▼               ▼
          upsell_agent    out_of_scope_agent
     (relevant add-ons)   (declines non-shopping, ends politely)

Agents
- cymbal_retail_agent (root) — Goal: help select products, ID plants, manage cart, using
  customer_profile for personalization. Delegates to sub-agents. [R1,R2,R3,R7]
- upsell_agent — Goal: suggest ≤1 relevant add-on/turn; suppressed at checkout/complaints. [R4]
- out_of_scope_agent — Goal: politely decline non-shopping asks; end_session if nothing else. [R5,R10]

Tools
- catalog_openapi (OpenAPI) — search products, price, stock. Grounds all product claims. [R1,R9]
- cart_openapi (OpenAPI) — add/remove/checkout (write; confirm before checkout). [R3]
- identify_plant (Python tool) — takes uploaded image → species + care; unclear → ask again. [R2]
- google_search — general horticulture/care questions not in catalog. [R2,R9]
- end_session (system tool) — clean close. [R10]

Variables
- customer_profile (schema) [R7]; image_uploaded (bool) [R2]; manager_discount_approved (bool) [R6]

Guardrails (all agents)
- prompt_guard (jailbreak/off-policy), blocklist (banned terms), safety_outcomes. [R8]
- grounding rule: no free-generated price/stock — must come from catalog_openapi. [R9]

Callbacks
- before_model (inject profile/context), after_model (enforce upsell cap + safety),
  after_tool (normalize catalog/cart results, set flags). [R4,R6,R8]

Discount flow: agent requests approval → human sets manager_discount_approved=true (≤20%)
→ only then apply. Agent never self-approves. [R6]
```

```artifact:TRACEABILITY_MATRIX
| Req | Design element(s) | Planned eval type(s) |
|-----|-------------------|----------------------|
| R1 | root + catalog_openapi | Tool Test, Platform Golden |
| R2 | identify_plant + image_uploaded + google_search | Local Simulation (image), Tool Test |
| R3 | cart_openapi (confirm turn) | Tool Test (incl. checkout), Turn Eval |
| R4 | upsell_agent + after_model cap | Turn Eval (≤1, suppressed contexts) |
| R5 | out_of_scope_agent | Local Simulation, Turn Eval |
| R6 | manager_discount_approved + human step | Callback Test, Turn Eval (no self-approve) |
| R7 | customer_profile + before_model | Platform Golden (personalized) |
| R8 | prompt_guard, blocklist, safety_outcomes | Callback Test, Turn Eval (adversarial) |
| R9 | grounding rule on catalog | Turn Eval (no ungrounded price/stock) |
| R10 | end_session | Local Simulation (session close) |
Coverage: 10/10 = 100%.
```

Trade-off: matched the sample's root+2-subagent shape (proven, evaluable) rather than
collapsing to one agent (weaker upsell control) or splitting further (needless overhead).

SELF-CHECK: pass. PAUSE for confirmation.
DECIDED: root + upsell + out-of-scope. ASSUMED: none new. NEED NEXT: Stage-4 build.
