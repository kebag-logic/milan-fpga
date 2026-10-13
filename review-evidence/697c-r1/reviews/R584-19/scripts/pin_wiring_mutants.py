#!/usr/bin/env python3
"""Reviewer mutation probe of round 20's pin wiring, in a DISPOSABLE copy of the checkout (argv[1]).
Each Makefile mutant is applied to tb/verilator/milan_dp/Makefile and judged by the gate's own
ctrl_pin.makefile_findings, then restored; each must yield a finding. The F5 mutant removes
stream_counter_f5.py's own pin check; F5 is then run against a stack clone with one line appended to
include/wire.h (the shape of the gate's own F5 pin arms) and must NOT print the refusal those arms require,
so the arms would fail. A clean run of each must give no finding / the refusal.
Usage: python3 -I pin_wiring_mutants.py <copy> <work>"""
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_pin  # noqa: E402

mk = root / "tb/verilator/milan_dp/Makefile"
orig = mk.read_text()
MUTANTS = {
    "clean": [],
    "counters unpinned": [("counters: | stack-pin\n", "counters:\n")],
    "counters-f5 unpinned": [("counters-f5: | stack-pin\n", "counters-f5:\n")],
    "counters-mutants unpinned": [("counters-mutants: | stack-pin\n", "counters-mutants:\n")],
    "counters-f5 unpinned and --stack dropped": [
        ("counters-f5: | stack-pin\n", "counters-f5:\n"),
        ("stream_counter_f5.py --stack $(STACK_DIR) --shape 1", "stream_counter_f5.py --shape 1"),
        ("stream_counter_f5.py --stack $(STACK_DIR) --shape 8", "stream_counter_f5.py --shape 8")],
    "counters-mutants unpinned and --stack dropped": [
        ("counters-mutants: | stack-pin\n", "counters-mutants:\n"),
        ("stream_counter_f5.py --stack $(STACK_DIR) --variant", "stream_counter_f5.py --variant")],
    "run without stack-pin": [("run: stack-pin ltn_rom.hex", "run: ltn_rom.hex")],
}
bad = 0
try:
    for name, edits in MUTANTS.items():
        text = orig
        for old, new in edits:
            n = text.count(old)
            assert n >= 1, (name, old)
            text = text.replace(old, new)
        mk.write_text(text)
        found = ctrl_pin.makefile_findings([mk], work / name.replace(" ", "_"))
        ok = (not found) if name == "clean" else bool(found)
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} makefile mutant [{name}]: {len(found)} finding(s): {'; '.join(found)[:300]}")
finally:
    mk.write_text(orig)

# F5 without its own pin check, against an edited clone.
f5 = root / "tb/verilator/milan_dp/stream_counter_f5.py"
f5_orig = f5.read_text()
clone = work / "stack-clone"
if clone.exists():
    shutil.rmtree(clone)
pin = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD:third_party/tsn-c-stack"], capture_output=True,
                     text=True, check=True).stdout.strip()
subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(root / "third_party/tsn-c-stack"), str(clone)],
               check=True)
subprocess.run(["git", "-C", str(clone), "-c", "advice.detachedHead=false", "checkout", "--quiet", pin], check=True)
wire = clone / "include/wire.h"
wire.write_text(wire.read_text() + "\n")
needle = "tsn-c-stack differs from the pinned"
try:
    for name, text in (("F5 as shipped", f5_orig),
                       ("F5 without its pin check", f5_orig.replace(
                           'print(f"tsn-c-stack at {stack_pin(stack)}", flush=True)',
                           'print("tsn-c-stack at (pin check removed)", flush=True)'))):
        assert name == "F5 as shipped" or text != f5_orig
        f5.write_text(text)
        r = subprocess.run([sys.executable, "-B", str(f5), "--stack", str(clone), "--shape", "1", "--build-only",
                            "--work", str(work / ("f5-" + name.replace(" ", "_")))],
                           capture_output=True, text=True, timeout=900)
        said = needle in r.stdout + r.stderr
        ok = said if name == "F5 as shipped" else not said
        bad += not ok
        print(f"{'OK ' if ok else 'BAD'} [{name}] vs wire.h+newline clone: rc={r.returncode}, "
              f"pin-arm needle {'present' if said else 'ABSENT (the gate arm would fail)'}; "
              f"last line: {(r.stdout + r.stderr).strip().splitlines()[-1][:160]}")
finally:
    f5.write_text(f5_orig)
print(f"pin_wiring_mutants: {len(MUTANTS) + 2} cases, {bad} unexpected")
sys.exit(1 if bad else 0)
