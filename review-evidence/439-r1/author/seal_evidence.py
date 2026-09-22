#!/usr/bin/env python3
"""Seal existing evidence after the public author handoff; verify every digest."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
p = Path(__file__).resolve().parent
root = Path("$CANDIDATE")
head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],check=True,capture_output=True,text=True).stdout.strip()
assert head == "f01f237d4b48c7b1ed59c80aca51430901791624",head
status = subprocess.run(["git", "-C", str(root), "status", "--porcelain=v2"],check=True,capture_output=True,text=True).stdout
assert not status,status
(p/"seal-command.json").write_text(json.dumps(dict(argv=["rtk","proxy","python3",str(Path(__file__).resolve())], head=head, status=status),indent=2)+"\n")
records = [json.loads(line) for line in (p/"commands.jsonl").read_text().splitlines()]
rows = ["label\texit\tseconds\targv\tlast stdout line"]
for record in records:
    output = (p/"logs"/f"{record['label']}.stdout").read_text().splitlines()
    rows.append(f"{record['label']}\t{record['exit']}\t{record['seconds']:.3f}\t{json.dumps(record['argv'])}\t{output[-1] if output else ''}")
(p/"results.tsv").write_text("\n".join(rows)+"\n")
files = sorted(f for f in p.rglob("*") if f.is_file() and f.name != "SHA256SUMS")
checksums = [(hashlib.sha256(f.read_bytes()).hexdigest(), f.relative_to(p)) for f in files]
(p/"SHA256SUMS").write_text("".join(f"{digest}  {rel}\n" for digest,rel in checksums))
for digest,rel in checksums:
    assert hashlib.sha256((p/rel).read_bytes()).hexdigest() == digest,rel
print(f"source={head} clean; {len(checksums)} evidence checksums verified")
print(f"SHA256SUMS sha256={hashlib.sha256((p/'SHA256SUMS').read_bytes()).hexdigest()}")
