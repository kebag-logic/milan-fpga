#!/usr/bin/env python3
"""Public-safety pattern scan of the round-2 text.

Usage: public_scan.py <file>...
Flags addresses, host-like names, local paths, vendor/product words, and
capture-layout tokens (channel counts or indices of the external capture,
'<n>ch', 'hw:' device strings). Every hit is printed for a human to judge;
a hit is not by itself a finding.
"""
import re, sys

PATTERNS = {
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "mac": r"\b[0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5}\b",
    "local-path": r"(?:/home/|/tmp/|/data/|/mnt/|/srv/|~/)\S*",
    "host-like": r"\b[a-z][a-z0-9-]{2,}\.(?:local|lan|home|internal)\b",
    "alsa-device": r"\bhw:\d|\bplughw:|\bcard\s*\d",
    "n-channel": r"\b\d+\s*-?ch\b|\b\d+[- ]channel\b|\bchannels? \d+\b",
    "usb-id": r"\b[0-9a-f]{4}:[0-9a-f]{4}\b",
    "vendor": r"(?i)\b(?:motu|rme|focusrite|presonus|behringer|yamaha|avid|apple|macbook|l-acoustics|meyer|<bench-switch-vendor-name>|biamp|"
              r"netgear|cisco|luminex|extreme networks|hive|milan-?ready|beagle\w*|raspberry|xilinx|zynq|arty|kria|digilent|"
              r"audio precision|apx|rohde|keysight|tektronix|ubuntu|debian|fedora|arch linux|steinberg|merging|"
              r"motu avb|ultralite|8a|112d|monitor 8|lk\d+|la_avdecc|hive-?controller)\b",
}

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8", errors="replace").read().splitlines()
    hits = 0
    for n, line in enumerate(text, 1):
        for name, rx in PATTERNS.items():
            for m in re.finditer(rx, line):
                hits += 1
                print(f"{path}:{n}: {name}: {m.group(0)!r} :: {line.strip()[:140]}")
    print(f"== {path}: {hits} hit(s)")
