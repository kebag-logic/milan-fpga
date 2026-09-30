#!/usr/bin/env python3
"""Check the published B3 evidence against the findings pages at the head.

usage: evidence_integrity.py <repo> <head> <evidence-root>

<evidence-root> is an extraction of review-evidence/b3-r1 from branch
b3-review-evidence. Checks:
1. every tool hash in the two pages' tool tables equals the file under author/tools;
2. the round-2 packet manifest (author-r2/packet/MANIFEST.sha256) against the
   round-1 manifest: which entries changed or were added, and that each file the
   round-2 packet actually carries matches its manifest line;
3. the evidence-root MANIFEST.json published hash of every author-r2 file.
"""
import hashlib
import json
import os
import re
import subprocess
import sys


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def manifest(p):
    out = {}
    for line in open(p):
        h, f = line.split(None, 1)
        out[f.strip()] = h
    return out


def main():
    repo, head, root = sys.argv[1:4]
    bad = 0
    print("1. page tool hashes against author/tools")
    for page in ("docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md", "docs/findings/451_USB_AUDIO_CAPTURE.md"):
        text = subprocess.run(["git", "-C", repo, "show", f"{head}:{page}"], capture_output=True, text=True,
                              check=True).stdout
        for tool, h in re.findall(r"^\| `([\w.]+\.py)`[^|]*\| `([0-9a-f]{64})` \|$", text, re.M):
            got = sha(os.path.join(root, "author/tools", tool))
            ok = got == h
            bad += not ok
            print(f"  {'OK' if ok else 'MISMATCH'} {page.split('/')[-1]} {tool} {h[:12]}")
    print("2. round-2 packet manifest against round 1")
    m1 = manifest(os.path.join(root, "author/MANIFEST.sha256"))
    m2 = manifest(os.path.join(root, "author-r2/packet/MANIFEST.sha256"))
    print(f"  entries: round 1 {len(m1)}, round 2 {len(m2)}")
    for f in sorted(set(m1) | set(m2)):
        if f not in m2:
            print(f"  REMOVED {f}")
        elif f not in m1:
            print(f"  ADDED {f}")
        elif m1[f] != m2[f]:
            print(f"  REHASHED {f}")
    for f, h in sorted(m2.items()):
        p = os.path.join(root, "author-r2/packet", f)
        if os.path.exists(p):
            ok = sha(p) == h
            bad += not ok
            print(f"  {'OK' if ok else 'MISMATCH'} carried file {f}")
    print("3. MANIFEST.json published hashes of author-r2 files")
    for e in json.load(open(os.path.join(root, "MANIFEST.json"))):
        if e["file"].startswith("author-r2/"):
            ok = sha(os.path.join(root, e["file"])) == e["published_sha256"]
            bad += not ok
            print(f"  {'OK' if ok else 'MISMATCH'} {e['file']}")
    print(f"{bad} mismatch(es)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
