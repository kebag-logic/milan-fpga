"""Verify the round 5 merge commit, its tree, unchanged pins and clean checkouts.

The merge must have parents (lane, dev) in that order and the tree that
`git merge-tree --write-tree` predicts. Every path either side changed must
carry that side's bytes unless both sides changed it. Gitlinks, raw blobs,
modes and every initialized dependency are re-read from disk.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess

LANE = "6b4feeca5d2fab0ec35cf071322cc775a5b15cb5"
DEV = "fa7347fc59173f90e4feec2df207692e6e6e72ec"
BASE = "d40e4e9827be2516f8f34b9d65f0a483fff2194c"
TREE = "f1c1f47cb4fefb8a6c68418d03dc762f72cbee15"
STACK_PIN = "70936b77dc41981e192438388cd0aced69954f18"
SUBJECT = "Merge dev fa7347fc into F3b parent lane"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repo", type=Path, required=True)
args = parser.parse_args()
root = args.repo.resolve()
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")


def git(directory, *argv):
    if directory != root:
        top = subprocess.check_output(["git", "-C", str(directory), "rev-parse", "--show-toplevel"], env=env).decode().strip()
        assert top == str(directory)
        origin = subprocess.check_output(["git", "-C", str(directory), "remote", "get-url", "origin"], env=env).decode().strip()
        expected = subprocess.check_output(["git", "-C", str(root), "config", "-f", ".gitmodules", "--get",
                                            "submodule." + directory.relative_to(root).as_posix() + ".url"], env=env).decode().strip()
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


def entry(revision, path):
    out = git(root, "ls-tree", "-z", revision, "--", path).rstrip(b"\0")
    return out.split(b"\t", 1)[0].decode() if out else None


def changed(a, b):
    return set(git(root, "diff", "--no-renames", "--name-only", a, b).decode().splitlines())


assert git(root, "remote", "get-url", "origin").decode().strip() == "https://github.com/kebag-logic/milan-fpga.git"
assert git(root, "branch", "--show-current").decode().strip() == "665-f3b-parent"
head = git(root, "rev-parse", "HEAD").decode().strip()
parents = git(root, "rev-list", "--parents", "-n", "1", "HEAD").decode().split()[1:]
assert parents == [LANE, DEV], parents
tree = git(root, "rev-parse", "HEAD^{tree}").decode().strip()
assert tree == TREE, tree
predicted = git(root, "merge-tree", "--write-tree", LANE, DEV).decode().split()[0]
assert predicted == TREE, predicted
assert git(root, "merge-base", LANE, DEV).decode().strip() == BASE
body = git(root, "log", "-1", "--format=%B").decode()
assert body.strip() == SUBJECT and len(body.strip().splitlines()) == 1
name = git(root, "config", "user.name").decode().strip()
mail = git(root, "config", "user.email").decode().strip()
identity = git(root, "log", "-1", "--format=%an%n%ae%n%cn%n%ce").decode().split("\n")[:4]
assert identity == [name, mail, name, mail], identity

lane_paths = changed(BASE, LANE)
dev_paths = changed(BASE, DEV)
both = sorted(lane_paths & dev_paths)
for path in lane_paths - dev_paths:
    assert entry(head, path) == entry(LANE, path), path
for path in dev_paths - lane_paths:
    assert entry(head, path) == entry(DEV, path), path
for path in set(git(root, "ls-tree", "-r", "--name-only", head).decode().splitlines()) - lane_paths - dev_paths:
    assert entry(head, path) == entry(BASE, path), path
versus_dev = sorted(changed(DEV, head))
assert set(versus_dev) == lane_paths, sorted(set(versus_dev) ^ lane_paths)

count, links = verify(root, head)
assert links == [(p, entry(LANE, p).split()[2]) for p, _ in links]
submodules = []
for relative, pin in links:
    directory = root / relative
    if relative == "external":
        assert not (directory / ".git").exists()
        submodules.append(dict(path=relative, pin=pin, initialized=False))
        continue
    actual = git(directory, "rev-parse", "HEAD").decode().strip()
    assert actual == pin
    if relative == "third_party/tsn-c-stack":
        assert pin == STACK_PIN
    measured, nested = verify(directory, pin)
    assert not nested
    submodules.append(dict(path=relative, pin=pin, initialized=True, blobs=measured))
print(json.dumps(dict(head=head, parents=parents, tree=tree, merge_tree_prediction=predicted, subject=SUBJECT,
                      lane_paths=len(lane_paths), dev_paths=len(dev_paths), both_sides=both,
                      head_versus_dev=len(versus_dev), superproject_blobs=count,
                      gitlinks_unchanged_from_lane=True, submodules=submodules, clean=True), indent=2))
