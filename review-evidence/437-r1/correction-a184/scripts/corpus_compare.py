#!/usr/bin/env python3
"""AC4: classify every tracked Markdown page with each walk and compare.

Populations: the tracked *.md pages of the base tree 88e9276b, of live dev
483a133e, and of the lane HEAD commit (read from git objects, not the
working tree). Walks: base 88e9276b, a172 b5e6c23e, and the lane working
tree's scripts/gen_toc.py. For every page: blocks, line_kinds, headings with
anchors, plan, generated_block, owns and refusals. Prints and writes the
per-population digests and every differing page.

Usage: corpus_compare.py OUT.json
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from three_way import LANE, REVS, load  # noqa: E402

TREES = {"base": REVS["base"], "dev": "483a133ed08867ea0d300d2b4a027b5b48a4282f", "head": "HEAD"}


def git(*a: str) -> str:
    return subprocess.run(["git", "-C", str(LANE), *a], check=True, capture_output=True,
                          text=True).stdout


def population(rev: str) -> dict[str, str]:
    names = [n for n in git("ls-tree", "-r", "--name-only", rev).split("\n") if n.endswith(".md")]
    return {n: git("show", f"{rev}:{n}") for n in names}


def classify(mod, rel: str, text: str) -> dict:
    return {"blocks": mod.blocks(text), "line_kinds": mod.line_kinds(text),
            "headings": mod.headings(text), "plan": mod.plan(text),
            "generated_block": mod.generated_block(text, rel), "owns": mod.owns(rel, text),
            "refusals": mod.refusals(text)}


def main() -> int:
    out = {"trees": {k: git("rev-parse", v).strip() for k, v in TREES.items()}, "populations": {}}
    with tempfile.TemporaryDirectory(prefix="a184.corpus.") as tmp:
        walks = {n: load(n, r, Path(tmp)) for n, r in REVS.items()}
        out["walk_sha256"] = {n: s for n, (_, s) in walks.items()}
        for tree, rev in TREES.items():
            pages = population(rev)
            res = {n: {rel: classify(mod, rel, text) for rel, text in pages.items()}
                   for n, (mod, _) in walks.items()}
            digest = {n: hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()
                      for n, r in res.items()}
            diffs = {n: sorted(rel for rel in pages if res[n][rel] != res["base"][rel])
                     for n in walks if n != "base"}
            lines = sum(t.count("\n") + 1 for t in pages.values())
            out["populations"][tree] = {"pages": len(pages), "lines": lines, "digests": digest,
                                        "pages_differing_from_base_walk": diffs}
            print(tree, len(pages), "pages", lines, "lines", digest, "diffs", diffs)
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + "\n")
    bad = any(d for p in out["populations"].values() for d in p["pages_differing_from_base_walk"].values())
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
