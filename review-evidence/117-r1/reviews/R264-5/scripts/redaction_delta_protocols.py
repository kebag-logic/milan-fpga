#!/usr/bin/env python3
"""Classify, by protocol, every capture record that differs between two archive commits.

Usage: redaction_delta_protocols.py <bare-repo> <old-commit> <new-commit>

Tap records are decoded past the 28-octet envelope; capture-host records
from byte 0. Reports per capture the differing records grouped by
(tap|host, ethertype, IP protocol, UDP port) and flags any differing gPTP
(0x88F7), AVTP/AVDECC (0x22F0) or MSRP/MVRP (0x22EA/0x88F5) frame, which
would mean a measurement frame was altered. Prints no payload bytes.
"""
import collections
import struct
import subprocess
import sys


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout


def recs(raw):
    off, out = 24, []
    while off + 16 <= len(raw):
        incl = struct.unpack("<I", raw[off + 8:off + 12])[0]
        out.append(raw[off + 16:off + 16 + incl])
        off += 16 + incl
    return out


def cls(p):
    tap = len(p) >= 42 and struct.unpack("<I", p[:4])[0] == 6 and struct.unpack("<I", p[8:12])[0] in (2, 3)
    fr = p[28:] if tap else p
    if len(fr) < 14:
        return ("tap" if tap else "host", "short")
    et, o = struct.unpack(">H", fr[12:14])[0], 14
    while et == 0x8100 and len(fr) >= o + 4:
        et, o = struct.unpack(">H", fr[o + 2:o + 4])[0], o + 4
    key = ["tap" if tap else "host", f"0x{et:04x}"]
    pl = fr[o:]
    if et == 0x0800 and len(pl) >= 24:
        ihl = (pl[0] & 15) * 4
        key.append(f"ip{pl[9]}")
        if pl[9] == 17:
            key.append(f"udp{min(struct.unpack('>HH', pl[ihl:ihl + 4]))}")
    elif et == 0x86DD and len(pl) >= 44:
        key.append(f"ip6-{pl[6]}")
        if pl[6] == 17:
            key.append(f"udp{min(struct.unpack('>HH', pl[40:44]))}")
    elif et == 0x22F0 and pl:
        key.append(f"subtype0x{pl[0]:02x}")
    return tuple(key)


def main():
    repo, old, new = sys.argv[1:]
    bad = 0
    for n in git(repo, "diff", "--name-only", old, new).decode().split():
        if not n.endswith(".pcap"):
            continue
        a, b = recs(git(repo, "cat-file", "blob", f"{old}:{n}")), recs(git(repo, "cat-file", "blob", f"{new}:{n}"))
        if len(a) != len(b):
            print(f"{n}: record count differs {len(a)} vs {len(b)}")
            bad += 1
            continue
        c = collections.Counter(cls(x) for x, y in zip(a, b) if x != y)
        meas = {k: v for k, v in c.items() if k[1] in ("0x88f7", "0x22ea", "0x88f5") or (k[1] == "0x22f0" and k[2] in ("subtype0x04", "subtype0x02", "subtype0xfc"))}
        bad += sum(meas.values())
        print(f"{n.split('117-r1/')[1]}: {sum(c.values())} records differ: {dict(c)}; measurement frames altered: {sum(meas.values())}")
    print("measurement frames altered in total:", bad)


if __name__ == "__main__":
    main()
