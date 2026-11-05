#!/usr/bin/env python3
"""Copy a sharded sweep's small records into the receipts, and summarise its suite logs.

For each <sweep>/shard-<k>: spec/complete.json, spec/results.json and spec/01.log (the runner's
own record and the sweep's tally) are copied; every suite and preflight log is listed in
suites.md with its size, sha256 and its last three lines (logs stay in scratch, over 200 KB).
Usage: collect_sweep.py <sweep-dir> <receipt-dir>"""
import hashlib
import shutil
import sys
from pathlib import Path

sweep, dest = Path(sys.argv[1]), Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=True)
for shard in sorted(sweep.glob("shard-*")):
    out = dest / shard.name
    out.mkdir(exist_ok=True)
    for name in ("complete.json", "results.json", "01.log", "02.log"):
        if (shard / "spec" / name).is_file():
            shutil.copy(shard / "spec" / name, out / name)
    rows = ["| Log | Bytes | sha256 | Last lines |", "|---|---:|---|---|"]
    for log in sorted((shard / "logs").rglob("*.log")):
        data = log.read_bytes()
        tail = [line.strip().replace("|", "/") for line in data.decode(errors="replace").splitlines()
                if line.strip()][-3:]
        rows.append(f"| `{log.relative_to(shard / 'logs').as_posix()}` | {len(data)} | "
                    f"`{hashlib.sha256(data).hexdigest()}` | {' / '.join(tail)[:400]} |")
    (out / "suites.md").write_text(f"# {shard.name} suite logs\n\n" + "\n".join(rows) + "\n")
print("collected", sorted(p.name for p in dest.iterdir()))
