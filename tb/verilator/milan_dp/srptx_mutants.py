#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""srptx_mutants.py - the split build's SRP transmit checks, each against a defect planted in the code (#867).

Each arm plants one line in a copy of lwSRP, the SRP adapter or the datapath, builds the split half through
its own recipe (twin_fw.py --replace for a firmware unit, DP_SRC for the datapath, make build-twin-sp into
an arm's own directories), runs the scenario the arm names, and srptx_grade.py must report a finding with
the arm's words. A clean control first builds the tracked sources the same way and must grade every
scenario an arm runs with no finding. A build failure is never a catch.

  python3 tb/verilator/milan_dp/srptx_mutants.py [--only NAME] [--list]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MRP = ROOT / "third_party/lwSRP/src/core/mrp_mad.c"
ADAPTER = ROOT / "sw/firmware/ctrl/srp/srp_mbx.c"
DP = ROOT / "hdl/milan/milan_datapath.sv"

#: (name, the source, its line as tracked, the planted line, scenario, run ms or 0, the words that must refuse it)
ARMS = (
    ("an AttributeList EndMark of 0x0001", MRP,
     "    end[0] = 0; end[1] = 0;", "    end[0] = 0; end[1] = 1;",
     "wire", 3000, "MSRP AttributeList EndMark missing where its AttributeListLength ends"),
    ("each declaration encoded twice", MRP,
     "        v += size;", "        memcpy(v + size, v, size); v += 2u * size;",
     "wire", 3000, "declared 2 times in one MRPDU"),
    ("a LeaveAll on the last AttributeType alone", MRP,
     "            for (unsigned type = 1; type <= last; ++type) {",
     "            for (unsigned type = last; type <= last; ++type) {",
     "wire", 16000, "a LeaveAll on AttributeTypes [4], not on every MSRP AttributeType [1, 2, 3, 4]"),
    ("a refused MRPDU reported sent", ADAPTER,
     "        return -SHLAN_ERROR_NO_BUFFER;", "        m->owed_len = 0; return 0;",
     "hold", 0, "never left the MAC"),
    ("the first MRPDU's source address unset", ADAPTER,
     "        wire_put_be(m->owed_frame + 6,s->interface->mac,6);",
     "        wire_put_be(m->owed_frame + 6,m->transmitted ? s->interface->mac : 0u,6);",
     "wire", 3000, "[SA] MSRP frame at ms 1 from 000000000000, not the port's MAC"),
    ("a Join timer of 23 centiseconds", MRP,
     "    shlan_timer_arm(&ps->join_timer, ps->join_cs);", "    shlan_timer_arm(&ps->join_timer, ps->join_cs + 3u);",
     "wire", 3000, "past JoinTime + the MRP service bound (218 ms"),
    ("a LeaveAll drawn past 1.5 x LeaveAllTime", MRP,
     "    return ps->leaveall_cs + 1u + ps->random % (ps->leaveall_cs / 2u - 1u);",
     "    return ps->leaveall_cs * 3u / 2u + 30u;",
     "wire", 40000, "outside 9782 to 15218 ms"),
    ("a withdrawal in LV that restarts LeaveTime (#608)", MRP,
     "        _RX,                                /* LV: -x-                  */",
     "        _RE(REG_IND_NONE, REG_TIMER_START, MRP_REG_STATE_LV),",
     "licence", 0, "[608] the talker stopped at ms"),
    ("the split's ACTIVE term held open", DP,
     "    assign pp_cd_srp_active_w         = i_ctl_pub_licence[ACMP_SRC_C-1:0];",
     "    assign pp_cd_srp_active_w         = '1;",
     "licence", 0, "[LIC] at ms 1 the policer reads active 0x3, admitted 0x0"),
)


def build(work: Path, source: Path | None, copy: Path | None) -> tuple[bool, str]:
    """The split half into work, with copy compiled in source's place."""
    args = ["make", "-s", "--no-print-directory", "-C", str(HERE), "build-twin-sp",
            f"TWIN_FW={work / 'fw'}", f"TWIN_SP_MDIR={work / 'sp'}"]
    if source == DP:
        args.append(f"DP_SRC={copy}")
    elif source is not None:
        args.append(f"TWIN_FW_ARGS=--replace {source}={copy}")
    built = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ))
    return built.returncode == 0, built.stdout[-3000:] + built.stderr[-3000:]


def run(work: Path, scenario: str, ms: int) -> tuple[int, list[str], str]:
    """One scenario on the build in work, graded: (the binary's rc, the findings, its output)."""
    capture = work / f"{scenario}-{ms}.json"
    cmd = [str(work / "sp" / "Vmilan_dp_twin_sp"), "--srptx", scenario, str(capture)]
    if ms:
        cmd += ["--ms", str(ms)]
    ran = subprocess.run(cmd, capture_output=True, text=True, cwd=HERE)
    if not capture.exists():
        return ran.returncode, [], ran.stdout + ran.stderr
    graded = subprocess.run([sys.executable, "-B", str(HERE / "srptx_grade.py"), str(capture)],
                            capture_output=True, text=True, cwd=HERE)
    found = [line for line in graded.stdout.splitlines() if line.startswith("[")]
    return ran.returncode, found, ran.stdout + ran.stderr + graded.stdout


def main() -> int:
    """Every arm, or --only one, or --list them; the exit status is the verdict."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    args = ap.parse_args()
    if args.list:
        print("\n".join(name for name, *_ in ARMS))
        return 0
    arms = [a for a in ARMS if args.only in (None, a[0])]
    if not arms:
        print(f"no arm named {args.only!r}")
        return 2
    work = Path(tempfile.mkdtemp(prefix="srptx-mutants-", dir=HERE))
    bad = 0
    try:
        ok, out = build(work / "clean", None, None)
        if not ok:
            print(f"FAIL control: the tracked sources did not build\n{out}")
            return 1
        for scenario, ms in sorted({(a[4], a[5]) for a in arms}):
            rc, found, out = run(work / "clean", scenario, ms)
            if rc != 0 or found:
                print(f"FAIL control: the tracked sources must grade {scenario} clean (rc {rc})\n"
                      + "\n".join(found[:5]))
                return 1
            print(f"ok   control: the tracked sources grade {scenario}{f' to {ms} ms' if ms else ''} clean")
        for name, src, old, new, scenario, ms, words in arms:
            text = src.read_text()
            if text.count(old) != 1:
                print(f"FAIL {name}: its anchor is not in {src.name} once")
                bad += 1
                continue
            arm = work / name.translate(str.maketrans(" '#()", "_____"))
            arm.mkdir()
            copy = arm / src.name
            copy.write_text(text.replace(old, new))
            ok, out = build(arm, src, copy)
            if not ok:
                print(f"FAIL {name}: the planted build failed, which is no catch\n{out}")
                bad += 1
                continue
            rc, found, out = run(arm, scenario, ms)
            shutil.rmtree(arm, ignore_errors=True)
            caught = [f for f in found if words in f]
            if caught:
                print(f"ok   {name}: refused by {caught[0]}")
            else:
                print(f"FAIL {name}: escaped; wanted {words!r}, rc {rc}\n" + "\n".join(found[:5]) + out[-1500:])
                bad += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"srptx mutants: {len(arms) - bad} of {len(arms)} refused")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
