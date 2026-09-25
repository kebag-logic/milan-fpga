#!/usr/bin/env python3
"""R324 probe driver: run the PR's own harness functions in resumable steps.

Usage (after `. probe_env.sh`), from a repository copy root:
  python3 probe_step.py elaborate --shape S --captures N --build-dir D
  python3 probe_step.py verilate  --build-dir D     # verilator --cc --exe, no --build
  python3 probe_step.py make      --build-dir D     # resumable; rerun until it reports DONE
  python3 probe_step.py simulate  --build-dir D     # runs Vsim and grades with run._grade
Every step calls the harness code at tb/verilator/nvm_capture_cpu unchanged; only
the single `verilator --build` call is split so that a compile can resume.
"""
import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
HARNESS = ROOT / 'tb/verilator/nvm_capture_cpu'
sys.path.insert(0, str(HARNESS))
import run  # noqa: E402  (the PR's harness module, unmodified)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('step', choices=['elaborate', 'verilate', 'make', 'simulate'])
    parser.add_argument('--shape')
    parser.add_argument('--captures', type=int, default=2)
    parser.add_argument('--mutation', default='none')
    parser.add_argument('--build-dir', type=Path, required=True)
    args = parser.parse_args()
    args.build_dir = args.build_dir.resolve()
    if args.step == 'elaborate':
        from soc import build
        build(args)
        print('ELABORATED', args.build_dir)
        return
    spec = json.loads((args.build_dir / 'sources.json').read_text())
    if args.step == 'verilate':
        captured = {}
        original = subprocess.run

        def fake_run(argv, cwd, check):
            argv = [a for a in argv if a != '--build']
            # keep '-j 8' harmless: verilator's -j only affects --build
            captured['argv'] = argv
            print('COMMAND', shlex.join(argv), flush=True)
            return original(argv, cwd=cwd, check=check)
        run.subprocess.run = fake_run
        try:
            run._compile(args.build_dir, spec)
        finally:
            run.subprocess.run = original
        print('VERILATED')
        return
    if args.step == 'make':
        native = args.build_dir / 'native'
        argv = ['make', '-C', str(native), '-f', 'Vsim.mk', '-j', '8', 'Vsim']
        print('COMMAND', shlex.join(argv), flush=True)
        subprocess.run(argv, check=True)
        print('MAKE DONE')
        return
    argv = [str(args.build_dir / 'native/Vsim')]
    print('COMMAND', shlex.join(argv), flush=True)
    with (args.build_dir / 'capture.log').open('w') as log:
        result = subprocess.run(argv, cwd=args.build_dir / 'gateware', stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    print('VSIM_RC', result.returncode, flush=True)
    run._grade(args.build_dir, spec, result.returncode)


if __name__ == '__main__':
    main()
