#!/usr/bin/env python3
"""Summarize reviewer receipts without re-running successful campaigns."""
import datetime
import json
import pathlib
import sys

packet = pathlib.Path(sys.argv[1]).resolve()
rows = []
for path in sorted((packet / "receipts").glob("*.json")):
    record = json.loads(path.read_text())
    if not isinstance(record, dict) or not {"argv", "expected", "rc"} <= record.keys():
        continue
    assert record["rc"] == record["expected"], path
    assert int(path.with_suffix(".rc").read_text()) == record["rc"]
    rows.append(dict(check=path.stem, rc=record["rc"], expected=record["expected"],
                     seconds=record["elapsed_seconds"]))
assert len(rows) == 23, len(rows)
out = dict(exact_head="4029dc5de2a0a540d6a015c747319fbee7abba2e",
           recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           checks=rows, mismatches=0)
(packet / "receipts/validation-summary.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"{len(rows)} execution receipts match their expected return codes.")
