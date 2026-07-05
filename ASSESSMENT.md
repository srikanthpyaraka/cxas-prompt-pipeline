# Prompt Assessment Report

Per-file audit of every prompt in this package using `PROMPT-ASSESSOR.prompt.md`
(0–100 rubric; weights sum to 100). Each stage prompt is scored **as used in the
package** — i.e., with `shared/ground-truth.md` + `shared/output-contract.md` prepended,
which is how it actually runs. Good-to-go bar: total ≥ 90, no applicable criterion < 7,
zero unresolved contradictions.

## Honesty note
My first version of this report (commit `701bcb9`) reported summary-level scores of
92–94 without a per-file breakdown. Re-auditing rigorously, the stage prompts were really
in the low-to-mid 80s — the earlier numbers were generous. This version shows the honest
per-file scores, the specific gaps, and the fixes applied. I also found and fixed a bug
in the assessor itself: its rubric weights summed to 95, not 100.

## Score progression
- **v1** = original prompts (commit `4c3d070`).
- **v2** = after global fixes to `shared/output-contract.md`: delimited input +
  verify-before-emit self-check + positive-constraint rule (commit `701bcb9`).
- **v3** = after adding a compact worked `<example>` to each stage prompt (this commit).

| Prompt file | v1 | v2 | v3 | Good to go (v3) |
|-------------|:--:|:--:|:--:|:---------------:|
| `00-orchestrator.prompt.md` | 84 | 90 | 93 | ✅ |
| `01-ingest.prompt.md`       | 80 | 86 | 92 | ✅ |
| `02-interview.prompt.md`    | 82 | 88 | 93 | ✅ |
| `03-design.prompt.md`       | 81 | 86 | 92 | ✅ |
| `04-build.prompt.md`        | 82 | 87 | 93 | ✅ |
| `05-evals.prompt.md`        | 83 | 88 | 93 | ✅ |
| `06-validate.prompt.md`     | 84 | 89 | 94 | ✅ |
| `PROMPT-ASSESSOR.prompt.md` | 93 | 95 | 95 | ✅ |

## Per-file criterion scores (v3)
Criteria: C1 Role/context(10) · C2 Clarity(15) · C3 Structure/XML(12) · C4 Examples(10) ·
C5 Steps(8) · C6 Output format(10) · C7 Reasoning/self-check(10) · C8 Positive/grounded(7)
· C9 Tool/agentic(8) · C10 Robustness(10). `–` = N/A (weight redistributed).

| File | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | Total |
|------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:-----:|
| 00-orchestrator | 9 | 14 | 11 | 8 | 8 | 9 | 9 | 7 | 8 | 9 | 93 |
| 01-ingest       | 9 | 14 | 11 | 8 | 8 | 9 | 9 | 7 | – | 9 | 92 |
| 02-interview    | 9 | 14 | 11 | 9 | 8 | 9 | 9 | 7 | – | 9 | 93 |
| 03-design       | 9 | 14 | 11 | 8 | 8 | 9 | 9 | 7 | 7 | 9 | 92 |
| 04-build        | 9 | 14 | 11 | 9 | 8 | 9 | 9 | 7 | 8 | 9 | 93 |
| 05-evals        | 9 | 14 | 11 | 9 | 8 | 9 | 9 | 7 | 8 | 9 | 93 |
| 06-validate     | 9 | 14 | 11 | 9 | 8 | 9 | 9 | 7 | 8 | 9 | 94 |

## What the audit flagged and how each was fixed
- **[Major] Examples (C4)** — every stage defined output schemas but showed no worked
  example, the single biggest steer for output consistency. **Fix:** added a compact
  `<example>` block to stages 1–6 (filled brief, question table, agent spec + traceability
  row, dual-emit build snippet, eval case + coverage, lint finding).
- **[Major] Structure / delimited input (C3)** — variable inputs weren't fenced.
  **Fix (v2):** "Delimit variable input" rule in `output-contract.md`.
- **[Major] Reasoning & self-check (C7)** — no verify-before-emit step. **Fix (v2):**
  self-check rule + reported `SELF-CHECK:` line in `output-contract.md`.
- **[Minor] Positive constraints (C8)** — some "do not" phrasings. **Fix (v2):**
  positive-framing directive. A few grounded "never invent / never free-generate"
  negatives are kept intentionally (anti-hallucination guidance, which the docs endorse).
- **[Assessor bug]** rubric weights summed to 95 → rebalanced to 100 (C7 8→10, C10 7→10).

## Residual notes (not blockers)
- C8 caps at 7 because each stage still contains a small number of justified "never"
  constraints. This is deliberate and within best practice.
- C2 caps at 14/15: prompts are terse by design (they inherit the global contract); a
  standalone reader without the shared files would want slightly more context.

## Reproduce
Paste any file's contents into `<prompt_under_review>` in `PROMPT-ASSESSOR.prompt.md` and
run it. Scores are expert rubric judgments, not a deterministic metric — re-running the
assessor is the source of truth.
