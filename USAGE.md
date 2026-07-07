# How to use CX Agent Builder

Three levels — pick by how far you want to go. If you only read one line:
**paste [`dist/cx-agent-builder.system.md`](dist/cx-agent-builder.system.md) into Claude or
Gemini, then type `demo`.**

---

## Level 0 — Watch it work (1 min, zero setup)
1. Open a Claude or Gemini chat.
2. Paste the whole of **[`dist/cx-agent-builder.system.md`](dist/cx-agent-builder.system.md)**
   (one self-contained file — orchestrator + all 7 stages).
3. Send **`demo`** → it runs the full pipeline on a built-in sample PRD, auto-answers the
   interview, and narrates every stage.
   - `template` → get a fill-in-the-blanks PRD instead.

---

## Level 1 — Build from your own PRD (2 min to first output)

**Install as a skill so it auto-triggers.** The repo is currently **private**, so use the
local copy (the `npx skills add` path only works once the repo is public):

```bash
git clone https://github.com/srikanthpyaraka/cxas-prompt-pipeline.git
cd cxas-prompt-pipeline
mkdir -p ~/.claude/skills && cp -R .agents/skills/cx-agent-builder ~/.claude/skills/
```
Restart Claude Code, then say: **"build a CX Agent Studio agent from this PRD"** and paste
your PRD. (No-install alternative: paste `dist/cx-agent-builder.system.md`, then your PRD.)

What happens:
1. **Ingest** — your PRD becomes numbered requirements; it classifies complexity (simple
   bots get a lean path).
2. **Interview ◆gate◆** — answer the blockers; it will not design until they're resolved.
3. **Design → Build → Evals → Validate** — say "continue" between stages; it pauses for
   your confirmation.

What you get:
- Every stage saved to disk as markdown under `cxbuild/<app>/artifacts/`.
- A pushable config tree under `cxas_app/<AppName>/`.
- A consolidated deliverable — render it anytime:
  ```bash
  python3 scripts/build-report.py cxbuild/<app>/artifacts   # → DELIVERABLE.md + DELIVERABLE.html
  ```

---

## Level 2 — Actually build/deploy on GCP (adds the official skills)

```bash
npx skills add googlecloudplatform/cxas-scrapi   # the official execution engine
pip install cxas-scrapi
gcloud auth application-default login
python3 scripts/smoke-test.py                    # verify the cxas-scrapi API before a real run
```
The pipeline now delegates on-platform work to the official skills:
- **Build / Validate →** `cxas-agent-foundry` (`cxas push`, lint via `lint-fixer`).
- **Evals →** `cxas-agent-foundry` `run-and-report.py` + `cxas-sim-eval`
  (use `modality="audio"` for voice agents).
- **Debug →** `triage-results.py` + `cxas-loss-analysis`.
- **Migration entry →** `cxas-dfcx-migration` if you start from a Dialogflow CX agent.

Break an agent and it returns a documented root cause + a regression test (Stage 7).

---

## Where things are
| I want to… | Go to |
|------------|-------|
| See a finished run | [`examples/order-support/`](examples/order-support/) · [`examples/cymbal-retail/`](examples/cymbal-retail/) |
| Present/demo it | [`docs/DEMO-PLAYBOOK.md`](docs/DEMO-PLAYBOOK.md) · [`docs/demo-reel.html`](docs/demo-reel.html) |
| Understand the official skills | [`docs/USING-CXAS-SKILLS.md`](docs/USING-CXAS-SKILLS.md) |
| Read the design/critique | [`docs/REVIEW.md`](docs/REVIEW.md) · [`docs/REVIEW-GECX.md`](docs/REVIEW-GECX.md) |
| Audit/improve a prompt | [`PROMPT-ASSESSOR.prompt.md`](PROMPT-ASSESSOR.prompt.md) |

## Two things to know before a real project
- The committed examples are **authored reference runs**, not live transcripts.
- The `cxas-scrapi` calls are modeled on the docs — **run `scripts/smoke-test.py`** to pin
  them to your installed version before the first real build.
