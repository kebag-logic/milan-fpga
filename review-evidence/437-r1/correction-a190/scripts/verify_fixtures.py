#!/usr/bin/env python3
"""Re-render every shape of the three committed fixtures and compare bytes.

Usage: verify_fixtures.py OUT.json
Each shape's page is sent fresh to GitHub's Markdown API (gfm); the request
bytes must equal the recorded request bytes, the response bytes the recorded
response bytes, and the walk at the checkout must list the recorded headings.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render import render  # noqa: E402

LANE = Path("$LANES/437-container-paragraph-scopes/scripts")
FIXTURES = ("gen_toc_family_one.json", "gen_toc_comment_shapes.json", "gen_toc_container_walk.json")


def main() -> int:
    sys.path.insert(0, str(LANE))
    import gen_toc
    rows, bad = [], 0
    for fixture in FIXTURES:
        for shape in json.loads((LANE / fixture).read_text(encoding="ascii"))["shapes"]:
            fresh = render(shape["page"])
            walk = [[lvl, raw] for lvl, raw, _ in gen_toc.headings(shape["page"])]
            ok = (fresh["request_bytes"] == shape["request_bytes"]
                  and fresh["response_bytes"] == shape["response_bytes"]
                  and walk == shape["headings"])
            bad += not ok
            rows.append({"fixture": fixture, "name": shape["name"], "identical": ok,
                         "fresh_response_sha256": fresh["response_sha256"],
                         "recorded_response_sha256": shape["response_sha256"],
                         "fresh_utc": fresh["recorded_utc"], "walk": walk,
                         "recorded_headings": shape["headings"]})
    Path(sys.argv[1]).write_text(json.dumps({"rows": rows}, indent=1) + "\n")
    print(f"{len(rows)} shapes re-rendered; {len(rows) - bad} byte-identical and agreeing, {bad} not")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
