#!/usr/bin/env python3
"""Replay normal store tests and independently build/kill 16 binding plants.
Usage: python3 -B focused_store.py REPO [--reuse-shapes PREVIOUS_SHAPES_DIR]
Without --reuse-shapes, build the normal binaries afresh. All disposable data
is placed beside this script under scratch/. Uses at most 13 concurrent jobs.
"""
import argparse, concurrent.futures, hashlib, os, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('repo',type=Path); p.add_argument('--reuse-shapes',type=Path)
a=p.parse_args(); repo=a.repo.resolve(); out=Path(__file__).resolve().parent
(out/'scratch').mkdir(exist_ok=True)
os.environ['PYTHONDONTWRITEBYTECODE']='1'; os.environ['TMPDIR']=str(out/'scratch')
sys.path.insert(0,str(repo/'sw/firmware/ctrl_nvm/test'))
import test_ctrl_nvm as t
import nvm_mutants as m
import fw_gtest
names='bind_window_none bind_window_for_all bind_window_longer bind_window_shorter bind_class_past_block bind_class_no_lower_bound bind_class_first_only bind_class_not_first bind_window_latest_end bind_window_ends_open_one window_left_armed bind_in_flight_no_window other_in_flight_windowed bind_in_flight_clears_next bind_in_flight_lost bind_window_ends_backoff'.split()
plants=[v for v in m.MUTANTS if v.name in names]; assert len(plants)==16
work=Path(tempfile.mkdtemp(prefix='focused-store-',dir=out/'scratch'))
base=t.prepare(repo/'configs/endstation_ax7101_1x1_tdm8.yaml',work/'base')
def normal(cfg):
 d=work/'normal'/cfg.stem; shape=t.prepare(cfg,d); logs=[]; good=True
 for binary in t.binaries(shape):
  if a.reuse_shapes:
   candidates=list((a.reuse_shapes/cfg.stem/binary.name).glob('nvm_*'))
   exes=[x for x in candidates if x.is_file() and os.access(x,os.X_OK)]
   assert len(exes)==1,(binary.name,exes)
   exe=exes[0]
  else: exe=t.build_suite(shape.inputs,d/binary.name,fw_gtest.Build(jobs=1),binary)
  ok,log=t.run_suite(exe,t.fixture_of(shape,binary)); good &= ok
  logs.append(f'BINARY {cfg.stem}/{binary.name} sha256 {hashlib.sha256(exe.read_bytes()).hexdigest()}\n{log}')
 (out/f'normal-{cfg.stem}.log').write_text('\n'.join(logs)); print('NORMAL',cfg.stem,'PASS' if good else 'FAIL',flush=True)
 return good
def mutant(v):
 d=work/'plants'/v.name; tree=d/'tree'; m.plant(v,tree)
 exe=t.build_suite(base.inputs,d/'build',fw_gtest.Build(jobs=1),t.SUITE,tree)
 ok,log=t.run_suite(exe,base.fixture,v.kills); survivors=m.survivors(v,log)
 (out/f'plant-{v.name}.log').write_text('Expected failing checks: '+repr(v.kills)+'\n'+log+'\nSurvivors: '+repr(survivors)+'\n')
 good=not ok and not survivors
 print('PLANT',v.name,'KILLED' if good else 'FAIL',flush=True); return good
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as baseline_pool, concurrent.futures.ThreadPoolExecutor(max_workers=8) as mutant_pool:
 jobs=[baseline_pool.submit(normal,cfg) for cfg in sorted((repo/'configs').glob('endstation_*.yaml'))]
 jobs += [mutant_pool.submit(mutant,v) for v in plants]
 results=[job.result() for job in jobs]
print('RESULT',sum(results),'/',len(results),flush=True)
raise SystemExit(0 if all(results) else 1)
