#!/usr/bin/env python3
"""Focused log refusals. Usage: python3 -B probe_logs.py CHECKOUT OUTPUT_DIR.

All generated inputs stay under OUTPUT_DIR/scratch; no source files change.
"""
import contextlib
import io
import json
import sys
from pathlib import Path

checkout, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
sys.dont_write_bytecode = True
sys.path.insert(0, str(checkout / 'tb/verilator/ctrl_service_budget'))
import kept_grade as kg

work = output / 'scratch' / 'log-probes'
work.mkdir(parents=True, exist_ok=True)
(work / 'results').mkdir(exist_ok=True)

def logs(interfaces=1):
    result = {}
    for name, kinds in [('srp-kept', ('kept_advertise', 'kept_recount', 'kept_failed')),
                        ('srp-bound', ('bound_advertise',))]:
        rows = []
        for interface in range(interfaces):
            for kind in kinds:
                at = (len(rows) + 1) * 1000000
                rows.extend([f'MARK {at} srp.{kind}.if{interface}',
                             f'SPAN {at+100} {at+100} 1000 00002000 srp_mbx:receive'])
        rows.extend(['PASS 0 100 100 1000', 'SUMMARY passes=1', 'RESULT: PASS'])
        result[name] = '\n'.join(rows) + '\n'
    return result

cases = []
def add(name, change, want, words=(), interfaces=1, beside=None):
    value = logs(interfaces)
    change(value)
    cases.append((name, value, want, words, interfaces, beside))

add('clean-no-json', lambda x: None, 0)
add('clean-two-interfaces', lambda x: None, 0, interfaces=2)
for sidecar in (None, '{}', '{"passes":{"share":{"over_passes":[]}}}', '{broken-json'):
    add('over-share-sidecar-' + str(len(cases)),
        lambda x: x.update({'srp-kept': x['srp-kept'].replace('PASS 0 100 100 1000', 'PASS 0 100 100 200001')}),
        1, ('srp-kept: a work pass', 'THE SHARE'), beside=sidecar)
for group in ('srp-kept', 'srp-bound'):
    for kind, inserted in [('failed', 'RESULT: FAIL'), ('incomplete', ''),
                           ('trap', 'TRAP 99\nRESULT: PASS'), ('bus-error', 'BUSERR 99\nRESULT: PASS')]:
        add(group + '-' + kind,
            lambda x, g=group, s=inserted: x.update({g: x[g].replace('RESULT: PASS', s)}),
            1, (group + ': its log measures nothing',))
    add(group + '-idle-over',
        lambda x, g=group: x.update({g: 'IDLE 4 1000 200001\n' + x[g]}),
        1, (group + ': idle run', 'THE SHARE'))
add('missing-bound-log', lambda x: x.pop('srp-bound'), 1, ('srp-bound: no srp-bound.log',))
add('missing-interface-mate',
    lambda x: x.update({'srp-bound': x['srp-bound'].replace('srp.bound_advertise.if1', 'srp.bound_advertise.if2')}),
    1, ('srp.bound_advertise.if1', 'kept <= bound is unchecked'), interfaces=2)
add('unknown-log-line', lambda x: x.update({'srp-kept': 'UNKNOWN 1\n' + x['srp-kept']}),
    1, ('srp-kept: its log does not parse',))
receipts = []
for name, value, expected, words, interfaces, beside in cases:
    (work / 'build.json').write_text(json.dumps(dict(sys_hz=100000000, cpu_hz=100000000, interfaces=interfaces)))
    for group in ('srp-kept', 'srp-bound'):
        for ext in ('log', 'json'):
            (work / 'results' / f'{group}.{ext}').unlink(missing_ok=True)
        if group in value:
            (work / 'results' / f'{group}.log').write_text(value[group])
        if beside is not None:
            (work / 'results' / f'{group}.json').write_text(beside)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        rc = kg.main([str(work)])
    text = capture.getvalue()
    passed = rc == expected and all(w in text for w in words)
    receipts.append(dict(name=name, expected=expected, rc=rc, passed=passed, stdout=text))
    print(f'{name}: {"PASS" if passed else "FAIL"}, rc={rc}')
(output / 'probe-results.json').write_text(json.dumps(receipts, indent=2) + '\n')
assert all(r['passed'] for r in receipts)
print(f'{len(receipts)} focused cases passed')
