#!/usr/bin/env python3
"""Run bounded independent review checks; keep builds separate from receipts."""
import concurrent.futures
import os
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1',
           VERILATOR='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator', VBUILD_JOBS='2')
tb = root / 'tb/verilator/mbx'
flags = subprocess.check_output(['make', '-s', 'print-dma-vflags'], cwd=tb, env=env, text=True).splitlines()
tasks = {
 'budget-selftest': [['python3', '-B', 'tb/verilator/ctrl_service_budget/run.py', '--self-test']],
 'mailbox-generator': [['python3', '-B', 'sw/mailbox/gen_mailbox.py', '--check', '--crosscheck', '--selftest']],
 'dma-positive': [[*flags, '--Mdir', str(scratch/'dma-positive'),
                   str(root/'hdl/milan/mailbox/KL_mbx_pkg.sv'),
                   str(root/'hdl/milan/mailbox/KL_mbx_dma.sv'), str(tb/'dma_main.cpp'), '-o', 'Vmbx_dma'],
                  [str(scratch/'dma-positive/Vmbx_dma')]],
 'dma-mutants': [['python3', '-B', 'tb/verilator/mbx/dma_mutants.py', '--jobs', '4', '--keep', str(scratch/'dma-mutants')]],
}
def run(item):
 name, commands = item
 with (packet/(name+'.log')).open('w') as log:
  rc = 0
  for command in commands:
   log.write('COMMAND '+repr(command)+'\n'); log.flush()
   rc = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
   if rc: break
 (packet/(name+'.rc')).write_text(str(rc)+'\n')
 print(name, rc, flush=True)
 return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results = list(pool.map(run, tasks.items()))
sys.exit(int(any(results)))
