#!/usr/bin/env python3
"""R366-2 disposable probes for PR #603 at 471892a9.

Copies nothing into the reviewed clone. Expects an exported copy of the head
tree at scratch/tree (tar of the clone without .git). Each probe plants one
edit into a copy of milan_datapath.sv, builds the named leg through the
suite's own make recipe (DP_SRC override, private Mdir) and runs it once.
Writes receipts/<probe>.log (full run output) and receipts/summary.txt.

Usage: probes.py VERILATOR_WRAPPER [probe ...]
"""
import concurrent.futures as cf
import subprocess
import sys
import time
from pathlib import Path

PKT = Path(__file__).resolve().parent
TREE = PKT / "scratch" / "tree"
SUITE = TREE / "tb/verilator/milan_dp"
DP = TREE / "hdl/milan/milan_datapath.sv"
WORK = PKT / "scratch" / "probes"
RCPT = PKT / "receipts"

TRIG = "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);"
DECL = "  wire mcr_restart_p_w = crf_clk_selected_r\n"

LATE_VETO_REG = (
    "  logic probe_rb_d_r;\n"
    "  always_ff @(posedge axis_clk) begin : probe_rb_delay\n"
    "    if (!axis_resetn) probe_rb_d_r <= 1'b0;\n"
    "    else probe_rb_d_r <= media_rebase_p_w;\n"
    "  end : probe_rb_delay\n")
ADJ_DELAY16_REG = (
    "  logic [15:0] probe_adj_sr_r;\n"
    "  always_ff @(posedge axis_clk) begin : probe_adj_delay\n"
    "    if (!axis_resetn) probe_adj_sr_r <= '0;\n"
    "    else probe_adj_sr_r <= {probe_adj_sr_r[14:0], eff_ptp_adjust_w};\n"
    "  end : probe_adj_delay\n")
ADJ_DELAY256_REG = (
    "  logic [8:0] probe_adj_cnt_r;\n"
    "  always_ff @(posedge axis_clk) begin : probe_adj_count\n"
    "    if (!axis_resetn) probe_adj_cnt_r <= '0;\n"
    "    else if (eff_ptp_adjust_w) probe_adj_cnt_r <= 9'd256;\n"
    "    else if (probe_adj_cnt_r != 9'd0) probe_adj_cnt_r <= probe_adj_cnt_r - 9'd1;\n"
    "  end : probe_adj_count\n")

# name: (leg, [(anchor, replacement), ...])
PROBES = {
    "G0_clean": ("gmstep", []),
    "G1_rebase_restored": ("gmstep", [(TRIG, TRIG[:-1] + " | media_rebase_p_w;")]),
    "G2_crf_propagation_removed": ("gmstep", [(TRIG, "                          & (tkd_crflk_q_r & ~crf_locked_w);")]),
    "G3_same_cycle_veto": ("gmstep", [(TRIG, TRIG[:-1] + " & ~media_rebase_p_w;")]),
    "G4_one_cycle_late_veto": ("gmstep", [(DECL, LATE_VETO_REG + DECL),
                                          (TRIG, TRIG[:-1] + " & ~probe_rb_d_r;")]),
    "G5_settime_only_restored": ("gmstep", [(TRIG, TRIG[:-1] + " | cfg_ptp_cmd_load;")]),
    "O0_clean": ("option-off", []),
    "O1_settime_only": ("option-off", [(TRIG, TRIG[:-1] + " | cfg_ptp_cmd_load;")]),
    "O2_adjtime_only": ("option-off", [(TRIG, TRIG[:-1] + " | eff_ptp_adjust_w;")]),
    "O3_both_causes": ("option-off", [(TRIG, TRIG[:-1] + " | media_rebase_p_w;")]),
    "O4_adjtime_delay16": ("option-off", [(DECL, ADJ_DELAY16_REG + DECL),
                                          (TRIG, TRIG[:-1] + " | probe_adj_sr_r[15];")]),
    "O5_adjtime_delay256": ("option-off", [(DECL, ADJ_DELAY256_REG + DECL),
                                           (TRIG, TRIG[:-1] + " | (probe_adj_cnt_r == 9'd1);")]),
}

for _n in (2, 4, 8, 12):
    PROBES[f"O6_adjtime_delay{_n}"] = ("option-off", [(DECL, ADJ_DELAY16_REG + DECL),
                                         (TRIG, TRIG[:-1] + f" | probe_adj_sr_r[{_n - 1}];")])
PROBES["G6_adjtime_delay16_gmstep"] = ("gmstep", PROBES["O4_adjtime_delay16"][1])
PROBES["G7_settime_delay16_gmstep"] = ("gmstep", [(DECL, ADJ_DELAY16_REG.replace("eff_ptp_adjust_w", "cfg_ptp_cmd_load") + DECL),
                                     (TRIG, TRIG[:-1] + " | probe_adj_sr_r[15];")])

LEGS = {
    "gmstep": ("gmstep-build", "GMSTEP_MDIR", "Vmilan_dp_gmstep", True),
    "option-off": ("option-off-build", "OPTOFF_MDIR", "Vmilan_dp_sim", False),
}


def run_probe(name: str, verilator: str) -> str:
    leg, edits = PROBES[name]
    target, mdir_var, exe_name, takes_aem = LEGS[leg]
    pdir = WORK / name
    pdir.mkdir(parents=True, exist_ok=True)
    text = DP.read_text()
    for anchor, repl in edits:
        n = text.count(anchor)
        if n != 1:
            return f"{name}: ANCHOR COUNT {n} (expected 1) - not planted"
        text = text.replace(anchor, repl)
    src = pdir / "milan_datapath.sv"
    src.write_text(text)
    mdir = pdir / "obj"
    log = RCPT / f"{name}.log"
    t0 = time.time()
    b = subprocess.run(["make", "-s", "-C", str(SUITE), target, f"{mdir_var}={mdir}",
                        f"DP_SRC={src}", f"VERILATOR={verilator}", "VERILATOR_JOBS=2"],
                       capture_output=True, text=True, check=False)
    exe = mdir / exe_name
    if b.returncode != 0 or not exe.is_file():
        log.write_text(f"BUILD FAILED rc={b.returncode}\n{b.stdout[-4000:]}\n{b.stderr[-4000:]}")
        return f"{name}: BUILD FAILED rc={b.returncode}"
    cmd = [str(exe)] + ([str(mdir / "aemi.bin")] if takes_aem else [])
    r = subprocess.run(cmd, cwd=str(SUITE), capture_output=True, text=True, check=False)
    out = r.stdout + r.stderr
    log.write_text(f"# probe {name} leg {leg} rc={r.returncode} "
                   f"elapsed={time.time() - t0:.0f}s\n{out}")
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    summ = [ln.strip() for ln in out.splitlines()
            if "PASS" in ln and "FAIL" in ln and "/" in ln][-1:]
    return (f"{name}: leg={leg} rc={r.returncode} fails={len(fails)} {summ}\n"
            + "".join(f"    {f[:160]}\n" for f in fails))


def main() -> int:
    verilator = sys.argv[1]
    names = sys.argv[2:] or list(PROBES)
    RCPT.mkdir(exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:  # 4 builds x 2 jobs = 8
        results = list(ex.map(lambda n: run_probe(n, verilator), names))
    text = "\n".join(results) + "\n"
    with (RCPT / "summary.txt").open("a") as fh:
        fh.write(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
