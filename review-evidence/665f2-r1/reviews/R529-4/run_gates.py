#!/usr/bin/env python3
"""Foreground gate runner; each child is awaited and owns a log/return receipt."""
import argparse, concurrent.futures, json, os, subprocess, time, signal
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--phase',choices=['firmware','rtl','docs','finish'],required=True);a=ap.parse_args()
r=a.root.resolve();p=a.packet.resolve();s=p/'scratch';logs=p/'receipts';s.mkdir(exist_ok=True);logs.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(s),PYTHONUNBUFFERED='1')
py='python3'
if a.phase=='firmware':
 cmds=[(f'ctrl-shard-{i}',[py,'sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--jobs','2','--mutation-shard',str(i),'4']) for i in range(4)]
 cmds += [('coverage',[py,'sw/firmware/gtest/fw_coverage.py','--check','--jobs','2']),('nvm',[py,'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py','--require-rv32','--self-test','--jobs','4'])]
 workers=6
elif a.phase=='finish':
 cmds=[('ctrl-shard-1-retry',[py,'sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--jobs','2','--mutation-shard','1','4']),('nvm-baseline',[py,'sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py','--require-rv32','--jobs','2']),('differential',[py,'sw/firmware/ctrl/test/maap_differential.py','--self-test','--keep',str(s/'differential')]),('mailbox',['make','-j16','-C',str(s/'mbx-tree/tb/verilator/mbx'),'VBUILD_JOBS=1'])];workers=4
elif a.phase=='rtl':
 cmds=[('differential',[py,'sw/firmware/ctrl/test/maap_differential.py','--self-test','--keep',str(s/'differential')]),('mailbox',['make','-j16','-C',str(s/'mbx-tree/tb/verilator/mbx'),'VBUILD_JOBS=1'])];workers=2
else:
 mdpy=env.get('MARKDOWN_PYTHON',py)
 cmds=[('docs-check',[py,'scripts/docs_check.py']),('gen-toc',[mdpy,'scripts/gen_toc.py','--check']),('em-dash',[mdpy,'scripts/check_em_dash.py','--base','d51b373a']),('coverage-selftest',[py,'sw/firmware/gtest/fw_coverage.py','--selftest']),('tally-selftest',[py,'sw/firmware/gtest/tally_selftest.py','--mutants']),('rv32-selftest',[py,'sw/firmware/gtest/fw_rv32_selftest.py']),('mailbox-generator',[py,'sw/mailbox/gen_mailbox.py','--check','--crosscheck'])];workers=4

def run(item):
 name,cmd=item;t=time.monotonic()
 print('START '+name,flush=True)
 with (logs/(name+'.log')).open('w') as f:
  child=subprocess.Popen(cmd,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
  try: rc=child.wait(timeout=570)
  except subprocess.TimeoutExpired:
   os.killpg(child.pid,signal.SIGKILL);child.wait();rc=124
 (logs/(name+'.rc')).write_text(str(rc)+'\n')
 receipt={'command':cmd,'rc':rc,'seconds':round(time.monotonic()-t,3)}
 (logs/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print('DONE '+name+' '+str(receipt),flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
 results=list(ex.map(run,cmds))
raise SystemExit(int(any(results)))
