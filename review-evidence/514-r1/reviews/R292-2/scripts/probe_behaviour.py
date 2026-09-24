#!/usr/bin/env python3
"""Behaviour probes for the optional linear retention arm (PR #552, #514).

    python3 -B probe_behaviour.py CHECKER_SCRIPTS_DIR WORK_DIR

Each scenario builds a fresh deterministic repository under WORK_DIR and runs
the real CLI. Prints scenario, exit and the verdict lines. Expectations are
written beside each scenario; the last line is PROBES PASS or PROBES FAIL(n).
"""
import os
import subprocess
import sys

SCRIPTS, WORK = (os.path.abspath(a) for a in sys.argv[1:3])
CHECKER = os.path.join(SCRIPTS, "check_merge_containment.py")
ENV = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
           GIT_AUTHOR_NAME="Probe", GIT_AUTHOR_EMAIL="probe@example.invalid",
           GIT_COMMITTER_NAME="Probe", GIT_COMMITTER_EMAIL="probe@example.invalid",
           GIT_AUTHOR_DATE="@1790000000 +0000", GIT_COMMITTER_DATE="@1790000000 +0000",
           LC_ALL="C")
MOD = "".join(f"line {i:02d}\n" for i in range(1, 41))


TICK = [1790000000]


def git(*args):
    TICK[0] += 60
    env = dict(ENV, GIT_AUTHOR_DATE=f"@{TICK[0]} +0000",
               GIT_COMMITTER_DATE=f"@{TICK[0]} +0000")
    p = subprocess.run(["git", "-c", "commit.gpgsign=false", *args], env=env,
                       capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"git {args}: {p.stderr}")
    return p.stdout.strip()


def write(path, text):
    with open(path, "w") as handle:
        handle.write(text)


def commit(msg):
    git("add", "-A")
    git("commit", "-q", "--allow-empty", "-m", msg)
    return git("rev-parse", "HEAD")


def edit(old, new, path="mod.txt"):
    with open(path) as handle:
        text = handle.read()
    write(path, text.replace(old, new, 1))


def seed():
    git("init", "-q", "-b", "main")
    write("mod.txt", MOD)
    return commit("O")


def run(*args):
    p = subprocess.run([sys.executable, "-B", "-I", CHECKER, *args],
                       capture_output=True, text=True, env=ENV)
    lines = [line.strip() for line in p.stdout.splitlines()
             if line.startswith("  ") and line.split()[0] in
             ("contained", "retained", "UNKNOWN", "STRANDED")]
    return p.returncode, lines, p.stderr.strip().splitlines()[:1]


def net_zero():
    """Source changes then reverts one line; both commits replayed exactly."""
    o = seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); a = commit("A")
    edit("line 05 x\n", "line 05\n"); b = commit("B")
    git("checkout", "-q", "main")
    git("cherry-pick", a); git("cherry-pick", b)
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def criss_cross():
    """Linear replay is exact, but the source/target have two merge bases."""
    o = seed()
    git("checkout", "-q", "-b", "x"); write("x", "x\n"); x = commit("X")
    git("checkout", "-q", "-b", "y", o); write("y", "y\n"); y = commit("Y")
    git("checkout", "-q", "-b", "pr", x)
    git("merge", "-q", "--no-ff", "-m", "pr merges y", "y")
    edit("line 05\n", "line 05 pr\n"); c = commit("C")
    git("checkout", "-q", "main"); git("reset", "-q", "--hard", y)
    git("merge", "-q", "--no-ff", "-m", "main merges x", "x")
    git("cherry-pick", c)
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def criss_cross_linear():
    """Criss-cross where the source-only range is linear (no source merge)."""
    o = seed()
    git("checkout", "-q", "-b", "x"); write("x", "x\n"); x = commit("X")
    git("checkout", "-q", "-b", "y", o); write("y", "y\n"); y = commit("Y")
    git("checkout", "-q", "-b", "m1", x)
    git("merge", "-q", "--no-ff", "-m", "m1", "y")
    git("checkout", "-q", "-b", "m2", y)
    git("merge", "-q", "--no-ff", "-m", "m2", "x")
    git("checkout", "-q", "-b", "pr", "m1")
    edit("line 05\n", "line 05 pr\n"); c = commit("C")
    git("checkout", "-q", "-b", "tgt", "m2")
    # main has m1 merged in as well so m1 is shared; pr..main has only replay
    git("checkout", "-q", "main"); git("reset", "-q", "--hard", "m2")
    git("cherry-pick", c)
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def stranded():
    seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); commit("A")
    git("checkout", "-q", "main"); edit("line 30\n", "line 30 y\n"); commit("L")
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def squash():
    seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); commit("A")
    edit("line 20\n", "line 20 x\n"); commit("B")
    git("checkout", "-q", "main"); git("merge", "-q", "--squash", "pr"); commit("squash")
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def ancestry():
    seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); commit("A")
    git("checkout", "-q", "main"); git("merge", "-q", "--no-ff", "-m", "M", "pr")
    return ["--no-fetch", "--base", "main", "pr"]


