#!/usr/bin/env python3
"""Reproduce focused review receipts, without source edits or network writes.
Usage: python3 replay.py EXACT_CHECKOUT PINNED_SIMULATOR
Requires the checkout's three required submodules and native test dependencies.
Use a fresh packet copy if original receipts must be retained.
"""
import os,sys,subprocess,tarfile,io
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
p=Path(__file__).resolve().parent
root=Path(sys.argv[1]).resolve(); sim=Path(sys.argv[2]).resolve()
work=p/'scratch'; work.mkdir(exist_ok=True)
source=work/'source'; source.mkdir(exist_ok=True)
subprocess.run([sys.executable,p/'integrity.py',root],check=True)
assert 'Verilator 5.050' in subprocess.check_output([sim,'--version'],text=True)
data=subprocess.check_output(['git','-C',root,'archive','HEAD'])
with tarfile.open(fileobj=io.BytesIO(data)) as t: t.extractall(source,filter='data')

def job(label,cwd,*cmd):
 subprocess.run([sys.executable,str(p/'run.py'),label,str(cwd),*map(str,cmd)],check=True)

def together(rows):
 with ThreadPoolExecutor(max_workers=len(rows)) as pool:
  results=[pool.submit(job,*row) for row in rows]
  for r in results: r.result()

job('integrity-before',root,'python3',p/'integrity.py',root)
together([
 ('generator',root,'python3','-B','sw/mailbox/gen_mailbox.py','--check','--crosscheck'),
 ('generator-selftest',root,'python3','-B','sw/mailbox/gen_mailbox.py','--selftest'),
 ('mbx-suite',source,'env','VERIFIED_SIMULATOR='+str(sim),'make','-j16','-C','tb/verilator/mbx','VERILATOR='+str(p/'simulator.py'),'run-wb','run-axil','run-cosim','run-if2'),
 ('firmware-native',root,'python3','-B','sw/firmware/ctrl/test/test_ctrl_firmware.py','--build-dir',work/'firmware-native')])
together([
 ('rtl-mutants',source,'env','VERIFIED_SIMULATOR='+str(sim),'VERILATOR='+str(p/'simulator.py'),'python3','-B','tb/verilator/mbx/mutants.py','--jobs','4','--keep',work/'rtl-mutants'),
 ('firmware-coverage',root,'python3','-B','sw/firmware/gtest/fw_coverage.py','--check','--jobs','4','--keep',work/'coverage'),
 ('firmware-mutants',root,'python3',p/'filter_mutants.py',root,work/'firmware-mutants')])
together([
 ('boundary-probe',root,'python3',p/'boundary_probe.py',source,sim),
 ('tally-selftest',root,'python3','-B','sw/firmware/gtest/tally_selftest.py','--mutants'),
 ('coverage-selftest',root,'python3','-B','sw/firmware/gtest/fw_coverage.py','--selftest'),
 ('fixture-audit',root,'python3',p/'fixture_audit.py',root,work)])
job('static-checks',root,'python3',p/'static_checks.py',root)
job('integrity-after',root,'python3',p/'integrity.py',root)
