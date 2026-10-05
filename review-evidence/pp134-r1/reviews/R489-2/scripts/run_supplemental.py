#!/usr/bin/env python3
"""Preserve the integrated reverse-order fault receipt and audit patch planting."""
import argparse
import concurrent.futures
import os
from pathlib import Path
import subprocess
import tarfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--packet', type=Path, required=True)
a = p.parse_args()
root, packet = a.source.resolve(), a.packet.resolve()
receipts, scratch = packet / 'receipts', packet / 'scratch'
env = os.environ.copy()
env.update(VERILATOR=str(scratch / 'bounded-simulator'), TMPDIR=str(scratch), MAKEFLAGS='-j16')

def masked():
    tree = scratch / 'masked-integrated'
    tree.mkdir(exist_ok=True)
    with tarfile.open(scratch / 'source.tar') as t:
        t.extractall(tree, filter='data')
    patch = root / 'tb/srp_top/mutations/lv-expiry-masked.patch'
    for args in [['--check'], []]:
        subprocess.run(['git', 'apply', *args, str(patch)], cwd=tree, check=True)
    with (receipts / 'masked-integrated.log').open('w') as log:
        r = subprocess.run(['make', '-j16', '-C', 'tb/srp_top', 'run', 'RUN_ARGS=lvcoll'],
                           cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT)
    (receipts / 'masked-integrated.rc').write_text(str(r.returncode) + '\n')
    text = (receipts / 'masked-integrated.log').read_text()
    failures = [line for line in text.splitlines() if line.startswith('FAIL:')]
    ok = r.returncode == 2 and len(failures) == 16 and all('SC2:' in line for line in failures)
    print('Integrated reverse-order mutant: expected red, rc=%d, failures=%d, verified=%s'
          % (r.returncode, len(failures), ok), flush=True)
    return ok

def patch_audit():
    patches = sorted((root / 'tb/srp_top/mutations').glob('*.patch'))
    patches.append(root / 'tb/pp_top/ctr_mutations/ctr-notify-one-window.patch')
    failures = 0
    with (receipts / 'patch-planting.log').open('w') as log:
        for patch in patches:
            r = subprocess.run(['git', 'apply', '--check', str(patch)], cwd=root,
                               text=True, capture_output=True)
            log.write('%s rc=%d\n%s%s' % (patch.relative_to(root), r.returncode, r.stdout, r.stderr))
            failures += r.returncode != 0
        log.write('PATCH_PLANTING %d checks, %d failures\n' % (len(patches), failures))
    (receipts / 'patch-planting.rc').write_text(str(int(bool(failures))) + '\n')
    print('Patch planting: %d checks, %d failures' % (len(patches), failures), flush=True)
    return not failures

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(lambda f: f(), [masked, patch_audit]))
raise SystemExit(not all(results))
