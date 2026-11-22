#!/usr/bin/env python3
"""Verify a published review-evidence packet against its own MANIFEST.json and receipt INDEX.md files.

usage: python3 -I verify_packet.py BARE_GIT COMMIT PREFIX
Reads blobs with `git cat-file` only; executes nothing from the packet.
For every MANIFEST.json entry: the published blob's sha256 equals published_sha256, and every blob under
PREFIX is listed. For each */receipts/INDEX.md and f5/round1-INDEX-corrected.md: every 64-hex sha256 row
naming a path is compared with that path's blob (rows whose path cannot be resolved are reported).
"""
import hashlib
import json
import re
import subprocess
import sys


def blob(git, commit, path):
    r = subprocess.run(["git", "-C", git, "cat-file", "blob", f"{commit}:{path}"], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    git, commit, prefix = sys.argv[1:4]
    names = subprocess.run(["git", "-C", git, "ls-tree", "-r", "--name-only", commit, prefix],
                           capture_output=True, text=True, check=True).stdout.split()
    rel = [n[len(prefix) + 1:] for n in names]
    manifest = json.loads(blob(git, commit, f"{prefix}/MANIFEST.json"))
    bad, listed = 0, set()
    for e in manifest:
        listed.add(e["file"])
        b = blob(git, commit, f"{prefix}/{e['file']}")
        if b is None or hashlib.sha256(b).hexdigest() != e["published_sha256"]:
            bad += 1
            print("MANIFEST MISMATCH", e["file"])
    unlisted = [r for r in rel if r not in listed and r != "MANIFEST.json"]
    print(f"manifest: {len(manifest)} entries, {bad} mismatches, {len(unlisted)} unlisted blobs")
    for u in unlisted:
        print("  unlisted:", u)
    redacted = [e["file"] for e in manifest if e.get("path_redacted")]
    print(f"manifest: {len(redacted)} entries publication-normalized (original != published)")
    for idx in [r for r in rel if r.endswith("receipts/INDEX.md") or r.endswith("round1-INDEX-corrected.md")]:
        text = blob(git, commit, f"{prefix}/{idx}").decode()
        base = idx.split("/receipts/")[0] + "/receipts/" if "/receipts/" in idx else ""
        if idx.endswith("round1-INDEX-corrected.md"):
            base = "author-r1/receipts/"
        ok = miss = unres = 0
        for line in text.splitlines():
            h = re.search(r"\b([0-9a-f]{64})\b", line)
            p = re.search(r"`([^`]+\.[A-Za-z0-9]+)`", line) or re.search(r"\|\s*([^|`\s]+/[^|\s]+)\s*\|", line)
            if not h or not p:
                continue
            cand = [base + p.group(1), p.group(1), f"{idx.split('/')[0]}/{p.group(1)}"]
            got = None
            for c in cand:
                got = blob(git, commit, f"{prefix}/{c}")
                if got is not None:
                    break
            if got is None:
                unres += 1
                print(f"  {idx}: unresolved row path {p.group(1)}")
                continue
            if hashlib.sha256(got).hexdigest() == h.group(1):
                ok += 1
            else:
                miss += 1
                print(f"  {idx}: HASH MISMATCH {p.group(1)}")
        print(f"index {idx}: {ok} match, {miss} mismatch, {unres} unresolved")


if __name__ == "__main__":
    main()
