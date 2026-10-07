#!/usr/bin/env python3
"""Bound each generated build to four jobs; select the executable via REVIEW_VERILATOR."""
import os,sys,shutil,subprocess
exe=os.environ.get('REVIEW_VERILATOR') or shutil.which('verilator')
if not exe or 'Verilator 5.050 ' not in subprocess.check_output([exe,'--version'],text=True):
 raise SystemExit('Expected scoped version 5.050; set REVIEW_VERILATOR')
args=sys.argv[1:]
for i,arg in enumerate(args[:-1]):
 if arg=='-j':args[i+1]='4'
os.execv(exe,[exe,*args])
