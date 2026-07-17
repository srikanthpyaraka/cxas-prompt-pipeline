STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)

```artifact:BUILD_PACKAGE

=== PART A — CONSOLE RUNBOOK (CX Agent Studio) ===
1. Create App "cymbal_retail" (global). (Or open the "Cymbal Home & Garden" sample to compare.)
2. Variables: add customer_profile (schema), image_uploaded (bool), manager_discount_approved (bool).
3. Tools: catalog_openapi + cart_openapi (paste OpenAPI specs), identify_plant (Python tool),
   google_search (built-in), end_session (system tool).
4. Agents: create cymbal_retail_agent (root) with global + agent instructions; add sub-agents
   upsell_agent and out_of_scope_agent; wire delegation.
5. Guardrails: prompt_guard, blocklist, safety_outcomes → attach to all agents.
6. Callbacks: register before_model, after_model, after_tool.
7. Save + version. [human: supply OpenAPI base URLs + auth here]

=== PART B — CONFIG-AS-CODE ===
(In current guidance the code path delegates to the official cxas-agent-foundry skill —
`inspect-app.py`, `cxas push`, lint via its `lint-fixer` sub-agent. Raw scrapi shown below
for illustration of the underlying resources.)
Real cxas pull/push tree (JSON; resource-per-folder; instructions + code as separate files):
```
cxas_app/CymbalRetail/
  app.json                       # displayName, rootAgent:"cymbal_retail_agent",
                                 #   variableDeclarations:[customer_profile(OBJECT), image_uploaded, manager_discount_approved],
                                 #   evaluationMetricsThresholds, loggingSettings, timeZoneSettings
  agents/cymbal_retail_agent/
    cymbal_retail_agent.json     # instruction:"agents/cymbal_retail_agent/instruction.txt",
                                 #   childAgents:["upsell_agent","out_of_scope_agent"],
                                 #   tools:["catalog_openapi","cart_openapi","identify_plant","google_search","end_session"],
                                 #   beforeModelCallbacks/afterModelCallbacks/afterToolCallbacks:[{pythonCode:path,description}]   [R7,R8]
    instruction.txt
    before_model_callbacks/before_model_callbacks_01/python_code.py
    after_model_callbacks/after_model_callbacks_01/python_code.py
    after_tool_callbacks/after_tool_callbacks_01/python_code.py
  agents/upsell_agent/upsell_agent.json + instruction.txt            # [R4]
  agents/out_of_scope_agent/out_of_scope_agent.json + instruction.txt # [R5,R10]
  tools/catalog_openapi/catalog_openapi.json          # {"displayName":"catalog_openapi","openApiTool":{...}}   [R1,R9]
  tools/cart_openapi/cart_openapi.json                # openApiTool                                             [R3]
  tools/identify_plant/identify_plant.json + python_function/python_code.py   # pythonFunction                 [R2]
  tools/google_search/google_search.json              # built-in search tool                                   [R2,R9]
  tools/end_session/end_session.json                  # system tool                                            [R10]
(eval authoring is a SIBLING of cxas_app/: <project>/evals/goldens/*.yaml + simulations/*.yaml — Stage 5)
```
Notes on the real format: guardrails (prompt guard / blocklist / safety outcomes) go in a
`guardrails/` folder in the app-dir (`cxas push` uploads `guardrails/` + `toolsets/`);
variables are in `app.json.variableDeclarations` (no `variables/` folder); sub-agents are the
root agent's `childAgents`.

Create the app, push, then push evals (this order fixes "no such app"):
```bash
export PID=cymbal-cx-demo LOC=global
cxas create "Cymbal Home & Garden" --project-id $PID --location $LOC   # new empty app
cxas apps list --project-id $PID --location $LOC                       # capture its resource id
cxas push --app-dir cxbuild/cymbal/cxas_app/CymbalRetail --to "Cymbal Home & Garden" \
  --project-id $PID --location $LOC
cxas push-eval --app-name projects/$PID/locations/$LOC/apps/<id> \
  --file cxbuild/cymbal/evals/goldens/PG-01.yaml
# then lint via cxas-agent-foundry's lint-fixer sub-agent (don't run cxas lint on the main thread)
```
```

SELF-CHECK: pass — 1 app / 3 agents / 5 tools / 3 variables + safety config / 3 callbacks;
both paths in sync; every resource cites its Rn. PAUSE before Evals.
DECIDED: build emitted. ASSUMED: env secrets. NEED NEXT: Stage-5 evals.
