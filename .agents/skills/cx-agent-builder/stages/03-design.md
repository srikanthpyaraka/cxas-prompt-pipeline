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

## Example (agent spec + traceability shape)
<example>
Agent: `order_status_agent`
- Goal: resolve "where is my order" without human handoff when data is available.
- Tools: `get_order_status` (read-only OMS). Guardrails: PII redaction, off-topic refusal.
- Fallback: if OMS returns no match after 2 turns → offer handoff. Satisfies: R1, R2.

| Req | Design element(s) | Planned eval type(s) |
|-----|-------------------|----------------------|
| R1  | order_status_agent + get_order_status tool | Tool Test, Turn Eval, Platform Golden |
| R2  | PII-redaction guardrail | Turn Eval (no PII leak), Local Simulation |
</example>

DECIDED / ASSUMED / NEED NEXT.
