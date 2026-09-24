"""Each file-view page of the fixture: what GitHub's file view shows
(level, text, anchor), what `headings()` lists at the reviewed head and at
this head, and whether each passes the file-view arm's test.
Usage: file_view_compare.py <old tree> <repo>"""
import json, subprocess, sys
old, repo = sys.argv[1], sys.argv[2]
PROBE = r'''
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g
views = json.load(open(sys.argv[2] + "/scripts/gen_toc_shapes.json"))["file_view"]
def read(page):
    try:
        return g.headings(page)
    except RecursionError:
        return "RecursionError"
print(json.dumps([read(v["page"]) for v in views]))
'''
views = json.load(open(repo + "/scripts/gen_toc_shapes.json"))["file_view"]
sys.path.insert(0, repo + "/scripts")
import gen_toc  # noqa: F401
from gen_toc import strip_md
def run(tree):
    return json.loads(subprocess.run([sys.executable, "-c", PROBE, tree, repo], capture_output=True, text=True,
                                     check=True).stdout)
def within(listed, shown):
    if listed == "RecursionError":
        return False
    rest = iter(tuple(h) for h in shown)
    return all((lvl, " ".join(strip_md(raw).split()), a) in rest for lvl, raw, a in listed)
before, after = run(old), run(repo)
for v, b, a in zip(views, before, after):
    print(f"== {v['name']}")
    print(f"   GitHub file view: {[tuple(h) for h in v['headings']]}")
    print(f"   reviewed head 196cb7d9: {b if b == "RecursionError" else [(r, x) for _, r, x in b]} -> {'PASS' if within(b, v['headings']) else 'FAIL'}")
    print(f"   this head:              {a if a == "RecursionError" else [(r, x) for _, r, x in a]} -> {'PASS' if within(a, v['headings']) else 'FAIL'}")
