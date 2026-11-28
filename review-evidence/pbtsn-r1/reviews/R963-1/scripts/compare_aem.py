#!/usr/bin/env python3
"""Compare two AEM descriptor dumps ("type index length hex" per line), keyed by the type/index
in each descriptor's own header (bytes 0..3); a dump column that disagrees is reported.
Usage: compare_aem.py FIRMWARE_DUMP OTHER_DUMP"""
import sys, zlib

def load(path):
    out = {}
    order = []
    for line in open(path, encoding='ascii'):
        f = line.split()
        if len(f) != 4:
            continue
        t, i, n, h = int(f[0]), int(f[1]), int(f[2]), bytes.fromhex(f[3])
        if len(h) != n:
            raise SystemExit(f'{path}: length mismatch at {t}/{i}')
        ht, hi = int.from_bytes(h[0:2], 'big'), int.from_bytes(h[2:4], 'big')
        if (ht, hi) != (t, i):
            print(f'{path}: dump column says {t}/{i}, descriptor header says {ht}/{hi}')
        t, i = ht, hi
        if (t, i) in out:
            raise SystemExit(f'{path}: duplicate {t}/{i}')
        out[(t, i)] = h
        order.append((t, i))
    return out, order

a, ao = load(sys.argv[1])
b, bo = load(sys.argv[2])
print(f'{sys.argv[1]}: {len(a)} descriptors, {sum(map(len, a.values()))} bytes')
print(f'{sys.argv[2]}: {len(b)} descriptors, {sum(map(len, b.values()))} bytes')
print('same key set:', set(a) == set(b))
diff = [k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
print('differing descriptors:', diff)
for name, d in (('A', a), ('B', b)):
    crc = zlib.crc32(b''.join(d[k] for k in sorted(d))) & 0xffffffff
    print(f'{name} CRC-32 of sorted concatenation: 0x{crc:08x}')
print('order identical:', ao == bo)
sys.exit(1 if diff or set(a) != set(b) else 0)
