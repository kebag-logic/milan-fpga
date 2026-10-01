#!/usr/bin/env python3
"""Check every SHA-256 the findings page cites against the pinned archive.

usage: hash_check.py <page.md> <extracted review-evidence/b5-r1 dir at the pin>

For each 64-hex value on the page: is it a manifest original_sha256 or
published_sha256 (and of which file, masked or not), and in which published
files of the three packets is it quoted. For the artifact table, the page's
byte count is checked against the masked RAW-ARTIFACTS.json entry too.
"""
import json
import os
import re
import sys

HEX = re.compile(r"\b[0-9a-f]{64}\b")


def main():
    page, root = sys.argv[1:3]
    text = open(page, encoding="utf-8").read()
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    orig = {e["original_sha256"]: e for e in man}
    pub = {e["published_sha256"]: e for e in man}
    files = {}
    for d in ("author", "author-r2", "author-r3"):
        for dp, _, fs in os.walk(os.path.join(root, d)):
            for f in fs:
                p = os.path.join(dp, f)
                try:
                    files[os.path.relpath(p, root)] = open(p, encoding="utf-8").read()
                except UnicodeDecodeError:
                    pass
    raw = json.load(open(os.path.join(root, "author/RAW-ARTIFACTS.json")))
    raw_by_sha = {e["sha256"]: e["bytes"] for e in raw["files"]}
    print(f"RAW-ARTIFACTS.json entries with a hash: {len(raw_by_sha)}")
    seen, problems = [], 0
    for m in HEX.finditer(text):
        h = m.group(0)
        if h in seen:
            continue
        seen.append(h)
        line = text.count("\n", 0, m.start()) + 1
        cls = []
        if h in orig:
            e = orig[h]
            cls.append(f"original_sha256 of {e['file']} "
                       f"({'path_redacted' if e['path_redacted'] else 'unmasked'}, "
                       f"published {'==' if e['published_sha256'] == h else '!='} original)")
        if h in pub and h not in orig:
            cls.append(f"published_sha256 only of {pub[h]['file']}")
        quoted = sorted(f for f, c in files.items() if h in c)
        if h in raw_by_sha:
            row = next((r for r in text.splitlines() if h in r and r.startswith("|")), "")
            cells = [c.strip() for c in row.strip("|").split("|")]
            page_bytes = cells[1] if len(cells) > 2 else "?"
            ok = str(raw_by_sha[h]) == page_bytes
            cls.append(f"RAW-ARTIFACTS entry size {raw_by_sha[h]} page {page_bytes} {'OK' if ok else 'MISMATCH'}")
            problems += not ok
        if not cls and not quoted:
            problems += 1
            cls.append("NOT FOUND")
        print(f":{line} {h[:16]} | {'; '.join(cls) or '-'} | quoted in {len(quoted)} published file(s)"
              + (f": {', '.join(quoted[:4])}" if quoted else ""))
    print(f"distinct hashes on the page: {len(seen)}; problems: {problems}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
