#!/usr/bin/env python3
"""Smoke-test the cxas-scrapi install AND (optionally) a real `cxas pull` tree against the
API surface and file layout this prompt suite assumes — so you catch drift BEFORE a demo
or a real run.

- FAIL = documented API / required layout the suite relies on is missing (blocks a real run).
- WARN = API or structure we inferred (verify against your version / pull).
- Exit code 1 if any FAIL.

Usage:
  python3 scripts/smoke-test.py                       # API + CLI checks
  python3 scripts/smoke-test.py --pull-dir <app-dir>  # + validate a real cxas pull tree
  python3 scripts/smoke-test.py --pull-dir <app-dir> --layout-only   # tree check only
Prereq for API checks: pip install cxas-scrapi  (and the `cxas` binary on PATH)
"""
import argparse, importlib, json, os, shutil, subprocess, sys

OK, WARN, FAIL = "✓ PASS", "⚠ WARN", "✗ FAIL"
results = []
def add(s, m): results.append((s, m)); print(f"  {s}  {m}")

# ---- expected API surface (name -> [(method, "documented"|"assumed")]) ----
EXPECTED = {
    # method names verified against an installed cxas_scrapi (create_<resource>/update_<resource>)
    "Apps":        [("list_apps", "documented"), ("create_app", "documented"), ("update_app", "documented"), ("import_app", "documented")],
    "Agents":      [("get_agents_map", "documented"), ("create_agent", "documented"), ("update_agent", "documented")],
    "Tools":       [("get_tools_map", "documented"), ("create_tool", "documented"), ("update_tool", "documented")],
    "Guardrails":  [("create_guardrail", "documented"), ("update_guardrail", "documented")],
    "Deployments": [], "Sessions": [], "Variables": [("create_variable", "documented"), ("update_variable", "documented")],
}
EVAL_CLASSES = ["ToolEvals", "SimulationEvals", "CallbackEvals", "GuardrailEvals"]
CLI_SUBCOMMANDS = ["lint", "push", "pull", "migrate", "test-tools", "test-callbacks", "push-eval"]

def check_api():
    print("cxas-scrapi API surface\n")
    try:
        cx = importlib.import_module("cxas_scrapi")
    except Exception as e:
        add(FAIL, f"cannot import cxas_scrapi ({e})  →  pip install cxas-scrapi"); return
    add(OK, f"import cxas_scrapi (version: {getattr(cx, '__version__', 'unknown')})")
    print("\nCore resource classes:")
    for cls_name, methods in EXPECTED.items():
        cls = getattr(cx, cls_name, None)
        if cls is None:
            add(FAIL, f"cxas_scrapi.{cls_name} missing (documented resource class)"); continue
        add(OK, f"cxas_scrapi.{cls_name} present")
        for meth, conf in methods:
            if callable(getattr(cls, meth, None)):
                add(OK, f"    {cls_name}.{meth}()")
            else:
                add(WARN if conf == "assumed" else FAIL,
                    f"    {cls_name}.{meth}() not found ({conf})"
                    + ("  → prompts use this; confirm the real method name" if conf == "assumed" else ""))
    print("\nEvals API:")
    for name in EVAL_CLASSES:
        found = getattr(cx, name, None) is not None
        if not found:
            for sub in ("cxas_scrapi.evals", "cxas_scrapi.api.evals"):
                try:
                    if getattr(importlib.import_module(sub), name, None) is not None:
                        found = True; break
                except Exception: pass
        add(OK if found else WARN, f"evals.{name} " + ("present" if found else "not found (verify eval entry points)"))
    print("\ncxas CLI:")
    if shutil.which("cxas") is None:
        add(WARN, "`cxas` not on PATH (CLI checks skipped)")
    else:
        try:
            help_txt = subprocess.run(["cxas", "--help"], capture_output=True, text=True, timeout=30).stdout
            for sub in CLI_SUBCOMMANDS:
                add(OK if sub in help_txt else WARN, f"cxas {sub}" + ("" if sub in help_txt else "  (not in --help; verify)"))
        except Exception as e:
            add(WARN, f"could not run `cxas --help` ({e})")

# ---- expected cxas pull/push tree layout (verified against bella_notte) ----
TOOL_TYPE_KEYS = ("pythonFunction", "openApiTool", "dataStoreTool")
# Inside the app dir these folders indicate the wrong format (variables belong in app.json;
# top-level callbacks belong under agents/<a>/..._callbacks/). Note: guardrails/ and toolsets/
# ARE valid app-dir folders (cxas push uploads them).
UNEXPECTED_DIRS = ("variables", "callbacks")

