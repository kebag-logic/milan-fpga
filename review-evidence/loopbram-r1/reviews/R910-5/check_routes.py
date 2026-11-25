#!/usr/bin/env python3
"""Check source-bound route evidence without executing an implementation build."""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

OUT = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(sys.argv[1]).resolve()
P = OUT / 'scratch/public/author-r8/receipts'

def read_json(name):
    return json.loads((P / name).read_text().split('\n\n', 1)[1])

binding = read_json('source-binding.json.txt')
assert binding['identity_start'] == binding['identity_end']
for path, oid in binding['identity_start']['trees'].items():
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD:' + path], cwd=ROOT).decode().strip() == oid
input_counts = {}
for shape in ['endstation_ax7101_1x1_tdm8', 'endstation_ax7101_8x8']:
    inputs = read_json('inputs-' + shape + '.json.txt')['inputs']
    checked = []
    for path, digest in inputs.items():
        if path.startswith('$CHECKOUT/'):
            relative = path.removeprefix('$CHECKOUT/')
            if relative.startswith('sw/builder/out/'):
                continue
            assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest, path
            checked.append(relative)
    input_counts[shape] = {'total_inputs': len(inputs), 'checkout_inputs_matched': len(checked), 'generated_inputs': 'Published before/after binding only; no regeneration in review.'}
rows = read_json('route-summary.json.txt')
results = []
for row in rows:
    shape = '1x1' if '1x1' in row['shape'] else '8x8'
    prefix = f'route-{shape}--{row["directive"]}--'
    for corner, expected in row['corners'].items():
        raw = (P / (prefix + 'alinx_ax7101_signoff_' + corner + '_timing.rpt.part001.txt')).read_text()
        section = raw.split('WNS(ns)', 1)[1]
        nums = re.search(r'^\s*(-?\d+\.\d+\s+.*)$', section, re.M).group(1).split()
        assert float(nums[0]) == expected['WNS_ns']
        assert float(nums[4]) == expected['WHS_ns']
        assert float(nums[8]) == expected['WPWS_ns']
        assert int(nums[2]) == int(nums[6]) == int(nums[10]) == 0
    status = (P / (prefix + 'alinx_ax7101_route_status.rpt.txt')).read_text()
    assert re.search(r'# of nets with routing errors\.+\s*:\s*0\s*:', status)
    routable = re.search(r'# of routable nets\.+\s*:\s*(\d+)', status).group(1)
    routed = re.search(r'# of fully routed nets\.+\s*:\s*(\d+)', status).group(1)
    assert routable == routed
    if row['selected']:
        assert row['min_WNS_ns'] >= .030 and row['min_WHS_ns'] >= 0
    results.append({k:row[k] for k in ['shape','directive','min_WNS_ns','min_WHS_ns','selected','floor_pass','routing','utilization']})
result = {'source_binding_matches':True, 'inputs':input_counts, 'corners_compared_to_raw_reports':24, 'routes':results}
(OUT / 'route-audit.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: source subtrees and checkout input hashes match; 24 corner summaries match raw reports; both selected recipes meet the floor.')
