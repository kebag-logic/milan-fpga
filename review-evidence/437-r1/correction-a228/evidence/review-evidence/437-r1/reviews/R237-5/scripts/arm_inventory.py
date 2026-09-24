#!/usr/bin/env python3
"""Arm inventory of gen_toc's self-test at one tree: every family's arm
names and pages, and for every page the walk's blocks(), headings() and
(where present) line_kinds() answers. Usage:

    python3 arm_inventory.py <tree> <out.json> [pages.json]

<tree> is an extracted source tree (scripts/ importable). With pages.json
(a list of pages), the answers are computed for those pages too, so the
base walk and the head renderer can be compared on one population.
"""
import json
import sys
from pathlib import Path


def main() -> int:
    tree, out = Path(sys.argv[1]), Path(sys.argv[2])
    extra = json.loads(Path(sys.argv[3]).read_text()) if len(sys.argv) > 3 else []
    sys.path.insert(0, str(tree / "scripts"))
    import gen_toc
    sys.modules.setdefault("gen_toc", gen_toc)
    import gen_toc_cases as cases
    import gen_toc_closer_cases as closers
    fam = {"walk": cases.walk_arms(), "tag": cases.tag_arms(),
           "guard": cases.guard_arms(), "heading": cases.heading_arms(),
           "predecessor": cases.predecessor_arms(),
           "provenance": cases.provenance_arms(),
           "refusal": cases.refusal_arms(), "I440": closers.closer_arms()}
    try:
        import gen_toc_shape_cases as shapes
        fam["shape"] = shapes.shape_arms()
    except ImportError:
        pass
    arms = {name: [[a[0], a[1]] for a in arms] for name, arms in fam.items()}
    pages = sorted({a[1] for arms_ in fam.values() for a in arms_} | set(extra))
    answers = {}
    for page in pages:
        entry = {}
        try:
            entry["blocks"] = gen_toc.blocks(page)
            entry["headings"] = [list(h) for h in gen_toc.headings(page)]
            if hasattr(gen_toc, "line_kinds"):
                entry["line_kinds"] = gen_toc.line_kinds(page)
            entry["refused"] = bool(gen_toc.refusals(page))
        except Exception as exc:  # recorded, not hidden
            entry["error"] = f"{type(exc).__name__}: {exc}"
        answers[page] = entry
    out.write_text(json.dumps({"arms": arms, "answers": answers},
                              ensure_ascii=False, indent=0))
    print(f"{tree}: {sum(len(v) for v in arms.values())} arms, "
          f"{len(pages)} pages -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
