#!/usr/bin/env python3
"""Probe whether the declared polls base contributes to the sustained load."""
import json
import pathlib
import sys
sys.dont_write_bytecode = True
repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'tb/verilator/ctrl_service_budget'))
import load_grade
import poll_grade
import rows_tiers
point = '8x8/1if'
rows = []
original = poll_grade.EIGHT_ONE['base']
try:
    for base in (300, 350, 10000):
        poll_grade.EIGHT_ONE['base'] = base
        terms = load_grade.load(repo, point, load_grade.STATED_US)
        inputs = rows_tiers.point_inputs(repo, point)
        window, row_terms = rows_tiers.solve('tx', inputs, rows_tiers.BUILT)
        passes = row_terms['passes'] / (inputs.c['events_none'] + inputs.c['base'])
        rows.append(dict(base_us=base, resolved_base_us=load_grade.stated(repo, point, load_grade.STATED_US)['base'],
                         load=sum(terms.values()), terms=terms, tx_ms=window,
                         row_base_us=inputs.c['base'], row_passes=passes,
                         row_pass_charge_us=row_terms['passes']))
finally:
    poll_grade.EIGHT_ONE['base'] = original
assert rows[0]['terms'] == rows[1]['terms'] == rows[2]['terms']
print(json.dumps(rows, indent=2))
print('PASS: the base is read into stated costs but contributes zero to load().')
assert rows[1]['row_base_us'] == 350 and rows[1]['row_passes'] >= 1
assert rows[1]['tx_ms'] > rows[0]['tx_ms']
print('PASS: response rows charge the declared base on every counted ordinary pass; increasing it raises the row.')
print('Under the approved base partition, neither observed-baseline subtraction is an additional load term.')
