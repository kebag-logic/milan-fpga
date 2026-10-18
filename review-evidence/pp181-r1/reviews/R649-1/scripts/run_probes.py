#!/usr/bin/env python3
"""Build isolated mutation probes. Every process is waited for in the foreground."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('group', choices=['queue', 'router'])
p.add_argument('--repo', required=True, type=Path)
p.add_argument('--packet', required=True, type=Path)
p.add_argument('--compiler', required=True, type=Path)
a = p.parse_args()
packet = a.packet.resolve()
root = packet / 'scratch'
receipts = packet / 'receipts'
if a.group == 'queue':
    path = 'hdl/aecp/KL_aecp_notify.sv'
    variants = {
        'base': None,
        'control': None,
        'push-unseen': ("          cmdq_nempty_r <= 1'b1;", ''),
        'pop-occupied': ("cmdq_nempty_r <= (cmdq_count_r != 5'd1);", "cmdq_nempty_r <= 1'b1;"),
        'pop-offbyone': ("cmdq_nempty_r <= (cmdq_count_r != 5'd1);", "cmdq_nempty_r <= (cmdq_count_r != 5'd0);")}
else:
    path = 'hdl/packet_engine/KL_pp_event_router.sv'
    variants = {
        'base': None,
        'control': None,
        'base-pointer': ('assign base_w = valid_r ? rr_next(sel_r) : ptr_r;', 'assign base_w = ptr_r;'),
        'presented-retained': ("if (valid_r) pend_after_w[sel_r] = 1'b0;", "if (1'b0) pend_after_w[sel_r] = 1'b0;"),
        'ignore-ack': ('if (deliver_w || !valid_r) begin', "if (1'b1) begin")}
failed = 0
for name, mutation in variants.items():
    label = a.group + '-' + name
    tree = root / label
    tree.mkdir(exist_ok=True)
    for directory in ('hdl', 'tb'):
        shutil.copytree(root / 'head' / directory, tree / directory,
                        ignore=shutil.ignore_patterns('obj*', '__pycache__'), dirs_exist_ok=True)
    f = tree / path
    if name == 'base':
        f.write_bytes(subprocess.check_output(['git', 'show', '77cf6fb4:' + path], cwd=a.repo))
    elif mutation:
        old, new = mutation
        source = f.read_text()
        assert source.count(old) == 1, (name, source.count(old))
        f.write_text(source.replace(old, new))
    if a.group == 'queue':
        cwd = tree / 'tb/aecp_notify'
        shutil.copyfile(packet / 'scripts/queue_probe.cpp', cwd / 'queue_probe.cpp')
        args = [str(a.compiler), '--cc', '--exe', '--build', '-j', '4', '--public-flat-rw',
                '--top-module', 'KL_aecp_notify', '-GN_CTRL_P=2', '-GN_STREAM_IN_P=1', '-GN_STREAM_OUT_P=1',
                '-Wno-fatal', '-CFLAGS', '-std=c++17 -O2 -I' + str(cwd),
                '../../hdl/common/pp_pkg.sv', '../../hdl/aecp/KL_aecp_notify.sv', 'queue_probe.cpp', '-o', 'queue_probe']
        binary = './obj_dir/queue_probe'
    else:
        cwd = tree / 'tb/event_router'
        args = ['make', '-j16', 'VERILATOR=' + str(packet / 'scratch/compiler')]
        binary = None
    with (receipts / (label + '-build.log')).open('w') as log:
        rc = subprocess.run(args, cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    (receipts / (label + '-build.rc')).write_text(str(rc)+'\n')
    if binary and rc == 0:
        with (receipts / (label + '.log')).open('w') as log:
            rc = subprocess.run([binary], cwd=cwd, stdout=log, stderr=subprocess.STDOUT).returncode
    (receipts / (label + '.rc')).write_text(str(rc)+'\n')
    expected_pass = name in ('base', 'control')
    ok = (rc == 0) == expected_pass
    if not ok: failed += 1
    print(label, 'rc', rc, 'expected', 'pass' if expected_pass else 'failure', 'OK' if ok else 'FAIL', flush=True)
if a.group == 'queue':
    equal = (receipts / 'queue-base.log').read_bytes() == (receipts / 'queue-control.log').read_bytes()
    print('base/head cycle trace identical:', equal, flush=True)
    if not equal: failed += 1
sys.exit(1 if failed else 0)
