#!/usr/bin/env python3
"""R226-2: enumerate the TOC arm families and the I440-E label rows of one tree.

Usage: python3 -B arm_population.py <tree-root> <out.json>

Imports the tree's own scripts (never the review clone), lists every arm as
(family, name, sha256(page), page) and, for the I440 family, the block kind the
arm's predicate expects on the probe line (read from its closure). The
check_em_dash I440-E rows are read from gen_toc_closer_cases._label_rows().
Each arm is also graded against the tree's own walk, so the file records
what the tree's own runner would score.
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
sys.dont_write_bytecode = True

import gen_toc  # noqa: E402

sys.modules.setdefault("gen_toc", gen_toc)
import gen_toc_cases as cases  # noqa: E402
import gen_toc_closer_cases as closers  # noqa: E402


def expected_kind(pred):
    cells = getattr(pred, "__closure__", None) or ()
    vals = [c.cell_contents for c in cells]
    return vals[0] if len(vals) == 1 and isinstance(vals[0], str) else None


families = {"walk": cases.walk_arms(), "tag": cases.tag_arms(),
            "guard": cases.guard_arms(), "heading": cases.heading_arms(),
            "predecessor": cases.predecessor_arms(),
            "provenance": cases.provenance_arms(),
            "refusal": cases.refusal_arms(), "I440": closers.closer_arms()}
on_walk = {"walk", "tag", "I440"}
out = {"root": str(root), "MIN_ARMS": gen_toc.MIN_ARMS,
       "ARM_FAMILIES": list(gen_toc.ARM_FAMILIES),
       "RAW_HTML_TAGS": list(gen_toc.RAW_HTML_TAGS), "arms": [],
       "label_rows": [list(r) for r in closers._label_rows()]}
for fam, arms in families.items():
    for name, page, holds in arms:
        page_s = page if isinstance(page, str) else repr(page)
        graded = bool(holds(gen_toc.blocks(page)) if fam in on_walk else holds(page))
        out["arms"].append({
            "family": fam, "name": name,
            "page_sha256": hashlib.sha256(page_s.encode("utf-8", "surrogatepass")).hexdigest(),
            "page": page_s,
            "expected_kind": expected_kind(holds) if fam == "I440" else None,
            "holds_here": graded})
out["counts"] = {fam: len(a) for fam, a in families.items()}
out["total"] = sum(out["counts"].values())
Path(sys.argv[2]).write_text(json.dumps(out, indent=1, ensure_ascii=True) + "\n")
print(json.dumps({"root": str(root), "counts": out["counts"], "total": out["total"],
                  "label_rows": len(out["label_rows"]),
                  "failing_here": sum(1 for a in out["arms"] if not a["holds_here"])}))
