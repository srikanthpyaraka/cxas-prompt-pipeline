# Worked example — "OrderBot" for AcmeShop

An end-to-end run of the pipeline on a realistic PRD, so you can see what each stage
produces before running it yourself. All identifiers are fictional — no real
`project_id`, keys, or PII.

## The run, stage by stage

| File | Stage | Artifact |
|------|-------|----------|
| [`00-prd.md`](00-prd.md) | input | The raw PRD handed to the pipeline |
| [`01-normalized-brief.md`](01-normalized-brief.md) | 1 Ingest | `NORMALIZED_BRIEF` + requirement records (R1–R9) |
| [`02-interview.md`](02-interview.md) | 2 Interview ◆gate◆ | Questions → `RESOLVED_BRIEF` + `ASSUMPTIONS_LOG` |
| [`03-architecture.md`](03-architecture.md) | 3 Design | `ARCHITECTURE` + `TRACEABILITY_MATRIX` |
| [`04-build-package.md`](04-build-package.md) | 4 Build | Console runbook **and** cxas-scrapi config + scripts |
| [`05-eval-suite.md`](05-eval-suite.md) | 5 Evals | All 5 eval types + thresholds + 100% coverage |
| [`06-deliverable.md`](06-deliverable.md) | 6 Validate ◆gate◆ | Lint audit + deploy runbook + sign-off |

## How this was produced
Load `shared/*.md` + `00-orchestrator.prompt.md`, paste [`00-prd.md`](00-prd.md), and let
the orchestrator run all six stages. This folder is the (lightly trimmed) result. Your own
run will differ based on how you answer the Stage-2 interview.
