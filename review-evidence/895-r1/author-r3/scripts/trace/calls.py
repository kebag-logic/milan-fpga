import sys, bisect, collections
# calls.py NM LOG ENTRY_HEX STOP_LO_HEX STOP_HI_HEX: each call from ENTRY until the first PC in [STOP_LO, STOP_HI);
# per function: commits, cycles (charged to the function of the previous commit), refills (FETCH lines) by function
syms = []
for l in open(sys.argv[1]):
    f = l.split()
    if len(f) == 4 and f[2] in 'tTwW':
        syms.append((int(f[0], 16), int(f[1], 16), f[3]))
syms.sort()
addrs = [a for a, _, _ in syms]
def fn(pc):
    i = bisect.bisect_right(addrs, pc) - 1
    if i >= 0 and syms[i][0] <= pc < syms[i][0] + max(syms[i][1], 1):
        return f"{syms[i][2]}@{syms[i][0]:x}"
    return f"?{pc:x}"
entry, lo, hi = (int(x, 16) for x in sys.argv[3:6])
ev = []
for l in open(sys.argv[2]):
    if l.startswith('PC '):
        _, c, p = l.split(); ev.append(('P', int(c), int(p, 16)))
    elif l.startswith('FETCH '):
        _, c, p = l.split(); ev.append(('F', int(c), int(p, 16)))
calls, cur = [], None
prev = None
for kind, c, p in ev:
    if kind == 'P':
        if cur is None and p == entry:
            cur = {'start': c, 'commits': collections.Counter(), 'cycles': collections.Counter(), 'fetch': [], 'seq': []}
        elif cur is not None and lo <= p < hi:
            cur['end'] = c; calls.append(cur); cur = None
        if cur is not None:
            f = fn(p)
            cur['commits'][f] += 1
            if prev is not None and prev[0] is not None:
                cur['cycles'][prev[1]] += c - prev[0]
            if not cur['seq'] or cur['seq'][-1] != f:
                cur['seq'].append(f)
            prev = (c, f)
        else:
            prev = None
    elif kind == 'F' and cur is not None:
        cur['fetch'].append((c, p, fn(p)))
for k, cl in enumerate(calls):
    print(f"== call {k}: cycles {cl['end'] - cl['start']} commits {sum(cl['commits'].values())} refills {len(cl['fetch'])}")
    for f, n in sorted(cl['commits'].items(), key=lambda x: -cl['cycles'][x[0]]):
        print(f"   {f:34s} commits {n:5d} cycles {cl['cycles'][f]:6d}")
    print('   refills: ' + ' '.join(f"{p:x}({f.split('@')[0]},set{(p>>6)&63})" for _, p, f in cl['fetch']))
