# GECX expert review — will this survive a real project?

A critical review of the prompt suite from a Google CX Agent Studio practitioner's lens,
focused on end-user adoption and delivery success. Verdict: **strong process discipline,
but it was too generic about the platform.** The findings below are addressed in the
prompts except where marked *Roadmap*.

## Findings

| # | Severity | Finding | Status |
|---|----------|---------|--------|
| 1 | High | **Grounding / Data Stores absent.** Design never forced "where does a factual answer come from — Data Store, tool, or static?" — the #1 thing CX projects get wrong. | ✅ Grounding now mandatory per intent in `03-design`; Data Store is a first-class resource in `ground-truth`; grounding-faithfulness is a required metric in `05-evals`. |
| 2 | High | **Examples treated as a footnote.** On this platform few-shot examples steer routing/tool-use more than instructions. | ✅ `03-design` now mandates example coverage: happy path · disambiguation · multi-intent · tool-failure · escalation. |
| 3 | High | **One-size ceremony.** Forcing 7 stages + 2 gates on a simple FAQ bot drives abandonment. | ✅ `01-ingest` classifies Simple/Standard/Complex; `00-orchestrator` scales ceremony to tier (gates always kept). |
| 4 | High | **Foundry handoff undefined.** cxas-agent-foundry also does PRD-to-agent → two overlapping intake systems confuse users. | ✅ `04-build` defines a `HANDOFF` note + seeds foundry `todo.md`; positions this suite as the front half foundry lacks. |
| 5 | High | **Eval realism.** Non-deterministic LLM outputs need variance runs, tool mocks, and semantic (not exact) assertions; "100% coverage" was brittle. | ✅ `05-evals` mandates `--runs 5`, tool mocks, semantic matching; adds containment/escalation-rate metrics. |
| 6 | Med-High | **Output was walls of chat**, not files in the `cxas push` layout. | ✅ `04-build` requires files under `<project>/cxas_app/<App>/` and validating against a real `cxas pull` schema. |
| 7 | Med | **Lint self-audit was "in the spirit of."** | ✅ `06-validate` now runs the real `cxas lint` via foundry's `lint-fixer`; manual list is fallback only. |
| 8 | Med | **Guardrails not mechanized.** "Redact PII" didn't name Cloud DLP, IAM, VPC-SC, residency. | ✅ Named in `ground-truth`; Design references the mechanism. |
| 9 | Med | **Voice/channel specifics missing** (barge-in, no-input/no-match timeouts, DTMF, SSML). | ✅ Channel branch added to `ground-truth` + `03-design`. |

## The meta-risk (not fixable by editing prompts) — *Roadmap*
Every artifact is still **authored, not executed** against a live `cxas` install or a
sandbox GCP project. For project success this is the gating risk: **one real end-to-end
build** will surface more truth than any further review. Priority-one before wider rollout:
1. Run the pipeline for real on a sandbox project; capture the transcript as the canonical example.
2. Pin the cxas-scrapi API surface to the installed version (smoke test).
3. Date-stamp `ground-truth` and set a re-verify cadence as the platform evolves.

## Round 2 — pre-share readiness review (fixes applied)
Verified specific claims against the repo (bella_notte pull + the cxas-agent-foundry
`project-template`), not a single example:

| # | Finding | Status |
|---|---------|--------|
| R2-1 | Build/Eval emitted the *pulled* JSON `evaluations/` form, but foundry (our handoff) authors evals as **YAML in a sibling `evals/`** folder (`goldens/`, `simulations/`, `callback_tests/`). | ✅ Build now targets the foundry project layout (`cxas_app/<App>/` JSON + sibling `evals/`); `05-evals` emits the real golden/simulation YAML (turns + `tool_calls` + NL `expectations` + `tags`; personas with `goal`/`response_guide`/`max_turns`). |
| R2-2 | Risk of asserting wrong/invented model IDs. | ✅ Confirmed `gemini-2.5-flash` + `gemini-3-flash` exist in-repo; corrected guidance to not invent per-agent model keys (model is typically an app-level default). |
| R2-3 | "No guardrails/variables folders" was from one example. | ✅ Re-confirmed via the `adding_guardrails` scenario + template (guardrails = app/agent safety config; variables = app.json). Dropped the uncertain `examples/` false-warn from the smoke test. |
| R2-4 | Smoke test only knew the pulled form. | ✅ Now accepts both pulled (`evaluations/`) and foundry authoring (sibling `evals/goldens`); `--pull-dir` documented as the `cxas_app/<App>` dir. Tested on good/bad/foundry fixtures. |

