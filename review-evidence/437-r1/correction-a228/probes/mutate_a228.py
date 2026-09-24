"""Remove each property this round adds, one per disposable copy of the
working tree's scripts/ and tools/markdown/, and run both shipped
self-tests. KILLED = a self-test exits non-zero.
Usage: mutate_a228.py <python> <repo> <workdir> <out.json>"""
import concurrent.futures as cf, json, shutil, subprocess, sys
from pathlib import Path
py, src, work, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
R, G, C = "scripts/gen_toc_renderer.py", "scripts/gen_toc.py", "scripts/gen_toc_shape_cases.py"
HEAD_NODES = subprocess.run(["git", "-C", str(src), "show", "196cb7d99cb0:scripts/gen_toc_renderer.py"],
                            capture_output=True, text=True, check=True).stdout
old_nodes = HEAD_NODES[HEAD_NODES.index("def _nodes("):HEAD_NODES.index("def render(")]
cur = (src / R).read_text()
new_nodes = cur[cur.index("def _nodes("):cur.index("def spells_position(")]
own = ('_OWN_ELEMENT = ("block_quote", "list", "heading", "code_block",\n'
       '                "thematic_break", "table")')
kinds = ("block_quote", "list", "heading", "code_block", "thematic_break", "table")
MUT = [
 ("A01 position guard removed", R, "forged = spells_position(ffi.string(plain_ptr))", "forged = False"),
 ("A02 position guard back to the page text, case-sensitive (reverse mutant)", R,
  "forged = spells_position(ffi.string(plain_ptr))", "forged = POSITION in text"),
 ("A03 position guard on the page text, any case (R238-4 M22 probe)", R,
  "forged = spells_position(ffi.string(plain_ptr))", "forged = POSITION in text.lower()"),
 ("A04 position guard on the HTML, case-sensitive", R,
  "return POSITION.encode() in html.lower()", "return POSITION.encode() in html"),
 ("A05 refusal does not name the attribute", G, "at = folded.find(POSITION)\n", "at = -1\n"),
 ("A06 refusal names the attribute case-sensitively", G,
  "folded = line.translate(_ASCII_LOWER)", "folded = line"),
 ("A07 recursive syntax-tree walk restored", R, new_nodes, old_nodes),
 ("A08 depth bound removed", R, "    if deepest > DEEPEST:", "    if False:"),
 ("A09 depth bound one lower", R, "    if deepest > DEEPEST:", "    if deepest >= DEEPEST:"),
 ("A10 depth bound raised to GitHub's own", R, "DEEPEST = 200", "DEEPEST = 256"),
] + [(f"A{11 + i} own-element kind {k!r} dropped", R, own,
      f"_OWN_ELEMENT = {tuple(x for x in kinds if x != k)!r}") for i, k in enumerate(kinds)] + [
 ("A17 heading tag not matched to its level (R238-4 M17, R237-5 M06)", G,
  '        if node is None or tag != f"h{node.level}":', "        if node is None:"),
 ("A18 bind() ignores a drifted release (R238-4 M15)", R, "    if bad:\n        raise RendererError",
  "    if False:\n        raise RendererError"),
 ("A19 strikethrough extension dropped (R238-4 M11)", R, '"table", "strikethrough", ', '"table", '),
 ("A20 autolink extension dropped (R238-4 M10)", R, '"strikethrough", "autolink", ', '"strikethrough", '),
 ("A21 tasklist extension dropped (R238-4 M12)", R, ', "tagfilter", "tasklist")', ', "tagfilter")'),
 ("A23 tight-list paragraphs given an element (R238-4 M04, R237-5 M03, at the stack walk)", R,
  '                          holder == "tight"))', '                          False))'),
 ("A22 file-view arm reads no heading the walk lists", C,
  "               for level, raw, anchor in headings(text))", "               for level, raw, anchor in [])"),
]
work.mkdir(parents=True, exist_ok=True)


def run(m):
    name, path, old, new = m
    d = work / name.split()[0]
    shutil.rmtree(d, ignore_errors=True)
    for part in ("scripts", "tools/markdown"):
        shutil.copytree(src / part, d / part, ignore=shutil.ignore_patterns("__pycache__"))
    f = d / path
    s = f.read_text()
    if s.count(old) != 1:
        return {"mutation": name, "applied": False, "matches": s.count(old)}
    f.write_text(s.replace(old, new))
    res = {"mutation": name, "applied": True}
    for key, script in (("toc", "scripts/gen_toc.py"), ("emdash", "scripts/check_em_dash.py")):
        p = subprocess.run([py, script, "--selftest"], cwd=d, capture_output=True, text=True, timeout=1800)
        lines = (p.stdout + p.stderr).splitlines()
        fails = [l.strip() for l in lines if "FAIL [" in l or l.strip().startswith("- [") or "GUARD" in l]
        res[key] = {"rc": p.returncode, "tail": lines[-1:] if lines else [], "failures": fails[:6],
                    "n_failures": len(fails)}
    res["killed"] = res["toc"]["rc"] != 0 or res["emdash"]["rc"] != 0
    shutil.rmtree(d)
    return res


with cf.ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(run, MUT))
out.write_text(json.dumps(results, indent=1, ensure_ascii=False))
for r in results:
    if not r["applied"]:
        print(f"NOT APPLIED ({r['matches']} matches): {r['mutation']}")
        continue
    print(f"{'KILLED' if r['killed'] else 'SURVIVED'}  toc rc={r['toc']['rc']} emdash rc={r['emdash']['rc']}  {r['mutation']}")
    for k in ("toc", "emdash"):
        print(f"      {k}: {r[k]['tail'][0][:110] if r[k]['tail'] else ''}")
        for l in r[k]["failures"][:3]:
            print(f"        {l[:160]}")
