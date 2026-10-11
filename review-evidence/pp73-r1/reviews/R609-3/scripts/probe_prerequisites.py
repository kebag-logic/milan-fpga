#!/usr/bin/env python3
"""Verify table-only edits regenerate every suite's ROM without compiling a bank."""
import argparse,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--scratch',type=Path,required=True);a=ap.parse_args()
for suite in ['pp_top','ucpu','aecp_cmds']:
 with tempfile.TemporaryDirectory(dir=a.scratch,prefix='prerequisite-') as tmp:
  root=Path(tmp)
  for name in ['hdl','tb/'+suite]:shutil.copytree(a.root/name,root/name,ignore=shutil.ignore_patterns('obj*','*.hex','image.bin','__pycache__'))
  cwd=root/'tb'/suite;cmd=['make','-j16','ucode.hex']
  subprocess.run(cmd,cwd=cwd,check=True,stdout=subprocess.DEVNULL)
  before=hashlib.sha256((cwd/'ucode.hex').read_bytes()).hexdigest()
  assert subprocess.run(['make','-q','ucode.hex'],cwd=cwd).returncode==0
  path=root/'hdl/aecp/ucode/aecp_commands.json';table=json.loads(path.read_text());table['status_codes']['STREAM_IS_RUNNING']['code']=13;path.write_text(json.dumps(table))
  assert subprocess.run(['make','-q','ucode.hex'],cwd=cwd).returncode==1
  subprocess.run(cmd,cwd=cwd,check=True,stdout=subprocess.DEVNULL)
  after=hashlib.sha256((cwd/'ucode.hex').read_bytes()).hexdigest()
  assert before!=after
  print(suite,'clean rc=0, table-only edit rc=1, regeneration changes',before,'to',after)
print('PASS: all three ROM prerequisites')
