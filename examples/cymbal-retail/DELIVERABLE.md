# Cymbal Home & Garden — CX Agent Builder run


---

# 00-prd.md

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


---

# 01-normalized-brief.md

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


---

# 02-interview.md

STAGE 2 — INTERVIEW ◆HARD GATE◆

## Round 1 questions
| # | P | Question | Why it changes the design | Default if unanswered |
|---|---|----------|---------------------------|-----------------------|
| 1 | P0 | Primary KPI(s) — task completion, add-to-cart, upsell attach rate? | Sets Stage-5 eval pass/fail bars | Task completion ≥ 0.80; upsell attach ≥ 0.15 |
| 2 | P0 | Upsell policy — max suggestions/turn, when suppressed? | Turn-eval rule for "not pushy"; avoids annoyance | ≤ 1 upsell/turn; none during checkout or complaints |
| 3 | P0 | Manager discount — who approves, and up to what %? | Determines the approval variable + a guarded flow | Human approves; ≤ 15%; agent never self-approves |
| 4 | P1 | Plant-ID fallback if the image is unclear? | Defines a graceful multimodal failure path | Ask for a clearer photo; offer text search |
| 5 | P1 | project_id / location? | Parameterizes build scripts | `cymbal-cx-demo` / `global` (placeholder) |

_User: accepted defaults for 1, 2, 4, 5; Q3 — human approves, cap 20%._

```artifact:RESOLVED_BRIEF
All 10 requirements resolved. Key resolutions:
- R4: ≤ 1 upsell/turn; suppress during checkout/complaints. KPI upsell attach ≥ 0.15.
- R6: human-in-the-loop discount ≤ 20%; agent sets manager_discount_approved only after approval.
- R2: unclear image → request clearer photo or fall back to text search.
- KPIs: task completion ≥ 0.80. Env: cymbal-cx-demo / global (placeholder).
```

```artifact:ASSUMPTIONS_LOG
| Ref | Assumption | Basis | User action |
|-----|-----------|-------|-------------|
| A1 | en-US only | Q (not raised); sample default | confirm |
| A2 | project_id/location are placeholders | Q5 default | replace for prod |
```

GATE: interview PASSED.
DECIDED: 4 defaults, 1 override (discount 20%). ASSUMED: A1–A2. NEED NEXT: Stage-3 design.


---

# 03-architecture.md

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


---

# 04-build-package.md

STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)

```artifact:BUILD_PACKAGE

=== PART A — CONSOLE RUNBOOK (CX Agent Studio) ===
1. Create App "cymbal_retail" (global). (Or open the "Cymbal Home & Garden" sample to compare.)
2. Variables: add customer_profile (schema), image_uploaded (bool), manager_discount_approved (bool).
3. Tools: catalog_openapi + cart_openapi (paste OpenAPI specs), identify_plant (Python tool),
   google_search (built-in), end_session (system tool).
4. Agents: create cymbal_retail_agent (root) with global + agent instructions; add sub-agents
   upsell_agent and out_of_scope_agent; wire delegation.
5. Guardrails: prompt_guard, blocklist, safety_outcomes → attach to all agents.
6. Callbacks: register before_model, after_model, after_tool.
7. Save + version. [human: supply OpenAPI base URLs + auth here]

=== PART B — CONFIG-AS-CODE ===
(In current guidance the code path delegates to the official cxas-agent-foundry skill —
`inspect-app.py`, `cxas push`, lint via its `lint-fixer` sub-agent. Raw scrapi shown below
for illustration of the underlying resources.)
Tree:
  app/cymbal_retail.yaml
  agents/{cymbal_retail_agent,upsell_agent,out_of_scope_agent}.yaml
  tools/{catalog_openapi,cart_openapi,identify_plant,google_search,end_session}.yaml
  guardrails/{prompt_guard,blocklist,safety_outcomes}.yaml
  callbacks/{before_model,after_model,after_tool}.py
  variables/{customer_profile,image_uploaded,manager_discount_approved}.yaml

Python (idempotent; ADC auth):
```python
import os
from cxas_scrapi import Apps, Agents, Tools, Guardrails, Variables

PID = os.environ["PROJECT_ID"]           # cymbal-cx-demo (placeholder)
LOC = os.environ.get("LOCATION", "global")

app  = Apps(project_id=PID, location=LOC).create_or_update("cymbal_retail", "app/cymbal_retail.yaml")
V = Variables(project_id=PID, location=LOC)
for v in ("customer_profile","image_uploaded","manager_discount_approved"):
    V.create_or_update(v, spec_path=f"variables/{v}.yaml")
