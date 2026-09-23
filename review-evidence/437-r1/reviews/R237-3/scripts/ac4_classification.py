#!/usr/bin/env python3
"""Acceptance 4: per-page classification of every tracked Markdown page,
under the base walk and the head walk, over a tree's tracked pages.

Usage: ac4_classification.py <repo> <rev> <base-scripts> <head-scripts> <out.json>
Pages are read from <rev> with `git show` (bytes as tracked). For each page
both walks' `blocks()` labels and `headings()` are compared; the page
digest is the SHA-256 of the per-page label lists, so two runs compare.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HELPER = r'''
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
pages = json.load(open(sys.argv[2]))
out = {}
for path, text in pages.items():
    out[path] = {"labels": gen_toc.blocks(text),
                 "headings": [list(h) for h in gen_toc.headings(text)],
                 "refused": bool(gen_toc.refusals(text))}
json.dump(out, open(sys.argv[3], "w"))
'''


def main() -> None:
    repo, rev, base, head, out_path = sys.argv[1:6]
    names = subprocess.run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev],
                           capture_output=True, text=True, check=True).stdout.split("\n")
    pages = {}
    for name in names:
        if name.endswith(".md"):
            blob = subprocess.run(["git", "-C", repo, "show", f"{rev}:{name}"],
                                  capture_output=True, check=True).stdout
            pages[name] = blob.decode("utf-8", errors="surrogateescape")
    tmp = Path(out_path).with_suffix(".work")
    tmp.mkdir(exist_ok=True)
    (tmp / "pages.json").write_text(json.dumps(pages))
    (tmp / "helper.py").write_text(HELPER)
    walks = {}
    for tag, tree in (("base", base), ("head", head)):
        subprocess.run([sys.executable, "-B", str(tmp / "helper.py"), tree,
                        str(tmp / "pages.json"), str(tmp / f"{tag}.json")], check=True)
        walks[tag] = json.loads((tmp / f"{tag}.json").read_text())
    diffs = {p: {"lines": [i + 1 for i, (a, b) in enumerate(zip(walks["base"][p]["labels"],
                                                               walks["head"][p]["labels"])) if a != b],
                 "base_headings": walks["base"][p]["headings"],
                 "head_headings": walks["head"][p]["headings"]}
             for p in pages if walks["base"][p] != walks["head"][p]}
    digest = {tag: hashlib.sha256(json.dumps([walks[tag][p]["labels"] for p in sorted(pages)])
                                  .encode()).hexdigest() for tag in walks}
    result = {"rev": rev, "pages": len(pages), "differing_pages": diffs, "label_digest": digest}
    json.dump(result, open(out_path, "w"), indent=1)
    print(f"{rev[:12]}: {len(pages)} tracked .md pages, {len(diffs)} differ; "
          f"base digest {digest['base'][:12]} head digest {digest['head'][:12]}")
    for p, d in diffs.items():
        print("  DIFF", p, d["lines"][:10])


if __name__ == "__main__":
    main()
