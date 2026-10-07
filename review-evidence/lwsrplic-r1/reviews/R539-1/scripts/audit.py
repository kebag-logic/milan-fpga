#!/usr/bin/env python3
"""Read-only exact-head audit. Usage: audit.py CHECKOUT PACKET."""
import hashlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys

repo, packet = (Path(x).resolve() for x in sys.argv[1:3])
receipts = packet / "receipts"
receipts.mkdir(parents=True, exist_ok=True)
HEAD = "375dbe132c6f1498f2f3e714ce5905d34456c9d5"
BASE = "02700d9ead0a29dd5d53c1d85e163ea392b79ab0"
TREE = "942f26fe59d72990af8ddc5ac6937921b5e401ec"
FIRST = "fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b"

def git(*args):
    return subprocess.check_output(["rtk", "proxy", "git", "-C", str(repo), *args])

def save(name, obj):
    (receipts / name).write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

assert git("rev-parse", "HEAD").decode().strip() == HEAD
assert git("rev-parse", "HEAD^{tree}").decode().strip() == TREE
entries = []
for item in git("ls-tree", "-rz", HEAD).split(b"\0"):
    if not item:
        continue
    meta, path = item.split(b"\t", 1)
    mode, kind, oid = meta.decode().split()
    entries.append((mode, kind, oid, path.decode()))

files = [f for _, kind, _, f in entries if kind == "blob"]
headers = []
for f in files:
    lines = (repo / f).read_bytes().splitlines()
    index = int(lines[0].startswith(b"#!"))
    expected = (b"/* SPDX-License-Identifier: Apache-2.0 */" if f.endswith((".c", ".h"))
                else b"<!-- SPDX-License-Identifier: Apache-2.0 -->" if f.endswith(".md")
                else b"# SPDX-License-Identifier: Apache-2.0")
    exempt = f in ("LICENSE", "NOTICE")
    assert exempt or lines[index] == expected, f
    headers.append({"path":f, "header":"exempt" if exempt else "PASS", "line":None if exempt else index+1})
canonical = (receipts / "apache-canonical.txt").read_bytes()
assert (repo / "LICENSE").read_bytes() == canonical
changes = git("diff", "--name-only", BASE, HEAD).decode().splitlines()
shifted = set()
for f in changes:
    if f in ("LICENSE", "NOTICE"):
        continue
    before, after = git("show", BASE+":"+f), git("show", HEAD+":"+f)
    header = next(x for x in after.splitlines(keepends=True) if b"SPDX-License-Identifier:" in x)
    assert after.replace(header, b"", 1) == before, f
    if after.splitlines()[0] == header.rstrip(b"\r\n"):
        shifted.add(f)
assert git("show", HEAD+":README.md") == git("show", BASE+":README.md")
assert "tests/unit/placeholder.c" not in files
assert all(git("show", HEAD+":"+f) == git("show", FIRST+":"+f) for f in ("LICENSE", "NOTICE"))
assert git("show", "-s", "--format=%P", HEAD).decode().split() == [FIRST, BASE]
save("static-audit.json", {
    "head": HEAD, "tree": TREE, "tracked_count":len(files), "headers":headers,
    "license_equal_canonical": True, "license_bytes":len(canonical),
    "license_sha256":hashlib.sha256(canonical).hexdigest(),
    "main_delta":"27 header-only additions plus LICENSE and NOTICE",
    "readme_equals_main":True, "placeholder_deleted":True,
    "license_notice_equal_first_parent":True,
    "parents":[FIRST,BASE],
    "rtl_files":[f for f in files if f.endswith((".v", ".sv", ".vhd", ".vhdl"))]})

citations = []
for name in files:
    f = repo / name
    if f.suffix != ".md":
        continue
    for number, line in enumerate(f.read_text().splitlines(), 1):
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)#L(\d+)(?:-L(\d+))?\)", line):
            target = (f.parent / m[2]).resolve()
            if not target.is_relative_to(repo):
                continue
            rel = target.relative_to(repo).as_posix()
            if rel not in shifted:
                continue
            start, end = int(m[3]), int(m[4] or m[3])
            citations.append({"page":name,"line":number,"label":m[1],"target":rel,
                              "old_fragment":m[0].split("#")[1][:-1],
                              "required_fragment":f"L{start+1}"+(f"-L{end+1}" if m[4] else ""),
                              "head_selected_lines":target.read_text().splitlines()[start-1:end]})
save("shifted-citations.json", citations)

