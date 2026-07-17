# STAGE 6 — VALIDATE & DOCUMENT  ◆HARD GATE◆
Input: all prior artifacts. Goal: self-audit, assemble the deliverable, and get sign-off.
You may not declare SHIP-READY until blockers are cleared AND the user confirms.

## Lint audit — run the real linter, don't simulate it
**Prefer running the actual `cxas lint`** via cxas-agent-foundry's `lint-fixer` sub-agent and
parse its findings — that's the real 60+ rules, not an approximation. Only if the tool isn't
available, fall back to the manual review below. Either way, report findings by severity
(Blocker / Warning / Info) across at least:
- Naming & structure hygiene; resource references resolve.
- Grounding: no free-generated facts; KB/tool routing present.
- Guardrail coverage: PII, off-topic/refusal, grounding on every agent.
- Instruction clarity: no ambiguous/conflicting playbook instructions.
- Tool schema hygiene: I/O typed, auth defined, failure handled, idempotent.
- Fallback + human-handoff present on every agent.
- Eval coverage = 100%; thresholds tied to KPIs.
For each finding: rule, location, severity, and the fix. Apply fixes or list required
user actions. **Blockers must be 0 to pass the gate.**

## DELIVERABLE_PACKAGE (assemble & emit)
1. Normalized/Resolved Brief + `ASSUMPTIONS_LOG`
2. Architecture doc + `TRACEABILITY_MATRIX`
3. Build config tree + create/update scripts + console runbook
4. Eval suite + thresholds + run commands + coverage report
5. Deploy runbook + monitoring/KPI dashboard plan + iteration loop (how feedback →
   new goldens/examples → re-eval → redeploy)

## Verify it's REAL before sign-off (not just narrated)
Before claiming ship-ready, prove the build actually exists — this is where testers got
burned ("no such app", "eval files only in logs"):
- **Files on disk:** `find cxbuild/<app> -type f` shows app.json + every agent/tool/instruction
  /callback + every `evals/**/*.yaml`. Report the count.
- **App on-platform:** `cxas apps list --project-id <pid> --location <loc>` shows the app by
  display name with a resource id. If it's absent, the app was never created — go create/push it.
- **Evals on-platform:** confirm `cxas push-eval` succeeded for the goldens.
- **Layout sanity:** `python3 scripts/smoke-test.py --pull-dir cxbuild/<app>/cxas_app/<App> --layout-only`.

## Gate & sign-off
Present a final summary: requirements covered, open assumptions, lint blockers = 0,
eval coverage %, **files-on-disk count, and the app's resource id from `cxas apps list`**.
Ask the user to confirm sign-off. Only then state `GATE: validate PASSED — SHIP-READY`.

## Example (lint-finding shape)
<example>
| Sev | Rule | Location | Finding | Fix |
|-----|------|----------|---------|-----|
| Blocker | grounding | order_status_agent | Answers order status from generation, no tool bound | Bind `get_order_status`; forbid free-generated status |
| Warning | handoff | order_status_agent | No handoff trigger defined | Add "escalate after 2 failed lookups" |
</example>
Blockers open: 0 required to pass the gate.

DECIDED / ASSUMED / NEED NEXT.
