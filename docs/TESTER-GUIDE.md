# Tester guide — CX Agent Builder

Thanks for testing. This takes ~15 minutes and the feedback template at the end is the
important part. Goal of this round: **does it produce correct, usable CX Agent Studio
output, and where does it break on a real project?**

## 0. Access
The repo is private. If you can't open it, ask Srikanth to add you as a collaborator
(GitHub → Settings → Collaborators), then:
```bash
git clone https://github.com/srikanthpyaraka/cxas-prompt-pipeline.git
cd cxas-prompt-pipeline
```

## 1. Two-minute smoke run (no GCP needed)
1. Open Claude or Gemini.
2. Paste the whole of `dist/cx-agent-builder.system.md`.
3. Send `demo`.
Expected: it runs a full PRD → interview → design → build → evals → validate pass on a
sample and narrates each stage. Then try `template`, then paste a real PRD of your own.

## 2. Real run (needs a sandbox GCP project + CX Agent Studio)
```bash
npx skills add googlecloudplatform/cxas-scrapi
pip install cxas-scrapi
gcloud auth application-default login
python3 scripts/smoke-test.py            # verifies the cxas-scrapi API matches our assumptions
```
- If the smoke test shows any **FAIL**, capture the output — that's the most useful bug.
- Install our skill so it auto-triggers:
  `mkdir -p ~/.claude/skills && cp -R .agents/skills/cx-agent-builder ~/.claude/skills/`
  (restart Claude Code), then: *"build a CX Agent Studio agent from this PRD"* + your PRD.
- After the build produces a `cxas_app/<App>/`, validate the format:
  ```bash
  python3 scripts/smoke-test.py --pull-dir cxas_app/<App> --layout-only
  ```
- If you have a comparable existing app, `cxas pull` it and run the same `--pull-dir` check
  against the real thing — mismatches there are gold.
- **Sanity checks the pipeline should pass** (report a bug if not):
  - Files exist on disk: `find cxbuild -type f` shows app.json + agent/tool/instruction/eval files
    (not just printed in chat).
  - The app was created: it appears in `cxas apps list` (the pipeline runs `cxas create` →
    `push` → `push-eval`). "No such app" means the create step didn't run.

## 3. Report these 4 things (copy/paste and fill in)
```
### CX Agent Builder — test feedback
Tester / date:
Model used (Claude / Gemini):
Ran: [ ] demo  [ ] own PRD (no GCP)  [ ] real build on GCP

1) FORMAT — did the emitted cxas_app/ tree + evals/ match the real platform?
   - smoke-test.py result (API): PASS / WARN / FAIL  (paste any FAIL lines)
   - smoke-test.py --pull-dir result: PASS / WARN / FAIL  (paste any FAIL lines)
   - Anything cxas push / lint rejected:

2) INTERVIEW — were the questions the RIGHT ones? Too many / too few?
   - Missing question that mattered:
   - Question that was noise:

3) CORRECTNESS — was the design/grounding/eval sound for your use case?
   - Wrong or missing: (grounding source? tool schema? guardrail? handoff? eval?)
   - Did it hallucinate any platform behavior?

4) FRICTION — where did you get stuck or lose trust?
   - Confusing step:
   - Time to first useful output:
   - Would you use it on a real project? Y/N — why:
```
Send the filled template back (Slack/email/issue). Short and specific beats polished.

## Known limitations (so you don't report these as surprises)
- The committed `examples/` are **authored reference runs**, not live transcripts.
- cxas-scrapi API was **verified against an installed package** (`create_app`/`update_app`,
  `create_agent`, `create_tool`, etc.; `list_apps`/`get_agents_map` confirmed). Run
  `smoke-test.py` to re-pin against your exact version. Deploys use the `cxas` CLI, not these.
- It has **not yet been run end-to-end on a live GCP project** — you may be the first; that's
  the point of this round.
- Voice: simulations run in `modality="audio"` (tests the TTS/STT path, not raw acoustics).
