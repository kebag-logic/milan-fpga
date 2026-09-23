#!/usr/bin/env python3
"""Resolve every SHA-256 on the issue 117 findings page against the archive.

usage: page_hashes.py <page.md> <archive-dir>

Full 64-hex values and 8-hex-prefix abbreviations ("abcd1234...") are both
resolved against MANIFEST.json (original and published hashes). For each
value it prints the page line, the archive file(s) it names, and whether
that file is published redacted. It then checks the Raw artifacts tables:
every row must name an archive file in the packet its heading gives, and
the count of rows naming redacted files is printed for comparison with the
page's own claim. Prints hashes and file names only.
"""
import json
import re
import sys
from pathlib import Path

FULL = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
ABBR = re.compile(r"`?([0-9a-f]{8})\.\.\.`?")


def main() -> int:
    page = Path(sys.argv[1]).read_text().splitlines()
    root = Path(sys.argv[2])
    man = json.loads((root / "MANIFEST.json").read_text())
    by_orig, by_pub = {}, {}
    for e in man:
        by_orig.setdefault(e["original_sha256"], []).append(e)
        by_pub.setdefault(e["published_sha256"], []).append(e)
    allh = set(by_orig) | set(by_pub)
    bad = 0
    print("== full SHA-256 values on the page")
    for i, line in enumerate(page, 1):
        for h in FULL.findall(line):
            o = by_orig.get(h, [])
            p = by_pub.get(h, [])
            if o:
                files = ", ".join(f"{e['file']}{' [REDACTED-COPY]' if e['original_sha256'] != e['published_sha256'] else ''}" for e in o)
                print(f"L{i} {h[:12]} ORIGINAL -> {files}")
            elif p:
                files = ", ".join(e["file"] for e in p)
                print(f"L{i} {h[:12]} PUBLISHED-ONLY -> {files}")
            else:
                print(f"L{i} {h[:12]} NOT-IN-ARCHIVE")
    print("== 8-hex abbreviations on the page")
    for i, line in enumerate(page, 1):
        for a in ABBR.findall(line):
            o = sorted({e["file"] for h, es in by_orig.items() if h.startswith(a) for e in es})
            p = sorted({e["file"] for h, es in by_pub.items() if h.startswith(a) and h not in by_orig for e in es})
            full = [h for h in FULL.findall("\n".join(page)) if h.startswith(a)]
            tag = "ORIGINAL" if o else ("PUBLISHED-ONLY" if p else ("FULL-ON-PAGE" if full else "NOT-IN-ARCHIVE"))
            print(f"L{i} {a} {tag} -> {', '.join(o or p)}")
    print("== Raw artifacts tables")
    sect = None
    rows = redacted = 0
    for i, line in enumerate(page, 1):
        if line.startswith("## "):
            sect = line
        if sect != "## Raw artifacts":
            continue
        if "A200 packet" in line:
            pkt = "bench-a200/"
        elif "A202 packet" in line and "(`117-a202" in line:
            pkt = "bench-a202/"
        m = re.match(r"\| (.+?) \| `([0-9a-f]{64})` \|", line)
        if not m:
            continue
        rows += 1
        label, h = m.groups()
        es = by_orig.get(h, [])
        if not es:
            print(f"L{i} ROW-NOT-RESOLVED {label}")
            bad += 1
            continue
        inpkt = [e for e in es if e["file"].startswith(pkt)]
        if not inpkt:
            print(f"L{i} ROW-IN-OTHER-PACKET {label} -> {[e['file'] for e in es]}")
            bad += 1
        red = any(e["original_sha256"] != e["published_sha256"] for e in es)
        redacted += red
        print(f"L{i} {'R' if red else '-'} {label} -> {', '.join(e['file'] for e in es)}")
    print(f"rows: {rows}; rows naming a file published only redacted: {redacted}")
    print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
