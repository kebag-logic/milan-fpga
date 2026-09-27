#!/usr/bin/env python3
"""Check every numeric cell of the findings page's duty, opportunity and schedule tables
against the reviewer's independent recomputation (output of independent_r2.py).

Usage: check_doc_tables.py <findings.md> <independent_r2-output.txt>
"""
import re, sys
doc, ind = open(sys.argv[1]).read(), open(sys.argv[2]).read()
shape_of = {'1x1': 'endstation_ax7101_1x1_tdm8', '8x8': 'endstation_ax7101_8x8'}
mine = {}
for block in re.split(r'^## ', ind, flags=re.M)[1:]:
    head, *lines = block.strip().splitlines()
    if head.startswith('schedules'):
        for l in lines:
            s, plan, gap, a, b, tail, samples, _ = [x.strip() for x in l.split('|')]
            mine[('sched', s, plan)] = (gap, a, b, tail, samples)
    else:
        s = head.split()[0]
        for l in lines:
            g, p, cyc, ms, span, ps, tx, cond = [x.strip() for x in l.split('|')]
            mine[('duty', s, g)] = (p, cyc, ms, span, ps, tx, cond)
bad = checked = 0
def cmp(label, got, want):
    global bad, checked
    checked += 1
    if got != want:
        bad += 1; print('MISMATCH', label, 'doc', got, 'independent', want)
cur = None
for line in doc.splitlines():
    m = re.match(r'\*\*(1x1|8x8)(: populated| duty opportunities)', line)
    if m: cur = (shape_of[m[1]], 'duty' if 'populated' in m[2] else 'opp')
    if not line.startswith('| ') or line.startswith('| ---') or line.startswith('| Duty'):
        continue
    cells = [c.strip() for c in line.strip('|').split('|')]
    if re.match(r'(1x1|8x8) / `', cells[0]) and len(cells) == 7:   # schedule table
        s, plan = cells[0].split(' / ')
        gap, a, b, tail, samples = mine[('sched', shape_of[s], plan.strip('`'))]
        cmp(cells[0] + ' gap', cells[1], gap)
        cmp(cells[0] + ' 500', cells[2], f'{500 - float(gap):.5f}')
        cmp(cells[0] + ' 2000', cells[3], f'{2000 - float(gap):.5f}')
        cmp(cells[0] + ' endpoints', cells[4], f'{a} to {b}')
        cmp(cells[0] + ' tail', cells[5], 'Yes' if tail == 'True' else 'No')
        cmp(cells[0] + ' samples', cells[6], samples.strip('[]'))
        continue
    if cur is None or ('duty', cur[0], cells[0]) not in mine:
        continue
    p, cyc, ms, span, ps, tx, cond = mine[('duty', cur[0], cells[0])]
    lab = f'{cur[0]} {cur[1]} {cells[0]}'
    if cur[1] == 'duty' and len(cells) == 6:
        cmp(lab + ' plan', cells[1], f'`{p}`'); cmp(lab + ' cycles', cells[2], cyc); cmp(lab + ' ms', cells[3], ms)
        if cells[4] != 'N/A':
            cmp(lab + ' margin', cells[5], f'{float(cells[4].replace(",", "")) - float(ms):.5f}')
    elif cur[1] == 'opp' and len(cells) == 7:
        cmp(lab + ' span', cells[1], span); cmp(lab + ' plan', cells[2], f'`{ps}`'); cmp(lab + ' tx', cells[3], tx)
        if cells[4] != 'Unarmed prefix':
            cmp(lab + ' cond', cells[4], cond)
            cmp(lab + ' 500', cells[5], f'{500 - float(cond):.5f}'); cmp(lab + ' 2000', cells[6], f'{2000 - float(cond):.5f}')
print(f'checked {checked} cells, mismatches {bad}')
sys.exit(1 if bad else 0)
