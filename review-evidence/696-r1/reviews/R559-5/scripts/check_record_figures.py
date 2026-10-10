#!/usr/bin/env python3
"""Cross-check record figures cited in the area docs against syn/ooc/pp_resource_baseline.json.
Usage: python3 -I check_record_figures.py <repo> <rev> <base_rev>
Prints each check and exits 1 on any mismatch."""
import json, subprocess, sys
repo, rev, base = sys.argv[1:4]
def show(r, p):
    return subprocess.check_output(['git', '-C', repo, 'show', f'{r}:{p}'], text=True)
J = json.loads(show(rev, 'syn/ooc/pp_resource_baseline.json'))['endpoints']
JB = json.loads(show(base, 'syn/ooc/pp_resource_baseline.json'))['endpoints']
ab = show(rev, 'docs/design/AREA_BUDGET.md').splitlines()
mk = show(rev, 'docs/design/MARK_II_AREA_PLAN.md').splitlines()
f234 = show(rev, 'docs/findings/234_PP_SHADOW_AREA_BASELINE.md').splitlines()
fail = 0
def chk(name, cond):
    global fail
    print(('PASS ' if cond else 'FAIL ') + name)
    fail |= not cond
r = J['route-1x1']['record']['figures']; rb = JB['route-1x1']['record']['figures']
fmt = lambda n: f'{n:,}'
print('head route-1x1', r); print('base', base, 'route-1x1', rb)
chk(f'base {base} route LUT is 50,267 (#645 record)', rb['LUT'] == 50267)
chk('head route LUT is 50,230', r['LUT'] == 50230)
chk('RAMB36/RAMB18 74/27 unchanged base->head', (r['RAMB36'], r['RAMB18']) == (rb['RAMB36'], rb['RAMB18']) == (74, 27))
chk('BRAM tiles 87.5 = 74 + 27/2', r['BRAM_TILE'] == 87.5 == 74 + 27 / 2)
# AREA_BUDGET.md:368 and MARK_II_AREA_PLAN.md:653-654 exact text
chk('AREA_BUDGET:368 names #645 50,267 at base and #696 50,230 replacing it',
    "comparison record was #645's 50,267-LUT route" in ab[367] and "50,230-LUT route has since replaced it" in ab[367])
chk('AREA_BUDGET:369 74/27 = 87.5', '74 RAMB36 plus 27 RAMB18 still total 87.5 tiles' in ab[368])
chk('MARK_II:653 base record 50,267 74/27', "50,267 LUTs and 74/27" in mk[652])
chk('MARK_II:654 #696 50,230 74/27 comparison anchor', '50,230 LUTs with 74/27 unchanged; that record is the comparison anchor' in mk[653])
# record table AREA_BUDGET 122-127
row = {l.split('|')[1].strip(): l for l in ab[118:130] if l.startswith('| ')}
chk('AREA_BUDGET Slice LUT row', f"| {fmt(r['LUT'])} |" in row['Slice LUT'])
chk('AREA_BUDGET Slice register row', f"| {fmt(r['FF'])} |" in row['Slice register'])
chk('AREA_BUDGET Slice row', f"| {fmt(r['SLICE'])} |" in row['Slice'])
chk('AREA_BUDGET BRAM row', f"| {r['BRAM_TILE']} |" in row['Block RAM tile'])
chk('AREA_BUDGET DSP row', f"| {r['DSP']} |" in row['DSP'])
chk('AREA_BUDGET timing row', f"+{r['WNS_ns']:.3f} / +{r['WHS_ns']:.3f} ns" in row['WNS / WHS'])
chk('AREA_BUDGET LUT over 38,040', f"{r['LUT']-38040:,} over" in row['Slice LUT'])
chk('AREA_BUDGET slice free', f"{15850-r['SLICE']} free" in row['Slice'])
# 234 findings current table line 47
l47 = f234[46]
chk('234:47 route row', all(s in l47 for s in [fmt(r['LUT']), fmt(r['FF']), fmt(r['SLICE']), '74 / 27', fmt(r['CARRY4']), f"+{r['WNS_ns']:.3f}", f"+{r['WHS_ns']:.3f}"]))
# MARK_II current inventory route column equals recorded scopes
sc = J['route-1x1']['record']['scopes']
inv = [l for l in mk[107:150] if l.startswith('| `')]
n = 0
for l in inv:
    cells = [c.strip() for c in l.split('|')]
    key = cells[1].strip('`')
    k2 = key
    if k2 not in sc and k2.startswith('u_pp/'):
        pass
    if k2 in sc:
        n += 1
        chk(f'MARK_II inventory route {key}', cells[2] == fmt(sc[k2]['LUT']))
    else:
        print('SKIP scope not in record', key)
print('inventory rows matched', n, 'of', len(inv))
# standalone records unchanged base->head
for ep in ('ooc-1x1', 'ooc-8x8'):
    chk(f'{ep} figures unchanged base->head', J[ep]['record']['figures'] == JB[ep]['record']['figures'])
sys.exit(1 if fail else 0)
