#!/usr/bin/env python3
"""Compare only the permitted render epoch leg at the assigned base and head.

Usage: python3 scripts/check_epoch.py CHECKOUT SIMULATOR
Each registered disposable clone and every build lives under scratch/.
"""
import concurrent.futures
import hashlib
import json
import os
import subprocess
import run_focused as f

env = os.environ.copy()
env.update(VERILATOR=f.SIM, VERILATOR_JOBS='4', TMPDIR=str(f.SCRATCH))


def arm(label, oid):
    source = f.SCRATCH / ('epoch-' + label)
    f.run('epoch-' + label + '-clone',
          ['git', 'clone', '--quiet', '--shared', '--no-checkout', str(f.REPO), str(source)],
          f.SCRATCH, env)
    f.run('epoch-' + label + '-checkout', ['git', 'checkout', '--quiet', '--detach', oid], source, env)
    for name in ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor']:
        subprocess.run(['git', 'config', 'submodule.' + name + '.url', str(f.REPO / name)],
                       cwd=source, env=env, check=True)
    f.run('epoch-' + label + '-submodules',
          ['git', '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init',
           '--jobs', '3', 'third_party/verilog-axis', 'protocol-processor', 'gptp-processor'],
          source, env)
    suite = source / 'tb/verilator/milan_dp_render'
    f.run('epoch-' + label + '-build',
          ['make', '-j16', '--no-print-directory', 'tdm8render-build', 'VERILATOR_JOBS=4'],
          suite, env)
    f.run('epoch-' + label + '-run', ['./obj_tdm8r/Vmilan_dp_tdm8r', '--epoch-only'],
          suite, env, 1)
    return (f.RECEIPTS / ('epoch-' + label + '-run.log')).read_bytes()


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    jobs = [pool.submit(arm, label, oid) for label, oid in [('base', f.BASE), ('head', f.HEAD)]]
    base, head = [j.result() for j in jobs]
result = {'base': f.BASE, 'head': f.HEAD, 'byte_equal': base == head,
          'base_sha256': hashlib.sha256(base).hexdigest(),
          'head_sha256': hashlib.sha256(head).hexdigest(),
          'base_bytes': len(base), 'head_bytes': len(head)}
(f.RECEIPTS / 'epoch-comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result), flush=True)
assert base == head
