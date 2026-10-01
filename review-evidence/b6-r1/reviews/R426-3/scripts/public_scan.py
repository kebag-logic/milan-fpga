#!/usr/bin/env python3
"""R426-3: public-safety scan of the round-3 delta, the page and the commit message.

Usage: public_scan.py <repo> <base> <head> <page-path>
Flags addresses, MACs, interface/device names, host-like names, audio-gear or
switch vendor names, capture-layout phrases (channel counts or indices of the
capture, ALSA device strings) and clock-topology/wiring words in ADDED lines of
the delta and in the commit message. The full page is scanned too and its hits
are listed with a note when the line is unchanged since <base>.
"""
import re, subprocess, sys

repo, base, head, page = sys.argv[1:5]
run = lambda *a: subprocess.run(["git", "-C", repo, *a], check=True, capture_output=True, text=True).stdout
pats = {
    "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
    "mac": r"\b[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}\b",
    "entity-id": r"\b0x[0-9a-fA-F]{16}\b",
    "iface": r"\b(eth\d|enp\w+|enx\w+|usb\d|wlan\d|br\d|lo\b)",
    "alsa": r"\b(hw|plughw):\d|\bcard ?\d",
    "host-like": r"\b[\w-]+\.(local|lan|home|internal)\b|@[\w-]+:",
    "vendor": r"(?i)\b(motu|rme|focusrite|presonus|l-acoustics|avid|behringer|tascam|zoom|apple|"
              r"netgear|cisco|extreme|luminex|biamp|meyer|<bench-switch-vendor-name>|yamaha|allen|steinberg|universal audio|"
              r"digigram|merging|hive|milan manager|la network)\b",
    "capture-layout": r"(?i)\b\d+[- ]?(ch|channel)s?\b(?![- ]?(AAF|stream))|channel (index|indices) \d|"
                      r"\bslot \d|capture'?s? \d+ channels",
    "topology": r"(?i)\b(grandmaster|wired to|cable|patch(ed)?|port \d|switch port|spdif|aes3|adat|madi|word ?clock)\b",
}
rx = {k: re.compile(v) for k, v in pats.items()}
hits = 0
diff = run("diff", "-U0", base, head, "--", page)
added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
msg = run("log", "-1", "--format=%B", head)
for label, lines in (("delta added line", added), ("commit message", msg.splitlines())):
    for l in lines:
        for k, r in rx.items():
            m = r.search(l)
            if m:
                hits += 1
                print(f"HIT {label} [{k}] {m.group(0)!r}: {l.strip()[:120]}")
print(f"delta+message: {len(added)} added lines scanned, {hits} hits")
old = set(run("show", f"{base}:{page}").splitlines())
ph = 0
for i, l in enumerate(run("show", f"{head}:{page}").splitlines(), 1):
    for k, r in rx.items():
        m = r.search(l)
        if m:
            ph += 1
            print(f"page:{i} [{k}] {m.group(0)!r} {'(unchanged since base)' if l in old else '(NEW)'}")
print(f"page: {ph} hits")
print("RESULT", "CLEAN" if hits == 0 else "REVIEW")
