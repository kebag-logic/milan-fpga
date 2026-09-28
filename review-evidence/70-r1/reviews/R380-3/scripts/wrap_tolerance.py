#!/usr/bin/env python3
"""Does D3's named sweep find multi-word statements wrapped across a line break
that carries a comment prefix (SV '//' or '//!', Python '#', block ' * ')?

Run from the parent repository root. Takes the sweep from D3 15.2 at HEAD,
builds a comment-tolerant variant (every [[:space:]]+ / [[:space:]/]* joint
becomes one-or-more of whitespace, '//', '//!', '#', '*'), then:
 A. synthetic wrapped fixtures under the given scratch dir: strict vs tolerant;
 B. the pinned processor docs/hdl/tb: matched lines the tolerant variant adds.
Prints results; exit 0 always (this is a measurement, not a gate).
"""
import os, re, subprocess, sys

scratch = sys.argv[1]
sec = open('docs/design/SAVED_STATE_MATERIALIZATION.md', encoding='utf-8').read()
cmd = [l for l in sec.split('### 15.2', 1)[1].split('\n## 16.', 1)[0].splitlines() if l.startswith('rg ')][0]
S = re.match(r"^rg -n -U -i -C 2 '(.*)' docs hdl tb$", cmd).group(1)
J = r'(?:[[:space:]]|//!?|#|\*)+'
T = S.replace('[[:space:]]+', J).replace('[[:space:]/]*', J)
print('strict  :', S)
print('tolerant:', T)

fixtures = {
    'a.sv': '// NVM commits are asynchronous and never\n// delay a response\n',
    'b.sv': "//! Manager 1 is the platform's\n//! saved-state writer; tied idle\n",
    'c.py': '# groups 6\n# and 7 have no processor writer\n',
    'd.sv': '//! owned by the integrating\n//! platform\n',
    'e.md': 'commits are asynchronous\nto protocol responses\n',
    'f.sv': '// sets the dirty\n// mark for the NVM class\n',
    'g.md': "Manager 1 is the platform's\nsaved-state writer\n",
}
os.makedirs(scratch, exist_ok=True)
print('## A. synthetic wrapped fixtures (count of matching lines)')
for name, body in fixtures.items():
    p = os.path.join(scratch, name)
    open(p, 'w').write(body)
    res = []
    for pat in (S, T):
        r = subprocess.run(['rg', '-c', '-U', '-i', pat, p], capture_output=True, text=True)
        res.append(r.stdout.strip() or '0')
    print(f'  {name:5} strict={res[0]} tolerant={res[1]}  {body!r}')

def lines(pat):
    r = subprocess.run(['rg', '-n', '-U', '-i', pat, 'docs', 'hdl', 'tb'], cwd='protocol-processor',
                       capture_output=True, text=True)
    return {tuple(m.groups()) for m in (re.match(r'^(.+?):(\d+):', l) for l in r.stdout.splitlines()) if m}

s, t = lines(S), lines(T)
print(f'## B. pinned processor tree: strict matched lines {len(s)}, tolerant {len(t)}, added by tolerance {len(t - s)}')
for f, n in sorted(t - s, key=lambda x: (x[0], int(x[1]))):
    src = open(f'protocol-processor/{f}', encoding='utf-8', errors='replace').read().splitlines()[int(n) - 1]
    print(f'  ADDED {f}:{n}  {src.strip()[:120]}')
