#!/usr/bin/env python3
"""Plant one reviewer probe per disposable tree copy of hdl/ and tb/ (never the clone)."""
import pathlib, shutil, sys
ENC = "hdl/srp/KL_srp_encoder.sv"
P = {
 # the merge and search rules, beyond the author's arms
 "rv-search-stops-one-early": ("((CNT_W_C'(sr_idx_r) + CNT_W_C'(1)) == tgt_cnt_w)", "((CNT_W_C'(sr_idx_r) + CNT_W_C'(2)) >= tgt_cnt_w)"),
 "rv-key-mac-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, v[271:224], 16'd0};"),
 "rv-key-uid-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, 48'd0, v[223:208]};"),
 "rv-key-low-mac-ignored": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, 8'd0, v[263:208]};"),
 "rv-merge-keeps-old-value": ("            ev_value_i};\n    end\n    if (push_mvrp_w)", "            sr_hit_w ? msrp_q_r[271:0] : ev_value_i};\n    end\n    if (push_mvrp_w)"),
 "rv-mvrp-no-merge": ("<= {sr_hit_w ? merge_ev_f(q_ev_w, ev_event_i) : ev_event_i, ev_value_i[271:256]};", "<= {ev_event_i, ev_value_i[271:256]};"),
 "rv-search-steals-other-read": ("assign msrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MSRP_C)) ? sr_raddr_w", "assign msrp_raddr_w = (sr_engage_w) ? sr_raddr_w"),
 "rv-search-steals-other-read-mvrp": ("assign mvrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MVRP_C)) ? sr_raddr_w", "assign mvrp_raddr_w = (sr_engage_w) ? sr_raddr_w"),
 "rv-hit-still-counts": ("if (push_msrp_w && !sr_hit_w) cnt_msrp_r", "if (push_msrp_w) cnt_msrp_r"),
 "rv-hit-still-counts-mvrp": ("if (push_mvrp_w && !sr_hit_w) cnt_mvrp_r", "if (push_mvrp_w) cnt_mvrp_r"),
 "rv-hit-writes-append-slot": ("assign msrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_msrp_r[IDX_W_C-1:0];", "assign msrp_waddr_w = cnt_msrp_r[IDX_W_C-1:0];"),
 "rv-join-over-lv-kept-lv": ("EV_JOININ_C, EV_JOINMT_C: return (old_e == EV_NEW_C) ? EV_NEW_C : new_e;", "EV_JOININ_C, EV_JOINMT_C: return ((old_e == EV_NEW_C) || (old_e == EV_LV_C)) ? old_e : new_e;"),
 "rv-join-keeps-older-reading": ("EV_JOININ_C, EV_JOINMT_C: return (old_e == EV_NEW_C) ? EV_NEW_C : new_e;", "EV_JOININ_C, EV_JOINMT_C: return ((old_e == EV_NEW_C) || (old_e == EV_JOININ_C) || (old_e == EV_JOINMT_C)) ? old_e : new_e;"),
 "rv-s-keeps-older-reading": ("? new_e : old_e;\n      default:", "? old_e : old_e;\n      default:"),
 "rv-new-does-not-replace-lv": ("default:                  return new_e;   // New, Lv", "default:                  return ((new_e == EV_NEW_C) && (old_e == EV_LV_C)) ? old_e : new_e;   // New, Lv"),
 "rv-fp-keeps-old-under-kept-new": ("return (new_s && !old_s) ? old_fp : new_fp;", "return ((new_s && !old_s) || (old_e == EV_NEW_C)) ? old_fp : new_fp;"),
 "rv-fp-s-takes-new": ("return (new_s && !old_s) ? old_fp : new_fp;", "return new_fp;"),
 "rv-search-ignores-start": ("assign sr_engage_w = ev_valid_i && valid_type_w && base_ok_w && (tgt_cnt_w != '0);", "assign sr_engage_w = ev_valid_i && valid_type_w && !tgt_full_w && !busy_app_w && (tgt_cnt_w != '0);"),
 "rv-sr-on-survives-accept": ("end else if (!sr_engage_w || sr_hit_w || sr_last_w) begin", "end else if (!sr_engage_w) begin"),
 "rv-full-table-merges-blocked-removed": ("assign base_ok_w   = !tgt_full_w && !busy_app_w && !start_tgt_w;", "assign base_ok_w   = !busy_app_w && !start_tgt_w;"),
}
def main():
    src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
    names = sys.argv[3:] or list(P)
    for n in names:
        a, b = P[n]
        t = out / n
        if t.exists(): shutil.rmtree(t)
        t.mkdir(parents=True)
        shutil.copytree(src / "hdl", t / "hdl")
        for s in ("common", "srp_top", "srp_encoder"):
            shutil.copytree(src / "tb" / s, t / "tb" / s, ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
        f = t / ENC; x = f.read_text()
        assert x.count(a) == 1, n
        f.write_text(x.replace(a, b))
        print(n)
main()
