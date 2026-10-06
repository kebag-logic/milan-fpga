#!/usr/bin/env python3
"""Run #134's six new fault definitions and preserve both masked-expiry receipts."""
import argparse, importlib.util, os, subprocess, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('repo',type=Path);p.add_argument('packet',type=Path);p.add_argument('--verilator',required=True,type=Path);p.add_argument('--jobs',type=int,default=3);a=p.parse_args()
assert 1 <= a.jobs <= 3
assert 'Verilator 5.050' in subprocess.check_output([str(a.verilator),'--version'],text=True)
work=a.packet/'scratch/new-mutations';work.mkdir(exist_ok=True)
os.environ.update(TMPDIR=str(work),MAKEFLAGS='-j16',REVIEW_COMPILER=str(a.verilator),
                  VERILATOR=str(a.packet/'scratch/focused/bounded-compiler.py'))
tempfile.tempdir=str(work);sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('srp_campaign',a.repo/'tb/srp_top/mutants.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=a.packet/'receipts/new-mutations';out.mkdir(exist_ok=True)
original=m.trial
def receipt(job):
    rc,text=original(job)
    label,suite,group=job;name=f'{label or "control"}-{suite}-{group}'
    (out/f'{name}.log').write_text(text);(out/f'{name}.rc').write_text(str(rc)+'\n')
    return rc,text
m.trial=receipt
sys.argv=[str(spec.origin),'--output',str(out),'--jobs',str(a.jobs),'--only',
          'lv-expiry-masked,lv-expiry-last,lv-expiry-dropped,lv-sweep-misses-collision,lv-second-lv-ends,lv-never-ends']
raise SystemExit(m.main())
