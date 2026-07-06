# Using the official cxas-scrapi Agent Skills with this package

The [cxas-scrapi](https://github.com/GoogleCloudPlatform/cxas-scrapi) project ships **5
official Agent Skills**. They are the **execution engine**; this prompt package is the
**orchestration + intake layer** that feeds them well. Where a skill exists, prefer it over
hand-written cxas-scrapi code — it's maintained by Google and comes with real scripts.

## Install
```bash
npx skills add googlecloudplatform/cxas-scrapi
```
Skills land in `.agents/skills/` and are picked up by Claude Code, Gemini CLI, and
Antigravity. Prerequisites: `pip install cxas-scrapi`, `gcloud auth application-default
login` (or `gcloud auth login`), and a GCP project with CX Agent Studio enabled.

## The skills
| Skill | Use it for | Key entry points |
|-------|-----------|------------------|
| **cxas-agent-foundry** | End-to-end build → eval → debug → iterate | `cxas pull/push`, `cxas lint` (via its `lint-fixer` sub-agent), `scripts/run-and-report.py --runs 5`, `scripts/inspect-app.py`, `scripts/triage-results.py --last 3`; enforces a `todo.md` checklist |
| **cxas-sim-eval** | Turn-by-turn goldens → `SimulationEvals` test cases | asks for the full app resource name + output dir |
| **cxas-dfcx-migration** | Dialogflow CX → CXAS migration | `cxas migrate dfcx --run …`, `--optimize --stage 1/2/3` |
| **cxas-cuj-report-generator** | Requirement docs (BRD/diagrams/code) → CUJ transcripts/reports | directory of docs in → interactive HTML reports |
| **cxas-loss-analysis** | Mine non-contained (lost) conversations → failure clusters | `scripts/fetch_losses.py --project-id … --app-id …` |

## How this package maps onto them
This package's job is to get from a messy PRD to a **clean, interviewed, traceable spec**,
then hand execution to the skills — and to add discipline (dual-emit, coverage, regression)
around whatever they produce.

| Pipeline stage | Delegate execution to |
|----------------|-----------------------|
| 1 Ingest | **cxas-cuj-report-generator** when inputs are rich docs (BRDs, diagrams, code) — it extracts journeys/transcripts you fold into the brief. |
| 2 Interview | (this package) — the gate the foundry skill doesn't front-load. |
| 3 Design | (this package) — architecture + traceability. `inspect-app.py` if refining an existing app. |
| 4 Build | **cxas-agent-foundry** — scaffold, `cxas push`, lint via its `lint-fixer` sub-agent. Console runbook stays here; the code path becomes foundry commands. |
| 5 Evals | **cxas-agent-foundry** `run-and-report.py` + **cxas-sim-eval** to generate `SimulationEvals`. This package keeps the 5-type taxonomy, thresholds, and coverage %. |
| 6 Validate | **cxas-agent-foundry** lint + report; this package adds the sign-off gate. |
| 7 Debug & Fix | **cxas-agent-foundry** `triage-results.py` + `run-and-report.py`; **cxas-loss-analysis** to turn real production losses into regression evals. |
| (entry) Migration | **cxas-dfcx-migration** if you're starting from a Dialogflow CX agent, then re-enter at stage 3/4. |

## How to invoke (Claude Code)
1. Run the install command above once per repo/workspace.
2. Skills trigger by description — mention the task ("build a CXAS agent", "run the evals",
   "triage the failures") and the matching skill activates. You can also name it, e.g.
   "use cxas-agent-foundry to push and lint this app."
3. The foundry skill will insist on a `todo.md` before doing work — that's by design; let it.
4. Provide what the skills ask for up front: the full app resource name
   (`projects/<id>/locations/<loc>/apps/<app_id>`), `project_id`, `location`, and an output
   directory.

## Division of labor, in one line
**This package decides *what* to build and holds the quality bars; the official skills
*do* the building, evaluating, and debugging on-platform.**
