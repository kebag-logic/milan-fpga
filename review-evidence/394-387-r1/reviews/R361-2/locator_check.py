#!/usr/bin/env python3
"""Cross-check the page's artifact locator against the public archive.

Usage: locator_check.py <repo> <rev> <archive_dir>
<archive_dir> holds review-evidence/394-387-r1 at 8f983d24 (blobs fetched and
git-hash verified separately). Checks:
  1. every MANIFEST.json entry exists and matches its published_sha256;
  2. every page raw-artifact row (cycle, name, bytes, sha256) appears in
     author/RAW-ARTIFACTS.json and in author/cycleNN/raw-artifacts.json;
  3. index paths are temporary-directory names (historical);
  4. the page carries no absolute local path and no private packet name.
Exit 1 on any failure.
"""
import hashlib
import json
import os
import re
import subprocess
import sys


def main() -> int:
    repo, rev, adir = sys.argv[1:4]
    page = subprocess.run(
        ["git", "-C", repo, "show", f"{rev}:docs/findings/394_387_E1_SWITCH_CYCLES.md"],
        check=True, capture_output=True, text=True).stdout
    bad = 0

    manifest = json.load(open(os.path.join(adir, "MANIFEST.json")))
    ok = 0
    for e in manifest:
        p = os.path.join(adir, e["file"])
        h = hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None
        if h == e["published_sha256"]:
            ok += 1
        else:
            bad += 1
            print(f"MANIFEST mismatch: {e['file']}")
    listed = {e["file"] for e in manifest}
    on_disk = set()
    for root, _, files in os.walk(adir):
        for f in files:
            on_disk.add(os.path.relpath(os.path.join(root, f), adir))
    print(f"MANIFEST.json entries {len(manifest)}, verified {ok}; "
          f"archive files {len(on_disk)}; unlisted {sorted(on_disk - listed)}")

    rows = re.findall(r"^\| (\d+) \| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$", page, re.M)
    raw = json.load(open(os.path.join(adir, "author/RAW-ARTIFACTS.json")))
    top = {(os.path.basename(r["path"]), r["size"], r["sha256"], r["path"]) for r in raw}
    hits_top = hits_cyc = 0
    for cyc, name, size, sha in rows:
        want = f"/cycle{int(cyc):02d}/{name}"
        if any(t[0] == name and t[1] == int(size) and t[2] == sha and t[3].endswith(want) for t in top):
            hits_top += 1
        else:
            bad += 1
            print(f"row not in RAW-ARTIFACTS.json: {cyc} {name}")
        per = json.load(open(os.path.join(adir, f"author/cycle{int(cyc):02d}/raw-artifacts.json")))
        if any(r["path"].endswith(want) and r["size"] == int(size) and r["sha256"] == sha for r in per):
            hits_cyc += 1
        else:
            bad += 1
            print(f"row not in cycle index: {cyc} {name}")
    tmp_paths = sum(r["path"].startswith("/tmp/") for r in raw)
    print(f"page rows {len(rows)}; in RAW-ARTIFACTS.json {hits_top}; in per-cycle {hits_cyc}; "
          f"RAW-ARTIFACTS entries {len(raw)}, of which /tmp paths {tmp_paths}")

    leaks = re.findall(r"(/tmp/\S*|/home/\S*|/data/\S*|2026-09-23/394-a375|a375/)", page)
    print(f"page absolute-path or private-packet tokens: {leaks}")
    bad += len(leaks)
    print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
