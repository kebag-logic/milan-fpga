# SPDX-License-Identifier: Apache-2.0
"""Emulate the parent's LeaveAll detector (milan-fpga 554e61d2,
sw/firmware/ctrl/test/srp_latency.cpp:68-77) over MVRP and MSRP PDUs in a
transmit trace, and compare its verdict with the true LeaveAll presence.

Usage: parent_walker_probe.py <trace> [--fixed]
--fixed emulates the vector walk proposed for the pin bump in the public handoff.
"""
import sys


def be16(b, o):
    return b[o] << 8 | b[o + 1]


def walker(frame, mvrp, fixed):
    la, off, n_len = False, 15, len(frame)
    steps = 0
    while off + 2 < n_len and (frame[off] or frame[off + 1]):
        steps += 1
        if steps > 10000:
            raise RuntimeError("no progress")
        width = frame[off + 1]
        off += 2
        end = n_len
        if not mvrp:
            end = off + 2 + be16(frame, off)
            off += 2
        la = la or bool(frame[off] & 0x20) if off < n_len else la
        if not mvrp:
            off = end
        elif not fixed:
            n = be16(frame, off) & 8191 if off + 1 < n_len else 0
            off += 2 + width + (n + 2) // 3 + 2
        else:
            while off + 2 <= n_len and (frame[off] or frame[off + 1]):
                n = be16(frame, off) & 8191
                off += 2 + width + (n + 2) // 3
            off += 2
    return la


def true_la(pdu, mvrp):
    off = 1
    while off + 2 <= len(pdu) and (pdu[off] or pdu[off + 1]):
        mtype, width = pdu[off], pdu[off + 1]
        off += 2
        end = len(pdu)
        if not mvrp:
            end = off + 2 + be16(pdu, off)
            off += 2
        while off + 2 <= end and (pdu[off] or pdu[off + 1]):
            vh = be16(pdu, off)
            if vh >> 13:
                return True
            n = vh & 8191
            sub = (n + 3) // 4 if (not mvrp and mtype == 3) else 0
            off += 2 + width + (n + 2) // 3 + sub
        off = end if not mvrp else off + 2
    return False


def main():
    fixed = "--fixed" in sys.argv
    counts = {"mvrp": 0, "msrp": 0, "false_la": 0, "missed_la": 0, "multi_vector_mvrp": 0}
    examples = []
    for line in open(sys.argv[1], encoding="ascii"):
        f = line.rstrip("\n").split("\t")
        if f[0] != "S" or len(f[8]) != 2 * int(f[7]):
            continue
        eth = int(f[4], 16)
        if eth not in (0x88F5, 0x22EA):
            continue
        mvrp = eth == 0x88F5
        pdu = bytes.fromhex(f[8])
        frame = bytes(12) + eth.to_bytes(2, "big") + pdu
        counts["mvrp" if mvrp else "msrp"] += 1
        truth = true_la(pdu, mvrp)
        got = walker(frame, mvrp, fixed)
        if mvrp and f[9].split(";")[0].count("x") and any(int(m.split("x")[1]) > 1 for m in f[9].split(";")[0].split(",")):
            counts["multi_vector_mvrp"] += 1
        if got and not truth:
            counts["false_la"] += 1
            examples.append(f"FALSE-LA {f[1]}#{f[2]} {f[8]}")
        if truth and not got:
            counts["missed_la"] += 1
            examples.append(f"MISSED-LA {f[1]}#{f[2]} {f[8]}")
    print(("fixed walk: " if fixed else "current walk: ") + str(counts))
    for e in examples[:10]:
        print(e)


if __name__ == "__main__":
    main()
