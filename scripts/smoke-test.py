#!/usr/bin/env python3
"""Smoke-test the cxas-scrapi install against the API surface this prompt suite assumes,
so you catch drift BEFORE a demo or a real run.

- FAIL  = documented API the suite relies on is missing (blocks a real run).
- WARN  = API the suite references but that we inferred/assumed (verify against your version).
- Exit code 1 if any FAIL (or if cxas_scrapi isn't installed).

Usage:  python3 scripts/smoke-test.py
Prereq: pip install cxas-scrapi   (and, for the CLI checks, the `cxas` binary on PATH)
"""
import importlib, shutil, subprocess, sys

# name -> list of (method, confidence)  where confidence in {"documented","assumed"}
EXPECTED = {
    "Apps":        [("list_apps", "documented"), ("create_or_update", "assumed")],
    "Agents":      [("get_agents_map", "documented"), ("create_or_update", "assumed")],
    "Tools":       [("get_tools_map", "documented"), ("create_or_update", "assumed")],
    "Guardrails":  [("create_or_update", "assumed")],
    "Deployments": [],   # constructor presence only
    "Sessions":    [],
    "Variables":   [("create_or_update", "assumed")],
}
EVAL_CLASSES = ["ToolEvals", "SimulationEvals", "CallbackEvals", "GuardrailEvals"]
CLI_SUBCOMMANDS = ["lint", "push", "pull", "migrate", "test-tools", "test-callbacks", "push-eval"]

OK, WARN, FAIL = "✓ PASS", "⚠ WARN", "✗ FAIL"
results = []  # (status, message)
def add(s, m): results.append((s, m)); print(f"  {s}  {m}")

def main():
    print("cxas-scrapi smoke test — verifying the API surface the prompts assume\n")

    # 1) module import
    try:
        cx = importlib.import_module("cxas_scrapi")
    except Exception as e:
        print(f"  {FAIL}  cannot import cxas_scrapi ({e})")
        print("\n  → Install it:  pip install cxas-scrapi")
        sys.exit(1)
    ver = getattr(cx, "__version__", "unknown")
    add(OK, f"import cxas_scrapi (version: {ver})")

    # 2) classes + methods
    print("\nCore resource classes:")
    for cls_name, methods in EXPECTED.items():
        cls = getattr(cx, cls_name, None)
        if cls is None:
            add(FAIL, f"cxas_scrapi.{cls_name} missing (documented resource class)"); continue
        add(OK, f"cxas_scrapi.{cls_name} present")
        for meth, conf in methods:
            has = callable(getattr(cls, meth, None))
            if has:
                add(OK, f"    {cls_name}.{meth}()")
            else:
                add(WARN if conf == "assumed" else FAIL,
                    f"    {cls_name}.{meth}() not found ({conf})"
                    + ("  → prompts use this; confirm the real method name" if conf == "assumed" else ""))

    # 3) evals classes (try top-level, then a few likely submodules)
    print("\nEvals API:")
    for name in EVAL_CLASSES:
        found = getattr(cx, name, None) is not None
        if not found:
            for sub in ("cxas_scrapi.evals", "cxas_scrapi.api.evals"):
                try:
                    if getattr(importlib.import_module(sub), name, None) is not None:
                        found = True; break
                except Exception:
                    pass
        add(OK if found else WARN, f"evals.{name} " + ("present" if found else "not found (verify eval entry points)"))

    # 4) CLI
    print("\ncxas CLI:")
    if shutil.which("cxas") is None:
        add(WARN, "`cxas` not on PATH (CLI checks skipped — install cxas-scrapi's console script)")
    else:
        try:
            help_txt = subprocess.run(["cxas", "--help"], capture_output=True, text=True, timeout=30).stdout
            for sub in CLI_SUBCOMMANDS:
                add(OK if sub in help_txt else WARN, f"cxas {sub}" + ("" if sub in help_txt else "  (not in --help; verify)"))
        except Exception as e:
            add(WARN, f"could not run `cxas --help` ({e})")

    # summary
    fails = sum(1 for s, _ in results if s == FAIL)
    warns = sum(1 for s, _ in results if s == WARN)
    print(f"\nSummary: {len(results)-fails-warns} pass, {warns} warn, {fails} fail")
    if fails:
        print("→ FAILs mean the suite's assumptions don't match your install. Update the prompts'")
        print("  cxas-scrapi calls (04-build, 05-evals) to the real API before a real run.")
    elif warns:
        print("→ No blockers. WARNs are assumed/inferred API — confirm those names against your version.")
    else:
        print("→ All good. The assumed API surface matches your install.")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
