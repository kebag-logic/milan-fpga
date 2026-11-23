import sys,subprocess,json,hashlib,re
from pathlib import Path
root=Path('$CHECKOUT');w=Path('$SCRATCH');out=w/'gateware-identity';out.mkdir(exist_ok=True)
sys.path.insert(0,str(root/'sw/builder'));import endstation_builder as b
results=[]
for name in ['endstation_ax7101_1x1_tdm8','endstation_ax7101_8x8']:
 cfg=b.load_config(root/'configs'/(name+'.yaml'));args=b.emit_soc_argv(cfg);args[args.index('--ctrl-firmware')+1]=str(w/'builds'/(name+'-off')/'ctrl_app.elf')
 for mode in ['baseline','final']:
  target=out/name/mode;target.mkdir(parents=True,exist_ok=True)
  cmd=[sys.executable,str(w/'identity_soc.py'),mode,*args,'--entity-gen-dir',str(root/'sw/builder/out/a826_off_identity'/name),'--output-dir',str(target),'--no-compile-software']
  with (target/'export.log').open('w') as log:r=subprocess.run(cmd,cwd=root,stdout=log,stderr=subprocess.STDOUT,timeout=3600)
  if r.returncode:raise RuntimeError((name,mode,r.returncode))
 a=out/name/'baseline';z=out/name/'final';files=['gateware/alinx_ax7101.v','aem_desc.bin','csr.csv']+[str(p.relative_to(a)) for p in (a/'gateware').glob('*.init')]
 for n in files:
  before=(a/n).read_bytes();after=(z/n).read_bytes()
  exact=before==after
  if n.endswith('.v'):
   # LiteX emits a wall-clock date and unordered hierarchy COMMENT tree.
   # Retain raw hashes and declare this comparison's narrower scope.
   clean=lambda b:re.sub(rb'/\*.*?\*/|//[^\n]*',b'',b,flags=re.S)
   assert clean(before)==clean(after),(name,n)
  elif n.endswith('.csv'):
   assert [v for v in before.splitlines() if not v.startswith(b'#')]==[v for v in after.splitlines() if not v.startswith(b'#')],(name,n)
  else:assert exact,(name,n)
  results.append({'shape':name,'file':n,'bytes':len(after),'byte_identical':exact,
    'scope':'excluding generated comments' if n.endswith(('.v','.csv')) else 'all bytes',
    'baseline_sha256':hashlib.sha256(before).hexdigest(),'sha256':hashlib.sha256(after).hexdigest()})
 print(name,'GATEWARE COMMENT-FREE IDENTITY AND IMAGE BYTE IDENTITY PASS',len(files),'files',flush=True)
(w/'gateware-identity.json').write_text(json.dumps(results,indent=2)+'\n')
