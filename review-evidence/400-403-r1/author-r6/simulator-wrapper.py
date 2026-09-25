#!/usr/bin/python3
import os,sys
from pathlib import Path
args=sys.argv[1:]
for i in range(len(args)-1):
 if args[i]=='-j' and args[i+1]=='0':args[i+1]='8'
if '--Mdir' in args:
 i=args.index('--Mdir')+1; args[i]=str(Path(args[i]).resolve())
elif '--cc' in args:
 args+=['--Mdir',str(Path('obj_dir').resolve())]
args=[str(Path(a).resolve()) if a.endswith(('.cpp','.c','.cc')) and Path(a).is_file() else a for a in args]
os.execv('$VALIDATION_TOOLS/verilator-v5.050/bin/verilator',['verilator',*args])
