#!/usr/bin/env python3
"""Reviewer probe: two edge classes outside the byte transport.

Usage: edge_probe.py <scripts-dir> <work-dir> <locpath>

1. subdir: a linear branch whose edit to sub/file never landed, and a
   redundant-merge replay whose edit to sub/file is reverted at the tip, both
   asked from the repository root and from sub/.
2. argv-ref: under a real Big5 locale, a stranded branch named with bytes
   a1 fe beside a contained branch named a2 41, asked by its exact bytes.
Prints one JSON object per measurement.  Fixtures use raw Git plumbing only.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from locale_probe import OLD, CHANGED, EXTENDED, git, commit, child_env  # noqa: E402


def tree2(entries):
    """Nested tree with one level: {b"sub/file": data, b"top": data}."""
    sub = {k.split(b"/", 1)[1]: v for k, v in entries.items() if k.startswith(b"sub/")}
    recs = b""
    if sub:
        srecs = b""
        for name, data in sorted(sub.items()):
            oid = git("hash-object", "-w", "--stdin", data=data)
            srecs += b"100644 blob " + oid + b"\t" + name + b"\0"
        soid = git("mktree", "-z", data=srecs)
        recs += b"040000 tree " + soid + b"\tsub\0"
    for name, data in sorted(entries.items()):
        if b"/" in name:
            continue
        oid = git("hash-object", "-w", "--stdin", data=data)
        recs += b"100644 blob " + oid + b"\t" + name + b"\0"
    return git("mktree", "-z", data=recs).decode()


def run(checker, cwd, env, *args):
    r = subprocess.run((sys.executable, "-B", str(checker), "--no-fetch", "--base", "main", *args),
                       cwd=cwd, env=env, capture_output=True)
    out = r.stdout.decode("ascii", "backslashreplace")
    return r.returncode, (out.split() or [""])[0], out.strip()[:300], r.stderr.decode("ascii", "backslashreplace")[-200:]


def main():
    scripts, work, locpath = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    checker = scripts / "check_merge_containment.py"
    repo = work / "subdir"
    repo.mkdir(parents=True)
    os.chdir(repo)
    git("init", "-q", "-b", "main")

    def t(content, control):
        return tree2({b"sub/file": content, b"top": control})
    original = commit(t(OLD, OLD), [], "original")
    src = t(CHANGED, OLD)
    linear = commit(src, [original], "linear source")
    missing = commit(t(OLD, EXTENDED), [original], "unrelated work")
    merge = commit(src, [original, linear], "redundant merge")
    fin = t(CHANGED, CHANGED)
    branch = commit(fin, [merge], "control edit")
    r1 = commit(src, [original], "replay 1")
    r2 = commit(fin, [r1], "replay 2")
    reverted = commit(t(OLD, EXTENDED), [r2], "revert sub/file")
    git("checkout", "-q", "--detach", original)
    env = child_env("C", "1", locpath)
    for kind, source, target, want in (("linear-missing", linear, missing, [1, "STRANDED"]),
                                       ("merge-reverted", branch, reverted, [1, "UNKNOWN"])):
        git("update-ref", "refs/heads/pr", source)
        git("update-ref", "refs/heads/main", target)
        for where in (repo, repo / "sub"):
            rc, word, out, err = run(checker, where, env, "pr")
            print(json.dumps({"probe": "subdir", "fixture": kind,
                              "cwd": "root" if where == repo else "sub",
                              "rc": rc, "word": word, "expected": want,
                              "as_expected": [rc, word] == want, "stdout": out, "stderr": err}))

    # argv-ref aliasing under a real Big5 locale
    repo = work / "argv"
    repo.mkdir(parents=True)
    os.chdir(repo)
    git("init", "-q", "-b", "main")
    base_t = t(OLD, EXTENDED)
    original = commit(t(OLD, OLD), [], "original")
    tip = commit(base_t, [original], "unrelated work")
    stranded = commit(t(CHANGED, OLD), [original], "never landed")
    git("update-ref", "refs/heads/main", tip)
    git("update-ref", b"refs/heads/\xa1\xfe", stranded)
    git("update-ref", b"refs/heads/\xa2\x41", tip)
    for label, lc in (("big5", "zh_TW.BIG5"), ("utf8-mode", "C")):
        env = child_env(lc, "1" if lc == "C" else "0", locpath)
        r = subprocess.run((sys.executable, "-B", str(checker).encode(), b"--no-fetch", b"--base",
                            b"main", b"\xa1\xfe"), env=env, capture_output=True)
        out = r.stdout.decode("ascii", "backslashreplace")
        word = (out.split() or [""])[0]
        print(json.dumps({"probe": "argv-ref", "locale": label, "operand": "a1fe",
                          "rc": r.returncode, "word": word, "expected": [1, "STRANDED"],
                          "as_expected": [r.returncode, word] == [1, "STRANDED"],
                          "stdout": out.strip()[:300],
                          "stderr": r.stderr.decode("ascii", "backslashreplace")[-300:]}))


if __name__ == "__main__":
    main()
