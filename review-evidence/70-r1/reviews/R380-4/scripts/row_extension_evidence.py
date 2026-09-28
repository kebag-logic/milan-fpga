#!/usr/bin/env python3
"""R380-4 evidence for the taken suggestions on D3 section 15.2 rows.

Run from the parent repository root, protocol-processor checked out at its pin.
For each newly required location (the acmp_nvm wrap banner, the E_SETSR
exemplar mark comment in gen_ucode.py, the 06 section 8 exemplar line):
  * the named sweep, extracted from D3 15.2 at HEAD and run as written, must
    MATCH the line or show it as -C 2 CONTEXT;
  * a 15.2 row must cite the line: either the row keyed by that file, or a row
    whose location cell links that file and gives 'line(s) N[-M]' after it;
  * the row's contract cell must contain the stated keyword(s).
Exit 0 iff every location passes.
"""
import re, subprocess, sys

D3 = 'docs/design/SAVED_STATE_MATERIALIZATION.md'
PP = 'protocol-processor'
REQUIRED = [
    ('tb/acmp_nvm/acmp_nvm_wrap.sv', [12, 13, 14], ['both descriptions', 'processor D3 writer']),
    ('hdl/aecp/ucode/gen_ucode.py', [472], ['E_SETSR exemplar', 'never the mark']),
    ('docs/architecture/06_aecp_engine.md', [874], ['sampling-rate exemplar', 'completion effect']),
]

sec, on = [], False
for line in open(D3, encoding='utf-8').read().splitlines():
    if line.startswith('### 15.2'):
        on = True; continue
    if on and line.startswith('## 16.'):
        break
    if on:
        sec.append(line)
cmd = [l for l in sec if l.startswith('rg ')]
assert len(cmd) == 1
PAT = re.match(r"^rg -n -U -i -C 2 '(.*)' docs hdl tb$", cmd[0]).group(1)
rows = [l for l in sec if re.match(r'^\| \[[^\]]+\]\(', l)]

def cells(row):
    return [c.strip() for c in row.strip().strip('|').split('|')]

def nums(s):
    got = set()
    for a, b in re.findall(r'(\d+)(?:-(\d+))?', s):
        a = int(a); b = int(b) if b else a
        got.update(range(a, b + 1))
    return got

def citation(f, row):
    key, loc, contract = cells(row)[:3]
    if key.startswith(f'[{f}]'):
        segs = re.split(r'\[[^\]]+\]\([^)]*\)', loc)[0]   # before any other linked file
        body = loc
    elif f'[{f}](' in loc:
        body = loc.split(f'[{f}](', 1)[1].split(')', 1)[1]
        segs = re.split(r'\[[^\]]+\]\([^)]*\)', body)[0]
    else:
        return None
    lines = set()
    for seg in re.split(r';', segs):
        for m in re.finditer(r'lines?\s+([\d,\s\-and]+)', seg):
            lines |= nums(m.group(1))
    return lines, contract

r = subprocess.run(['rg', '-n', '-U', '-i', '-C', '2', PAT, 'docs', 'hdl', 'tb'], cwd=PP, capture_output=True, text=True)
match, ctx = set(), set()
for l in r.stdout.splitlines():
    m = re.match(r'^(.+?)([:-])(\d+)([:-])', l)
    if m:
        (match if m.group(2) == ':' and m.group(4) == ':' else ctx).add((m.group(1), int(m.group(3))))
ctx -= match
print('## parent', subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
      'processor', subprocess.run(['git', '-C', PP, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
print('## 15.2 rows', len(rows))
ok = True
for f, lines, keys in REQUIRED:
    cites = [c for c in (citation(f, row) for row in rows) if c]
    allc = set().union(*[c[0] for c in cites]) if cites else set()
    kw = all(any(k in c[1] for c in cites) for k in keys)
    for n in lines:
        s = 'MATCH' if (f, n) in match else 'CONTEXT' if (f, n) in ctx else 'MISS'
        rc = 'ROW-CITED' if n in allc else 'NOT-CITED'
        src = open(f'{PP}/{f}', encoding='utf-8').read().splitlines()[n - 1].strip()[:110]
        good = s != 'MISS' and rc == 'ROW-CITED' and kw
        ok &= good
        print(f'  {"OK " if good else "BAD"} {s:7} {rc:9} contract-keywords={"yes" if kw else "NO"} {f}:{n}  {src}')
    print(f'    rows citing {f}: {len(cites)}; cited lines {sorted(allc)}; keywords {keys}')
print('## RESULT', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
