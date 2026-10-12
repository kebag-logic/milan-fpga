#!/usr/bin/env python3
"""Run the exact-head shipping-writer gate; all disposable output stays in scratch."""
import os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parents[1]
env=os.environ.copy()
env.update(TMPDIR=str(packet/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHONUNBUFFERED='1',PYTHONHASHSEED='0')
cmd=[sys.executable,'sw/firmware/nvm_hosttest/test_nvm_firmware.py','--self-test','--jobs','8']
start=time.monotonic()
with (packet/'receipts/writer.log').open('w') as log:
 log.write('COMMAND: '+' '.join(cmd)+'\n');log.flush()
 result=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1200)
 log.write(f'\nRETURN CODE: {result.returncode}\nELAPSED SECONDS: {time.monotonic()-start:.2f}\n')
(packet/'receipts/writer.rc').write_text(str(result.returncode)+'\n')
print('writer gate return code',result.returncode,flush=True)
raise SystemExit(result.returncode)
