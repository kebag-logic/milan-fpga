"""Sweep hits marked HIST whose only history markers are weak words that also occur in current prose.
Usage: python3 -I weak_markers.py <sweep.tsv> <out.txt>"""
import re
import sys
STRONG = re.compile(r"\b(was|were|had|before|earlier|previously|at round|round \d+'s|stated before|before it|"
                    r"at the merge|by then|used to|no longer|superseded|history|historical|refuted|then)\b", re.I)
WEAK = re.compile(r"\b(first|since|once|beside|would|from \d)\b", re.I)
seen = {}
for line in open(sys.argv[1]):
    f, no, rule, val, hist, sent = line.rstrip('\n').split('\t', 5)
    if hist != 'HIST' or STRONG.search(sent):
        continue
    seen.setdefault((f, no, sent), []).append(f'{rule}[{val}]')
with open(sys.argv[2], 'w') as out:
    for (f, no, sent), hits in seen.items():
        out.write(f'{f}:{no}\t{", ".join(hits)}\t{sent[:400]}\n')
print(len(seen), 'sentences,', sum(len(v) for v in seen.values()), 'hits')
