#!/usr/bin/env python3
"""The composed image's CPU budget legs, one build per (point, variant) and its parts reusing it.

  legs.py build CLONE BUILD POINT VARIANT NPARTS [GROUPS]
      builds the image, SoC and native model as run.py builds them by default (build.build: CPU regions cover, the
      split placement's L1, no XIP), then splits the arm's groups (run.all_groups, or GROUPS, comma-separated) into
      NPARTS parts balanced by simulated time (longest first, each to the lightest part) into BUILD/parts.json.
  legs.py run CLONE BUILD POINT VARIANT PART JOBS
      waits for BUILD/parts.json, then runs that part's groups with run.py --reuse-build --out BUILD/part<PART>,
      recording budget and share findings (the formal measurement's options), and exits with run.py's status.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

mode, clone, build_dir, point, variant = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]).resolve(), sys.argv[4], \
    sys.argv[5]
harness = clone / 'tb/verilator/ctrl_service_budget'
parts_json = build_dir / 'parts.json'

if mode == 'build':
    nparts = int(sys.argv[6])
    chosen = sys.argv[7].split(',') if len(sys.argv) > 7 else None
    sys.path.insert(0, str(harness))
    import build as builder  # noqa: E402
    import run  # noqa: E402
    import scenario  # noqa: E402
    shape, n_if = run.POINTS[point]
    print(f'BUILD {point} {variant} at {subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()} start {time.strftime("%H:%M:%S")}', flush=True)
    spec = builder.build(build_dir, shape, n_if, mutation='none', variant=variant,
                         core=builder.Core('cover', 'split', False))
    groups = run.all_groups(scenario.point(point, spec), spec)
    if chosen:
        known = {g.name for g in groups}
        missing = sorted(set(chosen) - known)
        assert not missing, f'groups the arm does not make: {missing}'
        groups = [g for g in groups if g.name in chosen]
    bins = [[0.0, []] for _ in range(nparts)]
    for g in sorted(groups, key=lambda g: (-g.sim_ms, g.name)):
        lightest = min(bins, key=lambda b: b[0])
        lightest[0] += g.sim_ms
        lightest[1].append(g.name)
    parts_json.write_text(json.dumps({'point': point, 'variant': variant, 'groups': len(groups),
                                      'parts': [{'sim_ms': round(b[0]), 'groups': b[1]} for b in bins]}, indent=1))
    print(f'BUILT {len(groups)} groups in {nparts} parts; end {time.strftime("%H:%M:%S")}', flush=True)
    sys.exit(0)

part, jobs = int(sys.argv[6]), sys.argv[7]
deadline = time.time() + 3 * 3600
while not parts_json.is_file():
    if time.time() > deadline:
        sys.exit('no build')
    time.sleep(30)
mine = json.loads(parts_json.read_text())['parts'][part]['groups']
if not mine:
    print('this part has no groups')
    sys.exit(0)
args = [sys.executable, '-B', str(harness / 'run.py'), '--point', point, '--build-dir', str(build_dir),
        '--reuse-build', '--out', str(build_dir / f'part{part}'), '--groups', ','.join(mine),
        '--record-budget-findings', '--record-share-findings', '--jobs', jobs]
if variant != 'none':
    args += ['--variant', variant]
print('COMMAND', ' '.join(args), f'start {time.strftime("%H:%M:%S")}', flush=True)
rc = subprocess.run(args).returncode
print(f'END rc={rc} {time.strftime("%H:%M:%S")}', flush=True)
sys.exit(rc)
