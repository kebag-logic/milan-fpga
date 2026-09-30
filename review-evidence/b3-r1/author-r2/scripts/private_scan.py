#!/usr/bin/env python3
"""Scan files for private names without ever printing one.

usage: private_scan.py <redaction-map.json> <bench.env> <target> [<target> ...]

Token sources, read at run time and never written out:
- the lane's redaction map: literal values, regular expressions and check
  strings, each reported by its label;
- the lane's private endpoint file: every assigned value, reported by its key;
- this host: its host name, the account name, every network interface name
  and hardware address, and the EUI-64 clock identity of each address;
- extra regular expressions, one per line of the SCAN_EXTRA environment
  variable, supplied at run time so that the word list itself is never
  written to a file.

A target is a file or a directory (walked recursively); '-' reads standard
input. Each hit prints the target, the line number and the label only. The
exit status is 1 when any hit is found, else 0.
"""
import json
import os
import re
import socket
import sys


def host_tokens():
    out = [("<this-host-name>", socket.gethostname()), ("<this-host-name>", socket.gethostname().split(".")[0])]
    try:
        import pwd
        out.append(("<account>", pwd.getpwuid(os.getuid()).pw_name))
    except (ImportError, KeyError):
        pass
    for dev in sorted(os.listdir("/sys/class/net")):
        if dev == "lo":
            continue
        out.append(("<interface>", dev))
        try:
            mac = open(f"/sys/class/net/{dev}/address").read().strip().lower()
        except OSError:
            continue
        if not mac or set(mac) <= {"0", ":"}:
            continue
        b = mac.split(":")
        out.append(("<host-mac>", mac))
        out.append(("<host-mac>", mac.replace(":", "")))
        out.append(("<host-mac>", mac.replace(":", "-")))
        if len(b) == 6:
            eui = b[:3] + ["ff", "fe"] + b[3:]
            out.append(("<host-clock-id>", "".join(eui)))
            out.append(("<host-clock-id>", ":".join(eui)))
            flip = eui[:]
            flip[0] = f"{int(flip[0], 16) ^ 2:02x}"
            out.append(("<host-clock-id>", "".join(flip)))
            out.append(("<host-clock-id>", ":".join(flip)))
    return out


WORDS = [w for w in os.environ.get("SCAN_EXTRA", "").split("\n") if w]


def main():
    rmap, env, targets = sys.argv[1], sys.argv[2], sys.argv[3:]
    m = json.load(open(rmap))
    lits = [(lab, val) for val, lab in m["literal"]]
    regs = [(lab, re.compile(rx, re.I)) for rx, lab in m["regex"]]
    lits += [("<check>", c) for c in m["check"]]
    for line in open(env):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            v = v.strip().strip("'\"")
            if len(v) >= 3:
                lits.append((f"<env:{k.replace('export ', '')}>", v))
    lits += host_tokens()
    lits = [(lab, val.lower()) for lab, val in lits if len(val) >= 3]
    regs += [("<agent-or-home-word>", re.compile(w, re.I)) for w in WORDS]
    files = []
    for t in targets:
        if t == "-" or os.path.isfile(t):
            files.append(t)
        else:
            for root, dirs, fs in os.walk(t):
                dirs.sort()
                files += [os.path.join(root, f) for f in sorted(fs)]
    hits = 0
    for f in files:
        text = sys.stdin.read() if f == "-" else open(f, errors="replace").read()
        for n, line in enumerate(text.split("\n"), 1):
            low = line.lower()
            labs = sorted({lab for lab, val in lits if val in low} | {lab for lab, rx in regs if rx.search(line)})
            for lab in labs:
                hits += 1
                print(f"HIT {f}:{n} {lab}")
    print(f"scanned {len(files)} file(s) against {len(lits)} literal and {len(regs)} pattern token(s): {hits} hit(s)")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
