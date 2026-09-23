#!/usr/bin/env python3
"""Find any 7+ hex-digit prefix of a superseded archive commit in Git objects.

Usage: superseded_link_sweep.py GITDIR SHAS.txt NAME:REV[,REV...] [...]
SHAS.txt lines are 'LABEL SHA'; the report prints labels only, so the report
itself never spells a superseded SHA.
For each scope, every blob of every listed tree and every listed commit
object is searched for the first 7 hex digits of each superseded SHA (as a
whole hex word, so longer hex strings that merely contain it do not count
unless they start with it). Reports counts and paths only.
"""
import re, subprocess, sys

gitdir, shafile = sys.argv[1], sys.argv[2]
pairs = [l.split() for l in open(shafile) if l.strip()]
shas = [s for _l, s in pairs]
label = {s[:7]: l for l, s in pairs}
pat = re.compile(rb"(?<![0-9a-fA-F])(" + b"|".join(s[:7].encode() for s in shas) + rb")[0-9a-f]*")


def git(*a, inp=None):
    return subprocess.run(["git", "--git-dir", gitdir, *a], input=inp, capture_output=True, check=True).stdout


grand = 0
for sc in sys.argv[3:]:
    name, revs = sc.split(":", 1)
    revs = revs.split(",")
    blobs = {}
    for r in revs:
        for rec in git("ls-tree", "-r", "-z", r).split(b"\0"):
            if rec:
                meta, path = rec.split(b"\t", 1)
                _m, t, oid = meta.split()
                if t == b"blob":
                    blobs.setdefault(oid.decode(), path.decode("utf-8", "replace"))
    oids = sorted(blobs)
    raw = git("cat-file", "--batch", inp=("\n".join(oids) + "\n").encode())
    pos, hits = 0, []
    for oid in oids:
        nl = raw.index(b"\n", pos)
        size = int(raw[pos:nl].split()[2])
        data = raw[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1
        for m in pat.finditer(data):
            hits.append((blobs[oid], label[m.group(1).decode()]))
    for r in revs:
        for m in pat.finditer(git("cat-file", "commit", r)):
            hits.append(("commit-object:" + name, label[m.group(1).decode()]))
    grand += len(hits)
    print(f"SCOPE {name} blobs={len(blobs)} commits={len(revs)} superseded_prefixes={len(shas)} hits={len(hits)}")
    agg = {}
    for p, s in hits:
        agg.setdefault(p, set()).add(s)
    for p in sorted(agg):
        print(f"  HIT {p} :: {','.join(sorted(agg[p]))}")
print(f"GRAND_TOTAL_HITS {grand}")
