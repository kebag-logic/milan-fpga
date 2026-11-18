#!/usr/bin/env python3
import concurrent.futures, os, pathlib, subprocess, sys
P=pathlib.Path(__file__).resolve().parents[1]
R=P/'receipts/firmware';R.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(P/'scratch'))
def run(i):
 cmd=[sys.executable,'-u','sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--jobs','4','--shard',f'{i}/4','--build-dir',str(P/'scratch'/f'fw{i}')]
 with (R/f'shard{i}.log').open('w') as f:
  f.write('COMMAND '+repr(cmd)+'\n');f.flush()
  rc=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env).returncode
 (R/f'shard{i}.rc').write_text(str(rc)+'\n')
 print('shard',i,'rc',rc,flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(run,range(4)))
sys.exit(any(results))
