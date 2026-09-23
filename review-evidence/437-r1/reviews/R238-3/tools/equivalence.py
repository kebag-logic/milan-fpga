#!/usr/bin/env python3
"""Does a surviving mutant change any heading the walk lists?

Usage: equivalence.py <head-scripts> <mutant-scripts-root> <out.json> <mutant-id>...
Regenerates the two sweep corpora (seeds 4371 full vocabulary, 5162 Markdown
only), adds every committed fixture page, and compares `headings()` of the
head walk and of each mutant walk page by page.
"""
import json
import os
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def corpus(head: str) -> list:
    pages = []
    for seed, count, vocab in ((4371, 60000, "full"), (5162, 80000, "markdown")):
        env = dict(os.environ, FUZZ_VOCAB=vocab)
        code = ("import sys,random,json;sys.path.insert(0,%r);import fuzz_diff as f;"
                "r=random.Random(%d);print(json.dumps(sorted({f.page(r) for _ in range(%d)})))"
                % (str(HERE), seed, count))
        out = subprocess.run([sys.executable, "-B", "-c", code], env=env, capture_output=True,
                             text=True, check=True).stdout
        pages += json.loads(out)
    for fixture in ("gen_toc_family_one.json", "gen_toc_comment_shapes.json",
                    "gen_toc_container_walk.json"):
        pages += [s["page"] for s in json.loads((Path(head) / fixture).read_text())["shapes"]]
    return sorted(set(pages))


def walk(scripts: str, pages: list, tmp: Path) -> list:
    src, dst = tmp.with_suffix(".in.json"), tmp.with_suffix(".out.json")
    src.write_text(json.dumps([{"name": str(i), "page": p} for i, p in enumerate(pages)]))
    subprocess.run([sys.executable, "-B", str(HERE / "walk.py"), scripts, str(src), str(dst)],
                   check=True)
    rows = json.loads(dst.read_text())
    src.unlink()
    dst.unlink()
    return [r["walk"] for r in rows]


def main() -> int:
    head, root, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    pages = corpus(head)
    base = walk(head, pages, out.with_name("eq-head"))
    report = {"pages": len(pages)}
    for ident in sys.argv[4:]:
        mut = walk(str(root / ident / "scripts"), pages, out.with_name(f"eq-{ident}"))
        diff = [{"page": p, "head": h, "mutant": m} for p, h, m in zip(pages, base, mut) if h != m]
        report[ident] = {"differing_pages": len(diff), "examples": diff[:40]}
        print(f"{ident}: {len(diff)} of {len(pages)} pages list different headings")
    out.write_text(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
