#!/usr/bin/env python3
"""R380-4: exhaustive joint x prefix matrix for D3's named contract sweep.

Usage: separator_matrix.py <D3 file> <scratch dir>
1. Extracts the sweep from the given D3 15.2 text and lists every multi-word
   joint (a bracket class followed by + or *) and its exact class body.
2. For each multi-word alternative and EACH of its joints, writes a fixture
   wrapped at that joint with each claimed continuation prefix (bare prose,
   '//', '//!', '#', ' * ') and with unclaimed ones ('--', ';', '>', '<br/>'),
   and counts rg -U -i matches. Claimed prefixes must all match; unclaimed
   ones are reported (they bound what the text may claim).
Exit 0 iff every joint uses the class the text states and every claimed cell matches.
"""
import os, re, subprocess, sys

d3, scratch = sys.argv[1], sys.argv[2]
sec = open(d3, encoding='utf-8').read().split('### 15.2', 1)[1].split('\n## 16.', 1)[0]
cmd = [l for l in sec.splitlines() if l.startswith('rg ')][0]
PAT = re.match(r"^rg -n -U -i -C 2 '(.*)' docs hdl tb$", cmd).group(1)
joints = re.findall(r'\[((?:\[:[a-z]+:\]|[^\]])*)\]([+*])', PAT)
print('## joints in sweep:', len(joints))
for body, q in sorted(set(joints)):
    print(f'   class [{body}]{q}  x{joints.count((body, q))}')
STATED = ('[:space:]/!#*', '+')
ok = all(j == STATED for j in joints)
print('## every joint is [[:space:]/!#*]+ :', ok)

PHRASES = [["dirty", "mark"], ["Nothing", "in", "the", "processor"], ["groups", "6", "and", "7"],
           ["integrating", "platform"], ["platform's", "saved-state"], ["never", "delay"],
           ["asynchronous", "to", "protocol"]]
CLAIMED = {'prose': ('', ''), '//': ('// ', '// '), '//!': ('//! ', '//! '), '#': ('# ', '# '), ' * ': (' * ', ' * ')}
UNCLAIMED = {'--': ('-- ', '-- '), ';': ('; ', '; '), '>': ('> ', '> '), '<br/>': None}
os.makedirs(scratch, exist_ok=True)
def count(path):
    r = subprocess.run(['rg', '-c', '-U', '-i', PAT, path], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)
print('## matrix: phrase | joint | ' + ' | '.join(list(CLAIMED) + list(UNCLAIMED)))
k = 0
for ph in PHRASES:
    for j in range(1, len(ph)):
        cells = []
        for name, pre in list(CLAIMED.items()) + list(UNCLAIMED.items()):
            k += 1
            if pre is None:
                body = 'x ' + ' '.join(ph[:j]) + '<br/>' + ' '.join(ph[j:]) + ' y\n'
            else:
                body = pre[0] + 'lead ' + ' '.join(ph[:j]) + '\n' + pre[1] + ' '.join(ph[j:]) + ' tail\n'
            p = os.path.join(scratch, f'fx{k:03}.txt')
            open(p, 'w').write(body)
            c = count(p)
            cells.append(str(c))
            if name in CLAIMED and c == 0:
                ok = False
        print(f'   {" ".join(ph):28} | {j} | ' + ' | '.join(cells))
print('## RESULT', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
