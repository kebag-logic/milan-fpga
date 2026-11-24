"""Probe: is a pass srp-bound gives whole to THE TRANSMIT's build (two MRPDUs), over the tier-2 slice but within
CTRL_LOOP_BUILD_PASS_US, owed to #977 by kept_grade.Disposition, where #969's amendment owes the build of one only?

usage: python3 -I -B probe_whole_slice.py <repo-root>
Uses the harness's own Synthetic logs (1x1/1if, 100 MHz), slice_grade.held and run.stated_misses, so the STATED line
graded is the one run.py prints. A control repeats it in srp-kept, and a second control with a build of one.
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
limits = whole_grade.held(grade.parse('', s.hz, s.hz), s.shape)['limits']
slice_limit = slice_grade.held(grade.parse('', s.hz, s.hz), s.shape)['limit']
cycles = (slice_limit + limits['build']) // 2
srp = scenario.CH['srp']
whole = (f'PASS 1 9500000 9500000 {cycles}', 'ENTRY 9500010 build_mrpdu', f'TXC 9500020 {srp} 0',
         f'TXC 9500030 {srp} 0')
print(f'1x1/1if: slice {slice_limit:,}, CTRL_LOOP_BUILD_PASS_US {limits["build"]:,}, build of one '
      f'{limits["build-one"]:,} CPU cycles; probe pass {cycles:,} with two SRP frames')
verdicts = []
for target in (kept_window.BOUND, kept_window.NAME):
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        extra = dict(bound_extra=whole) if target == kept_window.BOUND else dict(kept_extra=whole)
        for name, body in s.texts(*s.clean, **extra).items():
            (out / f'{name}.log').write_text(body)
        logs = {n: grade.parse((out / f'{n}.log').read_text(), s.hz, s.hz) for n in kept_grade.OWED_KINDS}
        w = whole_grade.held(logs[target], s.shape)
        sl = slice_grade.held(logs[target], s.shape)
        results = [dict(group=n, passes=dict(slices=slice_grade.held(logs[n], s.shape),
                                             stated=whole_grade.held(logs[n], s.shape)))
                   for n in kept_grade.OWED_KINDS]
        lines = run.stated_misses(results)
        d = kept_grade.Disposition([dict(group=n) for n in kept_grade.OWED_KINDS], out, s.spec)
        left = d.stated(list(lines))
        print(f'--- {target}: whole_grade kinds over {[o["kind"] for o in w["over"]]}, heaviest build '
              f'{w["heaviest"]["build"]:,}; slices over {[(o["kind"], o["cycles"]) for o in sl["over"]]}')
        print('  STATED lines run.py prints:', lines)
        print('  kept_grade findings:', d.findings)
        print('  OWED:', d.owed)
        print('  still failing:', left)
        verdicts.append((target, bool(d.owed) and not left))
for target, owed in verdicts:
    print(f'RESULT {target}: the whole build pass\'s slice line is', 'OWED (fails nothing)' if owed else
          'a failure')
