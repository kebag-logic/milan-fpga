#!/usr/bin/env python3
"""Render every shape of walk_shapes.py fresh and write the committed fixture
scripts/gen_toc_container_walk.json (format of the two existing fixtures:
indent 1, keys sorted, ASCII). Also writes the raw receipts beside it.

Usage: make_walk_fixture.py FIXTURE.json RECEIPTS.jsonl
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render import render  # noqa: E402
from walk_shapes import shapes  # noqa: E402

ABOUT = ("Issue #437 container walk and rendered-comment model (the R237-2 "
         "correction): a tag under a nested block, a block opened in an item, "
         "an empty item, lazy lines, raw HTML read as the page's HTML parser "
         "reads it, closers in Markdown text and comments opened in prose. "
         "pins names the finding or rule each shape holds.")
METHOD = ("Each page was sent to GitHub's Markdown API (POST /markdown, mode gfm, "
          "context kebag-logic/milan-fpga). request_bytes is the exact JSON body "
          "sent (keys sorted, no spaces, <, > and & escaped), response_bytes the "
          "exact HTML returned, each with its SHA-256; headings is every heading "
          "element of response_bytes as [level, text].")


def main() -> int:
    fixture, receipts = Path(sys.argv[1]), Path(sys.argv[2])
    rows = []
    with receipts.open("w") as out:
        for name, pins, page in shapes():
            row = render(page)
            out.write(json.dumps(row) + "\n")
            rows.append({"headings": row["headings"], "name": name, "page": page,
                         "pins": pins, "recorded_utc": row["recorded_utc"],
                         "request_bytes": row["request_bytes"],
                         "request_sha256": row["request_sha256"],
                         "response_bytes": row["response_bytes"],
                         "response_sha256": row["response_sha256"]})
    fixture.write_text(json.dumps({"about": ABOUT, "method": METHOD, "shapes": rows},
                                  indent=1, sort_keys=True, ensure_ascii=True) + "\n",
                       encoding="ascii")
    print(f"{len(rows)} shapes rendered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
