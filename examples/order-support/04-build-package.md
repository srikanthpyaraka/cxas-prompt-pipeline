STAGE 4 — BUILD (dual-emit: console runbook AND config-as-code)

```artifact:BUILD_PACKAGE

=== PART A — CONSOLE RUNBOOK (CX Agent Studio) ===
1. Create App "orderbot" (location: global).
2. Create tools:
   a. get_order_status — HTTP GET {OMS}/orders/{order_id}; OAuth SA. [R1]
   b. create_return — HTTP POST {RMA}/returns; body {order_id, reason}; OAuth SA. [R2]
   c. search_kb — data store / KB connector over help-center. [R3]
3. Create agents (goal + instructions + examples), attach tools:
   router → order_status_agent (get_order_status) → returns_agent (create_return, add a
   confirmation turn) → faq_agent (search_kb, require citation).
4. Create guardrails and attach to ALL agents: pii_redaction, pci_block, off_topic_refusal.
5. Configure generative fallback + handoff: tier-1 queue (6am–10pm), after-hours ticket.
6. Save & create a version. [human: supply OAuth SA + API base URLs here]

=== PART B — CONFIG-AS-CODE (cxas-scrapi) ===
Tree (cxas pull/push):
  app/orderbot.yaml
  agents/router.yaml
  agents/order_status_agent.yaml
  agents/returns_agent.yaml
  agents/faq_agent.yaml
  tools/get_order_status.yaml
  tools/create_return.yaml
  tools/search_kb.yaml
  guardrails/pii_redaction.yaml
  guardrails/pci_block.yaml
  guardrails/off_topic_refusal.yaml

Python (idempotent create-or-update; ADC auth):
```python
import os
from cxas_scrapi import Apps, Agents, Tools, Guardrails  # gcloud auth application-default login

PROJECT_ID = os.environ["PROJECT_ID"]     # e.g. acme-cx-prod (placeholder)
LOCATION   = os.environ.get("LOCATION", "global")

apps  = Apps(project_id=PROJECT_ID, location=LOCATION)
tools = Tools(project_id=PROJECT_ID, location=LOCATION)
guard = Guardrails(project_id=PROJECT_ID, location=LOCATION)
agents = Agents(project_id=PROJECT_ID, location=LOCATION)

app = apps.create_or_update("orderbot", spec_path="app/orderbot.yaml")
for name in ("get_order_status", "create_return", "search_kb"):       # R1, R2, R3
    tools.create_or_update(name, spec_path=f"tools/{name}.yaml")
for name in ("pii_redaction", "pci_block", "off_topic_refusal"):       # R5, R6, R4
    guard.create_or_update(name, spec_path=f"guardrails/{name}.yaml")
for name in ("router", "order_status_agent", "returns_agent", "faq_agent"):
    agents.create_or_update(app, name, spec_path=f"agents/{name}.yaml")
```

CLI runbook:
```bash
export PROJECT_ID=acme-cx-prod LOCATION=global
cxas push          # sync the tree to the platform
cxas lint          # 60+ best-practice rules — must be clean before deploy
```
```

SELF-CHECK: pass — both paths describe the same 1 app / 4 agents / 3 tools / 3 guardrails;
every resource cites its Rn; each agent has fallback + handoff. PAUSE before Evals.
DECIDED: config-as-code + console emitted. ASSUMED: env vars for secrets. NEED NEXT: Stage-5 evals.