def _json(path):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f), None
    except Exception as e:
        return None, str(e)

def check_pull_tree(root):
    print(f"\ncxas app tree layout: {root}\n")
    if not os.path.isdir(root):
        add(FAIL, f"{root} is not a directory"); return
    # app.json
    app_path = os.path.join(root, "app.json")
    if not os.path.isfile(app_path):
        add(FAIL, "app.json missing at app root")
    else:
        data, err = _json(app_path)
        if err: add(FAIL, f"app.json is not valid JSON ({err})")
        else:
            for k in ("displayName", "rootAgent"):
                add(OK if k in data else FAIL, f"app.json.{k}" + ("" if k in data else " missing"))
            add(OK if "variableDeclarations" in data else WARN,
                "app.json.variableDeclarations" + ("" if "variableDeclarations" in data else " absent (variables belong here, not a folder)"))
            add(OK if "evaluationMetricsThresholds" in data else WARN,
                "app.json.evaluationMetricsThresholds" + ("" if "evaluationMetricsThresholds" in data else " absent"))
    # agents/
    adir = os.path.join(root, "agents")
    if not os.path.isdir(adir):
        add(FAIL, "agents/ folder missing")
    else:
        for name in sorted(os.listdir(adir)):
            sub = os.path.join(adir, name)
            if not os.path.isdir(sub): continue
            add(OK if os.path.isfile(os.path.join(sub, f"{name}.json")) else FAIL, f"agents/{name}/{name}.json")
            add(OK if os.path.isfile(os.path.join(sub, "instruction.txt")) else WARN,
                f"agents/{name}/instruction.txt" + ("" if os.path.isfile(os.path.join(sub, "instruction.txt")) else " absent (instructions live in a separate file)"))
    # tools/
    tdir = os.path.join(root, "tools")
    if os.path.isdir(tdir):
        for name in sorted(os.listdir(tdir)):
            sub = os.path.join(tdir, name)
            if not os.path.isdir(sub): continue
            jp = os.path.join(sub, f"{name}.json")
            if not os.path.isfile(jp): add(FAIL, f"tools/{name}/{name}.json missing"); continue
            data, err = _json(jp)
            if err: add(FAIL, f"tools/{name}/{name}.json invalid ({err})"); continue
            add(OK if any(k in data for k in TOOL_TYPE_KEYS) else WARN,
                f"tools/{name}: type block " + (next((k for k in TOOL_TYPE_KEYS if k in data), "") or f"none of {TOOL_TYPE_KEYS}"))
    else:
        add(WARN, "tools/ folder absent (ok only if the app has no tools)")
    # evals: pulled form = evaluations/ inside the app; foundry authoring = sibling <project>/evals/goldens
    proj = os.path.dirname(os.path.dirname(os.path.abspath(root)))   # <project> when root is cxas_app/<App>
    if os.path.isdir(os.path.join(root, "evaluations")):
        add(OK, "evaluations/ present (pulled platform form)")
    elif os.path.isdir(os.path.join(proj, "evals", "goldens")):
        add(OK, "sibling evals/goldens present (foundry authoring form)")
    else:
        add(WARN, "no evals found (expected evaluations/ in a pull, or ../evals/goldens in a foundry project)")
    # unexpected structures
    for d in UNEXPECTED_DIRS:
        if os.path.isdir(os.path.join(root, d)):
            add(WARN, f"unexpected top-level '{d}/' — not part of the real format (guardrails=safety config, variables=app.json)")
    yamls = [f for dp, _, fs in os.walk(root) for f in fs if f.endswith((".yaml", ".yml"))]
    if yamls:
        add(WARN, f"{len(yamls)} YAML file(s) found — the real cxas tree is JSON; verify these belong")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pull-dir", help="path to the app dir `cxas_app/<App>` (from a real cxas pull or a build) to validate")
    ap.add_argument("--layout-only", action="store_true", help="only run the tree-layout check")
    a = ap.parse_args()
    print("cxas-scrapi smoke test\n")
    if not a.layout_only:
        check_api()
    if a.pull_dir:
        check_pull_tree(a.pull_dir)
    elif a.layout_only:
        add(FAIL, "--layout-only requires --pull-dir")
    fails = sum(1 for s, _ in results if s == FAIL)
    warns = sum(1 for s, _ in results if s == WARN)
    print(f"\nSummary: {len(results)-fails-warns} pass, {warns} warn, {fails} fail")
    if fails:   print("→ FAILs block a real run. Fix the prompts' cxas calls / your tree before pushing.")
    elif warns: print("→ No blockers. WARNs are inferred API/structure — confirm against your version.")
    else:       print("→ All good.")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
