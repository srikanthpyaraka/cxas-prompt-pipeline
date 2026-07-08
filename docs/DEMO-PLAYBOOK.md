# Demo playbook — install → overview → run (operator's guide)

The end-to-end sequence for giving the demo yourself. Pairs with `DEMO-RUNSHEET.md`
(minute-by-minute), `DEMO-TALK-TRACK.md` (script), and `demo-reel.html` (video reel).

---

## Phase 0 — Prep the night before (10 min, do this once)
1. **Get the repo locally** (it's private, so you need access):
   ```bash
   git clone https://github.com/srikanthpyaraka/cxas-prompt-pipeline.git
   cd cxas-prompt-pipeline
   ```
2. **Install the skill into Claude Code** (personal skills folder):
   ```bash
   mkdir -p ~/.claude/skills
   cp -R .agents/skills/cx-agent-builder ~/.claude/skills/
   ```
   Restart Claude Code so it loads. (Gemini CLI / Antigravity read `.agents/skills/`
   directly; `npx skills add …` only works once the repo is public.)
3. **Smoke-test it:** open Claude Code and type `demo`. Confirm it runs Stage 1→2 and asks
   interview questions. If it doesn't trigger, paste `dist/cx-agent-builder.system.md` and
   type `demo` (the no-install fallback — always works).
4. **Open tabs** you'll show: `README.md`, `examples/cymbal-retail/`, `docs/demo-reel.html`,
   and (optional) the CX Agent Studio console on the Cymbal sample.

## Phase 1 — Repo overview (2 min, on screen)
Show the tree and say what each part is:
```
cx-agent-builder/
├── 00-orchestrator … 07-debug-fix.prompt.md   ← the 7-stage pipeline (the engine)
├── PROMPT-ASSESSOR.prompt.md                   ← audits/rewrites any prompt to best practice
├── shared/ (ground-truth, output-contract)     ← platform facts + global output rules
├── .agents/skills/cx-agent-builder/            ← the installable Skill (what you just installed)
├── dist/cx-agent-builder.system.md             ← one-file paste bundle (no-install path)
├── examples/ (order-support, cymbal-retail)    ← full worked runs, end to end
└── docs/ (deck, reel, runsheet, talk-track, REVIEW, USING-CXAS-SKILLS)
```
One-breath pitch: *"Seven prompt stages with two hard gates. It takes a PRD, interviews you,
designs the agent, emits it as both console steps and cxas-scrapi code, writes a full eval
suite, and turns bugs into regression tests. It sits on top of Google's official cxas-scrapi
skills and delegates the on-platform work to them."*

## Phase 2 — Install, live (1 min)
Show the two lines from Phase 0 step 2, then: *"That's it — it's now a skill Claude picks up
by description. Your team runs one copy command, or `npx skills add …` once this is public."*

## Phase 3 — Run it (5–7 min, the main event)
Pick ONE path:

**Path A — Live skill run (most impressive if it behaves):**
1. In Claude Code type: **`build a CX Agent Studio agent from this PRD`** and paste the
   SkyHelp PRD from `DEMO-RUNSHEET.md` (or just type **`demo`**).
2. Narrate as it goes: Ingest → numbered requirements (flags UNKNOWNs) → **Interview: it
   stops and asks** (the wow moment) → answer a couple → Design → note dual-emit at Build.
3. **Time-box it.** After the interview + a peek at design, switch to the finished example.

**Path B — Guided walkthrough (zero risk, always works):**
1. Play `docs/demo-reel.html` full-screen (F) for the 2:55 overview, OR
2. Walk the `examples/cymbal-retail/` tabs `00`→`07` and, if you have it open, **diff
   `03-architecture.md` against the Cymbal sample in the console** (the credibility moment).

**The three moments to land** (either path): the **interview gate**, the **dual-emit**
(console + cxas-scrapi), and **debug → regression** (`07-bugfix.md`).

## Phase 4 — Close (1 min)
- CTA: *"Install it, point Stage 1 at a real PRD, answer the interview — you get a runbook,
  cxas-scrapi config, and a runnable eval suite."*
- **Say the honest caveats** (builds trust): examples are authored reference runs; pin the
  scrapi API to your installed version; it hasn't been run against a live project yet. (Full
  list: `docs/REVIEW.md`.)
- Leave-behind: repo link + `USAGE.md`.

## If you want the audience to install it themselves
The repo is currently **private**, so `npx skills add …` won't resolve for them. Either add
them as collaborators, or make it public for the session:
```bash
gh repo edit srikanthpyaraka/cxas-prompt-pipeline --visibility public --accept-visibility-change-consequences
# (revert with --visibility private afterwards)
```

## Fallbacks (keep calm)
- Skill won't trigger → paste `dist/cx-agent-builder.system.md`, type `demo`.
- Live gen drifts → narrate from the expected-output tables in `DEMO-RUNSHEET.md`.
- Console won't load → skip the diff; "you can verify the generated architecture against the sample."
- "Does it deploy?" → "It generates the scripts + `cxas` commands; you run them. Safe and reviewable."
