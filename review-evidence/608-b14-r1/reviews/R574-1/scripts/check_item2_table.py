#!/usr/bin/env python3
"""Compare the page's item 2 per-switch and per-return tables with the packet's
switches.json. usage: check_item2_table.py <packet-author-dir> <findings-page>"""
import json, os, re, sys
A, PAGE = sys.argv[1], sys.argv[2]
s = {r['tag']: r for r in json.load(open(os.path.join(A, 'item2', 'summary', 'switches.json')))}
mis = []; n = 0
for l in open(PAGE):
    m = re.match(r'^\| (\d\d) (INTERNAL to AAF|AAF to CRF) \| ([\d.]+)-([\d.]+) \| \+(\d+) \| (\d+) / (\d+) \| ([^|]+) \| 0/0 to 0/0 \| (\d+) to (\d+) \| 0 / 0 \| 0, 1 and 1 \|$', l.strip())
    if m:
        n += 1
        tag = 'c%s-%s' % (m.group(1), 'aaf' if m.group(2).startswith('INTERNAL') else 'crf'); r = s[tag]
        steps = '-' if not r['slip_lb_steps'] else ', '.join('%.2f' % x['s_hi'] for x in r['slip_lb_steps'])
        exp = ('%.2f' % r['locked_s'][0], '%.2f' % r['locked_s'][1], str(r['slip_lb_transient_dups']), str(r['slip_lb_after_dups']), str(r['slip_lb_after_skips']), steps, str(r['rails_before_end'][0]), str(r['rails_before_end'][1]))
        got = (m.group(3), m.group(4), m.group(5), m.group(6), m.group(7), m.group(8).strip(), m.group(9), m.group(10))
        tap = r['tap']; tapok = all(tap[k]['seq_gaps'] == 0 for k in ('peer-aaf', 'peer-crf', 'dut-aaf', 'dut-crf')) and len(tap['dut-aaf']['mr_toggles_s']) == 1 and len(tap['dut-crf']['mr_toggles_s']) == 1
        cnt = r['counters_locked_to_end']
        mu = sum(cnt.get(d, {}).get('MEDIA_UNLOCKED', 0) for d in ('dut-0x0005-0', 'dut-0x0005-1'))
        if got != exp or not tapok or mu or r['slip_tdm_before_end'] != [[0, 0], [0, 0]]: mis.append((tag, got, exp, tapok, mu))
    m = re.match(r'^\| (\d\d) CRF to INTERNAL \| \+(\d+) \| (\d+) to (\d+) \| \+1, \+1, \+1 \|$', l.strip())
    if m:
        n += 1
        r = s['c%s-int' % m.group(1)]
        exp = (str(r['slip_lb_end'][0] - r['slip_lb_before'][0]), str(r['rails_before_end'][0]), str(r['rails_before_end'][1]))
        if (m.group(2), m.group(3), m.group(4)) != exp: mis.append(('c%s-int' % m.group(1), m.group(2, 3, 4), exp))
print('rows matched', n, 'mismatches', mis)