**Round-2 verdict: safe to share for testing.** The format now matches the actual
cxas-agent-foundry project template, so what testers generate lines up with what the
official skill expects. The gating risk remains the same single item below.

## Round 3 — real tester feedback (fixes applied)
Tester ran it and reported: *"eval format correct, but no evaluation files created in app code
— only in cmd logs; and no such app name exists."* Root causes + fixes, verified against the
`cxas` CLI docs (`create`, `push`, `push-eval`, `apps`):

| # | Root cause | Fix |
|---|-----------|-----|
| R3-1 | **Files narrated, not written.** Prompts printed the tree/evals in chat but never wrote them to disk. | `output-contract` + Stages 4/5 now **mandate writing every file with the file tool** and **verifying with `find … -type f`**; "narration is not a build." |
| R3-2 | **"No such app exists."** Pipeline pushed with `--to <app_id>` but never *created* the app. | Stage 4 now runs `cxas create "<name>"` → `cxas apps list` (capture id) → `cxas push --to "<name>"` → `cxas push-eval --file <yaml>`. Ground-truth documents the sequence. |
| R3-3 | **Guardrails format wrong (my error).** I'd claimed "no `guardrails/` folder." | `cxas push` uploads `guardrails/` + `toolsets/` — corrected in ground-truth, Build, both examples, the presentation, and the smoke test (no longer warns on `guardrails/`). |
| R3-4 | **No ship verification.** | Stage 6 now proves it's real before sign-off: files-on-disk count, `cxas apps list` shows the app, `push-eval` succeeded, and the layout smoke test. |

**Round-3 verdict:** the build now actually materializes files on disk and creates/pushes a
real app + evals. This directly addresses the tester's two failures. Still requires a live
run to confirm end-to-end on their project.

## Round 4 — "nothing assumed" pass (verified against an installed package)
`cxas_scrapi` became installable, so every assumption was checked, not guessed:

| # | Was assumed | Verified result |
|---|-------------|-----------------|
| R4-1 | `create_or_update` method | **Wrong** — real methods are `create_app`/`update_app`, `create_agent`, `create_tool`, `create_guardrail`, `create_variable`. Smoke test: 33 pass / 0 warn. |
| R4-2 | `model` is an agent field | **Wrong** — model lives in `app.json.modelSettings` (app-level). Removed from agent JSON in ground-truth/Build/scaffolder. |
| R4-3 | tool naming | **Confirmed rule:** tool `name`==`displayName`==directory (snake_case) or push fails "Reference not found." Scaffolder now writes `name`. |
| R4-4 | `cxas push-eval` accepts the foundry golden YAML | **Confirmed** — `EvalUtils.load_golden_evals_from_yaml` models (`Turn`=user/agent/tool_calls, `Conversation`=…/expectations/tags) match our YAML. |
| R4-5 | model IDs | **Confirmed** in-repo: gemini-2.5-flash, gemini-3-flash, gemini-3.1-flash-live. |

**Explicitly still unverified** (now labeled as such in ground-truth, not asserted): the internal
bodies of `openApiTool`/`dataStoreTool`, the guardrail JSON schema, and `environment.json`.
These say "confirm against a real pull" rather than presenting a guess as fact.

## Still-open smaller items (backlog)
- Vertical question banks for the interview (retail/telco/airline/banking) so it asks the
  5 questions that matter, faster.
- Multilingual/localization depth beyond a language field.
- On-platform experiments / A-B and canary specifics in the deploy runbook.
- First-class observability stage (CCAI Insights) feeding `cxas-loss-analysis` regressions.
