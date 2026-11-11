# Each AEM response in a real wire.log (#868): command_type, the descriptor it names, status.
# Usage: python3 -I aecp_status.py <wire.log>
import collections
import sys
c = collections.Counter()
for line in open(sys.argv[1]):
    w = line.split()
    if not w or w[0] != 'TXW':
        continue
    d = bytes.fromhex(w[4])
    if d[12:14] != b'\x22\xf0' or d[14] != 0xFB or (d[15] & 0x0F) != 1:
        continue
    ct = int.from_bytes(d[36:38], 'big') & 0x7FFF
    desc = (int.from_bytes(d[38:40], 'big'), int.from_bytes(d[40:42], 'big')) if len(d) >= 42 else None
    c[(f'0x{ct:04x}', desc, d[16] >> 3)] += 1
for k, n in sorted(c.items()):
    print(k, n)
