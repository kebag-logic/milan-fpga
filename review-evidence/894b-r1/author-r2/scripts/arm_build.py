"""Build a harness arm at a point and construct its groups without running any (phase A: build only): the image as
run.py builds it (build.build), then run.all_groups on its spec, which refuses the answering-every-port arm where the
image's model holds another count of notices than AECP_NOTICES_MOST at its shape (notice_window.every_group). Prints
the build's figures, each group's name and probe count, and for the every-port arm the notices the model holds
against AECP_NOTICES_MOST; writes each group's script to <build-dir>/scripts.
usage: python3 -B arm_build.py TREE BUILD_DIR POINT VARIANT"""
import hashlib
import sys
from pathlib import Path

tree, build_dir, point, variant = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build as builder  # noqa: E402
import notice_window  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402

shape, n_if = run.POINTS[point]
spec = builder.build(build_dir.resolve(), shape, n_if, mutation='none', variant=variant,
                     core=builder.Core('cover', 'split', False))
elf = Path(spec['elf'])
print(f'# arm {variant} at {point} ({shape}, {n_if} interface(s)), built at the tree\'s head; no group run')
print(f"BUILT {elf.name} sha256 {hashlib.sha256(elf.read_bytes()).hexdigest()}, executable sha256 "
      f"{spec.get('executable_sha256')}, CLOCK {builder.clock_line(spec)}")
if variant == 'answering-every-port':
    print(f'NOTICES the model holds {len(notice_window.every_notice(spec))}, AECP_NOTICES_MOST at the build\'s shape '
          f'{notice_window.notices_most(spec)}')
groups = run.all_groups(scenario.point(point, spec), spec)
scripts = build_dir / 'scripts'
scripts.mkdir(parents=True, exist_ok=True)
for g in groups:
    (scripts / f'{g.name}.txt').write_text(g.script())
    queued = sum(1 for p in g.probes if p.path_key()[0] == notice_window.QUEUED)
    print(f'GROUP {g.name}: {len(g.probes)} probes, {queued} queued notices, {len(g.steps)} steps')
print(f'{len(groups)} groups constructed, none run')
