#!/usr/bin/env python3
"""Independent population/tally audit over fresh raw execution artifacts."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

out = Path(__file__).resolve().parents[1]
repo = Path(sys.argv[1]).resolve()
suite = out / 'scratch/tb/verilator/ptp_ts'
prefix = 'TOP.axis_mux_rr_2in_1out.u_sva.'
def labels(file):
    return re.findall(r'^\s*((?:ap|ai)_\w+): assert', file.read_text(), re.M)
stream = labels(repo/'tb/common/sva/axis_stream_source_sva.sv')
mux = labels(repo/'tb/common/sva/axis_mux_rr_2in_1out_sva.sv')
expected = {prefix+port+'.'+rule for port in ['u_s0_stimulus','u_s1_stimulus','u_m_dut'] for rule in stream}
expected |= {prefix+rule for rule in mux}
assert len(expected) == 21
witnesses = {}
for width in [8,64]:
    log = (suite/f'obj_dir_sva_campaign/clean-w{width}/run.log').read_text()
    rows = re.findall(r'^witness (\S+)\s+nonvacuous=(\d+) harness=(\d+) \(([^)]+)\)', log, re.M)
    assert len(rows) == 21 and {x[0] for x in rows} == expected
    populations = collections.Counter(row[3] for row in rows)
    assert populations == {'equal':15,'at least':2,'both above zero':4}, populations
    for name, observed, harness, relation in rows:
        observed,harness = int(observed),int(harness)
        assert observed > 0 and harness > 0
        if relation == 'equal': assert observed == harness
        elif relation == 'at least': assert observed >= harness
    witnesses[width] = dict(populations=populations, rows=rows)

detected = {}
for directory in sorted((suite/'obj_dir_sva_campaign').iterdir()):
    if not directory.name.startswith(('stimulus-','mutant-')):
        continue
    log = (directory/'run.log').read_text()
    paths = re.findall(r'Assertion failed in ([\w.$]+):',log)
    assert paths and 'SVA-STOP:' in log, directory.name
    for path in paths:
        path = path.replace('.forwarding_laws.', '.')
        detected.setdefault(path,[]).append(directory.name)
assert set(detected) == expected, sorted(expected-set(detected))
campaign = (out/'raw/focused-campaign.log').read_text()
assert len(re.findall(r'^  \[PASS\]',campaign,re.M)) == 62
assert '[FAIL]' not in campaign and 'Assertion failed in' not in campaign
assert 'checks: 62   failures: 0' in campaign

spec = importlib.util.spec_from_file_location('review_suite_tally',repo/'scripts/suite_tally.py')
tally = importlib.util.module_from_spec(spec)
sys.modules[spec.name]=tally
spec.loader.exec_module(tally)
fresh = '\n'.join((out/'raw'/f).read_text() for f in ['original-ptp-ts.log','focused-mux.log','focused-campaign.log'])
(out/'raw/focused-suite-composed.log').write_text(fresh)
counts = tally.scan(fresh)
assert counts[0:2] == (495,0),counts
assert len(counts[2]) == 4 and not counts[3] and not counts[4]
assert not tally.log_reports_failure(fresh)[1]
assert 'Assertion failed in' not in fresh and 'SVA-STOP:' not in fresh

manager = out/'public-manager'
public_summary={}
for name,total in [('manager-builder',48),('full-native',5)]:
    bank=json.loads((manager/name/'results.json').read_text())
    assert bank['head']=='059c3a60b8290873ed9fd14673f9981e8af754ce'
    assert bank['base']=='52711029f374650dc93830d5ea28e81cb5c8f410'
    assert len(bank['results'])==total and all(x['exit_code']==0 for x in bank['results'])
    public_summary[name]=dict(head=bank['head'],base=bank['base'],commands=total,all_exit_zero=True)

summary = dict(witnesses=witnesses, named_detection=detected,
               fresh_composed_tallies=counts, manager_ledger_audit=public_summary)
(out/'raw/result-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print('PASS: 21 distinct witness pairs at each width; 15 equality / 2 floor / 4 presence')
print('PASS: 21/21 pairs observed failing by name in successfully built campaign controls')
print('PASS: 62 campaign rows; composed focused log has 495 checks in 4 tallies, no failures or skips')
print('PASS: corrected-source public evidence, 48 static/builder and 5 native commands exit zero')
