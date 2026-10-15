#!/usr/bin/env python3
"""Read-only in-memory mutation of the two actual reached Python sources.
The stale unrelated declaration is reconciled ONLY in memory to let the probes
reach the import graph. This is diagnostic; the real current-tree check fails.
"""
import hashlib,json,os,pathlib,sys
from unittest.mock import patch
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT']=str(out/'scratch/shfmt');sys.path.insert(0,str(root/'scripts'))
import ci_tool_inventory as inventory
from ci_command_table import Audit
init=Audit.__init__;read_bytes=pathlib.Path.read_bytes;read_text=pathlib.Path.read_text
stale='scripts/check_baremetal_only.py'
def initialize(self,*args,**kwargs):
 init(self,*args,**kwargs)
 self.table['scripts'][stale]['sha256']=hashlib.sha256(read_bytes(root/stale)).hexdigest()
results=[]
with patch.object(Audit,'__init__',initialize):
 for target in [None,'tb/verilator/nvm_capture_cpu/run.py','sw/litex/flash_map.py']:
  def mutated_bytes(path):
   data=read_bytes(path)
   return data+b"\nimport subprocess\nsubprocess.run(['sudo','apt-get','install','-y','cowsay'],check=True)\n" if target and path.resolve()==root/target else data
  def mutated_text(path,*args,**kwargs):
   return mutated_bytes(path).decode() if target and path.resolve()==root/target else read_text(path,*args,**kwargs)
  with patch.object(pathlib.Path,'read_bytes',mutated_bytes),patch.object(pathlib.Path,'read_text',mutated_text):
   try:
    got=inventory.derive(root)
    committed=json.loads(read_text(root/'ci/image/tool-inventory.json'))
    results.append({'target':target,'status':'ACCEPTED','tools_equal':got['tools']==committed['tools'],'tool_count':len(got['tools']),
      'live_inputs':{k:got['inputs'].get(k) for k in ['tb/verilator/nvm_capture_cpu/run.py','sw/litex/flash_map.py']}})
   except Exception as error: results.append({'target':target,'status':'REFUSED','message':str(error)})
 # Explicitly run the no-local-module external allowance invariant.
 a=Audit(root,{})
 try: a.check_import_allowances();results.append({'external_allowance_invariant':'PASS'})
 except Exception as error: results.append({'external_allowance_invariant':str(error)})
text=json.dumps(results,indent=2)+'\n';(out/'live-gap-probes.json').write_text(text);print(text)
