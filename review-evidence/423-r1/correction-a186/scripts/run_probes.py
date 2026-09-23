#!/usr/bin/env python3
"""Run the R244-1 finding probes against one source tree and record receipts.

Usage: run_probes.py <source-root> <label>

<source-root> contains scripts/ (an archive of the head under test).  Every
fixture, locale and temporary tree lives under ../scratch; receipts are
written to ../receipts/probes-<label>/.  The lane checkout is only read: the
self-test runs from it because its first arm needs a repository with one commit.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
SCRATCH = PACKET / "scratch"
LOCALES = SCRATCH / "locales"
LANE = Path("$LANES/423-retained-redundant-replay")
PROBES = HERE / "r244-probes"

BASE_ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                PYTHONCOERCECLOCALE="0")
BASE_ENV.pop("PYTHONIOENCODING", None)
LOCALE_ENV = {
    "utf8-mode": {"PYTHONUTF8": "1", "LC_ALL": "C"},
    "utf8-strict": {"PYTHONUTF8": "0", "LC_ALL": "en_US.UTF-8"},
    "ascii": {"PYTHONUTF8": "0", "LC_ALL": "C"},
    "latin1": {"PYTHONUTF8": "0", "LC_ALL": "en_US.ISO-8859-1", "LOCPATH": str(LOCALES)},
    "big5": {"PYTHONUTF8": "0", "LC_ALL": "zh_TW.BIG5", "LOCPATH": str(LOCALES)},
}


def env_for(name, tmp):
    env = dict(BASE_ENV, TMPDIR=str(tmp), **LOCALE_ENV[name])
    if "LOCPATH" not in LOCALE_ENV[name]:
        env.pop("LOCPATH", None)
    return env


def run(argv, cwd, env, timeout=1800):
    p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=timeout)
    return {"argv": [os.fsdecode(a) if isinstance(a, bytes) else str(a) for a in argv],
            "cwd": str(cwd), "rc": p.returncode,
            "locale": {k: env.get(k) for k in ("LC_ALL", "PYTHONUTF8", "LOCPATH")},
            "stdout": p.stdout.decode("utf-8", "backslashreplace"),
            "stderr": p.stderr.decode("utf-8", "backslashreplace")[-3000:]}


def fixture_git(cwd, *args, data=None):
    p = subprocess.run(("git", "-c", "user.name=F", "-c", "user.email=f@example.invalid", *args),
                       cwd=cwd, input=data, capture_output=True, env=BASE_ENV)
    if p.returncode:
        raise SystemExit(f"fixture git {args!r}: {p.stderr!r}")
    return p.stdout.strip()


def build_multitarget(d):
    """aa-ok contained, pr stranded on non-UTF-8 and Big5-lossy names, zz-later contained."""
    d.mkdir(parents=True)
    fixture_git(d, "init", "-q", "-b", "main")
    names = (b"raw-\xff", b"\xa1\xfe.txt", b"plain")

    def tree(content):
        recs = b""
        for name in names:
            oid = fixture_git(d, "hash-object", "-w", "--stdin", data=content + name)
            recs += b"100644 blob " + oid + b"\t" + name + b"\0"
        return fixture_git(d, "mktree", "-z", data=recs).decode()

    o = fixture_git(d, "commit-tree", tree(b"old "), "-m", "O").decode()
    pr = fixture_git(d, "commit-tree", tree(b"new "), "-p", o, "-m", "pr").decode()
    other = fixture_git(d, "hash-object", "-w", "--stdin", data=b"unrelated\n").decode()
    base_tree = fixture_git(d, "ls-tree", "-z", o) + b"100644 blob " + other.encode() + b"\tzz\0"
    main = fixture_git(d, "commit-tree", fixture_git(d, "mktree", "-z", data=base_tree).decode(),
                       "-p", o, "-m", "unrelated main work").decode()
    for ref, oid in (("main", main), ("pr", pr), ("aa-ok", o), ("zz-later", o)):
        fixture_git(d, "update-ref", "refs/heads/" + ref, oid)


def main():
    root, label = Path(sys.argv[1]).resolve(), sys.argv[2]
    checker = root / "scripts" / "check_merge_containment.py"
    work = SCRATCH / ("probes-" + label)
    out = PACKET / "receipts" / ("probes-" + label)
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(out, ignore_errors=True)
    (work / "tmp").mkdir(parents=True)
    out.mkdir(parents=True)
    results = {}
    py = sys.executable

    # R244-A: exact redundant merge; tip reverts the Big5-lossy name.
    fx = work / "big5fx"
    subprocess.run((py, PROBES / "probe_big5.py", "build", fx), check=True, env=BASE_ENV,
                   capture_output=True)
    for loc in ("big5", "utf8-mode", "utf8-strict", "latin1", "ascii"):
        results[f"A-merge-{loc}"] = run((py, checker, "--no-fetch", "--base", "main", "pr"),
                                        fx, env_for(loc, work / "tmp"))
    # R244-A, existing touched-path arm: linear stranded work on the lossy name.
    fx = work / "big5lin"
    subprocess.run(("sh", PROBES / "probe_big5_linear.sh", fx), check=True, env=BASE_ENV,
                   capture_output=True)
    for loc in ("big5", "utf8-mode", "utf8-strict", "latin1", "ascii"):
        results[f"A-linear-{loc}"] = run((py, checker, "--no-fetch", "--base", "main", "pr"),
                                         fx, env_for(loc, work / "tmp"))
    # R244-D: several targets through a real process stdout.
    fx = work / "multitarget"
    build_multitarget(fx)
    for loc in ("utf8-strict", "utf8-mode", "ascii", "latin1", "big5"):
        results[f"D-multitarget-{loc}"] = run(
            (py, checker, "--no-fetch", "--base", "main", "aa-ok", "pr", "zz-later"),
            fx, env_for(loc, work / "tmp"))
    # R244-C: the reviewer's guard histories and single-guard mutants.
    results["C-guards"] = run((py, PROBES / "probe_guards.py", root, work / "guards"),
                              work, dict(BASE_ENV, TMPDIR=str(work / "tmp")))
    (out / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=True) + "\n")
    for key, value in results.items():
        first = value["stdout"].strip().splitlines()[:1]
        print(f"{key:24} rc={value['rc']} {first[0][:150] if first else value['stderr'][-150:]!r}")


if __name__ == "__main__":
    main()
