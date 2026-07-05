# CX Agent Builder — Prompt Package

A modular, chainable prompt system that turns **any input describing a desired
customer-experience agent** (a formal PRD, meeting notes, tickets, or bullet points)
into a **designed, built, and evaluated Google Cloud CX Agent Studio (Gemini
Enterprise CX) agent** using the **cxas-scrapi** framework.

It is deliberately split into an **orchestrator + six stage prompts** so each step is
independently runnable, cheaper per call, and version-controllable. The orchestrator
holds state and enforces two hard gates: **Interview** (never build on unstated
assumptions) and **Validate** (never ship without a lint self-audit and user sign-off).

Every Build and Eval output is emitted **twice, equally**: a **CX Agent Studio console
runbook** (UI path) **and** **cxas-scrapi config-as-code + CLI** (CI/CD path), kept in
sync.

## File map

| File | Purpose |
|------|---------|
| `00-orchestrator.prompt.md` | Drives the state machine, holds `PROJECT_STATE`, enforces gates, chains stages. |
| `01-ingest.prompt.md`   | Parse any input → `NORMALIZED_BRIEF` with requirement IDs + UNKNOWNs. |
| `02-interview.prompt.md`| **◆GATE◆** Batched, prioritized clarifying questions → resolved brief + `ASSUMPTIONS_LOG`. |
| `03-design.prompt.md`   | Decompose into App/Agents/Tools/Guardrails/Examples/Fallbacks + `TRACEABILITY_MATRIX`. |
| `04-build.prompt.md`    | Console runbook **and** scrapi config tree + Python create/update scripts. |
| `05-evals.prompt.md`    | All 5 eval types, thresholds, coverage %, console steps **and** `cxas` commands. |
| `06-validate.prompt.md` | **◆GATE◆** `cxas lint` self-audit + full deliverable package + final sign-off. |
| `shared/ground-truth.md`   | Platform + cxas-scrapi facts. Prepended to every stage. |
| `shared/output-contract.md`| Global output rules (artifact envelope, IDs, assumptions, dual-emit). |

## How to run

**Automated (recommended):** Use `00-orchestrator.prompt.md` as the system prompt. It
prepends `shared/ground-truth.md` + `shared/output-contract.md`, then invokes each stage
prompt in order, passing the prior stage's artifact forward. It will not cross a ◆GATE◆
without the required condition (P0 questions answered; lint findings resolved + user OK).

**Manual / stage-by-stage:** Prepend both `shared/*.md` files, then paste one stage
prompt plus the previous stage's output artifact. Good for iterating on a single stage.

## The state machine

```
1 INGEST → 2 INTERVIEW ◆GATE◆ → 3 DESIGN → 4 BUILD → 5 EVALS → 6 VALIDATE ◆GATE◆ → SHIP
```

## Artifact hand-offs (each stage's OUTPUT is the next stage's INPUT)

```
01 → NORMALIZED_BRIEF
02 → RESOLVED_BRIEF + ASSUMPTIONS_LOG
03 → ARCHITECTURE + TRACEABILITY_MATRIX
04 → BUILD_PACKAGE (console runbook + scrapi tree + scripts)
05 → EVAL_SUITE (5 types + thresholds + coverage report)
06 → DELIVERABLE_PACKAGE (lint audit + docs + deploy runbook)
```

## Ground truth this package targets

- **Hierarchy:** App → Agents (LLM playbooks) → Tools → Guardrails → Examples → Deployments; plus generative fallbacks + human handoff.
- **cxas-scrapi:** `Apps`, `Agents`, `Tools`, `Guardrails`, `Deployments`, `Sessions`, `Variables`; `cxas pull`/`push`; `cxas lint` (60+ rules).
- **Eval taxonomy (all 5):** Platform Goldens · Local Simulations · Tool Tests · Callback Tests · Turn Evals. Metrics: response-match, tool-call accuracy, latency.
