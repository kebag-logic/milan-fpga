#!/usr/bin/env python3
"""Compare all derived default artifacts with the exact review base."""
import argparse, dataclasses, hashlib, json, os, pathlib, subprocess, sys, types
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('--mode',choices=['base','head']);a=p.parse_args()
root=pathlib.Path(__file__).resolve().parent
if not a.mode:
 rows=[]
 for mode in ['base','head']:
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(root/'scratch'))
  data=subprocess.check_output([sys.executable,__file__,str(a.source),'--mode',mode],env=env,text=True)
  rows.append(json.loads(data))
 assert rows[0]==rows[1], 'default artifact difference'
 print(json.dumps({'result':'PASS','base':'3cda030c174b325e36c26af6420487ff91346d15','head':'2e278379c1ae9ea09063b3e3cb183d0e8a3f0929','artifacts':rows[1]},indent=2))
 raise SystemExit(0)
sys.path[:0]=[str(a.source/'sw/builder'),str(a.source/'avdecc')]
if a.mode=='base':
 for name,path in [('aem_specs','avdecc/aem_specs.py'),('endstation_builder','sw/builder/endstation_builder.py')]:
  text=subprocess.check_output(['git','show','3cda030c17:'+path],cwd=a.source,text=True)
  m=types.ModuleType(name);m.__file__=str(a.source/path);sys.modules[name]=m;exec(compile(text,m.__file__,'exec'),m.__dict__)
import endstation_builder as b
from test_input_loopback import image
result={}
for shape in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']:
 art=b._derive_artifacts(a.source/'configs'/(shape+'.yaml'))
 values=dataclasses.asdict(art)
 result[shape]={k:hashlib.sha256(json.dumps(v,sort_keys=True,default=str).encode()).hexdigest() for k,v in values.items()}
 result[shape]['descriptor_bytes']=hashlib.sha256(image(art.overlay)).hexdigest()
print(json.dumps(result,sort_keys=True))
