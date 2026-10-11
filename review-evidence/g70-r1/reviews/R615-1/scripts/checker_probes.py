#!/usr/bin/env python3
"""Reviewer probes of syn/ooc/check_ooc_clock.py at PR #79 head.

usage: python3 -I checker_probes.py TREE WORKDIR
TREE    exported exact-head tree (read only; never modified)
WORKDIR disposable directory for planted copies

Part A  rule-disable mutation sweep: each finding of the checker is
        suppressed in a copy; the copy's --selftest must fail by name.
Part B  arm attribution: for every selftest arm, which findings fire.
Part C  static plants through `make ooc` with a stub Vivado that exits 3,
        so a run that reaches Vivado is visible as STUB VIVADO REACHED.
Part D  gap probes the issue does not require (reported, not gated).
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
CHECK = TREE / "syn/ooc/check_ooc_clock.py"
SRC = CHECK.read_text(encoding="utf-8")
WORK.mkdir(parents=True, exist_ok=True)
results: list[tuple[str, str, bool]] = []


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def record(part, label, ok, detail):
    results.append((part, label, ok))
    print(f"[{part}] {'OK  ' if ok else 'FAIL'} {label}")
    for line in detail.strip().splitlines()[:8]:
        print(f"        {line}")


# ---- Part A: suppress each finding -------------------------------------
# (id, exact source fragment, replacement)
MUTANTS = [
    ("R1 one synth_design", 'return [f"{name}: expected one synth_design, found {len(synth)}"]',
     "return []"),
    ("R2 read before synth", 'findings.append(f"{name}: {XDC} is not read before synth_design")\n    for line',
     "pass\n    for line"),
    ("R3 constraint after synth", 'findings.append(f"{name}:{line}: {words[0]} after synth_design")',
     "pass"),
    ("X1 one create_clock form", 'return [f"{path.name}: expected one create_clock -period -name [get_ports]"]',
     "return []"),
    ("X2 period and port", 'return [f"{path.name}: clock is {period} ns on {port}, "\n                f"expected {PERIOD_NS:.3f} ns on {CLOCK_PORT}"]',
     "return []"),
    ("L1 synth never started", 'return [f"{name}: synth_design never started"]', "return []"),
    ("L2 synth not completed", 'return [f"{name}: synth_design did not complete"]', "return []"),
    ("L3 read echo before synth", 'findings.append(f"{name}: {XDC} is not read before synth_design")\n    mapping',
     "pass\n    mapping"),
    ("L4 parse inside synth", 'findings.append(f"{name}: synth_design did not parse {XDC} before mapping")',
     "pass"),
    ("L5 constraint echo after synth", 'findings.append(f"{name}:{index + 1}: {echo.group(1)} after synth_design")',
     "pass"),
    # missing-file rules: not claimed as selftest-covered; recorded for scope
    ("M1 script missing (not claimed)", 'return [f"{name}: missing"]\n    commands', "return []\n    commands"),
    ("M2 xdc missing (not claimed)", 'return [f"{path.name}: missing"]', "return []"),
    ("M3 log missing (not claimed)", 'return [f"{name}: missing"]\n    lines', "return []\n    lines"),
]
mdir = WORK / "mutants"
mdir.mkdir(exist_ok=True)
rc, out = run([sys.executable, "-I", str(CHECK), "--selftest"])
record("A", "unmutated control selftest passes", rc == 0 and "PASS (17 arms)" in out, out)
for mid, frag, repl in MUTANTS:
    n = SRC.count(frag)
    if n != 1:
        record("A", f"{mid}: fragment not unique ({n})", False, "")
        continue
    path = mdir / (re.sub(r"\W+", "_", mid) + ".py")
    path.write_text(SRC.replace(frag, repl), encoding="utf-8")
    rc, out = run([sys.executable, "-I", str(path), "--selftest"])
    killed_by_name = rc != 0 and "escaped" in out and "Traceback" not in out
    if mid.startswith("M"):
        record("A", f"{mid}: rc={rc} (informational)", True, out)
    else:
        record("A", f"{mid}: killed by name rc={rc}", killed_by_name, out)

# ---- Part B: arm attribution -------------------------------------------
sys.path.insert(0, str(TREE / "syn/ooc"))
import check_ooc_clock as c  # noqa: E402

import tempfile  # noqa: E402

with tempfile.TemporaryDirectory(dir=WORK) as d:
    root = Path(d)
    (root / c.XDC).write_text(c.GOOD_XDC)
    for s in c.SCRIPTS:
        (root / s).write_text(c.GOOD_TCL)
    print("[B] clean fixture findings:", c.check(root))
    read = "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\n"
    synth = "    -generic UCODE_HEX_P=gptp_ucode.hex\n"
    clock = "create_clock -period 10.000 -name clk [get_ports clk_i]\n"
    arms = {
        "read_xdc moved after synth_design": c.GOOD_TCL.replace(read, "").replace(synth, synth + read),
        "create_clock after synth_design": c.GOOD_TCL.replace(read, "").replace(synth, synth + clock),
        "no read_xdc": c.GOOD_TCL.replace(read, ""),
        "create_clock added after synth_design": c.GOOD_TCL + clock,
        "second synth_design": c.GOOD_TCL + "synth_design -top T -part P\n",
    }
    for label, text in arms.items():
        (root / c.SCRIPTS[-1]).write_text(text)
        print(f"[B] tcl arm {label!r}: {c.check(root)}")

# ---- Part C: static plants through make ooc with a stub Vivado -------------
stub = WORK / "stub"
(stub / "bin").mkdir(parents=True, exist_ok=True)
(stub / "bin/vivado").write_text("#!/bin/sh\necho \"STUB VIVADO REACHED: $*\"\nexit 3\n")
(stub / "bin/vivado").chmod(0o755)
(stub / "settings64.sh").write_text(f'PATH="{stub}/bin:$PATH"\nexport PATH\n')
env = dict(os.environ, VIVADO_SETTINGS=str(stub / "settings64.sh"))


def plant(name, edit):
    dst = WORK / "plants" / name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(TREE, dst, ignore=shutil.ignore_patterns("work"))
    (dst / "syn/ooc/work").mkdir()
    shutil.copy(TREE / "syn/ooc/work/gptp_ucode.hex", dst / "syn/ooc/work/gptp_ucode.hex")
    edit(dst / "syn/ooc")
    return dst


def move_read_after(script):
    def edit(ooc):
        p = ooc / script
        t = p.read_text()
        read = "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\n"
        assert t.count(read) == 1
        t = t.replace(read, "")
        t = t.replace("    -generic UCODE_HEX_P=gptp_ucode.hex\n",
                      "    -generic UCODE_HEX_P=gptp_ucode.hex\n" + read)
        p.write_text(t)
    return edit


def append(script, text):
    def edit(ooc):
        p = ooc / script
        p.write_text(p.read_text() + text)
    return edit


def xdc(old, new):
    def edit(ooc):
        p = ooc / "ooc_clock.xdc"
        p.write_text(p.read_text().replace(old, new))
    return edit


static_plants = [
    ("unplanted", lambda ooc: None, None),
    ("ucpu-read-after", move_read_after("ucpu_ooc.tcl"),
     ["ucpu_ooc.tcl: ooc_clock.xdc is not read before synth_design",
      "ucpu_ooc.tcl:17: read_xdc after synth_design"]),
    ("engine-read-after", move_read_after("engine_ooc.tcl"),
     ["engine_ooc.tcl: ooc_clock.xdc is not read before synth_design",
      "engine_ooc.tcl:23: read_xdc after synth_design"]),
    ("engine-extra-create_clock", append("engine_ooc.tcl", "create_clock -period 12.000 -name c2 [get_ports clk_i]\n"),
     ["engine_ooc.tcl:27: create_clock after synth_design"]),
    ("ucpu-source-after", append("ucpu_ooc.tcl", "source $SPEC/syn/ooc/late.tcl\n"),
     ["ucpu_ooc.tcl:21: source after synth_design"]),
    ("xdc-5ns", xdc("-period 10.000", "-period 5.000"),
     ["ooc_clock.xdc: clock is 5.000 ns on clk_i, expected 10.000 ns on clk_i"]),
]
for name, edit, expect in static_plants:
    dst = plant(name, edit)
    rc, out = run(["make", "ooc"], cwd=dst, env=env)
    reached = "STUB VIVADO REACHED" in out
    if expect is None:
        ok = reached and "PASS (17 arms)" in out
    else:
        ok = rc != 0 and not reached and "ooc clock order: FAIL" in out and all(e in out for e in expect)
    record("C", f"make ooc plant {name}: rc={rc} vivado_reached={reached}", ok, out)

# ---- Part D: gap probes (informational) -------------------------------------
gaps = [
    ("read_xdc of a different ooc_clock.xdc path", lambda ooc: (ooc / "ucpu_ooc.tcl").write_text(
        (ooc / "ucpu_ooc.tcl").read_text().replace("$SPEC/syn/ooc/ooc_clock.xdc", "/elsewhere/ooc_clock.xdc"))),
    ("XDC excluded from synthesis by property", lambda ooc: (ooc / "ucpu_ooc.tcl").write_text(
        (ooc / "ucpu_ooc.tcl").read_text().replace(
            "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\n",
            "read_xdc $SPEC/syn/ooc/ooc_clock.xdc\nset_property USED_IN_SYNTHESIS false [get_files ooc_clock.xdc]\n"))),
    ("XDC with an extra 5 ns generated clock", lambda ooc: (ooc / "ooc_clock.xdc").write_text(
        (ooc / "ooc_clock.xdc").read_text()
        + "create_generated_clock -name g -source [get_ports clk_i] -divide_by 1 [get_ports clk_i]\n")),
    ("malformed period 10.0.0", xdc("-period 10.000", "-period 10.0.0")),
]
for label, edit in gaps:
    dst = plant("gap-" + re.sub(r"\W+", "_", label), edit)
    rc, out = run([sys.executable, "-I", str(dst / "syn/ooc/check_ooc_clock.py")])
    print(f"[D] static check on gap '{label}': rc={rc}")
    for line in out.strip().splitlines()[-4:]:
        print(f"        {line}")

bad = [r for r in results if not r[2]]
print(f"SUMMARY: {len(results) - len(bad)}/{len(results)} expected outcomes")
sys.exit(1 if bad else 0)
