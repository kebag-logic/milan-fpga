#!/usr/bin/env python3
"""Record-level delta of the last redaction round between two archive commits.

Usage: redaction_delta_records.py <bare-repo> <old-commit> <new-commit>

For every capture that differs, walks both pcaps record by record (headers
must be identical) and classifies each differing record as a tap record
(28-octet envelope, tag 6, port 2 or 3: a frame on the DUT link) or a
capture-host record (the capture server's own traffic). Also reports whether
every changed byte in the new copy is '#'. Prints no payload bytes.
"""
import struct
import subprocess
import sys


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True).stdout


def records(raw):
    off, out = 24, []
    while off + 16 <= len(raw):
        hdr = raw[off:off + 16]
        incl = struct.unpack("<I", hdr[8:12])[0]
        out.append((hdr, raw[off + 16:off + 16 + incl]))
        off += 16 + incl
    return raw[:24], out


def main():
    repo, old, new = sys.argv[1:]
    names = git(repo, "diff", "--name-only", old, new).decode().split()
    ok = True
    for n in names:
        if not n.endswith(".pcap"):
            print(f"non-capture change: {n}")
            continue
        a = git(repo, "cat-file", "blob", f"{old}:{n}")
        b = git(repo, "cat-file", "blob", f"{new}:{n}")
        ga, ra = records(a)
        gb, rb = records(b)
        same_shape = ga == gb and len(ra) == len(rb) and all(x[0] == y[0] for x, y in zip(ra, rb))
        tap_changed = host_changed = 0
        only_hash = True
        for (_, pa), (_, pb) in zip(ra, rb):
            if pa == pb:
                continue
            is_tap = len(pa) >= 42 and struct.unpack("<I", pa[:4])[0] == 6 and struct.unpack("<I", pa[8:12])[0] in (2, 3)
            if is_tap:
                tap_changed += 1
            else:
                host_changed += 1
            if any(x != y and y != 0x23 for x, y in zip(pa, pb)) or len(pa) != len(pb):
                only_hash = False
        ok &= same_shape and tap_changed == 0 and only_hash
        print(f"{n.split('117-r1/')[1]}: records {len(ra)}; headers identical {same_shape}; changed tap records {tap_changed}; changed capture-host records {host_changed}; every changed byte now '#': {only_hash}")
    print("RESULT", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
