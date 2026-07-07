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
- Config-as-code: `cxas pull` (platform → disk) and `cxas push` (disk → platform),
  producing a directory tree (`app/`, `agents/`, `tools/`, `guardrails/`, `examples/`).
- `cxas lint` — validates configs against **60+ best-practice rules**.
- Auth: Application Default Credentials (`gcloud auth application-default login`),
  environment credentials on Cloud Run/Functions, or an explicit `creds_path`.
- Common constructors take `project_id=...`, `location='global'` (or region).

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
