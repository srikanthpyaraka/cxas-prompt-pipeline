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

## Still-open smaller items (backlog)
- Vertical question banks for the interview (retail/telco/airline/banking) so it asks the
  5 questions that matter, faster.
- Multilingual/localization depth beyond a language field.
- On-platform experiments / A-B and canary specifics in the deploy runbook.
- First-class observability stage (CCAI Insights) feeding `cxas-loss-analysis` regressions.
