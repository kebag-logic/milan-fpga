#!/usr/bin/env python3
"""Recompute the renderer-vs-GitHub comparison over the published fuzz set.
Usage: recompute_fuzz.py <tree> <gfm.json> <markdown-mode.json>
For each page: gen_toc.rendered_headings (head renderer) against the headings
html5lib reads from the recorded gfm and markdown-mode responses (the same
reader the shape arms use), after checking each receipt's SHA-256."""
import hashlib, json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc as g
from gen_toc_renderer import headings_of

def check(rec):
    ok = (hashlib.sha256(rec["request_bytes"].encode()).hexdigest() == rec["request_sha256"]
          and hashlib.sha256(rec["response_bytes"].encode()).hexdigest() == rec["response_sha256"])
    return ok and json.loads(rec["request_bytes"])["text"] == rec["page"]

gfm = json.load(open(sys.argv[2])); md = json.load(open(sys.argv[3]))
bad_receipts = [r["name"] for r in gfm + md if not check(r)]
print(f"receipts: {len(gfm)} gfm, {len(md)} markdown-mode, bad {bad_receipts}")
modes = {r["name"]: json.loads(r["request_bytes"]).get("mode") for r in gfm + md}
print("modes:", sorted(set(modes.values())))
dg = dm = 0
for rg, rm in zip(gfm, md):
    assert rg["page"] == rm["page"]
    mine = [(l, t) for l, t in g.rendered_headings(rg["page"])]
    hg = [tuple(h) for h in headings_of(rg["response_bytes"])]
    hm = [tuple(h) for h in headings_of(rm["response_bytes"])]
    if mine != hg:
        dg += 1; print("GFM DIFF", rg["name"], repr(rg["page"]), mine, hg)
    if mine != hm:
        dm += 1
        esc = [h for h in mine if h not in hm]
        wh = [h for h in hm if h not in mine]
        print(f"FILE-VIEW DIFF {rm['name']} listed-not-shown={esc} shown-not-listed={wh} page={rm['page']!r}")
print(f"differences: gfm {dg}/{len(gfm)}, markdown-mode {dm}/{len(md)}")
