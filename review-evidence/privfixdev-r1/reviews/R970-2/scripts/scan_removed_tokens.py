#!/usr/bin/env python3
"""Reviewer probe: do the names this change removed survive anywhere at HEAD?

The token list is DERIVED from the change, so this file spells none of them:
every word (and every part of a hyphenated word, and every dotted-quad) that
occurs on a removed line of BASE..HEAD and on no added line is a "removed
token".  Each one is then searched, case-insensitively and on word boundaries,
through every tracked text file at BASE and at HEAD.

Output names a token only by length and sha256 prefix.  A token still present
at HEAD is listed with its file:line locations (no line text), so the report
stays free of the removed names while a second reviewer can open each place.

Usage: scan_removed_tokens.py <repo> <base> <head>
"""
import hashlib
import re
import subprocess
import sys

repo, base, head = sys.argv[1:4]


def git(*args: str) -> str:
    done = subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True)
    return done.stdout.decode("utf-8", errors="replace")


WORD = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")
QUAD = re.compile(r"(?<![0-9.])\d{1,3}(?:\.\d{1,3}){3}(?![0-9.])")


def tokens(line: str) -> set[str]:
    found = set(QUAD.findall(line))
    for word in WORD.findall(line):
        low = word.lower()
        found.add(low)
        found.update(part for part in low.split("-") if len(part) >= 3)
    # A bare number is a count or an octet, never a name.
    return {t for t in found if len(t) >= 3 and not t.isdigit()}


removed: set[str] = set()
added: set[str] = set()
for line in git("diff", "--unified=0", base, head).split("\n"):
    if line.startswith(("+++", "---")):
        continue
    if line.startswith("-"):
        removed |= tokens(line[1:])
    elif line.startswith("+"):
        added |= tokens(line[1:])
gone = sorted(removed - added)


def hits(rev: str, token: str) -> list[str]:
    # An identifier that merely contains the letters (a signal name with an
    # underscore suffix) is not the name, so "_" counts as a word character.
    pattern = r"(^|[^A-Za-z0-9_.])" + re.escape(token) + r"($|[^A-Za-z0-9_.])"
    done = subprocess.run(
        ["git", "-C", repo, "grep", "-n", "-I", "-i", "-E", pattern, rev, "--", "."],
        capture_output=True,
    )
    if done.returncode not in (0, 1):
        raise SystemExit(done.stderr.decode())
    out = []
    for row in done.stdout.decode("utf-8", errors="replace").split("\n"):
        if row:
            _rev, path, lineno, _text = row.split(":", 3)
            out.append(f"{path}:{lineno}")
    return out


print(f"removed tokens (on a removed line, on no added line): {len(gone)}")
survivors = 0
for token in gone:
    ident = hashlib.sha256(token.encode()).hexdigest()[:12]
    at_base, at_head = hits(base, token), hits(head, token)
    kind = "dotted-quad" if QUAD.fullmatch(token) else "word"
    print(f"token sha256:{ident} len={len(token)} {kind}: base lines {len(at_base)}, head lines {len(at_head)}")
    if at_head:
        survivors += 1
        for place in at_head[:5]:
            print(f"    HEAD {place}")
        if len(at_head) > 5:
            print(f"    ... {len(at_head) - 5} more")
print(f"removed tokens still present at HEAD: {survivors}")
