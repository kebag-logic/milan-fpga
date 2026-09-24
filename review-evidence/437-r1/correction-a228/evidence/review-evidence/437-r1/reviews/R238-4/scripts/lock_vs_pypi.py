#!/usr/bin/env python3
"""Map every sha256 in the PR's Markdown lock to the PyPI file it names.

Usage: lock_vs_pypi.py <requirements.txt>
Prints, per pinned requirement, each locked hash with the PyPI filename it
matches in that exact release, or UNMATCHED. Exit 1 on any unmatched hash.
"""
import json, sys, urllib.request

def pins(text):
    out, name = {}, None
    for line in text.splitlines():
        for w in line.split("#", 1)[0].replace("\\", " ").split():
            if "==" in w:
                name, ver = w.split("==", 1); out[name] = (ver, [])
            elif w.startswith("--hash=sha256:"):
                out[name][1].append(w.split(":", 1)[1])
    return out

bad = 0
for name, (ver, hashes) in pins(open(sys.argv[1]).read()).items():
    url = f"https://pypi.org/pypi/{name}/{ver}/json"
    data = json.load(urllib.request.urlopen(url, timeout=30))
    files = {f["digests"]["sha256"]: (f["filename"], f["packagetype"]) for f in data["urls"]}
    sdists = [f["filename"] for f in data["urls"] if f["packagetype"] == "sdist"]
    for h in hashes:
        fn = files.get(h)
        print(f"{name}=={ver} {h} -> {fn[0] if fn else 'UNMATCHED'}")
        bad += fn is None
        if fn and fn[1] == "sdist":
            print(f"  NOTE {name}: locked hash is an sdist")
    print(f"  {name}: {len(data['urls'])} files on PyPI for {ver}; sdists not locked: {sdists}")
sys.exit(1 if bad else 0)
