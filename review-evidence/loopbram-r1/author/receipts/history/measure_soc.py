import sys,runpy,json
from pathlib import Path
root=Path('$CHECKOUT')
sys.path.insert(0,str(root/'sw/litex'))
import ctrl_memory
original=ctrl_memory.plan
def measure(image,**kw):
 try:
  return original(image,**kw)
 except ctrl_memory.Refusal as error:
  if error.rule != 'budget': raise
  print('MEASUREMENT ONLY; PRODUCT REFUSAL RETAINED:',error,flush=True)
  result=original(image,budget=float('inf'))
  print('S14 MEASURED ALLOCATION:',json.dumps(result.summary()),flush=True)
  return result
ctrl_memory.plan=measure
import milan_soc
def scratch_output(entity_gen_dir,name):
 path=Path(entity_gen_dir)/name
 if not path.is_file(): raise RuntimeError(path)
 return str(path)
milan_soc._builder_out=scratch_output
milan_soc.main()
