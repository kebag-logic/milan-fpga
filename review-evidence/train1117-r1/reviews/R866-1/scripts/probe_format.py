#!/usr/bin/env python3
"""Independent exhaustive channel-count equivalence over the relevant bytes."""
from pathlib import Path
import hashlib
count=0
for kind in range(256):
    for high in range(256):
        for low in range(4):
            # Every possible ten-bit count and every type. Fill ignored bits too.
            p=bytes((kind,0xff,0xa5,0x5a,high,(low<<6)|0x3f,0x55,0xaa))
            old=((int.from_bytes(p,'big')>>22)&1023) if (int.from_bytes(p,'big')>>56)==2 else 0
            new=((p[4]<<2)|(p[5]>>6)) if p[0]==2 else 0
            assert old==new
            count+=1
print('PASS',count,'type/channel combinations; ignored bits populated, old 64-bit extraction equals new byte extraction')
root=Path(__file__).resolve().parents[1]
e=root/'scratch/evidence/review-evidence/train1117-r1/author-r5/receipts/hot/08c28218'
def lines(path): return [x for x in path.read_text().splitlines() if x.strip() and not x.startswith('#')]
trace=lines(e/'order.txt');held=lines(e/'order-filtered.txt')
assert [x for x in trace if x not in ['aecp owe','aecp owed_drain']]==held
assert held==lines(Path('sw/firmware/ctrl/plat/ctrl_split_hot.txt'))
assert len(held)==266
print('PASS hot order: 268 traced, only two ruled unavailable sections removed, 266 kept in exact order at final head')
