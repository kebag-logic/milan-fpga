#!/usr/bin/env python3
"""Every superseded STATEMENT figure (R837-10-S2): each constant's old value, sentence by sentence, where the sentence
names what the constant states; every arithmetic derivation (a x b = c, a + b = c) one of those figures enters, and
each derived result wherever it appears; each hit flagged when its sentence cites a clause or table (IEEE, Milan,
802.1Q, 1722, Table, Clause). Scope: SPLIT_CONTROL_MEMORY.md section 13, FR_NFR.md 3.4.1, docs/design/MAILBOX_SPLIT.md,
every tracked README, every comment and docstring under sw/ and tb/ (comment_sweep.py's extraction), and the PR body
(argv[1]); every line, tables included. Run from the tree's top. usage: statement_sweep.py PR_BODY"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comment_sweep  # noqa: E402

N = r'(?<![\d.,])'
END = r'(?![\d]|[.,]\d)'
#: (label, the figure, the sentence must name) -- the old value of each statement the lane's moves superseded
STATEMENTS = [
    ('CTRL_LOOP_TX_MS 44 (pre-tiers)', N + r'44(?:\s?ms)?' + END, r'TX_MS|TRANSMIT|MRPDU|JoinTime'),
    ('CTRL_LOOP_TX_MS 30 (one interface, before round 11)', N + r'30(?:\s?ms|u)?' + END + r'(?!\s?(?:us|cs|%))', r'TX_MS'),
    ('CTRL_LOOP_TX_MS 98 (two interfaces, before round 16)', N + r'98(?:\s?ms|u)?' + END, r'TX_MS|TRANSMIT|tx row'),
    ('CTRL_LOOP_TX_BOUND_MS 40 (20 cs)', N + r'40(?:\s?ms)?' + END + r'(?!\s?(?:us|cs|%))', r'TX_BOUND|txL|tx row|MRPDU|timer budget'),
    ('CTRL_LOOP_TX_BOUND_MS 50 (19 cs, before T_egress)', N + r'50(?:\s?ms)?' + END + r'(?!\s?(?:us|cs|%))', r'TX_BOUND|txL|tx row|MRPDU|timer budget'),
    ('CTRL_LOOP_JOIN_CS 20 cs, JoinTime 200 ms', N + r'(?:200\s?ms|20\s?cs)' + END, r'(?i)join'),
    ('CTRL_LOOP_BUILD_ONE_PASS_US 725 / 430', N + r'(?:725|430)(?:\s?us)?' + END, r'(?i)build'),
    ('event.TICK 45 / 50 us', N + r'(?:45|50)(?:\s?us)?' + END + r'(?!\s?(?:ms|cs|%))', r'TICK'),
    ("AECP's timer slot 60 / 65 us", N + r'(?:60|65)(?:\s?us)?' + END + r'(?!\s?(?:ms|cs|%))', r'(?i)aecp\S*\s+timer slot|timer slot.{0,40}aecp'),
    ('a LINK 150 us', N + r'150(?:\s?us)?' + END + r'(?!\s?(?:ms|cs|%))', r'LINK'),
    ('CTRL_LOOP_SRP_UNIT_US 250 us', N + r'250(?:\s?us|u)?' + END + r'(?!\s?(?:ms|cs|%))', r'SRP_UNIT|SRP drain|(?i:the drain)'),
    ('CTRL_LOOP_SLICE_US 800 / 900 / 1,200 us', N + r'(?:800|900|1,200)\s?(?:us|u)\b', r'.'),
    ('AECP_PACE_MS 6 / 7 ms', N + r'[67]\s?ms' + END, r'(?i)pace'),
    ('the load 0.515 / 0.511', N + r'0\.51[15]' + END, r'.'),
]
NUM = r'\d[\d,]*(?:\.\d+)?'
OPERAND = r'(?:`[A-Za-z_]+`|' + NUM + r')(?:\s?(?:ms|us|cs))?'
ARITH = re.compile(OPERAND + r'(?:\s*[x×+]\s*' + OPERAND + r')+\s*=\s*(' + NUM + r')')
CLAUSE = re.compile(r'IEEE|Milan|802\.1Q|1722|Table \d|Clause')
SENT = re.compile(r'(?<=[.;])\s+(?=[A-Z(*`\[_-])')


def sources(body):
    lines = lambda f: open(f, encoding='utf-8').read().split('\n')
    sec = lines('docs/design/SPLIT_CONTROL_MEMORY.md')
    on, s13 = False, []
    for i, s in enumerate(sec, 1):
        if s.startswith('## ') and on and not s.startswith('## 13'):
            break
        on = on or s.startswith('## 13')
        if on:
            s13.append((i, s))
    yield 'docs/design/SPLIT_CONTROL_MEMORY.md', s13
    fr = lines('docs/reference/FR_NFR.md')
    on, f341 = False, []
    for i, s in enumerate(fr, 1):
        if on and re.match(r'#+ 3\.(4\.[2-9]|5)\b', s):
            break
        on = on or bool(re.match(r'#+ 3\.4\.1\b', s))
        if on:
            f341.append((i, s))
    yield 'docs/reference/FR_NFR.md', f341
    files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True).stdout.split()
    for f in files:
        if f == 'docs/design/MAILBOX_SPLIT.md' or (f.rsplit('/', 1)[-1].startswith('README') and
                                                     not f.startswith(('sw/', 'tb/'))):
            yield f, list(enumerate(lines(f), 1))
    for f in files:
        if not f.startswith(('sw/', 'tb/')):
            continue
        try:
            text = open(f, encoding='utf-8').read()
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        if f.endswith(comment_sweep.C_EXT):
            yield f, comment_sweep.c_comments(text)
        elif f.endswith('.py'):
            yield f, comment_sweep.py_comments(text)
        elif f.endswith('.sh'):
            yield f, comment_sweep.sh_comments(text)
        elif f.endswith('.md'):
            yield f, list(enumerate(text.split('\n'), 1))
    yield body.rsplit('/', 1)[-1], list(enumerate(open(body, encoding='utf-8').read().split('\n'), 1))


def main(argv):
    pats = [(lab, re.compile(p), re.compile(c)) for lab, p, c in STATEMENTS]
    hits, derived = [], {}
    for name, parts in sources(argv[1]):
        for line, text in parts:
            for k, sent in enumerate(SENT.split(text)):
                cite = 'clause' if CLAUSE.search(sent) else '-'
                for lab, pat, ctx in pats:
                    if ctx.search(sent):
                        for m in pat.finditer(sent):
                            hits.append((lab, f'{name}:{line}', k, cite, sent[max(0, m.start() - 120):m.end() + 80]))
                for m in ARITH.finditer(sent):
                    ops = re.findall(NUM, m.group(0)[:m.start(1) - m.start()])
                    # an operand counts only where the sentence names the statement it is the old value of
                    old = sorted({o for o in ops for lab, pat, ctx in pats
                                  if ctx.search(sent) and pat.fullmatch(o)})
                    if old:
                        hits.append((f'derivation from {"/".join(old)} = {m.group(1)}',
                                     f'{name}:{line}', k, cite, m.group(0)))
                        derived.setdefault(m.group(1), m.group(0))
    pats2 = [(f'derived {r} ({e})', re.compile(N + re.escape(r) + r'\s?(?:ms|us)' + END)) for r, e in derived.items()]
    for name, parts in sources(argv[1]):
        for line, text in parts:
            for k, sent in enumerate(SENT.split(text)):
                cite = 'clause' if CLAUSE.search(sent) else '-'
                for lab, pat in pats2:
                    for m in pat.finditer(sent):
                        if not any(h[1] == f'{name}:{line}' and h[2] == k and h[0].startswith('derivation') for h in hits):
                            hits.append((lab, f'{name}:{line}', k, cite, sent[max(0, m.start() - 120):m.end() + 80]))
    seen = set()
    for lab, loc, k, cite, text in hits:
        key = (lab, loc, k)
        if key in seen:
            continue
        seen.add(key)
        print(f'{lab}\t{loc}\t{k}\t{cite}\t{" ".join(text.split())}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
