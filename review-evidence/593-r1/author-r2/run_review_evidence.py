#!/usr/bin/env python3
"""Replay the read-only review packets and documented span adaptations."""
import json
from run_gates import OUT, ROOT, run

results = []
for number in ('362', '363'):
 packet = f'$REVIEWS/593-r{number}-1-packet/scripts'
 for kind, tail in [('probe', ['oracle_probe.py', str(ROOT)]),
                    ('mutants', ['reviewer_mutants.py', str(ROOT), f'/tmp/593-a380-final-r{number}'])]:
  command = ['python3', '-B', packet + '/' + tail[0], *tail[1:]]
  results.append(run(f'r{number}-{kind}', command))
  (OUT / 'review-evidence.json').write_text(json.dumps(results, indent=2)+'\n')
 results.append(run(f'r{number}-span-probe', ['python3', '-B', str(OUT / f'r{number}_span_probe.py'), str(ROOT)]))
 (OUT / 'review-evidence.json').write_text(json.dumps(results, indent=2)+'\n')
results.append(run('r363-survivor-recheck', ['python3', '-B',
 '$REVIEWS/593-r363-1-packet/scripts/survivor_recheck.py', str(ROOT),
 '/tmp/593-a380-final-survivors']))
(OUT / 'review-evidence.json').write_text(json.dumps(results, indent=2)+'\n')
raise SystemExit(any(result['rc'] for result in results))
