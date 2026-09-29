#!/usr/bin/env python3
"""Render gates.py result files as Markdown rows: command, rc, seconds, log size, SHA-256.
Usage: gates_table.py <results.jsonl> [<results.jsonl> ...]; one table per file."""
import json
import sys

for path in sys.argv[1:]:
    print(f"\n`{path.split('/')[-2]}`\n")
    print("| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |")
    print("|---|---|---:|---:|---:|---|")
    for line in open(path):
        r = json.loads(line)
        cmd = " ".join(c if not c.startswith("$VALIDATION_STORAGE/") else "<scratch>" for c in r["command"])
        print(f"| {r['group']} | `{cmd}` | {r['rc']} | {r['seconds']} | {r['size']:,} | "
              f"`{r['sha256'][:16]}…` |")
