"""The reviewers' named mutants of PR #1026, each a source edit applied in the checkout, run against the in-tree
self-tests, and restored byte for byte; each must make at least one self-test exit nonzero, and the restored tree
must pass. usage: mutants5.py OUT (cwd = checkout root)"""
import hashlib, json, subprocess, sys
from pathlib import Path
T = 'tb/verilator/ctrl_service_budget/'
SELFTESTS = {'egress_mii': [sys.executable, '-I', '-B', T + 'egress_mii.py', '--selftest'],
             'record_classes': [sys.executable, '-I', '-B', T + 'record_classes.py', '--selftest'],
             'egress_ledger': [sys.executable, '-I', '-B', T + 'egress_ledger.py', '--selftest'],
             'egress_fixed': [sys.executable, '-I', '-B', T + 'egress_fixed.py', '--selftest']}
MUTANTS = [
    ('R967 F2 a: sr_frames returns the talkers alone', T + 'egress_mii.py', '    return aaf + crf\n', '    return aaf\n'),
    ('R967 F2 b: CRF_AVTPDU = 0', T + 'egress_mii.py', 'CRF_AVTPDU = 28\n', 'CRF_AVTPDU = 0\n'),
    ('R968 M1: crf = ()', T + 'egress_mii.py',
     "    crf = (SR_HEADER + CRF_AVTPDU,) if (cfg['clocking'].get('crf_output') or {}).get('enabled') else ()\n",
     '    crf = ()\n'),
    ('R968 M8: point_name maps the 4x4 configuration to arty-1x1', T + 'record_classes.py',
     "            'endstation_arty_split_4x4': 'arty-4x4'}", "            'endstation_arty_split_4x4': 'arty-1x1'}"),
    ("R968 M9: poll_grade reads arty-1x1's record.acmp at (1,5,5)", T + 'poll_grade.py',
     "    arty = {shape_costs.Shape(1, 1, 2): 'arty-1x1', shape_costs.Shape(1, 5, 5): 'arty-4x4'}",
     "    arty = {shape_costs.Shape(1, 1, 2): 'arty-1x1', shape_costs.Shape(1, 5, 5): 'arty-1x1'}"),
    ("R968 M10 / R967 S1: ARTY_CLOCKS['arty-4x4'] = 80 MHz", T + 'record_classes.py',
     "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 100_000_000}",
     "ARTY_CLOCKS = {'arty-1x1': 80_000_000, 'arty-4x4': 80_000_000}"),
    ("R967 S2: CLOCK_KHZ['arty-4x4'] = 80,000", T + 'egress_ledger.py',
     "CLOCK_KHZ = {'8x8-1if': 100_000, 'arty-1x1': 80_000, 'arty-4x4': 100_000}",
     "CLOCK_KHZ = {'8x8-1if': 100_000, 'arty-1x1': 80_000, 'arty-4x4': 80_000}"),
    ('R968 S1: SYS_HZ read with no whole-ps check', T + 'egress_fixed.py',
     "    if not text.isdigit() or int(text) <= 0 or 10**12 % int(text):\n",
     "    if not text.isdigit():\n"),
]
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
def run_all(tag):
    rcs = {}
    for name, argv in SELFTESTS.items():
        r = subprocess.run(['nice', '-n', '19', *argv], capture_output=True, text=True)
        (out / f'{tag}-{name}.log').write_text(r.stdout + r.stderr); rcs[name] = r.returncode
    return rcs
rows = []
for k, (name, path, old, new) in enumerate(MUTANTS):
    p = Path(path); before = p.read_bytes(); text = before.decode()
    assert text.count(old) == 1, (name, text.count(old))
    p.write_text(text.replace(old, new))
    try:
        rcs = run_all(f'm{k}')
    finally:
        p.write_bytes(before)
    assert hashlib.sha256(p.read_bytes()).hexdigest() == hashlib.sha256(before).hexdigest()
    failing = {n: rc for n, rc in rcs.items() if rc}
    named = []
    for n in failing:
        named += [l for l in (out / f'm{k}-{n}.log').read_text().splitlines()
                  if l.startswith(('FAIL', 'ESCAPED', 'MISSED')) or 'failure' in l][:3]
    rows.append(dict(mutant=name, file=path, caught=bool(failing), failing=failing, named=named))
    print(('CAUGHT ' if failing else 'SURVIVED ') + name, failing, flush=True)
clean = run_all('clean')
rows.append(dict(mutant='none (restored tree)', caught=None, failing={n: rc for n, rc in clean.items() if rc}))
(out / 'mutants.json').write_text(json.dumps(rows, indent=2) + '\n')
bad = [r for r in rows[:-1] if not r['caught']] or rows[-1]['failing']
print('MUTANTS', 'PASS' if not bad else 'FAIL', f'{sum(bool(r["caught"]) for r in rows[:-1])} of {len(MUTANTS)} caught;',
      'restored tree', 'passes' if not rows[-1]['failing'] else f'FAILS {rows[-1]["failing"]}')
raise SystemExit(1 if bad else 0)
