#!/usr/bin/env python3
"""Independently reconstruct timestamp windows and measured shard envelopes."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import sys

root, packet = (Path(arg).resolve() for arg in sys.argv[1:3])
receipt = packet / 'receipts'
hosted = receipt / 'hosted'
jobs = {}
for path in hosted.glob('run-*.json'):
    for job in json.loads(path.read_text()):
        jobs[job['id']] = job
inventory = sorted(p.parent.name for p in (root / 'tb/verilator').glob('*/Makefile')
                   if p.parent.name != 'milan_dp_gptp')
owners = {suite: (4 if suite == 'milan_dp' else
                 int.from_bytes(hashlib.sha256(suite.encode()).digest()[:8], 'big') % 4)
          for suite in inventory}
new = {'capture_coherence': 2400, 'milan_dp_mclk': 3600, 'milan_dp': 4800}
windows, overheads = [], []
window_jobs, complete_jobs = 0, 0
def stamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

for path in sorted(hosted.glob('job-*.log.timestamps')):
    jobid = int(path.name.split('-')[1].split('.')[0])
    job = jobs[jobid]
    prior, shard, expected = None, None, None
    seen = []
    total = 0.0
    for line in path.read_text().splitlines():
        line = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', line)
        selected = re.match(r'^(\S+) shard: (\d+/\d+)\s+selected suites: (\d+)', line)
        verdict = re.match(r'^(\S+) (PASS|FAIL|TIMEOUT)\s+([a-z0-9_]+)(?:\s|$)', line)
        if selected:
            prior, shard, expected = stamp(selected[1]), selected[2], int(selected[3])
        elif verdict:
            assert prior is not None, (jobid, line)
            now = stamp(verdict[1])
            elapsed = (now - prior).total_seconds()
            assert elapsed >= 0
            windows.append(dict(job=jobid, run=job['run_id'], shard=shard, suite=verdict[3],
                                verdict=verdict[2], seconds=elapsed,
                                begin=prior.isoformat(), end=now.isoformat()))
            total += elapsed
            prior = now
            seen.append(verdict[3])
    if seen:
        window_jobs += 1
    if expected and len(seen) == expected:
        assert len(set(seen)) == expected
        if shard.endswith('/5'):
            assert sorted(seen) == [s for s in inventory if owners[s] == int(shard[0])]
        else:
            assert seen == ['milan_dp_gptp']
        duration = (stamp(job['completed_at']) - stamp(job['started_at'])).total_seconds()
        overhead = duration - total
        assert overhead >= 0
        overheads.append(dict(job=jobid, run=job['run_id'], shard=shard, seconds=overhead,
                              job_seconds=duration, window_seconds=total))
        complete_jobs += 1

assert len(windows) == 425 and window_jobs == 38 and complete_jobs == 36
maxima = {}
for window in windows:
    suite = window['suite']
    if suite not in maxima or window['seconds'] > maxima[suite]['seconds']:
        maxima[suite] = window
assert set(maxima) == set(inventory) | {'milan_dp_gptp'}
workflow = (root / '.github/workflows/rtl.yml').read_text()
block = workflow.split('\n  verilator-shards:', 1)[1].split('\n  physical-gptp:', 1)[0]
timeout = int(re.search(r'timeout-minutes: (\d+)', block)[1]) * 60
assert timeout == 7200
envelopes = []
for owner in range(5):
    suites = [s for s in inventory if owners[s] == owner]
    changed = sum(new[s] for s in suites if s in new)
    siblings = sum(maxima[s]['seconds'] for s in suites if s not in new)
    overhead = max((o for o in overheads if o['shard'] == f'{owner}/5'), key=lambda o: o['seconds'])
    envelope = changed + siblings + overhead['seconds']
    result = dict(shard=f'{owner}/5', changed_limits=changed, siblings=siblings,
                  overhead=overhead, envelope=envelope, headroom_seconds=timeout-envelope,
                  headroom_percent=100*(timeout-envelope)/timeout)
    envelopes.append(result)
    if changed:
        assert envelope <= 0.9 * timeout
        # Require the committed rounded table to match independent arithmetic.
        doc = (root / 'docs/testing/CI_WORKFLOWS.md').read_text()
        row = next(line for line in doc.splitlines() if line.startswith(f'| {owner}/5 |'))
        for number in (siblings, overhead['seconds'], envelope, timeout-envelope):
            rendered = '0 s' if number == 0 else f'{number:.3f} s'
            assert rendered in row, (row, number)
        assert f'{result["headroom_percent"]:.2f}%' in row
old = {'milan_dp': 3600, 'milan_dp_gptp': 5400}
near = [{**maxima[s], 'old_budget': old.get(s, 1800),
         'usage_percent': 100*maxima[s]['seconds']/old.get(s, 1800)}
        for s in sorted(maxima) if maxima[s]['seconds'] > .6*old.get(s, 1800)]
assert {r['suite'] for r in near} == {'capture_coherence','milan_dp','milan_dp_gptp',
                                      'milan_dp_mclk','milan_dp_render','mmcm_servo','pp_shadow'}
assert {r['suite'] for r in near if r['usage_percent'] > 80 and r['suite'] != 'milan_dp_gptp'} == set(new)
result = dict(windows=len(windows), window_jobs=window_jobs, complete_jobs=complete_jobs,
              near_limit=near, envelopes=envelopes, maxima=maxima, all_windows=windows,
              all_overheads=overheads, inventory=owners)
(receipt / 'measurement-analysis.json').write_text(json.dumps(result, indent=2) + '\n')
for item in near:
    print(f"{item['suite']}: {item['seconds']:.6f} s {item['verdict']}; run {item['run']}, job {item['job']}")
for item in envelopes:
    print(f"{item['shard']}: {item['changed_limits']} + {item['siblings']:.3f} + {item['overhead']['seconds']:.3f} = {item['envelope']:.3f} s; headroom {item['headroom_percent']:.2f}%")
print('PASS: frozen survey, complete inventory, published arithmetic and 10% margins')
