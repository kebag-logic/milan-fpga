"""Controls of round 4's acceptance gate (gate_r4.py), each its own process whose exit status is the verdict:
the unchanged ledger (each held-egress row at its ledger figure) passes; for each of the seven rows, one bus cycle over
its figure and a large increase each exit nonzero naming the row; R844-1's two probe inputs (backlog.owed.if0 at
100.0 ms; an unmeasured instance beside the seven) each exit nonzero; and the log-alone form passes the published
figures and fails a row printed one microsecond over its figure. One line a control; exit 1 when any does not hold.
usage: python3 -I gate_controls.py CHECKOUT GATE SCRATCH"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

checkout, gate, scratch = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import egress_ledger  # noqa: E402

LEDGER = egress_ledger.LEDGER['8x8-1if']
PUBLISHED = egress_ledger.doc_ledger(egress_ledger.DOC.read_text())[1]
shutil.rmtree(scratch, ignore_errors=True)
scratch.mkdir(parents=True)
bad = []


def leg(name: str, figures: dict, extra: list | None = None) -> str:
    """A leg directory of one backlog-owed grade (its form in R844-1's probe), each row at its figure."""
    d = scratch / name / 'results'
    d.mkdir(parents=True)
    probes = [dict(probe=n, ms=round(ms, 5), budget_ms=20, within_budget=False, status='measured', path=['owed'],
                   family='acmp') for n, ms in figures.items()] + (extra or [])
    (d / 'backlog-owed.json').write_text(json.dumps(dict(group='backlog-owed', probes=probes, passes={})))
    return str(scratch / name)


def log(name: str, figures: dict) -> str:
    """A leg's log alone: its BUDGET lines, its summary and its END line."""
    path = scratch / f'{name}.log'
    path.write_text('\n'.join([*(f'BUDGET {n}: {ms:.3f} ms over its budget 20 ms' for n, ms in figures.items()),
                               f'22 groups graded, 0 refusals, {len(figures)} budget misses (7 of 213 probe instances, '
                               '4 of 24 paths)', 'END rc=0 2026-11-15T00:00:00']) + '\n')
    return f'-:{path}'


def control(name: str, args: list[str], want_rc: int, row: str | None = None) -> None:
    r = subprocess.run([sys.executable, '-I', str(gate), str(checkout), *args], capture_output=True, text=True)
    out = r.stdout + r.stderr
    result = next((l for l in out.splitlines() if l.startswith('RESULT')), 'no RESULT line')
    named = row is None or any(l.startswith('- the ledger: ' + row) for l in out.splitlines())
    held = (r.returncode == want_rc if want_rc == 0 else r.returncode != 0) and named
    lines = [l for l in out.splitlines() if l.startswith('- the ledger:')]
    print(f"{'PASS' if held else 'FAIL'} {name}: exit {r.returncode}; {result}" + (f'; {lines[0]}' if lines else ''))
    if not held:
        bad.append(name)


control('the unchanged ledger, every row at its figure', [leg('at-ledger', LEDGER)], 0)
control("section 13's published measurement", [leg('published', PUBLISHED)], 0)
for k, row in enumerate(LEDGER):
    control(f'{row}: one bus cycle over its figure', [leg(f'cycle-{k}', {**LEDGER, row: LEDGER[row] + 1e-5})], 1, row)
    control(f'{row}: a large increase', [leg(f'large-{k}', {**LEDGER, row: LEDGER[row] + 36.76})], 1, row)
control("R844-1's larger-egress input (backlog.owed.if0 at 100.0 ms)",
        [leg('r844-larger', {**LEDGER, 'backlog.owed.if0': 100.0})], 1, 'backlog.owed.if0')
control("R844-1's unmeasured input (a required row not measured beside the seven)",
        [leg('r844-unmeasured', LEDGER, [dict(probe='required.cpu.row', status='unmeasured')])], 1, 'required.cpu.row')
control('a leg by its log alone, the published figures', [log('log-published', PUBLISHED)], 0)
control('a leg by its log alone, a row printed 1 us over its figure',
        [log('log-over', {**PUBLISHED, 'backlog.owed_behind3.if0': LEDGER['backlog.owed_behind3.if0'] + 0.001})], 1,
        'backlog.owed_behind3.if0')
print('RESULT:', 'FAIL ' + ', '.join(bad) if bad else f'PASS: every control held')
sys.exit(1 if bad else 0)
