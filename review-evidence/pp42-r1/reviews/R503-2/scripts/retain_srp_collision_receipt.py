#!/usr/bin/env python3
"""Retain the raw collision-arm log that the published driver overwrites with its unit-arm log."""
import importlib.util,json,os,pathlib,sys
p=pathlib.Path(__file__).resolve().parents[1];root=p/'scratch/source'
os.environ.update(TMPDIR=str(p/'scratch'),PYTHONDONTWRITEBYTECODE='1',REVIEW_LOCKDIR=str(p/'scratch/build-locks'),MAKEFLAGS='-j16',VERILATOR=str(p/'scripts/bounded-verilator.py'))
spec=importlib.util.spec_from_file_location('srp_controls',root/'tb/srp_top/mutants.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rc,log=m.trial(('lv-expiry-masked','srp_top','lvcoll'))
(p/'receipts/srp-controls/lv-expiry-masked-lvcoll.log').write_text(log)
(p/'receipts/srp-controls/lv-expiry-masked-lvcoll.rc').write_text(str(rc)+'\n')
fails=[s for s in log.splitlines() if s.startswith('FAIL:')]
assert rc!=0 and len(fails)==16 and all('SC2:' in s for s in fails)
assert 'checks:' in log and 'CYCLE_BUDGET' not in log
print(json.dumps({'arm':'lv-expiry-masked','suite':'srp_top lvcoll','rc':rc,'failures':len(fails),'verdict':'KILLED'}))
