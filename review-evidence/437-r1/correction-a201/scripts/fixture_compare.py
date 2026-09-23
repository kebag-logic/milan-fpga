#!/usr/bin/env python3
"""Every recorded fixture shape under the base, the reviewed head and the
working tree: which agree with GitHub's recorded headings."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import walks

BASE, PREV = "574c29fa111c74e5e5ed63e4670aff1f492e28e2", "e4906bfca65c61e7e109e3532ac1b2dd5b4c0096"
FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json", "gen_toc_container_walk.json")


def main():
    fixdir = Path(sys.argv[1]) if len(sys.argv) > 1 else walks.tree(PREV)
    rows = []
    for fx in FIXTURES:
        path = fixdir / fx
        if not path.exists():
            continue
        for s in json.loads(path.read_text())["shapes"]:
            rows.append((fx, s))
    pages = [s["page"] for _, s in rows]
    res = {rev: walks.walk(rev, pages) for rev in (BASE, PREV, "work")}
    out = []
    for i, (fx, s) in enumerate(rows):
        gh = s["headings"]
        b, p, w = (res[r][i]["headings"] for r in (BASE, PREV, "work"))
        out.append({"fixture": fx, "name": s["name"], "page": s["page"], "github": gh,
                    "base": b, "prev": p, "work": w,
                    "base_ok": b == gh, "prev_ok": p == gh, "work_ok": w == gh,
                    "limitation": s.get("limitation")})
    json.dump(out, sys.stdout, indent=1)


if __name__ == "__main__":
    main()
