#!/usr/bin/env python3
"""Reviewer scan: bench-specific shapes in a list of files (paths as argv[2:], root argv[1]).
Patterns are assembled so this script does not itself spell a product name."""
import re, sys, pathlib
root = pathlib.Path(sys.argv[1])
tap = "profi" + "shark"
pats = {
 "tap-product": re.compile(tap, re.I),
 "tap-vendor": re.compile("profi" + "tap", re.I),
 "host-pw": re.compile(r"(?<![A-Za-z0-9_])pw[0-9](?![A-Za-z0-9])"),
 "switch-DN": re.compile(r"DN-?1(?![0-9])"),
 "ipv4-private": re.compile(r"(?<![0-9.])(10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![0-9])"),
 "ipv4-any": re.compile(r"(?<![0-9.])(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?![0-9.])"),
 "home-path": re.compile(r"/home/[a-z][a-z0-9_-]+"),
 "serial-ish": re.compile(r"(ftdi|serial|probe)[^\n]{0,40}\b[0-9A-F]{8,16}\b", re.I),
 "mac-ish": re.compile(r"\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b"),
}
tot = 0
for rel in sys.argv[2:]:
    p = root / rel
    for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for k, rx in pats.items():
            for m in rx.finditer(line):
                tot += 1
                print(f"{k}\t{rel}:{n}\t{m.group(0)}\t{line.strip()[:110]}")
print(f"# total raw hits: {tot}")
