#!/usr/bin/env python3
"""Generic-shape privacy sweep (the CONTRIBUTING section 6 classes that have a
shape) over every blob added or modified in a commit range, plus commit
messages. Prints class, object and offset plus a sanitized shape of the
match (letters -> a, digits -> 9), never the match itself.

usage: shape_sweep.py <git-dir> <A..B> [pathprefix]
"""
import re
import subprocess
import sys

RULES = [
    ("home path", rb"/home/[a-z][a-z0-9._-]*"),
    ("macOS user path", rb"/Users/[A-Za-z]"),
    ("bench address 192.168", rb"\b192\.168\.\d+"),
    ("private 10/8 dotted", rb"\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    ("private 172.16/12 dotted", rb"\b172\.(1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}\b"),
    # assembled from code points, as scripts/docs_check.py does, so this file never spells it
    ("bench host prefix", rb"\b" + bytes((97, 109, 120, 45))),
    ("MAC-derived ifname", rb"\benx[0-9a-f]{8,}"),
    ("USB serial path", rb"serial/by-id/usb-[A-Za-z0-9]"),
    ("user@host", rb"\b[a-z_][a-z0-9_-]{1,31}@[a-z][a-z0-9-]{1,62}(\.[a-z0-9-]+)*\b(?![\w.-]*\.(com|org|net|io))"),
    ("email", rb"\b[\w.+-]+@[\w-]+\.(com|org|net|io|de|fr|ch)\b"),
    ("mdns .local host", rb"\b[a-z0-9][a-z0-9-]{2,}\.local\b"),
    ("absolute /data path", rb"/data/[a-z]"),
    ("windows user path", rb"[A-Z]:\\\\Users\\\\"),
]


def git(gd, *a):
    return subprocess.run(["git", "--git-dir", gd, *a], capture_output=True, check=True).stdout


def shape(b):
    return re.sub(rb"[A-Za-z]", b"a", re.sub(rb"[0-9]", b"9", b)).decode("latin-1")


def main():
    gd, rng = sys.argv[1], sys.argv[2]
    prefix = sys.argv[3] if len(sys.argv) > 3 else ""
    a, b = rng.split("..")
    commits = git(gd, "rev-list", "--reverse", f"{a}..{b}").decode().split()
    objs = {}
    for c in commits:
        objs[f"{c[:12]}:message"] = git(gd, "log", "-1", "--format=%B", c)
        args = ["diff-tree", "-r", "-z", "--no-renames", c] + (["--", prefix] if prefix else [])
        out = git(gd, *args).split(b"\0")
        for i in range(0, len(out) - 1):
            if out[i].startswith(b":"):
                meta = out[i][1:].split()
                if set(meta[3].decode()) != {"0"}:
                    objs[f"{c[:12]}:{out[i + 1].decode('utf-8', 'surrogateescape')}"] = ("blob", meta[3].decode())
    cache = {}
    counts = {}
    for label, o in objs.items():
        if isinstance(o, tuple):
            if o[1] not in cache:
                cache[o[1]] = git(gd, "cat-file", "blob", o[1])
            data = cache[o[1]]
            if label.endswith(".pcap"):
                continue  # binary captures are decoded by pcap_census.py
        else:
            data = o
        for name, rx in RULES:
            for m in re.finditer(rx, data):
                counts.setdefault(name, []).append(f"{label}@{m.start()} [{shape(m.group(0))}]")
    print(f"range {rng} prefix '{prefix or '*'}': {len(commits)} commits, {len(objs)} objects, {len(cache)} blobs (pcap skipped)")
    for name, _ in RULES:
        v = counts.get(name, [])
        print(f"  {name:26s} {len(v)}")
        for x in v[:12]:
            print(f"      {x}")
        if len(v) > 12:
            print(f"      ... {len(v) - 12} more")


if __name__ == "__main__":
    main()
