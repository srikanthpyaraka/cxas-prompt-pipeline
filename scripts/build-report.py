#!/usr/bin/env python3
"""Assemble a run's captured markdown artifacts into DELIVERABLE.md + a styled
DELIVERABLE.html. No third-party dependencies.

Usage:
  python3 scripts/build-report.py <dir> [--title "..."] [--out <dir>]

<dir> is a folder of stage markdown files (e.g. cxbuild/<app>/artifacts, or
examples/cymbal-retail). Files are included in filename order.
"""
import argparse, html, os, re, sys

def md_to_html(md):
    out, i, lines = [], 0, md.split("\n")
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):                       # fenced code
            i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>"); continue
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)          # heading
        if m:
            lvl = len(m.group(1)); out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i+1]):
            rows = []                                    # table
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            head, body = rows[0], rows[2:]
            t = ["<table><thead><tr>"] + [f"<th>{inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>"); out.append("".join(t)); continue
        if re.match(r"^\s*[-*]\s+", ln):                 # unordered list
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(f"<li>{inline(re.sub(r'^\\s*[-*]\\s+', '', lines[i]))}</li>"); i += 1
            out.append("<ul>" + "".join(items) + "</ul>"); continue
        if ln.strip() == "":
            i += 1; continue
        out.append(f"<p>{inline(ln)}</p>"); i += 1       # paragraph
    return "\n".join(out)

CSS = """
body{font-family:Calibri,'Segoe UI',Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 24px;color:#22284B;line-height:1.5}
h1,h2,h3,h4{font-family:Cambria,Georgia,serif;color:#1E2761}
h1{font-size:34px;border-bottom:3px solid #02C39A;padding-bottom:8px}
h2{margin-top:34px} code{background:#F2F6FF;padding:1px 5px;border-radius:4px;font-size:.92em}
pre{background:#141A47;color:#CADCFC;padding:16px;border-radius:8px;overflow:auto;font-size:13px}
pre code{background:none;color:inherit;padding:0}
table{border-collapse:collapse;width:100%;margin:14px 0}
th,td{border:1px solid #d7deee;padding:7px 10px;text-align:left;font-size:14px}
th{background:#1E2761;color:#fff} tr:nth-child(even) td{background:#F7F9FF}
.stage{border-top:1px solid #e5e9f5;margin-top:40px;padding-top:8px}
.meta{color:#5B6785;font-size:13px}
a{color:#00A896}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir"); ap.add_argument("--title", default="CX Agent Builder — Deliverable")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    src = a.dir; outdir = a.out or src
    files = sorted(f for f in os.listdir(src) if f.endswith(".md") and f.lower() != "readme.md")
    if not files:
        print(f"No .md artifacts in {src}", file=sys.stderr); sys.exit(1)
    md_parts, body = [], []
    for f in files:
        with open(os.path.join(src, f), encoding="utf-8") as fh:
            content = fh.read()
        md_parts.append(f"\n\n---\n\n# {f}\n\n" + content)
        body.append(f'<div class="stage"><div class="meta">{html.escape(f)}</div>{md_to_html(content)}</div>')
    with open(os.path.join(outdir, "DELIVERABLE.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# {a.title}\n" + "".join(md_parts))
    doc = (f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(a.title)}</title>"
           f"<style>{CSS}</style></head><body><h1>{html.escape(a.title)}</h1>"
           f"<p class='meta'>{len(files)} stage artifacts</p>" + "".join(body) + "</body></html>")
    with open(os.path.join(outdir, "DELIVERABLE.html"), "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"Wrote {outdir}/DELIVERABLE.md and DELIVERABLE.html from {len(files)} artifacts")

if __name__ == "__main__":
    main()
