#!/usr/bin/env python3
"""Check the source and packet, then enumerate every publication artifact."""
import ast
import hashlib
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(sys.argv[2]).resolve()
report = (packet / "REPORT.md").read_text()
assert report.splitlines()[0] == "[R609] POSITIVE - exact head 4029dc5de2a0a540d6a015c747319fbee7abba2e"
assert report.splitlines()[-1] == "R609-4 FINISHED"
assert "SKELETON" not in report
for lens in ("Conformance", "RTL", "Robustness", "Tests", "Docs"):
    assert f"| {lens} | CLEAN |" in report
for script in (packet / "scripts").glob("*.py"):
    ast.parse(script.read_text())
result = subprocess.check_output(["rtk", "proxy", "python3", packet / "scripts/integrity.py", root])
(packet / "receipts/integrity-after.json").write_bytes(result)
subprocess.run(["rtk", "proxy", "python3", packet / "scripts/summarize.py", packet], check=True)
files = sorted(p for folder in ("scripts", "receipts") for p in (packet / folder).rglob("*") if p.is_file())
files.append(packet / "REPORT.md")
files.sort()
assert not any("scratch" in p.relative_to(packet).parts for p in files)
lines = [hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.relative_to(packet).as_posix() for p in files]
(packet / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")
for line in lines:
    digest, relative = line.split("  ", 1)
    assert hashlib.sha256((packet / relative).read_bytes()).hexdigest() == digest
print(f"Verified {len(lines)} publication files; scratch excluded; exact source intact.")
