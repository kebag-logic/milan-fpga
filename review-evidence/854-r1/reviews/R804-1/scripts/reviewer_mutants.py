#!/usr/bin/env python3
"""Reviewer-owned disposable mutation probes of KL_pp_shadow's drop count (#854).

Each arm plants one text change in a private copy of hdl/milan/KL_pp_shadow.sv,
builds the pp_shadow base leg against it (DP_SRCS override, as drops_mutant.py
does) and runs the simulator with the given argument. A control runs first.
Reports, per arm, KILLED (exit != 0 and a [FAIL] line) or SURVIVED, and the
[FAIL] lines and DR/PR figure lines.

usage: reviewer_mutants.py <tree> <workdir> <sim-arg> <arm-set> [make VAR=VAL ...]
  arm-set: core (arms against the committed [DR]) | runt (arms for the runt probe)
"""
import subprocess, sys
from pathlib import Path

tree, work, simarg, armset = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
extra = sys.argv[5:]
HERE = tree / "tb" / "verilator" / "pp_shadow"
SHADOW = (tree / "hdl" / "milan" / "KL_pp_shadow.sv").resolve()
LK = "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w);\n"
EV = "  assign drop_evt_w = ff_overflow_w & last_kept_r;\n"
CT = "      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;\n"
CORE = [
    ("counts-runts", LK, "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w) || (fw_S == FW_HEAD0);\n"),
    ("head1-only", LK, "      last_kept_r <= ((fw_S == FW_BODY) & 1'b0) || ((fw_S == FW_HEAD1) && accept_w);\n"),
    ("counts-refused-at-head1", LK, "      last_kept_r <= (fw_S == FW_BODY) || (fw_S == FW_HEAD1) || (accept_w & 1'b0);\n"),
    ("saturates-at-254", CT, "      if (drop_evt_w & (rx_drops_o != 8'hFE)) rx_drops_o <= rx_drops_o + 8'd1;\n"),
    ("counts-two", CT, "      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + ((rx_drops_o == 8'hFE) ? 8'd1 : 8'd2);\n"),
    ("current-state-not-registered", EV, "  assign drop_evt_w = ff_overflow_w & ((fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w)) & (last_kept_r | 1'b1);\n"),
    ("counts-kept-frames-not-losses", EV, "  assign drop_evt_w = (fw_valid_w & fw_ready_w & fw_last_w & ((fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w))) | (ff_overflow_w & last_kept_r & 1'b0);\n"),
]
RUNT = [CORE[0]]
arms = CORE if armset == "core" else RUNT
orig = SHADOW.read_text()
listing = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp", "print-srcs"],
                         cwd=HERE, check=True, capture_output=True, text=True,
                         env={k: v for k, v in __import__("os").environ.items() if k not in ("MAKEFLAGS", "MFLAGS")})
sources = [(HERE / x).resolve() for x in listing.stdout.split()]
assert sources.count(SHADOW) == 1
work.mkdir(parents=True, exist_ok=True)

def leg(label, srcs):
    build = work / label
    log = work / f"{label}.log"
    cmd = ["make", "--no-print-directory", "build-base", f"BUILD_DIR={build}", *extra]
    if srcs is not None:
        cmd.append("DP_SRCS=" + " ".join(str(s) for s in srcs))
    with log.open("w") as f:
        m = subprocess.run(cmd, cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
        if m.returncode != 0:
            return m.returncode, log.read_text(), "BUILD-FAILED"
        r = subprocess.run([str(build / "Vpp_shadow_sim"), simarg], cwd=HERE, stdout=f, stderr=subprocess.STDOUT)
    return r.returncode, log.read_text(), "ran"

def summary(text):
    return [l.strip() for l in text.splitlines() if l.strip().startswith(("[FAIL]", "DR ", "PR ", "RESULT")) or "DR burst" in l or "DR refused" in l or "DR flood" in l or "PR runt" in l]

rc, text, how = leg("control", None)
print(f"control: exit {rc} ({how})"); [print("   ", l) for l in summary(text) if not l.startswith(("DR the", "DR ...", "DR a", "PR the", "PR runts", "PR kept"))]
for name, old, new in arms:
    assert orig.count(old) == 1, name
    m = work / name / "hdl" / "milan" / "KL_pp_shadow.sv"
    m.parent.mkdir(parents=True, exist_ok=True)
    m.write_text(orig.replace(old, new))
    rc, text, how = leg(name, [m if s == SHADOW else s for s in sources])
    fails = [l for l in summary(text) if l.startswith("[FAIL]")]
    verdict = "KILLED" if (rc != 0 and fails) else ("BUILD-FAILED" if how != "ran" else "SURVIVED")
    print(f"{name}: {verdict} (exit {rc})")
    for l in summary(text):
        if l.startswith(("[FAIL]", "RESULT")) or "burst:" in l or "flood:" in l:
            print("   ", l)
assert SHADOW.read_text() == orig
