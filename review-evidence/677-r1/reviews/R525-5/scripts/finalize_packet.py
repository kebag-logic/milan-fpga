#!/usr/bin/env python3
"""Manifest only scripts and receipts, never disposable scratch trees."""
import hashlib,pathlib
packet=pathlib.Path(__file__).resolve().parents[1]
files=sorted([packet/"REPORT.md",*(packet/"scripts").rglob("*.py"),*(f for f in (packet/"receipts").rglob("*") if f.is_file())])
lines=[]
for f in files:
 assert not f.is_symlink()
 lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+f.relative_to(packet).as_posix())
(packet/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
for line in lines:
 digest,name=line.split("  ",1)
 assert hashlib.sha256((packet/name).read_bytes()).hexdigest()==digest
print("PASS manifest:",len(lines),"publishable files; scratch excluded")
