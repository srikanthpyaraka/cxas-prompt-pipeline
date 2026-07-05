# Independent review — CX Agent Builder prompt package

Reviewer pass over the whole package: the seven prompts, the shared contract, the assessor,
and the two worked examples. Scope: correctness, best-practice adherence, and readiness to
share with Google Enterprise CX (GECX) developers.

## Verdict
**Ship-worthy as a v0.1 reference package.** The design is sound (gated pipeline,
config-as-code + console dual-emit, eval-first, now with a debug-fix loop). The main
caveats are about *provenance and executability*, documented below — none are blockers for
sharing, but they set honest expectations.

## Validation performed
Checked each example against the prompts' output contract and per-stage requirements:

| Check | Result |
|-------|--------|
| Stage announced + `DECIDED/ASSUMED/NEED NEXT` closer on every stage | ✅ |
| Artifacts wrapped in `artifact:<NAME>` envelopes | ✅ |
| Requirement records match the schema; IDs stable across stages | ✅ |
| Interview gate emits questions + `RESOLVED_BRIEF` + `ASSUMPTIONS_LOG` + `GATE PASSED` | ✅ |
| Dual-emit (console **and** cxas-scrapi) in Build & Evals | ✅ |
| All 5 eval types present; 100% requirement→eval coverage | ✅ (order-support 9/9, Cymbal 10/10) |
| Validate gate: lint audit, 0 blockers, sign-off | ✅ |
| Debug-fix: root cause + minimal fix + regression eval (RED→GREEN), coverage not reduced | ✅ (BUG-01) |

## Strengths
1. **Interview gate is the differentiator** — forces disambiguation before any build, with
   batched, defaulted questions. This is where most agent projects go wrong.
2. **Traceability end-to-end** — every requirement → design element → eval; coverage is a
   first-class, reported number.
3. **Dual-emit** keeps UI-built and CI/CD-built teams in sync from the same source.
4. **Debug-fix loop closes the lifecycle** — bugs produce documented root cause + a
   regression eval, not just a patch.
5. **Self-referential quality** — the assessor scores the package's own prompts, and a bug
   in the assessor's own rubric (weights summed to 95) was caught and fixed.

## Risks / limitations (be upfront with developers)
1. **Examples are authored reference runs, not live transcripts.** They conform to the
   contracts and are QA'd, but were not produced by executing the orchestrator. Labeled as
   such in each example README. *Recommendation:* capture one genuine live run before a
   public launch.
2. **cxas-scrapi API surface is approximate.** Method names like `create_or_update(...)` and
   the `Variables`/`Guardrails` module usage follow the documented shape but should be
   pinned against the installed version — the scrapi API may differ. *Recommendation:* add a
   smoke-test script that imports the real package and validates the calls.
3. **Platform facts have a shelf life.** "One sample agent (Cymbal), as of Nov 2025" and the
   eval taxonomy names will drift. *Recommendation:* date-stamp `shared/ground-truth.md` and
   re-verify per release.
4. **No license yet** — public repo without a LICENSE blocks legal reuse. *Recommendation:*
   add Apache-2.0.
5. **KPI targets in examples are assumed** (e.g., containment ≥ 0.45). Correct behavior
   (they're logged as assumptions), but a demo viewer should know they're illustrative.

## Recommended next steps (priority order)
1. Add LICENSE (Apache-2.0) + a non-affiliation disclaimer.
2. Capture one real end-to-end orchestrator run and commit it as the canonical example.
3. Add a scrapi smoke test to pin the real API.
4. Date-stamp ground-truth and set a re-verify cadence.
