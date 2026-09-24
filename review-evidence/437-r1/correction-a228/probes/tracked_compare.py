"""Every tracked page read by the reviewed head (196cb7d9) and by this head:
refusals, block labels, line kinds, headings, plan, the existing Contents
span, ownership, generated block and `apply()`. Each head runs in its own
interpreter. Usage: tracked_compare.py <old tree> <repo>"""
import json, subprocess, sys
old, repo = sys.argv[1], sys.argv[2]
PROBE = r'''
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g
repo = Path(sys.argv[2])
out = {}
for p in subprocess.run(["git", "-C", str(repo), "ls-files", "*.md"], capture_output=True, text=True).stdout.split():
    f = repo / p
    if not f.is_file():
        continue
    t = f.read_text()
    out[p] = {"refusals": g.refusals(t), "blocks": g.blocks(t), "kinds": g.line_kinds(t),
              "headings": g.headings(t), "plan": g.plan(t), "existing": g.existing(t),
              "owns": g.owns(p, t), "generated": g.generated_block(t, p), "apply": g.apply(f, t)}
print(json.dumps(out))
'''
def run(tree):
    return json.loads(subprocess.run([sys.executable, "-c", PROBE, tree, repo], capture_output=True,
                                     text=True, check=True).stdout)
a, b = run(old), run(repo)
print(len(a), "tracked pages at the reviewed head,", len(b), "at this head")
diff = {p: [k for k in a[p] if a[p][k] != b[p][k]] for p in a if a[p] != b.get(p)}
print("pages whose answers differ:", len(diff))
for p, keys in diff.items():
    print("  ", p, keys)
print("pages apply() would rewrite at this head:", sum(1 for p in b if b[p]["apply"] is not None))
print("pages refused at this head:", [p for p in b if b[p]["refusals"]])
