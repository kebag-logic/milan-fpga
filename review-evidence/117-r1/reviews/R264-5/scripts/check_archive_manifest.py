#!/usr/bin/env python3
"""Check a pinned 117-r1 evidence tree against its MANIFEST.json and packet manifests.

Usage: check_archive_manifest.py <tree-root containing MANIFEST.json> <page.md>

Reports:
  - every published file hashes to MANIFEST.json published_sha256, and the
    MANIFEST.json file list equals the tree's file list (MANIFEST.json excluded);
  - redaction counts (total, per packet, path-only vs identity);
  - each packet MANIFEST.sha256 line: OK / FAILED, and whether every FAILED
    line is exactly a redacted file whose original hash the line records;
  - every 64-hex hash on the page: where it resolves (original / published /
    packet manifest / none), and the redacted-only count among the page's
    Raw artifacts tables;
  - every abbreviated `xxxxxxxx...` hash prefix on the page and its resolution.
Exit 0 only when every structural check holds; the census itself is printed.
"""
import hashlib
import json
import os
import re
import sys


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    root, page = sys.argv[1], sys.argv[2]
    ok = True
    manifest = json.load(open(os.path.join(root, "MANIFEST.json")))
    by_file = {e["file"]: e for e in manifest}
    tree = []
    for d, _, fs in os.walk(root):
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), root)
            if rel != "MANIFEST.json":
                tree.append(rel)
    tree_set = set(tree)
    print(f"tree files (excl MANIFEST.json): {len(tree_set)}; MANIFEST.json entries: {len(by_file)}")
    if tree_set != set(by_file):
        ok = False
        print("MISMATCH tree-only:", sorted(tree_set - set(by_file)))
        print("MISMATCH manifest-only:", sorted(set(by_file) - tree_set))
    bad_pub = [f for f in sorted(tree_set & set(by_file)) if sha256(os.path.join(root, f)) != by_file[f]["published_sha256"]]
    print(f"published_sha256 mismatches: {len(bad_pub)} {bad_pub[:5]}")
    ok &= not bad_pub

    red = [e for e in manifest if e["original_sha256"] != e["published_sha256"]]
    ident = [e for e in red if e.get("identity_redacted")]
    path_only = [e for e in red if not e.get("identity_redacted")]
    print(f"redacted total {len(red)}; identity-masked {len(ident)}; path-only {len(path_only)}")
    for pk in ("bench-a200", "bench-a202"):
        print(f"  {pk}: redacted {sum(e['file'].startswith(pk + '/') for e in red)}")
    print("  path-only files:", [e["file"] for e in path_only])
    flag_mismatch = [e["file"] for e in manifest if e.get("path_redacted") != (e["original_sha256"] != e["published_sha256"]) ]
    print(f"  entries whose path_redacted flag differs from 'changed': {len(flag_mismatch)}")

    orig = {e["original_sha256"]: e for e in manifest}
    pub = {e["published_sha256"]: e for e in manifest}
    pkt_hashes = {}
    for pk in ("bench-a200", "bench-a202"):
        mpath = os.path.join(root, pk, "MANIFEST.sha256")
        failed, okc, missing = [], 0, []
        for line in open(mpath):
            line = line.rstrip("\n")
            if not line:
                continue
            h, name = line.split(None, 1)
            name = name.lstrip("*")
            rel = os.path.normpath(os.path.join(pk, name))
            pkt_hashes.setdefault(h, []).append(rel)
            p = os.path.join(root, rel)
            if not os.path.exists(p):
                missing.append(rel)
                continue
            if sha256(p) == h:
                okc += 1
            else:
                failed.append(rel)
        unexplained = [f for f in failed if not (f in by_file and by_file[f]["original_sha256"] in pkt_hashes and by_file[f]["original_sha256"] != by_file[f]["published_sha256"])]
        red_here = {e["file"] for e in red if e["file"].startswith(pk + "/")}
        print(f"{pk}/MANIFEST.sha256: OK {okc} FAILED {len(failed)} missing {len(missing)}; FAILED==redacted set: {set(failed) == red_here}; unexplained {unexplained}")
        unlisted = sorted(f for f in tree_set if f.startswith(pk + "/") and f not in {r for v in pkt_hashes.values() for r in v} and not f.endswith("MANIFEST.sha256"))
        print(f"  files in {pk} not listed in its MANIFEST.sha256: {unlisted}")
        ok &= set(failed) == red_here and not missing

    text = open(page, encoding="utf-8").read()
    full = re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", text)
    print(f"page 64-hex hashes: {len(full)} occurrences, {len(set(full))} distinct")
    # the two Raw artifacts tables
    ra = text[text.index("## Raw artifacts"):]
    ra_hashes = re.findall(r"`([0-9a-f]{64})`", ra)
    unresolved, red_only = [], []
    for h in ra_hashes:
        where = []
        if h in orig:
            where.append("original:" + orig[h]["file"])
            if orig[h]["original_sha256"] != orig[h]["published_sha256"]:
                red_only.append(orig[h]["file"])
        if h in pkt_hashes:
            where.append("pkt")
        if not where:
            unresolved.append(h)
    print(f"Raw artifacts table hashes: {len(ra_hashes)} ({len(set(ra_hashes))} distinct); unresolved {unresolved}; redacted-only (distinct files) {len(set(red_only))}")
    for f in sorted(set(red_only)):
        print("   redacted-only:", f)
    ok &= not unresolved
    other = sorted(set(full) - set(ra_hashes))
    for h in other:
        where = []
        if h in orig: where.append("original:" + orig[h]["file"])
        if h in pub: where.append("published:" + pub[h]["file"])
        if h in pkt_hashes: where.append("pkt:" + ",".join(pkt_hashes[h]))
        print(f"other page hash {h[:12]}: {where or 'not in archive'}")
    prefixes = sorted(set(re.findall(r"`([0-9a-f]{8})\.\.\.`", text)) | set(re.findall(r"\(`([0-9a-f]{8})\.\.\.`\)", text)))
    for p in prefixes:
        hits = sorted({e["file"] + (" [redacted]" if e["original_sha256"] != e["published_sha256"] else "") for e in manifest if e["original_sha256"].startswith(p)})
        phits = sorted({r for h, v in pkt_hashes.items() if h.startswith(p) for r in v})
        print(f"prefix {p}: MANIFEST.json original -> {hits or '-'}; packet manifests -> {phits or '-'}")
    print("STRUCTURAL", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
