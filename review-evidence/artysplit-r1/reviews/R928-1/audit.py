#!/usr/bin/env python3
"""Audit public receipt integrity, source binding, measured rows and route selection.

Usage: audit.py SOURCE PUBLIC_PACKET
PUBLIC_PACKET is the extracted review-evidence/artysplit-r1 directory.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root, public = map(lambda s: Path(s).resolve(), sys.argv[1:3])
r = public/'author/receipts'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
manifest = json.loads((public/'MANIFEST.json').read_text())
present = [row for row in manifest if (public/row['file']).is_file()]
bad = [row['file'] for row in present if sha(public/row['file']) != row['published_sha256']]
assert not bad, bad
print('PUBLIC HASHES:', len(present), 'verified; no mismatches')
q = json.loads((r/'build-corrected-qualified-source.json').read_text())
bad = [row['file'] for row in q['files'] if sha(root/row['file']) != row['sha256']]
assert not bad, bad
print('EXACT HEAD SOURCE:', len(q['files']), 'qualified source files match', q['head'])
grades = []
for f in sorted(r.glob('build-corrected-final-census-*.json')):
 d = json.loads(f.read_text())
 if 'probes' in d and 'passes' in d:
  grades.append((f, d))
variants = collections.Counter()
misses = []
worst = (0, '')
for f, d in grades:
 prefix = f.name.removeprefix('build-corrected-final-census-')
 variant = prefix.removesuffix('-'+d['group']+'.json')
 variants[variant] += 1
 assert int(f.with_suffix('.status').read_text()) == 0, f.name
 assert not d['timeouts'], f.name
 assert d['passes']['share']['over'] == d['passes']['share']['idle_over'] == 0, f.name
 assert int(d['summary']['traps']) == int(d['summary']['bus_errors']) == 0, f.name
 w = d['passes']['worst']['cycles']
 worst = max(worst, (w, f.name))
 for probe in d['probes']:
  assert probe['status'] == 'measured', (f.name, probe['probe'])
  if not probe['within_budget']:
   misses.append((variant, probe['probe'],probe['ms'],probe['wait_ms']))
print('SERVICE CASES:',len(grades),'VARIANTS:',dict(variants))
assert len(grades) == 145 and len(variants) == 8
print('WORST WHOLE PASS:',worst, 'ms',worst[0]/80000)
print('RECORDED PROBE MISSES:',json.dumps(misses))
qualification = json.loads((r/'build-corrected-final-census-qualification.json').read_text())
assert all(c['returncode'] == 0 for c in qualification['commands'])
print('QUALIFICATION CHECKS:',qualification['checks'])
print('MODEL:',json.dumps(qualification['model']))
for f in sorted(r.glob('build-corrected-final-census-*-build.json')):
 d=json.loads(f.read_text())
 assert (d['cpu_cd'],d['cpu_hz'],d['sys_hz'],d['milan_hz'],d['interfaces']) == ('sys',80000000,80000000,50000000,1)
print('BUILD CLOCKS: all eight variants are sys/CPU 80 MHz, datapath 50 MHz, one interface')
images=json.loads((r/'build-corrected-images-graded-images.json').read_text())
missing_timing=[]
for candidate in images['candidates']:
 rows=[(x['corner'],x['junction_c'],x['timing']['wns'],x['timing']['whs']) for x in candidate['corners']]
 print('ROUTE SUMMARY:',candidate['directive'],candidate['status'],rows)
 for corner in candidate['corners']:
  name='build-corrected-images-'+candidate['directive']+'-'+Path(corner['report']['path']).name
  if not (r/name).exists(): missing_timing.append(name)
selected=next(c for c in images['candidates'] if c['directive']=='ExtraTimingOpt')
assert min(x['timing']['wns'] for x in selected['corners']) == .617
assert min(x['timing']['whs'] for x in selected['corners']) == .017
u=(r/'build-corrected-images-ExtraTimingOpt-digilent_arty_utilization_place.rpt').read_text()
for label,expected,total in [('Slice LUTs',33411,63400),('Slice Registers',40479,126800),('Block RAM Tile',78.5,135),('Slice',14119,15850)]:
 m=re.search(r'^\| '+label+r' +\|\s*([\d.]+)\s*\|\s*0\s*\|\s*0\s*\|\s*([\d.]+)\s*\|',u,re.M)
 assert m and (float(m[1]),float(m[2])) == (expected,total),label
 print('PLACED RESOURCE:',label,expected,'/',total,round(expected/total*100,2),'percent')
print('MISSING RAW SIGNOFF TIMING REPORTS:',len(missing_timing),json.dumps(missing_timing))
print('PUBLIC RAW .log / .log.gz FILES:',len(list(public.rglob('*.log'))),len(list(public.rglob('*.log.gz'))))
print('RECEIPT INDEX EXISTS:',(r/'INDEX.md').exists())
for name in ['build-corrected-identity-final-compare.json','build-corrected-identity-final-export-compare.json']:
 d=json.loads((r/name).read_text())
 rows=d.get('records',d.get('rows',d.get('files',[])))
 assert rows and all(x['identical'] for x in rows),name
 print('IDENTITY RECEIPT:',name,len(rows),'comparisons all identical')
size=json.loads((r/'build-corrected-arty-product-final-size.json').read_text())
print('FIRMWARE MEMORY:',json.dumps(size['split']))
print('AUDIT PASS: published grades and summaries consistent; raw timing/native trace absence is an evidence limit')
