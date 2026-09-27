"""Focused controls for round-3 replay and declaration corrections.

Usage: python3 check_controls.py ADDENDUM ROUND_TWO_ADDENDUM
"""
import ast
import csv
import json
import os
from pathlib import Path
import subprocess
import sys

from declarations import declaration_events, require_all_holds_declared
from recompute import classify_stop, outcome_lines, require


def main():
    output, prior = map(Path, sys.argv[1:])
    checks = []
    for name, arguments, expected in [
        ('silent hold', (0, 100, 100), 'RESTART'),
        ('one settled PDU', (1, 101, 100), 'NOT_RESTART'),
        ('early resumption', (0, 99, 100), 'NOT_RESTART'),
        ('continuous hold', (754, 50, 100), 'NOT_RESTART'),
    ]:
        require(classify_stop(*arguments) == expected, name)
        checks.append(name)
    source = (output/'recompute.py').read_text()
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))), 'assert remains')
    require('except AssertionError' not in source, 'assertion exception classifier remains')
    checks.append('all replay consistency checks use explicit conditions')
    for label, option, environment in [
        ('optimization option', ['-O'], dict(os.environ)),
        ('optimization environment', [], dict(os.environ, PYTHONOPTIMIZE='1')),
    ]:
        result = subprocess.run([sys.executable, '-B', *option, str(output/'recompute.py')],
                                env=environment, capture_output=True, text=True, timeout=120)
        require(result.returncode != 0 and 'REFUSED: optimized execution' in result.stderr, label)
        checks.append(f'{label}: refused, rc {result.returncode}')
    events = [dict(event=e) for e in ('New', 'JoinIn', 'In', 'JoinMt', 'Mt', 'Lv', 'LeaveAll')]
    require([e['event'] for e in declaration_events(events)] == ['New', 'JoinIn', 'JoinMt'], 'declaration predicate')
    require(not declaration_events([dict(event='Mt'), dict(event='Lv')]), 'empty/withdrawal accepted')
    checks.append('only New, JoinIn, JoinMt declare; In, Mt, Lv, LeaveAll excluded')
    with (output/'hold-declarations.csv').open() as f:
        holds = [dict(cycle=int(r['cycle']), declaration_count=int(r['declaration_count'])) for r in csv.DictReader(f)]
    rejected = False
    try:
        require_all_holds_declared(holds)
    except ValueError as error:
        require(str(error) == 'holds without DUT declaration: [1]', 'unexpected old-claim rejection')
        rejected = True
    require(rejected, 'old universal declaration claim passed')
    checks.append('old universal declaration claim rejected on recorded cycle 1')
    require_all_holds_declared([r for r in holds if r['declaration_count']])
    checks.append('remaining declared holds pass the same predicate')
    rows = [dict(direction='talker', cycle=7, stop_check='FAIL', classification='NOT_RESTART'),
            dict(direction='listener', cycle=2, stop_check='PASS', classification='RESTART')]
    text = '\n'.join(outcome_lines(rows))
    require('2 raw hashes' in text and '1 PASS; 1 FAIL' in text and 'talker-007' in text, 'derived outcome')
    require('197' not in text and '013' not in text and '024' not in text and '075' not in text, 'pinned outcome')
    require('0 FAIL' in outcome_lines(rows[1:])[1] and 'none' in outcome_lines(rows[1:])[1], 'empty rejection set')
    checks.append('printed totals and rejected identities change with input; empty rejection set supported')
    for name in ('stop-checks.csv', 'recomputed-summary.json', 'input-hashes.csv'):
        require((output/name).read_bytes() == (prior/name).read_bytes(), f'{name} changed')
        checks.append(f'{name}: byte-identical to round-2 numeric evidence')
    receipt = dict(result='PASS', checks=checks)
    (output/'controls.json').write_text(json.dumps(receipt, indent=2)+'\n')
    for check in checks:
        print('PASS:', check)


if __name__ == '__main__':
    main()
