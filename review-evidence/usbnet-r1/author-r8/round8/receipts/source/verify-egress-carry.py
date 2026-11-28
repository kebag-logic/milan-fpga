"""Revalidate all retained wire replay bindings and the unchanged wire verdict."""
import dataclasses
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent.parent
OLD = OUT.parent.parent / 'round7/receipts'
sys.path.insert(0, str(ROOT / 'tb/verilator/usbnet'))
import egress_grade as g

p = g.usb.base.params(g.usb.base.arty_spec())
traces = {r['case']: r for r in json.loads((OUT / 'retained-trace-identity.json').read_text())}
sources = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in (
    'tb/verilator/usbnet/egress_usb.py', 'tb/verilator/usbnet/egress_grade.py',
    'tb/verilator/ctrl_service_budget/egress_mii.py', 'tb/verilator/ctrl_service_budget/grade.py')}
frozen = dict(sources=sources, params=dataclasses.asdict(p))
results, bindings = {}, []
paths = sorted((OLD / 'egress-cases').glob('*/*.json'))
assert len(paths) == len(traces) == 159
for path in paths:
    row = json.loads(path.read_text())
    key = '/'.join(row['case'])
    assert key == path.parent.name + '/' + path.stem
    assert row['trace_sha256'] == traces[key]['sha256']
    assert json.dumps(row['inputs'], sort_keys=True) == json.dumps(frozen, sort_keys=True)
    results[key] = row['result']
    bindings.append(dict(case=key, trace_sha256=row['trace_sha256'],
                         replay_receipt_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
assert set(results) == set(traces)
ok, lines = g.verdict(results, p)
wait = max(r['wait_ps'] for r in results.values())
total = ((wait + g.usb.base.gptp_wire_ps(p)) * g.usb.base.MARGIN + g.usb.HANDSHAKE_PS) / 1_000_000
total += g.usb.base.MII_FIXED_NS / 1000
record = dict(status='PASS' if ok else 'FAIL', mode='retained replay binding verification; no fresh wire replay',
              sources=frozen, cases=bindings, wait_us=wait / 1_000_000, total_us=total, bound_us=1000,
              verdict=lines)
(OUT / 'egress-evidence-identity.json').write_text(json.dumps(record, indent=2) + '\n')
print('\n'.join(lines))
print('RESULT:', 'PASS' if ok else 'FAIL', '159 retained replay receipts bound to unchanged inputs')
raise SystemExit(not ok)
