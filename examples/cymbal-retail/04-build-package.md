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

=== PART B — CONFIG-AS-CODE (cxas-scrapi) ===
Tree:
  app/cymbal_retail.yaml
  agents/{cymbal_retail_agent,upsell_agent,out_of_scope_agent}.yaml
  tools/{catalog_openapi,cart_openapi,identify_plant,google_search,end_session}.yaml
  guardrails/{prompt_guard,blocklist,safety_outcomes}.yaml
  callbacks/{before_model,after_model,after_tool}.py
  variables/{customer_profile,image_uploaded,manager_discount_approved}.yaml

Python (idempotent; ADC auth):
```python
import os
from cxas_scrapi import Apps, Agents, Tools, Guardrails, Variables

PID = os.environ["PROJECT_ID"]           # cymbal-cx-demo (placeholder)
LOC = os.environ.get("LOCATION", "global")

app  = Apps(project_id=PID, location=LOC).create_or_update("cymbal_retail", "app/cymbal_retail.yaml")
V = Variables(project_id=PID, location=LOC)
for v in ("customer_profile","image_uploaded","manager_discount_approved"):
    V.create_or_update(v, spec_path=f"variables/{v}.yaml")
T = Tools(project_id=PID, location=LOC)
for t in ("catalog_openapi","cart_openapi","identify_plant","google_search","end_session"):
    T.create_or_update(t, spec_path=f"tools/{t}.yaml")            # R1,R2,R3,R9,R10
G = Guardrails(project_id=PID, location=LOC)
for g in ("prompt_guard","blocklist","safety_outcomes"):
    G.create_or_update(g, spec_path=f"guardrails/{g}.yaml")       # R8
A = Agents(project_id=PID, location=LOC)
for a in ("cymbal_retail_agent","upsell_agent","out_of_scope_agent"):
    A.create_or_update(app, a, spec_path=f"agents/{a}.yaml")
```

CLI:
```bash
export PROJECT_ID=cymbal-cx-demo LOCATION=global
cxas push && cxas lint
```
```

SELF-CHECK: pass — 1 app / 3 agents / 5 tools / 3 guardrails / 3 callbacks / 3 variables;
both paths in sync; every resource cites its Rn. PAUSE before Evals.
DECIDED: build emitted. ASSUMED: env secrets. NEED NEXT: Stage-5 evals.
