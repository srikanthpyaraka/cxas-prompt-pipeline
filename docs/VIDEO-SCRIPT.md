# Demo video — voiceover script & recording guide

Pairs with **`docs/demo-reel.html`** — a self-running, auto-advancing reel (12 scenes,
~2:55). You full-screen it, hit record, and read the narration below in sync. No editing
tools required.

## How to record (5 minutes)
1. Open `docs/demo-reel.html` in Chrome. Press **F** for fullscreen, **R** to restart from
   scene 1. It auto-advances; **Space** pauses, **← →** step, **C** toggles the on-screen
   captions.
2. Start a screen recording: **QuickTime → File → New Screen Recording** (pick the mic),
   or Loom/OBS. Record at 1080p; make the browser window 16:9.
3. Press **R**, then start reading the VO below. Each scene's duration is fixed — the
   timings are your teleprompter. If you talk faster, press **Space** to hold a scene.
4. Decide on captions: leave them **on** (good for muted viewing / accessibility) or press
   **C** to hide them if you'd rather the visuals carry your voice alone.
5. Stop on the final scene. Trim the head/tail. Done.

## Voiceover (timed to the reel)

**Scene 1 — Title · 0:00–0:12**
> "This is CX Agent Builder. The idea is simple: a product requirements doc goes in, and a
> designed, built, and fully-evaluated CX Agent Studio agent comes out."

**Scene 2 — Problem · 0:12–0:26**
> "Today that translation is manual. A developer hand-converts the PRD into agents, tools,
> and guardrails — details drop, it ships under-tested, and there's no record of why it was
> built that way."

**Scene 3 — The pipeline · 0:26–0:44**
> "So we made it a pipeline: seven stages with two hard gates. Ingest, interview, design,
> build, evals, validate, ship. And a seventh stage — debug and fix — that runs as a loop:
> any failing eval becomes a documented root cause and a regression test. It's
> model-agnostic; Claude or Gemini."

**Scene 4 — How it fits · 0:44–1:00**
> "Importantly, this sits on top of Google's official cxas-scrapi Agent Skills — it doesn't
> replace them. This package owns intake, the interview gate, traceability, and quality
> bars; the official skills do the actual building, evaluating, and debugging on-platform."

**Scene 5 — Ingest · 1:00–1:12**
> "Stage one takes any PRD and normalizes it into numbered requirements, each with a
> priority. Crucially, when something's missing, it flags it as unknown — it never invents
> the answer."

**Scene 6 — Interview · 1:12–1:30**
> "Then the part that sets it apart: it interviews you. Batched, prioritized questions, each
> with a sensible default — and it will not start designing until the blocking questions are
> answered. Most agent projects fail right here. We turned it into a gate."

**Scene 7 — Design · 1:30–1:42**
> "Stage three designs the architecture — the smallest set of agents, tools, and guardrails
> that satisfies the spec — and ties every requirement to a design element and a test in a
> traceability matrix."

**Scene 8 — Dual-emit · 1:42–1:58**
> "Stage four is the one engineers love. The same resources come out twice: a console
> runbook for teams building in the UI, and cxas-scrapi config-as-code for CI/CD. One source
> of truth, two paths, always in sync."

**Scene 9 — Evals · 1:58–2:12**
> "Stage five generates all five evaluation types — goldens, simulations, tool tests,
> callback tests, and turn evals — with thresholds tied to your KPIs. Every requirement has
> at least one test: a hundred percent coverage."

**Scene 10 — Debug → regression · 2:12–2:30**
> "And when something breaks, stage seven closes the loop. Here an eval caught the agent
> upselling during checkout. It finds the root cause in a callback, applies a one-line fix
> that generalizes, and adds a new regression test — red before, green after. Coverage goes
> up, not down."

**Scene 11 — Why it holds up · 2:30–2:42**
> "So it holds up because it's engineering discipline, not a clever one-shot prompt:
> traceable, grounded in tools, self-auditing, and covering the whole lifecycle."

**Scene 12 — Call to action · 2:42–2:55**
> "Clone it, point stage one at a real PRD, and answer the interview. You'll get a console
> runbook, cxas-scrapi config, and a runnable eval suite. The repo's on GitHub — feedback
> and pull requests welcome."

## Tips
- Speak slightly slower than feels natural; the reel's pacing has slack.
- If you fluff a line, pause (Space), breathe, resume — trim it later.
- For a 60-second cut, record only scenes 1, 3, 4, 6, 8, and 12.
