#!/usr/bin/env python3
"""Focused original leg, malformed-input controls, seed controls and docs checks."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

out = Path(__file__).resolve().parents[1]
repo = Path(sys.argv[1]).resolve()
verilator = str(Path(sys.argv[2]).resolve())
suite = out / 'scratch/tb/verilator/ptp_ts'
receipts = []
def run(name, command, expected=0, cwd=repo):
    command = ['rtk', 'proxy', *command]
    start = time.time()
    log = out / 'raw' / (name + '.log')
    with log.open('wb') as stream:
        result = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT)
    row = dict(name=name, command=command, cwd=str(cwd), exit=result.returncode,
               expected=expected, seconds=time.time()-start)
    receipts.append(row)
    (out / 'raw/focused-controls-results.json').write_text(json.dumps(receipts, indent=2)+'\n')
    assert result.returncode == expected, row
    return log.read_text()

# Export the exact pinned FIFO input; no submodule checkout or source is edited.
fifo = repo / 'third_party/verilog-axis/rtl/axis_fifo.v'
target = out / 'scratch/third_party/verilog-axis/rtl/axis_fifo.v'
target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(fifo, target)
print('Pinned FIFO sha256', hashlib.sha256(target.read_bytes()).hexdigest())
makefile = (suite / 'Makefile').read_text()
flags = re.search(r'^VFLAGS = (.*?)\n\n', makefile, re.M | re.S).group(1)
flags = flags.replace('\\\n', '').replace('$(TOP)', 'ptp_ts_top').replace('$(RTL_DIR)', '../../../hdl')
assert flags.count('-j 0') == 1
# The sole recipe override is the user-authorized eight-job build cap.
flags = flags.replace('-j 0', '-j 8')
run('original-ptp-ts', ['make', '--no-print-directory', '-C', str(suite), 'run',
                        'VERILATOR='+verilator, 'VFLAGS='+flags])

for width in [8, 64]:
    binary = str(suite / f'obj_dir_mux_sva_w{width}/Vmux_sva')
    for seed in range(20):
        run(f'seed-w{width}-{seed}', [binary, f'+seed={seed}'])
    for number, arg in enumerate(['+scenario=missing', '+stimulus_fault=s2_flip_tdata',
                                  '+stimulus_fault=s0_unknown', '+seed=12x', '+seed=-1',
                                  '+seed=18446744073709551616']):
        run(f'usage-w{width}-{number}', [binary, arg], expected=2)
    log = run(f'default-stop-w{width}', [binary, '+scenario=single_beats',
                                       '+stimulus_fault=s0_drop_tvalid'], expected=1)
    assert 'u_s0_stimulus.ap_tvalid_held_until_handshake' in log and 'Verilog $stop' in log

for name, args in [
    ('docs-check', ['scripts/docs_check.py']),
    ('doc-style', ['scripts/check_doc_style.py']),
    ('doc-paths', ['scripts/check_doc_paths.py']),
    ('toc', ['scripts/gen_toc.py', '--check']),
    ('anchors', ['scripts/gen_toc.py', '--verify-anchors']),
    ('em-dash', ['scripts/check_em_dash.py', '--base', '52711029f374650dc93830d5ea28e81cb5c8f410']),
]:
    run(name, ['python3', '-B', *args])
run('diff-check', ['git', 'diff', '--check', '52711029f374650dc93830d5ea28e81cb5c8f410',
                   '059c3a60b8290873ed9fd14673f9981e8af754ce'])
print('PASS', len(receipts), 'focused commands; all actual exits match expected exits')
