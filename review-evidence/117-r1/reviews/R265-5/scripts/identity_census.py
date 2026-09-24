#!/usr/bin/env python3
"""Census identity tokens over every blob and commit message in a Git range.

Usage:
  identity_census.py --git-dir D --tokens T [--base B] REV [REV...]

Tokens are read from T (lines `class<TAB>token`, `#` comments), so this
script carries none. Every blob reachable from a REV and not from B, and
every commit message in B..REV, is searched for each token in these
encodings: raw (case-insensitive), ASCII hex (lower and upper, bare and with
`:`, ` ` or `-` separators), base64 (three alignments, plus URL-safe),
UTF-16LE, UTF-16BE, NetBIOS first-level, DNS label, URL-escaped,
JSON `\\u0026`, HTML `&amp;` and reversed. Output names the class, encoding,
object path and count, never the token.
"""
import argparse
import base64
import collections
import subprocess


def git(gd, *args, inp=None):
    return subprocess.run(
        ["git", "--git-dir", gd, *args], input=inp, capture_output=True, check=True
    ).stdout


def encodings(tok):
    b = tok.encode()
    out = {"raw": b}
    out["hex"] = b.hex().encode()
    out["HEX"] = b.hex().upper().encode()
    for sep in (":", " ", "-"):
        out[f"hex{sep!r}"] = sep.join(f"{c:02x}" for c in b).encode()
        out[f"HEX{sep!r}"] = sep.join(f"{c:02X}" for c in b).encode()
    for pad in range(3):
        enc = base64.b64encode(b"\x00" * pad + b)
        # drop the chars influenced by padding / alignment at both ends
        core = enc[(pad * 4 + 2) // 3 + 1:]
        core = core.rstrip(b"=")[:-2] if len(core) > 6 else core
        if len(core) >= 4:
            out[f"b64/{pad}"] = core
            out[f"b64url/{pad}"] = core.replace(b"+", b"-").replace(b"/", b"_")
    out["utf16le"] = tok.encode("utf-16-le")
    out["utf16be"] = tok.encode("utf-16-be")
    out["netbios"] = bytes(
        x for c in b.upper() for x in (0x41 + (c >> 4), 0x41 + (c & 0xF))
    )
    out["dnslabel"] = bytes([len(b)]) + b
    if b"&" in b:
        out["url"] = b.replace(b"&", b"%26")
        out["json"] = b.replace(b"&", b"\\u0026")
        out["html"] = b.replace(b"&", b"&amp;")
    out["reversed"] = b[::-1]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--base")
    ap.add_argument("revs", nargs="+")
    a = ap.parse_args()
    toks = []
    for ln in open(a.tokens, encoding="utf-8"):
        if ln.strip() and not ln.startswith("#"):
            cls, tok = ln.rstrip("\n").split("\t", 1)
            toks.append((f"{cls}#{len(toks) + 1}", tok))
    rng = list(a.revs) + ([f"^{a.base}"] if a.base else [])
    objs = git(a.git_dir, "rev-list", "--objects", *rng).decode().splitlines()
    commits = git(a.git_dir, "rev-list", *rng).decode().split()
    blobs = {}
    for ln in objs:
        oid, _, path = ln.partition(" ")
        if git(a.git_dir, "cat-file", "-t", oid).strip() == b"blob":
            blobs.setdefault(oid, path)
    print(f"range: {' '.join(rng)}")
    print(f"commits: {len(commits)}; distinct blobs: {len(blobs)}; tokens: {len(toks)}")
    hits = collections.Counter()
    where = collections.defaultdict(set)
    targets = [(f"blob:{p}", git(a.git_dir, "cat-file", "blob", o)) for o, p in blobs.items()]
    targets += [(f"commit:{c[:12]}", git(a.git_dir, "cat-file", "commit", c)) for c in commits]
    for cls, tok in toks:
        for name, needle in encodings(tok).items():
            ci = name == "raw"
            n_ = needle.lower() if ci else needle
            for tname, data in targets:
                hay = data.lower() if ci else data
                n = hay.count(n_)
                if n:
                    hits[(cls, name)] += n
                    where[(cls, name)].add(f"{tname} x{n}")
    total = sum(hits.values())
    print(f"total hits: {total}")
    for (cls, name), n in sorted(hits.items()):
        print(f"HIT class={cls} encoding={name} count={n}")
        for w in sorted(where[(cls, name)])[:40]:
            print(f"    {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
