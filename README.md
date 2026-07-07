# CX Agent Builder — Prompt Package

> **PRD in → a designed, built, and evaluated CX Agent Studio agent out.**
> An interview gate so it never builds on guesses · output as **both** console steps and
> `cxas-scrapi` config · **100% eval coverage** · a debug loop that turns every bug into a
> regression test. Model-agnostic (Claude or Gemini).
>
> **Fastest start (installable Skill):** `npx skills add srikanthpyaraka/cxas-prompt-pipeline`
> — then just ask "build a CXAS agent from this PRD" (it auto-triggers), or type **`demo`**.
> No-install alternative: paste [`dist/cx-agent-builder.system.md`](dist/cx-agent-builder.system.md)
> into Claude/Gemini, then **`demo`**. See [`QUICKSTART.md`](QUICKSTART.md).
>
> **Presenting this?** → [`docs/DEMO-PLAYBOOK.md`](docs/DEMO-PLAYBOOK.md) (install→overview→run) ·
> [`docs/DEMO-RUNSHEET.md`](docs/DEMO-RUNSHEET.md) (runsheet) ·
> [`docs/DEMO-TALK-TRACK.md`](docs/DEMO-TALK-TRACK.md) (script) ·
> [`docs/demo-reel.html`](docs/demo-reel.html) (record-ready reel) ·
> [`examples/cymbal-retail/`](examples/cymbal-retail/) (walkthrough vs. the console).

A modular, chainable prompt system that turns **any input describing a desired
customer-experience agent** (a formal PRD, meeting notes, tickets, or bullet points)
into a **designed, built, and evaluated Google Cloud CX Agent Studio (Gemini
Enterprise CX) agent** using the **cxas-scrapi** framework.

> **Works with the official cxas-scrapi Agent Skills.** cxas-scrapi ships 5 skills
> (`cxas-agent-foundry`, `cxas-sim-eval`, `cxas-dfcx-migration`, `cxas-cuj-report-generator`,
> `cxas-loss-analysis`). This package is the **intake + interview + traceability + dual-emit
> layer**; it **delegates on-platform build/eval/debug to those skills**. Install:
> `npx skills add googlecloudplatform/cxas-scrapi`. Mapping: [`docs/USING-CXAS-SKILLS.md`](docs/USING-CXAS-SKILLS.md).

It is deliberately split into an **orchestrator + seven stage prompts** (six linear stages
plus a non-linear debug/fix loop) so each step is
independently runnable, cheaper per call, and version-controllable. The orchestrator
holds state and enforces two hard gates: **Interview** (never build on unstated
assumptions) and **Validate** (never ship without a lint self-audit and user sign-off).

Every Build and Eval output is emitted **twice, equally**: a **CX Agent Studio console
runbook** (UI path) **and** **cxas-scrapi config-as-code + CLI** (CI/CD path), kept in
sync.

## File map

