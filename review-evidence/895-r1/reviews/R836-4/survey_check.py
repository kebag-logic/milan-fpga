#!/usr/bin/env python3
"""Check every published survey row against live tables and the rounding rule."""
from pathlib import Path
import math
import sys
src,ev=map(Path,sys.argv[1:])
sys.path.insert(0,str(src/'tb/verilator/ctrl_service_budget'))
import load_grade as lg
import poll_grade as pg
import whole_grade as wg
import rows_grade as rg
import rows_tiers as rt
import edit_rows as er
for point,n,label in [('1x1/1if',1,'1x1'),('8x8/2if',2,'8x8')]:
    tables={'load_grade.STATED_US':lg.STATED_US[point], 'load_grade.STATED_US_DONOR':lg.STATED_US_DONOR[point],
      'poll_grade.STATED_US':pg.STATED_US[n], 'whole_grade.stated_us':wg.stated_us(n),
      'rows_grade.ROW_COSTS':rg.ROW_COSTS[point], 'rows_tiers.DATAPATH_US':rt.DATAPATH_US[point],
      'rows_tiers.LONG_NOTICE_US':{'aecp_long':rt.LONG_NOTICE_US[point]},
      'rows_tiers.LONG_RECORD_US':{'record.aecp.long':rt.LONG_RECORD_US[point]},
      'edit_rows.EDIT_RECORD_US':{'record.aecp.edit':er.EDIT_RECORD_US[point]}}
    rows=0; unstaged=[]; bad=[]
    for line in (ev/f'author-r8/receipts/survey/survey-{label}-head-f93317cb.txt').read_text().splitlines():
        if not line.startswith('| '): continue
        f=[x.strip() for x in line.split('|')[1:-1]]
        if f[0] not in tables: continue
        table,key,stated,cycles,rule,where,verdict=f
        said=int(stated); cy=int(cycles.replace(',','')); rounded=math.ceil(cy*1.05/500-1e-9)*5
        actual=tables[table][key]; rows+=1
        if said!=actual or int(rule)!=rounded or actual<rounded: bad.append((table,key,said,actual,cy,rule,rounded))
        if verdict=='not staged': unstaged.append(table+'.'+key)
        print(point,table,key,'actual',actual,'cycles',cy,'rule',rounded,verdict)
    print('SURVEY',point,'rows',rows,'bad',bad,'not staged',unstaged)
    assert not bad
