#!/usr/bin/env python3
"""Verify the issue 117 evidence archive against its manifests and the page.

Usage: verify_manifest.py <archive-root> <findings-page>

<archive-root> is the extracted `review-evidence/117-r1` directory of the
pinned evidence commit. <findings-page> is the PR's
docs/findings/117_GPTP_SILICON_EVIDENCE.md. Prints a receipt; exits 1 on any
mismatch.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(sys.argv[1])
    page = Path(sys.argv[2]).read_text(encoding="utf-8")
    bad = 0
    manifest = json.loads((root / "MANIFEST.json").read_text())
    by_file = {e["file"]: e for e in manifest}
    tree = sorted(
        str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()
    )
    tree_set = set(tree) - {"MANIFEST.json"}
    print(f"tree files (excluding MANIFEST.json): {len(tree_set)}")
    print(f"MANIFEST.json entries: {len(manifest)}")
    missing = sorted(tree_set - set(by_file))
    extra = sorted(set(by_file) - tree_set)
    print(f"tree files missing from MANIFEST.json: {len(missing)} {missing}")
    print(f"MANIFEST.json entries missing from tree: {len(extra)} {extra}")
    bad += bool(missing) + bool(extra)

    published_mismatch = []
    for e in manifest:
        p = root / e["file"]
        if p.is_file() and sha256(p) != e["published_sha256"]:
            published_mismatch.append(e["file"])
    print(f"published_sha256 mismatches vs bytes: {len(published_mismatch)}")
    bad += bool(published_mismatch)

    redacted = [e for e in manifest if e["original_sha256"] != e["published_sha256"]]
    ident = [e for e in manifest if e.get("identity_redacted")]
    path_only = [e for e in redacted if not e.get("identity_redacted")]
    flagged_not_changed = [
        e["file"] for e in manifest
        if (e.get("identity_redacted") or e.get("path_redacted"))
        and e["original_sha256"] == e["published_sha256"]
    ]
    changed_not_flagged = [
        e["file"] for e in redacted
        if not (e.get("identity_redacted") or e.get("path_redacted"))
    ]
    print(f"redacted (original != published): {len(redacted)}")
    print(f"identity_redacted: {len(ident)}; path-only: {len(path_only)}")
    print(f"flagged but unchanged: {flagged_not_changed}")
    print(f"changed but unflagged: {changed_not_flagged}")
    bad += bool(flagged_not_changed) + bool(changed_not_flagged)

    # Per-packet MANIFEST.sha256 against MANIFEST.json originals and bytes.
    for pkt in ("bench-a200", "bench-a202"):
        lines = (root / pkt / "MANIFEST.sha256").read_text().splitlines()
        fails = []
        disagree = []
        for ln in lines:
            h, name = ln.split(None, 1)
            name = name.lstrip("*")
            rel = f"{pkt}/{name[2:] if name.startswith('./') else name}"
            p = root / rel
            if not p.is_file():
                fails.append((rel, "absent"))
                continue
            if sha256(p) != h:
                fails.append((rel, "FAILED"))
            e = by_file.get(rel)
            if e is None or e["original_sha256"] != h:
                disagree.append(rel)
        red_in_pkt = {e["file"] for e in redacted if e["file"].startswith(pkt + "/")}
        fail_set = {f for f, _ in fails}
        print(
            f"{pkt}: MANIFEST.sha256 lines {len(lines)}; sha256sum -c FAILED {len(fails)};"
            f" redacted in packet {len(red_in_pkt)}; FAILED == redacted set: {fail_set == red_in_pkt};"
            f" lines disagreeing with MANIFEST.json original: {len(disagree)}"
        )
        bad += (fail_set != red_in_pkt) + bool(disagree)

    # Every full 64-hex hash on the page.
    originals = {}
    for e in manifest:
        originals.setdefault(e["original_sha256"], []).append(e["file"])
    publisheds = {e["published_sha256"]: e["file"] for e in manifest}
    full = re.findall(r"`([0-9a-f]{64})`", page)
    raw_start = page.index("## Raw artifacts")
    table_hashes = re.findall(r"\| `([0-9a-f]{64})` \|", page[raw_start:])
    print(f"full 64-hex hashes on page: {len(full)} ({len(set(full))} distinct)")
    print(f"raw-artifact table rows: {len(table_hashes)} ({len(set(table_hashes))} distinct)")
    unresolved = []
    table_red = set()
    for h in table_hashes:
        if h not in originals:
            unresolved.append(h)
            continue
        for f in originals[h]:
            if by_file[f]["published_sha256"] != h:
                table_red.add(h)
    print(f"table hashes not an original_sha256 in MANIFEST.json: {unresolved}")
    print(f"distinct table hashes naming a redacted file: {len(table_red)}")
    bad += bool(unresolved)
    other = [h for h in set(full) - set(table_hashes)]
    for h in sorted(other):
        where = originals.get(h) or ([publisheds[h]] if h in publisheds else None)
        in_crc = any(
            h in (root / pkt / "identity" / "expected-crc.txt").read_text()
            for pkt in ("bench-a200", "bench-a202")
            if (root / pkt / "identity" / "expected-crc.txt").is_file()
        )
        print(f"non-table page hash {h[:12]}: manifest={where} expected-crc={in_crc}")

    # Abbreviated `xxxxxxxx...` hashes: resolve by prefix and file name.
    short = re.findall(r"`?([A-Za-z0-9_.\-]+)`? `([0-9a-f]{8})\.\.\.`", page)
    print(f"abbreviated name+hash pairs on page: {len(short)}")
    for name, pre in short:
        hits = sorted(
            {f for h, fs in originals.items() if h.startswith(pre) for f in fs}
        )
        ok = any(Path(f).name == name or name in f for f in hits)
        print(f"  {name} {pre}...: {'OK' if ok else 'UNRESOLVED'} {hits[:3]}")
    loose = set(re.findall(r"`([0-9a-f]{8})\.\.\.`", page)) - {p for _, p in short}
    for pre in sorted(loose):
        hits = sorted({f for h, fs in originals.items() if h.startswith(pre) for f in fs})
        print(f"  (unnamed) {pre}...: {hits[:3] if hits else 'not in MANIFEST.json'}")
    print("RESULT:", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
