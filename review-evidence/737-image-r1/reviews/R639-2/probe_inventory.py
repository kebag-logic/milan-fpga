#!/usr/bin/env python3
"""Check ordinary installer syntax against inventory regeneration and comparison."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

root=Path(sys.argv[1]).resolve()
out=Path(__file__).resolve().parent
cases={
 'positional-string-control': ('scripts/bootstrap.py', 'import subprocess\nsubprocess.run("python3 -m pip install fixture-package==1.0", shell=True)\n', 'python3 scripts/bootstrap.py'),
 'keyword-string': ('scripts/bootstrap.py', 'import subprocess\nsubprocess.run(args="python3 -m pip install fixture-package==1.0", shell=True)\n', 'python3 scripts/bootstrap.py'),
 'root-script': ('bootstrap.py', 'import subprocess\nsubprocess.run(["python3", "-m", "pip", "install", "fixture-package==1.0"])\n', 'python3 bootstrap.py'),
 'make-downloader': ('tb/fixture/Makefile', 'all:\n\tcurl -fsSL https://example.invalid/tool-v1.tar.gz -o tool.tar.gz\n\ttar xf tool.tar.gz\n\tmake -C tool install\n', 'make -C tb/fixture'),
}
results=[]
for name,(path,source,command) in cases.items():
 with tempfile.TemporaryDirectory(dir=out/'scratch') as temp:
  fixture=Path(temp)
  (fixture/'.github/workflows').mkdir(parents=True)
  target=fixture/path
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(source)
  (fixture/'.github/workflows/test.yml').write_text('jobs:\n  check:\n    steps:\n      - run: '+command+'\n')
  entry={'case':name,'path':path,'source':source,'workflow_command':command}
  for mode in ['--write','--check']:
   p=subprocess.run([sys.executable,str(root/'scripts/ci_tool_inventory.py'),'--root',str(fixture),mode],text=True,capture_output=True)
   entry[mode]={'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
  if (fixture/'ci/image/tool-inventory.json').exists():
   generated=json.loads((fixture/'ci/image/tool-inventory.json').read_text())
   entry['tools']=generated['tools']
   entry['inputs']=list(generated['inputs'])
  results.append(entry)
with tempfile.TemporaryDirectory(dir=out/'scratch') as temp:
 fixture=Path(temp)
 (fixture/'.github/workflows').mkdir(parents=True)
 (fixture/'.github/workflows/test.yml').write_text('jobs:\n  check:\n    steps:\n      - run: python3 -m pip install fixture-package==1.0\n')
 subprocess.run([sys.executable,str(root/'scripts/ci_tool_inventory.py'),'--root',str(fixture),'--write'],check=True,capture_output=True)
 path=fixture/'ci/image/tool-inventory.json';baseline=json.loads(path.read_text())
 for kind in ['missing-entry','orphan-entry']:
  value=json.loads(json.dumps(baseline))
  if kind=='missing-entry':value['tools']=[]
  else:value['tools'].append({'tool':'unused-fixture','kind':'pip','pin':'1.0','installed_by':[]})
  path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
  proc=subprocess.run([sys.executable,str(root/'scripts/ci_tool_inventory.py'),'--root',str(fixture),'--check'],capture_output=True,text=True)
  assert proc.returncode==2
  results.append({'case':kind,'--check':{'rc':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}})
(out/'inventory-probes.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
