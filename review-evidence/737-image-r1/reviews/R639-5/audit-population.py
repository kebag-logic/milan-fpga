import pathlib,sys,tarfile,json,hashlib,collections,subprocess
p=pathlib.Path(__file__).resolve().parent;root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'ci/image'));import image_archive
path=p/'scratch/image/cold-a.tar';_,manifest,_=image_archive.metadata(path,'linux/amd64');population=[];forbidden=[];embedded={};cpu={}
prefix='opt/python/lib/python3.12/site-packages/pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv/'
with tarfile.open(path) as outer:
 for number,layer in enumerate(manifest['layers']):
  counts=collections.Counter();roots=collections.Counter()
  with image_archive.blob(outer,layer['digest']) as stream,tarfile.open(fileobj=stream,mode='r|*') as t:
   for m in t:
    name=m.name.removeprefix('./');counts['members']+=1;roots[name.split('/')[0]]+=1
    if name.split('/')[0] in ('inputs','recipe','build','build-context','context'):forbidden.append(name)
    if name.startswith('opt/tsn-gen/') and any(x in name for x in ('__pycache__','.pyc','.log','CMakeCache','CMakeFiles')):forbidden.append(name)
    if m.isfile():counts['regular']+=1
    if m.issym():counts['symlinks']+=1
    if name in ('opt/ci-image/smoke.py','opt/ci-image/sources.lock.json'):
     data=t.extractfile(m).read();expected=(root/'ci/image'/pathlib.Path(name).name).read_bytes();embedded[name]={'sha256':hashlib.sha256(data).hexdigest(),'matches_head':data==expected}
    if name.startswith(prefix) and (m.isfile() or m.issym()):
     cpu[name.removeprefix(prefix)]={'mode':m.mode&0o111,'kind':'file' if m.isfile() else 'symlink','value':hashlib.sha256(t.extractfile(m).read()).hexdigest() if m.isfile() else m.linkname}
  population.append({'layer':number,'digest':layer['digest'],'counts':dict(counts),'top_roots':dict(roots)})
assert not forbidden and all(v['matches_head'] for v in embedded.values())
# Reconstruct only checksum-pinned public CPU archives and apply the committed patch.
pins=json.loads((root/'ci/image/sources.lock.json').read_text());rows={r['tool']:r for r in pins['sources']};selected={'VexiiRiscv'}
while True:
 more=selected|{r['tool'] for r in pins['sources'] if r.get('parent') in selected}
 if more==selected:break
 selected=more
out=p/'scratch/cpu-expected';out.mkdir(exist_ok=True);destinations={'VexiiRiscv':out/'pythondata_cpu_vexiiriscv/verilog/ext/VexiiRiscv'};pending=set(selected);proof=[]
while pending:
 for name in sorted(pending.copy()):
  row=rows[name]
  if name!='VexiiRiscv' and row['parent'] not in destinations:continue
  dst=destinations[name] if name=='VexiiRiscv' else destinations[row['parent']]/row['path'];destinations[name]=dst;dst.mkdir(parents=True,exist_ok=True)
  archive=p/'scratch/image/context'/row['filename']
  with archive.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
  assert sha==row['sha256'] and archive.stat().st_size==row['size']
  with tarfile.open(archive) as t:
   for m in t:
    _,sep,rest=m.name.partition('/')
    if not sep or not rest:continue
    m.name=rest;t.extract(m,dst,filter='data')
  pending.remove(name);proof.append({'tool':name,'version':row['version'],'sha256':sha})
patch=root/'sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch'
r=subprocess.run(['git','apply','--unsafe-paths',str(patch)],cwd=out,capture_output=True,text=True)
assert r.returncode==0,r.stderr
actual={}
for f in destinations['VexiiRiscv'].rglob('*'):
 if f.is_symlink():v={'mode':f.lstat().st_mode&0o111,'kind':'symlink','value':str(f.readlink())}
 elif f.is_file():v={'mode':f.stat().st_mode&0o111,'kind':'file','value':hashlib.sha256(f.read_bytes()).hexdigest()}
 else:continue
 actual[f.relative_to(destinations['VexiiRiscv']).as_posix()]=v
mismatch=[n for n in sorted(actual.keys()|cpu.keys()) if actual.get(n)!=cpu.get(n)]
result={'layers':population,'forbidden_roots_or_leftovers':forbidden,'embedded_inputs':embedded,'cpu_archives':proof,'cpu_expected':len(actual),'cpu_image':len(cpu),'cpu_mismatches':mismatch,'patch_sha256':hashlib.sha256(patch.read_bytes()).hexdigest()}
(p/'image-population.json').write_text(json.dumps(result,indent=2)+'\n')
print('members',sum(r['counts']['members'] for r in population),'CPU',len(cpu),'mismatches',len(mismatch));assert not mismatch
