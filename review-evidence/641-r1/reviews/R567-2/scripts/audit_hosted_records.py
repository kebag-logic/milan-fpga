#!/usr/bin/env python3
"""Validate published worker records against this head's actual top inventory."""
import json, subprocess, sys
from pathlib import Path
repo=Path(sys.argv[1]);p=Path(sys.argv[2])
sha='21a40e975a5e37453dd8089f80d5ea1b681eddc1';records=[]
for directory in sorted((p/'receipts/hosted-artifacts').iterdir()):
 assert (directory/'TARGET_SHA').read_text().strip()==sha
 for path in directory.glob('*.result'):
  row=dict(line.split('=',1) for line in path.read_text().splitlines())
  assert row['status']=='PASS',row
  if row['kind']=='top':assert row['mode']=='full' and int(row['cells'])>=0
  records.append(row)
tops=[r['name'] for r in records if r['kind']=='top']
expected=subprocess.check_output(['bash','syn/yosys/run.sh','--list'],cwd=repo,text=True).splitlines()
assert len(tops)==len(set(tops))==58
assert set(tops)==set(expected),(set(tops)-set(expected),set(expected)-set(tops))
out={'target_sha':sha,'unique_top_records':len(tops),'exact_inventory_match':True,'all_records_pass':True,'structural_records':[r for r in records if r['kind']=='gate']}
print(json.dumps(out,indent=2))
