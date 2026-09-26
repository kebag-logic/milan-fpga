#!/usr/bin/env python3
"""Reviewer mutation probe for the #502 pending glue (KL_pp_shadow.sv).

Usage: reviewer_mutants.py <repo-root> <scratch-dir> [mutant ...]

Each mutant is a textual edit of a COPY of hdl/milan/KL_pp_shadow.sv. The copy
is substituted for the shipping file in the milan_dp source list, exactly as the
lane's pending_mutant.py does, and two harness legs are built and run:
  static  = make run-base SIM_ARGS=--pending-only  (default static output map)
  dynamic = make run-pending                      (dynamic output fixture)
A build failure is reported as BUILD-FAIL and never counted as killed.
The shipping source is hashed before and after; any change aborts.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

LIVE = ("  assign aecp_live_wr_w = aecp_name_wr_w\n"
        "                        | (amap_edit_req_o && (amap_edit_phase_o == 3'd5));")
PEND = ("  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
        "                    | aecp_live_wr_w | aecp_live_pend_r;")
RST = "      aecp_live_pend_r <= 1'b0;"

MUTANTS = {
    "drop_name": (LIVE, "  assign aecp_live_wr_w = 1'b0\n"
                        "                        | (amap_edit_req_o && (amap_edit_phase_o == 3'd5));"),
    "drop_map": (LIVE, "  assign aecp_live_wr_w = aecp_name_wr_w\n"
                       "                        | 1'b0;"),
    "delay_one_cycle": (PEND, "  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
                              "                    | aecp_live_pend_r;"),
    "pulse_only_no_sticky": (PEND, "  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
                                   "                    | aecp_live_wr_w;"),
    "phase4_validate": (LIVE, LIVE.replace("3'd5", "3'd4")),
    "phase1_begin_commit": (LIVE, LIVE.replace("3'd5", "3'd1")),
    "phase0_begin": (LIVE, LIVE.replace("3'd5", "3'd0")),
    "phase2_finish": (LIVE, LIVE.replace("3'd5", "3'd2")),
    "reset_sets_sticky": (RST, "      aecp_live_pend_r <= 1'b1;"),
    "map_any_phase": (LIVE, "  assign aecp_live_wr_w = aecp_name_wr_w\n"
                            "                        | (amap_edit_req_o);"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd, cwd, log):
    with log.open("w") as fh:
        rc = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT).returncode
    return rc, log.read_text(errors="replace")


def verdict(rc, text):
    if "RESULT: PASS" in text and rc == 0:
        return "SURVIVED"
    if "RESULT: FAIL" in text:
        return "KILLED"
    return "BUILD-FAIL"


def main():
    root = Path(sys.argv[1]).resolve()
    scratch = Path(sys.argv[2]).resolve()
    names = sys.argv[3:] or list(MUTANTS)
    here = root / "tb/verilator/pp_shadow"
    source = root / "hdl/milan/KL_pp_shadow.sv"
    before = sha(source)
    original = source.read_text()
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"], cwd=here,
                             check=True, capture_output=True, text=True).stdout.split()
    sources = [(here / p).resolve() for p in listing]
    assert sources.count(source) == 1, "expected exactly one shipping shadow"
    print(f"shipping KL_pp_shadow.sv sha256 {before}")
    for name in names:
        old, new = MUTANTS[name]
        if original.count(old) != 1:
            print(f"{name}: REFUSED anchor count {original.count(old)}")
            continue
        mdir = scratch / "mut" / name
        (mdir / "hdl/milan").mkdir(parents=True, exist_ok=True)
        mutant = mdir / "hdl/milan/KL_pp_shadow.sv"
        mutant.write_text(original.replace(old, new))
        srcs = " ".join(str(mutant if p == source else p) for p in sources)
        results = []
        for leg, cmd in (
            ("static", ["make", "run-base", f"BUILD_DIR={mdir}/obj_static",
                        "SIM_ARGS=--pending-only", f"DP_SRCS={srcs}"]),
            ("dynamic", ["make", "run-pending", f"PENDING_BUILD_DIR={mdir}/obj_dyn",
                         f"DP_SRCS={srcs}"]),
        ):
            rc, text = run(cmd, here, mdir / f"{leg}.log")
            fails = [l.strip() for l in text.splitlines() if "[FAIL]" in l]
            v = verdict(rc, text)
            results.append(f"{leg}={v}({len(fails)} fails)")
            (scratch / "mut" / f"{name}.{leg}.fails.txt").write_text("\n".join(fails) + "\n")
        print(f"{name}: " + " ".join(results))
        if sha(source) != before:
            sys.exit("ABORT: shipping source changed")
    print(f"shipping KL_pp_shadow.sv sha256 after {sha(source)}")


if __name__ == "__main__":
    main()
