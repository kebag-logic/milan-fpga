#!/usr/bin/env python3
"""Focused author gates. No RTL builds, full sweeps, act, or Docker."""
import json
import sys
from receipt import BASE, HERE, identity, run

COMMANDS = [
    ('toc', 'scripts/gen_toc.py', '--selftest'),
    ('toc-check', 'scripts/gen_toc.py', '--check'),
    ('toc-anchors', 'scripts/gen_toc.py', '--verify-anchors'),
    ('toc-sites', 'scripts/gen_toc.py', '--sites'),
    ('em-dash', 'scripts/check_em_dash.py', '--selftest'),
    ('em-dash-base', 'scripts/check_em_dash.py', '--base', BASE),
    ('docs', 'scripts/docs_check.py'),
    ('docs-selftest', 'scripts/docs_check.py', '--selftest'),
    ('doc-style', 'scripts/check_doc_style.py'),
    ('doc-style-selftest', 'scripts/check_doc_style.py', '--selftest'),
    ('doc-paths', 'scripts/check_doc_paths.py'),
    ('py-idiom', 'scripts/check_py_idiom.py'),
    ('py-idiom-selftest', 'scripts/check_py_idiom.py', '--selftest'),
    ('hygiene', 'scripts/check_hygiene.py', '--check'),
    ('hygiene-selftest', 'scripts/check_hygiene.py', '--selftest'),
    ('test-evidence', 'scripts/measure_test_evidence.py', '--check'),
    ('test-evidence-selftest', 'scripts/measure_test_evidence.py', '--selftest'),
    ('fail-fast', 'scripts/measure_fail_fast.py', '--check'),
    ('fail-fast-selftest', 'scripts/measure_fail_fast.py', '--selftest'),
    ('todo', 'scripts/check_todo_ownership.py'),
    ('todo-selftest', 'scripts/check_todo_ownership.py', '--selftest'),
    ('cohesion-selftest', 'scripts/measure_cohesion.py', '--selftest'),
    ('control-flow-selftest', 'scripts/measure_control_flow.py', '--selftest'),
    ('ci-events', 'scripts/ci_events.py', '--check'),
    ('ci-events-selftest', 'scripts/ci_events.py', '--selftest'),
]

stamp = sys.argv[1]
results = []
for name, *args in COMMANDS:
    status = run(f'{stamp}-{name}', ['python3', '-B', *args])
    results.append({'name': name, 'command': ['rtk', 'proxy', 'python3', '-B', *args], 'exit': status})
    print(f'{name}: exit {status}', flush=True)
(HERE / f'gates-{stamp}.json').write_text(json.dumps({**identity(), 'results': results}, indent=2) + '\n')
sys.exit(any(row['exit'] for row in results))
