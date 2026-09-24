#!/usr/bin/env python3
"""Reproduce #514 fixture 30 (and its sibling 31) plus a linear-patch-fallback
replica, then run a checker tree with and without --current-retention.

    python3 -B repro_fixtures.py R242_FIXTURES_PY CHECKER_SCRIPTS_DIR WORK_DIR

R242_FIXTURES_PY is the immutable R242 fixture builder (extract it with
`git show badb350c0892fd5a6c771f24943463c9b1440c24:readiness-evidence/423/design/R242/scripts/fixtures.py`).
Its scenario builders are reused unchanged; TICK is reset per scenario exactly
as its own main() does, so object IDs reproduce for the same Git.
Prints one line per scenario/invocation: heads, exit code and verdict lines.
"""
import os
import subprocess
import sys

FIXTURES, SCRIPTS, WORK = (os.path.abspath(a) for a in sys.argv[1:4])
CHECKER = os.path.join(SCRIPTS, "check_merge_containment.py")

namespace = {"__name__": "r242_fixtures"}
saved_argv = sys.argv
sys.argv = ["fixtures.py", "unused", "unused", "unused", "unused"]
with open(FIXTURES, encoding="utf-8") as handle:
    exec(compile(handle.read(), FIXTURES, "exec"), namespace)
sys.argv = saved_argv
os.environ.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)


def run(branch, base, extra):
    p = subprocess.run([sys.executable, "-B", "-I", CHECKER, "--no-fetch",
                        "--base", base, branch, *extra], capture_output=True,
                       text=True, env=dict(namespace["BASE_ENV"]))
    lines = [line.rstrip() for line in p.stdout.splitlines() if line.strip()]
    return p.returncode, lines, p.stderr.strip()


def patch_fallback_replica():
    """Replica of merge_containment_selftest_content.py linear-patch-fallback."""
    git, write = namespace["git"], namespace["write"]
    git("init", "-q", "-b", "base")
    write("seed", "seed\n")
    git("add", "seed"); git("commit", "-qm", "seed")
    git("checkout", "-qb", "linear-feature", "base")
    write("linear", "landed\n")
    git("add", "linear"); git("commit", "-qm", "linear")
    linear_commit = git("rev-parse", "HEAD")
    git("checkout", "-qb", "linear-base", "base")
    write("advance", "first")
    git("add", "advance"); git("commit", "-qm", "advance")
    git("cherry-pick", linear_commit)
    with open("linear", "a") as handle:
        handle.write("superseded\n")
    git("add", "linear"); git("commit", "-qm", "supersede")


SCENARIOS = [
    ("fixture-30 linear-control-exact-revert", namespace["s_linear_revert_control"], "pr", "main"),
    ("fixture-31 linear-control-adjacent-extension", namespace["s_linear_extension_control"], "pr", "main"),
    ("linear-patch-fallback replica", patch_fallback_replica, "linear-feature", "linear-base"),
]

os.makedirs(WORK, exist_ok=False)
for name, build, branch, base in SCENARIOS:
    repo = os.path.join(WORK, name.split()[0])
    os.makedirs(repo)
    os.chdir(repo)
    namespace["TICK"][0] = 1790000000
    build()
    git = namespace["git"]
    print(f"== {name}: source {git('rev-parse', branch)} target {git('rev-parse', base)}")
    for extra in ([], ["--current-retention"]):
        rc, lines, err = run(branch, base, extra)
        print(f"   args={extra or ['(default)']} exit={rc}")
        for line in lines:
            print(f"     | {line}")
        if err:
            print(f"     stderr: {err}")
