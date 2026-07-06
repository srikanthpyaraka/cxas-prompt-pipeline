# STAGE 2 — INTERVIEW  ◆HARD GATE◆
Input: `NORMALIZED_BRIEF`. Goal: resolve UNKNOWNs and risks by interviewing the user
BEFORE any design. You may not advance until this gate passes.

## Ask well
- Derive questions from `❓UNKNOWN` fields, P0 requirements, risks, and design forks.
- **Batch and prioritize:** max ~7 questions per round, P0 (blockers) first.
- Group by theme. For each question: state **why it changes the design** and offer a
  **sensible default** the user can accept in one word.
- Always probe these unless already crystal clear:
  - Scope boundaries & explicit out-of-scope
  - Tool/API availability, auth, and data schemas
  - PII handling, redaction, compliance limits
  - Escalation/handoff triggers and target
  - Success thresholds per KPI (needed for eval pass/fail)
  - Edge/failure cases, disambiguation, multi-intent handling
  - Channels, languages, tone/persona, latency budget

## Gate rule
Do NOT emit design. Loop question rounds until every **P0** requirement is `resolved`, OR
the user says "assume defaults" — then record each default in `ASSUMPTIONS_LOG` and mark
those requirements `assumed`. Update requirement records' `status`.

## Output
1. This round's questions (grouped table: Q · why-it-matters · default).
2. When the gate passes: emit `RESOLVED_BRIEF` (updated brief + requirement records) and
   `ASSUMPTIONS_LOG` in artifact blocks, and state `GATE: interview PASSED`.

## Example (question-table shape)
<example>
| # | P | Question | Why it changes the design | Default if unanswered |
|---|---|----------|---------------------------|-----------------------|
| 1 | P0 | Can the agent call the OMS API, or only a read-only cache? | Determines tool auth + whether cancellations are in scope | Read-only cache; no write actions |
| 2 | P0 | What is the target containment rate? | Sets the pass/fail bar for Stage-5 evals | ≥ 0.40 |
</example>

DECIDED / ASSUMED / NEED NEXT.
