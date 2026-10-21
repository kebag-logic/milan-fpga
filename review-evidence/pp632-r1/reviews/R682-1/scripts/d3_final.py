#!/usr/bin/env python3
"""Run precisely the public twelve controls, reusing this review's completed golden."""
import argparse
import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
p=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser()
ap.add_argument('root',type=Path)
ap.add_argument('--jobs',type=int,required=True)
a=ap.parse_args()
assert 1 <= a.jobs <= 4
root=a.root.resolve()
os.environ.update(TMPDIR=str(p/'scratch'),MAKEFLAGS='-j16',PYTHONDONTWRITEBYTECODE='1')
spec=importlib.util.spec_from_file_location('d3',root/'tb/pp_top/d3_mutants.py')
d3=importlib.util.module_from_spec(spec); spec.loader.exec_module(d3)
out=p/'receipts/d3-final'; out.mkdir(exist_ok=True)
golden_path=p/'receipts/d3/golden-pp_top.log'
if not golden_path.is_file():
    golden_path.parent.mkdir(exist_ok=True)
    control=d3.judge('golden-pp_top',d3.PP_TOP,(),(),(root,golden_path.parent,str(p/'scripts/limited-simulator.py')))
    assert control['verdict']=='PASS',control
    (p/'receipts/d3-campaign.log').write_text(json.dumps({'mutant':'golden-pp_top','verdict':'PASS'})+'\n')
golden=golden_path.read_text()
assert d3.TALLY.search(golden) and not re.search(r'^FAIL:',golden,re.M)
assert re.search(r'^D3: \d+ checks, 0 failures$',golden,re.M)
assert '"mutant": "golden-pp_top", "verdict": "PASS"' in (p/'receipts/d3-campaign.log').read_text()
names=['latch_ignores_program','taint_ignored','clear_wins_same_edge','clear_by_group','clear_by_index','identify_is_a_change','unchanged_compare_ignores_validity','no_backoff_d3','fourth_attempt','alarm_forgiven_by_success','backoff_derivation','backoff_holds_dispatch']
known={m.name:m for m in d3.MUTANTS}
work=(root,out,str(p/'scripts/limited-simulator.py'))
def execute(name):
    m=known[name]
    r=d3.judge(m.name,m.suite,m.edits,m.checks,work)
    print(json.dumps(r),flush=True)
    return r
with concurrent.futures.ThreadPoolExecutor(a.jobs) as pool:
    results=list(pool.map(execute,names))
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
expected=json.loads((p/'receipts/public/receipts/round3/processor_51f88c7e/campaigns/d3.results.json').read_text())
counts={r['mutant']:len(r['failing_checks']) for r in expected}
ok=all(r['verdict']=='KILLED' and len(r['failing_checks'])==counts[r['mutant']] for r in results)
print('D3 required controls:',len(results),'all killed at the published failure counts:',ok,flush=True)
(p/'receipts/d3-final.rc').write_text(str(0 if ok else 1)+'\n')
raise SystemExit(0 if ok else 1)
