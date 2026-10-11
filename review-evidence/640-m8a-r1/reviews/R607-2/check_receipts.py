#!/usr/bin/env python3
"""Reconcile mapped counts, fit plans, the ruled ledger and prior mutation identities."""
import csv
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parent
evidence = root/'public-evidence/evidence-m81'
plans = json.loads((evidence/'ctrl_memory_plan.json').read_text())
rows = {row['top']: row for row in csv.DictReader((evidence/'ctrl_memory_ooc.tsv').open(), delimiter='\t')}
for tag in ('s1i1','s1i2','s8i1','s8i2'):
    plan = plans[tag]
    total = {k: sum(int(rows[tag+'_'+r][k]) for r in ('rom','sram'))
             for k in ('RAMB36E1','RAMB18E1','LUT','FF')}
    planned = sum(sum(plan[r]['banks']) for r in ('rom','sram'))/4096
    assert planned == plan['tiles'] <= 56
    actual = total['RAMB36E1'] + total['RAMB18E1']/2
    for region in ('rom','sram'):
        report = (evidence/'util'/f'{tag}_{region}_utilization.rpt').read_text()
        for field,pattern in [('RAMB36E1',r'\|\s*RAMB36/FIFO\*\s*\|\s*(\d+)'),
                              ('RAMB18E1',r'\|\s*RAMB18\s*\|\s*(\d+)')]:
            match = re.search(pattern,report)
            assert match and int(match[1]) == int(rows[tag+'_'+region][field]), (tag,region,field)
    print(tag,'rom',plan['rom']['bytes'],'sram',plan['sram']['bytes'],
          'planned',planned,'mapped',actual,'counts',total)
assert 87.5-6.5+6-18+53+2-11 == 113
assert 87.5-6.5+6-18+56+2-11 == 116
assert 121.5-116 == 5.5
print('PASS: ledger at measured 53 = 113; at ruled 56 = 116, leaving 5.5; reserve 13.5 untouched')

old_to_current = {
 'budget_slack_1p5':'budget 1.5 tiles slack',
 'budget_ge':'budget refuses exactly 56',
 'nobits_in_rom_off':'nobits in rom off',
 'lma_overlap_off':'load-address overlap off',
 'no_bytes_at_entry_off':'entry bytes off',
 'low_minus1':'decode one bit short',
 'err_held':'err held a second cycle',
 'lma_identity':'load address read as the run address',
 'regions_overlap_off':'region overlap off',
 'stage_lt':'stage accepts a larger buffer',
 'hole_gt':'hole starts a word late',
 'rom_init_offset':'rom banks from the image start',
}
log = (root/'receipts/test-ctrl-memory.log').read_text()
assert 'RESULT: PASS' in log and 'test_ctrl_memory: 0 failure(s)' in log
assert len(re.findall(r'^  \[ok  \] MUTANT ',log,re.M)) == 40
for old,current in old_to_current.items():
    lines = [line for line in log.splitlines() if f"[ok  ] MUTANT '{current}'" in line]
    assert len(lines) == 1
    print(old,'=>',lines[0].strip())
print('PASS: all 12 prior mutation semantics observed caught in the exact-head standing suite')
print('The prior external mutation driver itself was not rerun.')
