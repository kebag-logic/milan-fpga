#!/usr/bin/env python3
"""Show what the production union prints for a passing union with recorded rows.

Usage: python3 -I union_output_probe.py <tree> <leg0.json> <leg1.json>

Takes the real host leg receipts, marks them as run with both requirement
flags and a passing own verdict, and drops the host's no-LiteX rows (the host
has no LiteX), keeping only recorded-reason rows. Then runs the production
`ci_builder_legs.union` and prints everything it writes to stdout.
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(tree / "scripts"))
    import ci_builder_legs as legs  # noqa: E402

    receipts = [json.loads(Path(p).read_text()) for p in sys.argv[2:4]]
    for receipt in receipts:
        driver = receipt["driver"]
        driver["requirements"] = list(legs.REQUIRED)
        driver["require_elaboration"] = 0
        for row in driver["gates"]:
            row["not_run"] = [item for item in row["not_run"] if item[2] == "row"]
    names = legs.inventory(tree)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        result = legs.union(receipts, receipts[0]["head"], receipts[0]["tree"], names)
    print("union result:", result["union"], "not_run rows in JSON:", len(result["not_run"]))
    print("--- union stdout ---")
    print(captured.getvalue())
    print("--- end ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
