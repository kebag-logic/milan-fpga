#!/usr/bin/env python3
"""Reviewer mutant campaign for the #502 live-write pending glue.

Usage: r329_mutants.py <tree> <outdir> [mutant ...]

<tree> is a disposable copy of the repository at the reviewed head. Each
mutant rewrites one anchor of hdl/milan/KL_pp_shadow.sv in a copy under
<outdir>, then runs two legs of tb/verilator/pp_shadow with the mutant
substituted into the datapath source list:
  dyn    - `make run-pending` (dynamic-output fixture, --pending-only)
  static - `make run-base SIM_ARGS=--pending-only` (default static output)
A mutant is KILLED when any leg exits non-zero with at least one [FAIL]
line; a build failure is reported as BUILD-ERROR, never as a kill.
The shipping source is verified byte-identical before and after.
"""

import hashlib
import subprocess
import sys
from pathlib import Path

LIVE = ("  assign aecp_live_wr_w = aecp_name_wr_w\n"
        "                        | (amap_edit_req_o && (amap_edit_phase_o == 3'd5));")
PEND = ("  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
        "                    | aecp_live_wr_w | aecp_live_pend_r;")


def live(expr: str) -> tuple[str, str]:
    return LIVE, f"  assign aecp_live_wr_w = {expr};"


MUTANTS = {
    "control": None,
    "M1_drop_map": live("aecp_name_wr_w"),
    "M2_drop_name": live("(amap_edit_req_o && (amap_edit_phase_o == 3'd5))"),
    "M3_delay_one_cycle": (PEND, "  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
                                 "                    | aecp_live_pend_r;"),
    "M4_wrong_phase_2": live("aecp_name_wr_w | (amap_edit_req_o && (amap_edit_phase_o == 3'd2))"),
    "M5_early_phase_4": live("aecp_name_wr_w | (amap_edit_req_o && (amap_edit_phase_o == 3'd4))"),
    "M6_add_only": live("aecp_name_wr_w | (amap_edit_req_o && (amap_edit_phase_o == 3'd5)"
                        " && !amap_edit_remove_o)"),
    "M7_no_sticky": (PEND, "  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)\n"
                           "                    | aecp_live_wr_w;"),
    "M8_input_ports_only": live("aecp_name_wr_w | (amap_edit_req_o && (amap_edit_phase_o == 3'd5)"
                                " && (amap_edit_desc_type_o == 16'h000e))"),
    "M9_any_phase": live("aecp_name_wr_w | amap_edit_req_o"),
    "M10_late_mark": live("aecp_nvm_stb_w && ((aecp_nvm_mark_w == 8'd6)"
                          " || (aecp_nvm_mark_w == 8'd7))"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_leg(tb: Path, outdir: Path, name: str, leg: str, srcs: list[Path]) -> str:
    log = outdir / f"{name}.{leg}.log"
    bdir = outdir / "build" / f"{name}.{leg}"
    bdir.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["make"]
    if leg == "dyn":
        cmd += ["run-pending", f"PENDING_BUILD_DIR={bdir}"]
    else:
        cmd += ["run-base", f"BUILD_DIR={bdir}", "SIM_ARGS=--pending-only"]
    cmd.append("DP_SRCS=" + " ".join(str(p) for p in srcs))
    with log.open("w") as fh:
        rc = subprocess.run(cmd, cwd=tb, stdout=fh, stderr=subprocess.STDOUT,
                            check=False).returncode
    text = log.read_text(errors="replace")
    fails = sorted({ln.split("got=")[0].strip() for ln in text.splitlines()
                    if "[FAIL]" in ln})
    summary = [ln for ln in text.splitlines() if ln.startswith("pp_shadow:")]
    if rc == 0 and "RESULT: PASS" in text:
        verdict = "PASS"
    elif fails and "RESULT: FAIL" in text:
        verdict = "FAIL"
    else:
        verdict = f"BUILD-ERROR rc={rc}"
    return (f"{name:22s} {leg:6s} {verdict:16s} {summary[-1] if summary else '-'}\n"
            + "".join(f"    {f}\n" for f in fails))


def main() -> None:
    tree = Path(sys.argv[1]).resolve()
    outdir = Path(sys.argv[2]).resolve()
    chosen = sys.argv[3:] or list(MUTANTS)
    outdir.mkdir(parents=True, exist_ok=True)
    tb = tree / "tb/verilator/pp_shadow"
    shadow = tree / "hdl/milan/KL_pp_shadow.sv"
    before = sha(shadow)
    original = shadow.read_text()
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"],
                             cwd=tb, check=True, capture_output=True, text=True)
    srcs = [(tb / p).resolve() for p in listing.stdout.split()]
    assert srcs.count(shadow) == 1, "expected exactly one shipping shadow"
    results = outdir / "RESULTS.txt"
    with results.open("a") as res:
        res.write(f"# shipping KL_pp_shadow.sv sha256 {before}\n")
        for name in chosen:
            spec = MUTANTS[name]
            if spec is None:
                use = srcs
            else:
                old, new = spec
                if original.count(old) != 1:
                    res.write(f"{name:22s} REFUSED anchor count {original.count(old)}\n")
                    continue
                mdir = outdir / "src" / name / "hdl" / "milan"
                mdir.mkdir(parents=True, exist_ok=True)
                mut = mdir / "KL_pp_shadow.sv"
                mut.write_text(original.replace(old, new))
                use = [mut if p == shadow else p for p in srcs]
            for leg in ("dyn", "static"):
                line = run_leg(tb, outdir, name, leg, use)
                res.write(line)
                res.flush()
                print(line, end="", flush=True)
        after = sha(shadow)
        res.write(f"# shipping source unchanged after campaign: {after == before}\n")


if __name__ == "__main__":
    main()
