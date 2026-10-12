#!/usr/bin/env python3
"""Rebuild the b16b-points and b16c-points rows from the packet's per-point
summaries and compare them cell by cell with the findings page.
usage: check_point_tables.py <findings.md> <packet author-r2 root>"""
import json, re, sys
doc, R = sys.argv[1], sys.argv[2]
FILES = {'(a)': 'a-peer-tap.json', '(b)': 'b-dut-tap.json', '(c)': 'c-mcasp.json'}
def fmt(x, n): return f'{x:,.{n}f}' if abs(x) >= 1000 else f'{x:.{n}f}'
def row(run, pt):
    d = json.load(open(f'{R}/summary/{run}/{FILES[pt]}'))
    chans = {c['channel']: c for c in d['channels']}
    fr = f"{d['frames']:,}"
    if pt != '(c)':
        fr += f"; {d['info']['pdus']:,} PDUs, {d['info']['seq_gaps']} gaps"
    cells = [fr]
    lev = None
    for tone, ch in (('997', 0), ('9973', 1)):
        t = chans[ch][f'tone_{tone}']['median']
        lev = lev or t['level_dbfs']
        w = chans[ch][f'tone_{tone}']['worst_thdn_db']
        f = f"{t['f_hz']:,.4f} Hz" if tone == '9973' else f"{t['f_hz']:.4f} Hz"
        p = t['ppm']
        cells.append((f, p, f"{t['thdn_db']:.2f} ({w:.2f})", f"{t['snr_db']:.2f}"))
    return lev, cells
ok = bad = 0
mark = None
for n, line in enumerate(open(doc, encoding='utf-8'), 1):
    s = line.strip()
    if s in ('<!-- b16b-points -->', '<!-- b16c-points -->'):
        mark = s; continue
    if mark and not s:
        mark = None; continue
    if not mark or not s.startswith('| `'):
        continue
    c = [x.strip() for x in s.strip('|').split('|')]
    run = re.match(r'`([^`]+)`', c[0]).group(1); pt = c[1]
    lev, cells = row(run, pt)
    probs = []
    if c[2] != cells[0]: probs.append(f'frames {c[2]!r} vs {cells[0]!r}')
    if abs(float(c[3]) - lev) > 0.00005: probs.append(f'level {c[3]} vs {lev}')
    for i, (f, p, th, snr) in enumerate(cells[1:]):
        fc, thc, snrc = c[4 + 3 * i], c[5 + 3 * i], c[6 + 3 * i]
        fd, pd = fc.split(', ')
        if fd != f: probs.append(f'freq {fd} vs {f}')
        pv = float(pd.replace(' ppm', ''))
        dec = len(pd.split('.')[1].split(' ')[0])
        if abs(pv - p) > 0.5 * 10 ** -dec + 1e-9: probs.append(f'ppm {pd} vs {p}')
        if thc != th: probs.append(f'thdn {thc} vs {th}')
        if snrc != snr: probs.append(f'snr {snrc} vs {snr}')
    print(('OK ' if not probs else 'BAD') + f' line {n} {run} {pt} ' + '; '.join(probs))
    ok += not probs; bad += bool(probs)
print(f'ok={ok} bad={bad}')
