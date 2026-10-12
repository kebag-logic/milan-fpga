#!/usr/bin/env python3
"""Check arithmetic and coverage comparisons in the published author receipts."""
import csv
import json
import math
from pathlib import Path

p=Path(__file__).resolve().parent
timing=json.loads((p/'public-author-ROUND2-TIMING-RESULTS.json').read_text())
predictions=json.loads((p/'public-author-ROUND2-TIMING-PREDICTIONS.json').read_text())
assert len(timing)==4
for t,v in zip(timing,predictions['predictions']):
    assert t['head']==predictions['head']=='941e15593ef3dbf561bd8ed75aaf680f5d146a41'
    assert t['job']==v['job'] and t['seconds']==v['local_seconds']
    assert len(t['cpus'])==4 and all(c['rc']==0 for c in t['commands'])
    assert abs(sum(c['seconds'] for c in t['commands'])-t['seconds'])<0.1
    assert math.ceil(t['seconds']*predictions['ratio']+60)==v['calibrated_prediction']
    assert math.ceil(t['seconds']*predictions['original_ratio']+60)==v['original_ratio_prediction']
    assert v['calibrated_prediction']<=1620
    print(f"PASS: {t['job']} receipt rc values and prediction {v['calibrated_prediction']} s / 2700 s.")
assert predictions['ratio']==max(x['ratio'] for x in predictions['calibration_rows'])
assert len(predictions['calibration_rows'])==40
assert max(x['overhead_seconds'] for x in predictions['calibration_rows'])==33
rows=list(csv.DictReader((p/'public-author-ROUND2-COVERAGE-COMPARISON.csv').open()))
assert len(rows)==30
for row in rows:
    for field in ['raw_lines','raw_branches','kept_lines','kept_branches']:
        assert row['baseline_'+field]==row['candidate_'+field]
    assert row['covered_locations_equal']=='True'
print('PASS: published comparison has matching raw/retained line/branch fractions and covered-location equality for all 30 files.')
print('Scope: checks the published author records; does not independently repeat their timed firmware executions or measurements.')
