# STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)
Input: `ARCHITECTURE` + `TRACEABILITY_MATRIX`. Goal: make the design real in CX Agent
Studio, emitted BOTH as a console runbook AND as cxas-scrapi config-as-code, describing
the same resources and kept in sync (see output-contract dual-emit rule).

## Emit the REAL cxas pull/push format (JSON — not YAML, not markdown)
Write files into the exact tree `cxas pull` produces / `cxas push` consumes. **Resources
are JSON, one folder per resource named after it; instructions and callback/tool code are
separate files referenced by relative path:**
```
<project>/cxas_app/<AppName>/
  app.json                                  # displayName, rootAgent, variableDeclarations[], loggingSettings, evaluationMetricsThresholds, timeZoneSettings
  agents/<Agent_DisplayName>/
    <Agent_DisplayName>.json                # name(uuid), displayName, model?, instruction:"agents/<A>/instruction.txt", tools:[toolDisplayName], childAgents:[subAgentDisplayName], before/afterModel|Tool|AgentCallbacks:[{pythonCode:path, description}]
    instruction.txt                         # the playbook instructions live HERE, not inline in JSON
    before_model_callbacks/before_model_callbacks_01/python_code.py   # (and after_tool_/after_model_/before_agent_ as needed)
  tools/<tool_name>/
    <tool_name>.json                        # name(uuid), displayName, and ONE of: pythonFunction{name,pythonCode:path,description} | openApiTool{...} | dataStoreTool{...}
    python_function/python_code.py           # for python tools
  evaluations/<Eval_DisplayName>/<Eval_DisplayName>.json          # goldens (Stage 5 writes these) — turns/steps/expectations
  evaluationExpectations/<Name>/<Name>.json
```
Key rules that people get wrong:
- **Sub-agents** are the root/parent agent's `childAgents: []` (display names), not a folder.
- **Variables** are declared in `app.json` `variableDeclarations` (each: `name`, `description`,
  `schema:{type: OBJECT|STRING|…, default}`), not a `variables/` folder.
- **`rootAgent`** in app.json names the steering agent by displayName.
- **Evals are part of the app tree** (`evaluations/` + `evaluationExpectations/`); thresholds
  go in app.json `evaluationMetricsThresholds`. Stage 5 populates these.
- There is **no top-level `guardrails/` or `examples/` folder** — represent guardrails via the
  app/agent safety config and few-shot examples via the platform's mechanism; verify against a real `cxas pull`.
- **This suite is the front half foundry doesn't have.** Produce a single `HANDOFF` note for
  cxas-agent-foundry: the app path, the agent/tool inventory, `childAgents` topology,
  grounding sources, and the eval names. Seed the foundry `todo.md` from that inventory.
- If a real `cxas pull` of a comparable app is available, diff your tree against it before pushing.

## Part A — CONSOLE RUNBOOK
Numbered CX Agent Studio UI steps to create, in order: the App → each Agent (goal,
instructions, tools attach, examples) → each Tool → each Guardrail → attach fallbacks &
handoff → save/version. Note where a human must supply secrets/auth.

## Part B — CONFIG-AS-CODE (delegate to cxas-agent-foundry)
Prefer the official **cxas-agent-foundry** skill over hand-written code. Emit:
1. **The JSON app tree above** for `cxas pull`/`push` — each resource's JSON + its
   `instruction.txt` / `python_code.py` files, fully populated from the design.
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

## Example (real cxas JSON tree — keep console + code in sync)
<example>
Console: 1) App → root agent "Order_Router"  2) sub-agent "Order_Status_Agent", add tool
`get_order_status`  3) app safety/guardrail config  4) fallback → handoff.  [R1, R2]

```
cxas_app/OrderSupport/
  app.json                     # {"displayName":"Order Support","rootAgent":"Order_Router","variableDeclarations":[...],"evaluationMetricsThresholds":{...}}
  agents/Order_Router/
    Order_Router.json          # {"displayName":"Order_Router","instruction":"agents/Order_Router/instruction.txt","childAgents":["Order_Status_Agent"],"tools":["end_session"]}
    instruction.txt
  agents/Order_Status_Agent/
    Order_Status_Agent.json    # {"displayName":"Order_Status_Agent","instruction":"...instruction.txt","tools":["get_order_status"]}  [R1]
    instruction.txt
  tools/get_order_status/
    get_order_status.json      # {"displayName":"get_order_status","openApiTool":{...}}  or pythonFunction{...,"pythonCode":"tools/get_order_status/python_function/python_code.py"}
  evaluations/Order_Status_Happy_Path/Order_Status_Happy_Path.json   # golden (Stage 5)
```
```bash
cxas push --app-dir cxas_app/OrderSupport --to projects/$PID/locations/$LOC/apps/$APP_ID \
  --project-id $PID --location $LOC
# then lint via cxas-agent-foundry's lint-fixer sub-agent
```
</example>

DECIDED / ASSUMED / NEED NEXT.
