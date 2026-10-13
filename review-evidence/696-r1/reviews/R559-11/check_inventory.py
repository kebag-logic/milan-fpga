#!/usr/bin/env python3
"""Compare the current inventory's 66 LUT figures to the accepted record."""
import argparse,json,re
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);a=p.parse_args()
e=json.loads((a.root/'syn/ooc/pp_resource_baseline.json').read_text())['endpoints']
s=(a.root/'docs/design/MARK_II_AREA_PLAN.md').read_text()
s=s.split('## Current processor inventory',1)[1].split('\n## ',1)[0]
rows=[]
for l in s.splitlines():
 m=re.match(r'\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|',l)
 if not m:continue
 name=m[1];actual=[int(m[i].replace(',','')) for i in range(2,5)]
 expected=[e[ep]['record']['scopes'][name]['LUT'] for ep in ['route-1x1','ooc-1x1','ooc-8x8']]
 assert actual==expected,(name,actual,expected)
 rows.append({'scope':name,'LUT':actual})
assert len(rows)==22,len(rows)
print(json.dumps({'checks':66,'mismatches':0,'rows':rows},indent=2))
