#!/usr/bin/env python3
"""Run independent focused checks concurrently, retaining every command and rc."""
import concurrent.futures, json, os, pathlib, subprocess, sys, time
repo=pathlib.Path(sys.argv[1]).resolve()
packet=pathlib.Path(__file__).resolve().parents[1]
raw=packet/'scratch'/'raw';raw.mkdir(exist_ok=True)
env={**os.environ,'TMPDIR':str(packet/'scratch'/'tmp'),'PYTHONDONTWRITEBYTECODE':'1',
     'PYTHONUNBUFFERED':'1','PYTHON_CPU_COUNT':'3','MAKEFLAGS':'-j16',
     'MILAN_RV32_CC':str(packet/'scratch'/'sdk'/'bin'/'riscv32-linux-gcc')}
jobs={
'ctrl-campaign':['sw/firmware/ctrl/test/test_ctrl_firmware.py','--require-rv32','--self-test','--build-dir',str(packet/'scratch'/'ctrl')],
'nvm-campaign':['sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py','--require-rv32','--self-test','--jobs','6'],
'coverage':['sw/firmware/gtest/fw_coverage.py','--check','--jobs','4','--keep',str(packet/'scratch'/'coverage')],
'rv32-controls':['sw/firmware/gtest/fw_rv32_selftest.py','--require-rv32'],
}
def run(name,args):
 start=time.monotonic()
 with (raw/(name+'.log')).open('w') as out:
  result=subprocess.run([sys.executable,*args],cwd=repo,env=env,stdout=out,stderr=subprocess.STDOUT)
 (packet/'receipts'/(name+'.rc')).write_text(str(result.returncode)+'\n')
 receipt={'command':['python3',*args], 'rc':result.returncode,'elapsed_seconds':round(time.monotonic()-start,2)}
 (raw/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print(name,result.returncode,receipt['elapsed_seconds'],flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=list(pool.map(lambda item:run(*item),jobs.items()))
sys.exit(any(results))
