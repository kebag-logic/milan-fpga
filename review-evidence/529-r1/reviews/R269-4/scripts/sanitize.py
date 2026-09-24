#!/usr/bin/env python3
"""Redact host-identifying strings from the publishable packet files in place.

Replaces the packet root, the review clone, the pinned tool directory, the
home directory, the data root, the local account name and the host name with
neutral placeholders, then reports any file that still contains one of them.
Only text files under receipts/ and scripts/ plus REPORT.md are touched;
scratch/ is never published and is skipped, and so is this script, whose
rules are all taken from its arguments.

Usage: sanitize.py <packet-root> <review-clone> <pinned-bin> <data-root> <account> <host>
"""
import os
import sys
from pathlib import Path


def main() -> int:
    root, clone, pin, data, acct, host = sys.argv[1:7]
    home = os.path.expanduser("~")
    subs = [
        (pin, "<pinned-bin>"),
        (root, "<packet>"),
        (clone, "<review-clone>"),
        (home, "$HOME"),
        (data, "<data-root>"),
        (" %s %s " % (acct, acct), " <user> <group> "),
        (host, "<host>"),
    ]
    me = Path(__file__).resolve()
    files = [Path(root) / "REPORT.md"]
    for sub in ("receipts", "scripts"):
        files += [p for p in (Path(root) / sub).rglob("*") if p.is_file()]
    changed, left = 0, []
    for f in files:
        if f.resolve() == me:
            continue
        try:
            t = f.read_text()
        except UnicodeDecodeError:
            continue
        n = t
        for a, b in subs:
            n = n.replace(a, b)
        if n != t:
            f.write_text(n)
            changed += 1
        for needle in (home, data, acct, host):
            if needle and needle in n:
                left.append("%s: %s" % (f, needle))
    print("files rewritten: %d" % changed)
    print("residual matches: %d" % len(left))
    for l in left[:40]:
        print("  " + l)
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
