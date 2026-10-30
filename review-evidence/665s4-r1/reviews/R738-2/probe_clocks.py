"""Reproduce clock provenance checks on immutable receipts and repeated output use.

Run from the reviewed checkout after verify_public.py.
"""
import contextlib
import copy
import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path.cwd()
PACKET = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tb/verilator/nvm_split_target'))
import target_selftest as st

run = st.RUN
public = PACKET / 'scratch/public/author-r3/receipts'
for point in ('1x1', '8x8'):
    rec = json.loads((public / f'target-{point}/results.json').read_text())
    assert (rec['cpu_hz'], rec['sys_hz']) == (50_000_000, 100_000_000)
    assert not run.provenance(rec)
    report = run.table(rec)
    assert report == (public / f'target-{point}/table.md').read_text()
    assert report.count('Clocks, as') == 3
    for row in rec['results']:
        for label, cycles, value in run.figures(row):
            assert value == cycles / 50_000, (point, label)
    print(f'PASS: {point} published figures independently convert at 50 MHz; 3 tables reproduce byte-for-byte')
    for key in ('cpu_hz', 'sys_hz'):
        missing = copy.deepcopy(rec)
        del missing[key]
        assert run.provenance(missing) == [f'no {key} recorded']
    assert run.provenance(dict(rec, cpu_hz=100_000_000))
    print(f'PASS: {point} missing clocks and relabelled 100 MHz refused')

other = st.graded_record(62_500_000, 125_000_000)
(PACKET / 'synthetic-62_5MHz-table.md').write_text(run.table(other))
assert run.table(other).count('CPU 62.5 MHz (62,500,000 Hz), bus 125 MHz (125,000,000 Hz)') == 3
print('PASS: differently clocked synthetic input renders 62.5/125 MHz at all 3 tables')

# A successful run followed by a provenance failure in the same supported --out.
# Only the expensive producer is replaced, exactly as the built-in main_run does.
out = PACKET / 'scratch/repeated-output'
out.mkdir(parents=True, exist_ok=True)
def built(*args):
    return dict(cpu_hz=62_500_000, sys_hz=125_000_000)
def cases(*args):
    return st.graded_commit(62_500_000, 125_000_000)
argv = ['--point', '1x1', '--jobs', '1', '--build-dir', str(out)]
with patch.object(run, 'built', built), patch.object(run, 'run_cases', cases), contextlib.redirect_stdout(io.StringIO()):
    good = run.main(argv)
    before = (out / 'results/table.md').read_bytes()
    with patch.object(run, 'clocks', lambda specs: dict(cpu_hz=50_000_000, sys_hz=100_000_000)):
        bad = run.main(argv)
    after = (out / 'results/table.md').read_bytes()
    invalid = json.loads((out / 'results/results.json').read_text())
assert good == 0 and bad == 2
assert before == after
assert invalid['cpu_hz'] == 50_000_000
print('OBSERVED: successful run rc=0; wrong-build-clock rerun rc=2; previous table remains byte-identical')
print('OBSERVED: retained table says 62.5/125 MHz; replaced results.json says 50/100 MHz')
print('OBSERVED: built-in main_run uses a new TemporaryDirectory per invocation, so does not test this case')
