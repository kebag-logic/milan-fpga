"""Probe kept_grade.Disposition.owes on srp-bound's THE TRANSMIT slice lines at edges the self-test does not plant.

usage: python3 -I -B probe_owes_edges.py <repo-root>
Uses the harness's own Synthetic logs (1x1/1if, 100 MHz), slice_grade.held, whole_grade.held and run.stated_misses.
Cases, each in srp-bound, each pass one cycle-count apart from the slice so its line is distinct:
  idle-one    a build pass with one SRP frame whose round was idle (the self-test's case; control)
  busy-one    the same pass whose round did AECP work (mods=aecp:5000), which whole_grade.held does not class a
              build of one (round_idle false), so run.py prints no build-one pass line for it
  aged-one    the same pass marked an aged step (step=1 aged=1), which whole_grade.held classes 'step'
  equal       a build of one and a pass given whole to the build of the same length (ambiguous): must fail closed
For each, prints whole_grade's kinds, slice kinds, run.py's STATED lines, owed and still-failing lines.
"""
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import kept_grade  # noqa: E402
import kept_window  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402
import slice_grade  # noqa: E402
import whole_grade  # noqa: E402

s = kept_grade.Synthetic()
srp = scenario.CH['srp']
one = s.slice + 1
whole = s.whole_cycles
cases = {
    'idle-one': (f'PASS 1 9500000 9500000 {one}', 'ENTRY 9500010 build_mrpdu', f'TXC 9500020 {srp} 0'),
    'busy-one': (f'PASS 1 9500000 9500000 {one} x mods=aecp:5000', 'ENTRY 9500010 build_mrpdu',
                 f'TXC 9500020 {srp} 0'),
    'aged-one': (f'PASS 1 9500000 9500000 {one} x step=1 aged=1', 'ENTRY 9500010 build_mrpdu',
                 f'TXC 9500020 {srp} 0'),
    'equal': (f'PASS 1 9500000 9500000 {whole}', 'ENTRY 9500010 build_mrpdu', f'TXC 9500020 {srp} 0',
              f'PASS 2 9700000 9700000 {whole}', 'ENTRY 9700010 build_mrpdu', f'TXC 9700020 {srp} 0',
              f'TXC 9700030 {srp} 0'),
}
print(f'1x1/1if: slice {s.slice:,}, build-one {s.limits["build-one"]:,}, build {s.limits["build"]:,}')
for label, extra in cases.items():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        for name, body in s.texts(*s.clean, bound_extra=extra).items():
            (out / f'{name}.log').write_text(body)
        logs = {n: grade.parse((out / f'{n}.log').read_text(), s.hz, s.hz) for n in kept_grade.OWED_KINDS}
        w = whole_grade.held(logs[kept_window.BOUND], s.shape)
        sl = slice_grade.held(logs[kept_window.BOUND], s.shape)
        lines = run.stated_misses([dict(group=n, passes=dict(slices=slice_grade.held(logs[n], s.shape),
                                                             stated=whole_grade.held(logs[n], s.shape)))
                                   for n in kept_grade.OWED_KINDS])
        d = kept_grade.Disposition([dict(group=n) for n in kept_grade.OWED_KINDS], out, s.spec)
        left = d.stated(list(lines))
        print(f'--- {label}: whole_grade over {[(o["kind"], o["cycles"]) for o in w["over"]]}; '
              f'slices over {[(o["kind"], o["cycles"]) for o in sl["over"]]}; transmit_slices {d.slices}')
        print('  STATED:', lines)
        print('  findings:', d.findings)
        print('  owed slice lines:', [o for o in d.owed if kept_grade.TRANSMIT_SLICE in o])
        print('  still failing:', left)
        print(f'RESULT {label}: slice line', 'OWED' if not any(kept_grade.TRANSMIT_SLICE in x for x in left)
              else 'FAILS')
