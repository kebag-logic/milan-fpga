#!/usr/bin/env python3
"""Check published receipt hashes, mutation assertions, parent patch and identities."""
import argparse, concurrent.futures, hashlib, json, pathlib, re, subprocess, sys, urllib.request
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
pub=root/'public'; evidence=pub/'author-r2/receipts'
out=[]
def say(s): out.append(s);print(s,flush=True)
manifest=json.loads((pub/'MANIFEST.json').read_text()); n=0
for row in manifest:
    f=pub/row['file']
    if f.is_file():
        assert hashlib.sha256(f.read_bytes()).hexdigest()==row['published_sha256'],str(f)
        n+=1
say(f'Published hashes verified: {n}')
sys.dont_write_bytecode=True
sys.path.insert(0,str(a.repo/'tb/verilator/engine'))
from port_mutants import PORT_MUTATIONS
coverage=json.loads((evidence/'coverage/coverage.json').read_text())
controls={x['control']:x for x in coverage['controls']}
for name,filename,old,new,checks in PORT_MUTATIONS:
    c=controls[name];assert c['rc']!=0 and c['named_verdict']=='caught'
    log=(evidence/'coverage'/f"{c['k']:02}.log").read_text()
    for check in checks.split(' | '): assert any(line.startswith('FAIL '+check+' ') for line in log.splitlines()),(name,check)
    say(f'Named mutation failures verified: {name}')
checks=(evidence/'coverage/checks94.txt').read_text().splitlines()
allfails='\n'.join(f.read_text() for f in (evidence/'coverage').glob('[0-9][0-9].log'))
for check in checks: assert 'FAIL '+check+' ' in allfails,check
say(f'Covered issue checks: {len(checks)}; port controls: {len(PORT_MUTATIONS)}')
for d in ['repo-base-fast','repo-head-fast','repo-base-arm','repo-head-arm','parent-base-A','parent-base-B','parent-head-A','parent-head-B','parent-head-extra']:
    j=json.loads((evidence/d/'results.json').read_text())
    assert all(x['exit_code']==0 for x in j['results']),d
    say(f'{d}: head={j["head"]}; {len(j["results"])} commands rc 0')
for d,total in [('repo-base-arm',113),('repo-head-arm',136)]:
    assert f'{total} checks: {total} PASS, 0 FAIL' in (evidence/d/'01.log').read_text()
    say(f'{d}: {total}/{total}')
for f in ['12.log','13.log']:
    assert '205 checks: 205 PASS, 0 FAIL' in (evidence/'parent-head-A'/f).read_text()
    say('parent-head-A/'+f+': 205/205')
assert (evidence/'parent-head-B/base-pB-lines.txt').read_bytes()==(evidence/'parent-head-B/head-pB-lines.txt').read_bytes()
say('Parent physical-simulation event/verdict lines identical to base')
patch=(pub/'author-r2/milan-fpga-companion.patch').read_text()
parts=patch.split('diff --git ')[1:]
tree=root/'scratch/parent-subset';tree.mkdir(parents=True,exist_ok=True)
base='e06ade312a80eb578579365134ab797cda90622b'
files=[]
for part in parts:
    path=part.splitlines()[0].split(' b/')[1]
    ids=re.search(r'index ([0-9a-f]+)\.\.([0-9a-f]+) (\d+)',part)
    if ids[3]=='160000':
        assert path=='gptp-processor' and '+Subproject commit 409c3075a6c5525d283de5a93584ad87a4528137' in part
        say('Companion donor gitlink: exact reviewed head')
        continue
    files.append((path,ids[1],ids[2]))
def fetch(entry):
    path,before,after=entry;f=tree/path;f.parent.mkdir(parents=True,exist_ok=True)
    data=urllib.request.urlopen(f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{base}/{path}',timeout=60).read();f.write_bytes(data)
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob.startswith(before),path
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(fetch,files))
localpatch=tree/'companion.patch';localpatch.write_text(patch)
subprocess.run(['git','apply','--exclude=gptp-processor',str(localpatch)],cwd=tree,check=True)
for path,before,after in files:
    data=(tree/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob.startswith(after),path
    say(f'Companion verified preimage and postimage: {path} {before} -> {after}')
for name in ['CONTRIBUTING.md','REQUIREMENTS.md']:
    data=urllib.request.urlopen(f'https://raw.githubusercontent.com/kebag-logic/milan-fpga/{base}/{name}',timeout=60).read()
    f=pub/'parent'/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
(root/'evidence-check.log').write_text('\n'.join(out)+'\n')
