"""Re-derive THE RETRY's implied cold cost per (n, k) tally row from the author's published tally JSON:
implied = dearest_cycles/100 - n*W - k*34, W = 365 us at two interfaces and 255 at one; check each against the
ruling's trigger 1 (183.1 us), the stated 185 us + n*365 + k*34 line at 8x8/2if, and report the dearest.
usage: python3 -I rederive_trigger1.py TALLY_JSON"""
import json, sys
d = json.load(open(sys.argv[1]))
bad = 0
for leg, v in d.items():
    two = v['point'] == '8x8'
    W, C = (365, 185) if two else (255, 85)
    for key, t in v['tally'].items():
        n, k = (int(x.split('=')[1]) for x in key.split())
        implied = t['dearest'] / 100 - n * W - k * 34
        stated = (C + n * W + k * 34) * 100
        ok = abs(implied - t['cold_us']) < 0.01 or t['cold_us'] >= implied   # the author keeps the max over rounds
        over1 = implied > 183.1
        print(f"{leg:6s} {key:9s} dearest {t['dearest']:>7} implied {implied:8.2f} author {t['cold_us']:8.2f} "
              f"stated-line {stated:>7} {'OVER-STATED' if t['dearest'] > stated else 'within'} "
              f"{'TRIGGER1' if over1 else ''}")
        bad += over1 or t['dearest'] > stated and n == 0
print('rows over trigger 1 or a k-only round over its stated line:', bad)
sys.exit(1 if bad else 0)
