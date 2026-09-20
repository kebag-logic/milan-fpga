#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Which NAMED checks each case of the contract page's section 9 is graded by.

This is the map the page's ordering table becomes: one entry per case, each
naming the checks `cosim_checks.py` builds, plus the four lists that say where
a case may run -- the shapes, the cases a PRE-CONTRACT build cannot express,
the cases that run on the slots another case left, and the three historical
defects that MUST reproduce on that build.

`run_cases.py` reads this module and nothing else of the grading side.
"""
from __future__ import annotations

from cosim_oracle import Ctx, Run, ShapeInfo, _erased
from cosim_checks import (
    _c_ack_only_slot, _c_alarm_revokes, _c_arm_edge_deferred, _c_arm_in_gap,
    _c_arm_refused, _c_arm_refused_no_load, _c_arm_refused_while_deferred,
    _c_attest_intact, _c_attest_voided, _c_bits, _c_boot_load_closed,
    _c_closed_equals_load, _c_converged, _c_copy_in_gap, _c_deferred,
    _c_dirty_img, _c_early_ack, _c_every_slot, _c_failure_revokes,
    _c_first_boot_blank, _c_grant_wins_rebase, _c_hb_gap, _c_held_work,
    _c_hold_bounded, _c_hold_bounded_chained, _c_inflight_at_arm,
    _c_landed_or_reported, _c_late_ack, _c_no_101, _c_no_capture_no_load,
    _c_no_churn_pend, _c_no_claim_over_erased_live, _c_no_durable_claim,
    _c_no_loss, _c_no_uncert_flash, _c_nothing_durable_when_closed,
    _c_own_ack_ok, _c_own_exact_after_arm, _c_pend_bit,
    _c_producer_never_blocked, _c_reattached, _c_rec, _c_rec_in,
    _c_refused_ack, _c_refused_open, _c_reload_retried,
    _c_repeat_stops_when_live, _c_reset_row, _c_restart_stays_retired,
    _c_restart_takes_no_cold_boot, _c_restore, _c_slow_copy, _c_stable,
    _c_stale_id_refused, _c_stuck_reported, _c_terminal_row,
    _c_unmaterialized, _c_unres_bits, _c_write_spans_fill,
    _c_writer_retired, _ck, _strobes)

def _later(tag, rid, key):
    return _c_rec(tag, rid, key, "later_record_persists")


def _kept(tag, rid, key):
    return _c_rec(tag, rid, key, "last_verified_kept")


CHECKS = {
    "A1_stable_no_change": [_c_converged("end", {0x20: "X", 0x21: "Z"}), _c_stable("base", "end")],
    "A2_write_between_verify_and_ack": [_c_ack_only_slot("post_ack", 0x20, "X2"),
                                        _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A3_write_done_on_ack_edge": [_c_ack_only_slot("post_ack", 0x20, "X2"),
                                  _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A4_write_after_ack": [_c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A5_stray_duplicate_ack": [_c_ack_only_slot("after_stray", 0x20, "X2"),
                               _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A6_late_ack_while_new_capture_open": [_c_stale_id_refused("stray"),
                                           _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "A8_identity_wrap": [_c_ack_only_slot("end", 0x20, "X2")],
    "A9_updates_during_slow_erase": [_c_converged("end", {0x20: "X3", 0x21: "Z"}), _c_no_loss(),
                                     _c_hb_gap(500)],
    "A11_inflight_write_closes_after_arm": [_c_inflight_at_arm(0x21),
                                            _c_rec("first", 0x21, "Z", "inflight_record_excluded"),
                                            _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "A12_last_byte_before_arm_done_after": [_c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "B5_erase_then_no_write_yet": [_kept("gap", 0x20, "X"), _later("gap", 0x21, "Z2"),
                                   _c_no_durable_claim("gap", {0x20: "X3"}),
                                   _c_converged("end", {0x20: "X3", 0x21: "Z2"})],
    "B7_first_boot_erased_records": [_c_first_boot_blank("blank_commit"),
                                     _c_converged("end", {0x20: "X"})],
    "B8_first_boot_failed_erase": [_later("end", 0x21, "Z"),
                                   _ck("never_written_record_stays_erased@end:0x20",
                                      lambda c: (_erased(c.rec("end", 0x20)), "record 0x20 erased"))],
    "B9_abandoned_write_stream": [_later("abandoned", 0x20, "X2"), _kept("abandoned", 0x21, "Z"),
                                  _c_stuck_reported("abandoned"),
                                  _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "B10_partial_write_never_closes": [_kept("end", 0x20, "X"), _later("end", 0x21, "Z2")],
    "C1_request_during_hold_is_deferred": [_c_deferred(0x21),
                                           _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2_hold_expiry_then_erase_with_stale_mask": [
        _c_hold_bounded(0x21), _c_no_uncert_flash(), _kept("after", 0x21, "Z"),
        _later("after", 0x20, "X2"), _c_converged("end", {0x20: "X2", 0x21: "Z3"})],
    "C1r_real_port_request_deferred": [_c_deferred(0x21, "port"),
                                       _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2r_real_port_torn_record_under_stale_mask": [
        _c_hold_bounded(0x21, "port"), _c_no_uncert_flash(),
        _c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        _later("after", 0x20, "X2"), _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C2e_real_port_erased_span_under_stale_mask": [
        _c_hold_bounded(0x21, "port"), _c_no_uncert_flash(),
        _c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        _later("after", 0x20, "X2"), _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C1a_real_port_arm_after_erase_done": [
        _c_arm_in_gap(0x21), _c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        _later("after", 0x20, "X2"), _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C1g_real_port_copy_inside_erase_write_gap": [
        _c_copy_in_gap(0x21), _c_rec_in("after", 0x21, ["Z", "Z2"], "never_torn_or_erased"),
        _later("after", 0x20, "X2"), _c_converged("end", {0x20: "X2", 0x21: "Z2"})],
    "C3_hold_expiry_without_producer": [_c_slow_copy(), _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C5_concurrent_arm_refused": [_c_arm_refused("stray"), _c_own_ack_ok(),
                                  _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C7_late_ack_after_commit_deadline": [_c_late_ack("pre_hb"), _c_bits("end", 1, 0, 0),
                                          _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "C8_ack_refused_after_verified_slot": [
        _c_refused_ack("pre_hb"),
        _c_rec("pre_hb", 0x20, "X2", "attested_slot_promoted"),
                                           _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "D1_writer_loss_and_recovery": [_c_bits("lost", 0, 0, 1), _c_bits("back", 1, 0, 0),
                                    _c_bits("lost2", 0, 1, 1), _c_bits("end", 1, 0, 0),
                                    _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "E1_dyn_change_ack_then_second_change": [_c_unmaterialized("first"), _c_unmaterialized("end"),
                                             _c_no_churn_pend("end")],
    "E3_binding_inside_manager_debounce": [_c_no_durable_claim("in_debounce", {0x20: "X2"}),
                                           _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "F2_reported_flash_failure": [_c_failure_revokes(False), _c_failure_revokes(True),
                                  _kept("failed", 0x20, "X"),
                                  _ck("stale_until_good_commit@failed",
                                     lambda c: (c.o("failed")["stale"] == 1, f"stale {c.o('failed')['stale']}")),
                                  _c_bits("end", 1, 0, 0), _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    "F3_flash_absent_producer_unblocked": [_c_producer_never_blocked(), _kept("end", 0x20, "X"),
                                           _kept("end", 0x21, "Z"), _c_dirty_img("end", 1, "work_still_owned"),
                                           _ck("manager_flushed_everything@end",
                                              lambda c: (
                                                  c.o("end")["mgr_dirty"] == 0,
                                                  "manager dirty "
                                                  f"{c.o('end')['mgr_dirty']}"))],
    "U1_post_reset_ack": [_c_dirty_img("after", 1, "post_reset_ack_retires_nothing")],
    "U2_close_on_arm_edge": [_c_dirty_img("acked", 1, "close_on_arm_edge_stays_live")],
    "U3_grant_on_attest_edge": [_c_attest_voided("attest")],
    # revision b
    "U4_grant_request_on_arm_edge": [_c_arm_edge_deferred(0x20), _c_own_exact_after_arm("arm", 0x20),
                                     _c_attest_intact("attest", 0x20, "X")],
    "U5_reload_refused_inflight_at_rebase": [
        _c_refused_open("after", 0x20, "reload_refused_inflight_at_rebase"),
        _c_closed_equals_load("after", 0x20, "X")],
    "U6_reload_refused_after_boot": [_c_refused_open("gap", 0x21, "gap_record_stays_open"),
                                     _c_refused_open("inflight", 0x21, "inflight_record_stays_open"),
                                     _c_held_work("reload")],
    "U7_reset_row_and_pre_reset_ack": [_c_reset_row("reset"), _c_early_ack("early_ack"),
                                       _c_dirty_img("after", 1, "post_reset_ack_retires_nothing")],
    "R1_reload_after_failed_erase": [_c_reload_retried("boot"), _kept("end", 0x20, "X"),
                                     _c_every_slot("end", 0x20, "X"), _later("end", 0x21, "Z2"),
                                     _c_no_claim_over_erased_live("boot", 0x20),
                                     _c_no_claim_over_erased_live("end", 0x20),
                                     _c_converged("end", {0x20: "X", 0x21: "Z2"})],
    "W1_writer_restart_reattaches": [_c_reattached("restarted"),
                                     _c_no_durable_claim("restarted", {0x20: "X2"}),
                                     _c_converged("end", {0x20: "X2", 0x21: "Z"})],
    # revision c
    "U8_grant_on_rebase_edge": [_c_grant_wins_rebase("after", 0x20),
                                _c_closed_equals_load("after", 0x20, "X")],
    "U10_arm_refused_while_request_deferred": [_c_hold_bounded_chained(0x21),
                                               _c_arm_refused_while_deferred("arm2")],
    "U9_four_window_loads_refused": [_c_terminal_row("boot", (0, 0, 0), "refused 4 window loads",
                                                    "four_refusal_terminal_row"),
                                     _c_boot_load_closed("boot"),
                                     _c_writer_retired("end"),
                                     _kept("end", 0x20, "X"), _c_every_slot("end", 0x20, "X"),
                                     _c_no_claim_over_erased_live("boot", 0x20),
                                     _c_landed_or_reported("end", 0x21, "Z2")],
    # revision d: W2's expectation CHANGES. The restarted writer no longer
    # re-attaches and no longer commits what the window holds, so the
    # accepted change ends REPORTED beside the intact slot instead of in a
    # verified slot, and nothing in this boot reads durable.
    "W2_restart_after_refused_loads": [_c_restart_takes_no_cold_boot("restarted"),
                                       _c_restart_stays_retired("restarted"),
                                       _c_no_claim_over_erased_live("restarted", 0x20),
                                       _kept("end", 0x20, "X"), _c_every_slot("end", 0x20, "X"),
                                       _c_writer_retired("end"),
                                       _c_landed_or_reported("end", 0x21, "Z2")],
    # revision d
    "U11_arm_refused_without_accepted_load": [_c_arm_refused_no_load("stray"),
                                              _c_no_capture_no_load("end")],
    "U12_window_live_stops_the_repeat": [_c_repeat_stops_when_live("boot", 1),
                                         _c_writer_retired("end"),
                                         _kept("end", 0x20, "X"), _c_every_slot("end", 0x20, "X"),
                                         _c_landed_or_reported("end", 0x21, "Z2")],
    "U13_four_refusals_with_the_device_busy": [
        _c_terminal_row("boot", (1, 1, 0), "refused 4 window loads",
                        "terminal_row_writer_was_live"),
        _c_terminal_row("end", (0, 1, 1), "refused 4 window loads",
                        "terminal_row_after_the_loss"),
        _kept("end", 0x20, "X"), _c_every_slot("end", 0x20, "X"),
        _c_landed_or_reported("end", 0x21, "Z")],
    "W3_write_across_refused_fill_then_restart": [_c_write_spans_fill("live", 0x21),
                                                  _c_restart_stays_retired("restarted"),
                                                  _c_writer_retired("end"),
                                                  _kept("end", 0x20, "X"),
                                                  _c_every_slot("end", 0x20, "X"),
                                                  _c_landed_or_reported("end", 0x21, "Z2")],
    "W4_all_records_rewritten_after_refused_fill": [_c_write_spans_fill("live", 0x21),
                                                    _c_restart_stays_retired("restarted"),
                                                    _c_nothing_durable_when_closed("rewritten"),
                                                    _c_nothing_durable_when_closed("end2"),
                                                    _kept("end2", 0x20, "X"),
                                                    _c_every_slot("end2", 0x20, "X")],
}
for name in ("B1_erase_error_full_span", "B2_erase_error_partial_span",
             "B3_erase_error_no_byte", "B4_write_error_after_erase"):
    CHECKS[name] = [_kept("end", 0x20, "X"), _later("end", 0x21, "Z2"),
                    _c_no_durable_claim("end", {0x20: "X2", 0x21: "Z2"}),
                    _c_alarm_revokes("gave_up"), _c_alarm_revokes("end")]
for name in ("B6_two_failed_records_partial", "B6b_two_failed_records_full"):
    CHECKS[name] = [_kept("end", 0x20, "X"), _c_rec("end", 0x30, "FMT_A", "last_verified_kept"),
                    _later("end", 0x21, "Z2"), _c_unres_bits("end", [0x20, 0x30])]
for name in ("D4c_accepted_write_silent", "D4d_readiness_withheld", "D4e_silent_inside_capture"):
    CHECKS[name] = [_later("stuck", 0x20, "X2"), _kept("stuck", 0x21, "Z"), _c_stuck_reported("stuck")]
POWER_CYCLE = {   # case -> the bindings a power cycle must restore
    "B1_erase_error_full_span": {0: "X", 1: "Z2"},
    "B2_erase_error_partial_span": {0: "X", 1: "Z2"},
    "B4_write_error_after_erase": {0: "X", 1: "Z2"},
    "B9_abandoned_write_stream": {0: "X2", 1: "Z2"},
}
#: cases a PRE-CONTRACT writer cannot express (they hook contract-3 _strobes)
CONTRACT_ONLY = {"A6_late_ack_while_new_capture_open", "A8_identity_wrap",
                 "C1r_real_port_request_deferred", "C2r_real_port_torn_record_under_stale_mask",
                 "C2e_real_port_erased_span_under_stale_mask",
                 "C1a_real_port_arm_after_erase_done", "C1g_real_port_copy_inside_erase_write_gap",
                 "A11_inflight_write_closes_after_arm", "A12_last_byte_before_arm_done_after",
                 "C1_request_during_hold_is_deferred", "C2_hold_expiry_then_erase_with_stale_mask",
                 "C3_hold_expiry_without_producer", "C5_concurrent_arm_refused",
                 "C8_ack_refused_after_verified_slot", "D4e_silent_inside_capture",
                 "U2_close_on_arm_edge", "U3_grant_on_attest_edge",
                 "U4_grant_request_on_arm_edge", "U5_reload_refused_inflight_at_rebase",
                 "U6_reload_refused_after_boot", "U7_reset_row_and_pre_reset_ack",
                 "R1_reload_after_failed_erase", "W1_writer_restart_reattaches",
                 "U8_grant_on_rebase_edge", "U10_arm_refused_while_request_deferred",
                 "U9_four_window_loads_refused", "W2_restart_after_refused_loads",
                 "U11_arm_refused_without_accepted_load", "U12_window_live_stops_the_repeat",
                 "U13_four_refusals_with_the_device_busy",
                 "W3_write_across_refused_fill_then_restart",
                 "W4_all_records_rewritten_after_refused_fill"}
#: cases that run AFTER another case of the same build, on the slots it left
#: (the reviewers' RELOAD ordering starts from a verified slot A holding X)
DEPENDENT = {"R1_reload_after_failed_erase": "A1_stable_no_change",
             "U9_four_window_loads_refused": "A1_stable_no_change",
             "W2_restart_after_refused_loads": "A1_stable_no_change",
             "U12_window_live_stops_the_repeat": "A1_stable_no_change",
             "U13_four_refusals_with_the_device_busy": "A1_stable_no_change",
             "W3_write_across_refused_fill_then_restart": "A1_stable_no_change",
             "W4_all_records_rewritten_after_refused_fill": "A1_stable_no_change"}
#: the prototype's EXPECTED failures, each with its reason
PROTO_EXPECTED_FAIL = {
    ("E3_binding_inside_manager_debounce", "d1=0", "no_durable_claim@in_debounce"):
        "without donor scope D1 the parent cannot see a change the manager is debouncing",
}
#: checks the TRACKED build must fail: the #418 race, the ERASE-error
#: counterexample and the #420 one-pulse re-arm failure
PROD_MUST_FAIL = [
    ("A2_write_between_verify_and_ack", "ack_retires_only_slot@post_ack:0x20", "#418 ACK race"),
    ("B1_erase_error_full_span", "last_verified_kept@end:0x20", "round-1 ERASE-error counterexample"),
    ("E1_dyn_change_ack_then_second_change", "no_durable_claim_unmaterialized@end", "#420 one-pulse re-arm"),
]
CORE_8X8 = ["A2_write_between_verify_and_ack", "A3_write_done_on_ack_edge", "B1_erase_error_full_span",
            "B2_erase_error_partial_span", "B5_erase_then_no_write_yet", "B6_two_failed_records_partial",
            "B9_abandoned_write_stream", "C1_request_during_hold_is_deferred",
            "C2_hold_expiry_then_erase_with_stale_mask", "D1_writer_loss_and_recovery",
            "E1_dyn_change_ack_then_second_change",
            # revision b: the load, the arm edge and the reset row at the other shape
            "A1_stable_no_change", "R1_reload_after_failed_erase", "U4_grant_request_on_arm_edge",
            "U5_reload_refused_inflight_at_rebase", "U6_reload_refused_after_boot",
            "U7_reset_row_and_pre_reset_ack",
            # the boot that accepts no load, the writer restarts and the
            # record closed across a refused fill: each follows A1 on every
            # build that runs it, so the other shape gets them for free
            "U9_four_window_loads_refused", "U12_window_live_stops_the_repeat",
            "U13_four_refusals_with_the_device_busy",
            "W2_restart_after_refused_loads",
            "W3_write_across_refused_fill_then_restart",
            "W4_all_records_rewritten_after_refused_fill",
            # issue #484: the accepted-load term is shape-independent, and the
            # acceptance review asked for it to be shown so at the other shape
            "U11_arm_refused_without_accepted_load"]


#: which producer drives each case: "real" is the pinned donor manager
#: and port, "bfm" the device-face bus-functional model, "stray" a strobe
#: the harness writes on the control face, and "unit" no firmware at all
PRODUCER = {
    'A11_inflight_write_closes_after_arm': 'real + bfm',
    'A12_last_byte_before_arm_done_after': 'real + bfm',
    'A1_stable_no_change': 'real',
    'A2_write_between_verify_and_ack': 'real, #418',
    'A3_write_done_on_ack_edge': 'bfm, #418 control',
    'A4_write_after_ack': 'real',
    'A5_stray_duplicate_ack': 'real + stray',
    'A6_late_ack_while_new_capture_open': 'real + stray',
    'A8_identity_wrap': 'real + stray',
    'A9_updates_during_slow_erase': 'real',
    'B10_partial_write_never_closes': 'real + bfm',
    'B1_erase_error_full_span': 'real',
    'B2_erase_error_partial_span': 'real',
    'B3_erase_error_no_byte': 'real',
    'B4_write_error_after_erase': 'real',
    'B5_erase_then_no_write_yet': 'real + bfm',
    'B6_two_failed_records_partial': 'real + bfm',
    'B6b_two_failed_records_full': 'real + bfm',
    'B7_first_boot_erased_records': 'real',
    'B8_first_boot_failed_erase': 'real + bfm',
    'B9_abandoned_write_stream': 'real + bfm',
    'C1_request_during_hold_is_deferred': 'real + bfm',
    'C1a_real_port_arm_after_erase_done': 'real',
    'C1g_real_port_copy_inside_erase_write_gap': 'real',
    'C1r_real_port_request_deferred': 'real',
    'C2_hold_expiry_then_erase_with_stale_mask': 'real + bfm',
    'C2e_real_port_erased_span_under_stale_mask': 'real',
    'C2r_real_port_torn_record_under_stale_mask': 'real',
    'C3_hold_expiry_without_producer': 'real',
    'C5_concurrent_arm_refused': 'real + stray',
    'C7_late_ack_after_commit_deadline': 'real',
    'C8_ack_refused_after_verified_slot': 'real + stray',
    'D1_writer_loss_and_recovery': 'real',
    'D4c_accepted_write_silent': 'real',
    'D4d_readiness_withheld': 'real',
    'D4e_silent_inside_capture': 'real',
    'E1_dyn_change_ack_then_second_change': 'real dyn store',
    'E3_binding_inside_manager_debounce': 'real',
    'F2_reported_flash_failure': 'real',
    'F3_flash_absent_producer_unblocked': 'real',
    'U1_post_reset_ack': 'unit',
    'U2_close_on_arm_edge': 'unit',
    'U3_grant_on_attest_edge': 'unit',
}


PRODUCER.update({"U4_grant_request_on_arm_edge": "unit", "U5_reload_refused_inflight_at_rebase": "unit",
                 "U6_reload_refused_after_boot": "unit", "U7_reset_row_and_pre_reset_ack": "unit",
                 "R1_reload_after_failed_erase": "real + bfm, slots of A1",
                 "W1_writer_restart_reattaches": "real, writer restart model",
                 "U8_grant_on_rebase_edge": "unit",
                 "U10_arm_refused_while_request_deferred": "unit",
                 "U9_four_window_loads_refused": "real + bfm, slots of A1",
                 "W2_restart_after_refused_loads": "real + bfm, restart model, slots of A1",
                 "U11_arm_refused_without_accepted_load": "unit",
                 "U12_window_live_stops_the_repeat": "real + bfm, slots of A1",
                 "U13_four_refusals_with_the_device_busy": "real + bfm, slots of A1",
                 "W3_write_across_refused_fill_then_restart":
                     "real + bfm, restart model, slots of A1",
                 "W4_all_records_rewritten_after_refused_fill":
                     "real + bfm, restart model, slots of A1"})


def grade(run: Run, s: ShapeInfo) -> dict:
    """Every named check of one run: pass, fail, n/a (not expressible)."""
    c = Ctx(run, s)
    out = {}
    if run.exit != 0 or not run.done:
        return {"_harness": ("fail", f"exit {run.exit}, finished {run.done}")}
    if run.case.startswith("R_power_cycle"):
        base = run.variant.split("@")[0]
        return {n: ("pass" if ok else "fail", d) for n, (ok, d) in
                [(nm, f(c)) for nm, f in [_c_restore("restored", POWER_CYCLE[base])]]}
    checks = list(CHECKS.get(run.case, [])) + [_c_no_101(), _c_pend_bit()]
    if run.pending:
        return {n: ("n/a", "the hook this case needs never fired on this build")
                for n, _ in checks}
    for name, fn in checks:
        try:
            ok, detail = fn(c)
        except KeyError as e:
            ok, detail = False, f"missing: {e}"
        out[name] = ("n/a" if ok is None else "pass" if ok else "fail", detail)
    return out

