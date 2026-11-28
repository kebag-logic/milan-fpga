"""Qualify the complete 100 MHz Arty 4x4 census at the installed row (round 9's qualify-final-census.py at arty-4x4);
never promote a partial pass. usage: qualify4.py CENSUS_DIR MERGED_MODEL.json   (cwd = checkout root)"""
import concurrent.futures, hashlib, json, math, subprocess, sys, threading
from pathlib import Path
root = Path.cwd(); out = Path(sys.argv[1]).resolve(); model_path = Path(sys.argv[2])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import arty_grade, build, run, scenario, shape_costs, kept_grade
POINT, HZ = 'arty-4x4', 100_000_000
manifest = json.loads((out / 'manifest.json').read_text())
completed = json.loads((out / 'completed.json').read_text())
expected = {(v, g) for v, gs in manifest['groups'].items() for g in gs}
assert {(r['variant'], r['group']) for r in completed} == expected and len(completed) == len(expected)
assert not (out / 'stop-finding.json').exists()
for row in completed:
    assert row['native_status'] == 0
    log = out / row['variant'] / 'results' / (row['group'] + '.log')
    assert hashlib.sha256(log.read_bytes()).hexdigest() == row['trace_sha256']
    assert not any(row[k] for k in ('refusals', 'share', 'late')), row['group']
commands, lock = [], threading.Lock()


def command(name, argv):
    log = out / (name + '.log')
    with log.open('w') as stream:
        rc = subprocess.run(argv, cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=28800).returncode
    with lock:
        commands.append(dict(name=name, command=argv, returncode=rc, log=str(log),
                             sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
        (out / 'qualification-commands.json').write_text(json.dumps(commands, indent=2) + '\n')
    print(name, rc, flush=True)
    return rc


failed = []
none = out / 'none' / 'results'
disp = kept_grade.Disposition([json.loads((none / (g + '.json')).read_text()) for g in ('srp-kept', 'srp-bound')], none,
                              build.reused(out / 'none'))
for row in completed:
    lines = disp.stated(row['stated']) if row['variant'] == 'none' and row['group'] in ('srp-kept', 'srp-bound') \
        else row['stated']
    failed += [f"{row['variant']}/{row['group']}: {f}" for f in lines]
held = [dict(o, variant=r['variant']) for r in completed for o in r['over_budget']]
results, regrades = [], []
for variant, wanted in manifest['groups'].items():
    d = out / variant
    spec = build.reused(d)
    actual = run.all_groups(scenario.point(POINT, spec), spec)
    if variant == 'answering-ports':
        actual = [g for g in actual if g.name in ('aecp', 'aecp-fanout', 'aecp-largest-notice', 'aecp-reboot')]
    assert sorted(g.name for g in actual) == sorted(wanted)
    for g in actual:
        assert (d / 'results' / (g.name + '.txt')).read_text() == g.script()
    argv = [sys.executable, '-B', 'tb/verilator/ctrl_service_budget/run.py', '--point', POINT, '--build-dir', str(d),
            '--variant', variant, '--regrade', '--record-budget-findings']
    if variant == 'answering-ports':
        argv += ['--groups', ','.join(wanted)]
    regrades.append(('regrade-' + variant, argv))
    results.append(str(d / 'results'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    codes = list(pool.map(lambda j: command(*j), regrades))
regrade_rc = {n: c for (n, _), c in zip(regrades, codes)}
if command('record-classes', [sys.executable, '-I', '-B', 'tb/verilator/ctrl_service_budget/record_classes.py', *results]):
    failed.append('record-classes')
measured = json.loads(model_path.read_text())
model, findings = arty_grade.inspect(root, POINT)
failed += findings
if not measured['choices']:
    failed.append('OWNER: no measured choice meets the rules and owner bounds')
else:
    choice = measured['choices'][0]
    own = shape_costs.at(shape_costs.Shape(1, 5, 5), root)
    c = measured['costs']
    for name, value in {'CTRL_LOOP_SLICE_US': choice['slice_us'], 'AECP_PACE_MS': choice['pace_ms'],
                        'CTRL_LOOP_QUEUED_MS': choice['queued_ms'], 'CTRL_LOOP_BUILD_PASS_US': c['build'],
                        'CTRL_LOOP_BUILD_ONE_PASS_US': c['build_one'], 'CTRL_LOOP_SRP_UNIT_US': c['record.srp'],
                        'CTRL_LOOP_STEP_PASS_US': c['step'], 'CTRL_LOOP_TICK_US': c['centisecond'],
                        'CTRL_LOOP_TX_MS': math.ceil(choice['rows_ms']['tx'] - 1e-9),
                        'CTRL_LOOP_RETRY_COLD_US': measured['retry_us'][0],
                        'CTRL_LOOP_RETRY_ATTEMPT_US': measured['retry_us'][1],
                        'AECP_NOTICE_US': measured['retry_us'][2]}.items():
        if own[name] != value:
            failed.append(f'{name}: installed {own[name]}, measured rule {value}')
    same = set(model.get('rows_ms', {})) == set(choice['rows_ms']) and all(
        model['rows_ms'][k] is not None and v is not None and abs(model['rows_ms'][k] - v) <= 1e-9
        for k, v in choice['rows_ms'].items())
    if not same or abs(model.get('load', -1) - measured['load']) > 1e-9:
        failed.append('Installed cost model differs from the measured model; rederive before qualification')
for variant in manifest['groups']:
    build.reused(out / variant)
worst = max(completed, key=lambda r: r['worst_pass_cycles'])
# The held-egress rows: no ledger is stated at this point (#878's held-egress ruling names (1,1,2)); each row's
# figure by that ruling's rule, the 60 ms hold plus 1.05 x the measured service, up to 0.01 ms, is reported only.
would = {o['probe']: math.ceil((60 + 1.05 * (o['ms'] - 60)) * 100 - 1e-9) / 100 for o in held}
record = dict(status='FAIL' if failed else 'PASS', kind='complete measured Arty FPGA point', point=POINT, cpu_hz=HZ,
              shape=[1, 5, 5], groups=len(completed), findings=failed, regrade_returncodes=regrade_rc,
              model=model, worst_pass=dict(group=worst['group'], cycles=worst['worst_pass_cycles'],
                                           ms=worst['worst_pass_cycles'] / HZ * 1000),
              held_egress=dict(rows={o['probe']: o['ms'] for o in held}, would_be_ledger_ms=would,
                               note='no ledger stated at arty-4x4; a ruling is needed'),
              owed_969=list(disp.owed), commands=commands)
(out / 'qualification.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ('status', 'findings', 'regrade_returncodes', 'worst_pass', 'held_egress')},
                 indent=1), flush=True)
raise SystemExit(bool(failed))
