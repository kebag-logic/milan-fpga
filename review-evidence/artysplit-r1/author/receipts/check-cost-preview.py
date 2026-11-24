"""Run the Arty model against a read-only overlay of proposed cost edits.

This is a model check, never native-image qualification. Module filenames stay
at the real source paths so their ROOT constants and untouched inputs agree.
"""
import importlib.abc,importlib.util,json,sys
from pathlib import Path
from unittest.mock import patch
root=Path.cwd(); r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); preview=r/'candidate-cost-preview'
budget=root/'tb/verilator/ctrl_service_budget'
sys.path.insert(0,str(budget))
read_text=Path.read_text;read_bytes=Path.read_bytes
def overlay(path):
 try: proposed=preview/path.relative_to(root)
 except ValueError:return path
 return proposed if proposed.is_file() else path
class Loader(importlib.abc.SourceLoader):
 def __init__(self,path):self.path=path
 def get_filename(self,name):return str(self.path)
 def get_data(self,path):return read_bytes(overlay(Path(path)))
class Finder(importlib.abc.MetaPathFinder):
 def find_spec(self,name,path=None,target=None):
  source=budget/(name+'.py')
  if source.is_file() and overlay(source)!=source:
   return importlib.util.spec_from_loader(name,Loader(source))
finder=Finder();sys.meta_path.insert(0,finder)
with patch.object(Path,'read_text',lambda path,*args,**kwargs:read_text(overlay(path),*args,**kwargs)), \
     patch.object(Path,'read_bytes',lambda path:read_bytes(overlay(path))):
 import arty_grade,shape_costs,load_grade
 model,findings=arty_grade.inspect(root)
 print(json.dumps(dict(model=model,findings=findings),indent=2),flush=True)
 tests=dict(shape_controls=shape_costs.controls(root),load_controls=load_grade.controls(root))
 print(json.dumps(tests,indent=2),flush=True)
 if '--selftest' in sys.argv:
  import selftest
  tests['complete_grader_selftest']=['failed'] if selftest.main([]) else []
 (r/'candidate-cost-preview-model.json').write_text(json.dumps(dict(
     status='PASS' if not findings and not any(tests.values()) else 'FAIL',
     evidence='read-only model overlay; no compiled image',model=model,findings=findings,tests=tests),indent=2)+'\n')
 raise SystemExit(bool(findings or any(tests.values())))