| File | Purpose |
|------|---------|
| `00-orchestrator.prompt.md` | Drives the state machine, holds `PROJECT_STATE`, enforces gates, chains stages. |
| `01-ingest.prompt.md`   | Parse any input → `NORMALIZED_BRIEF` with requirement IDs + UNKNOWNs. |
| `02-interview.prompt.md`| **◆GATE◆** Batched, prioritized clarifying questions → resolved brief + `ASSUMPTIONS_LOG`. |
| `03-design.prompt.md`   | Decompose into App/Agents/Tools/Guardrails/Examples/Fallbacks + `TRACEABILITY_MATRIX`. |
| `04-build.prompt.md`    | Console runbook **and** scrapi config tree + Python create/update scripts. |
| `05-evals.prompt.md`    | All 5 eval types, thresholds, coverage %, console steps **and** `cxas` commands. |
| `06-validate.prompt.md` | **◆GATE◆** `cxas lint` self-audit + full deliverable package + final sign-off. |
| `07-debug-fix.prompt.md` | On-demand loop: bug/failing-eval → reproduce → root cause → minimal fix → regression eval. |
| `PROMPT-ASSESSOR.prompt.md` | Standalone skill: scores ANY prompt vs. Anthropic best practices, gives feedback, rewrites, re-scores until good-to-go. |
| `.agents/skills/cx-agent-builder/` | Installable Agent Skill (auto-triggers). `SKILL.md` + bundled `stages/` + `reference/`, synced by `scripts/build-skill.sh`. |
| `dist/cx-agent-builder.system.md` | One-file paste bundle (no-install path), built by `scripts/build-bundle.sh`. |
| `scripts/smoke-test.py` | Verify the installed cxas-scrapi matches the API the prompts assume (run before a real build). |
| `scripts/build-report.py` | Turn a run's captured markdown artifacts into a single `DELIVERABLE.md` + styled `DELIVERABLE.html`. |
| `docs/USING-CXAS-SKILLS.md` | How to install/use the 5 official cxas-scrapi skills and how this package maps to them. |
| `docs/REVIEW.md` | Independent reviewer's assessment of the package (strengths, risks, verdict). |
| `docs/REVIEW-GECX.md` | GECX-expert critique (grounding, examples, complexity tiering, foundry handoff…) + what was fixed. |
| `docs/DEMO-TALK-TRACK.md` | Demo script + talk track for presenting to GECX developers. |
| `docs/DEMO-RUNSHEET.md` | Minute-by-minute presenter runsheet with backup answers and fallbacks. |
| `docs/demo-reel.html` | Self-running animated demo reel (~2:55) — full-screen and screen-record it. |
| `docs/VIDEO-SCRIPT.md` | Timed voiceover script + recording guide that pairs with the reel. |
| `ASSESSMENT.md` | Report from running the assessor on this package (before/after scores + fixes). |
| `shared/ground-truth.md`   | Platform + cxas-scrapi facts. Prepended to every stage. |
| `shared/output-contract.md`| Global output rules (artifact envelope, IDs, assumptions, dual-emit, delimited input, self-check). |
| `examples/order-support/`  | A full worked run (sample PRD → all six stage artifacts). Start here to see output. |
| `examples/cymbal-retail/`  | Pipeline run against CX Agent Studio's **default sample** (Cymbal Home & Garden) — verifiable vs. the console. |

## How to run

This package is a set of **prompts**, not a script. "Running it" means loading the right
prompt files as context for an LLM (Claude, Gemini, etc.) and giving it your PRD. It is
model-agnostic.

### Option 0 — Install as an Agent Skill (auto-triggers)

The whole pipeline is packaged as an installable skill in `.agents/skills/cx-agent-builder/`
(works in Claude Code, Gemini CLI, Antigravity — same channel as the official cxas skills):

```bash
npx skills add srikanthpyaraka/cxas-prompt-pipeline
```

Or copy `.agents/skills/cx-agent-builder/` into your `~/.claude/skills/` (or project
`.claude/skills/`). Once installed it **triggers by description** — say "build a CX Agent
Studio agent from this PRD", or type `demo` / `template`. It reads its bundled stage
contracts on demand and delegates on-platform work to `cxas-agent-foundry` etc. Regenerate
the bundled files after editing prompts with `bash scripts/build-skill.sh`.

### Option A — Automated (recommended): one session drives all 6 stages

In Claude Code, from the repo folder:

```bash
cd cx-agent-builder
claude
```

Then send this as your first message:

```
Read and follow these files as your instructions, in this order:
shared/ground-truth.md, shared/output-contract.md, 00-orchestrator.prompt.md.
Act as the orchestrator they describe. Then begin STAGE 1 with the PRD below.

<PASTE YOUR PRD / NOTES / TICKETS / BULLETS HERE>
```

The orchestrator then runs Ingest → Interview → Design → Build → Evals → Validate,
pausing for your confirmation between stages. It will **not** cross a ◆GATE◆ until the
condition is met (P0 questions answered; lint findings resolved + your sign-off). Answer
its questions and say "continue" to advance.

