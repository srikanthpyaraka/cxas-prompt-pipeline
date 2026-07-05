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
