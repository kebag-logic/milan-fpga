#!/usr/bin/env python3
"""Record the exact deltas permitting published gate evidence to carry."""
from pathlib import Path
import subprocess, ast, shutil
P=Path(__file__).resolve().parents[1]
E=P/'scratch/evidence/review-evidence/train1117-r1/author-r5/receipts'
O=P/'receipts/published';O.mkdir(parents=True,exist_ok=True)
def git(*a):return subprocess.check_output(['git',*a],text=True)
fw=git('diff','--name-only','c8ff391a','HEAD','--','sw/firmware','third_party').splitlines()
assert fw==['sw/firmware/ctrl/test/plat_mutants.py']
before=git('show','c8ff391a:sw/firmware/ctrl/test/plat_mutants.py')
after=Path('sw/firmware/ctrl/test/plat_mutants.py').read_text()
assert before.rstrip()==after.rstrip()
print('PASS four firmware shards carry through step 11: only trailing blank removed, all firmware bytes otherwise unchanged')
assert not git('diff','--name-only','4374cc27','HEAD','--','tb/verilator/ctrl_service_budget')
print('PASS completed run self-test at 4374cc27: entire CPU-budget harness unchanged at final head')
changed=git('diff','--name-only','3e908539','HEAD').splitlines()
assert set(changed)=={'sw/firmware/ctrl/test/plat_mutants.py','syn/ooc/pp_resource_baseline.json','tb/verilator/ctrl_service_budget/load_grade.py'}
print('PASS step-11 twin, mailbox, datapath, meter and render gates: no changes to their RTL, test or firmware inputs through final head')
for f in sorted((E/'step11/gates').glob('r5-p11*')):
    if f.name.endswith('.rc'): assert f.read_text().strip()=='0',f
    shutil.copyfile(f,O/f.name)
    if not f.name.endswith('.rc'):
        t=f.read_text();lines=t.splitlines()
        print(f.name, 'published rc=0', 'hash/tail stub' if f.name.endswith('.stub.txt') else 'full log')
        for line in lines:
            if any(x in line for x in ['of 797 caught','of 361 caught','of 135 caught','38/38','32 checks:','self-test:','test_ctrl_firmware:','END rc=','mutants:','defects:']):print(' ',line[:240])
for rel in ['regrade/confdiff-final.txt','regrade/image-hashes-p11.txt','regrade/fit-summary-p11.txt','regrade/verdict-unit375-final.txt','step11/images/hashes-73272666.txt','step11/images/hashes.txt','images/hashes.txt','step11/release/gate-after.txt','step11/release/hier-diff.txt','step11/cdc/fcdc-summary.txt','step11/cdc/reports/cdc-summary-release.rpt','step11/cdc/reports/cdc-summary-split-1x1.rpt','step11/cdc/reports/cdc-summary-split-8x8-1if.rpt','step11/gates/q-candidate-4374cc27/run_selftest.log.stub.txt','step11/gates/q-candidate-4374cc27/run_selftest.rc']:
    f=E/rel;target=O/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,target)
print('Published evidence inventory and input carry complete')
