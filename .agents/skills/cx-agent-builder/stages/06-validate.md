# STAGE 6 — VALIDATE & DOCUMENT  ◆HARD GATE◆
Input: all prior artifacts. Goal: self-audit, assemble the deliverable, and get sign-off.
You may not declare SHIP-READY until blockers are cleared AND the user confirms.

## Lint self-audit (in the spirit of `cxas lint`, 60+ rules)
Review and report findings by severity (Blocker / Warning / Info) across at least:
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

## Gate & sign-off
Present a final summary: requirements covered, open assumptions, lint blockers = 0,
eval coverage %. Ask the user to confirm sign-off. Only then state
`GATE: validate PASSED — SHIP-READY`.

## Example (lint-finding shape)
<example>
| Sev | Rule | Location | Finding | Fix |
|-----|------|----------|---------|-----|
| Blocker | grounding | order_status_agent | Answers order status from generation, no tool bound | Bind `get_order_status`; forbid free-generated status |
| Warning | handoff | order_status_agent | No handoff trigger defined | Add "escalate after 2 failed lookups" |
</example>
Blockers open: 0 required to pass the gate.

DECIDED / ASSUMED / NEED NEXT.
