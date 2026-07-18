# STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)
Input: `ARCHITECTURE` + `TRACEABILITY_MATRIX`. Goal: make the design real in CX Agent
Studio, emitted BOTH as a console runbook AND as cxas-scrapi config-as-code, describing
the same resources and kept in sync (see output-contract dual-emit rule).

## Emit the REAL cxas pull/push format (JSON — not YAML, not markdown)
Write files into the exact tree `cxas pull` produces / `cxas push` consumes. **Resources
are JSON, one folder per resource named after it; instructions and callback/tool code are
separate files referenced by relative path:**
Match the **cxas-agent-foundry project layout** (its `assets/project-template`), since we
hand off to foundry — the pushable app under `cxas_app/<App>/` (JSON) and eval **authoring**
as YAML in a sibling `evals/` folder (Stage 5 fills that):
```
<project>/
  cxas_app/<AppName>/
    app.json                                # displayName, rootAgent, variableDeclarations[], loggingSettings, evaluationMetricsThresholds, timeZoneSettings
    agents/<Agent_DisplayName>/
      <Agent_DisplayName>.json              # name(==displayName==dir), displayName, instruction:"agents/<A>/instruction.txt", tools:[toolDisplayName], childAgents:[subAgentDisplayName], before/afterModel|Tool|AgentCallbacks:[{pythonCode:path, description}]  (NO model field — see modelSettings in app.json)
      instruction.txt                       # the playbook instructions live HERE, not inline in JSON
      before_model_callbacks/before_model_callbacks_01/python_code.py   # (and after_tool_/after_model_/before_agent_ as needed)
    tools/<tool_name>/
      <tool_name>.json                      # name==displayName==dir (snake_case!) + ONE of: pythonFunction{name,pythonCode:path,description} | openApiTool{...} | dataStoreTool{...}
      python_function/python_code.py         # for python tools
  evals/                                     # Stage 5 writes these (foundry authoring format, YAML)
    goldens/*.yaml   simulations/*.yaml   callback_tests/...
```
Key rules that people get wrong:
- **Sub-agents** are the root/parent agent's `childAgents: []` (display names), not a folder.
- **Variables** are declared in `app.json` `variableDeclarations` (each: `name`, `description`,
  `schema:{type: OBJECT|STRING|…, default}`), not a `variables/` folder.
- **`rootAgent`** in app.json names the steering agent by displayName. **Model lives in
  `app.json.modelSettings`** (app-level; models gemini-2.5-flash / gemini-3-flash /
  gemini-3.1-flash-live) — there is NO `model` field on an agent; don't add one.
- **Evals authoring lives in the sibling `evals/` folder as YAML** (Stage 5). The JSON
  `evaluations/` + `evaluationExpectations/` folders are the *pulled* platform form; thresholds
  live in app.json `evaluationMetricsThresholds`.
- **`cxas push` uploads these from the app-dir:** `app.json`, `global_instruction.txt`,
  `environment.json`, and folders `agents/`, `tools/`, `toolsets/`, `guardrails/`,
  `evaluations/`, `evaluationDatasets/`, `evaluationExpectations/`. So **`guardrails/` and
  `toolsets/` ARE valid folders** — put guardrail configs under `guardrails/`. Variables stay
  in `app.json.variableDeclarations` (no `variables/` folder).
- Also write **`gecx-config.json`** at the run root (GCP project_id, location, app display
  name/id) and a `HANDOFF` note (app path, agent/tool inventory, `childAgents` topology,
  grounding sources, eval names). Seed the foundry `todo.md` from that inventory.

## ⚠ You must WRITE every file to disk, then create the app — narration is not a build
Printing the tree in chat is NOT building. Two failures reported by testers you MUST avoid:
"eval/config files only in the logs, not on disk" and "no such app exists." So:

1. **Write every file** with your file tool (per the output contract), then verify:
   `find cxbuild/<app>/cxas_app -type f` — confirm app.json + every agent/tool/instruction/callback exists.
   *Deterministic option:* emit a `spec.json` (app/agents/tools/guardrails/goldens) and run
   `python3 scripts/scaffold-app.py spec.json` — it writes the correct tree for you.
2. **Create the app on-platform BEFORE pushing** (this is what fixes "no such app"):
   ```bash
   cxas create "<App Display Name>" --project-id <pid> --location <loc>
   cxas apps list --project-id <pid> --location <loc>        # confirm it exists; capture the resource name
   ```
3. **Push the written tree**, then push evals (Stage 5 files):
   ```bash
   cxas push --app-dir cxbuild/<app>/cxas_app/<App> --to "<App Display Name>" \
     --project-id <pid> --location <loc>
   cxas push-eval --app-name projects/<pid>/locations/<loc>/apps/<id> --file cxbuild/<app>/evals/goldens/<file>.yaml
   ```
4. Lint via cxas-agent-foundry's **`lint-fixer` sub-agent** (don't run `cxas lint` on the main
   thread). Honor the foundry `todo.md` checklist. Prefer the foundry skill over raw scrapi Python.

## Part A — CONSOLE RUNBOOK
Numbered CX Agent Studio UI steps to create, in order: the App → each Agent (goal,
instructions, tools attach, examples) → each Tool → each Guardrail → attach fallbacks &
handoff → save/version. Note where a human must supply secrets/auth.

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
