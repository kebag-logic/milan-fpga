#!/usr/bin/env python3
"""Extract a hash-verified disposable Clang 18 lexer; install nothing globally."""
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

packet = Path(__file__).resolve().parents[1]
work = packet / "scratch/clang18"
work.mkdir(parents=True, exist_ok=True)
for row in json.loads((packet / "receipts/clang18-download.json").read_text()):
    name = row["url"].rsplit("/", 1)[1]
    path = work / name
    if not path.exists():
        path.write_bytes(urllib.request.urlopen(row["url"]).read())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
    members = subprocess.check_output(["ar", "t", str(path)], text=True).splitlines()
    member = next(m for m in members if m.startswith("data.tar"))
    archive = path.with_suffix(".tar")
    archive.write_bytes(subprocess.check_output(["ar", "p", str(path), member]))
    subprocess.run(["bsdtar", "-xf", str(archive), "-C", str(work)], check=True)
print("Disposable lexer ready under scratch/clang18.")
