#!/usr/bin/env python3
"""Reviewer probe: an off-pin or modified tsn-c-stack must be refused before the F5 gap check builds and
before the milan_dp counter targets (counters, counters-f5, counters-mutants) and the aggregate run reach
their recipes. Every scenario uses a scratch clone of the stack; the milan_dp directory is mirrored (files
copied, every other checkout entry symlinked) so the Makefile's relative paths resolve; Verilator is a
recorder that writes a marker and builds nothing; TMPDIR is a fresh empty directory per run, so any
staging by stream_counters.py or stream_counter_f5.py is visible. One clean control shows the clone
mechanism accepts a pinned clone (F5 --build-only BUILT).

Usage: python3 -I probe_pin_order.py --root <checkout> --work <scratch dir>
Prints one line per (scenario, entry point) and exits 0 only if every expectation holds."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

RECORDER = """#!/bin/sh
echo "$@" >> "$PROBE_MARK"
exit 1
"""


def sh(argv, cwd=None, env=None, timeout=1800):
    r = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def mirror(root: Path, rel: str, into: Path) -> Path:
    if into.exists():
        shutil.rmtree(into)
    here, there = root, into
    for part in Path(rel).parts:
        there.mkdir(parents=True, exist_ok=True)
        for entry in here.iterdir():
            if entry.name != part:
                (there / entry.name).symlink_to(entry)
        here, there = here / part, there / part
    rc, out = sh(["git", "-C", str(here), "ls-files", "-z", "--cached", "."])
    assert rc == 0, out
    for name in filter(None, out.split("\0")):
        if (here / name).is_file():
            (there / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(here / name, there / name)
    return there


def clone(root: Path, work: Path, pin: str) -> Path:
    path = work / "stack-clone"
    if path.exists():
        shutil.rmtree(path)
    rc, out = sh(["git", "clone", "--quiet", "--no-hardlinks", str(root / "third_party/tsn-c-stack"), str(path)])
    assert rc == 0, out
    rc, out = sh(["git", "-C", str(path), "-c", "advice.detachedHead=false", "checkout", "--quiet", pin])
    assert rc == 0, out
    return path


def spoil(path: Path, how: str) -> None:
    if how == "clean":
        return
    if how == "wire-poisoned":
        w = path / "include/wire.h"
        w.write_text(w.read_text() + "\n#error PROBE-POISON compiled\n")
    elif how == "off-pin":
        rc, out = sh(["git", "-C", str(path), "checkout", "--quiet", "HEAD~1"])
        assert rc == 0, out
    elif how == "adp-edited":
        a = path / "src/adp.c"
        a.write_text(a.read_text() + "\n")
    elif how == "header-added":
        (path / "include/probe_added.h").write_text("/* added */\n")
    else:
        raise ValueError(how)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    a = ap.parse_args()
    root, work = a.root.resolve(), a.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    pin = sh(["git", "-C", str(root), "rev-parse", "HEAD:third_party/tsn-c-stack"])[1].strip()
    recorder = work / "recorder.sh"
    recorder.write_text(RECORDER)
    recorder.chmod(0o755)
    f5 = root / "tb/verilator/milan_dp/stream_counter_f5.py"
    bad = 0
    rows = []

    def env_for(tag):
        tmp = work / f"tmp-{tag}"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir()
        mark = work / f"mark-{tag}"
        if mark.exists():
            mark.unlink()
        e = dict(os.environ, TMPDIR=str(tmp), PROBE_MARK=str(mark), PYTHONDONTWRITEBYTECODE="1")
        e.pop("MAKEFLAGS", None)
        return e, tmp, mark

    # Clean control: F5 build-only against a pinned clone builds.
    stack = clone(root, work, pin)
    e, tmp, mark = env_for("clean-f5-build-only")
    rc, out = sh([sys.executable, "-B", str(f5), "--stack", str(stack), "--shape", "1", "--build-only",
                  "--work", str(work / "f5work-clean")], env=e)
    ok = rc == 0 and "F5 1x1: BUILT" in out and f"tsn-c-stack at {pin}" in out
    rows.append(("clean", "stream_counter_f5.py --build-only --shape 1", rc, "BUILT" if ok else out[-300:], ok))

    for how in ("wire-poisoned", "off-pin", "adp-edited", "header-added"):
        # F5 directly: refused (rc 2, REFUSED) before its work directory is created and before any compile.
        for extra in (["--shape", "1"], ["--shape", "8"], ["--shape", "1", "--build-only"],
                      ["--variant", "late"]):
            stack = clone(root, work, pin)
            spoil(stack, how)
            tag = f"{how}-f5-{'-'.join(x.strip('-') for x in extra)}"
            e, tmp, mark = env_for(tag)
            fw = work / f"f5work-{tag}"
            if fw.exists():
                shutil.rmtree(fw)
            rc, out = sh([sys.executable, "-B", str(f5), "--stack", str(stack), *extra, "--work", str(fw)], env=e)
            staged = fw.exists() or any(tmp.iterdir())
            ok = rc == 2 and "REFUSED:" in out and not staged and "PROBE-POISON" not in out
            rows.append((how, "stream_counter_f5.py " + " ".join(extra), rc,
                         next((ln for ln in out.splitlines() if "REFUSED" in ln), out[-200:])[:160]
                         + (" [STAGED]" if staged else ""), ok))
        # Makefile targets in a mirrored milan_dp, serial and -j16.
        for target, jobs in (("counters", "1"), ("counters-f5", "1"), ("counters-mutants", "1"),
                             ("counters-mutants", "16"), ("counters-f5", "16"), ("run", "1")):
            stack = clone(root, work, pin)
            spoil(stack, how)
            tag = f"{how}-make-{target}-j{jobs}"
            m = mirror(root, "tb/verilator/milan_dp", work / f"mirror-{tag}")
            e, tmp, mark = env_for(tag)
            rc, out = sh(["make", "--no-print-directory", "-C", str(m), f"-j{jobs}", f"STACK_DIR={stack}",
                          f"VERILATOR={recorder}", target], env=e, timeout=900)
            recipe_ran = ("stream_counters.py" in out.split("REFUSED")[-1] or "stream_counter_f5.py --stack"
                          in out.split("REFUSED")[-1]) if "REFUSED" in out else True
            staged = any(tmp.iterdir())
            verilated = mark.exists()
            # For `run`, RTL prerequisites listed after stack-pin are not reached serially.
            ok = rc != 0 and "REFUSED:" in out and not staged and not verilated and "PROBE-POISON" not in out \
                and not recipe_ran
            rows.append((how, f"make -j{jobs} {target}", rc,
                         next((ln for ln in out.splitlines() if "REFUSED" in ln), out[-200:])[:160]
                         + (" [STAGED]" if staged else "") + (" [VERILATOR RAN]" if verilated else "")
                         + (" [RECIPE RAN]" if recipe_ran else ""), ok))
            shutil.rmtree(m, ignore_errors=True)
    for how, entry, rc, said, ok in rows:
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} {how:14s} {entry:48s} rc={rc} {said}")
    print(f"probe_pin_order: {len(rows)} cases, {bad} unexpected")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
