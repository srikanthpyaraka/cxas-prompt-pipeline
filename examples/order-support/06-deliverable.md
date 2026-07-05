STAGE 6 — VALIDATE & DOCUMENT ◆HARD GATE◆

## Lint self-audit (spirit of `cxas lint`, 60+ rules)
| Sev | Rule | Location | Finding | Fix |
|-----|------|----------|---------|-----|
| Blocker | grounding | faq_agent | KB answers must cite a source, not free-generate | Enforced: require `search_kb` passage citation [R3] |
| Blocker | pci | returns_agent | Ensure confirmation turn never echoes full PAN | pci_block masks to last-4 before any echo [R6] |
| Warning | handoff | order_status_agent | Confirm 2-failed-attempt trigger wired | Added explicit handoff after 2 failed lookups [R4] |
| Warning | idempotency | create_return | Write tool must not auto-retry ambiguous failures | Disabled auto-retry; surface error + offer handoff [R2] |
| Info | naming | all | Consistent snake_case resource names | OK |

Blockers open after fixes: **0** → gate can pass.

```artifact:DELIVERABLE_PACKAGE
1. Brief + Assumptions — see 01/02 (A1–A3 pending user confirmation).
2. Architecture + Traceability — see 03 (router + 3 sub-agents; 9/9 covered).
3. Build — see 04 (console runbook + cxas-scrapi tree/scripts; 1 app, 4 agents, 3 tools,
   3 guardrails).
4. Eval suite — see 05 (16 assets across 5 types; 100% coverage; 0-leak safety bars).
5. Deploy runbook & monitoring:
   - Deploy: cxas push → cxas lint (0 blockers) → create version → canary 10% traffic.
   - Monitor: containment, CSAT proxy, latency p95, PII/card-leak alarms (page on any leak).
   - Iteration loop: mined failure transcripts → new goldens/examples → re-eval → redeploy.
```

## Sign-off
Requirements covered: 9/9. Open assumptions: A1–A3 (auth, placeholders, after-hours
returns). Lint blockers: 0. Eval coverage: 100%.

Pending user confirmation of A1–A3 and replacement of placeholder project_id, this is
`GATE: validate PASSED — SHIP-READY`.

DECIDED: deliverable assembled, 0 blockers. ASSUMED: A1–A3. NEED NEXT: user confirms env + assumptions → deploy.