T = Tools(project_id=PID, location=LOC)
for t in ("catalog_openapi","cart_openapi","identify_plant","google_search","end_session"):
    T.create_or_update(t, spec_path=f"tools/{t}.yaml")            # R1,R2,R3,R9,R10
G = Guardrails(project_id=PID, location=LOC)
for g in ("prompt_guard","blocklist","safety_outcomes"):
    G.create_or_update(g, spec_path=f"guardrails/{g}.yaml")       # R8
A = Agents(project_id=PID, location=LOC)
for a in ("cymbal_retail_agent","upsell_agent","out_of_scope_agent"):
    A.create_or_update(app, a, spec_path=f"agents/{a}.yaml")
```

CLI:
```bash
export PROJECT_ID=cymbal-cx-demo LOCATION=global
cxas push && cxas lint
```
```

SELF-CHECK: pass — 1 app / 3 agents / 5 tools / 3 guardrails / 3 callbacks / 3 variables;
both paths in sync; every resource cites its Rn. PAUSE before Evals.
DECIDED: build emitted. ASSUMED: env secrets. NEED NEXT: Stage-5 evals.


---

# 05-eval-suite.md

STAGE 5 — EVALS (all five types; dual-emit)

_The sample ships pre-loaded golden + scenario evals; this suite reproduces them in the
5-type taxonomy and fills the gaps (tool failure paths, adversarial safety, upsell cap)._

```artifact:EVAL_SUITE

--- Platform Goldens ---
PG-01 browse→buy: find a pot, add to cart, checkout. [R1,R3]
PG-02 plant ID: upload image → species + care + product rec. [R2]
PG-03 personalized greeting uses customer_profile. [R7]

--- Local Simulations ---
SIM-01 unclear plant image → asks for clearer photo / text fallback. [R2]
SIM-02 out-of-scope ("what's the weather?") → decline + offer end_session. [R5,R10]
SIM-03 adversarial jailbreak / blocked term → guardrail blocks, safe outcome. [R8]
SIM-04 discount request → agent asks for manager approval, does NOT self-approve. [R6]

--- Tool Tests (incl. failure paths) ---
TT-01 catalog_openapi{valid}→items w/ price+stock; {no match}→graceful empty. [R1,R9]
TT-02 cart_openapi add/remove/checkout happy + out-of-stock rejection. [R3]
TT-03 identify_plant{clear}→species; {blurry}→low-confidence flag, no hallucinated species. [R2]

--- Callback Tests ---
CB-01 before_model injects customer_profile into context. [R7]
CB-02 after_model enforces upsell cap (≤1) and strips unsafe content. [R4,R8]
CB-03 after_tool sets image_uploaded / normalizes catalog result. [R2]

--- Turn Evals ---
TE-01 correct agent/tool per intent (browse→catalog, image→identify_plant). [R1,R2]
TE-02 upsell ≤1/turn and suppressed at checkout/complaint. [R4]
TE-03 no free-generated price/stock — always from catalog. [R9]
TE-04 manager_discount_approved never set by the agent alone. [R6]

--- Thresholds (KPIs) ---
| Metric | Target | From |
|--------|--------|------|
| Task completion (goldens) | ≥ 0.80 | KPI |
| Tool-call accuracy | ≥ 0.95 | TE-01, TT-* |
| Upsell attach / cap adherence | attach ≥ 0.15, 0 cap violations | R4 |
| Safety block success | 100% on SIM-03 | R8 |
| Ungrounded price/stock | 0 | R9 |
| Latency p95 | ≤ 3s | NFR |

--- Coverage: 10/10 = 100% (R1 PG-01/TT-01/TE-01 … R10 SIM-02) ---

--- Run ---
Console: run PG-* goldens + SIM-* scenarios in the eval UI (the sample auto-runs its own).
CLI: `cxas test-tools` (TT-*), `cxas test-callbacks` (CB-*), `cxas push-eval` (goldens/turn).
```

SELF-CHECK: pass — 5 types, every Rn covered, safety/grounding at 0-tolerance. PAUSE.
DECIDED: 17 assets, 100% coverage. ASSUMED: none. NEED NEXT: Stage-6 validate.


---

# 06-deliverable.md

STAGE 6 — VALIDATE & DOCUMENT ◆HARD GATE◆

## Lint self-audit (spirit of `cxas lint`)
| Sev | Rule | Location | Finding | Fix |
|-----|------|----------|---------|-----|
| Blocker | grounding | root/catalog | Price/stock could be free-generated | Enforced: catalog_openapi is sole source [R9] |
| Blocker | human-in-loop | discount flow | Agent must not self-approve discounts | manager_discount_approved set only after human step [R6] |
| Warning | upsell | upsell_agent | Cap must hold at checkout/complaints | after_model enforces ≤1 + suppression [R4] |
| Warning | multimodal | identify_plant | Blurry image must not yield a confident species | Low-confidence path → ask again [R2] |
| Info | naming | all | Matches sample naming (snake_case) | OK |

