#!/usr/bin/env python3
"""Reviewer probes of the re-declare hold-off (#951).

Usage: python3 -B holdoff_probes.py <repo-root> <work-dir> [probe ...]

Each probe copies the repository's sw/firmware/ctrl tree into <work-dir>/<probe>/ctrl, applies its edits to
srp/srp_mbx.c (each edit must match exactly one site), and runs the Talker arms the firmware gate runs
(srp_talker.cpp at 1x1/1if and 8x8/2if, test_acmp_mbx.cpp SrpGate.* at 8x8/2if) plus srp_mbx.cpp at 1x1/1if.
It prints, per arm, the exit code and every failing test name, and writes each arm's log. The repository itself
is never written.
"""
from __future__ import annotations

import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(ROOT / "sw/firmware/gtest"))

OLD = "#define SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)\n"
LONGEST = "#define SRP_LEAVEALL_LONGEST_CS (SRP_LEAVEALL_CS + SRP_LEAVEALL_CS / 2u)\n"
LEAVEALL = "#define SRP_LEAVEALL_CS 1000u\n"

PROBES = {
    # unmodified: every arm passes
    "control": (),
    # the value before #951: 2 x LeaveAllTime
    "old-value": ((OLD, OLD.replace("2u * SRP_LEAVEALL_LONGEST_CS", "2u * SRP_LEAVEALL_CS")),),
    # the longest period one centisecond short: 20 ms less hold-off
    "longest-minus-1cs": ((LONGEST, LONGEST.replace("/ 2u)", "/ 2u - 1u)")),),
    # an equivalent spelling of 1.5 x LeaveAllTime: must pass (the tests read the value, not the text)
    "equivalent-3-halves": ((LONGEST, "#define SRP_LEAVEALL_LONGEST_CS (SRP_LEAVEALL_CS * 3u / 2u)\n"),),
    # the hold-off 1 s too long: the upper side
    "overlong-1s": ((OLD, OLD.replace("(2u * SRP_LEAVEALL_LONGEST_CS", "(100u + 2u * SRP_LEAVEALL_LONGEST_CS")),),
    # LeaveAllTime itself changed: configuration and hold-off together
    "leaveall-1100": ((LEAVEALL, "#define SRP_LEAVEALL_CS 1100u\n"),),
    # the mirrored literal the ruling forbids, at today's value: must pass (it is a spelling, not a value)
    "mirrored-literal": ((OLD, "#define SRP_REDECLARE_CS (3000u + SRP_JOIN_CS + (CTRL_LOOP_TX_MS + 9u) / 10u)\n"),),
}


def run(name: str) -> str:
    import fw_gtest
    import srp_arms
    from ctrl_build import CTRL, Tree, Refusal
    base = WORK / name
    if base.exists():
        shutil.rmtree(base)
    src = base / "ctrl"
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / "srp/srp_mbx.c"
    text = target.read_text()
    for old, new in PROBES[name]:
        if text.count(old) != 1:
            return f"== {name}: REFUSED, {text.count(old)} sites for {old!r}\n"
        text = text.replace(old, new)
    target.write_text(text)
    tree = Tree(src, base / "build", base / "reuse", fw_gtest.Build(jobs=4))
    lwsrp = ROOT / "third_party/lwSRP"
    e8 = ROOT / "configs/endstation_ax7101_8x8.yaml"
    arms = (("srp_talker-1x1-1if", dict(interfaces=1, test="srp_talker.cpp")),
            ("srp_talker-8x8-2if", dict(interfaces=2, test="srp_talker.cpp", config=e8)),
            ("SrpGate-8x8-2if", dict(interfaces=2, test=("test_acmp_mbx.cpp", "SrpGate.*"), config=e8)),
            ("srp_mbx-1x1-1if", dict(interfaces=1, test="srp_mbx.cpp")))
    lines = [f"== {name}: edits {len(PROBES[name])}"]
    for arm, kw in arms:
        try:
            out = srp_arms.arm_srp(tree, lwsrp, **kw)
        except Refusal as error:
            lines.append(f"  {arm}: REFUSAL {error}")
            continue
        (base / f"{arm}.log").write_text(out.log)
        fails = sorted(set(re.findall(r"^\s*\[FAIL\] ([A-Za-z0-9_.]+)", out.log, re.M)))
        passed = re.findall(r"^\[  PASSED  \] (\d+) tests?", out.log, re.M)
        lines.append(f"  {arm}: rc={out.rc} passed={passed[-1] if passed else '?'} failed={fails}")
    shutil.rmtree(base / "build", ignore_errors=True)
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    names = sys.argv[3:] or list(PROBES)
    with ProcessPoolExecutor(max_workers=2) as pool:
        for result in pool.map(run, names):
            print(result, flush=True)
