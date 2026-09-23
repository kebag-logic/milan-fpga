#!/usr/bin/env python3
"""Re-render every shape of the committed fixtures, fresh, at the lane HEAD,
and compare request and response bytes with what the fixtures record.

Usage: verify_fixture_at_head.py OUT.json
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import render_one  # noqa: E402
from three_way import LANE  # noqa: E402

FIXTURES = ("scripts/gen_toc_family_one.json", "scripts/gen_toc_comment_shapes.json")


def main() -> int:
    head = subprocess.run(["git", "-C", str(LANE), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()
    rows = []
    for f in FIXTURES:
        text = subprocess.run(["git", "-C", str(LANE), "show", f"HEAD:{f}"], check=True,
                              capture_output=True, text=True).stdout
        rows += [(f, s) for s in json.loads(text)["shapes"]]
    with ThreadPoolExecutor(max_workers=4) as pool:
        fresh = list(pool.map(lambda fs: render_one({"id": fs[1]["name"], "page": fs[1]["page"]}), rows))
    out, bad = [], []
    for (f, s), r in zip(rows, fresh):
        same = {"request_bytes": r["request_bytes"] == s["request_bytes"],
                "response_bytes": r["response_bytes"] == s["response_bytes"],
                "headings": r["github"] == s["headings"],
                "wire_length": r["request_length_matches_wire"], "exit": r["exit"] == 0}
        if not all(same.values()):
            bad.append(s["name"])
        out.append({"fixture": f, "name": s["name"], "checks": same, "fresh": r})
    doc = {"head": head, "shapes": len(out), "mismatches": bad, "rows": out}
    Path(sys.argv[1]).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
    print(f"head {head}: {len(out)} shapes re-rendered, mismatches {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
