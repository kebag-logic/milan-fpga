#!/usr/bin/env python3
import os,sys,subprocess
from pathlib import Path
repo,packet,pico,crt,lite,cc=map(Path,sys.argv[1:])
out=packet/'scratch/runtime';env={**os.environ,'MILAN_RV32_CC':str(cc)}
subprocess.run([sys.executable,'-B',str(repo/'sw/firmware/ctrl/test/ctrl_image_runtime.py'),'--picolibc',str(pico),'--compiler-rt',str(crt),'--litex-software',str(lite),'--output',str(out)],env=env,check=True)
subprocess.run([sys.executable,'-B',str(packet/'scripts/rebuild_runtime.py'),str(out),str(packet/'scratch/runtime-freestanding')],env=env,check=True)
