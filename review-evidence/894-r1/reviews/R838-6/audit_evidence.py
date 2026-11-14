#!/usr/bin/env python3
"""Independently reconcile published measurements, identity and source bounds."""
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path.cwd()
OUT=Path(__file__).resolve().parent
PUB=OUT/'scratch/review-evidence/894-r1/author-r11'
sys.path.insert(0,str(ROOT/'tb/verilator/ctrl_service_budget'))
import edit_rows, paced_rows, record_classes, rows_tiers

def git(*args):
    return subprocess.check_output(['git',*args])

def inventory(tag):
    p=PUB/f'receipts/final/images/image-sha256-{tag}.txt'
    return {line.split(None,1)[1]:line.split()[0] for line in p.read_text().splitlines() if re.match('[0-9a-f]{64} ',line)}

base=inventory('9fda93a1')
identity={}
for tag in ('3e0ca737','6ec12ad7','control-MAP_FLOOR-264'):
    other=inventory(tag)
    assert set(base)==set(other)
    identity[tag]={'entries':len(other),'differences':sum(base[p]!=other[p] for p in base)}
assert identity['3e0ca737']['differences']==identity['6ec12ad7']['differences']==0
assert len(base)==332 and identity['control-MAP_FLOOR-264']['differences']==24
after=git('diff','--name-only','6ec12ad7..HEAD').decode().splitlines()
assert not any(p.endswith(('.c','.cpp','.h','.sv','.v','.ld')) for p in after)

values=[22728,20595,24360,30563,4612,4890,2859,6193,18843,86978,145770,34280,61637,33724]
rules={c:5*math.ceil(c*105/50000) for c in values}
assert all(record_classes.rule(c,100_000_000)==rules[c] for c in values)

class_probes={}
for point in ('1x1/1if','8x8/2if'):
    i=rows_tiers.point_inputs(ROOT,point)
    for pace in (0,1,8,13):
        # The solver and paced_rows.edits contract use hundredths of a ms.
        for w in (0,0.01,6.99,7,7.01,8,15,30,130,238):
            for k in (0,1,2,16,63):
                want=k if pace==0 else min(k,math.ceil((w+1)/pace))
                assert edit_rows.edits_in(i._replace(pace_ms=pace),w,k)==want
    before={r:rows_tiers.solve(r,i,rows_tiers.BUILT)[0] for r in rows_tiers.LONG_ROWS}
    original=edit_rows.EDIT_RECORD_US[point]
    try:
        edit_rows.EDIT_RECORD_US[point]=100000
        after_long={r:rows_tiers.solve(r,i,rows_tiers.BUILT)[0] for r in rows_tiers.LONG_ROWS}
    finally:
        edit_rows.EDIT_RECORD_US[point]=original
    assert before==after_long
    class_probes[point]={'long_rows_unchanged_by_ordinary_edit_charge':before,'pace_ms':i.pace_ms}
legs,groups,stated=record_classes.synthetic()
assert not record_classes.findings(legs,groups,lambda p:stated)[0]
del legs[0].groups['aecp-fanout']
missing=record_classes.findings(legs,groups,lambda p:stated)[0]
assert any('missing aecp-fanout' in x for x in missing)

old_image=git('show','f3320c19:review-evidence/894-r1/author-r10/receipts/images/every-image-head.txt').decode()
(OUT/'receipts/previous-image-sizes.txt').write_text(old_image)
image_deltas={
 'fixture-1x1-1if':{'previous':110576,'published_current':110800,'delta':224},
 'platform-8x8-2if':{'previous':130496,'published_current':130704,'delta':208}}
assert 'rom 110576 ' in old_image and 'rom 130496 ' in old_image
docs=(ROOT/'docs/design/SPLIT_CONTROL_MEMORY.md').read_text()
assert 'adds 220 B of rom to every image' in docs
assert 'every 1x1/1if row holds by every source, R4 12.85 ms' in docs

survey={}
for key,name in [('1x1','compare-A-at-6ec12ad7-statements.txt'),('8x8','compare-8x8-at-final-statements.txt')]:
    txt=(PUB/'receipts/final/armA'/name).read_text().split('\n# ')[0]
    rows=[]
    for line in txt.splitlines():
        match=re.match(r'(.+?)\s+([\d,]+)\s+(\d+\.\d+)\s+(\d+)\s+(\d+)\s+(within|OVER(?:-raw)?)\s+(.+)',line)
        if not match: continue
        cost,cycles,us,rule,stated,verdict,source=match.groups()
        cycles=int(cycles.replace(',',''))
        assert int(rule)==5*math.ceil(cycles*105/50000),(cost,cycles,rule)
        expect='OVER-raw' if cycles/100>int(stated) else ('OVER' if int(rule)>int(stated) else 'within')
        assert verdict==expect
        rows.append({'cost':cost,'cycles':cycles,'rule':int(rule),'stated':int(stated),'verdict':verdict,'source':source})
    survey[key]={'comparisons':len(rows),'exceeded':[r for r in rows if r['verdict']!='within']}

out={'image_identity':identity,'image_kind_counts':{s:sum(p.endswith(s) for p in base) for s in ('.elf','.bin','.o')},
     'post_identity_paths':after,'rule_spotchecks':rules,'class_probes':class_probes,'missing_group_refusal':missing,
     'survey_arithmetic':survey,'image_delta_discrepancy':image_deltas,
     'archive_has_signature':b'\ngpgsig ' in git('cat-file','commit','f3320c19')}
(OUT/'receipts/evidence-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
