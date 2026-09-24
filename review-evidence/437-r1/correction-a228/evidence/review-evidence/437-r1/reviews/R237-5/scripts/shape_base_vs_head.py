#!/usr/bin/env python3
"""For every recorded shape: does the BASE walk agree with GitHub's
recorded headings, and does the HEAD walk? Text is compared after the
base label is reduced as a reader sees it (strip_md) and blanks collapse;
the N1 github_only heading is removed from GitHub's list first.
Usage: shape_base_vs_head.py <base-tree> <head-tree> (run with the locked
interpreter; the base walk needs no renderer)."""
import importlib.util, json, sys
def load(tree, name):
    spec = importlib.util.spec_from_file_location(name, f"{tree}/scripts/gen_toc.py")
    m = importlib.util.module_from_spec(spec); sys.path.insert(0, f"{tree}/scripts")
    spec.loader.exec_module(m); sys.path.pop(0); return m
base = load(sys.argv[1], "base_gen_toc")
sys.path.insert(0, f"{sys.argv[2]}/scripts"); import gen_toc as head
shapes = json.load(open(f"{sys.argv[2]}/scripts/gen_toc_shapes.json"))["shapes"]
norm = lambda s: " ".join(s.split())
tally = {}
for s in shapes:
    want = [tuple(h) for h in s["headings"]]
    for x in s.get("github_only", {}).get("headings", []):
        want.remove(tuple(x))
    b = [(l, norm(base.strip_md(r))) for l, r, _ in base.headings(s["page"])]
    h = [(l, t) for l, t in head.rendered_headings(s["page"])]
    key = ("base-agrees" if b == want else "base-differs", "head-agrees" if h == want else "head-differs")
    tally.setdefault(key, []).append(s["name"])
for k, v in sorted(tally.items()):
    print(k, len(v))
for k in (("base-agrees", "head-differs"), ("base-differs", "head-differs")):
    for n in tally.get(k, []):
        print("  ", k, n)
