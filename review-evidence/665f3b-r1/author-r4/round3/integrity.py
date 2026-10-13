"""Verify the candidate bytes, unchanged firmware inputs and dependency pins."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
root = args.repo.resolve()
resume = "651ccb5aea1bc4d99f356503c188947d39e0c9e4"
allowed = {"scripts/ci_scope.py", "docs/testing/CI_WORKFLOWS.md", "sw/firmware/ctrl/maap/README.md"}
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(directory, *argv):
    if directory != root:
        top = subprocess.check_output(["git", "-C", str(directory), "rev-parse", "--show-toplevel"], env=env).decode().strip()
        assert top == str(directory)
        origin = subprocess.check_output(["git", "-C", str(directory), "remote", "get-url", "origin"], env=env).decode().strip()
        expected = subprocess.check_output(["git", "-C", str(root), "config", "-f", ".gitmodules", "--get", "submodule." + directory.relative_to(root).as_posix() + ".url"], env=env).decode().strip()
        assert origin == expected
    return subprocess.check_output(["git", "-C", str(directory), *argv], env=env)

def verify(directory, revision):
    count = 0
    links = []
    for record in git(directory, "ls-tree", "-r", "-z", revision).split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        relative = os.fsdecode(raw_path)
        path = directory / relative
        if kind == b"commit":
            links.append((relative, oid.decode()))
            continue
        assert kind == b"blob"
        info = path.lstat()
        if mode == b"120000":
            assert stat.S_ISLNK(info.st_mode)
            data = os.fsencode(os.readlink(path))
        else:
            assert stat.S_ISREG(info.st_mode)
            assert bool(info.st_mode & stat.S_IXUSR) == (mode == b"100755")
            data = path.read_bytes()
        calculated = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        assert calculated == oid.decode(), relative
        count += 1
    assert not git(directory, "status", "--porcelain", "--ignored", "--untracked-files=all")
    return count, links

assert git(root, "remote", "get-url", "origin").decode().strip() == "https://github.com/kebag-logic/milan-fpga.git"
assert git(root, "branch", "--show-current").decode().strip() == "665-f3b-parent"
head = git(root, "rev-parse", "HEAD").decode().strip()
changed = git(root, "diff", "--name-only", resume, head).decode().splitlines()
assert set(changed) == allowed
body = git(root, "log", "-1", "--format=%B").decode().strip()
assert len(body.splitlines()) == 1
parent = git(root, "rev-parse", "HEAD^").decode().strip()
assert parent == resume
count, links = verify(root, head)
submodules = []
for relative, pin in links:
    directory = root / relative
    if relative == "external":
        assert not (directory / ".git").exists()
        submodules.append(dict(path=relative, pin=pin, initialized=False))
        continue
    actual = git(directory, "rev-parse", "HEAD").decode().strip()
    assert actual == pin
    measured, nested = verify(directory, pin)
    assert not nested
    submodules.append(dict(path=relative, pin=pin, initialized=True, blobs=measured))
print(json.dumps(dict(head=head, parent=parent, subject=body, changed=changed,
                     superproject_blobs=count, submodules=submodules,
                     clean=True, unchanged_firmware_and_build_inputs=True), indent=2))
