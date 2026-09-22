import argparse, hashlib, json, os, stat, subprocess
from pathlib import Path
root=Path('$VALIDATION_STORAGE/reviews/r243-423-r1'); output=Path(__file__).resolve().parent
HEAD='df53dfa116b34816db0193230ad9833e67bf46dd'; TREE='fb7bbe66e6326d9d55b4ad13170446dff12a133a'
required=['protocol-processor','gptp-processor','third_party/verilog-axis']
def git(repo,*args):
 return subprocess.run(['rtk','proxy','git','--no-replace-objects','-C',str(repo),*args],capture_output=True,check=True).stdout

def verify(repo,expected):
 head=git(repo,'rev-parse','HEAD').strip().decode(); assert head==expected,(repo,head,expected)
 tree=git(repo,'rev-parse','HEAD^{tree}').strip().decode()
 index=git(repo,'ls-files','--stage','-z');entries={}
 for record in index.split(b'\0'):
  if not record:continue
  meta,name=record.split(b'\t',1);mode,oid,stage=meta.split();assert stage==b'0';assert name not in entries;entries[name]=(mode,oid)
 rows=[];tracked={};links={}
 for record in git(repo,'ls-tree','-r','-z',expected).split(b'\0'):
  if not record:continue
  meta,name=record.split(b'\t',1);mode,kind,oid=meta.split();tracked[name]=(mode,oid)
  assert entries.get(name)==(mode,oid),(str(repo),name,'index differs')
  if mode==b'160000':links[os.fsdecode(name)]=oid.decode();continue
  path=repo/os.fsdecode(name);s=path.lstat()
  if kind!=b'blob':raise AssertionError(('unexpected kind',kind))
  if mode==b'120000':assert stat.S_ISLNK(s.st_mode);data=os.fsencode(os.readlink(path))
  else:
   assert stat.S_ISREG(s.st_mode);assert bool(s.st_mode&0o111)==(mode==b'100755');data=path.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert actual==oid.decode(),(str(repo),name,'blob differs')
  rows.append(dict(path=os.fsdecode(name),mode=mode.decode(),kind=kind.decode(),oid=actual,bytes=len(data)))
 assert entries==tracked,'extra or missing index entry'
 return dict(head=head,tree=tree,index_sha256=hashlib.sha256(index).hexdigest(),files=rows,gitlinks=links,status=git(repo,'status','--porcelain=v2','--untracked-files=normal').decode())
report={'root':verify(root,HEAD),'required_submodules':{}}
assert report['root']['tree']==TREE
for path in required:
 repo=root/path;assert repo.is_dir() and not repo.is_symlink();assert (repo/'.git').is_file()
 assert git(repo,'rev-parse','--show-superproject-working-tree').strip()==os.fsencode(root)
 report['required_submodules'][path]=verify(repo,report['root']['gitlinks'][path])
assert not report['root']['status'];assert all(not s['status'] for s in report['required_submodules'].values())
name=argparse.ArgumentParser();name.add_argument('label');args=name.parse_args()
(output/(args.label+'-integrity-data.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'head':HEAD,'tree':TREE,'root_files':len(report['root']['files']), 'root_gitlinks':report['root']['gitlinks'],'submodule_files':{k:len(v['files']) for k,v in report['required_submodules'].items()},'status':'all index/blob/kind/mode and registered required pins match'},indent=2))