### Option B — Manual, one stage at a time

Best for iterating on a single stage. Give the model the two shared files + that stage's
prompt + the previous stage's output artifact:

```
Follow shared/ground-truth.md + shared/output-contract.md + 03-design.prompt.md.
Here is the input artifact from the previous stage:

<PASTE THE RESOLVED_BRIEF ARTIFACT>
```

### Using it outside Claude Code

- **claude.ai / Claude Desktop:** paste the contents of `shared/ground-truth.md`,
  `shared/output-contract.md`, and `00-orchestrator.prompt.md` into one message (or
  attach them), then your PRD.
- **API:** concatenate those three files as the `system` prompt; send the PRD as the
  first `user` message.
- **Gemini / other models:** same idea — the prompts are not Claude-specific.

### What it produces vs. what you still execute

The pipeline **generates** the console runbook + `cxas-scrapi` config tree + Python
scripts + `cxas` eval commands. You then run those against a real GCP project:

```bash
pip install cxas-scrapi
gcloud auth application-default login
# run the generated scripts / cxas push, cxas lint, cxas test-tools, ...
```

## Prompt Assessor (score, feedback, rewrite any prompt)

`PROMPT-ASSESSOR.prompt.md` is a standalone skill that audits ANY prompt against
Anthropic's [prompt-engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices):
it scores the prompt on a 0–100 rubric, gives severity-ranked feedback, rewrites it, then
re-scores in a loop (up to 3 rounds) until it is "good to go" (≥ 90, no criterion < 7, no
unresolved contradictions).

**Use it:** paste the assessor as your instructions, then drop the prompt to review
between the input markers:

```
Follow PROMPT-ASSESSOR.prompt.md.

<prompt_under_review>
<PASTE THE PROMPT YOU WANT SCORED / IMPROVED HERE>
</prompt_under_review>

(Optional) Context: intended model, use case, system-prompt vs user-message, hard constraints.
```

It returns a scorecard, feedback, the rewritten prompt, a changelog, and any residual
gaps. Everything inside `<prompt_under_review>` is treated as data to evaluate, never as
instructions.

**Applied to this package:** all stage prompts were run through the assessor and improved
(delimited input + a verify-before-emit self-check were added to
`shared/output-contract.md`, so every stage inherits them). See `ASSESSMENT.md` for the
before/after scorecard.

## The state machine

```
1 INGEST → 2 INTERVIEW ◆GATE◆ → 3 DESIGN → 4 BUILD → 5 EVALS → 6 VALIDATE ◆GATE◆ → SHIP
                                                       ⤷ 7 DEBUG & FIX (loop on any bug / failing eval)
```
Stage 7 is non-linear: run it whenever a bug is reported or an eval fails. It root-causes
the issue, applies a minimal fix, documents *why it broke and how it was fixed*, and adds
a regression eval (RED-before / GREEN-after) without reducing coverage.

## Artifact hand-offs (each stage's OUTPUT is the next stage's INPUT)

```
01 → NORMALIZED_BRIEF
02 → RESOLVED_BRIEF + ASSUMPTIONS_LOG
03 → ARCHITECTURE + TRACEABILITY_MATRIX
04 → BUILD_PACKAGE (console runbook + scrapi tree + scripts)
05 → EVAL_SUITE (5 types + thresholds + coverage report)
06 → DELIVERABLE_PACKAGE (lint audit + docs + deploy runbook)
```

## Ground truth this package targets

- **Hierarchy:** App → Agents (LLM playbooks) → Tools → Guardrails → Examples → Deployments; plus generative fallbacks + human handoff.
- **cxas-scrapi:** `Apps`, `Agents`, `Tools`, `Guardrails`, `Deployments`, `Sessions`, `Variables`; `cxas pull`/`push`; `cxas lint` (60+ rules).
- **Eval taxonomy (all 5):** Platform Goldens · Local Simulations · Tool Tests · Callback Tests · Turn Evals. Metrics: response-match, tool-call accuracy, latency.
