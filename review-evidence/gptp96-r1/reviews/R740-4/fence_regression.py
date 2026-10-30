#!/usr/bin/env python3
"""Compare real-page fence probes at the reviewed and preceding commits."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

source = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / "scratch"
logs = packet / "receipts"
env = dict(os.environ, TMPDIR=str(scratch / "tmp"), PYTHONDONTWRITEBYTECODE="1")
rows = []
for revision in ("411b35fc", "db9ab2215ba18aec4c1828090b3611b001dbf2b8"):
    short = revision[:8]
    root = scratch / ("fence-" + short)
    root.mkdir(exist_ok=True)
    archive = scratch / ("fence-" + short + ".tar")
    with archive.open("wb") as out:
        subprocess.run(["git", "archive", revision], cwd=source, stdout=out, check=True)
    with tarfile.open(archive) as stream:
        stream.extractall(root, filter="data")
    target = root / "docs/HDL_DEVELOPER.md"
    original = target.read_bytes()
    cases = {
        "baseline": "",
        "plain-copy": "The Sync receipt timeout is 125 ms.\n",
        "fenced-copy": "~~~~text\n~~~\n~~~~\n\nThe Sync receipt timeout is 125 ms.\n",
        "four-marker-control": "~~~~text\nexample\n~~~~\n\nThe Sync receipt timeout is 125 ms.\n",
    }
    try:
        for name, addition in cases.items():
            target.write_bytes(original + ("\n" + addition).encode() if addition else original)
            result = subprocess.run(["make", "-j16", "docs"], cwd=root, env=env, capture_output=True, timeout=180)
            stem = "fence-" + short + "-" + name
            (logs / (stem + ".log")).write_bytes(result.stdout + result.stderr)
            (logs / (stem + ".rc")).write_text(str(result.returncode) + "\n")
            record = dict(revision=revision, case=name, rc=result.returncode, addition=addition,
                          mutated_page_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
            rows.append(record)
            print(json.dumps(record), flush=True)
    finally:
        target.write_bytes(original)
(logs / "fence-regression.json").write_text(json.dumps(rows, indent=2) + "\n")
expected = [0, 2, 2, 2, 0, 2, 0, 2]
assert [r["rc"] for r in rows] == expected, rows
