# STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)
Input: `ARCHITECTURE` + `TRACEABILITY_MATRIX`. Goal: make the design real in CX Agent
Studio, emitted BOTH as a console runbook AND as cxas-scrapi config-as-code, describing
the same resources and kept in sync (see output-contract dual-emit rule).

## Write to files, not chat — and hand off cleanly to cxas-agent-foundry
- Emit the config **as files written into the layout the toolchain expects**:
  `<project>/cxas_app/<AppName>/` with `app/`, `agents/`, `tools/`, `guardrails/`,
  `examples/` (and `datastores/` where grounding uses a Data Store). This is what
  `cxas push` consumes and what `cxas pull` produces — do not leave config as pasted
  markdown on a real project.
- **This suite is the front half foundry doesn't have.** Produce a single `HANDOFF` note
  that tells cxas-agent-foundry exactly what to build and verify: the app path above, the
  agent/tool/guardrail inventory, the grounding sources, and the eval definitions from
  Stage 5. Seed the foundry `todo.md` from that inventory so its checklist starts populated.
- If a real `cxas pull` schema is available, validate your tree against it before pushing.

## Part A — CONSOLE RUNBOOK
Numbered CX Agent Studio UI steps to create, in order: the App → each Agent (goal,
instructions, tools attach, examples) → each Tool → each Guardrail → attach fallbacks &
handoff → save/version. Note where a human must supply secrets/auth.

## Part B — CONFIG-AS-CODE (delegate to cxas-agent-foundry)
Prefer the official **cxas-agent-foundry** skill over hand-written code. Emit:
1. **Directory tree** for `cxas pull`/`push`:
   `app/`, `agents/`, `tools/`, `guardrails/`, `examples/` — each resource's config
   (YAML/JSON) fully populated from the design.
2. **Foundry runbook** (this is the code path):
   - `python .agents/skills/cxas-agent-foundry/scripts/inspect-app.py` to check current state.
   - `cxas push --app-dir <project>/cxas_app/<AppName> --to projects/<pid>/locations/<loc>/apps/<app_id> --project-id <pid> --location <loc>`
   - Lint via the skill's **`lint-fixer` sub-agent** (do not run `cxas lint` on the main
     thread — its output is verbose); push only after lint returns clean.
   Only drop to raw `Apps/Agents/Tools/Guardrails` Python where no skill path covers the step.
3. Note the foundry skill enforces a `todo.md` checklist first — honor it.

## Cross-checks
- Every resource cites the `Rn`(s) it satisfies.
- Tool schemas match the design's I/O; guardrails attached to every agent.
- Every agent has fallback + handoff configured.

## Output
Emit `BUILD_PACKAGE` (Console Runbook + tree + scripts + CLI) in an artifact block. Then
PAUSE for user confirmation before Evals.

## Example (dual-emit shape — keep both paths in sync)
<example>
Console: 1) App → New agent "order_status_agent"  2) Add tool `get_order_status`
(HTTP GET /orders/{id})  3) Attach PII guardrail  4) Set fallback → handoff.  [R1, R2]

```
app/order-support.yaml
agents/order_status_agent.yaml
tools/get_order_status.yaml
guardrails/pii_redaction.yaml
```
```python
from cxas_scrapi import Agents, Tools  # ADC auth
t = Tools(project_id=PROJECT_ID, location="global")
t.create_or_update("get_order_status", spec_path="tools/get_order_status.yaml")  # R1
```
```bash
cxas push && cxas lint
```
</example>

DECIDED / ASSUMED / NEED NEXT.
