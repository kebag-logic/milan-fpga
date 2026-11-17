#!/usr/bin/env python3
"""Verify published receipt digests and exact tracked bytes/modes/index at the review head."""
import hashlib, json, os, stat, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
head = "1a1e6665fcfd57943f2721cd3bd024eb16b0aa84"
archive = "d8bc5057f25ee85a2f19bd3a4149e7919dd7465d"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
def git(*args, cwd=root):
    return subprocess.check_output(["git", *args], cwd=cwd, env=env)
assert git("rev-parse", "HEAD").decode().strip() == head
assert git("rev-parse", "HEAD^{tree}").decode().strip() == "6a9d88680c7222514a0186e8ba8351e62b2d3514"
def audit(repo, rev):
    entries = git("ls-tree", "-rz", rev, cwd=repo).split(b"\0")
    count = 0
    links = []
    for entry in filter(None, entries):
        meta, name = entry.split(b"\t", 1)
        mode, typ, oid = meta.split()
        path = repo / os.fsdecode(name)
        if typ == b"commit":
            links.append((os.fsdecode(name), oid.decode()))
            continue
        st = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(st.st_mode), name
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(st.st_mode), name
            assert bool(st.st_mode & 0o111) == (mode == b"100755"), name
            data = path.read_bytes()
        digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert digest == oid.decode(), name
        count += 1
    assert git("diff-index", "--cached", "--raw", rev, cwd=repo) == b""
    assert git("write-tree", cwd=repo).strip() == git("rev-parse", rev+"^{tree}", cwd=repo).strip()
    print(f"{repo.name}: {count} tracked blob bytes/modes and index match {rev}")
    return dict(links)
links = audit(root, head)
for name in ["protocol-processor", "gptp-processor", "third_party/verilog-axis", "third_party/tsn-c-stack", "third_party/lwSRP"]:
    sub = root / name
    assert not sub.is_symlink()
    assert (sub / ".git").is_file()
    assert git("rev-parse", "HEAD", cwd=sub).decode().strip() == links[name]
    print(f"required gitlink {name} {links[name]}")
    audit(sub, links[name])
manifest = json.loads(git("show", archive+":review-evidence/919-r1/MANIFEST.json"))
verified = 0
for entry in manifest:
    name = entry["file"]
    if not name.startswith(("author-r3/receipts/", "author-r4/receipts/")): continue
    data = git("show", archive+":review-evidence/919-r1/"+name)
    assert hashlib.sha256(data).hexdigest() == entry["published_sha256"], name
    verified += 1
print(f"Archive {archive}: {verified} round-3/4 receipt hashes match published_sha256")
raw = git("cat-file", "commit", archive)
print("Archive commit signature header present:", b"\ngpgsig " in raw)
base = "review-evidence/919-r1/author-r4/receipts/workflows/"
rows = git("show", archive+":"+base+"verify-1a1e6665.md").decode().splitlines()
counts = {"0": 0, "NOT RUN": 0}
for line in rows:
    fields = [s.strip() for s in line.split("|")]
    if len(fields) < 8 or fields[1] not in {"rtl-fast", "elaborate", "docs"}: continue
    rc = fields[5]
    assert rc in counts, line
    counts[rc] += 1
print("Author workflow table:", counts)
paths = git("ls-tree", "-r", "--name-only", archive, "review-evidence/919-r1/author-r4/receipts/workflows/logs").decode().splitlines()
rcs = [name for name in paths if name.endswith(".rc")]
for name in rcs:
    assert git("show", archive+":"+name).strip() == b"0", name
print("Author individual workflow rc files:", len(rcs), "all zero")
assert len(rcs) == 89
assert counts == {"0":89, "NOT RUN":159}
print("PASS")
