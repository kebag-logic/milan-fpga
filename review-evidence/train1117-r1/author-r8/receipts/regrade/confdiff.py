#!/usr/bin/env python3
"""confdiff.py: RULING-1118c item 4's confirmation run against the candidate's receipts. For each group run on p11's
RTL (r5conf/<point>-<arm>/), the candidate's own run of that group (U's legs at 8x8/1if, B's at 1x1/1if and 8x8/2if,
whose images the candidate's hash-equal): the stimulus script (.txt), the simulation's log and the graded figures
(results.json's group entry, the passes' heaviest polls, the stated heaviest, and every SPAN line's cycles) compared.
An empty diff is every one equal."""
import hashlib
import json
import sys
from pathlib import Path

S = Path('<scratch>')
RUNS = [('8x8-1if', 'vd', 'srp-talker-held', 'unit375'), ('8x8-1if', 'ap', 'aecp', 'unit375'),
        ('8x8-1if', 'ap', 'aecp-largest-notice', 'unit375'), ('8x8-1if', 'ap', 'aecp-fanout', 'unit375'),
        ('1x1', 'ap', 'aecp-largest-notice', '41d2bc2b'), ('1x1', 'ap', 'aecp-fanout', '41d2bc2b'),
        ('8x8', 'ap', 'aecp-fanout', '41d2bc2b')]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else '-'


def spans(p: Path) -> list[str]:
    return [l.split()[3] + ' ' + l.split()[-1] for l in p.read_text(errors='replace').splitlines()
            if l.startswith('SPAN ') and len(l.split()) > 5]


def entry(results: Path, group: str):
    if not results.is_file():
        return None
    for g in json.loads(results.read_text())['results']:
        if g['group'] == group:
            return g
    return None


bad = 0
print('# the confirmation run on p11 (3e908539) against the candidate\'s receipts (U at 8x8/1if, B elsewhere)')
for point, arm, group, ref in RUNS:
    new = S / f'r5conf/{point}-{arm}'
    olds = sorted((S / f'r4meas/{ref}/{point}/{arm}').glob(f'part*/{group}.log'))
    if not (new / f'{group}.log').is_file() or not olds:
        print(f'{point} {arm} {group}: not run yet'); bad += 1; continue
    old = olds[0].parent
    if 'RESULT' not in (new / f'{group}.log').read_text(errors='replace')[-4000:]:
        print(f'{point} {arm} {group}: still running'); bad += 1; continue
    same_txt = sha(new / f'{group}.txt') == sha(old / f'{group}.txt')
    same_log = sha(new / f'{group}.log') == sha(old / f'{group}.log')
    a, b = spans(new / f'{group}.log'), spans(old / f'{group}.log')
    diff_spans = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - b.__len__())
    en, eo = entry(new / 'results.json', group), entry(old / 'results.json', group)
    # the measured figures: every graded key but the statements a run is judged against (limits) and what fell over
    # them (over), which follow the tables of the tree that graded it (U's are bf2c1184's, before the restatement)
    def figs(e):
        def strip(x):
            return {k: strip(v) for k, v in x.items() if k not in ('limits', 'over')} if isinstance(x, dict) else x
        return strip((e or {}).get('passes', {}))
    same_fig = en is not None and eo is not None and json.dumps(figs(en), sort_keys=True) == json.dumps(figs(eo), sort_keys=True)
    ok = same_txt and same_log and diff_spans == 0 and same_fig
    bad += not ok
    print(f"{point} {arm} {group} (against {ref} {old.relative_to(S / 'r4meas')}): script {'equal' if same_txt else 'DIFFERS'}, "
          f"log {'byte-identical' if same_log else 'DIFFERS'} ({sha(new / f'{group}.log')[:16]}), "
          f"{len(a)} SPAN lines, {diff_spans} differing, measured figures {'equal' if same_fig else 'DIFFER'}")
print(f'diff: {"EMPTY" if bad == 0 else f"{bad} group(s) differ or are not in"}')
sys.exit(0 if bad == 0 else 1)
