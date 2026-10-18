#!/usr/bin/env python3
import os,pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
s=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else p/'scratch/source'
e=os.environ.copy();e['VERILATOR']=str(p/'bounded-compiler.py');e['TMPDIR']=str(p/'scratch');e['MAKEFLAGS']='-j16'
c=['python3',str(s/'tb/srp_top/mutants.py'),'--jobs','4','--only','domain-rejoin-always-joinin,domain-rejoin-always-joinmt,domain-lv-ignored','--output',str(p/'mutation-logs')]
with (p/'mutations.log').open('w') as f:
 f.write('COMMAND '+repr(c)+'\n');f.flush();r=subprocess.run(c,env=e,stdout=f,stderr=subprocess.STDOUT)
(p/'mutations.rc').write_text(str(r.returncode)+'\n');print('mutations rc='+str(r.returncode))
