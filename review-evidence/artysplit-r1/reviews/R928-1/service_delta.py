#!/usr/bin/env python3
"""Recheck all service grader assertions and the two added clock mutations.
Usage: service_delta.py SOURCE PACKET
"""
from pathlib import Path
import os, sys, tempfile
root,packet=map(Path,sys.argv[1:3])
sys.dont_write_bytecode=True
tempfile.tempdir=str(packet/'scratch')
sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import selftest as s
checks=s.checks()
failed=[(n,detail) for n,ok,detail in checks if not ok]
for n,ok,detail in checks: print(('PASS ' if ok else 'FAIL ')+n)
assert not failed, failed
print('BASELINE',len(checks),'checks passed')
names=['clock: Arty stimulus keeps the 100 MHz cycle counts',
       'clock: the group factory omits its build clock']
for name in names:
 with s.mutated(name):
  failed=[n for n,ok,detail in s.checks() if not ok]
 assert failed,(name,'escaped')
 print('MUTATION CAUGHT',name,'by',failed)
print('PASS baseline and both new clock mutations')
