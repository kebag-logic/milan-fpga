#!/usr/bin/env python3
"""Cross-check the round-7 doc figures against the committed record and the published run receipts.
Usage: crosscheck_docs.py REPO RUN_RECEIPTS_JSON"""
import json, pathlib, re, sys
repo, receipts = pathlib.Path(sys.argv[1]), json.loads(pathlib.Path(sys.argv[2]).read_text())
page = (repo / 'docs/findings/234_PP_SHADOW_AREA_BASELINE.md').read_text()
budget = (repo / 'docs/design/AREA_BUDGET.md').read_text()
rec = json.loads((repo / 'syn/ooc/pp_resource_baseline.json').read_text())['endpoints']
bad = 0
def check(label, cond):
    global bad
    bad += not cond
    print(('ok   ' if cond else 'FAIL ') + label)
sec = page[page.index('## Re-baseline of 2026-10-03'):page.index('## Combinations')]
for r in receipts:
    if r['combination'] != 'C':
        continue
    row = f"| C | {r['run']} | {r['rc']} | {r['minutes']} | `{r['log']}` | `{r['log_digest']['sha256'][:16]}` | {r['log_digest']['bytes']:,} |"
    check(f'receipt row present: {row}', row in sec)
r, o1, o8 = (rec[k]['record']['figures'] for k in ('route-1x1', 'ooc-1x1', 'ooc-8x8'))
f = lambda n: f'{n:,}'
check('route C row', f"| C, dev `54643724` | {f(r['LUT'])} | {f(r['FF'])} | {f(r['SLICE'])} | {r['RAMB36']} | {r['RAMB18']} | {r['BRAM_TILE']} | {r['DSP']} | {f(r['CARRY4'])} | +{r['WNS_ns']} | +{r['WHS_ns']} |" in sec)
check('ooc 1x1 C row', f"| 1x1, C | {f(o1['LUT'])} | {f(o1['FF'])} | {o1['RAMB36']} | {o1['RAMB18']} | {o1['BRAM_TILE']} | {o1['DSP']} | {f(o1['CARRY4'])} | {o1['WNS_ns']} |" in sec)
check('ooc 8x8 C row', f"| 8x8, C | {f(o8['LUT'])} | {f(o8['FF'])} | {o8['RAMB36']} | {o8['RAMB18']} | {o8['BRAM_TILE']} | {o8['DSP']} | {f(o8['CARRY4'])} | {o8['WNS_ns']} |" in sec)
pct = lambda a, b: f'{100 * a / b:.2f}'
check('budget LUT row', f"| Slice LUT | 63,400 | {f(r['LUT'])} | {pct(r['LUT'], 63400)} % | NFR-RES-01: at most 38,040 (60 %) | not met, {f(r['LUT'] - 38040)} over |" in budget)
check('budget FF row', f"| Slice register | 126,800 | {f(r['FF'])} | {pct(r['FF'], 126800)} % |" in budget)
check('budget slice row', f"| Slice | 15,850 | {f(r['SLICE'])} | {pct(r['SLICE'], 15850)} % | must stay below the device to place | {15850 - r['SLICE']} free |" in budget)
check('budget BRAM row', f"| Block RAM tile | 135 | {r['BRAM_TILE']} | {pct(r['BRAM_TILE'], 135)} % |" in budget and f"{135 - r['BRAM_TILE']} free" in budget)
check('budget DSP row', f"| DSP | 240 | {r['DSP']} | {pct(r['DSP'], 240)} % |" in budget)
check('budget timing row', f"+{r['WNS_ns']} / +{r['WHS_ns']} ns" in budget)
check('budget slices-left sentence', f"placement has {15850 - r['SLICE']} slices left" in budget)
w = rec['route-1x1']['record']['scopes']['wrapper']['LUT']
check('budget standalone wrapper', f"The standalone wrapper uses {f(o1['LUT'])} LUTs, {100 * o1['LUT'] / 63400:.1f} % of the device" in budget)
check('budget routed wrapper', f"The wrapper names {f(w)} of them" in budget)
need = 38040 - (r['LUT'] - w)
check(f'budget wrapper target {need}', f"needs the wrapper below {f(need)} LUTs" in budget)
check(f'budget cut {r["LUT"] - 38040} and {round(100 * (r["LUT"] - 38040) / w)} %', f"That is a {f(r['LUT'] - 38040)}-LUT cut, {round(100 * (r['LUT'] - 38040) / w)} % of the wrapper" in budget)
check('budget timing fall', f"after a fall of {r['WNS_ns'] - 0.03:.3f} ns" in budget)
check('budget milan_datapath 42,200 = 66.6 %', '42,200 LUTs in the routed image, 66.6 %' in budget and abs(100 * 42200 / 63400 - 66.6) < 0.05)
for label, a, b in (('meter+wrapper+rest LUT', 483 - 33 + 223, 42200 - 41527), ('meter+wrapper+rest FF', 630 + 2 - 3, 48433 - 47804),
                    ('rest A LUT', 41527 - 23937, 17590), ('rest C LUT', 42200 - 23904 - 483, 17813),
                    ('rest A FF', 47804 - 24263, 23541), ('rest C FF', 48433 - 24265 - 630, 23538),
                    ('image LUT residual', 639 - (673 - 2 - 10), -22), ('image FF', 629 - 1 + 0, 628),
                    ('wrapper delta LUT', w - 23937, -33), ('route LUT over tol', r['LUT'] - 50128 - 500, 139),
                    ('route FF over tol', r['FF'] - 59006 - 600, 28), ('meter share %', round(100 * 483 / 639), 76),
                    ('levers residual', round((r['LUT'] - 3600) / 100) * 100, 47200), ('levers over', round((r['LUT'] - 3600 - 38040) / 100) * 100, 9100)):
    check(f'{label}: {a} == {b}', a == b)
print('CROSSCHECK PASS' if not bad else f'CROSSCHECK {bad} FAIL')
