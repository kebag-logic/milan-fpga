# Census of AVTP control statuses of the entity's transmitted ACMP and AECP frames in a real wire.log (#868).
# Usage: python3 -I status_census.py <wire.log>...
import collections
import sys
for path in sys.argv[1:]:
    c = collections.Counter()
    for line in open(path):
        w = line.split()
        if not w or w[0] != 'TXW':
            continue
        d = bytes.fromhex(w[4])
        if d[12:14] != b'\x22\xf0' or d[14] not in (0xFB, 0xFC):
            continue
        c[('aecp' if d[14] == 0xFB else 'acmp', d[15] & 0x0F, d[16] >> 3)] += 1
    print(path.rsplit('/', 1)[-1], ' '.join(f'{p}:type{t}:status{s}={n}' for (p, t, s), n in sorted(c.items())))
