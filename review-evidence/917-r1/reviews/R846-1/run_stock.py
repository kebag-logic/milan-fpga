#!/usr/bin/env python3
"""Reproduce the stock mailbox checks in scratch. Args: checkout packet compiler-wrapper."""
from pathlib import Path
import shutil
import subprocess
import sys
repo,packet,compiler=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve(),sys.argv[3]
bench=packet/'scratch/stock/tb/verilator/mbx'
bench.mkdir(parents=True,exist_ok=True)
for p in (repo/'tb/verilator/mbx').iterdir():
    if p.is_file():shutil.copy2(p,bench/p.name)
shutil.copytree(repo/'tb/common',packet/'scratch/stock/tb/common',dirs_exist_ok=True)
with (packet/'stock-mailbox.log').open('w') as log:
    rc=subprocess.run(['make','-j16',f'ROOT={repo}',f'VERILATOR={compiler}','VBUILD_JOBS=3',
                       'run-wb','run-axil','run-cosim','run-if2'],cwd=bench,
                      stdout=log,stderr=subprocess.STDOUT).returncode
(packet/'stock-mailbox.rc').write_text(str(rc)+'\n')
sys.exit(rc)
