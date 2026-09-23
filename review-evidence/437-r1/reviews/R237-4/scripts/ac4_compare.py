#!/usr/bin/env python3
"""Acceptance 4: classify every tracked Markdown page of one or more trees
under two revisions of the walk and report every difference.

Usage: ac4_compare.py <repo> <head-scripts> <base-scripts> <tree-ish>...

For each tree-ish, every `*.md` path of that tree is read from Git (as the
committed bytes, decoded UTF-8) and answered by both walks: blocks(),
line_kinds(), headings() with anchors, plan(), refusals() and
generated_block() (with the page's path). A digest of the base answers is
printed so two runs can be compared.
"""
import hashlib
import json
import subprocess
import sys

WORKER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc as g
pages = json.load(sys.stdin)
out = []
for path, text in pages:
    out.append({"blocks": g.blocks(text), "kinds": g.line_kinds(text),
                "headings": [list(h) for h in g.headings(text)],
                "plan": [list(h) for h in (g.plan(text) or [])],
                "refusals": [list(r) for r in g.refusals(text)],
                "generated": g.generated_block(text, path)})
json.dump(out, sys.stdout)
'''


def answers(scripts: str, pages: list) -> list:
    proc = subprocess.run([sys.executable, "-B", "-c", WORKER, scripts],
                          input=json.dumps(pages).encode(), capture_output=True, check=True)
    return json.loads(proc.stdout)


def main() -> int:
    repo, head, base = sys.argv[1:4]
    status = 0
    for tree in sys.argv[4:]:
        names = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "-z", "--name-only", tree],
                               capture_output=True, check=True).stdout.decode().split("\0")
        mds = sorted(n for n in names if n.endswith(".md"))
        pages = [(n, subprocess.run(["git", "-C", repo, "show", f"{tree}:{n}"], capture_output=True,
                                    check=True).stdout.decode("utf-8")) for n in mds]
        h, b = answers(head, pages), answers(base, pages)
        diffs = [(p[0], k) for p, x, y in zip(pages, h, b) for k in x if x[k] != y[k]]
        digest = hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()
        with_block = sum(1 for x in b if x["generated"])
        print(f"tree {tree}: {len(pages)} pages, {with_block} with a generated block, "
              f"{len(diffs)} field differences, base-answer digest {digest[:16]}")
        for d in diffs:
            print("  DIFF", d)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
