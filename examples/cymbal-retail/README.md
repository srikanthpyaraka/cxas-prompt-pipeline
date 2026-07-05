# Worked example — Cymbal Home & Garden (CX Agent Studio's default sample)

The pipeline run against **CX Agent Studio's shipped sample agent** — the
"Cymbal Home & Garden" retail assistant (`cymbal_retail_agent`). Using the platform's own
default use case makes this a **verifiable** example: the generated architecture can be
cross-checked against the sample in the console.

Source: CX Agent Studio → Build → [Sample agents](https://docs.cloud.google.com/customer-engagement-ai/conversational-agents/ps/agent-sample)
(one sample as of Nov 2025). All identifiers here are placeholders — no real project.

## The run, stage by stage
| File | Stage | Artifact |
|------|-------|----------|
| [`00-prd.md`](00-prd.md) | input | PRD reverse-engineered from the sample |
| [`01-normalized-brief.md`](01-normalized-brief.md) | 1 Ingest | 10 requirements (R1–R10) |
| [`02-interview.md`](02-interview.md) | 2 Interview ◆gate◆ | KPI/upsell/discount questions → resolved brief |
| [`03-architecture.md`](03-architecture.md) | 3 Design | Root + upsell + out-of-scope; tools, variables, guardrails, callbacks |
| [`04-build-package.md`](04-build-package.md) | 4 Build | Console runbook **and** cxas-scrapi config |
| [`05-eval-suite.md`](05-eval-suite.md) | 5 Evals | 5 eval types, 17 assets, 100% coverage |
| [`06-deliverable.md`](06-deliverable.md) | 6 Validate ◆gate◆ | Lint audit + deploy runbook + sign-off |
| [`07-bugfix.md`](07-bugfix.md) | 7 Debug & Fix | A real eval failure (upsell leaks into checkout) → root cause → minimal fix → regression eval |

> **Provenance:** these artifacts are an authored *reference run* — hand-written to conform
> to the pipeline prompts' contracts and QA'd against them — not the transcript of a live
> orchestrator execution. They show the shape and quality the prompts are built to produce.
> Identifiers are placeholders; no real project or PII.

## Why this one
It exercises the hard parts of the platform: a multi-agent (root + sub-agents) design,
OpenAPI + Python + Google-Search + system tools, custom + boolean variables, prompt
guards / blocklists / safety outcomes, `before/after_model` + `after_tool` callbacks, and
golden + scenario evals — all mapped back to requirements with 100% eval coverage.
