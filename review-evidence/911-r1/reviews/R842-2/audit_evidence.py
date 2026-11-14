#!/usr/bin/env python3
"""Usage: audit_evidence.py CHECKOUT PACKET. Read the fixed public archive.

Verifies published-byte hashes, gate censuses, update receipts, input lists,
and raw timing/CDC/clock/pin comparisons. Does not execute archived scripts.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, packet = map(Path, sys.argv[1:3])
archive = '489e06bd1c6adbf19eb36d5fbc7ca4e47944b18d'
prefix = 'review-evidence/911-r1/'
def read(name):
    return subprocess.check_output(['git', 'show', archive + ':' + prefix + name], cwd=root)
manifest = json.loads(read('MANIFEST.json'))
counts = Counter()
for row in manifest:
    if row['file'].startswith(('author-r1/', 'author-r2/')):
        assert hashlib.sha256(read(row['file'])).hexdigest() == row['published_sha256'], row['file']
        counts[row['file'].split('/')[0]] += 1
print('Archive', archive, 'published-byte SHA256 checks:', dict(counts))
print('Manifest verification proves hash integrity, not an author signature.')
def r(name):
    return read('author-r2/receipts/' + name).decode()
rows = [line.split('|')[1:-1] for line in r('gates/workflow-steps.md').splitlines()[2:] if line.startswith('|')]
states = Counter(row[4].strip() for row in rows)
assert states == {'0':150, 'NOT RUN':522}, states
assert all(row[5].strip() for row in rows)
assert len({tuple(cell.strip() for cell in row[:3]) for row in rows}) == len(rows)
print('Workflow rows:',dict(states),'; all reasons/log references present; unique workflow/job/step keys')
lane = re.findall(r'(\S+) rc=(\d+)', r('gates/lane-gates.txt'))
assert len(lane)==27 and all(rc=='0' for _,rc in lane)
assert '8e523a2b17faf17c4564e5af155b73f95dc2a0a5 (clean clone)' in r('gates/lane-gates.txt')
print('27 lane receipts rc=0 at exact head; these are author execution receipts.')
for label in ['02-update-200t-D-to-R','03-update-200t-R-to-D']:
    assert r('guide-run/'+label+'.rc').strip()=='0'
    log=r('guide-run/'+label+'.log')
    assert log.index('write+verify aem @ 0xa00000') < log.index('write+verify bitstream @ 0x000000')
    data=r('guide-run/'+label[3:]+'.flash.txt')
    assert data.count('True')==2 and '9730652' in data and '0xa00000' in data
    print(label, 'rc=0; AEM before bitstream; both readbacks match')
for label, rc in [('05-update-ax7101-old-target-refused','2'),('06-regenerate-layout-from-soch','0'),('07-update-ax7101-regenerated-target','0')]:
    assert r('guide-run/'+label+'.rc').strip()==rc
    print(label,'rc='+rc)
for recipe in ['ax7101','ax7a200t']:
    before=r('identity/'+recipe+'-1e604e1b.inputs.sha256')
    after=r('identity/'+recipe+'-8e523a2b.inputs.sha256')
    assert before==after and len(after.splitlines())==150
    other=recipe+('-b7d69295.inputs.sha256' if recipe=='ax7101' else '-8e523a2b.buildC-inputs.sha256')
    assert after==r('identity/'+other)
    found=0; absent=[]
    for line in after.splitlines():
        sha, name=line.split('  ',1)
        if name.startswith('<clone>/'):
            f=root/name[len('<clone>/'):]
            if f.is_file():
                assert hashlib.sha256(f.read_bytes()).hexdigest()==sha, name
                found+=1
            else: absent.append(name)
        else: absent.append(name)
    print(recipe, '150 input entries identical; list SHA256',hashlib.sha256(after.encode()).hexdigest())
    print('Current checkout hash matches:',found,'; generated/SDK entries unavailable here:',len(absent))
    for name in absent: print('  unavailable:',name)
for corner in ['Slow','Fast']:
    for temp in [0,85]:
        name=f'vivado-buildC-route/buildC_route_{corner}_{temp}C_timing_summary.rpt'
        text=r(name)
        lines=text.splitlines()
        i=next(i for i,l in enumerate(lines) if 'WNS(ns)' in l)
        vals=lines[i+2].split()
        expected=('0.174','0.102') if corner=='Slow' else ('1.633','0.036')
        assert (vals[0],vals[4])==expected and vals[1]==vals[5]=='0.000'
        assert 'Device       : 7a200t-fbg484' in text
        assert re.search(r'^  '+corner+r'\s+Yes\s+Yes',text,re.M)
        assert 'unconstrained_internal_endpoints (0)' in text
        print(corner,temp,'C: WNS',vals[0],'TNS',vals[1],'WHS',vals[4],'THS',vals[5])
def cdc(text):
    return {m[1]:(m[2],int(m[3])) for m in re.finditer(r'^(CDC-\d+)\s+(\w+)\s+(\d+)\s+',text,re.M)}
ca=cdc(r('ax7101-release/alinx_ax7101_signoff_cdc.rpt'))
cb=cdc(r('buildC-release/alinx_ax7101_signoff_cdc.rpt'))
cc=cdc(r('vivado-buildC-route/buildC_route_cdc_details.rpt'))
assert ca==cb==cc and len(ca)==8
print('Raw CDC categories agree across baseline, image signoff, reread checkpoint:',ca)
def clocks(text):
    lines=text.splitlines()
    i=next(i for i,l in enumerate(lines) if l.startswith('---') and len(re.findall('-+',l))==16)
    spans=[m.span() for m in re.finditer('-+',lines[i])]
    result={}
    for line in lines[i+1:]:
        if not line.strip(): break
        cols=[line[a:b].strip() for a,b in spans]
        result[tuple(cols[:2])]=tuple(cols[j] for j in [6,12,14,15])
    return result
ca=clocks(r('ax7101-release/alinx_ax7101_signoff_clock_interaction.rpt'))
cb=clocks(r('buildC-release/alinx_ax7101_signoff_clock_interaction.rpt'))
assert ca==cb and len(ca)==16
print('16 clock pairs agree in endpoints, classification and constraint; slack is not compared.')
def pins(text):
    result={}
    for line in text.splitlines():
        if not line.startswith('| ') or 'Pin Number' in line: continue
        cells=[x.strip() for x in line.strip('|').split('|')]
        if len(cells)>7 and cells[1]: result[cells[0]]=tuple(cells[j] for j in [1,3,4,5,6])
    return result
pa=pins(r('ax7101-release/alinx_ax7101_io.rpt'))
pb=pins(r('buildC-release/alinx_ax7101_io.rpt'))
assert pa==pb and len(pa)==113
print('113 used pins agree in signal, pin name, use, I/O standard and bank.')
print('PASS: public evidence audit. Binary/checkpoint and full job logs are not independently reproduced.')
