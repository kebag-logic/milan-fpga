#!/usr/bin/env python3
"""Decode the published DUT start/end console reads that differ: PP_STAT
(bit 11 nvm_pend), the milan_nvm lines, and the 0x8D4..0x8DF slip/rail words.
usage: dut_state_diff.py <dut-start.txt> <dut-end.txt>"""
import re, sys
def rd(p):
    t = re.sub(r"\x1b\[[0-9;]*m", "", open(p, errors="replace").read())
    pp = int(re.search(r"PP_STAT=([0-9a-f]{8})", t).group(1), 16)
    nvm = re.findall(r"^NVM: .*$", t, re.M)
    m = re.search(r"^0x900008d4\s+((?:[0-9a-f]{2} ){12})", t, re.M)
    w = [int.from_bytes(bytes.fromhex(m.group(1).replace(" ", ""))[i:i + 4], "little") for i in (0, 4, 8)]
    return pp, nvm, w
for name, p in (("start", sys.argv[1]), ("end", sys.argv[2])):
    pp, nvm, w = rd(p)
    print(f"{name}: PP_STAT=0x{pp:08x} nvm_pend(bit11)={pp >> 11 & 1}")
    for l in nvm:
        print(f"  {l}")
    print(f"  SLIP_LB dups={w[0] & 0xffff} skips={w[0] >> 16}; SLIP_TDM dups={w[1] & 0xffff} skips={w[1] >> 16}; 0x8DC=0x{w[2]:08x} (upper half {w[2] >> 16})")
