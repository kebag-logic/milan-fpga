#!/usr/bin/env python3
"""Value-blind privacy scan of lane B8's public surfaces.

usage: privacy_scan.py <file-or-dir>...

Prints, per pattern class, the file and line number of every hit, and the
matched token only where the class is non-sensitive by construction (labels,
placeholders). Classes: home paths, IPv4 literals, unicast MACs, interface
names, hostnames-like FQDNs, ALSA device strings and capture-command channel /
format arguments and USB serial-like strings. Bench product and vendor names
are not listed here (a published deny-list would itself hint at the bench); they
were checked by reading the hits of the other classes and the page.
"""
import os
import re
import sys

PATTERNS = {
    "home-path": re.compile(r"/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+|/root/"),
    "ipv4": re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
    "mac-unicast": re.compile(r"(?i)\b(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}\b"),
    "iface": re.compile(r"\b(?:enp\d+s\d+\w*|eth\d+|wlan\d+|enx[0-9a-f]{12}|eno\d+|ens\d+)\b"),
    "fqdn": re.compile(r"\b[a-z0-9-]+\.(?:local|lan|home|internal|corp)\b", re.I),
    "alsa-dev": re.compile(r"\b(?:hw|plughw):\s*[A-Za-z0-9_]+(?:,\d+)?"),
    "capture-args": re.compile(r"(?:\s-c\s*\d+|--channels[= ]\d+|\s-f\s*[SU]\d+_[LB]E|--format[= ][SU]\d+)"),
    "sample-format": re.compile(r"\b[SU](?:16|24|32)(?:_3)?_[LB]E\b"),
    "usb-serial": re.compile(r"(?i)\bserial[^\n]{0,20}[:=]\s*[A-Z0-9]{6,}"),
}


def files(args):
    for a in args:
        if os.path.isdir(a):
            for root, _, names in os.walk(a):
                for n in sorted(names):
                    yield os.path.join(root, n)
        else:
            yield a


hits = 0
for path in files(sys.argv[1:]):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    for ln, line in enumerate(text.splitlines(), 1):
        for cls, rx in PATTERNS.items():
            for m in rx.finditer(line):
                tok = m.group(0)
                if cls == "ipv4" and (tok.startswith("0.") or all(int(x) < 256 for x in tok.split(".")) is False):
                    continue
                if cls == "mac-unicast" and int(tok[:2], 16) & 1:
                    continue  # multicast (e.g. MAAP 91:e0:f0)
                hits += 1
                print(f"{cls}\t{path}:{ln}\t{tok if cls in ('alsa-dev', 'capture-args', 'sample-format') else '<value withheld>'}")
print(f"hits={hits}")
