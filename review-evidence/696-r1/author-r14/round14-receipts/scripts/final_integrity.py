import hashlib,json,subprocess
from pathlib import Path
w=Path(__file__).resolve().parent;repo=w/'candidate';lane=Path('$LANE')
head='e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd'
parents=['313616d1a18549d41907db389d378f0beb9bc543','d40e4e9827be2516f8f34b9d65f0a483fff2194c']
def git(root,*args):
 if root not in (lane,repo) and args!=('rev-parse','--show-toplevel'):
  actual=Path(subprocess.check_output(['git','-C',str(root),'rev-parse','--show-toplevel'],text=True).strip());assert actual==root,(actual,root)
 return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
for name in ['resource-bank','accepted-validation','record-measurements','static-bank']:
 assert (w/(name+'.rc')).read_text().strip()=='0',name
assert git(lane,'remote','get-url','origin')=='https://github.com/kebag-logic/milan-fpga.git'
assert git(lane,'branch','--show-current')=='696-maap-annexb'
assert git(lane,'rev-parse','HEAD')==head==git(repo,'rev-parse','HEAD')
assert git(lane,'show','-s','--format=%P','HEAD').split()==parents
assert git(lane,'log','-1','--format=%B')=='Merge shared stack candidate into MAAP Annex B lane'
submodules=[]
for root in [lane,repo]:
 for sub in ['protocol-processor','gptp-processor','third_party/verilog-axis','third_party/lwSRP','third_party/tsn-c-stack']:
  p=root/sub;assert Path(git(p,'rev-parse','--show-toplevel'))==p
  submodules.append(dict(root=str(p),head=git(p,'rev-parse','HEAD'),status=git(p,'status','--porcelain')))
assert all(not row['status'] for row in submodules)
checked=0
for group in json.loads((w/'source-inputs.json').read_text()):
 for entry in group['files']:
  p=Path(entry['path']);assert sha(p)==entry['sha256'],p;checked+=1
proof=json.loads((w/'merge-provenance.json').read_text())
for entry in proof['protected_blobs_equal_first_parent']:
 path=entry['path']
 assert git(lane,'rev-parse',head+':'+path)==git(lane,'rev-parse',parents[0]+':'+path),path
large=[]
for p in (w/'shipping-candidate').rglob('*'):
 if p.is_file() and p.suffix in ('.dcp','.bit','.bin','.elf'):
  large.append(dict(artifact=p.relative_to(w).as_posix(),bytes=p.stat().st_size,sha256=sha(p),disposition='retained in scratch; no binary copied to output'))
(w/'large-artifacts.json').write_text(json.dumps(large,indent=2)+'\n')
links=[]
for rel,target in [('sw/builder/out',w/'shipping-candidate/builder'),('configs/generated/ltn_rom.hex',w/'shipping-candidate/roms/ltn_rom.hex'),('configs/generated/ucode.hex',w/'shipping-candidate/roms/ucode.hex')]:
 p=repo/rel;assert p.is_symlink() and p.resolve()==target.resolve(),p
 links.append(dict(path=rel,target=str(target)));p.unlink()
status={str(root):git(root,'status','--porcelain') for root in [lane,repo]}
(w/'final-integrity.json').write_text(json.dumps(dict(head=head,parents=parents,tree=git(lane,'rev-parse','HEAD^{tree}'),submodules=submodules,measured_inputs_checked=checked,protected_paths_checked=len(proof['protected_blobs_equal_first_parent']),scratch_recipe_links_removed=links,status=status),indent=2)+'\n')
assert all(not value for value in status.values()),status
subprocess.run(['git','diff','--check'],cwd=lane,check=True)
print('Integrity verified:',head,checked,'input-file checks;',len(large),'binary artifact identities retained')
