"""Verify named failures in the reviewed external and standing controls."""
from pathlib import Path
import json
r=Path('$VALIDATION_STORAGE/pp73-a595/r5')
records=[]
for label,folder,variant,expected in [
 ('echo-hide','review-probes','echo-hide',[1,2,1,2]),
 ('echo-control','review-probes','echo-control',[0,2,1,2]),
 ('echo-hide-explicit-shared','shared-probe','echo-hide',[0,2,1,2])]:
    steps=['write','record','gate','suite']
    codes=[int((r/folder/f'{variant}.{step}.rc').read_text()) for step in steps]
    assert codes==expected,(label,codes)
    words=['schema: echo_entries: EAVL','nor listed in shared_entries'] if label=='echo-hide' else ['decode: ENTITY_AVAILABLE: EAVL answered SUCCESS at cdl 12',"response is 32",'rom: ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12']
    gate=(r/folder/f'{variant}.gate.log').read_text()
    assert all(word in gate for word in words),(label,gate)
    records.append({'probe':label,'codes':dict(zip(steps,codes)),'required_failure_words':words})
for name in ['command-selftest-optimized','head-check']:
    assert (r/'logs'/f'{name}.rc').read_text().strip()=='0'
    assert '231 planted defects, 231 caught by name, OK' in (r/'logs'/f'{name}.log').read_text()
assert len((r/'planted-drifts.tsv').read_text().splitlines())==232
positive=json.loads((r/'membership-positive.json').read_text())
assert len(positive)==2 and all(not x['findings'] for x in positive)
disabled=json.loads((r/'disabled-checks.json').read_text())
assert len(disabled)==3 and all(x['selftest_rc']==1 for x in disabled)
(r/'external-control-results.json').write_text(json.dumps(records,indent=2)+'\n')
print('External echo probes: all expected statuses and named failures match')
print('Standing controls: 231/231 normally and optimized; all 30 held fields planted')
print('Round-4 controls: both membership positives pass; all three disabled checks fail their named self-test')
