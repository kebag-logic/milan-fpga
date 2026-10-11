#!/usr/bin/env python3
"""Audit round-five unchanged mechanisms and the published capture inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('root', type=Path)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
path = 'sw/firmware/milan_baremetal/milan_baremetal.c'
old = subprocess.check_output(['git','-C',str(a.root),'show','7bc7ceca:'+path],text=True)
new = (a.root/path).read_text()
for name in ('nvm_restage','nvm_pick_slot','nvm_go_live','nvm_boot','nvm_fill_window',
             'nvm_commit','nvm_capture','nvm_service'):
    # Locate definitions rather than earlier calls or comments.
    import re
    pattern = r'\nstatic [^\n]+\b'+name+r'\([^;]*?\n\{'
    def extract(text):
        m = re.search(pattern,text)
        assert m, name
        start=m.start();pos=m.end();level=1
        while level:
            level += (text[pos]=='{')-(text[pos]=='}');pos+=1
        return text[start:pos]
    assert extract(old)==extract(new),name
    print('UNCHANGED round 5:',name)
oldjudge = old[old.index('static struct nvm_read nvm_judge_slot'):old.index('static int nvm_restage')]
newjudge = new[new.index('static struct nvm_read nvm_judge_slot'):new.index('static int nvm_restage')]
assert oldjudge.replace('{VD_LEN, 0u, 0u, 0u}', '{VD_LEN, 0u, 0u, 0u, 0u}') == newjudge
print('UNCHANGED judgement control flow; initializer adds tail field')
j=json.loads((a.root/'tb/verilator/nvm_capture_cpu/measurements.json').read_text())
digest=hashlib.sha256((a.root/path).read_bytes()).hexdigest()
assert digest==j['product_firmware_sha256']
assert subprocess.check_output(['git','-C',str(a.root),'show',j['base']+':'+path])==(a.root/path).read_bytes()
print('Capture measured base',j['base'],'same firmware as review head',digest)
for arm in j['measurements']:
    files=list((packet/'public/author-r5').glob('*measurement.json'))
    assert any(all(arm.get(k)==v for k,v in json.loads(f.read_text()).items()) for f in files)
    assert len(arm['rows'])==16 and all(r['ok']==1 and r['mismatches']==0 for r in arm['rows'])
    ms=max(r['sys_cycles']/arm['sys_hz']*1000 for r in arm['rows'])
    assert abs(ms-arm['maximum_ms'])<1e-10
    print(arm['shape'],arm['cpu_hz'],arm['traffic'],len(arm['rows']),'max_ms',round(ms,5))
print('PASS all fields of six raw public capture arms equal committed receipt; 96 clean captures')
sys.dont_write_bytecode=True
sys.path.insert(0,str(a.root/'sw/firmware/nvm_hosttest'))
import read_fault_cases as c
for body in (1686,6646):
    cases=c.fault_cases(body)
    assert len(cases)==3422
    assert sum(x.restart for x in cases)==1647
    categories=0
    for older,faulted,manners,seqs in c.GROUPS:
        for valid in 'ab':
            slot=c.faulted_slot(faulted,valid)
            for restart in (False,True):
                for manner in manners:
                    if manner not in c.SEALED:
                        continue
                    off=c.SEALED[manner][0] or body
                    found={x.seq for x in cases if x.older==older and x.valid==valid and
                           x.restart==restart and x.fault[0]=='--read-sealed' and
                           x.fault[1].startswith(f'{slot}:{off}:') and
                           c.expect(x).judgement['ab'.index(slot)]=='ffc'}
                    assert found==set(seqs)
                    categories+=1
    print(f'PASS body offset {body}: 3422 cases, 1775 cold/1647 restart; all sequences in {categories} sealed categories')
