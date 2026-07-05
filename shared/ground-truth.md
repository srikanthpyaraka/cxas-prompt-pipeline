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

## cxas-scrapi framework
- Python modules mapped to resources: `Apps`, `Agents`, `Tools`, `Guardrails`,
  `Deployments`, `Sessions`, `Variables`.
- Config-as-code: `cxas pull` (platform → disk) and `cxas push` (disk → platform),
  producing a directory tree (`app/`, `agents/`, `tools/`, `guardrails/`, `examples/`).
- `cxas lint` — validates configs against **60+ best-practice rules**.
- Auth: Application Default Credentials (`gcloud auth application-default login`),
  environment credentials on Cloud Run/Functions, or an explicit `creds_path`.
- Common constructors take `project_id=...`, `location='global'` (or region).

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
