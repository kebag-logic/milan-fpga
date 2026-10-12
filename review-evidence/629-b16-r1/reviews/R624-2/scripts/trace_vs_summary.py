#!/usr/bin/env python3
"""Cross-check a published round-2 poll trace against the round-1 poll-summary
already published in the case's events.jsonl (first/last/distinct words per span,
span membership: poll start >= span start and poll end <= span end).
usage: trace_vs_summary.py <trace.tsv> <events.jsonl>"""
import csv, json, sys
rows = list(csv.DictReader(open(sys.argv[1]), delimiter='\t'))
ev = [json.loads(l) for l in open(sys.argv[2]) if l.strip()]
summ = next(e for e in ev if e['kind'] == 'poll-summary')
m = summ['marks_raw']; t_set = m['dut-set']
pts = sorted(m.items(), key=lambda kv: kv[1])
spans = {f'{a}..{b}': (ta, tb) for (a, ta), (b, tb) in zip(pts, pts[1:])}
spans[f'{pts[-1][0]}..poll-end'] = (pts[-1][1], None)
W = [k for k in rows[0] if k.startswith('0x')]
P = [dict(r0=float(r['start_after_set_s']), r1=float(r['start_after_set_s']) + float(r['length_ms']) / 1000,
          w={k: r[k] for k in W}) for r in rows]
ok = bad = 0
for tag, (a, b) in spans.items():
    a_s = (a - t_set) / 1e9; b_s = None if b is None else (b - t_set) / 1e9
    rs = [p for p in P if p['r0'] >= a_s - 0.0005 and (b_s is None or p['r1'] <= b_s + 0.0005)]
    pub = summ['spans'][tag]
    probs = []
    if len(rs) != pub['polls']:
        probs.append(f'polls {len(rs)} vs {pub["polls"]}')
    for k in pub.get('first', {}):
        if k not in W:
            continue
        if rs and rs[0]['w'][k] != pub['first'][k]: probs.append(f'first {k} {rs[0]["w"][k]} vs {pub["first"][k]}')
        if rs and rs[-1]['w'][k] != pub['last'][k]: probs.append(f'last {k} {rs[-1]["w"][k]} vs {pub["last"][k]}')
        d = len({p['w'][k] for p in rs})
        if d != pub['distinct'][k]: probs.append(f'distinct {k} {d} vs {pub["distinct"][k]}')
    print(('OK ' if not probs else 'BAD') + f' {tag}: {len(rs)} polls ' + '; '.join(probs))
    ok += not probs; bad += bool(probs)
print(f'ok={ok} bad={bad}')
