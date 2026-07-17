#!/usr/bin/env python3
"""Deterministically write a cxas app tree + evals from a spec JSON, so file creation
doesn't depend on the model remembering to write each file.

Usage:  python3 scripts/scaffold-app.py <spec.json>
Output: cxbuild/<slug>/  (gecx-config.json, cxas_app/<App>/…, evals/…) then prints the file list.

Spec shape (only what's present is written):
{
  "slug": "orderbot", "project_id": "...", "location": "global",
  "app":   {"displayName":"OrderBot","rootAgent":"router","variableDeclarations":[...]},
  "agents":[{"displayName":"router","instruction":"<text>","tools":["end_session"],
             "childAgents":["order_status_agent"],
             "callbacks":{"beforeModelCallbacks":"<python code>"}}],
  "tools": [{"displayName":"get_order_status","openApiTool":{...}},
            {"displayName":"lookup","pythonFunction":{"description":"...","code":"<python>"}}],
  "guardrails":[{"displayName":"pii_redaction", ...}],
  "goldens":[{"name":"PG-01","yaml":"<golden yaml>"}],
  "simulations":[{"name":"SIM-01","yaml":"<sim yaml>"}]
}
"""
import json, os, re, sys

def w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text if isinstance(text, str) else json.dumps(text, indent=2))

def main():
    if len(sys.argv) != 2:
        print("usage: scaffold-app.py <spec.json>", file=sys.stderr); sys.exit(2)
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    slug = spec["slug"]
    app_name = spec["app"]["displayName"].replace(" ", "_")
    root = f"cxbuild/{slug}"
    app_dir = f"{root}/cxas_app/{app_name}"

    w(f"{root}/gecx-config.json",
      {"project_id": spec.get("project_id", "<PROJECT_ID>"),
       "location": spec.get("location", "global"),
       "app_display_name": spec["app"]["displayName"]})
    w(f"{app_dir}/app.json", spec["app"])

    for ag in spec.get("agents", []):
        name = ag["displayName"]
        d = f"{app_dir}/agents/{name}"
        node = {"displayName": name, "instruction": f"agents/{name}/instruction.txt"}
        for k in ("tools", "childAgents"):
            if ag.get(k): node[k] = ag[k]
        w(f"{d}/instruction.txt", ag.get("instruction", ""))
        for cb_type, code in ag.get("callbacks", {}).items():          # e.g. beforeModelCallbacks
            folder = re.sub(r"(?<!^)(?=[A-Z])", "_", cb_type).lower()   # before_model_callbacks
            rel = f"agents/{name}/{folder}/{folder}_01/python_code.py"
            w(f"{app_dir}/{rel}", code)
            node[cb_type] = [{"pythonCode": rel, "description": f"{name} {cb_type}"}]
        w(f"{d}/{name}.json", node)

    for t in spec.get("tools", []):
        name = t["displayName"]; node = {"displayName": name}
        for key, block in t.items():
            if key == "displayName": continue
            if key == "pythonFunction" and "code" in block:
                rel = f"tools/{name}/python_function/python_code.py"
                w(f"{app_dir}/{rel}", block["code"])
                node[key] = {"name": name, "pythonCode": rel,
                             "description": block.get("description", "")}
            else:
                node[key] = block
        w(f"{app_dir}/tools/{name}/{name}.json", node)

    for g in spec.get("guardrails", []):
        name = g["displayName"]
        w(f"{app_dir}/guardrails/{name}/{name}.json", g)

    for kind in ("goldens", "simulations"):
        for e in spec.get(kind, []):
            w(f"{root}/evals/{kind}/{e['name']}.yaml", e["yaml"])

    files = [os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs]
    print(f"Wrote {len(files)} files under {root}/:")
    for f in sorted(files): print("  " + f)
    print(f"\nVerify:  python3 scripts/smoke-test.py --pull-dir {app_dir} --layout-only")

if __name__ == "__main__":
    main()
