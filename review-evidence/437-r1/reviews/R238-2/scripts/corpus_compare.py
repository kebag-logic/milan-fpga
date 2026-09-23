#!/usr/bin/env python3
"""Acceptance 4 comparison: classify every tracked Markdown page of one tree
under two walk revisions and report every difference.

Usage: corpus_compare.py <repo> <tree-rev> <walkA-root> <walkB-root> <out.json>
Pages are read from `git show <tree-rev>:<path>` (the committed bytes, text
mode as git gives them), so the checkout is not consulted.
Fields compared per page: refusals, blocks, line_kinds, headings with anchors,
plan, existing() span and the generated block.
"""
import hashlib
import json
import subprocess
import sys

HELPER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc as g
pages = json.load(sys.stdin)
out = {}
for path, text in pages.items():
    rec = {"refusals": g.refusals(text)}
    if not rec["refusals"]:
        rec["blocks"] = g.blocks(text)
        rec["line_kinds"] = g.line_kinds(text)
        rec["headings"] = g.headings(text)
        rec["plan"] = g.plan(text)
        rec["existing"] = list(g.existing(text))
        rec["generated"] = g.generated_block(text, path)
    out[path] = rec
json.dump(out, sys.stdout, sort_keys=True, default=list)
'''


def main():
    repo, rev, root_a, root_b, out_path = sys.argv[1:6]
    names = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                           capture_output=True, text=True, check=True).stdout.split("\n")
    pages = {}
    for name in names:
        if name.endswith(".md"):
            blob = subprocess.run(["git", "-C", repo, "show", f"{rev}:{name}"],
                                  capture_output=True, check=True).stdout
            pages[name] = blob.decode("utf-8")
    results = {}
    for label, root in (("A", root_a), ("B", root_b)):
        proc = subprocess.run([sys.executable, "-B", "-c", HELPER, root + "/scripts"],
                              input=json.dumps(pages).encode(), capture_output=True, check=True)
        results[label] = json.loads(proc.stdout)
    diffs = []
    for name in sorted(pages):
        a, b = results["A"][name], results["B"][name]
        for field in sorted(set(a) | set(b)):
            if a.get(field) != b.get(field):
                diffs.append({"page": name, "field": field})
    digest = {label: hashlib.sha256(json.dumps(results[label], sort_keys=True).encode()).hexdigest()
              for label in results}
    report = {"rev": rev, "pages": len(pages), "differences": diffs, "digest": digest,
              "headings_total": {label: sum(len(r.get("headings", [])) for r in results[label].values())
                                 for label in results}}
    json.dump(report, open(out_path, "w"), indent=1)
    print(json.dumps({k: report[k] for k in ("rev", "pages", "digest", "headings_total")}),
          "differences:", len(diffs))


if __name__ == "__main__":
    main()