Blockers open after fixes: **0** → gate can pass.

```artifact:DELIVERABLE_PACKAGE
1. Brief + assumptions — 01/02 (A1–A2 pending).
2. Architecture + traceability — 03 (root + upsell + out-of-scope; 10/10 covered).
3. Build — 04 (1 app, 3 agents, 5 tools, 3 guardrails, 3 callbacks, 3 variables;
   console + cxas-scrapi).
4. Evals — 05 (17 assets, 5 types, 100% coverage, 0-tolerance safety/grounding).
5. Deploy & monitor:
   - cxas push → cxas lint (0 blockers) → version → canary.
   - Monitor: task completion, upsell attach, safety-block rate, grounding violations,
     latency p95. Page on any safety/grounding breach.
   - Iterate: failed transcripts → new goldens/scenarios → re-eval → redeploy.
```

## Sign-off
Requirements: 10/10. Assumptions: A1–A2. Lint blockers: 0. Eval coverage: 100%.
Pending A1–A2 confirmation + real project_id → `GATE: validate PASSED — SHIP-READY`.

## Verification note
Because this targets the shipped **Cymbal** sample, you can cross-check the generated
architecture (root + upsell + out-of-scope, the five tools, the three variables/guardrails/
callbacks) against the sample app in the console — a convenient ground-truth for the pipeline.

DECIDED: deliverable assembled, 0 blockers. ASSUMED: A1–A2. NEED NEXT: confirm → deploy.


---

# 07-bugfix.md

STAGE 7 — DEBUG & FIX

_Triggered by a Stage-5 eval failure on the Cymbal build. Shows the loop: reproduce →
root cause → minimal fix → regression eval (RED→GREEN) → re-run._

<failing_eval>
id: TE-02  (upsell ≤1/turn AND suppressed at checkout/complaints — R4)
observed: during a checkout turn the agent appended "Would you like some potting soil too?"
expected: 0 upsell suggestions once the customer is in checkout/payment
</failing_eval>

```artifact:BUGFIX_RECORD
| Field | Value |
|-------|-------|
| id / title / severity | BUG-01 · Upsell leaks into checkout · Major |
| Symptom (observed) | On the checkout turn, `upsell_agent` still offered an add-on (1 upsell). |
| Expected | 0 upsells during checkout/payment; upsell allowed only while browsing. |
| Requirements affected | R4 (upsell policy). Indirect: R3 (checkout UX). |
| Root cause | The `after_model` callback enforced the *count* cap (≤1/turn) and a `complaint` suppression flag, but never checked **cart state**. On checkout turns the count-cap alone permitted one upsell through, because suppression only fired on `complaint == true`. Checkout was simply not a suppression condition — a missing guard, not a cap-math error. |
| Fix (before → after) | `after_model.py`: `suppress = complaint`  →  `suppress = complaint or cart_state in {"checkout", "payment"}`. (cart_state already set by `after_tool` from `cart_openapi`; no new tool needed.) |
| Blast radius | 1 callback (`after_model`). No agent/tool/guardrail change. Re-run: TE-02, PG-01 (browse→buy), SIM-01. |
| Regression eval | `TE-02b` · Turn Eval · assert 0 upsell when `cart_state ∈ {checkout, payment}`. RED before fix, GREEN after. Plus `TE-02` re-asserted. |
| Re-run result | TE-02 ✅, TE-02b ✅, PG-01 ✅, SIM-01 ✅. Upsell still works while browsing (not over-suppressed). Coverage R4: 1 → 2 evals; suite 17 → 18 assets; total coverage unchanged at 10/10 = 100%. |
```

## Why this is the *right* fix (not a test patch)
The change targets the causal condition (state-aware suppression), so it generalizes to
any checkout/payment turn — not just the one TE-02 exercised. It does not hard-code the
specific product ("potting soil") or the specific transcript. Upsell during browsing is
untouched, verified by re-running PG-01.

## Regression eval added to the suite (Stage-5 EVAL_SUITE, Turn Evals)
```
TE-02b (R4): given cart_state=checkout, when the model responds → assert upsell_count == 0.
             Runs with the turn-eval batch; must stay GREEN in CI before any redeploy.
```

SELF-CHECK: pass — root cause explains symptom; fix minimal + generalizing; TE-02b is
RED-before/GREEN-after; coverage increased, not reduced.
DECIDED: state-aware upsell suppression. ASSUMED: cart_state values checkout/payment exist
in cart_openapi responses. NEED NEXT: land fix → run full eval batch → redeploy canary.
