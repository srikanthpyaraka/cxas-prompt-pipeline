# STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)
Input: `ARCHITECTURE` + `TRACEABILITY_MATRIX`. Goal: make the design real in CX Agent
Studio, emitted BOTH as a console runbook AND as cxas-scrapi config-as-code, describing
the same resources and kept in sync (see output-contract dual-emit rule).

## Part A — CONSOLE RUNBOOK
Numbered CX Agent Studio UI steps to create, in order: the App → each Agent (goal,
instructions, tools attach, examples) → each Tool → each Guardrail → attach fallbacks &
handoff → save/version. Note where a human must supply secrets/auth.

## Part B — CONFIG-AS-CODE (cxas-scrapi)
1. **Directory tree** for `cxas pull`/`push`:
   `app/`, `agents/`, `tools/`, `guardrails/`, `examples/` — with each resource's config
   file (YAML/JSON) fully populated from the design.
2. **Python create/update scripts** using `Apps`, `Agents`, `Tools`, `Guardrails`,
   `Deployments`, parameterized by `project_id` / `location`, with auth note (ADC).
   Show idempotent create-or-update where possible.
3. **CLI runbook:** ordered `cxas push` / lint / deploy commands.

## Cross-checks
- Every resource cites the `Rn`(s) it satisfies.
- Tool schemas match the design's I/O; guardrails attached to every agent.
- Every agent has fallback + handoff configured.

## Output
Emit `BUILD_PACKAGE` (Console Runbook + tree + scripts + CLI) in an artifact block. Then
PAUSE for user confirmation before Evals.

DECIDED / ASSUMED / NEED NEXT.
