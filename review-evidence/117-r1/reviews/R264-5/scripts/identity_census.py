#!/usr/bin/env python3
"""Search git objects for private bench-identity tokens in several encodings.

Usage:
  identity_census.py [--summary] <repo> <private-tokens-file> <label>=<rev-range-or-commit> ...

--summary prints per-scope totals only (no object paths).

A scope `name=A..B` covers every blob, commit message and ident reachable from
B and not from A (`git rev-list --objects`), i.e. every version of every file
that range ever published, not only the tip. A scope `name=C` with no `..`
covers only the tree of commit C.

Each token is searched as: ASCII case-insensitive; UTF-16LE and UTF-16BE;
lower- and upper-case contiguous hex of its bytes; space- and colon-separated
hex; base64 of the token at the three byte alignments (inner, whole-sextet
part only); percent-encoding; DNS-SD `\\032` space escaping. Tokens shorter
than 5 bytes are matched only as ASCII with non-alphanumeric boundaries,
because their other encodings are too short to be distinctive.

The token file is private and never published. Output names each token only
by an opaque ID (its position in the private file), never by a hash or a
length: a digest of a short identity value can be brute-forced.
"""
import base64
import re
import subprocess
import sys


def git(repo, *args, inp=None):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, input=inp).stdout


def encodings(tok):
    out = {"ascii-ci": re.compile(re.escape(tok), re.I)}
    if len(tok) < 5:
        out = {"ascii-word": re.compile(rb"(?<![A-Za-z0-9])" + re.escape(tok) + rb"(?![A-Za-z0-9])")}
        return out
    out["utf16le"] = re.compile(re.escape(tok.decode("latin-1").encode("utf-16-le")), re.I)
    out["utf16be"] = re.compile(re.escape(tok.decode("latin-1").encode("utf-16-be")), re.I)
    hx = tok.hex().encode()
    out["hex"] = re.compile(re.escape(hx), re.I)
    out["hex-spaced"] = re.compile(rb"[ :]?".join(re.escape(hx[i:i + 2]) for i in range(0, len(hx), 2)), re.I)
    for off in range(3):
        b = base64.b64encode(b"\0" * off + tok)
        # drop the characters that depend on the padding bytes and the tail
        start = (off * 8 + 5) // 6 + (1 if off else 0)
        inner = b[start:len(b) - 4]
        if len(inner) >= 6:
            out[f"b64@{off}"] = re.compile(re.escape(inner))
    pct = "".join(c if c.isalnum() or c in "-._~" else "%%%02X" % ord(c) for c in tok.decode("latin-1")).encode()
    if pct != tok:
        out["pct"] = re.compile(re.escape(pct), re.I)
    if b" " in tok:
        out["dnssd-esc"] = re.compile(re.escape(tok.replace(b" ", b"\\032")), re.I)
    return out


def objects(repo, scope):
    if ".." in scope:
        a, b = scope.split("..", 1)
        lines = git(repo, "rev-list", "--objects", b, "^" + a).decode().splitlines()
        commits = git(repo, "rev-list", b, "^" + a).decode().split()
    else:
        lines = git(repo, "ls-tree", "-r", "--full-tree", scope).decode().splitlines()
        lines = [f"{l.split()[2]} {l.split(chr(9), 1)[1]}" for l in lines if l.split()[1] == "blob"]
        commits = [scope]
    blobs = {}
    for line in lines:
        parts = line.split(" ", 1)
        if len(parts) == 2:
            blobs.setdefault(parts[0], parts[1])
    batch = git(repo, "cat-file", "--batch-check", inp="\n".join(blobs).encode()).decode().splitlines()
    kinds = {l.split()[0]: l.split()[1] for l in batch}
    return {o: p for o, p in blobs.items() if kinds.get(o) == "blob"}, commits


def main():
    args = sys.argv[1:]
    summary = "--summary" in args
    args = [a for a in args if a != "--summary"]
    repo, tokfile, *scopes = args
    toks = [t for t in open(tokfile, "rb").read().split(b"\n") if t]
    pats = {t: encodings(t) for t in toks}
    tid = {t: f"T{i + 1:02d}" for i, t in enumerate(toks)}
    total = 0
    for sc in scopes:
        label, rng = sc.split("=", 1)
        blobs, commits = objects(repo, rng)
        texts = [(f"commit:{c[:8]}", git(repo, "cat-file", "commit", c)) for c in commits]
        hits = {}
        for oid, path in blobs.items():
            data = git(repo, "cat-file", "blob", oid)
            texts.append((f"{oid[:8]}:{path}", data))
        for name, data in texts:
            for t, encs in pats.items():
                for enc, rx in encs.items():
                    n = len(rx.findall(data))
                    if n:
                        hits.setdefault((tid[t], enc), []).append((name, n))
        print(f"scope {label} ({rng}): {len(blobs)} blobs, {len(commits)} commits, {len(toks)} tokens x encodings")
        if not hits:
            print("  hits: 0")
        for (h, enc), where in sorted(hits.items()):
            total += sum(n for _, n in where)
            if summary:
                continue
            print(f"  HIT token={h} enc={enc} objects={len(where)} occurrences={sum(n for _, n in where)}")
            for name, n in where[:12]:
                print(f"    {name} x{n}")
        if summary and hits:
            print(f"  SUMMARY distinct tokens hit {len({h for h, _ in hits})}; occurrences {sum(n for w in hits.values() for _, n in w)}")
    print(f"TOTAL occurrences: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
