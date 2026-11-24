"""Validate the pending edits on disposable file copies; no native simulation."""
import ast,hashlib,importlib.util,json,shutil,subprocess,sys
from pathlib import Path
r=Path('$VALIDATION_STORAGE/artysplit-a829/r4'); source=Path.cwd(); target=r/'candidate-cost-preview-1424'
names=['sw/firmware/ctrl/loop/ctrl_loop.h','sw/firmware/ctrl/loop/ctrl_loop.c',
       'sw/firmware/ctrl/aecp/aecp_mbx.h','sw/firmware/ctrl/plat/ctrl_plat_phy.h',
       'tb/verilator/ctrl_split_boot/run.py']
names += ['tb/verilator/ctrl_service_budget/'+n+'.py' for n in
          ('shape_costs','poll_grade','load_grade','rows_grade','rows_tiers','edit_rows','run')]
before={}
for name in names:
 p=target/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/name,p)
 before[name]=hashlib.sha256((source/name).read_bytes()).hexdigest()
with (r/'candidate-cost-preview-1424.log').open('w') as log:
 subprocess.run([sys.executable,'-B',str(r/'install-own-costs.py'),str(r/'model-1424.json')],
                cwd=target,stdout=log,stderr=subprocess.STDOUT,check=True)
for name in names:
 if name.endswith('.py'):ast.parse((target/name).read_text())
 assert hashlib.sha256((source/name).read_bytes()).hexdigest()==before[name]
path=target/'tb/verilator/ctrl_service_budget/shape_costs.py'
spec=importlib.util.spec_from_file_location('preview_shape_costs',path);module=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=module;spec.loader.exec_module(module)
new=module.listed((target/module.HEADER).read_text());old=module.listed((source/module.HEADER).read_text().replace(
 '#elif CTRL_LOOP_SHAPE(1u, 1u, 2u)', '#elif CTRL_LOOP_SHAPE(1u, 100u, 2u)'))
for shape,costs in old.items():
 if shape.sources!=100:assert new[shape]==costs
own=new[module.Shape(1,1,2)]
assert all(own[n]>0 for n in module.ARTY_NAMES)
result=dict(status='PASS; disposable edit preview only',own=own,original_files_unchanged=before)
(r/'candidate-cost-preview-1424.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
