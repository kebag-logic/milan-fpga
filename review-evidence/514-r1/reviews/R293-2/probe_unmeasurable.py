#!/usr/bin/env python3
"""Arm-level unmeasurable cases for the optional linear retention arm.

    python3 -B probe_unmeasurable.py HEAD_CHECKER MUTANT_CHECKER ROOT

Builds two deterministic fixtures whose linear H succeeds but whose T raises a
measurement error at the arm level (not per path):
  empty-net-delta   source A then revert(A), both replayed exactly;
  criss-cross-base  linear source/replay whose merge-base --all has two bases.
Runs the exact-head checker and a mutant whose arm-level except branch returns
True, both with --current-retention. Expected: head UNKNOWN/1; if the mutant
reports retained/0 while its self-test still passes (see mutation-probe), the
branch is unguarded by the self-test. Exit 0 when head is UNKNOWN/1 on both.
"""
import os
import shutil
import subprocess
import sys

HEAD, MUTANT, ROOT = (os.path.abspath(a) for a in sys.argv[1:4])
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_AUTHOR_NAME="F", GIT_AUTHOR_EMAIL="f@example.invalid",
           GIT_COMMITTER_NAME="F", GIT_COMMITTER_EMAIL="f@example.invalid",
           GIT_AUTHOR_DATE="@1790000000 +0000", GIT_COMMITTER_DATE="@1790000000 +0000",
           LC_ALL="C")


def git(*args):
    p = subprocess.run(["git", "-c", "commit.gpgsign=false", *args], env=ENV,
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"git {args}: {p.stderr}")
    return p.stdout.strip()


def put(name, text, msg):
    with open(name, "w") as fh:
        fh.write(text)
    git("add", "-A"); git("commit", "-qm", msg)
    return git("rev-parse", "HEAD")


def empty_net_delta():
    git("init", "-q", "-b", "main")
    put("f", "1\n", "O")
    git("checkout", "-qb", "pr")
    a = put("f", "2\n", "A")
    git("revert", "--no-edit", "HEAD"); r = git("rev-parse", "HEAD")
    git("checkout", "-q", "main")
    put("g", "unrelated\n", "target advance")
    git("cherry-pick", a); git("cherry-pick", r)


def criss_cross():
    git("init", "-q", "-b", "main")
    o = put("f", "1\n", "O")
    git("checkout", "-qb", "x"); x1 = put("x", "x\n", "X1")
    git("checkout", "-qb", "y", o); y1 = put("y", "y\n", "Y1")
    git("checkout", "-q", "x"); git("merge", "-q", "--no-ff", "-m", "X2", y1)
    git("checkout", "-q", "y"); git("merge", "-q", "--no-ff", "-m", "Y2", x1)
    git("checkout", "-qb", "pr", "x"); a = put("f", "2\n", "A")
    git("checkout", "-q", "-B", "main", "y"); git("cherry-pick", a)


def run(checker):
    p = subprocess.run([sys.executable, "-B", "-I", checker, "--no-fetch", "--base",
                        "main", "pr", "--current-retention"], env=ENV,
                       capture_output=True, text=True)
    return p.returncode, [l.strip() for l in p.stdout.splitlines() if l.strip()][:2]


def main():
    if os.path.isdir(ROOT):
        shutil.rmtree(ROOT)
    bad = 0
    for name, build in (("empty-net-delta", empty_net_delta), ("criss-cross-base", criss_cross)):
        repo = os.path.join(ROOT, name)
        os.makedirs(repo); os.chdir(repo)
        build()
        bases = git("merge-base", "--all", "main", "pr").split()
        h = run(HEAD); m = run(MUTANT)
        ok = h[0] == 1 and any(l.startswith("UNKNOWN") for l in h[1])
        bad += not ok
        print(f"{name}: pr={git('rev-parse', 'pr')[:10]} main={git('rev-parse', 'main')[:10]} "
              f"merge-bases={len(bases)}")
        print(f"  head   rc={h[0]} {h[1]}")
        print(f"  mutant rc={m[0]} {m[1]}")
    print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
