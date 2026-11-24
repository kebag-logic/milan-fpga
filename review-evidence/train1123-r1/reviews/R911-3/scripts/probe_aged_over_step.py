"""Probe the kind filter in kept_grade.transmit_slices (`o['kind'] in BOUND_OWED_BUILDS`): an aged step in srp-bound
over both the slice and its stated step cost, which whole_grade.held puts in 'over' as kind 'step'.

usage: python3 -I -B probe_aged_over_step.py <repo-root>
Prints, at the head and with the kind filter removed (in-memory), the slice line's disposition and the lines that
still fail; uses the harness's own Synthetic logs at 1x1/1if.
"""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import kept_grade  # noqa: E402
import kept_window  # noqa: E402
import run  # noqa: E402
import scenario  # noqa: E402
import slice_grade  # noqa: E402
import whole_grade  # noqa: E402

s = kept_grade.Synthetic()
srp = scenario.CH['srp']
w0 = whole_grade.held(grade.parse('', s.hz, s.hz), s.shape)['limits']
cyc = max(s.slice, w0['step']) + 1
extra = (f'PASS 1 9500000 9500000 {cyc} step=1 aged=1', 'ENTRY 9500010 build_mrpdu', f'TXC 9500020 {srp} 0')


def no_kind_filter(log, shape):
    ones = {o['start_sys'] for o in whole_grade.held(log, shape)['over']}
    out = {'build': set(), 'build-one': set()}
    for o in slice_grade.held(log, shape)['over']:
        if o['kind'] == 'build':
            out['build-one' if o['start_sys'] in ones else 'build'].add(o['cycles'])
    return out


print(f'1x1/1if: slice {s.slice:,}, step {w0["step"]:,}; aged step pass of {cyc:,} with one build and one SRP frame')
for label, fn in (('head', kept_grade.transmit_slices), ('no-kind-filter', no_kind_filter)):
    saved = kept_grade.transmit_slices
    kept_grade.transmit_slices = fn
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            for name, body in s.texts(*s.clean, bound_extra=extra).items():
                (out / f'{name}.log').write_text(body)
            logs = {n: grade.parse((out / f'{n}.log').read_text(), s.hz, s.hz) for n in kept_grade.OWED_KINDS}
            lines = run.stated_misses([dict(group=n, passes=dict(slices=slice_grade.held(logs[n], s.shape),
                                                                 stated=whole_grade.held(logs[n], s.shape)))
                                       for n in kept_grade.OWED_KINDS])
            d = kept_grade.Disposition([dict(group=n) for n in kept_grade.OWED_KINDS], out, s.spec)
            left = d.stated(list(lines))
    finally:
        kept_grade.transmit_slices = saved
    print(f'--- {label}: whole_grade over '
          f'{[(o["kind"], o["cycles"]) for o in whole_grade.held(logs[kept_window.BOUND], s.shape)["over"]]}; '
          f'transmit_slices {d.slices}')
    print('  STATED:', lines)
    print('  findings:', d.findings)
    print('  still failing:', left)
    print(f'RESULT {label}: slice line', 'FAILS' if any(kept_grade.TRANSMIT_SLICE in x for x in left) else 'OWED',
          f'; run fails: {bool(left)}')
