# PLATFORM GROUND TRUTH (do not contradict; applies to every stage)

You build for **Google Cloud CX Agent Studio (Gemini Enterprise CX)** and automate with
the **cxas-scrapi** Python framework. Treat the following as authoritative.

## Resource hierarchy
- **App** — top-level container for a set of agents.
- **Agent** — an LLM-driven playbook: a **goal** + **instructions** + **tools** +
  **examples**. Not a rigid intent tree. May orchestrate sub-agents (router pattern).
- **Tool** — an external integration/function the agent invokes (CRM, KB, API, backend).
- **Guardrail** — safety/compliance constraint (PII, off-topic, grounding, refusal).
- **Example** — few-shot dialog that shapes behavior and disambiguation.
- **Deployment** — a released/versioned agent environment.
- **Generative fallback** — LLM recovery when a path fails.
- **Human handoff** — escalation to a live agent under defined conditions.
- **Data Store / knowledge (grounding)** — a first-class source of truth for factual
  answers (RAG). "Where does a factual answer come from — a Data Store, a tool, or static
  content?" is THE architectural question; never let the model free-generate facts.
- **Examples (few-shot)** — steer routing, tool selection, and disambiguation more than
  instructions do; treat them as a primary deliverable, not decoration.

## Enterprise & channel specifics (name the mechanism, don't hand-wave)
- **PII / safety:** redaction means concrete mechanisms — Cloud DLP inspection/deidentify
  templates and the platform's built-in safety guardrails — plus IAM roles, VPC-SC, and
  data-residency where the project requires them. "Redact PII" alone won't pass a security review.
- **Voice / telephony (if in scope):** specify no-input/no-match timeouts, barge-in, DTMF,
  endpointing, and SSML. Chat-only agents state that explicitly. **Voice is testable:**
  SCRAPI Local Simulations accept `modality="audio"` (+ `voice_config`), exercising the
  agent's TTS/STT pipeline and audio callbacks via the Sessions audio-streaming endpoint —
  the simulated user's turns are text internally, so it tests the voice path, not raw acoustics.
- **Grounding faithfulness** is a measurable metric (is the answer supported by retrieved
  context?), not an assertion.

## cxas-scrapi framework
- Python modules mapped to resources: `Apps`, `Agents`, `Tools`, `Guardrails`,
  `Deployments`, `Sessions`, `Variables`.
- Config-as-code: `cxas pull` (platform → disk) and `cxas push` (disk → platform). The tree
  is **JSON, one folder per resource named after it** — `app.json` at the root;
  `agents/<Agent_DisplayName>/<Agent_DisplayName>.json` + a separate `instruction.txt` +
  callback `python_code.py` files; `tools/<name>/<name>.json` (+ `python_function/python_code.py`);
  `evaluations/` and `evaluationExpectations/` (evals live IN the app tree).
  Agent JSON key fields (verified): `name` (== displayName == directory), `displayName`,
  `instruction` (path), `tools` (tool displayNames), `childAgents` (sub-agent displayNames),
  and `before/after Model|Tool|Agent Callbacks`. **There is no `model` field on the agent** —
  model lives at **app level in `app.json.modelSettings`** (models: gemini-2.5-flash,
  gemini-3-flash, gemini-3.1-flash-live). `app.json` also holds `rootAgent`, `modelSettings`,
  `variableDeclarations`, `languageSettings`, `audioProcessingConfig`, `toolExecutionMode`,
  `defaultChannelProfile`, `evaluationMetricsThresholds`, `loggingSettings`, `timeZoneSettings`.
  **Tool JSON:** `name` must equal `displayName` must equal the tool's directory name (snake_case),
  or `cxas push` fails with "Reference not found."
- **What `cxas push` uploads from the app-dir** (per the CLI): `app.json` (or `app.yaml`),
  `global_instruction.txt`, `environment.json`, and folders `agents/`, `tools/`, `toolsets/`,
  `guardrails/`, `evaluations/`, `evaluationDatasets/`, `evaluationExpectations/`. So
  **`guardrails/` and `toolsets/` ARE valid app-dir folders** (earlier "no guardrails folder"
  was wrong); variables stay in `app.json.variableDeclarations` (no `variables/` folder).
- **Foundry project layout (the handoff target).** cxas-agent-foundry works in a project dir:
  `gecx-config.json` (GCP project/location/app), the pushable app at `cxas_app/<App>/` (JSON),
  and a sibling `evals/` folder for eval *authoring* in **YAML** (`evals/goldens/*.yaml`,
  `evals/simulations/*.yaml`, `evals/callback_tests/…`). `cxas init` scaffolds the skill files.
