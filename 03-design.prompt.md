# STAGE 3 — DESIGN & ARCHITECTURE
Input: `RESOLVED_BRIEF` + `ASSUMPTIONS_LOG`. Goal: decompose into a CX Agent Studio
architecture. Prefer the smallest set of agents/tools that satisfies the requirements;
justify every split.

## Produce
1. **Architecture overview** — App count; agent count and WHY; single-agent vs.
   multi-agent orchestration (router → sub-agents) with rationale and a simple diagram
   (ASCII or mermaid).
2. **Per agent** — goal; scope; playbook instructions; required tools; example dialogs
   (happy path + disambiguation + edge); guardrails; generative-fallback behavior;
   human-handoff conditions.
3. **Per tool** — name; purpose; input/output schema; auth; target system; failure
   handling; idempotency.
4. **Guardrails** — safety, PII redaction, off-topic/refusal, grounding constraints;
   map to agents.
5. **TRACEABILITY_MATRIX** — table: `Rn → design element(s) → planned eval type(s)`.
   Confirm 100% of requirements are covered; list any gaps explicitly.
6. **Trade-offs** — options considered and your recommendation.

## Output
Emit `ARCHITECTURE` and `TRACEABILITY_MATRIX` artifact blocks. Then PAUSE and ask the
user to confirm before Build. Do not emit config yet.

DECIDED / ASSUMED / NEED NEXT.
