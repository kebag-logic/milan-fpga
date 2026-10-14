#!/usr/bin/env python3
"""Re-run the prior literal inventory forms and executable drift comparisons."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import yaml

checkout=Path(sys.argv[1]).resolve()
packet=Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT']=str(packet/'scratch/shfmt')
sys.path.insert(0,str(checkout/'scripts'))
import ci_tool_inventory as inventory
records=[]
with tempfile.TemporaryDirectory(dir=packet/'scratch') as directory:
 root=Path(directory)
 (root/'ci/image').mkdir(parents=True)
 for name in ('command-table.json','sources.lock.json'):
  shutil.copyfile(checkout/'ci/image'/name,root/'ci/image'/name)
 workflow=root/'.github/workflows/control.yml'; workflow.parent.mkdir(parents=True)
 def check(label, command=None, source=None, image=None):
  if source is not None: (root/'bootstrap.py').write_text(source)
  job={'steps':[{'run':command}]} if command else {}
  if image: job.update(image)
  workflow.write_text(yaml.safe_dump({'jobs':{'control':job}}))
  try:
   value=inventory.derive(root)
   result={'label':label,'refused':False,'tools':value['tools']}
  except inventory.Refusal as error:
   result={'label':label,'refused':True,'reason':str(error).replace(str(root),'<fixture>')}
  records.append(result)
  return result
 for command in ('sudo dpkg -i fixture.deb','npx --yes fixture@1.2.3','go install fixture@v1.0.0',
                 'sudo snap install fixture','uv tool install fixture','docker run fixture:tag',
                 'git -C somewhere fetch https://example.invalid/repo','brand_new_command --version'):
  assert check(command,command)['refused']
 for label, source in (
  ('Python keyword string','import subprocess\nsubprocess.run(args="python3 -m pip install fixture==1.0", shell=True)\n'),
  ('Python positional string','import subprocess\nsubprocess.run("python3 -m pip install fixture==1.0", shell=True)\n'),
  ('Python command alias','import subprocess\ncmd=["pip","install","fixture"]\nsubprocess.run(cmd)\n'),
  ('root Python literal list','import subprocess\nsubprocess.run(["pip","install","fixture"])\n'),
  ('undeclared network','import urllib.request\nurllib.request.urlretrieve("https://example.invalid/tool", "tool")\n')):
  assert check(label,'python3 bootstrap.py',source)['refused']
 (root/'Makefile').write_text('all:\n\tcurl https://example.invalid/tool -o tool\n\ttar xf tool\n\tmake install\n')
 assert check('Makefile downloader','make')['refused']
 assert check('missing script','python3 absent.py')['refused']
 for role in ('container','services'):
  for pinned in (False,True):
   reference='fixture@sha256:'+'a'*64 if pinned else 'fixture:latest'
   value=reference if role=='container' else {'database':{'image':reference}}
   result=check(role+(' pinned' if pinned else ' moving'),image={role:value})
   assert result['refused'] != pinned
   if pinned: assert result['tools'][0]['pin']=='sha256:'+'a'*64
 table_path=root/'ci/image/command-table.json'; table=json.loads(table_path.read_text())
 table['commands']['brand_new_command']={'class':'non-installing','prefixes':[['--version']]}
 table_path.write_text(json.dumps(table))
 assert not check('new name classified','brand_new_command --version')['refused']
 assert check('new name unclassified subcommand','brand_new_command install fixture')['refused']
 source='import socket\n'; (root/'bootstrap.py').write_text(source)
 table['scripts']['bootstrap.py']={'class':'reviewed non-installing','reason':'Local validation only.','sha256':hashlib.sha256(source.encode()).hexdigest()}
 table_path.write_text(json.dumps(table))
 assert not check('network declaration accepted','python3 bootstrap.py')['refused']
 assert check('changed declaration refused','python3 bootstrap.py','import socket\nprint("changed")\n')['refused']
 check('baseline pip','python3 -m pip install fixture==1.0')
 baseline=inventory.derive(root)
 path=root/inventory.OUTPUT
 for label in ('baseline','missing','orphan'):
  data=copy.deepcopy(baseline)
  if label=='missing': data['tools']=[]
  if label=='orphan': data['tools'].append({'tool':'unused','kind':'pip','pin':'1'})
  path.write_text(inventory.serialized(data))
  run=subprocess.run([sys.executable,str(checkout/'scripts/ci_tool_inventory.py'),'--root',str(root),'--check'],capture_output=True,text=True)
  assert run.returncode == (0 if label=='baseline' else 2)
  records.append({'label':label+' CLI comparison','rc':run.returncode,'output':run.stdout+run.stderr})
print(json.dumps(records,indent=2))
