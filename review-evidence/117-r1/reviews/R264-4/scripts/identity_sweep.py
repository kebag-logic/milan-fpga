#!/usr/bin/env python3
"""Sweep git blobs, commit messages and path names for bench-identity tokens
in several encodings. Prints class labels, scopes, object paths and offsets,
never the matched bytes, so the output is publishable.

usage: identity_sweep.py <git-dir> <tokens.tsv> <scope-spec>...

scope-spec is  NAME=REV[:PATHPREFIX]  (every blob in REV's tree under the
prefix, plus REV's message) or  NAME=RANGE@A..B[:PATHPREFIX]  (every commit in
the range: each commit's message, and every blob added or modified under the
prefix by that commit, plus every path name it touches).

tokens.tsv lines: class<TAB>ci|cs<TAB>hex(token). Keep that file private.
Exit 0 when no hit, 1 when any hit, 2 on usage error.
"""
import base64
import re
import subprocess
import sys


def variants(tok, ci):
    """(encoding-name, bytes, case_insensitive) tuples for one token."""
    forms = {tok}
    if ci:
        forms |= {tok.lower(), tok.upper()}
    out = [("raw", tok, ci)]
    for f in sorted(forms):
        h = f.hex()
        out.append(("hex", h.encode(), True))
        for sep in (":", " ", "-", "\\x", "0x", ", 0x"):
            out.append(("hex-sep", sep.join(h[i:i + 2] for i in range(0, len(h), 2)).encode(), True))
        out.append(("utf16le", f.decode("latin-1").encode("utf-16-le"), False))
        out.append(("utf16be", f.decode("latin-1").encode("utf-16-be"), False))
        out.append(("decimal-list", ", ".join(str(b) for b in f).encode(), False))
        out.append(("decimal-list", ",".join(str(b) for b in f).encode(), False))
        out.append(("nbns", b"".join(bytes([0x41 + (b >> 4), 0x41 + (b & 15)]) for b in f.upper()), False))
        out.append(("url", "".join("%%%02X" % b if not chr(b).isalnum() else chr(b) for b in f).encode(), True))
        if len(f) >= 6:
            for pad in range(3):
                # keep only the characters fixed by the token bytes alone:
                # encode with two different neighbourhoods and keep the
                # longest run where both encodings agree
                e1 = base64.b64encode(b"\x00" * pad + f + b"\x00\x00\x00")
                e2 = base64.b64encode(b"\xff" * pad + f + b"\xff\xff\xff")
                best, cur = b"", b""
                for x, y in zip(e1, e2):
                    cur = cur + bytes([x]) if x == y else b""
                    if len(cur) > len(best):
                        best = cur
                if len(best) >= 6:
                    out.append(("base64", best, False))
    seen, uniq = set(), []
    for e in out:
        k = (e[1].lower() if e[2] else e[1], e[2])
        if k in seen or not e[1]:
            continue
        seen.add(k)
        uniq.append(e)
    return uniq


def git(gd, *args, inp=None):
    return subprocess.run(["git", "--git-dir", gd, *args], input=inp,
                          capture_output=True, check=True).stdout


def blobs_of_tree(gd, rev, prefix):
    out = git(gd, "ls-tree", "-r", "-z", rev, "--", prefix) if prefix else git(gd, "ls-tree", "-r", "-z", rev)
    res = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, typ, sha = meta.split()
        if typ == b"blob":
            res.append((path.decode("utf-8", "surrogateescape"), sha.decode()))
    return res


def range_objects(gd, a, b, prefix):
    commits = git(gd, "rev-list", "--reverse", f"{a}..{b}").decode().split()
    items = []
    for c in commits:
        items.append((f"{c[:12]}:message", git(gd, "log", "-1", "--format=%B", c)))
        args = ["diff-tree", "-r", "-z", "--no-renames", "--root", c]
        if prefix:
            args += ["--", prefix]
        out = git(gd, *args).split(b"\0")
        i = 0
        while i < len(out):
            rec = out[i]
            if rec.startswith(b":"):
                meta = rec[1:].split()
                path = out[i + 1].decode("utf-8", "surrogateescape")
                newsha = meta[3].decode()
                items.append((f"{c[:12]}:pathname:{path}", path.encode()))
                if set(newsha) != {"0"}:
                    items.append((f"{c[:12]}:{path}", ("blob", newsha)))
                i += 2
            else:
                i += 1
    return commits, items


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    gd, tokf = sys.argv[1], sys.argv[2]
    table = []
    for line in open(tokf):
        cls, mode, hx = line.rstrip("\n").split("\t")
        table.append((cls, variants(bytes.fromhex(hx), mode == "ci")))
    any_hit = 0
    for spec in sys.argv[3:]:
        name, rest = spec.split("=", 1)
        prefix = ""
        if ":" in rest:
            rest, prefix = rest.split(":", 1)
        if rest.startswith("RANGE@"):
            a, b = rest[6:].split("..")
            commits, items = range_objects(gd, a, b, prefix)
            desc = f"{len(commits)} commits"
        else:
            items = [(f"{rest[:12]}:message", git(gd, "log", "-1", "--format=%B", rest))]
            for path, sha in blobs_of_tree(gd, rest, prefix):
                items.append((f"{rest[:12]}:pathname:{path}", path.encode()))
                items.append((f"{rest[:12]}:{path}", ("blob", sha)))
            desc = "1 tree"
        cache = {}
        hits = {}
        nobj = 0
        for label, obj in items:
            if isinstance(obj, tuple):
                sha = obj[1]
                if sha not in cache:
                    cache[sha] = git(gd, "cat-file", "blob", sha)
                data = cache[sha]
            else:
                data = obj
            nobj += 1
            low = data.lower()
            for cls, vs in table:
                for enc, pat, ci in vs:
                    hay = low if ci else data
                    p = pat.lower() if ci else pat
                    for m in re.finditer(re.escape(p), hay):
                        hits.setdefault((cls, enc), []).append(f"{label}@{m.start()}")
        print(f"== scope {name} ({desc}, prefix '{prefix or '*'}'): {nobj} objects scanned, {len(cache)} distinct blobs")
        classes = sorted({c for c, _ in table})
        for cls in classes:
            tot = sum(len(v) for (c, e), v in hits.items() if c == cls)
            print(f"   {cls:22s} hits {tot}")
            for (c, e), v in sorted(hits.items()):
                if c == cls:
                    print(f"      [{e}] {len(v)}: " + "; ".join(v[:6]) + (" ..." if len(v) > 6 else ""))
        any_hit |= bool(hits)
    return 1 if any_hit else 0


if __name__ == "__main__":
    sys.exit(main())
