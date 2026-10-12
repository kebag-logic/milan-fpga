#!/usr/bin/env python3
"""Prove the merge path set, merged builder bytes, and raw checkout/index/gitlinks."""
import hashlib,json,os,pathlib,stat,subprocess,sys,tempfile
ROOT=pathlib.Path(sys.argv[1]).resolve()
PACKET=pathlib.Path(__file__).resolve().parents[1]
BASE='e8454e2751d05b02ee8e5a571857589ab358ab86'
PREV='c7d0ad63510cf1aaee41ef440675d110ad2730d7'
DEV='c6bd08c6f52632c6d33d834ce842ac3cf63f29cc'
MERGE='44416838b90c40536a2104ab1f2bd4ff02268bec'
HEAD='9b32002cc0c3aafae9e864af7b4f08c1089a188a'
ENV=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1')
def git(*args,root=ROOT):return subprocess.check_output(['git','--no-replace-objects',*args],cwd=root,env=ENV)
def tree(ref,root=ROOT):
 return {p:tuple(h.split()) for entry in git('ls-tree','-rz',ref,root=root).split(b'\0') if entry for h,p in [entry.split(b'\t',1)]}
def paths(a,b):return {p for p in a.keys()|b.keys() if a.get(p)!=b.get(p)}
def verify(root,ref):
 entries=tree(ref,root)
 idx={}
 for rec in git('ls-files','--stage','-z',root=root).split(b'\0'):
  if not rec:continue
  h,p=rec.split(b'\t',1);mode,oid,stage=h.split();assert stage==b'0',p
  assert p not in idx,p
  idx[p]=(mode,oid)
 assert idx=={p:(v[0],v[2]) for p,v in entries.items()},'index differs from commit'
 count=0
 for raw,(mode,kind,oid) in entries.items():
  if kind!=b'blob':continue
  f=root/os.fsdecode(raw);s=f.lstat()
  if mode==b'120000':assert stat.S_ISLNK(s.st_mode),raw;content=os.fsencode(os.readlink(f))
  else:
   assert stat.S_ISREG(s.st_mode),raw
   assert bool(s.st_mode&0o111)==(mode==b'100755'),raw
   content=f.read_bytes()
  got=hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest().encode()
  assert got==oid,raw
  count+=1
 return count
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip()=='7ac62ffdcfcf060c763d5dd7d63ada7fdbeca40f'
assert git('show','-s','--format=%P',MERGE).decode().split()==[PREV,DEV]
assert git('show','-s','--format=%P',HEAD).decode().split()==[MERGE]
b,p,d,h,m=map(tree,(BASE,PREV,DEV,HEAD,MERGE))
own=paths(b,p);net=paths(d,h)
assert own==net
print('Own branch path set equals HEAD minus DEV:',len(net))
for path in sorted(net):print(os.fsdecode(path),'unchanged from round 6' if p[path]==h[path] else 'merged/refreshed')
exceptions={b'docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md',b'tb/verilator/nvm_capture_cpu/measurements.json',b'sw/builder/test_builder.py'}
assert {x for x in net if p[x]!=h[x]}==exceptions
assert paths(m,h)==exceptions-{b'sw/builder/test_builder.py'}
with tempfile.TemporaryDirectory(dir=PACKET/'scratch') as t:
 files=[]
 for n,ref in enumerate((PREV,BASE,DEV)):
  f=pathlib.Path(t)/str(n);f.write_bytes(git('show',ref+':sw/builder/test_builder.py'));files.append(str(f))
 out=subprocess.run(['git','merge-file','-p',*files],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=ENV)
 assert out.returncode==0 and out.stdout==git('show',HEAD+':sw/builder/test_builder.py')
print('Builder = exact clean three-way merge of both parent changes')
for name in ['hdl','scripts','protocol-processor','gptp-processor','third_party']:
 assert not [x for x in net if x==name.encode() or x.startswith(name.encode()+b'/')]
print('RTL, scripts, and all gitlinks equal named dev')
print('Parent tracked blobs/modes and exact index verified:',verify(ROOT,HEAD))
for name in ['protocol-processor','gptp-processor','third_party/verilog-axis']:
 pin=h[name.encode()][2].decode();sub=ROOT/name
 assert git('rev-parse','HEAD',root=sub).decode().strip()==pin
 assert (sub/'.git').is_file()
 assert pathlib.Path(git('rev-parse','--show-superproject-working-tree',root=sub).decode().strip()).resolve()==ROOT
 print('Required submodule',name,pin,'tracked blobs/modes and exact index verified:',verify(sub,pin))
print('Raw tracked restoration: PASS')
