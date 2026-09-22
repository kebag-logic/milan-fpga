#!/usr/bin/env python3
"""Snapshot or compare read-only checkout integrity (R242 scratch tool).

snapshot REPO OUT.json : HEAD, symbolic ref, raw index sha256, `ls-files -s`,
                         per-tracked-path working-tree kind/mode/raw-blob,
                         porcelain status (untracked+ignored), refs.
compare A.json B.json  : exit 0 iff every recorded field is identical.
Never writes to REPO (GIT_OPTIONAL_LOCKS=0, no index refresh).
"""
import hashlib
import json
import os
import stat
import subprocess
import sys

ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0", LC_ALL="C")


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", repo, *args], env=ENV, check=check,
                          capture_output=True).stdout


def blob_sha1(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def snapshot(repo, out):
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    sym = git(repo, "symbolic-ref", "-q", "HEAD", check=False).decode().strip()
    index_rel = git(repo, "rev-parse", "--git-path", "index").decode().strip()
    index_path = index_rel if os.path.isabs(index_rel) else os.path.join(repo, index_rel)
    with open(index_path, "rb") as fh:
        index_sha = hashlib.sha256(fh.read()).hexdigest()
    ls = git(repo, "ls-files", "-s", "-z")
    entries = []
    for rec in ls.split(b"\0"):
        if not rec:
            continue
        meta, path = rec.split(b"\t", 1)
        mode, sha, stage = meta.decode().split()
        full = os.path.join(repo.encode(), path)
        try:
            st = os.lstat(full)
        except FileNotFoundError:
            entries.append([path.decode("utf-8", "surrogateescape"), mode, sha, stage,
                            "missing", None, None])
            continue
        if stat.S_ISLNK(st.st_mode):
            kind, wt = "symlink", blob_sha1(os.readlink(full))
        elif stat.S_ISREG(st.st_mode):
            with open(full, "rb") as fh:
                kind, wt = "regular", blob_sha1(fh.read())
        elif stat.S_ISDIR(st.st_mode):
            sub = subprocess.run(["git", "-C", full, "rev-parse", "HEAD"], env=ENV,
                                 capture_output=True)
            top = subprocess.run(["git", "-C", full, "rev-parse", "--show-toplevel"],
                                 env=ENV, capture_output=True).stdout.strip()
            own = top == os.path.realpath(full)
            kind = "dir"
            wt = sub.stdout.decode().strip() if (sub.returncode == 0 and own) else "no-own-repo"
        else:
            kind, wt = "other", None
        entries.append([path.decode("utf-8", "surrogateescape"), mode, sha, stage, kind,
                        oct(stat.S_IMODE(st.st_mode)), wt])
    status = git(repo, "status", "--porcelain=v2", "--branch", "--ignored",
                 "--untracked-files=all", "-z")
    refs = git(repo, "for-each-ref", "--format=%(objectname) %(refname)")
    snap = {
        "head": head,
        "symbolic_ref": sym,
        "index_file_sha256": index_sha,
        "ls_files_sha256": hashlib.sha256(ls).hexdigest(),
        "tracked_entries": len(entries),
        "wt_mismatch_vs_index": [e[0] for e in entries
                                 if e[4] == "regular" and e[6] != e[2]],
        "entries_sha256": hashlib.sha256(json.dumps(entries).encode()).hexdigest(),
        "status_porcelain": status.decode("utf-8", "surrogateescape"),
        "refs_sha256": hashlib.sha256(refs).hexdigest(),
        "refs_count": len(refs.splitlines()),
        "entries": entries,
    }
    with open(out, "w") as fh:
        json.dump(snap, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in snap.items() if k != "entries"}, indent=1,
                     sort_keys=True))


def compare(a, b):
    with open(a) as fa, open(b) as fb:
        ja, jb = json.load(fa), json.load(fb)
    diff = sorted(k for k in set(ja) | set(jb) if ja.get(k) != jb.get(k))
    print("IDENTICAL" if not diff else "DIFFERENT: " + ", ".join(diff))
    return 0 if not diff else 1


if __name__ == "__main__":
    if sys.argv[1] == "snapshot":
        snapshot(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "compare":
        sys.exit(compare(sys.argv[2], sys.argv[3]))
    else:
        sys.exit(2)
