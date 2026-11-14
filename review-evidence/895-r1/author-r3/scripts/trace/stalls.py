#!/usr/bin/env python3
"""stalls.py ELF LOG CPU_START CYCLES [TOP]: in LOG's committed-PC trace, the pass that runs CYCLES CPU cycles from
CPU_START (its PASS line's start_cpu): each commit's wait (cycles since the previous commit, less one) charged to the
instruction that committed, summed by function, and the TOP instructions by wait with their disassembly. Read-only."""
import bisect, collections, re, subprocess, sys
BIN = '$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-'
elf, logp, c0, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
top = int(sys.argv[5]) if len(sys.argv) > 5 else 25
syms = []
for l in subprocess.run([BIN + 'nm', '-S', elf], capture_output=True, text=True).stdout.splitlines():
    f = l.split()
    if len(f) == 4 and f[2] in 'tTwW':
        syms.append((int(f[0], 16), int(f[1], 16), f[3]))
syms.sort(); addrs = [a for a, _, _ in syms]
def fn(pc):
    i = bisect.bisect_right(addrs, pc) - 1
    return syms[i][2] if i >= 0 and pc < syms[i][0] + max(syms[i][1], 1) else f'?{pc:x}'
dis = {}
for l in subprocess.run([BIN + 'objdump', '-d', elf], capture_output=True, text=True).stdout.splitlines():
    m = re.match(r'\s*([0-9a-f]+):\s+[0-9a-f]+\s+(.*)', l)
    if m: dis[int(m.group(1), 16)] = m.group(2).split('#')[0].strip()
prev = None; byfn = collections.Counter(); bypc = collections.Counter(); commits = 0; fetch = collections.Counter()
for l in open(logp, errors='replace'):
    if l.startswith('PC '):
        _, c, p = l.split(); c = int(c); p = int(p, 16)
        if c < c0 or c >= c0 + n: prev = c if c0 <= c else None; continue
        commits += 1
        if prev is not None:
            w = c - prev - 1
            byfn[fn(p)] += w; bypc[p] += w
        prev = c
    elif l.startswith('FETCH '):
        _, c, p = l.split(); c = int(c)
        if c0 <= c < c0 + n: fetch[fn(int(p, 16))] += 1
print(f"commits {commits}, waits {sum(byfn.values())}, refills {sum(fetch.values())}")
for f, w in byfn.most_common(14):
    print(f"   {f:28s} wait {w:6d} refills {fetch[f]}")
for p, w in bypc.most_common(top):
    print(f"   {p:08x} {fn(p):24s} wait {w:5d}  {dis.get(p, '')}")
