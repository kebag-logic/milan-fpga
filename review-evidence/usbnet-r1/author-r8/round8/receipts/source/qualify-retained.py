"""Qualify the regraded census at the separate USB ledger point, without changing measured data."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent.parent
OLD = OUT.parent.parent / 'round7/receipts'
RESULTS = Path('$VALIDATION_STORAGE/usbnet-a855/round8/census')
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import arty_grade
import egress_ledger as ledger

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
manifest = json.loads((OLD / 'census/manifest.json').read_text())
traces = json.loads((OUT / 'retained-trace-identity.json').read_text())
grades = json.loads((OUT / 'regraded-identity.json').read_text())
regrades = json.loads((OUT / 'regrade-commands.json').read_text())
assert len(regrades) == 8 and all(r['returncode'] == 0 for r in regrades)
assert len(grades) == len(traces) == 159 and {r['case'] for r in grades} == {r['case'] for r in traces}
paths = [RESULTS / v / 'results' for v in manifest['groups']]
commands = []

def command(name, arguments, expected=0):
    path = OUT / (name + '.log')
    argv = [sys.executable, '-I', '-B', *map(str, arguments)]
    with path.open('w') as log:
        proc = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT)
    text = path.read_text()
    commands.append(dict(name=name, head=head, command=argv, returncode=proc.returncode,
                         expected=expected, log=path.name, log_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    (OUT / 'qualification-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    assert proc.returncode == expected, (name, proc.returncode, text[-5000:])
    return text

command('record-classes', ['tb/verilator/ctrl_service_budget/record_classes.py', *paths])
command('egress-ledger', ['tb/verilator/ctrl_service_budget/egress_ledger.py', '--point', 'arty-usbnet-1x1', *paths])
negative = command('original-arty-negative', ['tb/verilator/ctrl_service_budget/egress_ledger.py',
                   '--point', 'arty-1x1', *paths], expected=1)
assert '62.03635 ms, over its ledger figure 61.99 ms by 0.04635 ms' in negative
assert len([line for line in negative.splitlines() if line.startswith('- ')]) == 1

source = RESULTS / 'none/results/backlog-owed.json'
original = json.loads(source.read_text())
controls = []
for name, cycles, expected in [('usb-at-figure', 4971200, 0), ('usb-one-cycle-over', 4971201, 1)]:
    fixture = OUT / 'controls' / name
    fixture.mkdir(parents=True, exist_ok=True)
    grade = copy.deepcopy(original)
    for probe in grade['probes']:
        if probe['probe'] == 'backlog-owed.service.aecp.last.if0':
            probe.update(sys_cycles=cycles, cpu_cycles=cycles, ms=round(cycles / 80_000, 5),
                         end_sys=probe['start_sys'] + cycles)
    (fixture / 'backlog-owed.json').write_text(json.dumps(grade, indent=1) + '\n')
    shutil.copyfile(RESULTS / 'none/results/results.json', fixture / 'results.json')
    text = command(name, ['tb/verilator/ctrl_service_budget/egress_ledger.py', '--point', 'arty-usbnet-1x1', fixture], expected)
    if expected:
        assert '62.14001 ms, over its ledger figure 62.14 ms' in text
        assert len([line for line in text.splitlines() if line.startswith('- ')]) == 1
    controls.append(dict(name=name, cycles=cycles, cpu_hz=80_000_000, returncode=expected,
                         source_grade_sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
(OUT / 'boundary-controls.json').write_text(json.dumps(controls, indent=2) + '\n')

instances, read_findings, logs = ledger.read(paths)
findings = read_findings + ledger.findings(instances, 'arty-usbnet-1x1', logs)
assert not findings, findings
model, owner_findings = arty_grade.inspect(ROOT)
old = json.loads((OLD / 'census/qualification.json').read_text())
assert not owner_findings and model == old['model']
wire = json.loads((OUT / 'egress-evidence-identity.json').read_text())
assert wire['status'] == 'PASS'
for variant in manifest['groups']:
    dest = OUT / 'census' / variant / 'results'
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RESULTS / variant / 'build.json', dest.parent / 'build.json')
    for path in (RESULTS / variant / 'results').iterdir():
        if path.suffix in ('.json', '.txt', '.status', '.md') or 'journal' in path.name:
            shutil.copyfile(path, dest / path.name)
rows = {}
for name, figure in ledger.LEDGER['arty-usbnet-1x1'].items():
    ms = max(p['ms'] for p in instances if p['probe'] == name and p['group'] == ledger.GROUP)
    rows[name] = dict(measured_ms=ms, ledger_ms=figure, margin_ms=round(figure - ms, 5))
record = dict(status='PASS', head=head, ledger_point='arty-usbnet-1x1', measurement_point='arty-1x1',
    groups=159, images=8, raw_traces_unchanged=True, measured_grades_identical=True, native_rerun=False,
    checks={name:'PASS' for name in ('owner-model','share','record-classes','retry-costs','transmit-costs',
                                   'egress-ledger','egress-100')},
    findings=findings + owner_findings, model=model, worst_pass=old['worst_pass'],
    held_egress_rows=rows, commands=commands, owed_969=old['owed_969'],
    note='Seven held-egress rows remain service-budget misses, within the separate ruled ledger. '
         'Wire replay evidence is carried after exact trace, source and parameter verification.')
(OUT / 'qualification.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
