#!/usr/bin/env python3
"""inventory.py FIGURES.tsv SWEEP.tsv OUT.md (lane 895 round 11, R835-5-F1 and S2), run from the tree: the superseded
figures' inventory. FIGURES.tsv is the figure sweep (where, figure, heuristic class, sentence); SWEEP.tsv the phrase
sweep (phrase_sweep.py, each line marked PR or base by git blame against the source base cec88385). Each figure hit the
heuristic leaves is classed by its line's enclosing section 13 heading or a named table; any left unclassed is
printed and makes the exit 1."""
import sys

inv, sweep, dst = sys.argv[1:4]
SCM = 'docs/design/SPLIT_CONTROL_MEMORY.md'
head_of, cur = {}, ''
for k, line in enumerate(open(SCM).read().splitlines(), 1):
    if line.startswith('#'):
        cur = line
    head_of[k] = cur
LEADS = {"### The final pass's restatements": "attributed: #894's head (the subsection's lead)",
         "### SRP's Talker declarations on THE TIERS": "historical: round 5's head `62298ab5` (the subsection's lead)",
         "### The composition measured again (#895)": "historical: round 6's head `bf0844f1` (the subsection's lead)",
         "### The rule's slice built (#895)": "historical: round 7A's head `4c9757ee` (the subsection's lead)",
         "### The composition with #894's SET_CONFIGURATION cut (#895)":
             "historical: round 7B's head `0c93071e` (the subsection's lead)"}
NAMED = {146: "historical: the next sentence states the head's 18,240",
         344: "historical: round 29's head's table (`b2d39235`)", 346: "historical: round 29's head's table (`b2d39235`)",
         354: "historical: round 2's head's table (`18300f6e`)",
         493: "historical: round 30's head's table", 495: "historical: round 30's head's table",
         507: "historical: `9e30c2c3`'s table",
         525: "historical: round 6's head's table (`bf0844f1`); this head's table follows",
         526: "historical: round 6's head's table (`bf0844f1`); this head's table follows",
         396: 'unrelated: another quantity (a substring of a larger number)',
         485: 'unrelated: another quantity (a substring of a larger number)',
         2441: 'historical: a tiers-table row named for its stage', 2449: 'historical: a tiers-table row named for its stage',
         2685: "historical: round 8's stop, the figure then"}
HEADS = {2672, 2673, 2694, 2701}


def manual(loc):
    f, n = loc.rsplit(':', 1)
    n = int(n)
    if f != SCM:
        return 'unrelated: another quantity'
    if head_of[n] in LEADS:
        return LEADS[head_of[n]]
    if n in NAMED:
        return NAMED[n]
    if n in HEADS:
        return "this head's: a comparison with the figure before"
    return 'REVIEW-LEFT'


rows = []
for line in open(inv):
    loc, pat, c, sent = line.rstrip('\n').split('\t', 3)
    if c == 'REVIEW':
        c = manual(loc)
    rows.append((loc, pat, c, sent.replace('|', '\\|')))
left = [r for r in rows if r[2] == 'REVIEW-LEFT']
counts = {}
for r in rows:
    counts[r[2].split(':')[0]] = counts.get(r[2].split(':')[0], 0) + 1
phr = [line.rstrip('\n').split('\t', 4) for line in open(sweep)]
out = ["# Superseded figures at round 11's head (R835-5-F1, R835-5-S2)", '',
       "Two sweeps of the tracked markdown after round 11's pass.", '',
       "**1. The figure sweep.** Every hit of each figure this head supersedes: round 10's list (the queued bound 130 "
       "ms, THE TRANSMIT's 99 ms, the slice 950 us, the tx row 33.38, the first notices 14.66 and 20.93, the last "
       "127.21, the loads 0.516, 0.512 and 0.794, the hold-off 2,029, the ctrl_plat sizes 18,176, 19,008 and 20,288, "
       "the image sizes 131,464, 126,320, 130,920, 125,792 and 111,024, and #894's R4 13.10, ACMP 28.95, txL 48.43 and "
       "806.60) and the figures R835-5 found it missed: 392 B, 245 us, 220, 33.69, 94.99, 1,656 and 1,864. Each hit is "
       "classed: this head's, attributed to #894's head, historical (past tense, a named round or commit, or under a "
       "subsection lead that names its image), or another quantity.", '',
       'Counts: ' + ', '.join(f'{k} {v}' for k, v in sorted(counts.items())) + f'; left unclassed: {len(left)}.', '',
       '**2. The phrase sweep** (R835-5-S2): every "at this head", "at the head", "this head\'s" and "now" in '
       "SPLIT_CONTROL_MEMORY.md section 13's marked subsections, FR_NFR.md 3.4.1, and the READMEs this PR touches. A "
       "README line the PR did not write (git blame: a commit before the source base `cec88385`) is `dev-soft-core`'s "
       "statement, not this PR's, and is listed as `base`. Every hit on a line this PR wrote states this head's figure "
       'or carries no figure.', '',
       "**No statement gives a superseded figure as this head's.** R835-5's `f1_sites.py` reports 0 of 7 present.", '',
       '## The phrase sweep', '', '| Where | Phrase | Written by | Sentence |', '|---|---|---|---|']
out += [f'| {p[1]} | {p[2]} | {"this PR" if p[3] == "PR" else "base (before `cec88385`)"} | '
        f'{p[4].replace("|", chr(92) + "|")[:260]} |' for p in phr]
out += ['', '## The figure sweep', '', '| Where | Figure | Disposition | Sentence |', '|---|---|---|---|']
out += [f'| {a} | `{b}` | {c} | {d[:240]} |' for a, b, c, d in rows]
open(dst, 'w').write('\n'.join(out) + '\n')
print(counts, 'left', len(left))
for r in left:
    print('LEFT', r[:3])
sys.exit(1 if left else 0)
