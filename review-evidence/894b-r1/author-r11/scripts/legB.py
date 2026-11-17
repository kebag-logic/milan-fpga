"""One part of a harness arm at a point, on a clean clone (phase B's measurement): build the image as run.py builds it
by default (build.build: CPU regions cover, the split placement's L1, no XIP), construct every group of the arm
(run.all_groups), split them into NPARTS parts balanced by simulated time (longest first, each to the lightest part;
the same split in every part, so the parts together run every group once), write the split to
<build-dir>/parts.txt, and run this part's groups through leg.sh with --reuse-build. GROUPS, if given, runs those
groups instead (comma-separated), with no split.
usage: python3 -B legB.py CLONE BUILD_DIR POINT VARIANT PART NPARTS JOBS [GROUPS]"""
import subprocess
import sys
from pathlib import Path

clone, build_dir, point, variant = Path(sys.argv[1]), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
part, nparts, jobs = int(sys.argv[5]), int(sys.argv[6]), sys.argv[7]
chosen = sys.argv[8].split(',') if len(sys.argv) > 8 else None
sys.path.insert(0, str(clone / 'tb/verilator/ctrl_service_budget'))
import build as builder  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402

shape, n_if = run.POINTS[point]
spec = builder.build(build_dir, shape, n_if, mutation='none', variant=variant,
                     core=builder.Core('cover', 'split', False))
groups = run.all_groups(scenario.point(point, spec), spec)
if chosen:
    known = {g.name for g in groups}
    assert set(chosen) <= known, f'groups the arm does not make: {sorted(set(chosen) - known)}'
    mine = chosen
else:
    bins = [[0.0, []] for _ in range(nparts)]
    for g in sorted(groups, key=lambda g: (-g.sim_ms, g.name)):
        lightest = min(bins, key=lambda b: b[0])
        lightest[0] += g.sim_ms
        lightest[1].append(g.name)
    (build_dir / 'parts.txt').write_text(''.join(f'part {k}: {b[0]:.0f} ms simulated, {len(b[1])} groups: '
                                                 f'{",".join(b[1])}\n' for k, b in enumerate(bins)))
    mine = bins[part][1]
print(f'# {point} {variant}: {len(groups)} groups in the arm; part {part} of {nparts} runs {len(mine)}', flush=True)
args = ['bash', '/data-2/milan/tmp/894b-a781/scripts/leg.sh', str(clone), str(build_dir), point, jobs, '--reuse-build',
        '--groups', ','.join(mine)] + ([] if variant == 'none' else ['--variant', variant])
sys.exit(subprocess.run(args).returncode)
