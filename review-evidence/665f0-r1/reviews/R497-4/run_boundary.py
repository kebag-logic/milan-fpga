#!/usr/bin/env python3
"""Usage: python3 run_boundary.py REPO PACKET"""
import pathlib, subprocess, sys
repo,packet=map(lambda x:pathlib.Path(x).resolve(),sys.argv[1:3])
f=repo/'sw/firmware/ctrl'
binary=packet/'scratch/boundary-probe'
cmd=['cc','-std=c11','-O2','-Wall','-Wextra','-Werror','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all', '-I'+str(f/'adp'),'-I'+str(f/'wire'),str(packet/'boundary_probe.c'),str(f/'adp/adp.c'),'-o',str(binary)]
r=subprocess.run(cmd,capture_output=True,text=True)
assert r.returncode==0,r.stderr
r=subprocess.run([str(binary)],capture_output=True,text=True,timeout=60)
(packet/'boundary.log').write_text(r.stdout+r.stderr)
(packet/'boundary.rc').write_text(str(r.returncode)+'\n')
print(r.stdout,end='');sys.exit(r.returncode)
