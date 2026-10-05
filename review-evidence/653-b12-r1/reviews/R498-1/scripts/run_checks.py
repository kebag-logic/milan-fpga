#!/usr/bin/env python3
"""Foreground bounded checks, with independent jobs joined before exit.

Usage: python3 run_checks.py EVIDENCE_ROOT REPOSITORY PACKET_DIRECTORY
"""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

evidence,repo,packet=map(Path,sys.argv[1:])
receipts=packet/'receipts';receipts.mkdir(exist_ok=True)
scripts=packet/'scripts'
jobs={
    'evidence-audit':[sys.executable,str(scripts/'audit_evidence.py'),str(evidence),str(repo),str(receipts)],
    'offline-controls':[sys.executable,str(scripts/'offline_controls.py'),str(evidence),str(packet/'scratch/controls')],
    'restore-controls':[sys.executable,str(scripts/'restore_controls.py'),str(evidence),str(packet/'scratch/restore-controls')],
    'integrity':[sys.executable,str(scripts/'check_integrity.py'),str(repo)],
    'diff-check':['git','-C',str(repo),'diff','--check','fa450d301805881ad713b67521477bf042ddadfd..bef8dd7036f711bf286929fa4cba6bf724c7118d'],
}


def run(item):
    name,cmd=item
    result=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
    (receipts/(name+'.log')).write_text(result.stdout+result.stderr)
    (receipts/(name+'.rc')).write_text(str(result.returncode)+'\n')
    return name,result.returncode


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=dict(pool.map(run,jobs.items()))
(receipts/'check-results.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
for name,rc in results.items(): print(name+': rc '+str(rc))
sys.exit(0 if not any(results.values()) else 1)
