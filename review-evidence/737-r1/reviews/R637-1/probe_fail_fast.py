#!/usr/bin/env python3
"""Exercise actual watcher selection against generated workflow job inventories."""
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'scripts'))
from ci_fail_fast import observe
from ci_gate_workflows import TEMPLATES, load_template, generate
from ci_workflow_plan import expand_workflow
import yaml

for name in TEMPLATES:
    generated = generate(name, load_template(root, name))
    _, labels = expand_workflow('.github/workflows/' + name + '.yml', yaml.safe_dump(generated))
    watcher = generated['jobs']['ci-fail-fast']
    watch_step = next(s for s in watcher['steps'] if s.get('name') == 'Observe the first failed job')
    expected = set(json.loads(watch_step['env']['EXPECTED_JOBS']))
    collector = generated['jobs']['ci-manifest']
    rows = [{'name': label, 'status': 'completed', 'conclusion': 'success'} for label in expected]
    assert observe(rows, expected) == (True, None)
    rows.append({'name': collector['name'], 'status': 'completed', 'conclusion': 'failure'})
    result = observe(rows, expected)
    assert result == (True, None)
    assert 'ci-fail-fast' in collector['needs']
    assert not any('ci_fail_fast.py cancel' in s.get('run', '') for s in collector['steps'])
    control = [dict(row) for row in rows[:-1]]
    control[0]['conclusion'] = 'failure'
    assert observe(control, expected)[1] is not None
    print(json.dumps({'workflow': name, 'watched_jobs': len(expected),
                      'excluded_jobs': sorted(set(labels.values()) - expected),
                      'ordinary_failure_detected': True,
                      'collector_failure_detected': result[1] is not None,
                      'watcher_must_finish_before_collector': True,
                      'collector_has_cancellation_step': False}, sort_keys=True))
