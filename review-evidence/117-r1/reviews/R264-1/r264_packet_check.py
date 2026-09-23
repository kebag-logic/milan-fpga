#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer integrity check of the published issue 117 evidence archive.

  r264_packet_check.py <evidence_root> <findings_page>

<evidence_root> is review-evidence/117-r1 extracted from the archive commit.
Checks, printing one line per result:
  1. every MANIFEST.json entry's published_sha256 equals the file on disk;
  2. entries whose original and published hashes differ are exactly the
     entries marked path_redacted;
  3. no file on disk is missing from MANIFEST.json;
  4. every line of each packet MANIFEST.sha256 equals the MANIFEST.json
     original hash of the same file;
  5. every full SHA-256 and every 8-hex abbreviated hash the findings page
     quotes, mapped to the archive file(s) carrying it (or NOT IN ARCHIVE).
"""
import hashlib
import json
import os
import re
import sys


def main(root, page):
    os.chdir(root)
    m = json.load(open("MANIFEST.json"))
    print(f"MANIFEST.json entries: {len(m)}")
    bad = [e["file"] for e in m if hashlib.sha256(open(e["file"], "rb").read()).hexdigest() != e["published_sha256"]]
    print(f"1. published hash mismatches: {len(bad)} {bad}")
    diff = sorted(e["file"] for e in m if e["original_sha256"] != e["published_sha256"])
    red = sorted(e["file"] for e in m if e["path_redacted"])
    print(f"2. original!=published: {len(diff)}; path_redacted: {len(red)}; sets equal: {diff == red}")
    listed = {e["file"] for e in m}
    unlisted = []
    for top, _, files in os.walk("."):
        for f in files:
            p = os.path.relpath(os.path.join(top, f))
            if p != "MANIFEST.json" and p not in listed:
                unlisted.append(p)
    print(f"3. files on disk not in MANIFEST.json: {len(unlisted)} {unlisted}")
    orig = {e["file"]: e["original_sha256"] for e in m}
    for pk in ("bench-a200", "bench-a202"):
        n = mism = 0
        for line in open(os.path.join(pk, "MANIFEST.sha256")):
            h, p = line.split(None, 1)
            p = os.path.normpath(os.path.join(pk, p.strip().lstrip("*")))
            n += 1
            if orig.get(p) != h:
                mism += 1
                print(f"   packet manifest mismatch {p}")
        print(f"4. {pk}/MANIFEST.sha256: {n} lines, {mism} mismatches against MANIFEST.json originals")
    by = {}
    for e in m:
        by.setdefault(e["original_sha256"], []).append(e["file"])
        by.setdefault(e["published_sha256"], []).append(e["file"])
    text = open(page).read()
    full = re.findall(r"`([0-9a-f]{64})`", text)
    short = re.findall(r"`([0-9a-f]{8})\.\.\.`", text)
    print(f"5. page quotes {len(full)} full and {len(short)} abbreviated hashes")
    for h in full:
        print(f"   full  {h[:16]} -> {sorted(set(by.get(h, ['NOT IN ARCHIVE'])))}")
    for s in short:
        hits = sorted({f for h, fs in by.items() if h.startswith(s) for f in fs})
        print(f"   short {s} -> {hits if hits else ['NOT IN ARCHIVE']}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(main(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])))
