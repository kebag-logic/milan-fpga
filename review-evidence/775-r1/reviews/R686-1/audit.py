#!/usr/bin/env python3
"""Read-only exact-head, index, submodule and published-receipt audit.
Usage: python3 audit.py CHECKOUT PACKET
The published evidence commit must already be fetched into CHECKOUT.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tarfile

root, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
head = 'c7e87c8c87494f3444000b46954648ba1a94dcb8'
evidence = '976fb2d33b358f41bbff082a69f76fba6b749a77'
def git(*args, cwd=root):
    return subprocess.check_output(['git', *args], cwd=cwd)
def entries(cwd):
    rows = {}
    for row in git('ls-tree', '-rz', '--full-tree', 'HEAD', cwd=cwd).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, oid = meta.split()
            rows[os.fsdecode(name)] = (mode.decode(), kind.decode(), oid.decode())
    return rows
def audit_tree(cwd):
    rows = entries(cwd)
    index = {}
    for row in git('ls-files', '--stage', '-z', cwd=cwd).split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, oid, stage = meta.split()
            assert stage == b'0'
            index[os.fsdecode(name)] = (mode.decode(), oid.decode())
    assert index == {n:(r[0],r[2]) for n,r in rows.items()}, 'index differs from HEAD'
    count = 0
    for name, (mode,kind,oid) in rows.items():
        if kind != 'blob':
            continue
        path = cwd / name
        info = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(info.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode), name
            actual_mode = '100755' if info.st_mode & 0o111 else '100644'
            assert mode == actual_mode, name
            data = path.read_bytes()
        measured = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        assert measured == oid, name
        count += 1
    return {'head':git('rev-parse','HEAD',cwd=cwd).decode().strip(), 'blobs_checked':count, 'index':'exact', 'bytes_modes':'exact'}
assert git('rev-parse','HEAD').decode().strip() == head
result = {'source':audit_tree(root), 'tree':git('rev-parse','HEAD^{tree}').decode().strip(), 'dependencies':{}}
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/tsn-c-stack','third_party/lwSRP']:
    pin = entries(root)[name][2]
    record = audit_tree(root/name)
    assert record['head'] == pin, name
    assert (root/name/'.git').is_file(), 'requires initialized submodule metadata'
    result['dependencies'][name] = record
result['git_status'] = git('status','--porcelain=v1').decode()
assert not result['git_status']
(packet/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')

evroot = packet/'scratch/review-evidence/775-r1'
if not (evroot/'MANIFEST.json').exists():
    archive = git('archive', evidence, 'review-evidence/775-r1/author/receipts', 'review-evidence/775-r1/MANIFEST.json')
    (packet/'scratch').mkdir(exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        bundle.extractall(packet/'scratch', filter='data')
manifest = json.loads((evroot/'MANIFEST.json').read_text())
verified = []
for entry in manifest:
    if not entry['file'].startswith('author/receipts/'):
        continue
    p = evroot/entry['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == entry['published_sha256'], entry['file']
    verified.append(entry['file'])
r = evroot/'author/receipts'
suite_names=[]; checks=0; shards=[]
for n in range(4):
    receipt=json.loads((r/f'sweep-c7e87c8c/shard-{n}/spec/results.json').read_text())
    assert receipt['head']==head and receipt['results'][0]['exit_code']==0
    log=(r/f'sweep-c7e87c8c/shard-{n}/spec/01.log').read_text()
    names=re.findall(r'^PASS\s+(\S+)$',log,re.M)
    tally=int(re.search(r'checks: (\d+)',log)[1])
    checks+=tally;suite_names+=names;shards.append({'shard':n,'suites':len(names),'checks':tally,'rc':0})
assert len(suite_names)==len(set(suite_names))==64 and checks==2189615
docs=json.loads((r/'docs-c7e87c8c/receipts.json').read_text())
final={(s['job'],s['id']):s for s in docs['steps'] if s.get('rc') is not None}
initial_failed=[str(k) for k,v in final.items() if v['rc']!=0]
for n in range(2):
    rerun=json.loads((r/f'docs-builder{n}-c7e87c8c/receipts.json').read_text())
    assert rerun['head']==rerun['head_after']==head
    for step in rerun['steps']:final[(step['job'],step['id'])]=step
assert len(final)==42 and all(v['rc']==0 and v['make']=='GNU Make 4.3' for v in final.values())
audit={'evidence_commit':evidence,'verified_published_receipts':len(verified),'shards':shards,'suites':64,'checks':checks,'docs_initial_failed':initial_failed,'docs_final_executed':len(final),'docs_final_rcs':sorted(set(v['rc'] for v in final.values())),'docs_skips':['candidate host runner contract','strip git metadata step'],'note':'Published hashes account for path redaction; original hash fields are not hashes of redacted bytes.'}
(packet/'evidence_audit.json').write_text(json.dumps(audit,indent=2)+'\n')

hits=[]
for name,(mode,kind,oid) in entries(root).items():
    if kind!='blob' or Path(name).suffix not in ('.sv','.v','.py','.tcl'):
        continue
    text=(root/name).read_text(errors='replace')
    text=re.sub(r'/\*.*?\*/',lambda m:'\n'*m[0].count('\n'),text,flags=re.S)
    text=re.sub(r'//[^\n]*','',text)
    for i,line in enumerate(text.splitlines(),1):
        if re.search(r'\bKL_avtp_rx_monitor\b\s*#\s*\(',line) and not re.search(r'\bmodule\s+KL_avtp_rx_monitor',line):
            hits.append({'path':name,'line':i,'text':line.strip()})
assert all(x['path'].startswith('tb/') for x in hits)
(packet/'flat_instantiations.json').write_text(json.dumps(hits,indent=2)+'\n')
print(json.dumps({'integrity':'PASS','evidence':audit,'flat_instantiations':hits},indent=2))
