#!/usr/bin/env python3
"""Verify the issue 117 evidence archive against its MANIFEST.json.

usage: verify_archive.py <archive-dir> [<pre-redaction-archive-dir>]

<archive-dir> is review-evidence/117-r1 extracted from the pinned commit.
The optional second directory is the same subtree from the pre-redaction
commit; when given, each MANIFEST.json original_sha256 is checked against
the pre-redaction bytes and every capture is checked for equal length.
Prints only hashes, sizes, counts and file names; never file contents.
Exit 0 when every check holds, 1 otherwise.
"""
import hashlib
import json
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    root = Path(sys.argv[1])
    orig_root = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    bad = 0
    man = json.loads((root / "MANIFEST.json").read_text())
    files = sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())
    listed = {e["file"]: e for e in man}
    print(f"files on disk: {len(files)}; MANIFEST.json entries: {len(man)}")
    unlisted = [f for f in files if f not in listed and f != "MANIFEST.json"]
    missing = [f for f in listed if not (root / f).is_file()]
    print(f"on disk but not in MANIFEST.json (excluding itself): {unlisted}")
    print(f"in MANIFEST.json but missing on disk: {missing}")
    bad += len(unlisted) + len(missing)
    changed = 0
    ident = 0
    pathred = 0
    for f, e in sorted(listed.items()):
        got = sha(root / f)
        if got != e["published_sha256"]:
            print(f"PUBLISHED-HASH-MISMATCH {f} manifest={e['published_sha256']} disk={got}")
            bad += 1
        if e["original_sha256"] != e["published_sha256"]:
            changed += 1
        if e.get("identity_redacted"):
            ident += 1
        if e.get("path_redacted"):
            pathred += 1
    print(f"entries whose published copy differs from the original: {changed}")
    print(f"entries flagged identity_redacted: {ident}; path_redacted: {pathred}")
    flagged_same = [f for f, e in listed.items()
                    if (e.get("identity_redacted") or e.get("path_redacted"))
                    and e["original_sha256"] == e["published_sha256"]]
    unflagged_diff = [f for f, e in listed.items()
                      if not (e.get("identity_redacted") or e.get("path_redacted"))
                      and e["original_sha256"] != e["published_sha256"]]
    print(f"flagged redacted but bytes unchanged: {flagged_same}")
    print(f"bytes changed but not flagged: {unflagged_diff}")
    bad += len(unflagged_diff)
    # Packet manifests list original hashes; each must equal MANIFEST.json's original.
    for pkt in ("bench-a200", "bench-a202"):
        mf = root / pkt / "MANIFEST.sha256"
        n = ok = pub_only = 0
        for line in mf.read_text().splitlines():
            if not line.strip():
                continue
            h, name = line.split(None, 1)
            name = name.lstrip("*").strip()
            if name.startswith("./"):
                name = name[2:]
            rel = f"{pkt}/{name}"
            n += 1
            e = listed.get(rel)
            if e is None:
                print(f"PACKET-ENTRY-NOT-IN-ARCHIVE {rel}")
                bad += 1
                continue
            if h == e["original_sha256"]:
                ok += 1
                if h != e["published_sha256"]:
                    pub_only += 1
            else:
                print(f"PACKET-HASH-NOT-ORIGINAL {rel} packet={h} original={e['original_sha256']}")
                bad += 1
        in_pkt = [f for f in files if f.startswith(pkt + "/") and f != f"{pkt}/MANIFEST.sha256"]
        listed_names = set()
        for l in mf.read_text().splitlines():
            if l.strip():
                nm = l.split(None, 1)[1].lstrip("*").strip()
                listed_names.add(f"{pkt}/" + (nm[2:] if nm.startswith("./") else nm))
        not_in_pkt_manifest = [f for f in in_pkt if f not in listed_names]
        print(f"{pkt}/MANIFEST.sha256: {n} entries, {ok} equal MANIFEST.json original, "
              f"{pub_only} of those published redacted; files in packet not in its manifest: "
              f"{not_in_pkt_manifest}")
    if orig_root is not None:
        old_man = {e["file"]: e for e in json.loads((orig_root / "MANIFEST.json").read_text())}
        pre_redacted = 0
        o_bad = 0
        caps_same = caps_total = 0
        lens = {"same": 0, "changed": 0}
        for f, e in sorted(listed.items()):
            op = orig_root / f
            if not op.is_file():
                print(f"PRE-REDACTION-MISSING {f}")
                o_bad += 1
                continue
            oh = sha(op)
            if oh != e["original_sha256"]:
                old = old_man.get(f, {})
                if (old.get("published_sha256") == oh
                        and old.get("original_sha256") == e["original_sha256"]):
                    # The pre-redaction commit already published this file
                    # path-redacted; its as-run bytes were never public.
                    pre_redacted += 1
                else:
                    print(f"ORIGINAL-HASH-MISMATCH {f} manifest={e['original_sha256']} pre={oh}")
                    o_bad += 1
            if e["original_sha256"] != e["published_sha256"]:
                same = op.stat().st_size == (root / f).stat().st_size
                lens["same" if same else "changed"] += 1
                if f.endswith(".pcap"):
                    caps_total += 1
                    caps_same += same
                    if not same:
                        print(f"CAPTURE-LENGTH-CHANGED {f} {op.stat().st_size} -> {(root / f).stat().st_size}")
        print(f"files already path-redacted at the pre-redaction commit "
              f"(same original recorded by both manifests): {pre_redacted}")
        print(f"pre-redaction original hashes mismatching MANIFEST.json: {o_bad}")
        print(f"redacted files with unchanged length: {lens['same']}; changed length: {lens['changed']}")
        print(f"redacted captures with unchanged length: {caps_same} of {caps_total}")
        bad += o_bad + (caps_total - caps_same)
    print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
