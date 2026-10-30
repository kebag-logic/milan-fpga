#!/usr/bin/env python3
"""Verify publicly named post-seal cases without altering the source checkout."""
import json
import os
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
logs = packet / "receipts"
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), PYTHONDONTWRITEBYTECODE="1")
records = []
for short in ("411b35fc", "db9ab221"):
    root = scratch / ("fence-" + short)
    page = root / "docs/HDL_DEVELOPER.md"
    original = page.read_bytes()
    cases = {
        "underscore-ms": "The Sync receipt timeout is _125 ms_.\n",
        "underscore-minutes": "A _5 minutes_ countdown.\n",
        "underscore-word": "A _five minutes_ countdown.\n",
        "asterisk-control": "The Sync receipt timeout is *125 ms*.\n",
        "tilde-trailing-text": "~~~text\n~~~example\n~~~\n\nThe Sync receipt timeout is 125 ms.\n",
    }
    try:
        for name, addition in cases.items():
            page.write_bytes(original + ("\n" + addition).encode())
            result = subprocess.run(["make", "-j16", "docs"], cwd=root, env=env, capture_output=True, timeout=180)
            stem = "reconcile-" + short + "-" + name
            (logs / (stem + ".log")).write_bytes(result.stdout + result.stderr)
            (logs / (stem + ".rc")).write_text(str(result.returncode) + "\n")
            record = dict(revision=short, case=name, rc=result.returncode, addition=addition)
            records.append(record)
            print(json.dumps(record), flush=True)
    finally:
        page.write_bytes(original)
(logs / "reconciliation-probes.json").write_text(json.dumps(records, indent=2) + "\n")
assert [r["rc"] for r in records] == [0, 0, 0, 2, 2, 0, 0, 0, 2, 0]
