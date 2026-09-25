#!/usr/bin/env python3
"""Export receipts with only machine-local path prefixes replaced.
Raw originals stay in scratch. Program output, verdicts and rows are unchanged.
"""
import argparse, hashlib, json, os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--root',type=Path,required=True);a=p.parse_args()
pkt=a.packet.resolve();root=a.root.resolve()
replacements=[(str(pkt/'scratch/sdk'),'$SDK'),(str(pkt/'scratch'),'$SCRATCH'),(str(pkt),'$PACKET'),(str(root),'$CHECKOUT'),(str(Path.home()),'$WORKSPACE_HOME')]
rows=[];dest=pkt/'receipts';dest.mkdir(exist_ok=True)
for source in sorted((pkt/'scratch/raw').glob('*')):
    if not source.is_file():continue
    data=source.read_bytes();text=data.decode()
    for before,after in replacements:text=text.replace(before,after)
    target=dest/source.name;target.write_text(text)
    rows.append({'path':str(target.relative_to(pkt)),'raw_sha256':hashlib.sha256(data).hexdigest(),'published_sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
source=pkt/'scratch/sdk-install.log';text=source.read_text()
for before,after in replacements:text=text.replace(before,after)
(dest/'sdk-install.log').write_text(text)
(pkt/'receipt-export.json').write_text(json.dumps({'transformation':'Only local path prefixes replaced by role placeholders; raw originals retained in unpublished scratch.','receipts':rows},indent=2)+'\n')
print('Exported',len(rows),'execution receipts and SDK provenance')
