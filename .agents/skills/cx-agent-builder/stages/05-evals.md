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
Set explicit pass/fail bars and state metric, target, and rationale for each. Cover the
metrics CX projects are actually judged on, not just response-match:
- **Grounding faithfulness** (answer supported by retrieved context) — required wherever a
  Data Store / RAG grounds an intent.
- **Containment** and **escalation rate** (tie to the brief's KPIs).
- **Tool-call accuracy** ≥ 0.95 · **latency** ≤ budget (voice budgets differ from chat) ·
  **0 PII / safety leaks** (hard bar).

## Eval realism (mandatory — LLM outputs are non-deterministic)
- **Run multiple times** to handle variance (foundry's `run-and-report.py --runs 5`); report
  pass *rates*, not a single lucky green.
- **Mock tools** so evals are deterministic and don't hit live backends; test failure paths.
- **Assert semantically**, not by exact string match — check intent/outcome/tool-choice,
  not verbatim wording, or evals will be flaky.

## Voice agents — run simulations in audio modality
If the agent handles voice (per the Stage-3 channel decision), run Local Simulations in
**`modality="audio"`** (default is `"text"`), which uses the Sessions API audio-streaming
endpoint and exercises the agent's TTS/STT pipeline and audio callbacks:
```python
simulation.run(test_case=tc, modality="audio",
               voice_config={"language_code": "en-US", "voice_name": "en-US-Standard-A"})
```
Caveat to set expectations: the simulated user's turns are still text internally, so this
tests the voice *path* (TTS/STT + audio callbacks), not real acoustic robustness (noise,
accents, human-ASR error). Semantic assertion matters even more here (phrasing varies more
in voice). Cover DTMF / no-input / no-match / barge-in paths as their own simulation cases.

## Dual-emit run instructions (delegate to skills)
- **Console:** where/how to run goldens & simulations in the CX Agent Studio UI.
- **Config-as-code (prefer official skills):**
  - Run + triage + report in one shot with **cxas-agent-foundry**:
    `python .agents/skills/cxas-agent-foundry/scripts/run-and-report.py --message "<what changed>" --runs 5`.
  - Generate `SimulationEvals` from turn-by-turn goldens with **cxas-sim-eval** (it will
    ask for the full app resource name + output dir).
  - Fall back to direct evals-module calls (ToolEvals, SimulationEvals, CallbackEvals,
    GuardrailEvals) / `cxas test-tools` / `cxas test-callbacks` only where a skill doesn't cover it.

## Coverage
Emit a coverage table `Rn → eval id(s) → type`. Report **coverage %**; if < 100%, list
the uncovered requirements and add evals until covered.

## Output
Emit `EVAL_SUITE` (assets + thresholds + run commands + coverage report) in an artifact
block. Then PAUSE for confirmation before Validate.

## Example (eval case + coverage shape)
<example>
Tool Test `TT-01` (get_order_status): input `{order_id:"A123"}` → expect status field
present; failure path input `{order_id:"NOPE"}` → expect graceful "not found", no crash.
Threshold: tool-call accuracy ≥ 0.95. Runs via `cxas test-tools`.  Covers: R1.

| Req | Eval id(s) | Type |
|-----|-----------|------|
| R1  | TT-01, TE-04, PG-02 | Tool Test, Turn Eval, Platform Golden |
| R2  | TE-07, SIM-03 | Turn Eval (0 PII leaks), Local Simulation |

Coverage: 2/2 requirements = 100%.
</example>

DECIDED / ASSUMED / NEED NEXT.
