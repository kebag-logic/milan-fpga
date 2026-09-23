#!/usr/bin/env python3
"""Probe every clause of the new fixture_guards.main() docstring against behaviour.

Usage: probe_main_contract.py <tree>/tb/pp_top

Imports fixture_guards from the given directory (an extracted copy of the head
tree, never the review clone) and exercises main() with mocked compiler results
and with small fake executables. Each arm prints OBSERVED behaviour and whether
it matches the docstring's claim. Exit 0 when every arm matched the claim it
checks; the arms tagged INFO record behaviour the docstring does not state.
"""

import contextlib
import io
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

WIRE = "SRP VID fixture must differ from product default 2 in the 16-bit wire value"
CLASS_D = "SRP VID fixture must differ from product default 2 in the 12-bit class-D value"
GOOD = [(0, ""), (0, ""),
        (1, f"b:1: error: static assertion failed: {WIRE}\nb:2: error: static assertion failed: {CLASS_D}\n"),
        (1, f"b:1: error: static assertion failed: {CLASS_D}\n")]
ARGV = ["fixture_guards.py", "--verilator", "v", "--cxx", "c++", "--", "--cc", "x.sv"]


def run_mocked(fg, compiles, argv=ARGV):
    results = [subprocess.CompletedProcess([], 0)]
    results += [subprocess.CompletedProcess([], rc, out) for rc, out in compiles]
    buf = io.StringIO()
    with patch("sys.argv", argv), \
            patch.object(fg.subprocess, "check_output", return_value="/r\n"), \
            patch.object(fg.subprocess, "run", side_effect=results) as run, \
            contextlib.redirect_stdout(buf):
        rv = fg.main()
    return rv, buf.getvalue(), run.call_count


def fake_exe(d: Path, name: str, body: str) -> str:
    p = d / name
    p.write_text("#!/bin/sh\n" + body + "\n")
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return str(p)


def call_real(fg, argv):
    buf = io.StringIO()
    try:
        with patch("sys.argv", argv), contextlib.redirect_stdout(buf), \
                contextlib.redirect_stderr(io.StringIO()):
            return f"returned {fg.main()}", buf.getvalue()
    except BaseException as e:  # noqa: BLE001 - classifying what escapes main()
        return f"raised {type(e).__name__}", buf.getvalue()


def main() -> int:
    sys.path.insert(0, sys.argv[1])
    os.chdir(sys.argv[1])
    import fixture_guards as fg
    ok = True

    def check(name, cond, detail):
        nonlocal ok
        ok &= cond
        print(f"[{'MATCH' if cond else 'MISMATCH'}] {name}: {detail}")

    rv, out, n = run_mocked(fg, GOOD)
    check("0 = all four PASS", rv == 0 and out.endswith("fixture guards: 4 cases PASS\n") and n == 5,
          f"rv={rv} calls={n} last={out.splitlines()[-1]!r}")
    print("  annotation: type(rv) is", type(rv).__name__)

    bad = [(1, "")] + GOOD[1:]  # exit status differs, no error line
    rv, out, n = run_mocked(fg, bad)
    check("exit status differs -> 1 after printing output", rv == 1 and "FAIL: fixture default" in out,
          f"rv={rv} calls={n} out={out!r}")

    bad = GOOD[:2] + [(1, f"b:1: error: static assertion failed: {WIRE}\nb:2: error: unrelated\n")] + GOOD[3:]
    rv, out, n = run_mocked(fg, bad)
    check("static-assertion diagnostics differ -> 1", rv == 1 and "FAIL: fixture 0002" in out and "unrelated" in out,
          f"rv={rv} calls={n}")

    bad = GOOD[:3] + [(1, f"b:1: error: static assertion failed: {CLASS_D}\nb:9: error: unrelated\n")]
    rv, out, n = run_mocked(fg, bad)
    check("error count differs -> 1", rv == 1 and "FAIL: fixture 1002" in out and "unrelated" in out,
          f"rv={rv} calls={n}")

    bad = GOOD[:1] + [(0, "b:1: warning: w\n")] + GOOD[2:]
    rv, out, n = run_mocked(fg, bad)
    check("warnings alone do not fail (error count only)", rv == 0, f"rv={rv}")

    bad = [(1, "")] + GOOD[1:]
    rv, out, n = run_mocked(fg, bad)
    print(f"[INFO] first mismatch returns immediately: compiler calls made = {n - 1} of 4")

    with tempfile.TemporaryDirectory(prefix="r261-fake-") as t:
        d = Path(t)
        root_fail = fake_exe(d, "v_rootfail", "exit 7")
        r, _ = call_real(fg, ["fg", "--verilator", root_fail, "--", "--cc"])
        check("failed VERILATOR_ROOT query (non-zero exit) raises CalledProcessError",
              r == "raised CalledProcessError", r)
        gen_fail = fake_exe(d, "v_genfail", 'if [ "$1" = --getenv ]; then echo /r; exit 0; fi; exit 3')
        r, _ = call_real(fg, ["fg", "--verilator", gen_fail, "--", "--cc"])
        check("failed model generation (non-zero exit) raises CalledProcessError",
              r == "raised CalledProcessError", r)
        r, _ = call_real(fg, ["fg", "--verilator", str(d / "absent-verilator"), "--", "--cc"])
        print(f"[INFO] verilator executable absent: {r} (docstring names only CalledProcessError)")
        gen_ok = fake_exe(d, "v_ok", 'if [ "$1" = --getenv ]; then echo /r; exit 0; fi; exit 0')
        r, _ = call_real(fg, ["fg", "--verilator", gen_ok, "--cxx", str(d / "absent-cxx"), "--", "--cc"])
        print(f"[INFO] compiler executable absent: {r} (docstring: returns 1 on a case mismatch)")
        r, _ = call_real(fg, ["fg", "--verilator", gen_ok, "--bogus", "--", "--cc"])
        print(f"[INFO] unknown option before --: {r}")
        rec = fake_exe(d, "v_rec", f'if [ "$1" = --getenv ]; then echo /r; exit 0; fi; echo "$@" > {d}/args; exit 0')
        call_real(fg, ["fg", "--verilator", rec, "--cxx", "false", "--", "--cc", "-Wall", "x.sv"])
        print(f"[INFO] flags after -- reach model generation as: {(d / 'args').read_text().strip()!r}")
        (d / "args").unlink(missing_ok=True)
        r, _ = call_real(fg, ["fg", "--verilator", rec, "--cxx", "false", "--cc", "x.sv"])
        seen = (d / "args").read_text().strip() if (d / "args").exists() else "(model generation not reached)"
        print(f"[INFO] flags WITHOUT --: {r}; model generation args: {seen!r}")

    print("MAIN CONTRACT PROBE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
