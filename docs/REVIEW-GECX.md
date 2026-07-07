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

## Still-open smaller items (backlog)
- Vertical question banks for the interview (retail/telco/airline/banking) so it asks the
  5 questions that matter, faster.
- Multilingual/localization depth beyond a language field.
- On-platform experiments / A-B and canary specifics in the deploy runbook.
- First-class observability stage (CCAI Insights) feeding `cxas-loss-analysis` regressions.