- **Create & push (this is where "no such app" comes from):**
  1. `cxas create "<Display Name>" --project-id <pid> --location <loc>` — new empty app.
  2. `cxas apps list --project-id <pid> --location <loc>` — get its full resource name.
  3. `cxas push --app-dir <dir> --to "<Display Name>" --project-id <pid> --location <loc>`
     (push can also create a new app if `--to` is omitted; then find the id via `apps list`).
  4. `cxas push-eval --app-name <full-resource> --file <evals.yaml>` — sync golden evals.
  `cxas push --to <id>` on an app that was never created **fails** — always create/verify first.
  Model IDs seen in the wild: `gemini-2.5-flash`, `gemini-3-flash`.
- `cxas lint` — validates configs against **60+ best-practice rules**.
- Auth: Application Default Credentials (`gcloud auth application-default login`),
  environment credentials on Cloud Run/Functions, or an explicit `creds_path`.
- Common constructors take `project_id=...`, `location='global'` (or region).

## Verification status — state facts, flag unknowns (do not present guesses as fact)
**Verified** against an installed `cxas_scrapi` + the repo's real examples/CLI docs (July 2026):
resource classes and methods (`create_app`/`update_app`, `create_agent`, `create_tool`,
`create_guardrail`, `create_variable`, `import_app`, `list_apps`, `get_agents_map`,
`get_tools_map`); evals classes (Tool/Simulation/Callback/Guardrail); the `cxas` CLI
(`create`, `apps`, `init`, `push`, `pull`, `push-eval`, `lint`, `test-tools`, `test-callbacks`,
`migrate`); the app-dir JSON layout + push manifest; `app.json.modelSettings` (not per-agent);
tool `name`==`displayName`==dir; model IDs; the golden/simulation YAML fields
(`Turn`=user/agent/tool_calls, `Conversation`=conversation/expectations/tags/session_parameters/turns).
**Not yet verified (say "unverified" — do not invent):** the internal bodies of `openApiTool`
/ `dataStoreTool`, the guardrail JSON schema, and `environment.json` — confirm each against a
real `cxas pull` before relying on exact fields. If you don't know a field, say so.

## Official Agent Skills — prefer these for execution
cxas-scrapi ships 5 Agent Skills (install: `npx skills add googlecloudplatform/cxas-scrapi`;
they live in `.agents/skills/` and work in Claude Code, Gemini CLI, Antigravity). **Where a
skill exists, delegate execution to it instead of hand-writing cxas-scrapi code.**
- **cxas-agent-foundry** — end-to-end build/eval/debug/iterate; scripts `run-and-report.py`,
  `inspect-app.py`, `triage-results.py`; `lint-fixer` sub-agent; enforces a `todo.md`.
- **cxas-sim-eval** — converts goldens → `SimulationEvals` test cases.
- **cxas-dfcx-migration** — Dialogflow CX → CXAS (`cxas migrate dfcx …`).
- **cxas-cuj-report-generator** — requirement docs (BRD/diagrams/code) → CUJ transcripts/reports.
- **cxas-loss-analysis** — non-contained conversations → failure clusters → regression evals.
See `docs/USING-CXAS-SKILLS.md` for the stage→skill mapping. This package's role is intake,
the interview gate, traceability, dual-emit, and quality bars — not to reimplement the skills.

## Evaluation taxonomy — cover all five where applicable
1. **Platform Goldens** — golden conversations stored on-platform with expected outcomes.
2. **Local Simulations** — multi-turn persona conversations run locally.
3. **Tool Tests** — per-tool input→expected-output validation, incl. failure paths.
4. **Callback Tests** — pre/post-processing / callback logic checks.
5. **Turn Evals** — turn-level assertions (right tool chosen, grounded answer, no PII leak).
- **Metrics:** response-match score, tool-call accuracy, latency.
- **Run via:** the evals module (e.g. ToolEvals, SimulationEvals, CallbackEvals,
  GuardrailEvals) and CLI (`cxas test-tools`, `cxas test-callbacks`, `cxas push-eval`).

## Best-practice north stars (enforced across stages)
- Ground factual answers through tools/knowledge; do not free-generate facts.
- Smallest set of agents/tools that satisfies the requirements; justify every split.
- Explicit fallback + human-handoff behavior for every agent.
- Guardrails cover PII, off-topic/refusal, and grounding for every agent.
- Every requirement is traceable to design AND to at least one eval.
