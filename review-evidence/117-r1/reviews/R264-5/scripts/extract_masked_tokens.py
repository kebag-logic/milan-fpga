#!/usr/bin/env python3
"""Derive the values later redaction rounds masked, from superseded public archive commits.

Usage: extract_masked_tokens.py <bare-repo> <pin-commit> <out-private-tokens.txt> <superseded-commit>...

For every blob path that exists both in a superseded commit's review-evidence/117-r1
tree and at the pin, with different bytes, the differing regions are located
(position-aligned when the lengths agree, otherwise by a byte sequence match)
and the superseded bytes of each region are widened to a whole token. The
tokens are written to a PRIVATE file (never published: the values are the
bench identity the census must not find). stdout carries only counts and the
SHA-256/length of each token, so the receipt is public-safe.
"""
import difflib
import re
import subprocess
import sys

TOKCH = re.compile(rb"[A-Za-z0-9_\-.:/]")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True).stdout


def tree(repo, commit):
    out = {}
    for line in git(repo, "ls-tree", "-r", commit, "--", "review-evidence/117-r1").splitlines():
        meta, path = line.split(b"\t", 1)
        _, typ, oid = meta.split()
        if typ == b"blob":
            out[path.decode()] = oid.decode()
    return out


def widen(buf, s, e):
    while s > 0 and TOKCH.match(buf[s - 1:s]):
        s -= 1
    while e < len(buf) and TOKCH.match(buf[e:e + 1]):
        e += 1
    return buf[s:e]


def regions(old, new):
    if len(old) == len(new):
        i, n = 0, len(old)
        while i < n:
            if old[i] != new[i]:
                j = i
                while j < n and old[j] != new[j]:
                    j += 1
                yield i, j
                i = j
            else:
                i += 1
    else:
        # line-level match first (fast), then a character match inside each
        # changed line pair, mapped back to offsets in the superseded bytes
        ol, nl = old.splitlines(keepends=True), new.splitlines(keepends=True)
        starts, pos = [], 0
        for line in ol:
            starts.append(pos)
            pos += len(line)
        sm = difflib.SequenceMatcher(None, ol, nl, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag not in ("replace", "delete"):
                continue
            for k in range(i1, i2):
                o = ol[k]
                n = nl[j1 + (k - i1)] if tag == "replace" and j1 + (k - i1) < j2 else b""
                if len(o) > 20000 or len(n) > 20000:
                    yield starts[k], starts[k] + len(o)
                    continue
                cm = difflib.SequenceMatcher(None, o, n, autojunk=False)
                for t2, a1, a2, _, _ in cm.get_opcodes():
                    if t2 in ("replace", "delete") and a2 > a1:
                        yield starts[k] + a1, starts[k] + a2


def main():
    repo, pin, outp, *sup = sys.argv[1:]
    pin_t = tree(repo, pin)
    toks = {}
    done = set()
    for s in sup:
        chain = git(repo, "rev-list", s, "^" + pin).decode().split()
        for c in chain:
            t = tree(repo, c)
            for path, oid in t.items():
                if path not in pin_t or pin_t[path] == oid or (oid, pin_t[path]) in done:
                    continue
                done.add((oid, pin_t[path]))
                old = git(repo, "cat-file", "blob", oid)
                new = git(repo, "cat-file", "blob", pin_t[path])
                if len(old) != len(new) and b"\0" in old[:65536]:
                    print(f"skip-unaligned-binary {c[:8]} {path}")
                    continue
                for a, b in regions(old, new):
                    tok = widen(old, a, b).strip(b".:/-_")
                    if len(tok) >= 3 and not set(tok) <= set(b"#"):
                        toks.setdefault(tok, set()).add(f"{c[:8]}:{path.split('117-r1/')[1]}")
    with open(outp, "wb") as f:
        for tok in sorted(toks):
            f.write(tok + b"\n")
    hexes = [t for t in toks if re.fullmatch(rb"[0-9a-f]{64}", t)]
    print(f"superseded commits examined: {len(sup)}; distinct changed tokens: {len(toks)}")
    print(f"  of which 64-hex manifest values (published hashes that changed between rounds, not identity): {len(hexes)}")
    print(f"  other tokens (identity candidates, kept only in the private file): {len(toks) - len(hexes)}")


if __name__ == "__main__":
    main()
