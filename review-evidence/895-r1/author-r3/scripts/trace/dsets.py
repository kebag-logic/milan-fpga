import sys
# dsets.py NM_FILE: data/bss symbols, address, size, D-cache sets (64 B lines, 128 sets)
for l in open(sys.argv[1]):
    f = l.split()
    if len(f) == 4 and f[2] in 'dDbBrR' and int(f[1], 16) >= 8:
        a, s = int(f[0], 16), int(f[1], 16)
        print(f"{a:08x} {s:6d} {f[2]} {f[3]:30s} dsets {(a >> 6) & 127:3d}..{((a + s - 1) >> 6) & 127:3d}")
