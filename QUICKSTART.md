# Quickstart — your first CX agent build in ~10 minutes

Three levels of effort. Pick one.

## Level 0 — Just watch it work (0 setup, 1 minute)
1. Open a Claude or Gemini chat.
2. Paste the contents of **[`dist/cx-agent-builder.system.md`](dist/cx-agent-builder.system.md)**
   (one file — the whole engine).
3. Send: **`demo`**.

It runs the full pipeline on a built-in sample PRD, auto-answers the interview, and narrates
every stage. You see a complete PRD→build→evals→debug run without providing anything.

## Level 1 — Build from your own PRD (2 minutes to first output)
1. Paste **`dist/cx-agent-builder.system.md`** as your first message (or, in Claude Code,
   load `shared/*.md` + `00-orchestrator.prompt.md`).
2. Paste your PRD — or send **`template`** to get a fill-in-the-blanks PRD first.
3. Answer the interview questions (it won't build until the blockers are resolved).
4. Continue through Design → Build → Evals → Validate. Say "continue" between stages.

Output: a console runbook, cxas-scrapi config, and an eval suite — all traceable to your
requirements.

## Level 2 — Actually deploy on GCP (adds the official skills)
1. Install the official skills once:
   ```bash
   npx skills add googlecloudplatform/cxas-scrapi
   pip install cxas-scrapi
   gcloud auth application-default login
   ```
2. Run Level 1 to produce the design + config.
3. Let the pipeline hand execution to **cxas-agent-foundry** (push + lint) and
   **cxas-sim-eval** (test cases). See [`docs/USING-CXAS-SKILLS.md`](docs/USING-CXAS-SKILLS.md).
4. Break something and send a bug → Stage 7 gives you a root cause + a regression eval.

---

### The one thing to remember
> Paste **`dist/cx-agent-builder.system.md`**, then type **`demo`**, **`template`**, or paste a PRD.

### Regenerate the bundle after editing prompts
```bash
bash scripts/build-bundle.sh
```

### See a finished run
[`examples/order-support/`](examples/order-support/) · [`examples/cymbal-retail/`](examples/cymbal-retail/) (verifiable against the console).
