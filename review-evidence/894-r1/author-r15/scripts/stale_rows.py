#!/usr/bin/env python3
"""Every hit of a superseded 1x1/1if row or load figure (R837-8-F1), one line each: token, its source, file:line, and
the text around it. The row tokens are taken from section 13's rows-history table by construction (R837-8-S1): every
figure of every row before the head's, less any equal to the head's figure in its column. The load tokens are every
0.xxx figure on a line naming the load in section 13, FR_NFR 3.4.1 or the PR body, less the head's (0.516, 0.512 and
0.695 at 1x1/1if; 0.794 and 0.754 at 8x8/2if) and the ceilings (0.70, 0.75).
Scope: section 13, FR_NFR 3.4.1, docs/design/MAILBOX_SPLIT.md, every tracked README and every tracked C, C++, header,
Python and SystemVerilog file, outside table lines; and the PR body (argv[1]), every line, its tables included.
Run from the tree's top. usage: stale_rows.py PR_BODY [--tokens]"""
import re
import subprocess
import sys

SEC = 'docs/design/SPLIT_CONTROL_MEMORY.md'
FR = 'docs/reference/FR_NFR.md'
HEAD_LOADS = {'0.516', '0.512', '0.695', '0.794', '0.754', '0.70', '0.75'}
FIG = re.compile(r'(?<![\d.])\d+\.\d\d(?!\d)')
LOAD = re.compile(r'(?<![\d.])0\.\d{2,3}(?!\d)')


def span(lines, start, stop):
    """1-based line numbers from the heading matching start to the next heading matching stop."""
    out, on = [], False
    for i, s in enumerate(lines, 1):
        if on and stop.match(s):
            break
        on = on or bool(start.match(s))
        if on:
            out.append(i)
    return out


def row_tokens(lines):
    """{token: 'column, head'} from the rows-history table's rows before its last (the head's)."""
    top = next(i for i, s in enumerate(lines) if s.startswith('| Head | R4 (20)'))
    head = lines[top].strip('|').split('|')
    body = []
    for s in lines[top + 2:]:
        if not s.startswith('|'):
            break
        body.append([c.strip() for c in s.strip().strip('|').split('|')])
    last = body[-1]
    toks = {}
    for row in body[:-1]:
        for col in range(1, len(head)):
            now = set(FIG.findall(last[col]))
            for f in FIG.findall(row[col]):
                if f not in now:
                    toks.setdefault(f, f'{head[col].strip().split(" (")[0]}, {row[0][:40]}')
    return toks


def main(argv):
    body = argv[1]
    sec = open(SEC, encoding='utf-8').read().split('\n')
    fr = open(FR, encoding='utf-8').read().split('\n')
    pr = open(body, encoding='utf-8').read().split('\n')
    s13 = span(sec, re.compile(r'## 13\b'), re.compile(r'## (?!13\b)\d'))
    f341 = span(fr, re.compile(r'#+ 3\.4\.1\b'), re.compile(r'#+ 3\.4\.(?!1\b)\d|#+ 3\.5\b'))
    toks = row_tokens(sec)
    loads = set()
    for lines, nums in ((sec, s13), (fr, f341), (pr, range(1, len(pr) + 1))):
        for i in nums:
            if 'load' in lines[i - 1].lower():
                loads.update(LOAD.findall(lines[i - 1]))
    for t in sorted(loads - HEAD_LOADS):
        toks.setdefault(t, 'load')
    if '--tokens' in argv:
        for t, why in sorted(toks.items(), key=lambda kv: float(kv[0])):
            print(f'{t}\t{why}')
        return 0
    scope = [(SEC, sec, s13, True), (FR, fr, f341, True), (body.rsplit('/', 1)[-1], pr, range(1, len(pr) + 1), False)]
    files = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, check=True).stdout.split()
    ext = ('.c', '.h', '.cpp', '.hpp', '.py', '.sv', '.svh', '.v')
    for f in files:
        if f in (SEC, FR):
            continue
        if f == 'docs/design/MAILBOX_SPLIT.md' or f.rsplit('/', 1)[-1].startswith('README') or f.endswith(ext):
            try:
                lines = open(f, encoding='utf-8').read().split('\n')
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            scope.append((f, lines, range(1, len(lines) + 1), True))
    pat = re.compile(r'(?<![\d.])(' + '|'.join(re.escape(t) for t in toks) + r')(?![\d])')
    for name, lines, nums, skip_tables in scope:
        for i in nums:
            s = lines[i - 1]
            if skip_tables and s.lstrip().startswith('|'):
                continue
            for m in pat.finditer(s):
                t = m.group(1)
                print(f'{t}\t{toks[t]}\t{name}:{i}\t{s[max(0, m.start() - 150):m.end() + 60]}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
