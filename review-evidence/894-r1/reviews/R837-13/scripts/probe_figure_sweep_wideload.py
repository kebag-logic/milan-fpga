# Probe: the author figure_sweep.py with its LOAD pattern widened from 0.ddd to loads of 1 or more (d.ddd), every other rule unchanged; run only to count what the LOAD rule cannot see.
# Adapted from the R837-11 review's packet (review-evidence/894-r1/reviews/R837-11/scripts/figure_sweep.py), by its reviewer: its RULES, ROW and LOAD
# unchanged; round 18 adds one rule per constant constant_history.py finds moved (AUTO, below), so no hand list bounds the sweep.
"""Reviewer sweep for superseded statement figures, row figures and derived products in prose and comments.

Usage: python3 -I -B figure_sweep.py <repo-root> <base-sha> <pr-body.md> <out.tsv> <constant_history.txt>

Scope: every Markdown file the PR changes (base..HEAD), every README.md in first-party trees, every first-party
source file under sw/ and tb/ (whole lines, comments and code), and the PR body. Each sentence that names a subject
beside a superseded value of it, or any two-decimal ms / three-decimal load figure that is not one of the head's row
or load figures, is a hit. A hit is marked HIST when the sentence carries a history or comparison marker; the
reviewer reads every hit (HIST ones by sample) and classifies it by hand.
"""
import re
import subprocess
import sys
from pathlib import Path

root, base, body, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
history = Path(sys.argv[5])  # round 18: constant_history.py's output, for the AUTO rules
SRC = ('.c', '.h', '.py', '.cpp', '.hpp', '.sv', '.svh', '.ld', '.yaml', '.txt', '.sh', '.mk')
SKIP = ('third_party/', 'protocol-processor/', 'gptp-processor/', 'external/')

changed = subprocess.run(['git', '-C', str(root), 'diff', '--name-only', f'{base}..HEAD'], capture_output=True,
                         text=True, check=True).stdout.split()
tracked = subprocess.run(['git', '-C', str(root), 'ls-files'], capture_output=True, text=True, check=True).stdout.split()
files = set(p for p in changed if p.endswith('.md'))
files |= set(p for p in tracked if p.endswith('README.md') and not p.startswith(SKIP))
files |= set(p for p in tracked if p.startswith(('sw/', 'tb/')) and p.endswith(SRC) and not p.startswith(SKIP))

# subject regex, superseded value regex (each a statement figure the PR moved), rule name
RULES = [
    ('TX_MS', r'CTRL_LOOP_TX_MS|THE TRANSMIT|tx row|MRPDU', r'\b44 ?ms\b|\b44u\b|\b30 and 98\b|\b98 ?ms\b|\b98u\b|\b176\b|2 x `?MBX_N_IF`? x'),
    ('JOIN', r'JoinTime|[Jj]oin ?[Tt]im|SRP_JOIN_CS|CTRL_LOOP_JOIN_CS|kJoinCs|join_cs|joinCs', r'\b20 ?cs\b|\b200 ?ms\b|\b20u\b|=\s*20\b'),
    ('TX_BOUND', r'CTRL_LOOP_TX_BOUND_MS|TX_BUDGET|timer budget|MRPDU bound|txL\'s bound|MRPDU \(4|bound', r'\b40 ?ms\b|\b50 ?ms\b|\b240 ?ms less[^.]*\b(40|50)\b'),
    ('SLICE', r'[Ss]lice|CTRL_LOOP_SLICE_US', r'\b800 ?us\b|\b900 ?us\b|\b1,?200 ?us\b|\b800u\b|\b900u\b'),
    ('PACE', r'\bpace\b|AECP_PACE_MS|PACE', r'\b6 ?ms\b|\b7 ?ms\b|\b6u\b|\b7u\b'),
    ('BUILD_ONE', r'build of one|BUILD_ONE_PASS|build_one', r'\b725\b|\b430 ?us\b'),
    ('TICK', r'\bTICK\b|event\.TICK', r'\b45 ?us\b|\b50 ?us\b|\bat 45\b|\bat 50\b'),
    ('AECP_TIMER', r'timer slot|event\.AECP', r'\b60 ?us\b|\b65 ?us\b|\bat 60\b|\bat 65\b'),
    ('LINK', r'\bLINK\b', r'\b150 ?us\b|\bat 150\b'),
    ('SRP_UNIT', r'SRP_UNIT|SRP drain', r'\b250 ?us\b|\b250u\b'),
    ('RECORD', r'record', r'\b940 ?us\b|\b920 ?us\b|\b1,?040 ?us\b|\b1,?555 ?us\b'),
    ('DATAPATH', r'AMAP_LIVE_WRITE|DATAPATH_US', r'\b25 ?us\b|\b25 stated\b'),
    ('QUEUED', r'AECP_QUEUED_MS|last queued notice', r'\b125 ?ms\b'),
    # the stated costs and statements constant_history.py finds moved in the PR beyond the author's token list
    ('EDIT_RECORD', r'EDIT_RECORD_US|paced class\'s record', r'\b240 ?us\b|\b260 ?us\b|\b325 ?us\b|\b240\b|\b260\b|\b325\b'),
    ('OWED_BYTES', r'AECP_OWED_BYTES|owed-notice slot', r'\b128 ?B\b'),
    ('BUILD_PASS', r'BUILD_PASS_US|build of both', r'\b900 ?us\b|\b955 ?us\b'),
    ('REC_AECP', r'record\.aecp|ordinary record', r'\b205 ?us\b|\b205\b'),
    ('REC_SRP', r'record\.srp|SRP record|retained', r'\b250 ?us\b|\b260 ?us\b'),
    ('CENTI', r'centisecond', r'\b125 ?us\b|\b130 ?us\b'),
    ('BASE', r'\bbase\b', r'\b155 ?us\b|\b160 ?us\b|\b245 ?us\b|\b285 ?us\b'),
    ('WALK', r'\bwalk\b', r'\b20 ?us\b'),
    ('REBUILD', r'\brebuild\b', r'\b630 ?us\b'),
    ('ACMP_ITEM', r'item\.acmp|ACMP\'s (owed )?(item|frame)|acmp-cmd', r'\b(35|50|65|120|125|165|185|195) ?us\b'),
    ('LONG_NOTICE', r'aecp_long|LONG_NOTICE_US|notice\'s stated cost', r'\b360 ?us\b|\b650 ?us\b|\b665 ?us\b'),
    ('DP_EVENTS', r'AVB_INFO_CHANGED|AS_PATH_CHANGED', r'\b30 ?us\b'),
    ('LONG_RECORD', r'LONG_RECORD_US|largest legal command\'s record|stated record', r'\b(910|920|940|1,?470|1,?555) ?us\b'),
    ('ROUND_COLD', r'AECP_ROUND_COLD_US|cold start', r'\b165 ?us\b'),
    ('EVENTS_NONE', r'events_none|events\' fixed part', r'\b25 ?us\b'),
    ('EV_GM', r'event\.GM|GM event', r'\b35 ?us\b'),
    ('EV_ADP', r'event\.ADP|ADP event', r'\b110 ?us\b'),
    ('NOTICE', r'item\.aecp\.notice|a notice\'s cost', r'\b270 ?us\b'),
]
def auto_rules(path):
    """Round 18: one rule per constant constant_history.py finds moved. Its subject is the constant's own name (a
    #define's identifier; a stated table's key, and the table's name), its values every number its history held that
    the head's value does not. A #define's bare number counts; a table key's, only with a unit, the keys being words."""
    out = []
    for line in path.read_text().splitlines():
        name, _, rest = line.partition(': head ')
        head, _, hist = rest.partition('; history ')
        nums = lambda s: set(re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])', s.replace('u)', ')').replace('u ', ' ')
                                        .replace('u:', ':')))
        now = nums(head)
        old = set()
        for item in re.findall(r'(.*?)@[0-9a-f]{8}(?:, |$)', hist):
            old |= nums(item)
        old = sorted(v for v in old - now if v not in ('0', '1', '2'))
        if not old:
            continue
        if '[' in name:
            table, key = re.match(r'[^.]+\.([A-Z_]+)\[([^\]]+)\]', name).groups()
            subj = re.escape(key)
            unit = r'(?: ?(?:us|ms|cs|B)\b)'
        else:
            subj = re.escape(name)
            unit = r'(?:u\b| ?(?:us|ms|cs|B)\b)?'
        vals = '|'.join(r'(?<![\d.,])' + re.escape(f'{int(v):,}' if v.isdigit() and int(v) >= 1000 else v) + unit +
                        r'(?![\d]|[.,]\d)' for v in old)
        out.append((f'AUTO {name}', subj, vals))
    return out


