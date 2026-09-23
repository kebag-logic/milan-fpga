#!/usr/bin/env python3
"""Sweep Git objects for identity tokens in several encodings.

Usage:
  identity_sweep.py --repo GITDIR --tokens TOKENS.tsv --scope NAME:REV[,REV...]
                    [--scope ...] [--prefix PATH_PREFIX] [--hide-revs]

Limit: base64 is searched by stable core only, so a token shorter than four
octets is covered at alignment 0 only.

The token file is never published. Each line is:
  label<TAB>class<TAB>ci|cs<TAB>python-bytes-literal
The report names tokens only by their opaque label and class, never by value
or by any digest of the value.

For every scope the script collects the unique blobs of every listed tree
(recursively), plus the full message and author/committer lines of every
listed commit, and searches each byte string for every token as:
  raw         the bytes (case-insensitive when mode is ci)
  hex         lower/upper hex, bare and with ':', ' ', '-', '\\x' and '0x' joins
  base64      standard and URL-safe, all three alignments, stable core only
  utf16       UTF-16LE and UTF-16BE of the token
  escaped     HTML-entity and URL-encoded forms of '&'
Compressed members (gzip, xz, bzip2, zip) are expanded and searched too.
"""
import argparse, ast, base64, bz2, collections, gzip, io, lzma, re, subprocess, sys, zipfile


def git(repo, *args, inp=None):
    return subprocess.run(["git", "--git-dir", repo, *args], input=inp,
                          capture_output=True, check=True).stdout


def load_tokens(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line:
            continue
        label, cls, mode, lit = line.split("\t", 3)
        out.append((label, cls, mode, ast.literal_eval(lit)))
    return out


def b64_cores(tok):
    cores = set()
    for enc in (base64.b64encode, base64.urlsafe_b64encode):
        for k in range(3):
            s = enc(b"\0" * k + tok)
            lead = (k * 4 + 2) // 3
            tail_bytes = (k + len(tok)) % 3
            trail = 0 if tail_bytes == 0 else 4
            core = s[lead: len(s) - trail] if trail else s[lead:]
            if len(core) >= 4:
                cores.add(core)
    return cores


def patterns(tok, mode):
    pats = []
    flags = re.IGNORECASE if mode == "ci" else 0
    variants = {tok, tok.lower(), tok.upper()} if mode == "ci" else {tok}
    pats.append(("raw", re.compile(re.escape(tok), flags)))
    if b"&" in tok:
        # spacing-tolerant and escaped forms of any token that carries '&'
        parts = tok.split(b"&")
        spaced = rb"\s*&\s*".join(re.escape(x) for x in parts)
        pats.append(("raw-spaced", re.compile(rb"\b" + spaced + rb"\b", re.IGNORECASE)))
        esc = b"|".join(re.escape(j.join(parts)) for j in (b"&amp;", b"%26", b"\\u0026"))
        pats.append(("escaped", re.compile(esc, re.IGNORECASE)))
    hexes = set()
    for v in variants:
        h = v.hex()
        for hh in (h, h.upper()):
            pairs = [hh[i:i + 2] for i in range(0, len(hh), 2)]
            for j in ("", ":", " ", "-"):
                hexes.add(j.join(pairs).encode())
            hexes.add(("".join("\\x" + p for p in pairs)).encode())
            hexes.add((", ".join("0x" + p for p in pairs)).encode())
    pats.append(("hex", re.compile(b"|".join(re.escape(x) for x in sorted(hexes)))))
    cores = set()
    for v in variants:
        cores |= b64_cores(v)
    if cores:
        pats.append(("base64", re.compile(b"|".join(re.escape(x) for x in sorted(cores)))))
    u16 = set()
    for v in variants:
        s = v.decode("latin-1")
        u16.add(s.encode("utf-16-le"))
        u16.add(s.encode("utf-16-be"))
    pats.append(("utf16", re.compile(b"|".join(re.escape(x) for x in sorted(u16)))))
    return pats


def expand(data, depth=0):
    yield data
    if depth > 2:
        return
    try:
        if data[:2] == b"\x1f\x8b":
            yield from expand(gzip.decompress(data), depth + 1)
        elif data[:6] == b"\xfd7zXZ\x00":
            yield from expand(lzma.decompress(data), depth + 1)
        elif data[:3] == b"BZh":
            yield from expand(bz2.decompress(data), depth + 1)
        elif data[:4] == b"PK\x03\x04":
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for n in z.namelist():
                    yield from expand(z.read(n), depth + 1)
    except Exception:
        return


def tree_blobs(repo, rev, prefix):
    out = git(repo, "ls-tree", "-r", "-z", "--full-tree", rev, *( [prefix] if prefix else [] ))
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, typ, oid = meta.split()
        if typ == b"blob":
            yield oid.decode(), path.decode("utf-8", "surrogateescape")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--scope", action="append", required=True,
                    help="NAME:REV[,REV...] trees and commit messages to sweep")
    ap.add_argument("--prefix", default="", help="limit trees to this path prefix")
    ap.add_argument("--hide-revs", action="store_true",
                    help="print only the scope label and a commit count, not the revisions")
    a = ap.parse_args()
    toks = load_tokens(a.tokens)
    compiled = [(l, c, pats) for (l, c, m, t) in toks for pats in [patterns(t, m)]]
    grand = 0
    for sc in a.scope:
        name, revs = sc.split(":", 1)
        revs = [r for r in revs.split(",") if r]
        blobs = {}
        for r in revs:
            for oid, path in tree_blobs(a.repo, r, a.prefix):
                blobs.setdefault(oid, path)
        msgs = {r: git(a.repo, "cat-file", "commit", r) for r in revs}
        hits = collections.Counter()
        where = collections.defaultdict(set)
        nbytes = 0
        # batch read blobs
        oids = sorted(blobs)
        inp = ("\n".join(oids) + "\n").encode()
        raw = git(a.repo, "cat-file", "--batch", inp=inp)
        pos = 0
        for oid in oids:
            nl = raw.index(b"\n", pos)
            hdr = raw[pos:nl].split()
            size = int(hdr[2])
            data = raw[nl + 1: nl + 1 + size]
            pos = nl + 1 + size + 1
            nbytes += size
            for part in expand(data):
                for l, c, pats in compiled:
                    for enc, p in pats:
                        n = len(p.findall(part))
                        if n:
                            hits[(l, c, enc)] += n
                            where[(l, c, enc)].add(blobs[oid])
        for r, data in msgs.items():
            for l, c, pats in compiled:
                for enc, p in pats:
                    n = len(p.findall(data))
                    if n:
                        hits[(l, c, enc)] += n
                        where[(l, c, enc)].add("commit-object:" + ("<withheld>" if a.hide_revs else r))
        total = sum(hits.values())
        grand += total
        shown = f"<{len(revs)} commit(s), revisions withheld>" if a.hide_revs else ",".join(revs)
        print(f"SCOPE {name} revs={shown} prefix={a.prefix or '(whole tree)'} "
              f"unique_blobs={len(blobs)} blob_bytes={nbytes} commit_objects={len(msgs)} "
              f"tokens={len(toks)} total_hits={total}")
        for k in sorted(hits):
            l, c, enc = k
            paths = sorted(where[k])
            print(f"  HIT {l} ({c}) enc={enc} count={hits[k]} files={len(paths)}")
            for p in paths[:40]:
                print(f"      {p}")
    print(f"GRAND_TOTAL_HITS {grand}")


if __name__ == "__main__":
    main()
