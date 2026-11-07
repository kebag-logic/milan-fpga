#!/usr/bin/env python3
"""make_arm_patches.py <tree>: write tb/srp_top/mutations/<arm>.patch for the round's new arms, each one exact text
replacement in hdl/srp/KL_srp_encoder.sv, as a three-line-context unified diff. Refuses an edit that does not match
exactly once."""
import difflib
import sys
from pathlib import Path

ENC = "hdl/srp/KL_srp_encoder.sv"
MVRP_WRITE = "<= {sr_hit_w ? merge_ev_f(q_ev_w, ev_event_i) : ev_event_i, ev_value_i[271:256]};"


def kept(old: str, new: str) -> str:
    """The MVRP write with one (pending, pushed) pair of the merge keeping the pending event."""
    return ("<= {sr_hit_w ? (((q_ev_w == " + old + ") && (ev_event_i == " + new + ")) ? q_ev_w\n"
            "                            : merge_ev_f(q_ev_w, ev_event_i)) : ev_event_i, ev_value_i[271:256]};")


ARMS = {
    "msrp-read-taken-by-any-search": (
        "assign msrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MSRP_C)) ? sr_raddr_w",
        "assign msrp_raddr_w = sr_engage_w ? sr_raddr_w"),
    "mvrp-read-taken-by-any-search": (
        "assign mvrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MVRP_C)) ? sr_raddr_w",
        "assign mvrp_raddr_w = sr_engage_w ? sr_raddr_w"),
    "identity-drops-top-octet": (
        "return {APP_MSRP_C, t, v[271:208]};",
        "return {APP_MSRP_C, t, 8'd0, v[263:208]};"),
    "identity-vid-low-octet-only": (
        "return {APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256], 48'd0};",
        "return {APP_MVRP_C, ATTR_MVRP_VID_C, 8'd0, v[263:256], 48'd0};"),
    "merge-keeps-older-value": (
        "            ev_value_i};\n    end\n    if (push_mvrp_w)",
        "            sr_hit_w ? msrp_q_r[271:0] : ev_value_i};\n    end\n    if (push_mvrp_w)"),
    "mvrp-merge-never-written": (
        "assign mvrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_mvrp_r[IDX_W_C-1:0];",
        "assign mvrp_waddr_w = cnt_mvrp_r[IDX_W_C-1:0];"),
    "mvrp-lv-keeps-joinin": (MVRP_WRITE, kept("EV_JOININ_C", "EV_LV_C")),
    "mvrp-lv-keeps-new": (MVRP_WRITE, kept("EV_NEW_C", "EV_LV_C")),
    "mvrp-new-keeps-lv": (MVRP_WRITE, kept("EV_LV_C", "EV_NEW_C")),
    "listener-type-s-over-s-kept": (
        "return (new_s && !old_s) ? old_fp : new_fp;",
        "return new_s ? old_fp : new_fp;"),
    "unknown-type-held-while-pending": (
        "&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);",
        "&& ((tgt_cnt_w == '0) || sr_hit_w || sr_last_w);"),
    "push-on-drain-start": (
        "assign base_ok_w   = !tgt_full_w && !busy_app_w && !start_tgt_w;",
        "assign base_ok_w   = !tgt_full_w && !busy_app_w;"),
    "search-survives-accept": (
        "end else if (!sr_engage_w || sr_hit_w || sr_last_w) begin",
        "end else if (!sr_engage_w) begin"),
}


def main() -> int:
    tree = Path(sys.argv[1])
    src = (tree / ENC).read_text()
    for arm, (old, new) in ARMS.items():
        assert src.count(old) == 1, (arm, src.count(old))
        lines = difflib.unified_diff(src.splitlines(keepends=True),
                                     src.replace(old, new).splitlines(keepends=True),
                                     fromfile="a/" + ENC, tofile="b/" + ENC, n=3)
        (tree / "tb/srp_top/mutations" / (arm + ".patch")).write_text("".join(lines))
        print(arm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
