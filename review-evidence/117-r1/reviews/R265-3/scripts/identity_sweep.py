#!/usr/bin/env python3
"""Sweep git objects for bench identity tokens in several encodings.

Usage:
  identity_sweep.py --repo <checkout with scripts/docs_check.py>
                    --git-dir <git dir holding the objects>
                    [--secret-json <file of private original field values, hex>]
                    --label <name> (--range A..B | --tree REV | --commit-msgs A..B)...

Tokens: the deny-listed identity stems are imported from the repository's own
scripts/docs_check.py (never spelled here); optional private original values are
read from a local file that is never published.

Encodings per token: raw bytes (ASCII case-insensitive), UTF-16LE/BE, hex text
(contiguous, and with ' ', ':', '-', '\\x', '%' separators, any case), base64 and
base64url at all three alignments, and the same inside gzip/bz2/xz/zip members.

Output: per scope, per token class and encoding, a hit count and the object
path and offset of each hit. Never prints the matched bytes.
"""
import argparse
import base64
import bz2
import gzip
import importlib.util
import io
import json
import lzma
import re
import subprocess
import sys
import zipfile


def load_docs_check(repo):
    spec = importlib.util.spec_from_file_location("docs_check", f"{repo}/scripts/docs_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def case_variants(t):
    out = {t, t.lower(), t.upper(), t.title(), t.capitalize()}
    return {v for v in out if v}


def b64_cores(t, urlsafe=False):
    """Base64 substrings that depend only on t, for each of the 3 alignments."""
    enc = base64.urlsafe_b64encode if urlsafe else base64.b64encode
    cores = set()
    for k in range(3):
        e = enc(b"\0" * k + t)
        lo = -(-8 * k // 6)
        hi = (8 * (k + len(t))) // 6
        c = e[lo:hi]
        if len(c) >= 3:
            cores.add(c)
    return cores


def encodings(token_bytes, exact_case):
    """Return list of (encoding-name, compiled bytes regex)."""
    pats = []
    variants = {token_bytes} if exact_case else {v.encode("latin-1") for v in case_variants(token_bytes.decode("latin-1"))}
    flags = 0 if exact_case else re.IGNORECASE
    pats.append(("raw", re.compile(re.escape(token_bytes), flags)))
    for name, codec in (("utf16le", "utf-16-le"), ("utf16be", "utf-16-be")):
        alts = [re.escape(v.decode("latin-1").encode(codec)) for v in variants]
        pats.append((name, re.compile(b"|".join(alts))))
    hex_alts = []
    for v in variants:
        hx = v.hex()
        pairs = [hx[i:i + 2] for i in range(0, len(hx), 2)]
        hex_alts.append(re.escape(hx.encode()))
        for sep in (b" ", b":", b"-", b"\\x", b"%", b", 0x", b",0x", b" 0x"):
            hex_alts.append(re.escape(sep.join(p.encode() for p in pairs)))
    pats.append(("hex", re.compile(b"|".join(hex_alts), re.IGNORECASE)))
    for name, url in (("base64", False), ("base64url", True)):
        cores = set()
        for v in variants:
            cores |= b64_cores(v, url)
        if cores:
            pats.append((name, re.compile(b"|".join(re.escape(c) for c in sorted(cores)))))
    return pats


def expand(name, data, depth=0):
    """Yield (subname, bytes) for the object and any decompressible layers."""
    yield name, data
    if depth > 3:
        return
    try:
        if data[:2] == b"\x1f\x8b":
            yield from expand(name + "|gunzip", gzip.decompress(data), depth + 1)
        elif data[:3] == b"BZh":
            yield from expand(name + "|bunzip2", bz2.decompress(data), depth + 1)
        elif data[:6] == b"\xfd7zXZ\x00":
            yield from expand(name + "|unxz", lzma.decompress(data), depth + 1)
        elif data[:4] == b"PK\x03\x04":
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for info in z.infolist():
                    yield from expand(name + "|" + info.filename, z.read(info), depth + 1)
    except Exception as exc:  # report, never hide
        print(f"   note: could not expand {name}: {type(exc).__name__}")


def git(gd, *args, inp=None):
    return subprocess.run(["git", f"--git-dir={gd}", *args], input=inp,
                          capture_output=True, check=True).stdout


def objects_for(gd, spec):
    kind, arg = spec
    if kind == "range":
        out = git(gd, "rev-list", "--objects", arg).decode()
        objs = []
        for line in out.splitlines():
            parts = line.split(" ", 1)
            objs.append((parts[0], parts[1] if len(parts) > 1 else ""))
        # keep blobs only
        shas = "\n".join(o for o, _ in objs).encode()
        types = git(gd, "cat-file", "--batch-check=%(objectname) %(objecttype)", inp=shas).decode().split("\n")
        t = dict(l.split() for l in types if l.strip())
        return [(o, p) for o, p in objs if t.get(o) == "blob"]
    if kind == "tree":
        out = git(gd, "ls-tree", "-r", arg).decode()
        res = []
        for line in out.splitlines():
            meta, path = line.split("\t", 1)
            mode, typ, sha = meta.split()
            if typ == "blob":
                res.append((sha, path))
        return res
    if kind == "msgs":
        out = git(gd, "rev-list", arg).decode().split()
        return [("msg:" + c, "commit message " + c[:12]) for c in out]
    raise ValueError(kind)


def read_obj(gd, sha):
    if sha.startswith("msg:"):
        return git(gd, "cat-file", "commit", sha[4:])
    return git(gd, "cat-file", "blob", sha)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--secret-json")
    ap.add_argument("--label", required=True)
    ap.add_argument("--range", action="append", default=[])
    ap.add_argument("--tree", action="append", default=[])
    ap.add_argument("--commit-msgs", action="append", default=[])
    a = ap.parse_args()

    dc = load_docs_check(a.repo)
    tokens = [
        ("peer product stem (docs_check)", dc._PEER_TOKEN.encode(), False),
        ("switch vendor long name (docs_check)", dc._VENDOR_TOKEN.encode(), False),
        ("switch vendor short mark (docs_check)", dc._VENDOR_MARK.encode(), False),
        ("suite name (docs_check)", dc._SUITE_TOKEN.encode(), False),
        ("test-plan stem (docs_check)", dc._PLAN_TOKEN.encode(), False),
    ]
    if a.secret_json:
        sec = json.load(open(a.secret_json))
        for k, hx in sec.items():
            tokens.append((f"peer original {k} (private value)", bytes.fromhex(hx), True))
            # also the distinctive part that survives if only a prefix/suffix is masked
    compiled = [(name, encodings(tb, exact)) for name, tb, exact in tokens]

    specs = [("range", r) for r in a.range] + [("tree", t) for t in a.tree] + [("msgs", m) for m in a.commit_msgs]
    objs = []
    seen = set()
    for s in specs:
        for sha, path in objects_for(a.git_dir, s):
            if sha not in seen:
                seen.add(sha)
                objs.append((sha, path))
    total_bytes = 0
    hits = {}
    for sha, path in objs:
        data = read_obj(a.git_dir, sha)
        total_bytes += len(data)
        for sub, layer in expand(path or sha, data):
            for tname, pats in compiled:
                for ename, rx in pats:
                    for m in rx.finditer(layer):
                        hits.setdefault((tname, ename), []).append((sha[:12], sub, m.start()))
    print(f"[{a.label}] objects scanned: {len(objs)}, bytes: {total_bytes}, specs: {specs}")
    for tname, pats in compiled:
        for ename, _ in pats:
            h = hits.get((tname, ename), [])
            print(f"  {tname:48s} {ename:10s} hits {len(h)}")
            for sha, sub, off in h[:40]:
                print(f"      {sha} {sub} @{off}")
            if len(h) > 40:
                print(f"      ... {len(h) - 40} more")


if __name__ == "__main__":
    main()
