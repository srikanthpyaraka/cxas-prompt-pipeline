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

=== PART B — CONFIG-AS-CODE ===
(In current guidance the code path delegates to the official cxas-agent-foundry skill —
`inspect-app.py`, `cxas push`, lint via its `lint-fixer` sub-agent. Raw scrapi shown below
for illustration of the underlying resources.)
Real cxas pull/push tree (JSON; resource-per-folder; instructions + code as separate files):
```
cxas_app/OrderBot/
  app.json                       # displayName, rootAgent:"router",
                                 #   variableDeclarations:[...], evaluationMetricsThresholds, loggingSettings
  agents/router/
    router.json                  # instruction:"agents/router/instruction.txt",
                                 #   childAgents:["order_status_agent","returns_agent","faq_agent"], tools:["end_session"]  [R4]
    instruction.txt
  agents/order_status_agent/order_status_agent.json + instruction.txt   # tools:["get_order_status"]  [R1]
  agents/returns_agent/returns_agent.json + instruction.txt             # tools:["create_return"]     [R2]
  agents/faq_agent/faq_agent.json + instruction.txt                     # tools:["search_kb"]         [R3]
  tools/get_order_status/get_order_status.json    # {"openApiTool":{...}}   [R1]
  tools/create_return/create_return.json          # openApiTool (write)     [R2]
  tools/search_kb/search_kb.json                  # dataStoreTool (grounding) [R3]
  evaluations/… evaluationExpectations/…          # goldens (Stage 5) live here
```
Real-format notes: guardrails (PII redaction / PCI block / off-topic refusal) are app/agent
safety config — Cloud DLP for redaction — not a `guardrails/` folder; sub-agents are the
router's `childAgents`; variables live in `app.json.variableDeclarations`.

Push:
```bash
export PID=acme-cx-prod LOC=global
cxas push --app-dir cxas_app/OrderBot --to projects/$PID/locations/$LOC/apps/$APP_ID \
  --project-id $PID --location $LOC
# then lint via cxas-agent-foundry's lint-fixer sub-agent (don't run cxas lint on the main thread)
```
```

SELF-CHECK: pass — 1 app / 4 agents (router + 3 childAgents) / 3 tools / safety config;
every resource cites its Rn; each agent has fallback + handoff. PAUSE before Evals.
DECIDED: config-as-code + console emitted. ASSUMED: env vars for secrets. NEED NEXT: Stage-5 evals.
