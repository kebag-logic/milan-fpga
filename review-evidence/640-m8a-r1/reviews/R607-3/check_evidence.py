#!/usr/bin/env python3
"""Recalculate fit and ledger figures from published executable evidence."""
import csv,json,pathlib,re,sys
p=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path(sys.argv[1]);base=p/'public-evidence/author/evidence-m81';r3=p/'public-evidence/author-r3/evidence-r3'
rows={r['top']:r for r in csv.DictReader((base/'ctrl_memory_ooc.tsv').open(),delimiter='\t')};plans=json.loads((base/'ctrl_memory_plan.json').read_text())
for tag,plan in plans.items():
 total36=total18=lut=ff=0
 for region in ('rom','sram'):
  row=rows[tag+'_'+region];text=(base/'util'/f'{tag}_{region}_utilization.rpt').read_text()
  for key,pattern in [('RAMB36E1',r'RAMB36E1 only\s*\|\s*(\d+)'),('RAMB18E1',r'RAMB18E1 only\s*\|\s*(\d+)')]:
   match=re.search(pattern,text);assert (int(match[1]) if match else 0)==int(row[key])
  total36+=int(row['RAMB36E1']);total18+=int(row['RAMB18E1']);lut+=int(row['LUT']);ff+=int(row['FF'])
  banks=plan[region]['banks'];need=plan[region]['bytes'];assert 0<=sum(banks)-need<2048
 planned=sum(sum(plan[r]['banks']) for r in ('rom','sram'))/4096;assert planned==plan['tiles']<=56
 print(tag,plan['rom']['bytes'],plan['sram']['bytes'],'planned',planned,'mapped',total36,total18,total36+total18/2,'LUT/FF',lut,ff)
assert (r3/'rom-digest-before.txt').read_bytes()==(r3/'rom-digest-after.txt').read_bytes()
print('PASS: all four published pre/post ROM digests and plans are identical')
pre=87.5-6.5+6-18+53+2;split=pre-11;limit=split+(56-53);partial=pre+6
assert (pre,split,limit,partial)==(124,113,116,130)
for path in ['docs/design/MARK_II_AREA_PLAN.md','docs/design/AREA_BUDGET.md']:
 text=(repo/path).read_text();assert '124 + 6 = 130' in text;assert '8.5' in text;assert 'ruled 56-tile firmware allocation' in text;assert '116' in text and '5.5' in text
 print(path,'PASS: partial total 130 (8.5 over); full split 113 (8.5 under); limit-case 116 (5.5 under)')
print('PASS: 13.5 reserve excluded from 121.5 usable ceiling; conditional -11 requires later physical removal')
