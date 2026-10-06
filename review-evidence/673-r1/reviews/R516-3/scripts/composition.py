#!/usr/bin/env python3
"""Reproduce exact tree overlap and section-preservation evidence."""
import os
from pathlib import Path
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
head = "72d3780d23a0b96362f8ae64059311b866ff5776"
parent = "28cdb5891b2b2d8a79b94a5bc2fb703c9fa8c721"
source = "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(*args):
    return subprocess.check_output(["rtk", "proxy", "git", "-c", "core.commitGraph=false", *args], cwd=repo, env=env)

def entries(rev):
    return {x.split(b"\t", 1)[1]: x.split(b"\t", 1)[0]
            for x in git("ls-tree", "-rz", rev).split(b"\0") if x}

base = git("merge-base", parent, source).decode().strip()
b, p, s, h = map(entries, [base, parent, source, head])
changed = {k for k in b.keys() | s.keys() if b.get(k) != s.get(k)}
predecessor = {k for k in b.keys() | p.keys() if b.get(k) != p.get(k)}
overlap = changed & predecessor
print("HEAD", git("rev-parse", "HEAD").decode().strip())
assert git("rev-parse", "HEAD").decode().strip() == head
print("TREE", git("rev-parse", head + "^{tree}").decode().strip())
print("SOURCE", source, "PARENT", parent, "COMMON_BASE", base)
print("CHANGED", len(changed), "PREDECESSOR_CHANGED", len(predecessor))
print("OVERLAP", [x.decode() for x in sorted(overlap)])
assert overlap == {b"docs/testing/CI_WORKFLOWS.md"}
for path in sorted(changed - overlap):
    assert h.get(path) == s.get(path)
    print("SOURCE_IDENTICAL", path.decode(), h.get(path).decode())
for path in (h.keys() | p.keys()) - changed:
    assert h.get(path) == p.get(path), path
print("ALL OTHER ENTRIES IDENTICAL TO PREDECESSOR")
for path in sorted(overlap):
    print(git("log", "--format=%H %s", base + ".." + parent, "--", path.decode()).decode())
    docs = [git("show", rev + ":" + path.decode()) for rev in [source, base, parent, head]]
    paths = [packet / "scratch" / ("merge-doc-" + str(i)) for i in range(3)]
    for name, content in zip(paths, docs):
        name.write_bytes(content)
    merged = subprocess.check_output(["rtk", "proxy", "git", "merge-file", "-p", *map(str, paths)], env=env)
    assert merged == docs[3]
    print("RAW THREE-WAY MERGE EXACTLY EQUALS CANDIDATE")
    def section(data, title):
        return data.split(b"## " + title + b"\n", 1)[1].split(b"\n## ", 1)[0]
    for title in [b"Fast feedback", b"Local commands"]:
        assert section(docs[2], title) == section(docs[3], title)
        print("PREDECESSOR SECTION INTACT", title.decode())
    assert section(docs[0], b"Exhaustive validation") == section(docs[3], b"Exhaustive validation")
    print("SOURCE SECTION INTACT Exhaustive validation")
print("GITLINKS")
for path, entry in sorted(h.items()):
    if entry.startswith(b"160000 "):
        assert p.get(path) == entry == s.get(path)
        print(path.decode(), entry.decode(), "UNCHANGED source/parent/candidate")
print("PASS composition entry and section identity")
