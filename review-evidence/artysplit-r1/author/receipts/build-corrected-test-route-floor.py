"""Offline boundary controls for the four-report route floor; no implementation run."""
import ast,hashlib,json,re,sys,tempfile
from pathlib import Path
root=Path('$LANES/arty-split')
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4/build-corrected')
sys.path.insert(0,str(root/'scripts'))
from area_baseline import parse_timing
tree=ast.parse((r/'grade-images.py').read_text())
functions=[node for node in tree.body if isinstance(node,ast.FunctionDef)
           and node.name in ('signoff_timing','meets_floor')]
assert len(functions)==2
scope={'parse_timing':parse_timing,'re':re}
exec(compile(ast.Module(body=functions,type_ignores=[]),'grade-images.py','exec'),scope)
rows=[('equal floors','0.030 0.000 0 100 0.000 0.000 0 100',True),
      ('setup below floor','0.029 0.000 0 100 0.000 0.000 0 100',False),
      ('negative hold','0.100 0.000 0 100 -0.001 -0.001 1 100',False),
      ('hold rounds to zero','0.100 0.000 0 100 -0.000 -0.000 1 100',False),
      ('failing setup endpoint','0.100 0.000 1 100 0.000 0.000 0 100',False),
      ('missing hold counts','0.100 0.000 0 100 0.000 0.000',False)]
results=[]
with tempfile.TemporaryDirectory(dir=r/'work-tmp') as directory:
 for name,row,wanted in rows:
  path=Path(directory)/'timing.rpt'
  path.write_text('WNS(ns) TNS(ns) TNS Failing Endpoints TNS Total Endpoints WHS(ns) THS(ns) THS Failing Endpoints THS Total Endpoints\n'
                  '------- ------- ------- ------- ------- ------- ------- -------\n'+row+'\n')
  measured=scope['signoff_timing'](path)
  accepted=scope['meets_floor'](measured)
  assert accepted==wanted,(name,measured,accepted)
  results.append(dict(control=name,expected=wanted,accepted=accepted,timing=measured))
record=dict(status='PASS',controls=results,
            helper_sha256=hashlib.sha256((r/'grade-images.py').read_bytes()).hexdigest(),
            note='Zero failing hold endpoints enforces the stated WHS floor despite printed rounding; no new numerical floor.')
(r/'route-floor-controls.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
