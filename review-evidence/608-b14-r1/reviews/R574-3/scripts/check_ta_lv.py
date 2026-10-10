#!/usr/bin/env python3
"""Independent check of the round 2 re-decode against item3/cycles.tsv.
usage: check_ta_lv.py <round2-recompute/outputs/ta_lv_all.txt> <author/item3/cycles.tsv>"""
import csv, re, sys
from decimal import Decimal
dec = {}
cur = None
for line in open(sys.argv[1]):
    m = re.search(r'cycle-(\d{3})/tap\.pcap', line)
    if m:
        cur = int(m.group(1)); dec[cur] = {'lv': None, 'ta': None}; continue
    m = re.search(r'bridge Listener Lv after the response\s+([0-9.]+) s', line)
    if m: dec[cur]['lv'] = Decimal(m.group(1))
    m = re.search(r'DUT Talker Advertise Lv after bridge Lv\s+([0-9.]+) s', line)
    if m: dec[cur]['ta'] = Decimal(m.group(1))
rows = {int(r['cycle'].split('-')[-1]): r for r in csv.DictReader(open(sys.argv[2]), delimiter='\t')}
print('decoded captures', len(dec), 'cycles.tsv rows', len(rows))
worst = Decimal(0); rounding_ok = 0; ta_ok = 0
for c in sorted(rows):
    tv = Decimal(rows[c]['lv_after_disconnect_s'])
    d = dec[c]['lv']
    diff = abs(d - tv) * 1000000
    worst = max(worst, diff)
    if tv.quantize(Decimal('0.000001')) == d: rounding_ok += 1
    if (dec[c]['ta'] is not None) == (rows[c]['dut_ta_lv_in_hold'].strip() not in ('0', '', 'False', 'false')): ta_ok += 1
print('largest |diff| us', worst)
print('cycles where decoder value == cycles.tsv rounded to 1 us', rounding_ok)
print('cycles where TA Lv presence agrees with dut_ta_lv_in_hold', ta_ok)
print('TA Lv cycles', [(c, str(dec[c]['ta'].quantize(Decimal('0.0001')))) for c in sorted(dec) if dec[c]['ta'] is not None])
