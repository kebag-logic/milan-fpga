#!/usr/bin/env python3
"""Compare all 22 core CI object variants with stable debug-free compile paths."""
import argparse,hashlib,json,pathlib,shlex,shutil,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);a=ap.parse_args();repo=a.repo.resolve();p=a.packet.resolve();active=p/'scratch/object-comparison';active.mkdir(parents=True,exist_ok=True)
for d in ['src','include','examples']: shutil.copytree(repo/d,active/d,dirs_exist_ok=True)
base=p/'scratch/base'; variants=[]
for configuration in ['gcc','clang','rv32/debug','rv32/release']:
 for e in json.loads((p/'scratch/checks'/configuration/'compile_commands.json').read_text()):
  if pathlib.Path(e['file']).parent==repo/'src': variants.append((configuration,e))
rows=[]
for i,(configuration,e) in enumerate(variants):
 obj=active/'comparison.o'; argv=shlex.split(e['command']); result={'configuration':configuration,'target':argv[argv.index('-o')+1],'source':pathlib.Path(e['file']).name}
 argv=[x.replace(str(repo),str(active)) for x in argv];argv[argv.index('-o')+1]=str(obj);argv+=['-g0','-frandom-seed=0']
 for label,source in [('base',base),('head',repo)]:
  for d in ['src','include']:shutil.copytree(source/d,active/d,dirs_exist_ok=True)
  comp=subprocess.run(argv,cwd=active,capture_output=True,text=True)
  result[label+'_rc']=comp.returncode
  if comp.returncode:result[label+'_output']=comp.stdout+comp.stderr
  else:result[label+'_sha256']=hashlib.sha256(obj.read_bytes()).hexdigest()
 result['equal']=result.get('base_sha256')==result.get('head_sha256') and result['base_rc']==result['head_rc']==0
 rows.append(result);print(json.dumps(result),flush=True)
(p/'receipts/object-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
raise SystemExit(len(rows)!=22 or any(not x['equal'] for x in rows))
