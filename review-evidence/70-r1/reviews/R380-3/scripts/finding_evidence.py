#!/usr/bin/env python3
"""R380-3 current-head evidence for R380-2 F1 (and the round-3 item-1 list).

Run from the parent repository root, protocol-processor checked out at its pin.
1. Extracts the named contract sweep from D3 section 15.2 AT THE CHECKED-OUT HEAD
   and runs it exactly as written (rg -n -U -i -C 2 ... docs hdl tb) in the
   processor tree; records matched lines and context lines separately.
2. For every required location, reports whether the sweep MATCHES the line,
   only shows it as CONTEXT, or misses it, and whether a section 15.2 row for
   that file cites a line or range containing it.
3. Optional reviewer probes (argv: extra 'label::regex' strings) are run with
   rg -n -i -U over docs hdl tb; each hit is classified the same way.
Exit 0 iff every required location is (sweep MATCH or CONTEXT) AND row-cited.
"""
import re, subprocess, sys

D3 = 'docs/design/SAVED_STATE_MATERIALIZATION.md'
PP = 'protocol-processor'

REQUIRED = [
    ('hdl/aecp/ucode/gen_ucode.py', [1364, 1439, 1582, 1583, 1584, 1675, 1791, 1925, 2002, 2091]),
    ('docs/architecture/06_aecp_engine.md', [341, 342, 343, 344, 365, 421, 422, 423, 424, 425]),
    ('docs/00_MILAN_COMPLIANCE_REVIEW.md', [206, 207, 208]),
    ('docs/architecture/03_packet_engine.md', [236]),
    ('docs/architecture/02_interfaces.md', [492, 493]),
    ('hdl/top/protocol_processor_top.sv', [2448, 2449, 2450, 2451]),
    ('tb/acmp_nvm/README.md', [15]),
]

def section_152(text):
    out, on = [], False
    for line in text.splitlines():
        if line.startswith('### 15.2'):
            on = True; continue
        if on and line.startswith('## 16.'):
            break
        if on:
            out.append(line)
    return out

def rows_by_file(sec):
    rows = {}
    for line in sec:
        m = re.match(r'^\| \[([^\]]+)\]\([^)]*\) \| ([^|]*) \|', line)
        if m:
            rows.setdefault(m.group(1), []).append(m.group(2))
    return rows

def cited_lines(cell):
    got = set()
    for m in re.finditer(r'lines?\s+((?:\d+(?:-\d+)?(?:,\s*(?:and\s+)?|\s+and\s+)?)+)', cell):
        for a, b in re.findall(r'(\d+)(?:-(\d+))?', m.group(1)):
            a = int(a); b = int(b) if b else a
            got.update(range(a, b + 1))
    return got

def rg(args):
    r = subprocess.run(['rg'] + args, cwd=PP, capture_output=True, text=True)
    if r.returncode not in (0, 1):
        sys.exit('rg failed: ' + r.stderr)
    return r.stdout

def parse(out):
    match, ctx = set(), set()
    for line in out.splitlines():
        m = re.match(r'^(.+?)([:-])(\d+)([:-])', line)
        if not m:
            continue
        f, s1, n, s2 = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        (match if s1 == ':' and s2 == ':' else ctx).add((f, n))
    return match, ctx - match

text = open(D3, encoding='utf-8').read()
sec = section_152(text)
cmd = [l for l in sec if l.startswith('rg ')]
assert len(cmd) == 1, cmd
m = re.match(r"^rg -n -U -i -C 2 '(.*)' docs hdl tb$", cmd[0])
assert m, cmd[0]
PAT = m.group(1)
rows = rows_by_file(sec)
print('## parent head', subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
print('## processor', subprocess.run(['git', '-C', PP, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip())
print('## sweep as written in D3 15.2:', cmd[0])
print('## 15.2 rows:', sum(len(v) for v in rows.values()), 'files:', len(rows))
match, ctx = parse(rg(['-n', '-U', '-i', '-C', '2', PAT, 'docs', 'hdl', 'tb']))
print('## sweep matched lines:', len(match), 'context-only lines:', len(ctx))

ok = True
print('## required locations')
for f, lines in REQUIRED:
    cited = set().union(*[cited_lines(c) for c in rows.get(f, [])]) if f in rows else set()
    for n in lines:
        s = 'MATCH' if (f, n) in match else 'CONTEXT' if (f, n) in ctx else 'MISS'
        r = 'ROW-CITED' if n in cited else ('ROW-FILE-ONLY' if f in rows else 'NO-ROW')
        if s == 'MISS' or r != 'ROW-CITED':
            ok = False
        src = open(f'{PP}/{f}', encoding='utf-8').read().splitlines()[n - 1].strip()[:110]
        print(f'  {s:7} {r:13} {f}:{n}  {src}')

for probe in sys.argv[1:]:
    label, pat = probe.split('::', 1)
    hits, _ = parse(rg(['-n', '-i', '-U', pat, 'docs', 'hdl', 'tb']))
    print(f'## probe {label} :: {pat}  ({len(hits)} lines)')
    for f, n in sorted(hits):
        s = 'MATCH' if (f, n) in match else 'CONTEXT' if (f, n) in ctx else 'MISS'
        cited = set().union(*[cited_lines(c) for c in rows.get(f, [])]) if f in rows else set()
        r = 'ROW-CITED' if n in cited else ('ROW-FILE' if f in rows else 'NO-ROW')
        src = open(f'{PP}/{f}', encoding='utf-8', errors='replace').read().splitlines()[n - 1].strip()[:120]
        print(f'  {s:7} {r:9} {f}:{n}  {src}')

print('## RESULT', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
