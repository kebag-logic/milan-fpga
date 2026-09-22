from pathlib import Path
import subprocess,json,hashlib
out=Path(__file__).parent;root=out/'scratch';results=[]
for label in ['base','head']:
 for args in [[],['--out-dir',str(root/('output-'+label))]]:
  cmd=['rtk','proxy','python3','-B','avdecc/gen_aem_store.py',*args];p=subprocess.run(cmd,cwd=root/label,capture_output=True,text=True)
  (out/('store-cli-'+label+('-default' if not args else '-out-dir')+'.log')).write_text(p.stdout+p.stderr);assert p.returncode==0
  results.append({'snapshot':label,'argv':cmd,'exit_code':p.returncode})
for f in ['aem_rom.json','aecp_aem_rom.svh']:
 a=(root/'output-base'/f).read_bytes();b=(root/'output-head'/f).read_bytes();assert a==b
 results.append({'output':f,'sha256':hashlib.sha256(a).hexdigest(),'equal':True})
a=(root/'base/avdecc/aem_rom.json').read_bytes();assert a==(root/'head/avdecc/aem_rom.json').read_bytes()
results.append({'output':'default aem_rom.json','sha256':hashlib.sha256(a).hexdigest(),'equal':True})
(out/'store-cli-comparison.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS default JSON and both --out-dir output files byte-identical')
