#!/usr/bin/env python3
"""Compare raw suite output without deleting, sorting or masking any simulation line."""
import pathlib,hashlib,json,difflib,sys
P=pathlib.Path(__file__).resolve().parents[1];R=P/'receipts';rows=[]
for suite in ('crf_rx','maap','mmcm_servo','aaf_clock_meter'):
 for v in ('base','head'):
  assert (R/(v+'.'+suite+'.rc')).read_text().strip()=='0',(v,suite)
 a=(R/('base.'+suite+'.output.log')).read_bytes();b=(R/('head.'+suite+'.output.log')).read_bytes()
 # Exact bytes also retain every named mutation rejection, not only aggregate verdicts.
 row={'suite':suite,'identical':a==b,'base_sha256':hashlib.sha256(a).hexdigest(),'head_sha256':hashlib.sha256(b).hexdigest(),'base_bytes':len(a),'head_bytes':len(b),'lines':len(a.splitlines()),'named_rejections':sum(b'named rejection:' in l for l in a.splitlines())}
 rows.append(row)
 if a!=b:print(''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='base',tofile='head')))
# An altered figure or exchanged check/value association must fail the literal comparison.
control=b'[PASS] check-one got=1 exp=1\n[PASS] check-two got=2 exp=2\n'
assert control != control.replace(b'got=1',b'got=9')
assert control != b'[PASS] check-one got=2 exp=2\n[PASS] check-two got=1 exp=1\n'
print(json.dumps({'suites':rows,'comparison_negative_controls':'PASS'},indent=2))
assert all(x['identical'] for x in rows)
