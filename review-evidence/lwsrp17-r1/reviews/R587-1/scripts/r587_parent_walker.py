#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Emulate the parent LeaveAll detector (milan-fpga 554e61d2,
sw/firmware/ctrl/test/srp_latency.cpp:68-77) and the vector walk proposed in
the public handoff, over real MRPDUs taken from r587_fuzz outputs.

Usage: r587_parent_walker.py ETHERTYPE_HEX FILE...
Ground truth is the reviewer decoder: any VectorAttribute with LeaveAll set.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r587_decode import decode  # noqa: E402


def be16(b, o):
    return (b[o] << 8) | b[o + 1] if o + 1 < len(b) else (b[o] << 8 if o < len(b) else 0)


def old_walk(f, mvrp):
    # Verbatim logic of srp_latency.cpp:68-77; out-of-frame reads count as a fault.
    la, off, n_len = False, 15, len(f)
    while off + 2 < n_len and (f[off] or f[off + 1]):
        width = f[off + 1]
        off += 2
        end = n_len
        if not mvrp:
            end = off + 2 + be16(f, off)
            off += 2
        if off >= n_len:
            return la, True
        la = la or bool(f[off] & 0x20)
        if not mvrp:
            off = end
        else:
            n = be16(f, off) & 8191
            off += 2 + width + (n + 2) // 3 + 2
    return la, off > n_len


def new_walk(f, mvrp):
    # The handoff's proposed MVRP branch: every vector up to the EndMark.
    la, off, n_len = False, 15, len(f)
    while off + 2 < n_len and (f[off] or f[off + 1]):
        width = f[off + 1]
        off += 2
        end = n_len
        if not mvrp:
            end = off + 2 + be16(f, off)
            off += 2
        la = la or bool(f[off] & 0x20)
        if not mvrp:
            off = end
        else:
            while off + 2 <= n_len and (f[off] or f[off + 1]):
                n = be16(f, off) & 8191
                off += 2 + width + (n + 2) // 3
            off += 2
    return la, off > n_len


def main():
    eth = int(sys.argv[1], 16)
    mvrp = eth == 0x88F5
    seen = old_false = old_oob = new_false = 0
    example = None
    for path in sys.argv[2:]:
        for line in open(path):
            p = line.split()
            if not p or p[0] != "S" or len(p) < 4:
                continue
            pdu = bytes.fromhex(p[3])
            truth = any(v["la"] for _, vecs, _ in decode(pdu, eth)[0] for v in vecs)
            frame = bytes(12) + eth.to_bytes(2, "big") + pdu
            seen += 1
            la, oob = old_walk(frame, mvrp)
            if la != truth:
                old_false += 1
                example = example or pdu.hex()
            old_oob += oob
            la2, _ = new_walk(frame, mvrp)
            new_false += la2 != truth
    print(f"pdus={seen} old_walk_wrong={old_false} old_walk_past_end={old_oob} "
          f"proposed_walk_wrong={new_false} example={example}")


if __name__ == "__main__":
    main()
