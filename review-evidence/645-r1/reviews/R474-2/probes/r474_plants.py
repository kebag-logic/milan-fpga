#!/usr/bin/env python3
"""R474-2 reviewer-planted defects. Each plant is applied to a disposable COPY
of the exact-head tree (SRC, a `git archive` export) under OUT/<name>/, never
to a tracked file. Usage: r474_plants.py SRC OUT NAME...  Prints the tree path.
The legs are run by r474_run_plants.sh."""
import shutil, sys
from pathlib import Path

CMAP = "hdl/ieee1722/aaf/KL_chan_map_capture.sv"
DP = "hdl/milan/milan_datapath.sv"
PLANTS = {
    # one-sided settle: the full side never drops
    "NODROP": (CMAP, "? LB_DROPW_C'(32'(rc_left_w) - LB_LEFT_C) : '0;", "? LB_DROPW_C'(0) : '0;"),
    # one-sided settle: the empty side never holds
    "NOHOLD": (CMAP, "? LB_HOLDW_C'(LB_LEFT_C - 32'(rc_left_w)) : '0;", "? LB_HOLDW_C'(0) : '0;"),
    # slip counting during the settle: a held pop counts as a dup
    "HOLDDUP": (CMAP, "&& q_fed_r[pop_pair_w] && (pop_cnt_w == '0);",
                "&& q_fed_r[pop_pair_w] && ((pop_cnt_w == '0) || pop_hold_w);"),
    # slip counting during the settle: a settle drop counts as a skip
    "DROPSKIP": (CMAP, "  wire [1:0] skip_inc_w = 2'(push_drop_w)",
                 "  wire [1:0] skip_inc_w = 2'(pop_act_w && (pop_drop_n_w != '0)) + 2'(push_drop_w)"),
    # wrong excursion band: one cycle (below twice the quiet excursion)
    "BAND1": (DP, "  localparam int unsigned SETTLE_EXC_ERR_C   = 2;", "  localparam int unsigned SETTLE_EXC_ERR_C   = 1;"),
    # wrong excursion band: eight cycles (still below the +9 pull)
    "BAND8": (DP, "  localparam int unsigned SETTLE_EXC_ERR_C   = 2;", "  localparam int unsigned SETTLE_EXC_ERR_C   = 8;"),
    # early re-arm: recovery qualifies after 64 quiet ticks, not 2048
    "REARM64": (DP, "end else if (settle_run_ticks_r >= SETTLE_RUN_W_C'(SRC_SETTLE_TICKS_C)) begin",
                "end else if (settle_run_ticks_r >= SETTLE_RUN_W_C'(64)) begin"),
    # early re-arm: recovery ends at the action (no qualification at all is NO-RECOVERY;
    # this one re-arms after 512 ticks, a quarter dwell)
    "REARM512": (DP, "end else if (settle_run_ticks_r >= SETTLE_RUN_W_C'(SRC_SETTLE_TICKS_C)) begin",
                 "end else if (settle_run_ticks_r >= SETTLE_RUN_W_C'(512)) begin"),
}

def main() -> int:
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    for name in sys.argv[3:]:
        path, old, new = PLANTS[name]
        tree = out / name
        if tree.exists():
            shutil.rmtree(tree)
        (tree / "tb/verilator").mkdir(parents=True)
        shutil.copytree(src / "hdl", tree / "hdl")
        for link in ("configs", "tb/common", "tb/verilator/mmcm_servo"):
            (tree / link).symlink_to(src / link)
        for d in ("follow_ring", "chmap_capture"):
            shutil.copytree(src / "tb/verilator" / d, tree / "tb/verilator" / d,
                            ignore=shutil.ignore_patterns("obj_dir*"))
        f = tree / path
        text = f.read_text()
        assert text.count(old) == 1, (name, old)
        f.write_text(text.replace(old, new))
        print(tree)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
