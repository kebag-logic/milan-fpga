#!/usr/bin/env python3
"""Compare the base and head arm inventories (arm_inventory.py outputs).

Usage: compare_inventory.py <inv_base.json> <inv_head.json> <shapes.json>

Reports: arm names removed or added per family; every arm page on which the
base walk and the head renderer answer differently (blocks or headings);
and whether each such page is recorded in the shape fixture with GitHub's
rendering, and whether the head headings equal the recorded ones.
"""
import json
import sys


def main() -> int:
    base = json.load(open(sys.argv[1]))
    head = json.load(open(sys.argv[2]))
    shapes = json.load(open(sys.argv[3]))["shapes"]
    by_page = {}
    for s in shapes:
        by_page.setdefault(s["page"], []).append(s)
    for fam in sorted(set(base["arms"]) | set(head["arms"])):
        b = [a[0] for a in base["arms"].get(fam, [])]
        h = [a[0] for a in head["arms"].get(fam, [])]
        gone = [n for n in b if n not in h]
        new = [n for n in h if n not in b]
        print(f"family {fam}: base {len(b)} head {len(h)} "
              f"removed {len(gone)} added {len(new)}")
        for n in gone:
            print(f"   REMOVED: {n}")
    base_pages = {a[1] for arms in base["arms"].values() for a in arms}
    diff_blocks, diff_heads = [], []
    for page, hb in head["answers"].items():
        bb = base["answers"].get(page, {})
        if "error" in hb or "error" in bb:
            print("ERROR", repr(page)[:80], hb.get("error"), bb.get("error"))
            continue
        if bb["blocks"] != hb["blocks"]:
            diff_blocks.append(page)
        if bb["headings"] != hb["headings"]:
            diff_heads.append(page)
    both = sorted(set(diff_blocks) | set(diff_heads))
    print(f"pages answered differently: {len(both)} "
          f"(blocks {len(diff_blocks)}, headings {len(diff_heads)}); "
          f"of them base-arm pages: {len(set(both) & base_pages)}")
    unrecorded = 0
    for page in both:
        rec = by_page.get(page)
        tag = "recorded" if rec else "NOT RECORDED"
        agree = ""
        if rec:
            want = [tuple(x) for x in rec[0]["headings"]]
            for extra in rec[0].get("github_only", {}).get("headings", []):
                want.remove(tuple(extra))
            got = [(h[0], " ".join(h[1].split())) for h in head["answers"][page]["headings"]]
            agree = f" sets={sorted({r['set'] for r in rec})}"
        else:
            unrecorded += 1
        in_base = "base-arm" if page in base_pages else "head-only"
        print(f" - [{tag}; {in_base}]{agree} {page!r}"[:260])
        print(f"     base blocks {base['answers'][page]['blocks']}"[:260])
        print(f"     head blocks {head['answers'][page]['blocks']}"[:260])
        print(f"     base heads {base['answers'][page]['headings']}"[:260])
        print(f"     head heads {head['answers'][page]['headings']}"[:260])
    print(f"differing pages without a recorded rendering: {unrecorded}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
