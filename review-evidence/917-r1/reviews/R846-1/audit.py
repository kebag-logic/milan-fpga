#!/usr/bin/env python3
"""Check source integrity, generated ABI, and the published receipts. Args: checkout packet."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
repo,packet=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
head='3926c271aaf77420fb9093694be0ab9d511b898d'
base='cec88385ad0a0ec0d61b91597640797766e45010'
def git(*args,cwd=repo):
    return subprocess.check_output(['git','--no-replace-objects',*args],cwd=cwd)
def tree(cwd,ref):
    out={}
    for row in git('ls-tree','-rz',ref,cwd=cwd).split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1); mode,kind,oid=meta.split()
            out[os.fsdecode(name)]=(mode.decode(),kind.decode(),oid.decode())
    return out
def integrity(cwd,ref,label):
    entries=tree(cwd,ref); checked=0
    index={}
    for row in git('ls-files','--stage','-z',cwd=cwd).split(b'\0'):
        if row:
            meta,name=row.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0'
            index[os.fsdecode(name)]=(mode.decode(),oid.decode())
    assert index=={name:(mode,oid) for name,(mode,kind,oid) in entries.items()},label+' index mismatch'
    for name,(mode,kind,oid) in entries.items():
        if kind!='blob':continue
        p=cwd/name;s=p.lstat()
        if mode=='120000':
            assert stat.S_ISLNK(s.st_mode); data=os.fsencode(os.readlink(p))
        else:
            assert stat.S_ISREG(s.st_mode)
            assert bool(s.st_mode & 0o111)==(mode=='100755'),name+' mode'
            data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert actual==oid,name+' bytes'
        checked+=1
    print(label,ref,': index, modes and',checked,'tracked blobs match')
    return entries
assert git('rev-parse','HEAD').decode().strip()==head
assert git('rev-parse','HEAD^{tree}').decode().strip()=='09b50fe085b129c81e7b033b9611a861af4fb9d4'
entries=integrity(repo,head,'source')
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    mode,kind,pin=entries[name];assert mode=='160000' and kind=='commit'
    sub=repo/name;assert git('rev-parse','HEAD',cwd=sub).decode().strip()==pin
    assert (sub/'.git').is_file(),name+' not registered as submodule'
    integrity(sub,pin,name)
gen=packet/'scratch/generator'
shutil.copytree(repo/'sw/mailbox',gen/'sw/mailbox',dirs_exist_ok=True)
outputs=['hdl/milan/mailbox/KL_mbx_pkg.sv','hdl/milan/mailbox/KL_mbx.sv',
         'sw/firmware/ctrl/mbx/mbx_contract.h','docs/reference/MAILBOX_CONTRACT.md']
for name in outputs:
    (gen/name).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(repo/name,gen/name)
subprocess.run([sys.executable,'-B',str(gen/'sw/mailbox/gen_mailbox.py'),'--write'],check=True)
for name in outputs:
    data=(gen/name).read_bytes();assert data==(repo/name).read_bytes()
    if name!=outputs[-1]:assert data==git('show',base+':'+name)
    print('Generated unchanged at source head:',name,hashlib.sha256(data).hexdigest())
import yaml
assert yaml.safe_load(git('show',base+':sw/mailbox/mailbox.yaml'))==yaml.safe_load((repo/'sw/mailbox/mailbox.yaml').read_bytes())
print('Parsed contract identical to base: all rates, fields, register values, rings and version.')
archive=packet/'scratch/review-evidence/917-r1'
manifest=json.loads((archive/'MANIFEST.json').read_text());checked=0
for row in manifest:
    p=archive/row['file']
    if not p.exists():continue
    assert hashlib.sha256(p.read_bytes()).hexdigest()==row['published_sha256'];checked+=1
print('Published archive manifest hashes verified:',checked)
receipts=archive/'author-r1/receipts'
table=(receipts/'workflows/verify-3926c271.md').read_text()
ran=skipped=hash_only=0
large={ln.split()[2]:ln.split()[:2] for ln in (receipts/'workflows/large-logs.sha256').read_text().splitlines()}
for line in table.splitlines():
    if not line.startswith('| '):continue
    parts=[s.strip() for s in line.split('|')[1:-1]]
    if len(parts)!=6:continue
    if parts[4]=='NOT RUN':assert parts[5];skipped+=1
    elif parts[4]=='0':
        name=parts[5].strip('`');log=receipts/'workflows/logs'/name
        if log.exists(): assert head in log.read_text().splitlines()[0]
        else:
            assert name in large
            print('Hash-only log, full text not published:',name,*large[name]);hash_only+=1
        assert log.with_suffix('.rc').read_text().strip()=='0';ran+=1
assert (ran,skipped)==(139,226)
print('Workflow receipt table: 139 rc=0 receipts; 226 stated skip reasons;',ran-hash_only,'source-head log headers and',hash_only,'hash-only logs.')
for p in sorted((receipts/'workflows/logs').glob('*__DONE')): assert p.read_text().strip()=='failed 0'
image_base=(receipts/'images/fixture-images-base.sha256').read_bytes()
assert image_base==(receipts/'images/fixture-images-head.sha256').read_bytes()
assert len(image_base.splitlines())==46
print('Fixture image hash lists: 46/46 identical.')
mutants=(receipts/'mbx/mutants-full-3926c271.log').read_text()
assert 'mbx mutants: 238 of 238 caught' in mutants and '[ESCAPED]' not in mutants
assert len(re.findall(r'^\[ok\] (?!positive control)',mutants,re.M))==238
print('Published mailbox mutation campaign: four controls and 238/238 named catches.')
fw=(receipts/'workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log').read_text()
assert 'mutants: 699 of 699 caught' in fw and 'test_ctrl_firmware: PASS' in fw
print('Published firmware mutation campaign: 699/699 caught; source-head receipt header checked above.')
for p in sorted(receipts.glob('sweep-*/*summary.txt')):
    lines=[ln for ln in p.read_text().splitlines() if ln.startswith('suites:')]
    print(p.relative_to(receipts),':','; '.join(lines))
for p in sorted(receipts.glob('route/1x1/*/signoff.txt')):
    lines=[ln for ln in p.read_text().splitlines() if re.match(r'(Slow|Fast)_',ln)]
    for ln in lines:
        m=re.search(r'WNS ([+\-.0-9]+).*WHS ([+\-.0-9]+)',ln)
        assert float(m[1])>=.030 and float(m[2])>=0
    assert len(lines)==4
    print('All four #818 setup/hold corners PASS:',p.parent.name)
print('Source review only: no manager source bank or current-dev merge candidate executed here.')
