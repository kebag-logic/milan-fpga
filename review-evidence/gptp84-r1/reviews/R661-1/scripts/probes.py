#!/usr/bin/env python3
"""Reviewer-owned fault probes for FPGA-gPTP PR #86 (#84, #85).

Each probe copies a pristine exact-head source tree, applies one textual
mutation that must match exactly once, runs the engine suite's `make run`
(all four passes) with the pinned simulator on PATH, and records rc and the
FAIL lines. A probe is CAUGHT when the suite exits nonzero with at least one
FAIL line and no build error. Nothing is written into the source clone.

Usage: probes.py HEAD_TREE WORK_DIR OUT_DIR [--jobs N]
"""
import argparse, concurrent.futures as cf, shutil, subprocess, sys
from pathlib import Path

GEN = "hdl/ucode/gen_gptp_ucode.py"
ENG = "hdl/top/KL_gptp_engine.sv"

PROBES = [
    ("A-ascap-fall-clears-master-syncok", GEN,
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)\n"
     "    p.label(\"done\")\n",
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C)\n"
     "    p.label(\"done\")\n",
     "a Pdelay asCapable fall during mastership clears sync-ok"),
    ("A2-lost-responses-clear-master-syncok", GEN,
     "    p.emit(\"BRS\", cnd=BRS_LT, label=\"pd_go\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n"
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)\n",
     "    p.emit(\"BRS\", cnd=BRS_LT, label=\"pd_go\")\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n"
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C)\n",
     "lost Pdelay responses during mastership clear sync-ok"),
    ("A3-cease-clears-master-syncok", GEN,
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_CEASECNT, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n"
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_SYNCOK_C)\n",
     "    p.emit(\"WRST\", ra=RT, imm=RG_SCR | S_CEASECNT, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n"
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C)\n",
     "the multiple-response cease during mastership clears sync-ok"),
    ("A4-incapable-master-publishes-no-syncok", ENG,
     "  assign pub_flags_o     = {pub_flags_r[31:1],\n",
     "  assign pub_flags_o     = {pub_flags_r[31:4],\n"
     "                            pub_flags_r[3] & (pub_flags_r[2] | !pub_flags_r[1]),\n"
     "                            pub_flags_r[2:1],\n",
     "a master whose port is not asCapable publishes no sync-ok"),
    ("B-self-publication-claims-syncok", ENG,
     "  assign pub_flags_o     = {pub_flags_r[31:1],\n",
     "  assign pub_flags_o     = {pub_flags_r[31:4],\n"
     "                            pub_flags_r[3] | ((pub_gm_r == rom_clock_id_w)"
     " && !pub_flags_r[1]),\n"
     "                            pub_flags_r[2:1],\n",
     "a self publication without mastership publishes sync-ok"),
    ("C-slave-srto-keeps-syncok", GEN,
     "           imm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)\n"
     "    p.emit(\"ALU\", rd=RT, ra=RT, rb=RU, cnd=ALU_AND)\n",
     "           imm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C | FL_SYNCOK_C)\n"
     "    p.emit(\"ALU\", rd=RT, ra=RT, rb=RU, cnd=ALU_AND)\n",
     "a slave's Sync receipt timeout keeps sync-ok"),
    ("D-srto-shift-by-one", GEN,
     "cnd=ALU_SHL, imm=SYNCOK_BY_AMGM_C)\n",
     "cnd=ALU_SHL, imm=1)\n",
     "the receipt-timeout mask keys sync-ok on asCapable, not mastership"),
    ("E-append-slot-left-zero", ENG,
     "                    pub_path_r[64*pk +: 64] <= rom_clock_id_w;\n",
     "                    pub_path_r[64*pk +: 64] <= 64'd0;\n",
     "the count gains one but thisClock is not written"),
    ("F-count-not-incremented", ENG,
     "  wire [3:0] path_trace_count_w = ann_pub_count_clamped_w +\n"
     "                                  {3'd0, path_append_w};\n",
     "  wire [3:0] path_trace_count_w = ann_pub_count_clamped_w;\n",
     "thisClock is written but the count is not incremented"),
    ("G-append-on-unclamped-count", ENG,
     "  wire       path_append_w = (ann_pub_count_clamped_w != 4'd0) &&\n"
     "                             (ann_pub_count_clamped_w != 4'd8);\n",
     "  wire       path_append_w = (ann_pub_count_r != 8'd0) &&\n"
     "                             (ann_pub_count_r != 8'd8);\n",
     "a path deeper than eight entries takes a ninth count"),
    ("H-become-sets-syncok-only-on-handover", GEN,
     "    e_flags(p, andm=FL_ASCAP_C, orm=FL_AMGM_C | FL_SYNCOK_C)\n",
     "    e_flags(p, andm=FL_ASCAP_C | FL_SYNCOK_C, orm=FL_AMGM_C)\n",
     "becoming grandmaster keeps a prior verdict instead of setting it"),
]


def run_probe(head: Path, work: Path, out: Path, probe) -> str:
    name, rel, old, new, what = probe
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(head, tree)
    f = tree / rel
    text = f.read_text(encoding="utf-8")
    n = text.count(old)
    if n != 1:
        return f"{name}: PATTERN-MATCHES={n} (not applied) - {what}"
    f.write_text(text.replace(old, new), encoding="utf-8")
    log = out / f"probe_{name}.log"
    with log.open("w") as fh:
        rc = subprocess.run(["make", "-C", str(tree / "tb/verilator/engine"),
                             "run"], stdout=fh, stderr=subprocess.STDOUT).returncode
    body = log.read_text(errors="replace")
    fails = [l for l in body.splitlines() if l.startswith("FAIL ")]
    built = "Vengine_sim" in body and "%Error" not in body
    verdict = "CAUGHT" if rc != 0 and fails and built else (
        "BUILD-ERROR" if not built else "SURVIVED")
    (out / f"probe_{name}.rc").write_text(f"{rc}\n")
    shutil.rmtree(tree / "tb/verilator/engine/obj_dir", ignore_errors=True)
    head_fails = "; ".join(fails[:6])
    return f"{name}: {verdict} rc={rc} fails={len(fails)} - {what} | {head_fails}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("head"); ap.add_argument("work"); ap.add_argument("out")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    head, work, out = Path(a.head), Path(a.work), Path(a.out)
    work.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
    probes = [p for p in PROBES if not a.only or p[0] in a.only.split(",")]
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        results = list(ex.map(lambda p: run_probe(head, work, out, p), probes))
    (out / "probes_summary.txt").write_text("\n".join(results) + "\n")
    print("\n".join(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
