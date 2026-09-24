#!/usr/bin/env python3
"""Write the reviewer's own gmstep probe variants.

Every variant starts from the EDITED datapath (the tree's milan_datapath.sv
plus the published #387 patch, which passes the leg) or from the tree's
KL_render_setpoint.sv, and changes exactly one behaviour through anchored
text replacements; each anchor must match exactly once or the script refuses.

Usage: make_mutants.py <edited milan_datapath.sv> <tree KL_render_setpoint.sv> <outdir>
"""
import pathlib
import sys

REBASE = "  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;\n"
RESTART_TAIL = "                       | media_rebase_p_w;\n"
RENDER = "       media_rebase_p_w | src_recentre_p_r;\n"
TALKER_EN = "    .stream_en_i (aaf_stream_en_w),\n    .dest_mac_i (eff_aaf_dmac),\n"


def delay_block(name: str, source: str, cycles: int, width: int) -> str:
    """A one-shot pulse `name` that fires `cycles` after `source` pulses."""
    return (
        f"  logic [{width - 1}:0] {name}_cnt_r;\n"
        f"  logic {name}_p_r;\n"
        f"  always_ff @(posedge axis_clk) begin : g_{name}\n"
        f"    if (!axis_resetn) begin\n"
        f"      {name}_cnt_r <= '0; {name}_p_r <= 1'b0;\n"
        f"    end else begin\n"
        f"      {name}_p_r <= 1'b0;\n"
        f"      if ({source}) {name}_cnt_r <= {width}'d{cycles};\n"
        f"      else if ({name}_cnt_r != '0) begin\n"
        f"        {name}_cnt_r <= {name}_cnt_r - 1'b1;\n"
        f"        if ({name}_cnt_r == {width}'d1) {name}_p_r <= 1'b1;\n"
        f"      end\n"
        f"    end\n"
        f"  end : g_{name}\n"
    )


def kill_block(cycles: int) -> str:
    """A sticky flag that stops the AAF packetizer `cycles` after the SECOND
    plane step (the first is the link-up step at acquisition)."""
    return (
        "  logic [20:0] rv_kill_cnt_r;\n"
        "  logic rv_kill_r;\n"
        "  logic rv_seen_r;\n"
        "  always_ff @(posedge axis_clk) begin : g_rv_kill\n"
        "    if (!axis_resetn) begin\n"
        "      rv_kill_cnt_r <= '0; rv_kill_r <= 1'b0; rv_seen_r <= 1'b0;\n"
        "    end else begin\n"
        "      if (gptp_step_we_w) rv_seen_r <= 1'b1;\n"
        f"      if (gptp_step_we_w && rv_seen_r && !rv_kill_r) rv_kill_cnt_r <= 21'd{cycles};\n"
        "      else if (rv_kill_cnt_r != '0) begin\n"
        "        rv_kill_cnt_r <= rv_kill_cnt_r - 1'b1;\n"
        "        if (rv_kill_cnt_r == 21'd1) rv_kill_r <= 1'b1;\n"
        "      end\n"
        "    end\n"
        "  end : g_rv_kill\n"
    )


def replace_once(text: str, old: str, new: str, what: str) -> str:
    n = text.count(old)
    if n != 1:
        sys.exit(f"anchor for {what} matched {n} times; refusing")
    return text.replace(old, new)


def main() -> int:
    dp_path, rsp_path, out = map(pathlib.Path, sys.argv[1:4])
    dp = dp_path.read_text()
    rsp = rsp_path.read_text()
    out.mkdir(parents=True, exist_ok=True)
    dp_variants = {
        # the mr restart keyed to the grandmaster identity, not the step
        "D1-restart-on-identity": [(RESTART_TAIL, "                       | gm_recentre_p_r;\n")],
        # the mr restart on the identity AND on the step
        "D2-restart-on-both": [(RESTART_TAIL,
                                "                       | media_rebase_p_w | gm_recentre_p_r;\n")],
        # the step's restart delayed 4000 cycles (about six talker intervals)
        "D3-restart-late-4000": [(REBASE, REBASE + delay_block("rv_rs", "media_rebase_p_w", 4000, 13)),
                                 (RESTART_TAIL, "                       | rv_rs_p_r;\n")],
        # the step's render re-centre delayed 1000 cycles (four AAF periods)
        "D4-render-late-1000": [(REBASE, REBASE + delay_block("rv_rc", "media_rebase_p_w", 1000, 11)),
                                (RENDER, "       rv_rc_p_r | src_recentre_p_r;\n")],
        # the talker stops for good 300000 / 600000 cycles after the step
        "D6-talker-stops-300k": [(REBASE, REBASE + kill_block(300000)),
                                 (TALKER_EN, TALKER_EN.replace("(aaf_stream_en_w)",
                                                               "(aaf_stream_en_w & {N_STREAMS{~rv_kill_r}})"))],
        "D7-talker-stops-600k": [(REBASE, REBASE + kill_block(600000)),
                                 (TALKER_EN, TALKER_EN.replace("(aaf_stream_en_w)",
                                                               "(aaf_stream_en_w & {N_STREAMS{~rv_kill_r}})"))],
    }
    for name, edits in dp_variants.items():
        text = dp
        for old, new in edits:
            text = replace_once(text, old, new, name)
        (out / f"{name}.milan_datapath.sv").write_text(text)
    # the recentre (not the prefill release or the rail) snaps one event short
    snap_old = ("              if (enough_w) begin\n"
                "                rptr_r[s]    <= snap_rptr_w;\n")
    snap_new = ("              if (enough_w) begin\n"
                "                rptr_r[s]    <= (pend_r[s] && !prefill_r[s]) ? snap_rptr_w + 1'b1\n"
                "                                                       : snap_rptr_w;\n")
    (out / "D5-recentre-snap-short.KL_render_setpoint.sv").write_text(
        replace_once(rsp, snap_old, snap_new, "D5"))
    print("\n".join(sorted(p.name for p in out.iterdir())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
