from pathlib import Path
import json
import re

root = Path('/tmp/502-a345')
r329_old = (root / 'r329-unchanged/RESULTS.txt').read_text()
assert len(re.findall(r'^control\s+(?:dyn|static)\s+PASS\b', r329_old, re.M)) == 2
assert len(re.findall(r'^M(?:3|7)_\S+\s+(?:dyn|static)\s+FAIL\b', r329_old, re.M)) == 4
assert r329_old.count('REFUSED') == 8
r328_old = (root / 'r328-unchanged.log').read_text()
assert r328_old.count('REFUSED') == 7
assert r328_old.count('static=KILLED') == 3
assert r328_old.count('dynamic=KILLED') == 3
r329_new = (root / 'r329-reanchored/RESULTS.txt').read_text()
assert len(re.findall(r'^M\d+_\S+\s+(?:dyn|static)\s+FAIL\s+pp_shadow: \d+ checks, [1-9]\d* failures$', r329_new, re.M)) == 16
assert 'REFUSED' not in r329_new
r328_new = (root / 'r328-reanchored.log').read_text()
assert r328_new.count('static=KILLED') == 7
assert r328_new.count('dynamic=KILLED') == 7
assert 'REFUSED' not in r328_new
for phrase in ['K12 refused record input sticky_pending_PP_STAT',
               'K12 refused record output sticky_pending_PP_STAT',
               'K12 remove input no_durable_claim_over_unsaved',
               'K12 remove output no_durable_claim_over_unsaved']:
    assert phrase in r329_new
probe = (root / 'r329-probe-unchanged.log').read_text()
assert 'pp_shadow: 295 checks, 0 failures' in probe
assert 'P3 duplicate ADD status 0, phase-5 records 1, marks 0, mappings after 1, PP_STAT[11] pend 0, durable 1' in probe
print(json.dumps({
    'r329_unchanged_clean_controls': 2,
    'r329_unchanged_killed_legs': 4,
    'r329_unchanged_refused_anchors': 8,
    'r328_unchanged_killed_legs': 6,
    'r328_unchanged_refused_anchors': 7,
    'r329_adapted_killed_legs': 16,
    'r328_adapted_killed_legs': 14,
    'named_refusal_and_remove_failures_present': True,
    'r329_probe_checks': 295,
    'r329_probe_failures': 0,
    'r329_duplicate_pending': 0,
    'r329_duplicate_durable': 1
}, indent=2))
