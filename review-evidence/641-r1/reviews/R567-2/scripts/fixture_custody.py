#!/usr/bin/env python3
"""Bind the public measurements to the committed derived-size trace fixture."""
import argparse, hashlib, importlib.util, json, tempfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument("--repo",type=Path,required=True);ap.add_argument("--evidence",type=Path,required=True);ap.add_argument("--work",type=Path,required=True);a=ap.parse_args()
root=a.repo.resolve();a.work.mkdir(parents=True,exist_ok=True)
path=root/'tb/verilator/fw_service_budget/run.py'
spec=importlib.util.spec_from_file_location('service_run',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
oracle=json.loads((path.parent/'oracle.json').read_text());results=[]
names=['MEASUREMENT-1X1-ALL.json','MEASUREMENT-8X8-ALL.json','MEASUREMENT-1X1-PACED.json']
for o,name in zip(oracle,names,strict=True):
 raw=(a.evidence/name).read_bytes();measurement=json.loads(raw)
 assert measurement['raw_log']==o['raw_log']
 assert hashlib.sha256(o['raw_log'].encode()).hexdigest()==o['log_sha256']==measurement['log_sha256']
 assert set(o['media'])=={'populated','plan','slots_sha256'}
 with tempfile.TemporaryDirectory(dir=a.work) as td:
  media=mod.oracle_media(Path(td),o['shape'],o['media'])
 assert media==measurement['media']
 grade=mod.grade(o['raw_log'],media)
 for field in ('rows','budget_findings','heartbeat','liveness'):assert grade[field]==o[field]==measurement[field],field
 results.append(dict(artifact=name,artifact_sha256=hashlib.sha256(raw).hexdigest(),shape=o['shape'],media=media,log_sha256=o['log_sha256'],budget_findings=o['budget_findings'],custody='PASS'))
print(json.dumps(results,indent=2))
