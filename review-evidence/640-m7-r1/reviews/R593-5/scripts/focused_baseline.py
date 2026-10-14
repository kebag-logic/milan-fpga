#!/usr/bin/env python3
"""Build and run only gptp_tables in a byte-verified disposable input copy."""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
compiler = Path(sys.argv[2]).resolve()
identity = subprocess.check_output([str(compiler), '--version'], text=True)
assert 'Verilator 5.050 ' in identity
print(identity.strip(), flush=True)
sys.path.insert(0, str(repo / 'scripts'))
sys.path.insert(0, str(repo / 'tb/verilator/gptp_shadow'))
from owned_process import OwnedProcesses
from private_inputs import copy_inputs

scratch = packet / 'scratch/focused-baseline'
scratch.mkdir(exist_ok=True)
suite = Path('tb/verilator/gptp_tables')
with OwnedProcesses() as owner:
    copy_inputs(repo, repo / suite, scratch, owner, [])
sources = sorted(x for x in scratch.rglob('*') if x.is_file())
with (packet / 'receipts/baseline-inputs.sha256').open('w') as receipt:
    for path in sources:
        receipt.write(hashlib.sha256(path.read_bytes()).hexdigest() + '  ' + str(path.relative_to(scratch)) + '\n')
print(f'Verified and copied {len(sources)} inputs from exact parent and pinned donor blobs', flush=True)
result = subprocess.run(['make', '-j16', 'run', f'VERILATOR={compiler}', 'VERILATOR_JOBS=16'], cwd=scratch / suite, check=False)
if result.returncode:
    sys.exit(result.returncode)
runtime = subprocess.check_output(['./obj_dir/Vgptp_tables_sim', 'one_valued.tsv'], cwd=scratch / suite)
(packet / 'receipts/gptp-tables-runtime.log').write_bytes(runtime)
print('Second execution retained as receipts/gptp-tables-runtime.log', flush=True)
