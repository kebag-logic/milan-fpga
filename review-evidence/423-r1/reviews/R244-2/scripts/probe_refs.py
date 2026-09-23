#!/usr/bin/env python3
"""Reviewer probe: branch names with non-injective bytes (outside filenames).

Two branches whose names differ only by a lossy pair: the lossy-named one is
STRANDED, its alias equals main.  (i) no operand with HEAD on the lossy
branch; (ii) the lossy name given as an argv operand.  Runs the CLI in a fresh
process per locale.  Applies to any checker source directory.

    probe_refs.py <checker-src-dir> <locale-dir> <scratch-dir>
"""
import json
import os
import subprocess
import sys
from pathlib import Path

CASES = (("big5", "zh_TW.BIG5", b"\xa1\xfe", b"\xa2\x41"),
         ("big5hkscs", "zh_HK.BIG5-HKSCS", b"\xa1\xfe", b"\xa2\x41"),
         ("johab", "ko_KR.JOHAB", b"\x84\x41", b"\xd9\x31"),
         ("cp932", "ja_JP.WINDOWS-31J", b"\x87\x90", b"\x81\xe0"))


def git(*args, cwd, data=None):
    p = subprocess.run(("git", *args), cwd=cwd, input=data, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


def main():
    src, locales, scratch = (Path(a).resolve() for a in sys.argv[1:4])
    checker = src / "check_merge_containment.py"
    rows = []
    for label, loc, lossy, alias in CASES:
        repo = scratch / label
        repo.mkdir(parents=True)
        env = {"PATH": os.environ["PATH"], "HOME": str(repo), "LOCPATH": str(locales),
               "LC_ALL": loc, "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
               "PYTHONDONTWRITEBYTECODE": "1", "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_CONFIG_GLOBAL": os.devnull}
        git("init", "-q", "-b", "main", cwd=repo)
        t = git("mktree", cwd=repo, data=b"")
        o = git("commit-tree", t.decode(), "-m", "O", cwd=repo,
                data=None).decode()
        blob = git("hash-object", "-w", "--stdin", cwd=repo, data=b"work\n").decode()
        t2 = git("mktree", "-z", cwd=repo,
                 data=b"100644 blob " + blob.encode() + b"\twork.txt\0").decode()
        s = git("commit-tree", t2, "-p", o, "-m", "stranded", cwd=repo).decode()
        git("update-ref", "refs/heads/main", o, cwd=repo)
        git("update-ref", b"refs/heads/" + lossy, s, cwd=repo)
        git("update-ref", b"refs/heads/" + alias, o, cwd=repo)
        git("symbolic-ref", "HEAD", b"refs/heads/" + lossy, cwd=repo)
        for kind, operands in (("no-operand", []), ("argv-operand", [lossy]),
                               ("argv-full-ref", [b"refs/heads/" + lossy])):
            p = subprocess.run([sys.executable, "-B", str(checker), "--no-fetch",
                                "--base", "main", *operands], cwd=repo, env=env,
                               capture_output=True)
            out = p.stdout.decode("ascii", "backslashreplace")
            err = p.stderr.decode("ascii", "backslashreplace")
            rows.append({"codec": label, "case": kind, "rc": p.returncode,
                         "stdout": out, "stderr": err[-400:],
                         "truth": "lossy-named branch is STRANDED (1 commit)"})
        git("symbolic-ref", "HEAD", "refs/heads/main", cwd=repo)
    print(json.dumps(rows, indent=1, ensure_ascii=True))
    for r in rows:
        first = (r["stdout"].split() or ["-"])[0]
        print(f"# {r['codec']:10} {r['case']:14} rc={r['rc']} first={first}"
              f" {'FALSE-PASS' if r['rc'] == 0 else ''}", file=sys.stderr)


if __name__ == "__main__":
    main()
