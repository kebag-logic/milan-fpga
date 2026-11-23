#!/usr/bin/env python3
"""Exercise standalone kept grading with controlled missing evidence: CHECKOUT PACKET.
Logs are synthetic, following the repository's own selftest format.
"""
import json
from pathlib import Path
import subprocess
import sys
root, packet = (Path(x).resolve() for x in sys.argv[1:3])
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade
import kept_grade
import run as harness
import scenario
scratch = packet / 'scratch/grader-probes'
scratch.mkdir(parents=True, exist_ok=True)
hz = 100_000_000
spec = dict(sys_hz=hz, cpu_hz=hz, shape='endstation_ax7101_1x1_tdm8', interfaces=1)
def text(probes, cycles):
    lines = []
    for i, name in enumerate(probes):
        at = 1_000_000 * (i + 1)
        lines += [f'MARK {at} {name}', f'SPAN {at+100} {at+100} 1000 00002000 srp_mbx:receive']
    lines += [f'PASS 0 10000000 10000000 {cycles}', 'SUMMARY passes=1', 'RESULT: PASS']
    return '\n'.join(lines) + '\n'
kept_names = ['srp.kept_advertise.if0', 'srp.kept_recount.if0', 'srp.kept_failed.if0']
def run(name, kind, cycles=250000):
    build = scratch / name
    results = build / 'results'
    results.mkdir(parents=True, exist_ok=True)
    (build / 'build.json').write_text(json.dumps(spec))
    for group, probes in [('srp-kept', kept_names), ('srp-bound', ['srp.bound_advertise.if1' if kind=='missing-mate' else 'srp.bound_advertise.if0'])]:
        data = text(probes, cycles if group=='srp-kept' else 1000)
        actual = data.replace('RESULT: PASS', 'RESULT: FAIL') if group=='srp-kept' and kind=='stale-result' else data
        (results / (group+'.log')).write_text(actual)
        parsed = grade.parse(data, hz, hz)
        if group=='srp-kept' and kind=='stale-result':
            parsed = grade.parse(text(probes, 1000), hz, hz)
        result = dict(group=group, passes=dict(share=grade.pass_share(parsed)))
        if group=='srp-kept' and kind=='empty-result': result = {}
        if group=='srp-kept' and kind=='missing-share': result = dict(group=group, passes={})
        if group=='srp-kept' and kind=='absent-result': continue
        (results / (group+'.json')).write_text(json.dumps(result))
    if kind=='stale-result':
        before = (results/'srp-kept.json').read_bytes()
        fresh, refusals, misses = harness.graded([scenario.Group('srp-kept')], [results/'srp-kept.log'], spec, results)
        (packet/'grader-stale-result-regrade.json').write_text(json.dumps(dict(fresh_results=fresh,
            refusals=refusals, misses=misses, prior_json_retained=before==(results/'srp-kept.json').read_bytes()),indent=2)+'\n')
    command = [sys.executable, '-B', str(root/'tb/verilator/ctrl_service_budget/kept_grade.py'), str(build)]
    r = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = r.stdout.replace(str(root), '<checkout>').replace(str(packet), '<packet>')
    (packet / ('grader-'+name+'.log')).write_text(output)
    (packet / ('grader-'+name+'.rc')).write_text(str(r.returncode)+'\n')
    return dict(name=name, rc=r.returncode, kind=kind, kept_pass_cycles=cycles,
                verdict=output.splitlines()[-1])
rows = [run('valid-within','valid',1000),run('valid-over','valid'),
        run('absent-result','absent-result'),run('empty-result','empty-result'),
        run('missing-share','missing-share'),run('missing-mate','missing-mate',1000),
        run('stale-result','stale-result')]
(packet/'grader-probe-results.json').write_text(json.dumps(rows, indent=2)+'\n')
for row in rows: print(json.dumps(row))
