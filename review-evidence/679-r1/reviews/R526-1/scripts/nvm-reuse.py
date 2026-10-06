#!/usr/bin/env python3
"""Run the unchanged store driver with one reusable physical tree per worker.

All 106 mutations, source changes, compiler flags, fixtures, expected tests,
cache keys and failure grading are the exact-head implementation. Only the
work / mutant.name operation resolves to a thread-owned physical directory.
"""
import argparse,os,pathlib,sys,threading
ap=argparse.ArgumentParser();ap.add_argument('repo',type=pathlib.Path);ap.add_argument('--jobs',type=int,required=True);args=ap.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1];repo=args.repo.resolve();os.chdir(repo)
os.environ.update(TMPDIR=str(packet/'scratch/tmp'),PYTHONDONTWRITEBYTECODE='1',PYTHON_CPU_COUNT=str(args.jobs),MILAN_RV32_CC=str(packet/'scratch/sdk/bin/riscv32-linux-gcc'))
sys.dont_write_bytecode=True;sys.path.insert(0,str(repo/'sw/firmware/ctrl_nvm/test'))
import test_ctrl_nvm as subject
original=subject.plant_and_grade;lock=threading.Lock();slots={}
class WorkSlot:
 def __init__(self,path,name):self.path,self.name=path,name
 def __truediv__(self,name):
  assert name==self.name,(name,self.name)
  return self.path
def reuse(mutant,shape,held,work,build):
 with lock:
  index=slots.setdefault(threading.get_ident(),len(slots));assert index<args.jobs
 return original(mutant,shape,held,WorkSlot(work/f'slot-{index}',mutant.name),build)
subject.plant_and_grade=reuse
sys.argv=['test_ctrl_nvm.py','--require-rv32','--self-test','--jobs',str(args.jobs)]
print('Original store driver and all grading; reusable physical worker directories',flush=True)
raise SystemExit(subject.main())