def ancestry_opt():
    return ancestry() + ["--current-retention"]


def rename_reverted():
    seed(); write("keep.txt", "keep\n"); commit("K")
    git("checkout", "-q", "-b", "pr")
    git("mv", "keep.txt", "moved.txt"); a = commit("rename")
    git("checkout", "-q", "main"); git("cherry-pick", a)
    git("mv", "moved.txt", "keep.txt"); commit("undo rename")
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def rename_retained():
    seed(); write("keep.txt", "keep\n"); commit("K")
    git("checkout", "-q", "-b", "pr")
    git("mv", "keep.txt", "moved.txt"); a = commit("rename")
    git("checkout", "-q", "main"); git("cherry-pick", a)
    edit("line 35\n", "line 35 later\n"); commit("unrelated later")
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def hostile_attributes():
    """Exact revert under an 'ours' merge driver and quiet textconv."""
    seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); a = commit("A")
    git("checkout", "-q", "main"); git("cherry-pick", a)
    git("revert", "--no-edit", "HEAD")
    write(".gitattributes", "* merge=ours diff=quiet\n"); commit("attrs")
    git("config", "merge.ours.driver", "true")
    git("config", "diff.quiet.textconv", "true")
    return ["--no-fetch", "--base", "main", "pr", "--current-retention"]


def base_consumes_flag():
    seed()
    git("checkout", "-q", "-b", "pr")
    edit("line 05\n", "line 05 x\n"); a = commit("A")
    git("checkout", "-q", "main"); git("cherry-pick", a)
    return ["--no-fetch", "--base", "--current-retention", "main", "pr"]


def option_alone():
    seed()
    return ["--no-fetch", "--current-retention"]


# name, builder, expected exit, expected verdict words
SCENARIOS = [
    ("net-zero-source-delta", net_zero, 1, ["contained", "UNKNOWN"]),
    ("criss-cross-source-merge", criss_cross, 1, None),
    ("criss-cross-linear-two-bases", criss_cross_linear, 1, ["contained", "UNKNOWN"]),
    ("stranded-with-option", stranded, 1, ["STRANDED"]),
    ("squash-path-arm-with-option", squash, 1, ["contained", "UNKNOWN"]),
    ("ancestry-default", ancestry, 0, ["contained"]),
    ("ancestry-with-option", ancestry_opt, 1, ["contained", "UNKNOWN"]),
    ("rename-reverted", rename_reverted, 1, ["contained", "UNKNOWN"]),
    ("rename-retained", rename_retained, 0, ["contained", "retained"]),
    ("hostile-attributes-revert", hostile_attributes, 1, ["contained", "UNKNOWN"]),
    ("base-flag-then-option", base_consumes_flag, None, None),
    ("option-without-target", option_alone, None, None),
]

os.makedirs(WORK, exist_ok=False)
bad = 0
for name, build, want_rc, want_words in SCENARIOS:
    repo = os.path.join(WORK, name)
    os.makedirs(repo)
    os.chdir(repo)
    TICK[0] = 1790000000
    args = build()
    rc, lines, err = run(*args)
    words = [line.split()[0] for line in lines]
    ok = ((want_rc is None or rc == want_rc)
          and (want_words is None or words == want_words))
    bad += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name} args={args} exit={rc} words={words}"
          f" expect=({want_rc}, {want_words})")
    for line in lines:
        print(f"     | {line}")
    if err:
        print(f"     stderr: {err[0][:200]}")
print("PROBES PASS" if not bad else f"PROBES FAIL({bad})")
