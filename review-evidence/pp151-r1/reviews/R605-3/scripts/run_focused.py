#!/usr/bin/env python3
"""Foreground orchestration of concurrent, bounded review checks; no detached jobs."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('root', type=Path)
    p.add_argument('packet', type=Path)
    p.add_argument('--verilator', default='verilator')
    args = p.parse_args()
    root, packet = args.root.resolve(), args.packet.resolve()
    env = dict(os.environ, TMPDIR=str(packet / 'scratch'), PYTHONDONTWRITEBYTECODE='1',
               VERILATOR=args.verilator)
    docs = packet / 'scratch/docs-checkout'
    subprocess.run(['git', 'clone', '--quiet', '--shared', '--no-checkout', str(root), str(docs)], check=True)
    subprocess.run(['git', '-C', str(docs), 'checkout', '--quiet', '--detach',
                    '02063dc1b593d422406991bf0bc60e5cc47828ff'], check=True)
    py = sys.executable
    sources = sorted(root.glob('hdl/**/*_pkg.sv'))
    sources += sorted(x for x in root.glob('hdl/**/*.sv') if not x.name.endswith('_pkg.sv'))
    jobs = [
        ('guards', [py, '-B', 'tb/elab_guards/guards.py', '--frontend', 'verilator',
                    '--frontend', 'yosys', '--verilator', args.verilator, '--jobs', '2'], root),
        ('mutants', [py, '-B', 'tb/elab_guards/mutants.py', '--frontend', 'verilator',
                     '--verilator', args.verilator, '--jobs', '4', '--output',
                     str(packet / 'receipts/mutant-logs')], root),
        ('docs', ['make', '-j16', 'check'], docs),
    ]
    legacy = [
        ('nvm-bounds', ['bash', 'tb/nvm_port/elab_bounds.sh'], root),
        ('if-guards', [py, '-B', 'tb/pp_top/if_guards.py', '--verilator', args.verilator,
                       '--', *map(str, sources)], root),
        ('line-guards', [py, '-B', 'tb/pp_top/line_guards.py', '--verilator', args.verilator,
                         '--', *map(str, sources)], root),
    ]
    def run(job):
        name, cmd, cwd = job
        stem = packet / 'receipts' / name
        stem.with_suffix('.cmd.json').write_text(json.dumps({'argv': cmd, 'cwd': str(cwd),
                                                            'TMPDIR': env['TMPDIR']}, indent=2) + '\n')
        start = time.monotonic()
        with stem.with_suffix('.log').open('w') as out:
            rc = subprocess.run(cmd, cwd=cwd, env=env, stdout=out, stderr=subprocess.STDOUT).returncode
        stem.with_suffix('.rc').write_text(str(rc) + '\n')
        stem.with_suffix('.seconds').write_text(f'{time.monotonic()-start:.3f}\n')
        print(f'{name}: rc={rc}', flush=True)
        return rc
    def run_legacy():
        return max(run(job) for job in legacy)
    with ThreadPoolExecutor(4) as pool:
        futures = [pool.submit(run, job) for job in jobs] + [pool.submit(run_legacy)]
        codes = [f.result() for f in futures]
    return int(any(codes))


if __name__ == '__main__':
    raise SystemExit(main())
