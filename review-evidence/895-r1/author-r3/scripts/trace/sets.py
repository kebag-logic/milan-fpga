import sys
# sets.py NM_FILE [names...]: address, size and fetch-L1 sets (64 B lines, 64 sets) of each text symbol, in address order
syms = []
for l in open(sys.argv[1]):
    f = l.split()
    if len(f) == 4 and f[2] in 'tTwW':
        syms.append((int(f[0], 16), int(f[1], 16), f[3]))
want = set(sys.argv[2:])
for a, s, n in syms:
    if not want or n in want:
        print(f"{a:08x} {s:5d} {n:28s} sets {(a >> 6) & 63:2d}..{((a + s - 1) >> 6) & 63:2d}")
