#!/usr/bin/env python3
"""Resolve every SHA-256 quoted by the #117 findings page against the pinned
evidence archive's MANIFEST.json, and check the page's archive count claims.

usage: verify_manifest.py <archive-root review-evidence/117-r1> <page.md>
Exit 0 when every check holds, 1 otherwise. Prints one line per check.
"""
import hashlib
import json
import os
import re
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    root, page = sys.argv[1], sys.argv[2]
    bad = 0
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    files = set()
    for dp, _, fns in os.walk(root):
        for fn in fns:
            files.add(os.path.relpath(os.path.join(dp, fn), root))
    files.discard("MANIFEST.json")
    listed = {e["file"] for e in man}
    print(f"tree files (excl MANIFEST.json): {len(files)}; manifest entries: {len(man)}")
    if files != listed:
        bad += 1
        print("FAIL tree/manifest mismatch:", sorted(files ^ listed)[:20])
    else:
        print("PASS tree == manifest file set")
    pub_ok = 0
    for e in man:
        p = os.path.join(root, e["file"])
        if os.path.isfile(p) and sha(p) == e["published_sha256"]:
            pub_ok += 1
        else:
            bad += 1
            print("FAIL published hash", e["file"])
    print(f"published_sha256 matches bytes: {pub_ok}/{len(man)}")
    red = [e for e in man if e["original_sha256"] != e["published_sha256"]]
    path_only = [e for e in red if e.get("path_redacted") and not e.get("identity_redacted", True)]
    print(f"redacted (original != published): {len(red)}")
    keys = sorted({k for e in man for k in e})
    print("manifest keys:", keys)
    for k in keys:
        if k in ("file", "original_sha256", "published_sha256"):
            continue
        vals = {}
        for e in red:
            vals[str(e.get(k))] = vals.get(str(e.get(k)), 0) + 1
        print(f"  redacted entries by {k}: {vals}")
    for pk in ("bench-a200", "bench-a202"):
        n = sum(1 for e in red if e["file"].startswith(pk + "/"))
        print(f"  redacted in {pk}: {n}")
    # per-packet MANIFEST.sha256 behaviour
    for pk in ("bench-a200", "bench-a202"):
        ms = os.path.join(root, pk, "MANIFEST.sha256")
        fail = ok = missing = 0
        for line in open(ms, encoding="utf-8", errors="replace"):
            m = re.match(r"^([0-9a-f]{64}) [ *](.+)$", line.rstrip("\n"))
            if not m:
                continue
            p = os.path.join(root, pk, m.group(2))
            if not os.path.isfile(p):
                missing += 1
            elif sha(p) == m.group(1):
                ok += 1
            else:
                fail += 1
        print(f"  {pk}/MANIFEST.sha256: OK {ok} FAILED {fail} missing {missing}")
    orig = {}
    for e in man:
        orig.setdefault(e["original_sha256"], []).append(e)
    text = open(page, encoding="utf-8").read()
    # Raw-artifacts section full hashes
    ra = text.split("## Raw artifacts", 1)[1]
    full = re.findall(r"`([0-9a-f]{64})`", ra)
    print(f"raw-artifact table hashes: {len(full)} (unique {len(set(full))})")
    red_named = set()
    for h in full:
        if h not in orig:
            bad += 1
            print("FAIL page hash not an original in MANIFEST.json:", h)
            continue
        for e in orig[h]:
            if e["original_sha256"] != e["published_sha256"]:
                red_named.add(e["file"])
    unique_red = {h for h in set(full) if any(e["original_sha256"] != e["published_sha256"] for e in orig.get(h, []))}
    print(f"raw-artifact unique hashes naming redacted files: {len(unique_red)} (files {len(red_named)})")
    for f in sorted(red_named):
        print("   redacted-named:", f)
    # every other full hash on the page, reported with its resolution
    allfull = sorted(set(re.findall(r"(?<![0-9a-f])([0-9a-f]{64})(?![0-9a-f])", text)))
    print(f"all 64-hex tokens on page: {len(allfull)}")
    for h in allfull:
        if h in orig:
            where = ",".join(e["file"] for e in orig[h])
        else:
            pub = [e["file"] for e in man if e["published_sha256"] == h]
            where = "published-only:" + ",".join(pub) if pub else "NOT IN ARCHIVE"
        print(f"   {h[:12]} -> {where}")
    # abbreviated tool hashes `xxxxxxxx...`
    short = sorted(set(re.findall(r"`([0-9a-f]{8})\.\.\.`", text)))
    print(f"abbreviated 8-hex tokens: {len(short)}")
    for s in short:
        o = sorted({e["file"] for e in man if e["original_sha256"].startswith(s)})
        p = sorted({e["file"] for e in man if e["published_sha256"].startswith(s) and not e["original_sha256"].startswith(s)})
        print(f"   {s}: original-in {o[:4]}{' +' if len(o) > 4 else ''} published-only {p[:3]}")
    print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
