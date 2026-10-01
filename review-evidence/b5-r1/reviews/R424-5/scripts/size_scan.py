#!/usr/bin/env python3
"""Withheld-value scan for the every-channel capture sizes.

Usage: size_scan.py <old-page> <target> [<target> ...]
The withheld sizes and the capture's channel count are derived IN MEMORY from
the three every-channel rows of <old-page> and are never printed. Each target
is scanned for (1) any withheld size, in plain or comma-grouped form; (2) any
number that divides, at 24 or 32 bits and 48 kHz, to the derived channel count
over any duration the target states (within 1% and in whole frames, with or
without a 44-byte WAV header); whole multiples with no matching duration are
listed as info
when the line states bytes or is an artifact-table row; (3) the channel count as a standalone token next to a word
starting "channel". Output is line numbers and labels only.
"""
import re
import sys

ROW = re.compile(r"^\| [^|]*every channel, ([0-9.]+) s \| ([0-9]+) \|", re.M)
NUM = re.compile(r"(?<![0-9A-Za-z_.,])([0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?![0-9A-Za-z_])")
BYTEISH = re.compile(r"bytes?\b|\| [0-9]+ \| `[0-9a-f]{64}` \|", re.I)
DUR = re.compile(r"([0-9]+(?:\.[0-9]+)?) ?s\b")


def derive(old):
    rows = [(float(d), int(s)) for d, s in ROW.findall(old)]
    exact = {s / (d * 48000 * 3) for d, s in rows if s % int(d * 48000 * 3) == 0}
    assert len(rows) == 3 and len(exact) == 1, "control: old page must hold three rows, the exact ones consistent"
    chan = int(exact.pop())
    assert all(s % (3 * chan) == 0 for _, s in rows), "control: every row is whole frames of the derived width"
    return [s for _, s in rows], chan


def scan(path, sizes, chan):
    text = open(path, encoding="utf-8").read()
    durs = {float(d) for d in DUR.findall(text) if float(d) > 0} | {10.0, 25.0, 3.0}
    hits, infos = [], []
    for ln, line in enumerate(text.splitlines(), 1):
        for m in NUM.finditer(line):
            n = int(m.group(1).replace(",", ""))
            if n in sizes:
                hits.append((ln, "withheld size"))
                continue
            if n >= 100000:
                for d in durs:
                    for b in (3, 4):
                        for hdr in (0, 44):
                            r = (n - hdr) / (d * 48000 * b)
                            if abs(r - chan) / chan < 0.01 and (n - hdr) % (b * chan) == 0:
                                hits.append((ln, f"divides to the channel count within 1% of a stated duration ({b} bytes, header {hdr})"))
                if (n % (3 * chan) == 0 or n % (4 * chan) == 0) and BYTEISH.search(line):
                    infos.append((ln, "whole multiple of the derived frame width, no stated duration matches" ))
            if n == chan and re.search(r"channel", line[max(0, m.start() - 20):m.end() + 20], re.I):
                hits.append((ln, "channel count beside 'channel'"))
    print(f"{path}: {len(hits)} hit(s)")
    for ln, why in hits:
        print(f"  :{ln} {why}")
    for ln, why in infos:
        if not any(h[0] == ln for h in hits):
            print(f"  info :{ln} {why}")
    return len(hits)


def main(old, *targets):
    sizes, chan = derive(open(old, encoding="utf-8").read())
    print(f"control: derived {len(sizes)} withheld sizes and one channel count from the old page (values not printed)")
    ctl = scan(old, sizes, chan)
    print(f"control result: {'PASS' if ctl >= 3 else 'FAIL'} (the old page must hit at least its three rows)")
    total = sum(scan(t, sizes, chan) for t in targets)
    print(f"targets total hits: {total}")
    return 0 if ctl >= 3 else 2


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
