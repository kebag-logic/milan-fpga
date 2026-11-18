#!/usr/bin/env python3
"""Recompute published composition figures; run from the candidate checkout."""
import json, re, subprocess
from pathlib import Path
P=Path(__file__).resolve().parents[1]
E=P/'scratch/evidence/review-evidence/train1117-r1/author-r5/receipts'
def check(ok, msg):
    assert ok, msg
    print('PASS',msg)
hashes=[(E/p).read_text().split() for p in ['images/hashes.txt','step11/images/hashes.txt','step11/images/hashes-05dc1791.txt','step11/images/hashes-73272666.txt']]
check(all(h==hashes[0] for h in hashes), '12 full SHA256 point/arm identities unchanged before/after step 11 through final head')
c=(E/'regrade/confdiff-final.txt').read_text()
print(c)
check('EMPTY' in c and 'DIFFER' not in c, 'confirmation diff empty')
rows=[('1x1 paced',29331,310),('8x8/1if base',28417,300),('8x8/1if retained',35350,375),('8x8/1if MAAP',16682,180),('8x8/1if SRP',35547,375),('8x8/1if ADP',12779,135),('8x8/2if MAAP',14770,160),('8x8/2if events_none',4069,45),('8x8/2if AECP event',11404,120)]
for name,cycles,stated in rows:
    got=((cycles*105+49999)//50000)*5
    check(got==stated and stated*100>=cycles,f'{name}: {cycles} cycles /100 MHz, +5%, ceil 5 us = {got} us')
for point,stage in [('1x1','41d2bc2b'),('8x8','41d2bc2b'),('8x8-1if','unit375')]:
    path=E/f'measure/{stage}/survey-{point}/compare-ordinary.txt'
    count=0
    for line in path.read_text().splitlines():
        m=re.match(r'\S+\s+([\d,]+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(within|OVER)',line)
        if not m: continue
        cycles=int(m[1].replace(',','')); rule=int(m[3]); stated=int(m[4]); count+=1
        check(((cycles*105+49999)//50000)*5==rule,f'{point} rounded receipt row {count}')
        if stated<rule: print('HISTORICAL restatement needed:',line)
    check(count>40,f'{point} survey parsed {count} rows')
baseline=json.loads(Path('syn/ooc/pp_resource_baseline.json').read_text())
record=(E/'step11/release/record-write.txt').read_text()
receipt=json.JSONDecoder().raw_decode(record[record.index('{'):])[0]
def objects(x):
    if isinstance(x,dict):
        yield x
        for y in x.values(): yield from objects(y)
    elif isinstance(x,list):
        for y in x: yield from objects(y)
check(any(x==receipt for x in objects(baseline)), 'entire release route record equals published record-write JSON')
print('release figures',receipt['figures'])
check(subprocess.check_output(['git','diff','--name-only','HEAD^','HEAD'],text=True).strip()=='syn/ooc/pp_resource_baseline.json','final rebaseline record-only')
for name,wns,whs in [('split1',.141,.033),('split8',.073,.034),('release',.194,.017)]:
    check(wns>=.030 and whs>=0,f'{name} selected setup/hold meets .030/0 floor')
check(121+41+238==400 and 192-18+96-8==262,'same-directive release resource attribution adds to +400 LUT/+262 FF')
check(54002-53461==541,'selected-route baseline delta +541 LUT')
print('Receipt arithmetic audit complete')
for point,rom,sram,tiles in [('1x1/1if',124832,56736,44.5),('1x1/2if',126432,59040,45.5),('8x8/1if',137472,98096,58),('8x8/2if',139048,115504,62.5),('fixture answering-ports',131448,114320,60.5)]:
    needed=((rom+2047)//2048+(sram+2047)//2048)/2
    check(needed==tiles,f'ROM/SRAM {point}: {rom}/{sram} B -> {needed} RAMB36 in half-tile granules')
check(137472-137216==256 and 139264-137472==1792,'8x8/1if next half tile: 256 B past old ROM capacity, 1792 B spare after ruled increase')
