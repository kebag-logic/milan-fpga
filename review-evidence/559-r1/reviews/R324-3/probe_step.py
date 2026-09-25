#!/usr/bin/env python3
"""R324-3 probe driver: run the PR's own harness functions in bounded steps.

Round-1 driver plus the head's two new harness arguments (--cpu-hz, --traffic).
Usage (after `. probe_env.sh`), from a repository copy root:
  python3 probe_step.py build    --shape S --captures N --cpu-hz H --traffic T --build-dir D
      (soc.build + run._compile without --build, then make -f Vsim.mk; this is
       the committed run.py --build-only path with the build split in two)
  python3 probe_step.py simulate --build-dir D   (runs Vsim; grades with run._grade)
The harness modules under tb/verilator/nvm_capture_cpu are imported unchanged.
"""
import argparse
import hashlib
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
HARNESS = ROOT / 'tb/verilator/nvm_capture_cpu'
sys.path.insert(0, str(HARNESS))
import run  # noqa: E402  (the PR's harness module, unmodified)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=['build', 'simulate'])
    parser.add_argument('--shape')
    parser.add_argument('--captures', type=int, default=16)
    parser.add_argument('--cpu-hz', type=int, default=50_000_000)
    parser.add_argument('--traffic', choices=['on', 'off'], default='on')
    parser.add_argument('--mutation', default='none')
    parser.add_argument('--build-dir', type=Path, required=True)
    args = parser.parse_args()
    args.build_dir = args.build_dir.resolve()
    t0 = time.monotonic()
    if args.step == 'build':
        from soc import build
        build(args)
        spec = json.loads((args.build_dir / 'sources.json').read_text())
        # As in round 1: the scoped Verilator wrapper cannot re-exec itself for
        # --build, so verilate without it (argv otherwise unchanged), then make.
        original = subprocess.run

        def no_build(argv, cwd, check):
            argv = [a for a in argv if a != '--build']
            print('COMMAND', shlex.join(argv), flush=True)
            return original(argv, cwd=cwd, check=check)
        run.subprocess.run = no_build
        try:
            run._compile(args.build_dir, spec)
        finally:
            run.subprocess.run = original
        make = ['make', '-C', str(args.build_dir / 'native'), '-f', 'Vsim.mk', '-j', '8', 'Vsim']
        print('COMMAND', shlex.join(make), flush=True)
        subprocess.run(make, check=True)
        fw = args.build_dir / 'measurement_firmware/milan_baremetal.c'
        print('INSTRUMENTED_FIRMWARE_SHA256', hashlib.sha256(fw.read_bytes()).hexdigest())
        print('BUILT', args.build_dir, f'{time.monotonic() - t0:.1f}s', flush=True)
        return
    spec = json.loads((args.build_dir / 'sources.json').read_text())
    argv = [str(args.build_dir / 'native/Vsim')]
    print('COMMAND', shlex.join(argv), flush=True)
    with (args.build_dir / 'capture.log').open('w') as log:
        result = subprocess.run(argv, cwd=args.build_dir / 'gateware', stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    print('VSIM_RC', result.returncode, f'{time.monotonic() - t0:.1f}s', flush=True)
    run._grade(args.build_dir, spec, result.returncode)


if __name__ == '__main__':
    main()
