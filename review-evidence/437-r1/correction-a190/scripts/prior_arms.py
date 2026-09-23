#!/usr/bin/env python3
"""Every arm page of the TOC self-test, classified by the base, starting and
new walks: blocks() and headings() per page, differences listed by family.

Usage: prior_arms.py OUT.json
The arm pages come from the checkout's case tables (the base-era families are
unchanged there); the base and starting walks are loaded from git.
"""
import json, sys
from pathlib import Path

PKT = Path("$REVIEWS/437-a190-packet")
LANE = "$LANES/437-container-paragraph-scopes"
sys.path.insert(0, str(PKT / "scripts"))
from sweep import load_rev  # noqa: E402


def main():
    base = load_rev("88e9276b2a220c716f64a843f7e1eb8f9265e896", "base")
    start = load_rev("4741498f3b2b4f67f431037d327c96cf65691278", "start")
    sys.path.insert(0, f"{LANE}/scripts")
    import gen_toc
    sys.modules.setdefault("gen_toc", gen_toc)
    import gen_toc_cases as cases, gen_toc_closer_cases as closers, gen_toc_container_cases as containers
    fams = {"walk": cases.walk_arms(), "tag": cases.tag_arms(), "guard": cases.guard_arms(),
            "heading": cases.heading_arms(), "predecessor": cases.predecessor_arms(),
            "provenance": cases.provenance_arms(), "refusal": cases.refusal_arms(),
            "I440": closers.closer_arms(), "I437": containers.container_arms()}
    out = {}
    for fam, arms in fams.items():
        pages = list(dict.fromkeys(page for _, page, _ in arms if page))
        diff_base, diff_start = [], []
        for p in pages:
            if gen_toc.refusals(p):
                continue
            n = (gen_toc.blocks(p), gen_toc.headings(p))
            if (base.blocks(p), base.headings(p)) != n:
                diff_base.append(p)
            if (start.blocks(p), start.headings(p)) != n:
                diff_start.append(p)
        out[fam] = {"arms": len(arms), "pages": len(pages), "differ_from_base": diff_base,
                    "differ_from_start": diff_start}
        print(f"{fam:12} {len(arms):5} arms {len(pages):5} pages; differ from base "
              f"{len(diff_base)}, from start {len(diff_start)}")
    Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
