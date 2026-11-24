#!/usr/bin/env python3
"""Recompute #998 corrected receipt claims without executing candidate code."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / 'inputs'
manifest = {row['file']: row for row in json.loads((INPUTS / 'MANIFEST.json').read_text())}
verified = []

def read(name):
    data = (INPUTS / name).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert digest == manifest[name]['published_sha256'], name
    verified.append({'path': name, 'sha256': digest})
    return data

def timing(name):
    raw = read(name).decode()
    values = {}
    for key in ('wall', 'user', 'sys'):
        match = re.search(r'(\d+\.\d+) ' + key + r'\b', raw)
        assert match, (name, key)
        values[key] = float(match[1])
    return values

def reduction(base, new):
    return 100 * (1 - new / base)

def counters(name):
    rows = read(name).decode().splitlines()
    result = {}
    for line in rows:
        if line and not line.startswith('#'):
            fields = line.split(',')
            result[fields[2]] = float(fields[0])
    return result

correction = read('author-r1b/CORRECTIONS.md').decode()
crf_root = 'author-r1b/receipts/ccache/crf_rx-mutants/'
crf_times = {kind: timing(crf_root + kind + '.time') for kind in ('nocc', 'cold', 'warm')}
logs = {kind: read(crf_root + kind + '.log') for kind in crf_times}
assert len(set(logs.values())) == 1, 'Full CRF logs differ'
verdicts = {}
for kind, data in logs.items():
    lines = data.decode().splitlines()
    verdicts[kind] = [line for line in lines if line.startswith('[PASS]')]
    assert len(verdicts[kind]) == 23
    assert len(set(verdicts[kind])) == 23
    assert sum(line.endswith('rc=0') for line in verdicts[kind]) == 3
    assert sum(line.endswith('rc=1') for line in verdicts[kind]) == 20
    assert sum(line.startswith('  named rejection:') for line in lines) == 20
    assert lines[-1] == '== crf_rx mutants: checks: 23   failures: 0 =='
crf_reductions = {kind: {key: reduction(crf_times['nocc'][key], crf_times[kind][key])
                         for key in ('user', 'wall')}
                  for kind in ('cold', 'warm')}
assert round(crf_reductions['cold']['user']) == 47
assert round(crf_reductions['warm']['user']) == 54

avtp_root = 'author-r1b/receipts/ccache/avtp_rxmon/'
avtp_times = {kind: timing(avtp_root + kind + '.time') for kind in ('nocc', 'cold')}
avtp_reductions = {key: reduction(avtp_times['nocc'][key], avtp_times['cold'][key])
                   for key in ('user', 'wall')}
# The correction states 65.5%; the PR's 65% is a conservative integer summary,
# not nearest-integer rounding (which would be 66%).
assert round(avtp_reductions['user'], 1) == 65.5
assert int(avtp_reductions['user']) == 65
read(avtp_root + 'cold.stats')
# Confirm the correction reattributes existing AVTP timings, rather than altering them.
for kind in ('nocc', 'cold'):
    assert read('author/receipts/ccache/' + kind + '.time') == (INPUTS / (avtp_root + kind + '.time')).read_bytes()

pairs = []
for suffix in ('', '-2', '-3'):
    base = counters('author/receipts/budget/base' + suffix + '.perf')
    optimized = counters('author/receipts/budget/tbO3' + suffix + '.perf')
    event = 'L1-dcache-load-misses:u'
    pairs.append({'pair': suffix or 'unsuffixed', 'base_l1d': int(base[event]),
                  'optimized_l1d': int(optimized[event]),
                  'l1d_reduction_percent': reduction(base[event], optimized[event]),
                  'task_clock_reduction_percent': reduction(base['task-clock:u'], optimized['task-clock:u'])})
assert [round(pair['l1d_reduction_percent'], 1) for pair in pairs] == [14.5, 8.8, 5.4]
pr = (INPUTS / 'pr-body.md').read_text()
assert 'CPU -47 % on a cold cache (-54 % warm)' in pr
assert 'avtp_rxmon -65 % cold' in pr
statement = 'L1d misses 5-15 % lower in three paired runs (median 8.8 %)'
assert statement in pr and statement in correction
assert 'L1d misses -7..-9 %' not in pr

result = {'result': 'PASS', 'metric': 'user CPU for ccache; L1-dcache-load-misses:u for budget',
          'formula': '100 * (1 - optimized / baseline)', 'crf_times_seconds': crf_times,
          'crf_reduction_percent': crf_reductions,
          'crf_full_logs_identical': True, 'crf_log_bytes': len(logs['nocc']),
          'crf_log_sha256': hashlib.sha256(logs['nocc']).hexdigest(),
          'crf_verdict_lines': verdicts['nocc'], 'crf_clean_controls': 3,
          'crf_named_rejections': 20, 'avtp_times_seconds': avtp_times,
          'avtp_reduction_percent': avtp_reductions,
          'avtp_pr_precision': '65% is a conservative integer summary; nearest integer is 66%',
          'avtp_original_timing_bytes_preserved': True,
          'budget_pairs': pairs, 'pr_claims_match': True,
          'manifest_checks': verified,
          'limits': ['Checks retained receipts; no performance rerun.',
                     'AVTP full logs are not published; their identity is not re-proved here.',
                     'SHA-256 matches are integrity checks, not digital signature verification.']}
print(json.dumps(result, indent=2))
