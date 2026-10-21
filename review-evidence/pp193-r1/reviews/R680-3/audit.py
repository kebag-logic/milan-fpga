#!/usr/bin/env python3
"""Verify published hashes, merge composition, and every tracked byte/mode/index entry."""
import argparse,hashlib,json,os,pathlib,re,subprocess,datetime
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args();a.source=a.source.resolve();a.packet=a.packet.resolve()
HEAD='474346357043218c4e6b728f4ab4b83a2a8579e1';TREE='5ad76c02f6cfd8dbfa0b8d09e34b1cd22acec312'
def git(*args):return subprocess.check_output(['git',*args],cwd=a.source)
def sha(b):return hashlib.sha256(b).hexdigest()
def record(name,lines):(a.packet/name).write_text('\n'.join(lines)+'\n')
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip()==TREE
entries=git('ls-tree','-rz','HEAD').split(b'\0');inventory=[];expected=[];links=[]
for e in entries:
 if not e:continue
 meta,path=e.split(b'\t');mode,kind,oid=meta.decode().split();name=os.fsdecode(path);f=a.source/name
 expected.append((mode,oid,name))
 if mode=='160000':
  links.append((name,oid));assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=f).decode().strip()==oid;continue
 b=os.readlink(f).encode() if mode=='120000' else f.read_bytes()
 actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert actual==oid,name
 actualmode='120000' if f.is_symlink() else ('100755' if f.stat().st_mode&0o111 else '100644')
 assert actualmode==mode,(name,actualmode,mode)
 inventory.append(f'{mode} {oid} {sha(b)} {name}')
index=[]
for e in git('ls-files','--stage','-z').split(b'\0'):
 if not e:continue
 meta,path=e.split(b'\t');mode,oid,stage=meta.decode().split();assert stage=='0';index.append((mode,oid,os.fsdecode(path)))
assert sorted(index)==sorted(expected)
status=git('status','--porcelain=v1','--untracked-files=all','--ignored').decode();assert not status,status
record('tracked-blobs.txt',inventory)
record('source-integrity.txt',[datetime.datetime.now(datetime.timezone.utc).isoformat(),f'HEAD {HEAD}',f'TREE {TREE}',f'MATCH {len(inventory)} tracked blobs: byte content, mode and index',f'MATCH gitlinks {len(links)}: {links}','Clean status including ignored files; no source restoration necessary.'])
rows=[]
for f in ['hdl/aecp/ucode/gen_ucode.py','hdl/aecp/ucode/aecp_commands.json','tb/aecp_cmds/decode.json','tb/pp_top/notify_phases.hpp','tb/pp_top/notify_mutants.py','tb/pp_top/d3_phases.hpp','tb/pp_top/sim_main.cpp']:
 b=(a.source/f).read_bytes();assert git('show','859b537b:'+f)==b;rows.append(f'MATCH main 859b537b {f} sha256={sha(b)}')
for ref in ['65d39b0c','324ac9a7']:
 f='hdl/srp/KL_srp_listener_fsm.sv';assert git('show',ref+':'+f)==(a.source/f).read_bytes();rows.append(f'MATCH listener {ref} -> exact head')
def declaration(b,name):
 text=re.sub(r'/\*.*?\*/|//[^\n]*','',b.decode(),flags=re.S)
 return re.search(r'module '+name+r'\b.*?\);',text,re.S).group()
for f in ['hdl/top/protocol_processor_top.sv','hdl/srp/KL_srp_listener_fsm.sv','hdl/srp/KL_srp_top.sv']:
 for ref in ['21601694','7b424cdf','859b537b']:
  assert declaration(git('show',ref+':'+f),pathlib.Path(f).stem)==declaration((a.source/f).read_bytes(),pathlib.Path(f).stem)
  rows.append(f'MATCH module ports/parameters {ref} -> exact head {f}')
for f in ['hdl/common/pp_pkg.sv','docs/architecture/07_memory_maps.md','docs/architecture/02_interfaces.md']:
 assert git('show','21601694:'+f)==(a.source/f).read_bytes();rows.append(f'MATCH base 21601694 map/interface {f}')
merged=git('merge-tree','--write-tree','324ac9a7','859b537b').decode().strip();assert merged==TREE;rows.append('MATCH clean automatic merge tree '+merged)
s=a.packet/'scratch';uc=s/'audit-main-ucode';uc.mkdir(exist_ok=True)
for f in git('ls-tree','-r','--name-only','859b537b','hdl/aecp/ucode').decode().splitlines():(uc/pathlib.Path(f).name).write_bytes(git('show','859b537b:'+f))
for n,script in [('main',uc/'gen_ucode.py'),('head',a.source/'hdl/aecp/ucode/gen_ucode.py')]:subprocess.run(['python3',str(script),'-o',str(s/(n+'-ucode.hex'))],check=True,stdout=subprocess.DEVNULL)
b=(s/'head-ucode.hex').read_bytes();assert b==(s/'main-ucode.hex').read_bytes();rows.append('MATCH complete generated ROM main/head sha256='+sha(b));record('merge-identity.txt',rows)
m=json.loads((a.packet/'published-manifest-subset.json').read_text());m={x['file']:x for x in m};rows=[]
for f in sorted((a.packet/'published').rglob('*')):
 if not f.is_file():continue
 key='author-r3/receipts/round3/'+str(f.relative_to(a.packet/'published'));h=sha(f.read_bytes());assert h==m[key]['published_sha256'];rows.append(f'MATCH {h} {key}')
record('published-hash-check.txt',rows)
print(f'PASS: {len(inventory)} tracked blobs, {len(links)} gitlinks, clean index/status, merge/ROM/ports, {len(rows)} published hashes')
