#!/usr/bin/env python3
"""Reproduce a compiling assembly comment bypass in a disposable source copy."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--work',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args();r=a.repo.resolve();w=a.work.resolve();w.mkdir(parents=True,exist_ok=True)
cc=shutil.which('riscv64-unknown-elf-gcc') or shutil.which('riscv64-elf-gcc')
if not cc:raise SystemExit('An RV32 cross compiler is required')
for d in ['src','include','tests','examples','scripts']:shutil.copytree(r/d,w/d,dirs_exist_ok=True)
rows=[]; f=w/'examples/rv32/start.S'; original=(r/'examples/rv32/start.S').read_text();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');obj=w/'start.o'
for name,addition in [('clean','.equ reviewer_quote, 34\n'),('prose','.equ reviewer_quote, \'" # narrative "\n')]:
 f.write_text(original+addition)
 row={'name':name,'added_source':addition}
 for phase,cmd in [('compile',[cc,'-march=rv32i','-mabi=ilp32','-Wall','-Wextra','-Werror','-c',str(f),'-o',str(obj)]),('gate',['python3',str(w/'scripts/check_comments.py'),'--selftest'])]:
  result=subprocess.run(cmd,capture_output=True,text=True,env=env);row[phase+'_rc']=result.returncode;row[phase+'_output']=result.stdout+result.stderr
 row['object_sha256']=hashlib.sha256(obj.read_bytes()).hexdigest();rows.append(row)
result={'rows':rows,'object_bytes_equal':rows[0]['object_sha256']==rows[1]['object_sha256'],'bypass':rows[1]['compile_rc']==rows[1]['gate_rc']==0}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'}));raise SystemExit(not result['bypass'])
