# STAGE 5 — EVALS (design + generate; dual-emit)
Input: `ARCHITECTURE` + `BUILD_PACKAGE` + `TRACEABILITY_MATRIX`. Goal: generate a
concrete evaluation suite covering all five eval types, with measurable thresholds tied
to KPIs, and EVERY requirement covered by ≥1 eval.

## Generate assets across all five types (where applicable)
1. **Platform Goldens** — golden conversations + expected outcomes.
2. **Local Simulations** — multi-turn personas incl. adversarial/edge cases.
3. **Tool Tests** — per-tool input→expected-output cases INCLUDING failure paths.
4. **Callback Tests** — pre/post-processing / callback logic checks.
5. **Turn Evals** — turn-level assertions (right tool chosen, grounded answer, no PII leak).

## Thresholds (tie to KPIs from the brief)
Set explicit pass/fail bars, e.g. tool-call accuracy ≥ 0.95, response-match ≥ target,
latency ≤ budget, 0 PII leaks. State metric, target, and rationale for each.

## Dual-emit run instructions
- **Console:** where/how to run goldens & simulations in the CX Agent Studio UI.
- **Config-as-code:** evals-module calls (ToolEvals, SimulationEvals, CallbackEvals,
  GuardrailEvals) + CLI (`cxas test-tools`, `cxas test-callbacks`, `cxas push-eval`),
  parameterized by `project_id`/`location`.

## Coverage
Emit a coverage table `Rn → eval id(s) → type`. Report **coverage %**; if < 100%, list
the uncovered requirements and add evals until covered.

## Output
Emit `EVAL_SUITE` (assets + thresholds + run commands + coverage report) in an artifact
block. Then PAUSE for confirmation before Validate.

DECIDED / ASSUMED / NEED NEXT.