RULES += auto_rules(history)

# the head's row figures (flip_grade.py --check at both points) and its load figures (load_grade.py --check,
# tier_grid.py, flip_grade.py)
HEAD_ROWS = {'13.10', '74.07', '69.86', '14.66', '127.21', '188.48', '28.95', '27.30', '27.42', '33.38', '48.43',
             '44.24', '206.45', '196.31', '20.93', '806.60', '195.76', '67.94', '68.08', '69.13', '98.49', '459.40'}
HEAD_LOADS = {'0.516', '0.512', '0.794', '0.754', '2.175', '1.684', '0.695'}
HIST = re.compile(r"\b(was|were|had|before|then|earlier|previously|first|at round|round \d+'s|since|stated before|"
                  r"before it|at the merge|by then|once|used to|no longer|superseded|history|historical|"
                  r"would|refuted|from \d|beside)\b", re.I)
SENT = re.compile(r'(?<=[.;:])\s+(?=[A-Z`(*\[])')


def sentences(path, text):
    for no, line in enumerate(text.splitlines(), 1):
        for s in SENT.split(line):
            yield no, s


rows = []
for rel in sorted(files) + ['PR-BODY']:
    p = body if rel == 'PR-BODY' else root / rel
    if not p.is_file():
        continue
    try:
        text = p.read_text()
    except UnicodeDecodeError:
        continue
    for no, s in sentences(rel, text):
        hist = 'HIST' if HIST.search(s) else 'CUR?'
        for name, subj, val in RULES:
            if re.search(subj, s):
                for m in re.finditer(val, s):
                    rows.append((rel, no, name, m.group(0), hist, s.strip()[:400]))
        for m in re.finditer(r'(?<![\d.,])(\d{1,3}\.\d{2})(?= ?ms\b| and \d| within| over|,| ms| \()', s):
            if m.group(1) not in HEAD_ROWS and re.search(r'ms|row|txL|R4L|R4\b|R5|R6|ACMP|ADP|MAAP|notice|tx\b', s):
                rows.append((rel, no, 'ROW', m.group(1), hist, s.strip()[:400]))
        for m in re.finditer(r'(?<![\d.,])([1-9]\d*\.\d{3})(?!\d)', s):
            if m.group(1) not in HEAD_LOADS and re.search(r'load', s):
                rows.append((rel, no, 'LOAD', m.group(1), hist, s.strip()[:400]))

seen = set()
with out.open('w') as f:
    for r in rows:
        key = r[:4]
        if key in seen:
            continue
        seen.add(key)
        f.write('\t'.join(str(x) for x in r) + '\n')
n = len(seen)
cur = sum(1 for r in rows if r[4] == 'CUR?')
print(f'files {len(files) + 1}, hits {n}, without a history marker {cur}')
