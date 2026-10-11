#!/usr/bin/env python3
"""List the complete publication set, excluding scratch and peer reports."""
import argparse, hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("packet",type=Path);a=ap.parse_args();p=a.packet.resolve()
files=[p/"REPORT.md"]
for root in ["receipts","scripts","public/retained-r1"]:
 files.extend(f for f in (p/root).rglob("*") if f.is_file() and "__pycache__" not in f.parts)
for name in ["pr-body.txt","upstream-MANIFEST.json","issue151.json","frozen-scope.json","issue-comment-6105580039.json","pr-comment-6106551240.json","hosted-runs.json","hosted-checks.json","hosted-checks-final.json","hosted-pr-jobs.json","hosted-push-jobs.json","hosted-source-docs.log","hosted-source-portability.log"]:
 files.append(p/"public"/name)
lines=[]
for f in sorted(set(files)):
 assert f.is_file(),f
 rel=f.relative_to(p).as_posix();assert not rel.startswith("scratch/")
 lines.append(hashlib.sha256(f.read_bytes()).hexdigest()+"  "+rel)
(p/"MANIFEST.sha256").write_text("\n".join(lines)+"\n")
print(f"Manifest: {len(lines)} publishable files; scratch and prior review reports excluded")
