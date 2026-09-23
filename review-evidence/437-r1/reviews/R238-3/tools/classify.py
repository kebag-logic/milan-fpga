#!/usr/bin/env python3
"""Classify the sweep's regressions (base walk agreed with GitHub, head walk
does not) by the documented hazard classes their pages carry.

Usage: classify.py <results.json> [<results.json> ...]
A page may carry several classes; a regression carrying none is UNEXPLAINED.
"""
import json
import sys

CLASSES = [
    ("select element", lambda p: "<select>" in p),
    ("type 3-5 raw HTML (#413)", lambda p: "<? " in p or "<!DOCTYPE" in p),
    ("open quoted value", lambda p: "title='" in p),
    ("empty comment <!-->", lambda p: "<!-->" in p),
    ("opener GitHub prints as text", lambda p: "`<!--`" in p or "\\<!--" in p),
    ("other comment delimiter", lambda p: "<!--" in p.replace("<!-->", "").replace("`<!--`", "")
     .replace("\\<!--", "") or "-->" in p.replace("<!-->", "")),
]


def main() -> int:
    rows = [r for f in sys.argv[1:] for r in json.load(open(f))]
    reg = [r for r in rows if r["base_agrees"] and not r["head_agrees"]]
    tally, unexplained, by_dir = {}, [], {"escape": 0, "withhold": 0, "mixed": 0}
    for r in reg:
        extra = [h for h in r["head"] if h not in r["github"]]
        missing = [h for h in r["github"] if h not in r["head"]]
        d = "escape" if extra and not missing else "withhold" if missing and not extra else "mixed"
        by_dir[d] += 1
        hit = [name for name, test in CLASSES if test(r["page"])]
        for name in hit:
            tally[(name, d)] = tally.get((name, d), 0) + 1
        if not hit:
            unexplained.append(r)
        only = [n for n in hit]
        r["_classes"], r["_dir"] = only, d
    print(f"rendered {len(rows)}; regressions {len(reg)}; by direction {by_dir}")
    for (name, d), n in sorted(tally.items()):
        print(f"  {name} [{d}]: {n}")
    comment_free = [r for r in reg if not any(c in r["_classes"] for c in (
        "empty comment <!-->", "opener GitHub prints as text", "other comment delimiter"))]
    print(f"regressions with no comment delimiter at all: {len(comment_free)}")
    single = {}
    for r in reg:
        if len(r["_classes"]) == 1:
            single[(r["_classes"][0], r["_dir"])] = single.get((r["_classes"][0], r["_dir"]), 0) + 1
    print("regressions carrying exactly one class:")
    for (name, d), n in sorted(single.items()):
        print(f"  {name} [{d}]: {n}")
    print(f"UNEXPLAINED (no documented hazard token): {len(unexplained)}")
    for r in unexplained:
        print("  ", r["name"], r["github"], r["head"], json.dumps(r["page"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
