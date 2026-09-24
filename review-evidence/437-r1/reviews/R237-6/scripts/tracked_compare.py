#!/usr/bin/env python3
"""Reviewer probe: every tracked Markdown page of the head, read by two
trees' walks (the reviewed head before the correction, and the correction).

For each page: blocks(), line_kinds(), headings(), plan(), refusals() and
generated_block(). The page text is the head's, so only the code differs.
Also records the deepest element nesting the head's renderer reports.

Usage: tracked_compare.py PYTHON REPO TREE_A TREE_B OUT_JSON
"""
import json
import subprocess
import sys

DUMP = r"""
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc
out = {}
for rel in json.load(open(sys.argv[3])):
    text = open(sys.argv[2] + "/" + rel, encoding="utf-8").read()
    rec = {"refusals": [list(r) for r in gen_toc.refusals(text)]}
    try:
        rec["blocks"] = gen_toc.blocks(text)
        rec["kinds"] = gen_toc.line_kinds(text)
        rec["headings"] = [list(h) for h in gen_toc.headings(text)]
        rec["plan"] = [list(h) for h in (gen_toc.plan(text) or [])]
        blk = gen_toc.generated_block(text, rel)
        rec["generated"] = None if blk is None else [blk[0], blk[1]]
    except Exception as exc:
        rec["error"] = repr(exc)
    out[rel] = rec
json.dump(out, open(sys.argv[4], "w"))
"""

DEPTH = r"""
import json, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
import gen_toc_renderer as r
orig, worst = r._elements, [0]
def spy(bound, html):
    res = orig(bound, html)
    worst[0] = max(worst[0], res[1])
    return res
r._elements = spy
for rel in json.load(open(sys.argv[3])):
    r.render(open(sys.argv[2] + "/" + rel, encoding="utf-8").read())
print(worst[0])
"""


def main() -> int:
    py, repo, tree_a, tree_b, dest = sys.argv[1:]
    pages = subprocess.run(["git", "-C", repo, "ls-files", "*.md"],
                           capture_output=True, text=True,
                           check=True).stdout.split()
    listing = dest + ".pages.json"
    json.dump(pages, open(listing, "w"))
    dumps = []
    for tree in (tree_a, tree_b):
        out = f"{dest}.{tree.rstrip('/').rsplit('/', 1)[1]}.json"
        subprocess.run([py, "-c", DUMP, tree, repo, listing, out], check=True)
        dumps.append(json.load(open(out)))
    a, b = dumps
    diffs = {rel: sorted(k for k in set(a[rel]) | set(b[rel])
                         if a[rel].get(k) != b[rel].get(k))
             for rel in pages if a[rel] != b[rel]}
    depth = subprocess.run([py, "-c", DEPTH, tree_b, repo, listing],
                           capture_output=True, text=True, check=True)
    summary = {"pages": len(pages), "differing_pages": diffs,
               "errors": {rel: (a[rel].get("error"), b[rel].get("error"))
                          for rel in pages
                          if "error" in a[rel] or "error" in b[rel]},
               "refused_at_b": [rel for rel in pages if b[rel]["refusals"]],
               "deepest_element_nesting_head": int(depth.stdout.strip()),
               "headings_total_b": sum(len(b[r].get("headings", []))
                                       for r in pages)}
    json.dump(summary, open(dest, "w"), indent=1)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
