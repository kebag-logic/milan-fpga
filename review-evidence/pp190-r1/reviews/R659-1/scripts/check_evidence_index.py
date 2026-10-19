#!/usr/bin/env python3
"""Check a published review-evidence directory against its MANIFEST.json and
its INDEX.md files.

Usage: python3 -I check_evidence_index.py EVIDENCE_DIR

MANIFEST.json: every listed file exists with published_sha256, and every file
present (except MANIFEST.json) is listed.
INDEX.md (any directory holding one): every `path`  N bytes  sha256 H line
matches the file's bytes and sha256, or, for a file the manifest marks
path_redacted, the manifest's original_sha256; every file in that directory
tree (except INDEX.md and nested INDEX trees) is listed.
Exit 0 when all hold, 1 otherwise.
"""
import hashlib
import json
import os
import re
import sys

LINE = re.compile(r"^- `([^`]+)`\s+(\d+) bytes\s+sha256 ([0-9a-f]{64})\s*$")


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def files_under(root):
    out = set()
    for d, _, fs in os.walk(root):
        for f in fs:
            out.add(os.path.relpath(os.path.join(d, f), root))
    return out


def main(ev):
    bad = 0
    man = json.load(open(os.path.join(ev, "MANIFEST.json")))
    listed = {}
    for e in man:
        listed[e["file"]] = e
        p = os.path.join(ev, e["file"])
        if not os.path.isfile(p):
            print("MANIFEST missing file:", e["file"]); bad += 1; continue
        if sha(p) != e["published_sha256"]:
            print("MANIFEST sha mismatch:", e["file"]); bad += 1
        if not e["path_redacted"] and e["original_sha256"] != e["published_sha256"]:
            print("MANIFEST unredacted but sha differs:", e["file"]); bad += 1
    present = files_under(ev) - {"MANIFEST.json"}
    for f in sorted(present - set(listed)):
        print("MANIFEST unlisted file:", f); bad += 1
    print(f"MANIFEST: {len(listed)} entries, {len(present)} files present, "
          f"{sum(e['path_redacted'] for e in man)} path-redacted")
    for d, _, fs in os.walk(ev):
        if "INDEX.md" not in fs:
            continue
        rel_d = os.path.relpath(d, ev)
        idx = {}
        for ln in open(os.path.join(d, "INDEX.md"), encoding="utf-8"):
            m = LINE.match(ln.rstrip("\n"))
            if m:
                idx[m.group(1)] = (int(m.group(2)), m.group(3))
        # files of this INDEX: under d, excluding nested trees with their own INDEX
        nested = [os.path.relpath(x, d) for x, _, y in os.walk(d) if x != d and "INDEX.md" in y]
        here = {f for f in files_under(d) if f != "INDEX.md"
                and not any(f.startswith(n + os.sep) for n in nested)}
        for f, (n, h) in sorted(idx.items()):
            p = os.path.join(d, f)
            if not os.path.isfile(p):
                print(f"INDEX {rel_d}: missing file", f); bad += 1; continue
            key = os.path.normpath(os.path.join(rel_d, f))
            e = listed.get(key)
            if e and e["path_redacted"]:
                if h != e["original_sha256"]:
                    print(f"INDEX {rel_d}: redacted {f} sha differs from original"); bad += 1
                continue
            if os.path.getsize(p) != n or sha(p) != h:
                print(f"INDEX {rel_d}: mismatch {f}"); bad += 1
        for f in sorted(here - set(idx)):
            print(f"INDEX {rel_d}: unlisted file", f); bad += 1
        for f in sorted(set(idx) - here):
            if os.path.isfile(os.path.join(d, f)):
                print(f"INDEX {rel_d}: lists file of a nested index", f)
        print(f"INDEX {rel_d}: {len(idx)} lines, {len(here)} files")
    print("RESULT", "OK" if bad == 0 else f"FAIL ({bad})")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
