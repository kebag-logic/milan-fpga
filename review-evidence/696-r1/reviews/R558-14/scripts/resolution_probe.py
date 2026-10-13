#!/usr/bin/env python3
"""Resolution probe: run the merged differential's self-test with one intent of the merge removed at run time.

  drop-rtl   - differential() ignores its rtl argument (696's Annex B RTL plant would lose its source)
  drop-stack - differential() ignores its stack argument and builds the pinned submodule (697c's planted stack copy)
Usage: resolution_probe.py <repo> <mode> <workdir>. Nothing in <repo> is written. Exit 0 iff the self-test FAILS
with exactly the expected escapes, i.e. the self-test detects the lost intent."""
import contextlib, io, sys
from pathlib import Path

repo, mode, work = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import maap_differential as md  # noqa: E402

real = md.differential
if mode == "drop-rtl":
    md.differential = lambda out, ctrl=md.CTRL, stack=md.STACK, rtl=None: real(out, ctrl, stack)
    expect = {"parent-ignores-mac"}
elif mode == "drop-stack":
    md.differential = lambda out, ctrl=md.CTRL, stack=md.STACK, rtl=None: real(out, ctrl, md.STACK, rtl)
    expect = {"wire", "release", "probe-1ms", "probe-500ms", "probe-600ms",
              *(f"maap-table-b7-{k}" for k in (0, 1, 2, 6, 7, 8, 12, 13, 14))}
else:
    sys.exit(f"unknown mode {mode}")
print(f"tsn-c-stack at {md.stack_pin(md.STACK)}", flush=True)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = md.sensitivity(work / "mutants", md.STACK)
lines = [ln for ln in buf.getvalue().splitlines() if "differential mutant" in ln]
print("\n".join(lines))
escaped = {ln.split("differential mutant ", 1)[1].split(":", 1)[0] for ln in lines if ln.startswith("[ESCAPED]")}
print(f"mode={mode} self-test rc={rc} escaped={sorted(escaped)} expected={sorted(expect)}")
ok = rc == 1 and escaped == expect
print("PROBE DETECTED" if ok else "PROBE NOT AS EXPECTED")
sys.exit(0 if ok else 1)
