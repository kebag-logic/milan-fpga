#!/usr/bin/env python3
"""Joined controls, with three existing simulations paused to retain the job cap."""
import concurrent.futures
import json
import os
from pathlib import Path
import signal
import sys
import run_review as review

sys.path.insert(0, str(review.HARNESS))
import grade
import scenario

def standard(name, extra):
    return review.run(name + '-control', [sys.executable, '-B', str(review.HARNESS / 'run.py'),
        '--point', '1x1', '--build-dir', str(review.SCRATCH / name), '--reuse-build', '--jobs', '1', *extra])

def independent():
    spec = json.loads((review.SCRATCH / 'A1/build.json').read_text())
    p = scenario.point('1x1', spec)
    g = scenario.Group('review-acmp')
    scenario.ready(g, p, link=False)
    ch = scenario.CH['acmp']
    g.probe(scenario.Probe('review.bind.if0', 'independent slow ACMP', 'acmp', f'rxc:{ch}',
        [f'resp:{ch}:7a00', f'acmp_cmd:{ch}:PROBE_TX', 'arm:1'],
        expect='acmp_status:BIND_RX_RESPONSE:0'),
        f'frame 0 {scenario.acmp_cmd(p, "BIND_RX", 0, 0x7a00).hex()}',
        wait=f'tx {ch} 2 within {100 * scenario.MS}', settle=f'cycles {50 * scenario.MS}')
    results = {}
    for name in ['A1', 'own-slow']:
        out = review.SCRATCH / name / 'own-probe'
        out.mkdir(exist_ok=True)
        script = out / 'review-acmp.txt'
        script.write_text(g.script())
        rc = review.run(name + '-own-probe', [str(review.SCRATCH / name / 'native/Vsim'), str(script), '-'],
                        review.SCRATCH / name / 'gateware')
        assert rc == 0
        text = (review.SCRATCH / (name + '-own-probe.raw.log')).read_text()
        results[name] = grade.grade(text, g, spec['sys_hz'], spec['cpu_hz'])
    assert results['A1']['probes'][0]['within_t_svc']
    assert not results['own-slow']['probes'][0]['within_t_svc']
    (review.PACKET / 'independent-control.json').write_text(json.dumps(results, indent=2) + '\n')
    print('Independent slow ACMP caught', flush=True)
    return 0

pids = []
for entry in Path('/proc').iterdir():
    if not entry.name.isdecimal():
        continue
    try:
        argv = (entry / 'cmdline').read_bytes().split(b'\0')
        exe = argv[0].decode()
    except (OSError, UnicodeError):
        continue
    if exe.startswith(str(review.SCRATCH / 'A1') + '/') and exe.endswith('/native/Vsim') and len(pids) < 3:
        pids.append(int(entry.name))
# No pause is needed when this script is reproduced without the main campaigns.
try:
    for pid in pids:
        os.kill(pid, signal.SIGSTOP)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(standard, 'asbuilt', ['--cpu-regions', 'as-built']),
                pool.submit(standard, 'slow', ['--mutation', 'slow-adp-rx']),
                pool.submit(independent)]
        codes = [j.result() for j in jobs]
    raise SystemExit(bool(any(codes)))
finally:
    for pid in pids:
        try:
            os.kill(pid, signal.SIGCONT)
        except ProcessLookupError:
            pass
