#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""split_parallel.py - the split leg under make -j8, from a clean tree (#665).

`make split` builds the split leg's binary (build-split) and runs it (exec-split). Under a parallel make the
run must not start before the binary has linked (#665), so the rule runs
exec-split in a make of its own once build-split is done. This gate clones the checkout's committed HEAD into
a scratch directory, each submodule the leg reads at its gitlink and taken from the checkout's own clone of
it, and runs make -j8 split there. It passes when make exits 0 and the leg prints its own verdict with no
failure ("failures: 0").

--selftest first proves the gate can fail for the race: in another clean tree the split rule is planted as the
race had it (split: build-split exec-split, the run a prerequisite beside the build), and make -j8 split there
must fail with the binary missing. The planted run has no prerequisite and the build takes minutes, so the run
starts long before the link. Then the real run, with HEAD's rule, must pass.

  python3 tb/verilator/milan_dp/split_parallel.py [--selftest] [--keep] [MAKE ARGUMENT ...]

The make arguments are handed to make after -j8 split, e.g. VERILATOR=... VERILATOR_JOBS=8. Exit 0 = every
run gave its verdict; 1 = a run did not; 2 = no clean tree could be made.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LEG = HERE.relative_to(ROOT)
#: the submodules the leg reads, as the hosted suite jobs fetch them: the AXI-Stream FIFOs, both processors'
#: sources and generators, and the stack its pin check proves
SUBMODULES = ("third_party/verilog-axis", "protocol-processor", "gptp-processor", "third_party/tsn-c-stack")
#: HEAD's split rule, and the race's (the run beside the link it needs), which --selftest plants
RULE = "split: build-split\n\t$(MAKE) --no-print-directory exec-split\n"
RACE = "split: build-split exec-split\n"
#: the leg's verdict line, its failure count in group 1
VERDICT = re.compile(r"^checks: \d+\s+failures: (\d+)$", re.MULTILINE)
#: what the race leaves in make's output: the run started before the binary existed
MISSING = "Vmilan_dp_split: No such file or directory"


class NoTree(Exception):
    """A clean tree could not be made."""


def git(*args: str, cwd: Path) -> str:
    """Run git in `cwd`; its output, or NoTree naming the command."""
    done = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        raise NoTree(f"git {' '.join(args)} in {cwd}: {done.stderr.strip()}")
    return done.stdout.strip()


def clean_tree(where: Path) -> Path:
    """A clone of the checkout's HEAD at `where`, each of SUBMODULES at its gitlink from the checkout's own clone
    of it, its origin the URL .gitmodules declares; nothing in it built."""
    head = git("rev-parse", "HEAD", cwd=ROOT)
    git("clone", "--quiet", "--no-checkout", str(ROOT), str(where), cwd=ROOT)
    git("-c", "advice.detachedHead=false", "checkout", "--quiet", "--detach", head, cwd=where)
    declared = dict(line.split()[::-1] for line in
                    git("config", "--file", ".gitmodules", "--get-regexp", r"^submodule\..*\.path$",
                        cwd=where).splitlines())
    for path in SUBMODULES:
        if path not in declared or not (ROOT / path / ".git").exists():
            raise NoTree(f"{path}: not a submodule .gitmodules declares, or the checkout has no clone of it")
        url = declared[path].removesuffix(".path") + ".url"
        origin = git("config", "--file", ".gitmodules", url, cwd=where)
        git("submodule", "init", "--", path, cwd=where)
        git("config", url, str(ROOT / path), cwd=where)
        git("-c", "protocol.file.allow=always", "submodule", "update", "--quiet", "--", path, cwd=where)
        git("remote", "set-url", "origin", origin, cwd=where / path)
    if git("status", "--porcelain", cwd=where):
        raise NoTree(f"the clone at {where} is not clean")
    return where


def run_split(tree: Path, extra: list[str]) -> tuple[int, str]:
    """make -j8 split in the tree's leg directory: make's exit status and its output."""
    done = subprocess.run(["make", "-C", str(tree / LEG), "-j8", "split", *extra], capture_output=True, text=True,
                          check=False)
    return done.returncode, done.stdout + done.stderr


def passed(rc: int, output: str) -> bool:
    """make exited 0 and the leg's every verdict line counts no failure."""
    verdicts = VERDICT.findall(output)
    return rc == 0 and bool(verdicts) and all(v == "0" for v in verdicts)


def arm(name: str, tree: Path, extra: list[str], expect_pass: bool) -> bool:
    """One run of the gate: its verdict as expected, with the lines it judged (the leg's verdict, or the missing
    binary), and make's last lines when it is not."""
    rc, output = run_split(tree, extra)
    ok = passed(rc, output) if expect_pass else rc != 0 and MISSING in output
    want = "passes" if expect_pass else f"fails with \"{MISSING}\""
    print(f"split_parallel: {name} at {git('rev-parse', 'HEAD', cwd=tree)}: make -j8 split rc {rc}, "
          f"{'as' if ok else 'NOT as'} expected ({want})", flush=True)
    for line in output.splitlines():
        if VERDICT.match(line) or MISSING in line:
            print(f"  {line}", flush=True)
    if not ok:
        print("\n".join(output.splitlines()[-30:]), flush=True)
    return ok


def selftest(work: Path, extra: list[str]) -> bool:
    """The race's rule, planted in a clean tree, refused: make -j8 split fails with the binary missing."""
    race = clean_tree(work / "race")
    makefile = race / LEG / "Makefile"
    text = makefile.read_text()
    if text.count(RULE) != 1:
        raise NoTree(f"{LEG / 'Makefile'} does not hold the split rule once, so its race cannot be planted")
    makefile.write_text(text.replace(RULE, RACE))
    return arm("selftest, the race's rule planted", race, extra, expect_pass=False)


def main() -> int:
    """Run the gate (and its self-test) in clean trees under a scratch directory."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true", help="first prove the gate fails for the race")
    parser.add_argument("--keep", action="store_true", help="keep the scratch directory and name it")
    parser.add_argument("make_args", nargs="*", help="handed to make after -j8 split")
    args = parser.parse_args()
    work = Path(tempfile.mkdtemp(prefix="split-parallel-"))
    try:
        ok = selftest(work, args.make_args) if args.selftest else True
        ok = arm("make -j8 split from a clean tree", clean_tree(work / "tree"), args.make_args, True) and ok
    except NoTree as refused:
        print(f"split_parallel: REFUSED: {refused}", flush=True)
        return 2
    finally:
        if args.keep:
            print(f"split_parallel: kept {work}", flush=True)
        else:
            shutil.rmtree(work, ignore_errors=True)
    print(f"split_parallel: {'PASS' if ok else 'FAIL'}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
