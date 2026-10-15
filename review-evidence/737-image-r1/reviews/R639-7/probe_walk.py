#!/usr/bin/env python3
"""Non-mutating differential probes; set CHECKOUT and CI_IMAGE_SHFMT."""
import json, os, sys, tempfile, shutil, subprocess
from pathlib import Path
root=Path(os.environ.get('CHECKOUT', os.getcwd())).resolve()
packet=Path(__file__).resolve().parent
os.environ['TMPDIR']=str(packet/'scratch')
sys.path.insert(0,str(root/'scripts'))
import ci_differential as d
fixtures=[
 {'id':'local-self-reference','run':'X=outer\nf() { local X="$X"; zz_probe "$X"; }\nf\n'},
 {'id':'local-redeclaration','run':'f() { local X=first; local X; zz_probe "$X"; }\nf\n'},
 {'id':'loop-errexit','run':'set -e\nfor x in one two; do cd missing; set +e; done\nzz_probe end\n'},
 {'id':'make-dry-run-plus','run':'make -n\n','files':{'Makefile':'all:\n\t+zz_probe forced\n'}},
]
results=[]
for fixture in fixtures:
 fixture.update(expect='identical',shapes=[])
 with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='walk-') as name:
  scratch=Path(name); tree=scratch/'tree'; tree.mkdir()
  d.build(fixture,tree)
  walked=d.walk(fixture,tree)
  actual,statuses=d.run(fixture,tree,scratch)
  unknown=sorted(set(walked['shapes'])-set(json.loads(d.CENSUS.read_text())['shapes']))
  results.append(dict(id=fixture['id'],fixture=fixture,walked=walked,actual=actual,statuses=statuses,outcome=d.outcome(fixture,walked,actual),shapes_outside_census=unknown))
fixture={'id':'local-script-selection','run':'X=evil\nf() { local X="$X"; bash "${X}bootstrap.sh"; }\nf\n',
         'files':{'bootstrap.sh':'true\n','evilbootstrap.sh':'r639_hidden_command\n'},
         'observe':['r639_hidden_command']}
with tempfile.TemporaryDirectory(dir=packet/'scratch',prefix='selection-') as name:
 scratch=Path(name); tree=scratch/'tree'; tree.mkdir()
 d.build(fixture,tree)
 shutil.copyfile(root/'ci/image/differential-receipt.json',tree/'ci/image/differential-receipt.json')
 gates=[]
 for mode in ['--write','--check']:
  proc=subprocess.run([sys.executable,str(root/'scripts/ci_tool_inventory.py'),'--root',str(tree),mode],capture_output=True,text=True)
  gates.append({'mode':mode,'rc':proc.returncode,'stdout':proc.stdout.replace(str(tree),'<fixture>'),'stderr':proc.stderr.replace(str(tree),'<fixture>')})
 actual,statuses=d.run(fixture,tree,scratch)
 results.append({'id':fixture['id'],'fixture':fixture,'gate_enabled':True,'gates':gates,'actual':actual,'statuses':statuses})
print(json.dumps(results,indent=2))
