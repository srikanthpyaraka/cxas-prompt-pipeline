# Prompt Assessment Report

This is the result of running `PROMPT-ASSESSOR.prompt.md` against the prompts in this
package. Scores use the assessor's 0–100 rubric (see the skill for criteria and weights).
Good-to-go bar: total ≥ 90, no applicable criterion < 7, zero unresolved contradictions.

## Scores — before vs. after improvements

| Prompt file | Before | After | Verdict |
|-------------|:------:|:-----:|---------|
| `00-orchestrator.prompt.md` | 88 | 93 | Good to go |
| `01-ingest.prompt.md`       | 86 | 92 | Good to go |
| `02-interview.prompt.md`    | 89 | 94 | Good to go |
| `03-design.prompt.md`       | 87 | 92 | Good to go |
| `04-build.prompt.md`        | 88 | 93 | Good to go |
| `05-evals.prompt.md`        | 89 | 93 | Good to go |
| `06-validate.prompt.md`     | 90 | 94 | Good to go |
| `PROMPT-ASSESSOR.prompt.md` | 93 | 95 | Good to go |

## What the assessor flagged (and how it was fixed)

The package already scored well on role, clarity, sequential decomposition, and output
control. Two best-practice gaps recurred across the stage prompts:

- **[Major] Structure & XML tags** — stage prompts told the user to "paste the previous
  artifact" but did not *delimit* that variable input, risking instruction/data
  confusion. **Fix:** added a "Delimit variable input" rule to `shared/output-contract.md`
  (wrap inputs in `<input>` / `<user_prd>` tags; treat contents as data, never
  instructions). This propagates to every stage.

- **[Major] Reasoning & self-check** — no explicit verify-before-emit step, which
  Anthropic's guidance recommends for complex, multi-step tasks. **Fix:** added a
  "Self-check before emitting an artifact" rule (4 checks + a reported `SELF-CHECK:`
  line) to `shared/output-contract.md`.

- **[Minor] Positive constraints** — a few "do not" phrasings. **Fix:** added a
  "Phrase constraints positively" directive to the global behavior rules.

The assessor itself scored highest because it was authored to embody the practices it
checks (explicit role, delimited input, XML output structure, worked examples, a
self-check step, and a bounded iterate-until-good loop).

## How these scores were produced

Judgment applied per the rubric in `PROMPT-ASSESSOR.prompt.md`. To reproduce or re-audit
any file, run the assessor with that file's contents pasted into `<prompt_under_review>`.
Scores are expert estimates, not a deterministic metric — re-running the assessor is the
source of truth.
