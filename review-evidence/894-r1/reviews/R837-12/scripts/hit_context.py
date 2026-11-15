"""Print sweep hits with a window around each matched value. Usage: hit_context.py <tsv> <CUR?|HIST|ALL> <ROW|NONROW|ALL> [width]"""
import sys
tsv, mark, kind = sys.argv[1:4]
w = int(sys.argv[4]) if len(sys.argv) > 4 else 110
n = 0
for line in open(tsv):
    f, no, rule, val, hist, sent = line.rstrip('\n').split('\t', 5)
    if mark != 'ALL' and hist != mark:
        continue
    if kind == 'ROW' and rule != 'ROW' or kind == 'NONROW' and rule in ('ROW',):
        continue
    i = sent.find(val)
    ctx = sent[max(0, i - w): i + len(val) + w // 2] if i >= 0 else sent[:2 * w]
    n += 1
    print(f'{n}\t{f}:{no}\t{rule}\t[{val}]\t{ctx}')
