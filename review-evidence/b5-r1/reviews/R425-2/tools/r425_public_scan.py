#!/usr/bin/env python3
"""Structural public-text scan (reviewer-written). Prints per-pattern hit counts and
the hit lines for review. A further vendor/product/host list is applied privately
and is deliberately not part of this file.
usage: r425_public_scan.py <file> [<file> ...]"""
import re, sys
PATS = {
    "mac": r"\b[0-9a-fA-F]{2}([:-][0-9a-fA-F]{2}){5}\b",
    "ipv4": r"\b\d{1,3}(\.\d{1,3}){3}\b",
    "home path": r"(/home/|/Users/|~/)",
    "iface": r"\b(enp\d|eth\d|wlan\d|enx[0-9a-f]|wlp\d|br\d|tap\d)",
    "hostname-like": r"\bpw\d\b|\blocalhost\b|\.local\b|\.lan\b",
    "em dash": "—",
    "digital audio connector/format": r"\b(AES3|AES/EBU|S/?PDIF|ADAT|MADI|TOSLINK|XLR|BNC|optical|coax(ial)?)\b",
    "clock wiring words": r"(?i)\b(word ?clock|AES11|clocked from|clock (master|slave)|sync(ed)? (to|from) the (switch|peer|capture)|reference clock input)\b",
    "numbered channel map": r"(?i)\b(capture|input|output|interface) channels? \d+|\bchannels? \d+ and \d+ of the capture|\bch ?\d+\b",
    "cable/patch": r"(?i)\b(cable|patch(ed)?|wired to|connected to port|switch port \d+)\b",
    "serial-like": r"\b[A-Z0-9]{12,}\b",
}
tot = 0
for f in sys.argv[1:]:
    txt = open(f, encoding="utf-8", errors="replace").read().split("\n")
    for name, p in PATS.items():
        hits = [(i + 1, l.strip()[:140]) for i, l in enumerate(txt) if re.search(p, l)]
        tot += len(hits)
        print(f"{f}: {name}: {len(hits)}")
        for i, l in hits:
            print(f"    {i}: {l}")
print(f"total hits {tot}")
