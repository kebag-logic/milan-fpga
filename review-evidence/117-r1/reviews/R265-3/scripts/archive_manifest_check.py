#!/usr/bin/env python3
"""Check the pinned evidence archive against its manifests and the page.

Usage: archive_manifest_check.py <evidence-root: .../review-evidence/117-r1> <page.md>

Prints counts and hash resolution only; never prints file content.
"""
import hashlib
import json
import os
import re
import sys


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    root, page = sys.argv[1], sys.argv[2]
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    files = {}
    for dp, _, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            files[os.path.relpath(p, root)] = sha(p)
    by_file = {e["file"]: e for e in man}
    print("files on disk (excluding MANIFEST.json):", len(files) - 1)
    print("MANIFEST.json entries:", len(man))
    missing = sorted(set(files) - set(by_file) - {"MANIFEST.json"})
    extra = sorted(set(by_file) - set(files))
    print("on disk but not in MANIFEST.json:", missing)
    print("in MANIFEST.json but not on disk:", extra)
    bad = [f for f, e in by_file.items() if f in files and files[f] != e["published_sha256"]]
    print("published_sha256 mismatches:", bad)

    red = [e for e in man if e["original_sha256"] != e["published_sha256"]]
    print("redacted (original != published):", len(red))
    for pk in ("bench-a200", "bench-a202"):
        r = [e for e in red if e["file"].startswith(pk + "/")]
        ident = [e for e in r if e.get("identity_redacted")]
        pathonly = [e for e in r if e.get("path_redacted") and not e.get("identity_redacted")]
        other = [e for e in r if not e.get("path_redacted") and not e.get("identity_redacted")]
        print(f"  {pk}: redacted {len(r)}, identity {len(ident)}, path-only {len(pathonly)}, unflagged {len(other)}")
    flagged_same = [e["file"] for e in man if (e.get("path_redacted") or e.get("identity_redacted"))
                    and e["original_sha256"] == e["published_sha256"]]
    print("flagged redacted but bytes unchanged:", flagged_same)
    ident_all = [e for e in red if e.get("identity_redacted")]
    path_only_all = [e for e in red if not e.get("identity_redacted")]
    print("total identity-redacted:", len(ident_all), "path-only:", len(path_only_all))
    print("path-only files:", sorted(e["file"] for e in path_only_all))

    # per-packet MANIFEST.sha256 behaviour
    for pk in ("bench-a200", "bench-a202"):
        ms = os.path.join(root, pk, "MANIFEST.sha256")
        ok = fail = absent = 0
        listed = set()
        for line in open(ms):
            line = line.rstrip("\n")
            if not line.strip():
                continue
            h, name = line.split(None, 1)
            name = name.lstrip("*")
            rel = os.path.normpath(os.path.join(pk, name))
            listed.add(rel)
            if rel not in files:
                absent += 1
            elif files[rel] == h:
                ok += 1
            else:
                fail += 1
        unlisted = sorted(f for f in files if f.startswith(pk + "/") and f not in listed
                          and not f.endswith("MANIFEST.sha256"))
        print(f"{pk}/MANIFEST.sha256: OK {ok}, FAILED {fail}, missing-file {absent}, files not listed {len(unlisted)}")
        if unlisted:
            print("   not listed:", unlisted)

    # page hash resolution
    text = open(page, encoding="utf-8").read()
    orig = {}
    pub = {}
    for e in man:
        orig.setdefault(e["original_sha256"], []).append(e)
        pub.setdefault(e["published_sha256"], []).append(e)
    sums = {}
    for pk in ("bench-a200", "bench-a202"):
        for line in open(os.path.join(root, pk, "MANIFEST.sha256")):
            if line.strip():
                h, name = line.split(None, 1)
                sums.setdefault(h, []).append(os.path.normpath(os.path.join(pk, name.strip().lstrip("*"))))
    full = re.findall(r"`([0-9a-f]{64})`", text)
    print("page full SHA-256 values (backticked):", len(full), "distinct", len(set(full)))
    unresolved = []
    redacted_named = set()
    for h in dict.fromkeys(full):
        if h in orig:
            es = orig[h]
            if any(e["original_sha256"] != e["published_sha256"] for e in es):
                redacted_named.add(h)
        elif h in pub or h in sums:
            pass
        else:
            unresolved.append(h)
    print("page full hashes not in MANIFEST.json or MANIFEST.sha256:", len(unresolved))
    for h in unresolved:
        i = text.index(h)
        ln = text.count("\n", 0, i) + 1
        print(f"   line {ln}: {h[:8]}...")
    # hashes inside the Raw artifacts tables only
    raw = text[text.index("## Raw artifacts"):]
    raw_full = list(dict.fromkeys(re.findall(r"`([0-9a-f]{64})`", raw)))
    raw_red = [h for h in raw_full if h in redacted_named]
    print("Raw artifacts table distinct hashes:", len(raw_full), "naming redacted files:", len(raw_red))
    print("  redacted-named files:", sorted(e["file"] for h in raw_red for e in orig[h]))
    raw_unres = [h for h in raw_full if h not in orig and h not in pub and h not in sums]
    print("  Raw artifacts hashes unresolved:", raw_unres)

    # truncated hashes `abcdef12...`
    trunc = re.findall(r"`([0-9a-f]{8})\.\.\.`", text)
    allh = set(orig) | set(pub) | set(sums)
    print("page truncated hashes:", len(set(trunc)))
    for t in dict.fromkeys(trunc):
        hits = sorted(h for h in allh if h.startswith(t))
        where = []
        for h in hits:
            for e in orig.get(h, []):
                where.append(("orig", e["file"], e["original_sha256"] != e["published_sha256"]))
            for e in pub.get(h, []):
                if e["original_sha256"] != e["published_sha256"]:
                    where.append(("pub", e["file"], True))
            for f in sums.get(h, []):
                where.append(("sums", f, None))
        i = text.index(t + "...")
        ln = text.count("\n", 0, i) + 1
        uniq = sorted(set((w[0], w[1], w[2]) for w in where))
        print(f"   line {ln}: {t}... -> {len(hits)} full hash(es); {uniq if uniq else 'UNRESOLVED in archive'}")


if __name__ == "__main__":
    main()
