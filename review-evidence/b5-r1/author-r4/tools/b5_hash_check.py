#!/usr/bin/env python3
"""Check every SHA-256 the B5 page cites against the evidence archive.

Usage: b5_hash_check.py <page.md> <archive-git-dir> <archive-commit>

For each 64-hex value on the page it reports, read-only from the archive
commit:
  - every MANIFEST.json entry whose original_sha256 or published_sha256 is
    that value, with path_redacted;
  - whether the published blob of that entry hashes to published_sha256;
  - otherwise, which published archive files quote the value as text.
Exit 1 if a page hash is neither a manifest hash nor quoted in the archive,
or if a published blob does not match its manifest entry.
"""
import hashlib
import json
import re
import subprocess
import sys

ROOT = "review-evidence/b5-r1"


def git(gitdir, *args):
    return subprocess.run(["git", "-C", gitdir, *args], check=True,
                          capture_output=True).stdout


def main():
    page, gitdir, commit = sys.argv[1:4]
    text = open(page, encoding="utf-8").read()
    cited = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for h in re.findall(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])", line):
            cited.append((lineno, h))
    manifest = json.loads(git(gitdir, "show", f"{commit}:{ROOT}/MANIFEST.json"))
    files = git(gitdir, "ls-tree", "-r", "--name-only", commit, ROOT).decode().split()
    blobs = {f: git(gitdir, "show", f"{commit}:{f}") for f in files}
    print(f"archive {commit}, {len(manifest)} manifest entries, "
          f"{sum(1 for e in manifest if e.get('path_redacted'))} path_redacted")
    print(f"page {page}: {len(cited)} cited SHA-256 values")
    bad = 0
    for lineno, h in cited:
        hits = [e for e in manifest
                if h in (e.get("original_sha256"), e.get("published_sha256"))]
        if hits:
            for e in hits:
                field = ("original_sha256" if e["original_sha256"] == h
                         else "published_sha256")
                blob = blobs.get(f"{ROOT}/{e['file']}")
                got = hashlib.sha256(blob).hexdigest() if blob is not None else None
                ok = got == e["published_sha256"]
                bad += not ok
                print(f"  :{lineno} {h[:12]} = {field} of {e['file']}; "
                      f"path_redacted={str(bool(e.get('path_redacted'))).lower()}; "
                      f"published blob {'matches' if ok else 'MISMATCH'} "
                      f"published_sha256 {e['published_sha256'][:12]}")
            continue
        quoted = sorted(f[len(ROOT) + 1:] for f, b in blobs.items()
                        if h.encode() in b)
        if quoted:
            print(f"  :{lineno} {h[:12]} not a manifest file hash; quoted in "
                  f"{len(quoted)} published file(s): {', '.join(quoted[:4])}"
                  f"{' ...' if len(quoted) > 4 else ''}")
        else:
            bad += 1
            print(f"  :{lineno} {h[:12]} NOT FOUND in the manifest or archive text")
    print(f"result: {'PASS' if not bad else 'FAIL'} ({bad} problem(s))")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
