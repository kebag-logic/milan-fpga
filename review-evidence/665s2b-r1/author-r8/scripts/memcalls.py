#!/usr/bin/env python3
"""Per-call shape of the memory primitives in one traced window: calls, instructions a call, and how many
committed PCs fall on each source line of ctrl_mem.c (objdump -l). Scratch analysis.
usage: memcalls.py IMAGE_DIR TRACE_LOG OBJDUMP"""
import collections, re, subprocess, sys
img, log, objdump = sys.argv[1:4]
syms = {}
for line in open(f'{img}/symbols.txt'):
    f = line.split()
    if len(f) < 4:
        continue
    syms[f[3]] = (int(f[0], 16), int(f[1], 16))
funcs = {n: syms[n] for n in ('forward', 'backward', 'memset', 'memcmp', 'memmove', 'memcpy') if n in syms}
lines = {}
dis = subprocess.run([objdump, '-d', '-l', f'{img}/ctrl_app.elf'], capture_output=True, text=True).stdout
cur = None
for l in dis.splitlines():
    m = re.match(r'^(/.*ctrl_mem\.c):(\d+)', l) or re.match(r'^(.*ctrl_mem\.c):(\d+)', l)
    if m:
        cur = int(m.group(2)); continue
    if re.match(r'^\S.*:\d+', l):
        cur = None; continue
    m = re.match(r'^\s+([0-9a-f]+):', l)
    if m and cur is not None:
        lines[int(m.group(1), 16)] = cur
def which(pc):
    for n, (a, s) in funcs.items():
        if a <= pc < a + s:
            return n
    return None
calls = collections.Counter(); instr = collections.Counter(); per_line = collections.Counter()
sizes = collections.defaultdict(list)
prev = None; run = 0; runname = None
for l in open(log):
    if not l.startswith('PC '):
        continue
    pc = int(l.split()[2], 16)
    n = which(pc)
    if n:
        instr[n] += 1
        if pc in lines:
            per_line[lines[pc]] += 1
        if pc == funcs[n][0]:
            calls[n] += 1
    if n != runname:
        if runname in ('forward', 'memset', 'memcmp', 'backward'):
            sizes[runname].append(run)
        runname, run = n, 0
    run += 1
for n in funcs:
    s = sorted(sizes.get(n, []))
    q = (s[len(s)//4], s[len(s)//2], s[3*len(s)//4], s[-1]) if s else ()
    print(f'{n}: calls {calls[n]} instructions {instr[n]} runs {len(s)} instructions a run q1/med/q3/max {q}')
for ln, c in per_line.most_common(30):
    print(f'  ctrl_mem.c:{ln} {c}')
