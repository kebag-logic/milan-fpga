#!/usr/bin/env python3
import argparse,concurrent.futures,importlib.util,json,pathlib,subprocess
p=argparse.ArgumentParser();p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);a=p.parse_args();root=a.source.resolve()
patches=sorted(root.glob('tb/**/*.patch'))
def test(f):
 r=subprocess.run(['git','apply','--check',str(f)],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);return {'patch':str(f.relative_to(root)),'rc':r.returncode,'output':r.stdout}
with concurrent.futures.ThreadPoolExecutor(8) as pool:records=list(pool.map(test,patches))
spec=importlib.util.spec_from_file_location('notify',root/'tb/pp_top/notify_mutants.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
anchors=[]
for mutant in m.MUTANTS:
 buffers={};errors=[]
 for path,old,new in mutant.edits:
  s=buffers.setdefault(path,(root/path).read_text());count=s.count(old)
  if count!=1:errors.append({'path':path,'count':count})
  buffers[path]=s.replace(old,new,1)
 anchors.append({'mutant':mutant.name,'errors':errors})
out={'patches':records,'notification_arms':anchors};(a.packet/'receipts/plant-check.json').write_text(json.dumps(out,indent=2)+'\n')
print('patches',len(records),'refused',sum(x['rc']!=0 for x in records));print('notification arms',len(anchors),'refused',sum(bool(x['errors']) for x in anchors));raise SystemExit(any(x['rc'] for x in records) or any(x['errors'] for x in anchors))
