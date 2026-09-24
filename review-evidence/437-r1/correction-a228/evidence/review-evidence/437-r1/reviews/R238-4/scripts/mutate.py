#!/usr/bin/env python3
"""Reviewer mutation campaign over the #437 renderer-backed walk.

Usage: mutate.py <python-with-lock> <source-repo> <workdir> <out.json>
Each mutation is applied to a fresh `git archive HEAD scripts tools/markdown`
copy under <workdir>/<id>; the replacement must match exactly once. Then
`gen_toc.py --selftest` and `check_em_dash.py --selftest` run in the copy
(at most 8 copies in parallel). KILLED = a selftest exits non-zero.
FIX-PROBE rows are candidate fixes, expected to stay green.
"""
import concurrent.futures as cf, json, shutil, subprocess, sys
from pathlib import Path
py, src, work, out = sys.argv[1], sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
R, G = "scripts/gen_toc_renderer.py", "scripts/gen_toc.py"
MUT = [
 ("M01 positions left quoted", R, "    head, *rest = html.split(f' {POSITION}=\"')", "    return html\n    head, *rest = html.split(f' {POSITION}=\"')"),
 ("M02 walk ignores what the HTML parse swallows", G, "    shown = {position for _, position, _ in rendered.shown if position}", "    shown = {n.position for n in rendered.nodes}"),
 ("M03 headings not filtered by the HTML parse", G, "    for tag, position, rendered_text in rendered.shown:", "    for tag, position, rendered_text in [(f\"h{n.level}\", n.position, \"\") for n in rendered.nodes if n.kind == \"heading\"]:"),
 ("M04 tight-list paragraphs given an element", R, "out += _nodes(bound, child, bare=holder == \"tight\")", "out += _nodes(bound, child, bare=False)"),
 ("M05 raw HTML/indented code extent from reported end", G, "    if node.kind == \"html_block\" or (node.kind == \"code_block\"", "    if False and node.kind == \"html_block\" or (False and node.kind == \"code_block\""),
 ("M06 position-attribute guard removed", R, "    if POSITION in text:", "    if False:"),
 ("M07 ATX label from rendered text", G, "        if node.last == node.first:", "        if False:"),
 ("M08 tagfilter extension dropped", R, "\"autolink\", \"tagfilter\", \"tasklist\"", "\"autolink\", \"tasklist\""),
 ("M09 table extension dropped", R, "EXTENSIONS = (\"table\", ", "EXTENSIONS = ("),
 ("M10 autolink extension dropped", R, "\"strikethrough\", \"autolink\", ", "\"strikethrough\", "),
 ("M11 strikethrough extension dropped", R, "\"table\", \"strikethrough\", ", "\"table\", "),
 ("M12 tasklist extension dropped", R, ", \"tagfilter\", \"tasklist\")", ", \"tagfilter\")"),
 ("M13 footnotes option dropped", R, "lib.CMARK_OPT_UNSAFE\n               | lib.CMARK_OPT_FOOTNOTES", "lib.CMARK_OPT_UNSAFE\n               | 0"),
 ("M14 unsafe option dropped", R, "(lib.CMARK_OPT_SOURCEPOS | lib.CMARK_OPT_UNSAFE", "(lib.CMARK_OPT_SOURCEPOS | 0"),
 ("M15 binding ignores a drifted release", R, "    if bad:\n        raise RendererError", "    if False:\n        raise RendererError"),
 ("M16 bundled cmark-gfm release unchecked", R, "    if core != CMARK_GFM:", "    if False:"),
 ("M17 element tag not matched to heading level", G, "        if node is None or tag != f\"h{node.level}\":", "        if node is None:"),
 ("M18 comment block labelled raw HTML", G, "COMMENT if node.literal.lstrip(\" \").startswith(\n                     \"<!--\") else HTML", "HTML"),
 ("M19 lone carriage return not a line end", G, "if char == \"\\n\" or (char == \"\\r\" and text[at + 1:at + 2] != \"\\n\"):", "if char == \"\\n\":"),
 ("M20 headings in source order, not rendered order", G, "    return tuple(labels), tuple(kinds), tuple(found)", "    found.sort(key=lambda h: h[2])\n    return tuple(labels), tuple(kinds), tuple(found)"),
 ("M21 own-element kinds ignored", R, "element=element or kind in _OWN_ELEMENT)", "element=element)"),
 ("M22 position guard case-sensitive -> ignore case (FIX-PROBE)", R, "    if POSITION in text:", "    if POSITION in text.lower():"),
]
work.mkdir(parents=True, exist_ok=True)
def run(m):
    name, path, old, new = m
    d = work / name.split()[0]
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    tar = subprocess.run(["git", "-C", src, "archive", "HEAD", "scripts", "tools/markdown"], capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(d)], input=tar, check=True)
    f = d / path; s = f.read_text()
    n = s.count(old)
    if n != 1:
        return {"mutation": name, "applied": False, "matches": n}
    f.write_text(s.replace(old, new))
    res = {"mutation": name, "applied": True}
    for key, args in (("toc", [py, "scripts/gen_toc.py", "--selftest"]), ("emdash", [py, "scripts/check_em_dash.py", "--selftest"])):
        p = subprocess.run(args, cwd=d, capture_output=True, text=True, timeout=900)
        fails = [l.strip() for l in (p.stdout + p.stderr).splitlines() if "FAIL" in l or l.strip().startswith("- [") or "GUARD" in l]
        res[key] = {"rc": p.returncode, "tail": (p.stdout + p.stderr).strip().splitlines()[-1:] , "first_failures": fails[:4], "n_fail_lines": len(fails)}
    res["killed"] = res["toc"]["rc"] != 0 or res["emdash"]["rc"] != 0
    return res
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(run, MUT))
out.write_text(json.dumps(results, indent=1))
for r in results:
    if not r["applied"]:
        print(f"NOT APPLIED ({r['matches']} matches): {r['mutation']}"); continue
    print(f"{'KILLED' if r['killed'] else 'SURVIVED'}  toc rc={r['toc']['rc']} emdash rc={r['emdash']['rc']}  {r['mutation']}")
    for k in ("toc", "emdash"):
        for l in r[k]["first_failures"][:2]:
            print(f"      {k}: {l[:170]}")
