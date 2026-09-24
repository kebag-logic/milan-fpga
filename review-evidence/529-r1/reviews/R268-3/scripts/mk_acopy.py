#!/usr/bin/env python3
"""Disposable harness probe: just before [NOTIFY-CRF]'s A-copy check, flip
one bit of A's logged push inside the counter block (the FRAMES_RX quadlet's
last byte, frame offset 46 + 4*11 + 3). Only that check should turn red.
usage: mk_acopy.py TREE"""
import sys
p = sys.argv[1] + "/tb/verilator/milan_dp/sim_nxn.cpp"
s = open(p).read()
old = '''        ck("[NOTIFY-CRF] ...and so is A's copy", static_cast<long>(notify_same_from('''
assert s.count(old) == 1
new = '''        {   // R268-3 PROBE: corrupt one body bit of A's logged copy
            const std::vector<uint8_t>* pa = notify_last(0x0029, CTL_A, 0x0005, ix);
            if (pa && pa->size() > 93)
                const_cast<std::vector<uint8_t>*>(pa)->at(46 + 4 * 11 + 3) ^= 0x01;
        }
''' + old
open(p, "w").write(s.replace(old, new))
print("patched", p)