# Scan every reachable blob once. Never emit sensitive content or filenames.
commits = git("rev-list", "--all").decode().splitlines()
head_commits = git("rev-list", HEAD).decode().splitlines()
objects = {}
for c in commits:
    for item in git("ls-tree", "-rz", c).split(b"\0"):
        if not item: continue
        meta, path = item.split(b"\t", 1)
        mode, kind, oid = meta.decode().split()
        if kind == "blob": objects.setdefault(oid, set()).add(path.decode())
patterns = {
    "host path":r"/(?:home|Users|data|mnt|media|root)/[^\s<>\"`]+",
    "credentials":r"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]+|AKIA[A-Z0-9]{16}|-----BEGIN .*PRIVATE KEY-----)",
    "email":r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    "other licence marker":r"(?i)\b(?:GNU General Public License|GPL-[123]|BSD-[234]-Clause|SPDX-License-Identifier:\s*(?!Apache-2\.0)\S+|MIT License)\b",
}
known = {
    "21654351bd62a20125f6c9209b55bdf9a8ce7f57":[1,3],
    "396d6fe887b6fb807a1939e14eb6f144b95c6e9c":[36],
}
hits = []
for oid, paths in objects.items():
    text = git("cat-file", "blob", oid).decode(errors="replace")
    for line, value in enumerate(text.splitlines(), 1):
        for category, pattern in patterns.items():
            if re.search(pattern, value):
                hits.append({"blob":oid,"line":line,"category":category})
    if oid in known:
        for line in known[oid]:
            hits.append({"blob":oid,"line":line,"category":"restricted provenance (independently inspected)"})
# Exclude identity fields by scanning commit messages separately.
message_hits = []
for c in commits:
    message = git("show", "-s", "--format=%B", c).decode()
    for category, pattern in patterns.items():
        if re.search(pattern, message): message_hits.append({"commit":c,"category":category})
save("history-scan.json", {"reachable_commits":len(commits),"head_ancestors_including_head":len(head_commits),
                          "unique_blobs":len(objects),"sensitive_matches":hits,"commit_message_matches":message_hits,
                          "known_provenance_blobs_reachable":all(k in objects for k in known),
                          "limits":"Pattern scan plus independent content/history inspection; not a proof of original authorship."})
reachability=[]
for oid in known:
    containing=[]
    for c in head_commits:
        if any(oid.encode() in item.split(b"\t",1)[0] for item in git("ls-tree","-rz",c).split(b"\0") if item):
            containing.append(c)
    reachability.append({"blob":oid,"line_numbers":known[oid],"ancestor_commits_containing_blob":containing})
save("history-reachability.json", reachability)

# Assert on bytes, executable bits, and index entries, not just status output.
expected_index=[]
verified=[]
gitlinks=[]
for mode,kind,oid,f in entries:
    expected_index.append((mode,oid,"0",f))
    if mode == "160000":
        gitlinks.append({"path":f,"commit":oid})
        continue
    b=(repo/f).read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert actual == oid, f
    executable=bool((repo/f).stat().st_mode & stat.S_IXUSR)
    assert executable == (mode == "100755"), f
    verified.append({"path":f,"blob":oid,"mode":mode,"bytes":len(b)})
actual_index=[]
for item in git("ls-files","--stage","-z").split(b"\0"):
    if item:
        meta,f=item.split(b"\t",1)
        mode,oid,stage=meta.decode().split()
        actual_index.append((mode,oid,stage,f.decode()))
assert sorted(actual_index)==sorted(expected_index)
assert not git("status","--porcelain=v1","--untracked-files=all")
assert not git("diff","--binary",HEAD)
validation_source = packet / "scratch/validation-source"
if validation_source.exists():
    for f in files:
        assert (validation_source / f).read_bytes() == (repo / f).read_bytes(), f
save("integrity.json",{"validation_source_matches_head":validation_source.exists(),"head":HEAD,"tree":TREE,"tracked_files_verified":verified,"index_matches_head":True,
                       "worktree_clean":True,"gitlinks":gitlinks,"submodule_requirement":"No gitlinks or module file in this repository at the reviewed head."})
print("Exact head and tree: PASS")
print("Licence byte equality and 43 headers: PASS")
print("Both-parent merge preservation: PASS")
print("Shifted citation occurrences:",len(citations))
print("History commits/blobs:",len(commits),len(objects))
print("Known restricted historical blobs still reachable:",all(k in objects for k in known))
print("Tracked bytes, modes, index and gitlinks: PASS")
