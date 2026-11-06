#!/usr/bin/env python3
"""Reviewer mutation arms on KL_srp_encoder.sv. Each arm is one exact text
replacement applied to a scratch copy. Usage: reviewer_mutants.py <tree> <arm>;
with no arm prints the arm names."""
import sys
ARMS = {
 "rv-last-one-early": ("((CNT_W_C'(sr_idx_r) + CNT_W_C'(1)) == tgt_cnt_w)", "((CNT_W_C'(sr_idx_r) + CNT_W_C'(2)) >= tgt_cnt_w)"),
 "rv-key-low-octets-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, 32'd0, v[239:208]};"),
 "rv-key-high-octets-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, v[271:240], 32'd0};"),
 "rv-key-unique-id-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, 48'd0, v[223:208]};"),
 "rv-key-domain-class-only": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, (t == ATTR_DOMAIN_C) ? {v[271:264], 56'd0} : v[271:208]};"),
 "rv-key-domain-no-vid": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, (t == ATTR_DOMAIN_C) ? {v[271:256], 48'd0} : v[271:208]};"),
 "rv-mvrp-key-low-byte": ("return {APP_MVRP_C, ATTR_MVRP_VID_C, v[271:256], 48'd0};", "return {APP_MVRP_C, ATTR_MVRP_VID_C, 8'd0, v[263:256], 48'd0};"),
 "rv-hit-counts-entry": ("if (push_msrp_w && !sr_hit_w) cnt_msrp_r", "if (push_msrp_w) cnt_msrp_r"),
 "rv-hit-counts-entry-mvrp": ("if (push_mvrp_w && !sr_hit_w) cnt_mvrp_r", "if (push_mvrp_w) cnt_mvrp_r"),
 "rv-msrp-hit-appends-addr": ("assign msrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_msrp_r[IDX_W_C-1:0];", "assign msrp_waddr_w = cnt_msrp_r[IDX_W_C-1:0];"),
 "rv-mvrp-hit-appends-addr": ("assign mvrp_waddr_w = sr_hit_w ? sr_idx_r : cnt_mvrp_r[IDX_W_C-1:0];", "assign mvrp_waddr_w = cnt_mvrp_r[IDX_W_C-1:0];"),
 "rv-mvrp-no-merge-rule": ("<= {sr_hit_w ? merge_ev_f(q_ev_w, ev_event_i) : ev_event_i, ev_value_i[271:256]};", "<= {ev_event_i, ev_value_i[271:256]};"),
 "rv-msrp-no-merge-rule": ("sr_hit_w ? merge_ev_f(q_ev_w, ev_event_i) : ev_event_i,\n            sr_hit_w ? merge_fp_f", "ev_event_i,\n            sr_hit_w ? merge_fp_f"),
 "rv-lv-then-join-keeps-lv": ("EV_JOININ_C, EV_JOINMT_C: return (old_e == EV_NEW_C) ? EV_NEW_C : new_e;", "EV_JOININ_C, EV_JOINMT_C: return ((old_e == EV_NEW_C) || (old_e == EV_LV_C)) ? old_e : new_e;"),
 "rv-join-keeps-older-join": ("EV_JOININ_C, EV_JOINMT_C: return (old_e == EV_NEW_C) ? EV_NEW_C : new_e;", "EV_JOININ_C, EV_JOINMT_C: return ((old_e == EV_NEW_C) || (old_e == EV_JOININ_C) || (old_e == EV_JOINMT_C)) ? old_e : new_e;"),
 "rv-s-keeps-older-s": ("EV_IN_C, EV_MT_C:         return ((old_e == EV_IN_C) || (old_e == EV_MT_C))\n                                       ? new_e : old_e;", "EV_IN_C, EV_MT_C:         return old_e;"),
 "rv-new-keeps-lv": ("default:                  return new_e;   // New, Lv", "default:                  return ((new_e == EV_NEW_C) && (old_e == EV_LV_C)) ? old_e : new_e;"),
 "rv-lv-keeps-new": ("default:                  return new_e;   // New, Lv", "default:                  return ((new_e == EV_LV_C) && (old_e == EV_NEW_C)) ? old_e : new_e;"),
 "rv-fp-always-newest": ("return (new_s && !old_s) ? old_fp : new_fp;", "return new_fp;"),
 "rv-fp-s-replaces-kept": ("return (new_s && !old_s) ? old_fp : new_fp;", "return (new_s) ? old_fp : new_fp;"),
 "rv-value-keeps-oldest": ("sr_hit_w ? merge_fp_f(q_ev_w, ev_event_i, q_fp_w, ev_fourpack_i)\n                     : ev_fourpack_i,\n            ev_value_i};", "sr_hit_w ? merge_fp_f(q_ev_w, ev_event_i, q_fp_w, ev_fourpack_i)\n                     : ev_fourpack_i,\n            sr_hit_w ? msrp_q_r[271:0] : ev_value_i};"),
 "rv-search-steals-drain-port": ("assign sr_engage_w = ev_valid_i && valid_type_w && base_ok_w && (tgt_cnt_w != '0);", "assign sr_engage_w = ev_valid_i && valid_type_w && !tgt_full_w && !start_tgt_w && (tgt_cnt_w != '0);"),
 "rv-push-on-drain-start": ("assign base_ok_w   = !tgt_full_w && !busy_app_w && !start_tgt_w;", "assign base_ok_w   = !tgt_full_w && !busy_app_w;"),
 "rv-restart-reads-next": ("assign sr_raddr_w  = sr_cont_w ? (sr_idx_r + IDX_W_C'(1)) : '0;", "assign sr_raddr_w  = sr_cont_w ? (sr_idx_r + IDX_W_C'(1)) : sr_idx_r;"),
 "rv-empty-table-searches": ("&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);", "&& (!valid_type_w || sr_hit_w || sr_last_w);"),
 "rv-invalid-type-searches": ("&& (!valid_type_w || (tgt_cnt_w == '0) || sr_hit_w || sr_last_w);", "&& ((tgt_cnt_w == '0) || sr_hit_w || sr_last_w);"),
 "rv-hit-only-first-entry": ("assign sr_hit_w    = sr_cont_w && (q_key_w == sr_key_r);", "assign sr_hit_w    = sr_cont_w && (sr_idx_r == '0) && (q_key_w == sr_key_r);"),
 "rv-q-event-from-offer": ("assign q_ev_w      = (ev_app_i == APP_MSRP_C) ? msrp_q_r[276:274] : mvrp_q_r[18:16];", "assign q_ev_w      = (ev_app_i == APP_MSRP_C) ? msrp_q_r[276:274] : ev_event_i;"),
 "rv-msrp-port-taken-by-any-search": ("assign msrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MSRP_C)) ? sr_raddr_w", "assign msrp_raddr_w = sr_engage_w ? sr_raddr_w"),
 "rv-mvrp-port-taken-by-any-search": ("assign mvrp_raddr_w = (sr_engage_w && (ev_app_i == APP_MVRP_C)) ? sr_raddr_w", "assign mvrp_raddr_w = sr_engage_w ? sr_raddr_w"),
 "rv-key-top-mac-octet-ignored": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, 8'd0, v[263:208]};"),
 "rv-search-survives-accept": ("end else if (!sr_engage_w || sr_hit_w || sr_last_w) begin", "end else if (!sr_engage_w) begin"),
}
if len(sys.argv) < 3:
    print("\n".join(ARMS)); sys.exit(0)
tree, arm = sys.argv[1], sys.argv[2]
p = tree + "/hdl/srp/KL_srp_encoder.sv"
s = open(p).read()
a, b = ARMS[arm]
assert s.count(a) == 1, (arm, s.count(a))
open(p, "w").write(s.replace(a, b))
