#!/usr/bin/env python3
"""Reviewer probe: literal Git filename bytes under real process locales.

Usage: locale_probe.py <scripts-dir> <work-dir> <locpath> [<label> ...]

Builds every fixture with raw Git plumbing over bytes (no checker code is
imported), then runs the checker CLI named by <scripts-dir> in a fresh
process per locale.  Each locale gets a codec-specific name that the codec
decodes to the same text as a different byte string (the alias), and the
alias is kept unchanged in every tree, so a lossy transport measures the
alias and reports a false pass.  Prints one JSON object per measurement.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# (label, LC_ALL, PYTHONUTF8, codec-specific (name, alias) or None)
LOCALES = (
    ("utf8-mode", "C", "1", None),
    ("ascii", "C", "0", None),
    ("utf8-strict", "en_US.UTF-8", "0", None),
    ("latin1", "en_US.ISO-8859-1", "0", (b"\xc3\xa9.txt", b"\xe9.txt")),
    ("big5", "zh_TW.BIG5", "0", (b"\xa1\xfe.txt", b"\xa2\x41.txt")),
    ("big5hkscs", "zh_HK.BIG5-HKSCS", "0", (b"\xa2\x7e.txt", b"\xf9\xfa.txt")),
    ("johab", "ko_KR.JOHAB", "0", (b"\x84\x41.txt", b"\xd9\x31.txt")),
    ("cp932", "ja_JP.WINDOWS-31J", "0", (b"\x87\x90.txt", b"\x81\xe0.txt")),
)
GENERIC = (b"raw-\xff", b":(exclude)x\tcr\r\nlf\n")
OLD = b"".join(b"line %02d\r\n" % i for i in range(40))
CHANGED = OLD.replace(b"line 05", b"source 05 \xff \xa1\xfe \x87\x90")
EXTENDED = CHANGED.replace(b"line 35", b"later 35")
ENV = dict(os.environ, LC_ALL="C", GIT_CONFIG_NOSYSTEM="1",
           GIT_CONFIG_GLOBAL=os.devnull, GIT_AUTHOR_NAME="P",
           GIT_AUTHOR_EMAIL="p@example.invalid", GIT_COMMITTER_NAME="P",
           GIT_COMMITTER_EMAIL="p@example.invalid",
           GIT_AUTHOR_DATE="@1790000000 +0000",
           GIT_COMMITTER_DATE="@1790000000 +0000")


def git(*args, data=None):
    r = subprocess.run(("git", *args), input=data, capture_output=True, env=ENV)
    if r.returncode:
        raise RuntimeError(f"fixture git {args!r}: {r.stderr!r}")
    return r.stdout.strip()


def tree(entries):
    recs = b""
    for name, data in sorted(entries.items()):
        oid = git("hash-object", "-w", "--stdin", data=data)
        recs += b"100644 blob " + oid + b"\t" + name + b"\0"
    return git("mktree", "-z", data=recs).decode()


def commit(t, parents, msg):
    a = ["commit-tree", t, "-m", msg]
    for p in parents:
        a += ["-p", p]
    return git(*a).decode()


def histories(name, alias):
    """Return {kind: (source, target, expected rc, expected word)}."""
    def t(content, control):
        e = {name: content, b"control": control}
        if alias:
            e[alias] = b"unchanged alias\n"
        return tree(e)
    original = commit(t(OLD, OLD), [], "original")
    src = t(CHANGED, OLD)
    linear = commit(src, [original], "linear source")
    missing = commit(t(OLD, EXTENDED), [original], "unrelated work")
    retained = commit(t(CHANGED, EXTENDED), [original], "retained")
    merge = commit(src, [original, linear], "redundant merge")
    fin = t(CHANGED, CHANGED)
    branch = commit(fin, [merge], "source control edit")
    r1 = commit(src, [original], "replay 1")
    r2 = commit(fin, [r1], "replay 2")
    reverted = commit(t(OLD, EXTENDED), [r2], "revert the named file")
    extended = commit(t(CHANGED, EXTENDED), [r2], "far extension")
    return {"linear-missing": (linear, missing, 1, "STRANDED"),
            "linear-retained": (linear, retained, 0, "contained"),
            "merge-reverted": (branch, reverted, 1, "UNKNOWN"),
            "merge-retained": (branch, extended, 0, "contained")}


def child_env(lc_all, utf8, locpath):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("LC_", "PYTHON")) and k not in ("LANG", "LOCPATH")}
    env.update(LC_ALL=lc_all, PYTHONUTF8=utf8, PYTHONCOERCECLOCALE="0",
               PYTHONDONTWRITEBYTECODE="1", GIT_CONFIG_NOSYSTEM="1",
               GIT_CONFIG_GLOBAL=os.devnull)
    if lc_all not in ("C", "POSIX"):
        env["LOCPATH"] = locpath
    return env


def main():
    scripts, work, locpath = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    wanted = set(sys.argv[4:])
    checker = scripts / "check_merge_containment.py"
    for label, lc_all, utf8, pair in LOCALES:
        if wanted and label not in wanted:
            continue
        env = child_env(lc_all, utf8, locpath)
        enc = subprocess.run((sys.executable, "-c",
                              "import sys,codecs;print(codecs.lookup(sys.getfilesystemencoding()).name,"
                              "sys.stdout.encoding,sys.stdout.errors)"),
                             env=env, capture_output=True).stdout.decode().split()
        names = [pair] if pair else []
        names += [(n, None) for n in GENERIC]
        for name, alias in names:
            repo = work / f"{label}-{name.hex()}"
            repo.mkdir(parents=True)
            os.chdir(repo)
            git("init", "-q", "-b", "main")
            for kind, (src, dst, want_rc, want_word) in histories(name, alias).items():
                git("update-ref", "refs/heads/pr", src)
                git("update-ref", "refs/heads/main", dst)
                r = subprocess.run((sys.executable, "-B", str(checker), "--no-fetch",
                                    "--base", "main", "pr"), env=env, capture_output=True)
                out = r.stdout.decode("ascii", "backslashreplace")
                word = out.split()[0] if out.split() else ""
                label_text = repr(name)[1:]
                print(json.dumps({
                    "locale": label, "fs/stdout": enc, "name": name.hex(),
                    "alias": alias.hex() if alias else None, "fixture": kind,
                    "rc": r.returncode, "word": word,
                    "expected": [want_rc, want_word],
                    "pass": [r.returncode, word] == [want_rc, want_word],
                    "names_path": (label_text in out) if kind == "merge-reverted" else None,
                    "stderr": r.stderr.decode("ascii", "backslashreplace")[-300:],
                    "stdout": out.strip()[:400]}), flush=True)
            os.chdir(work)


if __name__ == "__main__":
    main()
