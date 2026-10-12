#!/usr/bin/env python3
"""Decode a published B16c poll trace (eight raw words per poll) by
docs/reference/REGISTER_MAP.md, independently of the author's receipt tool.
Marks (seconds against the DUT's set) come from the receipt only for span cuts.
usage: decode_poll_trace.py <trace.tsv> <receipt.json>"""
import csv, json, sys
STATES = {0: 'IDLE', 1: 'VERIFY', 2: 'REPAIR', 3: 'ACQUIRE', 4: 'LOCKED', 5: 'HOLDOVER', 6: 'FAULT'}
def s16(x): return x - 0x10000 if x & 0x8000 else x
def s32(x): return x - (1 << 32) if x & 0x80000000 else x
rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
mk = json.load(open(sys.argv[2]))['marks_after_set_s']
P = []
for r in rows:
    w = {k: int(r[k], 16) for k in ('0x8f8', '0x8e0', '0x8e4', '0x8d4', '0x8d8', '0x738', '0x748')}
    P.append(dict(t=float(r['start_after_set_s']), end=float(r['start_after_set_s']) + float(r['length_ms']) / 1000,
                  st=STATES[w['0x8f8'] & 7], lo16=w['0x8f8'] & 0xFFFF, trim=s16(w['0x8f8'] >> 16) / 16,
                  aafm=w['0x8e0'], aafr=s32(w['0x8e4']) / 512, lb=w['0x8d4'] & 0xFFFF, lbs=w['0x8d4'] >> 16,
                  tdm=w['0x8d8'], crfl=w['0x738'] >> 31, crfr=s32(w['0x748']) / 512))
out = {'polls': len(P)}
# LOCKED bracket: last non-LOCKED poll after the set, first LOCKED poll
after = [p for p in P if p['t'] >= 0]
first_locked = next(i for i, p in enumerate(after) if p['st'] == 'LOCKED')
out['locked_bracket_s'] = [round(after[first_locked - 1]['t'], 3), round(after[first_locked]['t'], 3), round(after[first_locked]['end'], 3)]
out['states_set_to_lock'] = sorted({p['st'] for p in after[:first_locked]})
out['left_locked_after_first'] = [round(p['t'], 3) for p in after[first_locked:] if p['st'] != 'LOCKED' and p['t'] < mk['window-end']]
win = [p for p in P if mk['window-start'] <= p['t'] < mk['window-end']]
out['window_polls'] = len(win)
out['window_states'] = {s: sum(p['st'] == s for p in win) for s in {p['st'] for p in win}}
out['window_lo16'] = {f'{v:04x}': sum(p['lo16'] == v for p in win) for v in {p['lo16'] for p in win}}
out['window_trim_ppm'] = [min(p['trim'] for p in win), max(p['trim'] for p in win)]
out['window_crf_rate_ppm'] = [round(min(p['crfr'] for p in win), 3), round(max(p['crfr'] for p in win), 3)]
out['window_crf_locked_polls'] = sum(p['crfl'] for p in win)
out['window_aafm_stat'] = sorted({f'{p["aafm"]:08x}' for p in win})
if any(p['aafm'] for p in win):
    out['window_aafm_rate_ppm'] = [round(min(p['aafr'] for p in win), 3), round(max(p['aafr'] for p in win), 3)]
out['slip_tdm_values'] = sorted({p['tdm'] for p in P})
out['slip_lb_skips'] = sorted({p['lbs'] for p in P})
out['slip_lb_range'] = [P[0]['lb'], P[-1]['lb']]
steps = []
for a, b in zip(P, P[1:]):
    if b['lb'] != a['lb']:
        steps.append(dict(from_s=round(a['t'], 3), to_s=round(b['t'], 3), dups=[a['lb'], b['lb']], states=[a['st'], b['st']]))
out['slip_lb_steps'] = steps
out['marks'] = mk
lockt = after[first_locked]['t']
out['steps_after_first_locked'] = [s for s in steps if s['to_s'] > lockt]
out['last_poll_s'] = round(P[-1]['t'], 3)
out['polls_after_restore'] = sum(p['t'] > mk['restored'] for p in P)
print(json.dumps(out, indent=1))
