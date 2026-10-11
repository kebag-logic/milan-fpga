#!/usr/bin/env python3
"""Independently verify the late public padding-test suggestion in scratch."""
import concurrent.futures
from pathlib import Path
import os
import subprocess
import sys

p = Path(__file__).resolve().parents[1]
src = p / 'scratch/head'
work = p / 'scratch/padding-control'
work.mkdir(parents=True, exist_ok=True)
rtl = work / 'KL_gptp_rx_parser.sv'
text = (src / 'hdl/wire/KL_gptp_rx_parser.sv').read_text()
old = "        if (rx_err_i) bad_r <= 1'b1;"
new = "        if (rx_err_i && (rx_sof_i || cnt_r <= 11'(OFF_MSGLEN_END_C) || cnt_r <= msg_end_r)) bad_r <= 1'b1;"
assert text.count(old) == 1
rtl.write_text(text.replace(old, new))
logs = p / 'receipts/local'
(logs / 'padding-control.diff').write_text('-' + old + '\n+' + new + '\n')
env = dict(os.environ, PATH=str(p / 'scratch/bin') + ':' + os.environ['PATH'], TMPDIR=str(p / 'scratch'))

def check(kind, cpp):
    tag = 'padding-' + kind
    obj = work / kind
    cmd = ['verilator', '--cc', '--exe', '--build', '-j', '4', '--top-module', 'KL_gptp_rx_parser', '-Wall', '-Wno-fatal', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '-Wno-WIDTHEXPAND', '-Wno-WIDTHTRUNC', '-Wno-UNUSEDPARAM', '--Mdir', str(obj), '-CFLAGS', '-std=c++17 -O2', str(src / 'hdl/ucpu/gptp_ucpu_pkg.sv'), str(rtl), str(src / 'tb/verilator/parser' / cpp), '-o', 'Vpadding']
    for suffix, args in [('-build', cmd), ('', [str(obj / 'Vpadding')])]:
        with (logs / (tag + suffix + '.log')).open('w') as out:
            rc = subprocess.run(args, cwd=src, env=env, stdout=out, stderr=subprocess.STDOUT).returncode
        (logs / (tag + suffix + '.rc')).write_text(str(rc) + '\n')
        if suffix and rc: return False
    output = (logs / (tag + '.log')).read_text()
    if kind == 'committed':
        return rc == 0 and '337 checks: 337 PASS, 0 FAIL' in output
    return rc == 1 and 'FAIL extended refusal drop' in output and 'FAIL extended refusal event' in output

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(check, 'committed', 'sim_main.cpp'), pool.submit(check, 'expanded', 'review_edges.cpp')]
    results = [f.result() for f in jobs]
message = f'committed suite survives padding-only defect: {results[0]}\nexpanded probe detects padding-only defect: {results[1]}\n'
(logs / 'padding-control-summary.txt').write_text(message)
print(message)
sys.exit(0 if all(results) else 1)
