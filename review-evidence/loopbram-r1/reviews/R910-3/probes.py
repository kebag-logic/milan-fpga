#!/usr/bin/env python3
"""Focused review probes; all generated files stay in the packet scratch tree."""
import argparse
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('checkout', type=Path)
p.add_argument('output', type=Path)
p.add_argument('--verilator', required=True)
a = p.parse_args()
root, out = a.checkout.resolve(), a.output.resolve()
scratch = out / 'scratch' / 'probes'
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, VERILATOR=a.verilator, VERILATOR_JOBS='16', MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
version = subprocess.check_output([a.verilator, '--version'], text=True)
assert 'Verilator 5.050' in version, version
source = (root / 'hdl/milan/milan_datapath.sv').read_text()
needle = '.stream_en_i (aaf_stream_en_w),'
assert source.count(needle) == 1
mutant = scratch / 'talker7.sv'
mutant.write_text(source.replace(needle, ".stream_en_i (aaf_stream_en_w & N_STREAMS'(8'h7f)),"))
command = [sys.executable, str(root/'tb/verilator/input_loopback_dp/run.py'), '--shape', '8', '--work', str(scratch/'talker7'), '--dp-source', str(mutant)]
with (scratch/'talker7.raw.log').open('w') as log:
    result = subprocess.run(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
log = (scratch/'talker7.raw.log').read_text()
tags = [f'[FAIL] WIRE_STREAM_{label} {phase} stream 7' for label in ('DELIVERY','COMPLETE') for phase in ('edits','clipped')]
built = (scratch/'talker7/obj/parent_loopback').is_file()
ok = built and result.returncode != 0 and all(t in log for t in tags) and 'RESULT: FAIL' in log
summary = dict(version=version.strip(), command=command, exit=result.returncode, built=built, required=tags, detected=ok)
clean = lambda s: s.replace(str(root), '$CHECKOUT').replace(str(out), '$PACKET')
(out/'talker7.json').write_text(clean(json.dumps(summary, indent=2))+'\n')
(out/'talker7.log').write_text(clean('\n'.join(line for line in log.splitlines() if any(x in line for x in ('[FAIL]', 'phase ', 'parent loopback streams=', 'RESULT:', 'checks,', 'Traceback', 'Error', 'error:'))))+'\n')
(out/'talker7.full.log.gz').write_bytes(gzip.compress(clean(log).encode(),mtime=0))
print(json.dumps(summary, indent=2))
sys.exit(0 if ok else 1)
