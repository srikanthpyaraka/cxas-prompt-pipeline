# Demo talk track — CX Agent Builder (for GECX developers)

A ready-to-present script for demoing the package to Google Enterprise CX (GECX)
developers building on CX Agent Studio. Target length: **8–10 minutes**. Repo:
https://github.com/srikanthpyaraka/cxas-prompt-pipeline

---

## 0. One-liner (say this first, 15s)
> "This turns a PRD into a fully-built, fully-evaluated CX Agent Studio agent — with an
> interview gate so it never builds on guesses, output as both console steps and
> cxas-scrapi config, 100% eval coverage, and a debug loop that turns every bug into a
> regression test."

## 1. The problem (30s)
Teams write a PRD, then a developer hand-translates it into agents, tools, guardrails, and
evals. It's slow, inconsistent between people, under-tested, and undocumented. The gap
between "PRD" and "a CX Agent Studio app you'd trust in production" is manual and lossy.

## 2. The idea (30s)
A prompt **pipeline**, not a single prompt: an orchestrator drives seven stages with two
hard gates. It's model-agnostic (Claude, Gemini) and grounds every output in real CX Agent
Studio resources and the cxas-scrapi framework.

```
1 INGEST → 2 INTERVIEW ◆gate◆ → 3 DESIGN → 4 BUILD → 5 EVALS → 6 VALIDATE ◆gate◆ → SHIP
                                                     ⤷ 7 DEBUG & FIX (loop)
```

## 3. Live demo (5–6 min) — use `examples/cymbal-retail/`
Demo against **CX Agent Studio's own default sample** (Cymbal Home & Garden) so developers
can diff the output against the console.

1. **Show the input** — `00-prd.md`. "A realistic, deliberately imperfect PRD."
2. **Ingest** — `01-normalized-brief.md`: "10 requirements, each with an ID and priority;
   note it flags the UNKNOWNs instead of inventing — e.g., no KPI was stated."
3. **Interview gate** — `02-interview.md`: "This is the differentiator. It won't design
   until P0 questions are answered — batched, prioritized, each with a default. Here it
   pins the upsell policy and the manager-discount approval rule."
4. **Design** — `03-architecture.md`: "It reconstructs the sample's real shape — root
   `cymbal_retail_agent` + upsell + out-of-scope sub-agents, the OpenAPI/Python/Search
   tools, variables, guardrails, callbacks — and every element cites the requirement it
   satisfies."
5. **Build (the money slide)** — `04-build-package.md`: "Same resources emitted **twice**:
   a console runbook for UI teams and cxas-scrapi config + Python + `cxas push/lint` for
   CI/CD. One source of truth, two paths."
6. **Evals** — `05-eval-suite.md`: "All five cxas eval types — goldens, simulations, tool
   tests, callback tests, turn evals — with KPI-tied thresholds and a coverage table.
   100%. Every requirement has at least one test."
7. **Debug & Fix (the closer)** — `07-bugfix.md`: "A turn eval failed — the agent upsold
   during checkout. Watch the loop: reproduce → root cause (the `after_model` callback
   suppressed on complaints but never on cart state) → a one-line minimal fix → and a new
   regression eval `TE-02b` that was RED before and GREEN after. Coverage went up, not
   down. The fix generalizes; it's not a test patch."

## 4. Why it's good engineering (45s)
- **Traceability:** requirement → design → eval, with coverage as a number.
- **Grounded, not generative:** product facts route through tools; guardrails on every agent.
- **Best-practice prompts:** audited by an included assessor skill (`PROMPT-ASSESSOR`),
  which even caught a weighting bug in its own rubric.
- **Lifecycle, not one-shot:** the debug-fix loop makes every bug a permanent test.

## 5. Honest caveats (30s — say these, they build trust)
- The committed examples are **authored reference runs**, not live transcripts (labeled).
- cxas-scrapi method names follow the documented shape — **pin them to your installed
  version**; a smoke test is on the roadmap.
- Ground-truth (e.g., "one sample agent as of Nov 2025") needs periodic re-verification.

## 6. Call to action (20s)
> "Clone it, point stage 1 at one of your real PRDs, and answer the interview. You'll get a
> console runbook, cxas-scrapi config, and an eval suite you can run with `cxas`. Try
> breaking an agent and run stage 7 — you'll get a documented root cause and a regression
> test. Feedback and PRs welcome."

## Q&A — likely questions
- **"Does it run cxas-scrapi for me?"** No — it *generates* the scripts/config + `cxas`
  commands; you execute them against your GCP project. Keeps it safe and reviewable.
- **"Gemini or Claude?"** Model-agnostic. The prompts follow general best practices; load
  the three shared/orchestrator files as system context in either.
- **"How is this different from 'Start with AI' in the console?"** Complementary. This adds
  the *interview gate*, *traceability*, *dual-emit for CI/CD*, and an *eval + regression*
  discipline around whatever you build — in or out of the console.
- **"Can I customize the eval thresholds?"** Yes — they're set in the interview from your
  KPIs and live in the EVAL_SUITE artifact.

## Leave-behind
- Repo + README quickstart · `examples/cymbal-retail/` (verifiable vs. console) ·
  `docs/REVIEW.md` (honest risk list) · `PROMPT-ASSESSOR.prompt.md` (audit your own prompts).
