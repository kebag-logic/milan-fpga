#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant ONE named defect in a copy of a shipping source.

Every entry is the defect the snapshot-ownership contract page names, and
``run_cases.py`` runs each one against the SINGLE CHECK the page names as its
killer. A seam is matched EXACTLY and must hit exactly once, so a line that
moves breaks this file rather than letting a mutant compile unchanged and
report a vacuous pass.

    python3 mutate.py <rtl|fw|glue> <name> <src> <dst>

`rtl` mutates hdl/milan/KL_nvm_backend.sv, `fw` the shipping writer
sw/firmware/milan_baremetal/milan_baremetal.c, and `glue` this suite's
cosim_top.sv, which carries the parent wiring transcribed from
hdl/milan/KL_pp_shadow.sv. A COMBINED entry names a rule that lives in two
files and is reverted in both, so a review finding is reproduced whole.
"""
import sys
from pathlib import Path

#: name -> (which source, [(exact text, replacement), ...])
MUTANTS = {'A01_composite_durable_bit': ('rtl',
                               [('  assign nvm_dirty_o   = dirty_img_w;\n',
                                 '  assign nvm_dirty_o   = dirty_img_w | nvm_pend_o;\n'),
                                ('                                     nvm_stale_o, '
                                 'dirty_img_w, img_valid_r,\n',
                                 '                                     nvm_stale_o, '
                                 '(dirty_img_w | nvm_pend_o), img_valid_r,\n'),
                                ('  assign comp_n_w  = dirty_live_n_w | dirty_cap_n_w;\n',
                                 '  assign comp_n_w  = dirty_live_n_w | dirty_cap_n_w | pend_i '
                                 '| unres_w;\n')]),
 'F01_attestation_not_checked': ('fw',
                                 [('\tif (!(milan_read(MILAN_PP_NVM_STAT) & '
                                   'NVM_RD_CAP_ATTEST)) {\n',
                                   '\tif (!(milan_read(MILAN_PP_NVM_STAT) & NVM_RD_CAP_ATTEST) '
                                   '&& 0) {\n')]),
 'F02_copies_open_records': ('fw',
                             [('\t\tcopy = !((own[rec.id >> 5] >> (rec.id & 31u)) & 1u);\n',
                               '\t\tcopy = !((own[rec.id >> 5] >> (rec.id & 31u)) & 0u);\n')]),
 'F03_prefill_from_blank': ('fw',
                            [('\tif (nvm_auth_slot == NVM_SLOT_NONE) {\n'
                              '\t\tnvm_stage_blank_image();\n',
                              '\tif (1) {\n\t\tnvm_stage_blank_image();\n')]),
 'F04_ack_without_identity': ('fw',
                              [('\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK | (cap.id << '
                                '16));\n',
                                '\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK);\n')]),
 'F05_device_busy_gate_kept': ('fw',
                               [('\tif (stat & NVM_RD_COMMIT_BUSY)\n\t\treturn;\n',
                                 '\tif (stat & (NVM_RD_DEV_BUSY | NVM_RD_COMMIT_BUSY))\n'
                                 '\t\treturn;\n')]),
 'F06_ack_after_failed_slot': ('fw',
                               [('\t\tnvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | vd);\n'
                                 '\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_RELEASE);\n',
                                 '\t\tnvm_csr_write(NVM_W_STAT, NVM_STAT_VALID | vd);\n'
                                 '\t\tmilan_write(MILAN_PP_NVM_STAT, NVM_STROBE_ACK | (cap.id '
                                 '<< 16));\n')]),
 'F07_reload_refusal_ignored': ('fw',
                                [('\treturn !(milan_read(MILAN_PP_NVM_STAT) & '
                                  'NVM_RD_RELOAD_REF);\n',
                                  '\t(void)milan_read(MILAN_PP_NVM_STAT);\n\treturn 1;\n')]),
 'F08_restart_reloads_window': ('fw',
                                [('\t} else if (!(stat & NVM_RD_LOAD_PEND)) {\n',
                                  '\t} else if (0) {\n')]),
 'F10_retired_writer_keeps_heartbeating': ('fw',
                                           [('\tif (nvm_retired)\n\t\treturn;\n',
                                             '\tif (0)\n\t\treturn;\n')]),
 'F11_restart_reattaches_without_load': ('fw',
                                         [('\t} else if (!(stat & NVM_RD_LOAD_PEND) && !(stat '
                                           '& NVM_RD_LOAD_ACC)) {\n',
                                           '\t} else if (0) {\n')]),
 'F12_repeat_ignores_window_live': ('fw',
                                    [('\t\t\tif (!loaded && !(milan_read(MILAN_PP_NVM_STAT) & '
                                      'NVM_RD_LOAD_PEND)) {\n',
                                      '\t\t\tif (0) {\n')]),
 'G01_edge_detected_change': ('glue',
                              [('  assign pend_w = aecp_dyn_dirty_w | '
                                '(|mgr_dirty_w);\n',
                                '  logic dyn_q_mut;\n'
                                '  always_ff @(posedge clk_i) dyn_q_mut <= aecp_dyn_dirty_w;\n'
                                '  assign pend_w = (aecp_dyn_dirty_w & ~dyn_q_mut) | '
                                '(|mgr_dirty_w);\n')]),
 'M01_open_at_erase_completion': ('rtl',
                                  [('                          | (set_q_r & hit_w)\n',
                                    '                          | (done_r & ~was_write_r & '
                                    'op_mut_r & hit_w)\n')]),
 'M02_close_on_any_completion': ('rtl',
                                 [('  assign rec_close_w = done_r & was_write_r & op_mut_r & '
                                   'op_full_r;\n',
                                   '  assign rec_close_w = done_r & op_mut_r;\n')]),
 'M03_close_on_partial_write': ('rtl',
                                [('  assign rec_close_w = done_r & was_write_r & op_mut_r & '
                                  'op_full_r;\n',
                                  '  assign rec_close_w = done_r & was_write_r & '
                                  'op_mut_r;\n')]),
 'M04_ack_ignores_identity': ('rtl',
                              [('                     & (ack_id_w == cap_id_r) & '
                                '~void_hard_w;\n',
                                '                     & ~void_hard_w;\n')]),
 'M05_ack_retires_live_work': ('rtl',
                               [("  assign dirty_live_n_w = rec_close_w ? 1'b1\n"
                                 "                        : reload_ok_w ? 1'b0\n",
                                 "  assign dirty_live_n_w = rec_close_w ? 1'b1\n"
                                 "                        : ack_ok_w    ? 1'b0\n"
                                 "                        : reload_ok_w ? 1'b0\n")]),
 'M06_hold_does_not_defer': ('rtl',
                             [('  assign gnt_now_w   = (st_r == S_IDLE) && dev_req_i\n'
                               '                     && !((cap_hold_r | arm_ok_w) && '
                               'mut_req_w);\n',
                               '  assign gnt_now_w   = (st_r == S_IDLE) && dev_req_i;\n')]),
 'M07_hold_never_expires': ('rtl',
                            [('  assign hold_exp_w  = cap_hold_r & ms_tick_w & (hold_r == '
                              "HOLD_W_C'(1));\n",
                              "  assign hold_exp_w  = 1'b0;\n")]),
 'M08_attestation_ignores_grant': ('rtl',
                                   [('  assign att_ok_w    = attest_w & cap_open_r & '
                                     '~cap_att_r & cap_valid_r\n'
                                     '                     & ~void_grant_w & ~void_hard_w;\n',
                                     '  assign att_ok_w    = attest_w & cap_open_r & '
                                     '~cap_att_r & ~void_hard_w;\n')]),
 'M09_second_arm_accepted': ('rtl',
                             [('  assign arm_ok_w    = arm_w & img_cfg_w & img_valid_r & '
                               '~cap_open_r & ~void_hard_w\n'
                               '                     & ~mut_defer_r & ld_acc_r;\n',
                               '  assign arm_ok_w    = arm_w & img_cfg_w & img_valid_r & '
                               '~void_hard_w\n'
                               '                     & ~mut_defer_r & ld_acc_r;\n')]),
 'M10_release_forgets_work': ('rtl',
                              [('                        : drop_w      ? (dirty_live_r | '
                                'dirty_cap_r)\n',
                                '                        : drop_w      ? dirty_live_r\n')]),
 'M11_dirty_from_accepted_bytes': ('rtl',
                                   [("  assign dirty_live_n_w = rec_close_w ? 1'b1\n",
                                     '  assign dirty_live_n_w = (mem_wr_valid_o & '
                                     "mem_wr_ready_i) ? 1'b1\n")]),
 'M12_alarm_not_revoking': ('rtl',
                            [('  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w | '
                              'alarm_i;\n',
                              '  assign loss_ev_w = alive_exp_w | commit_exp_w | '
                              'fail_rep_w;\n')]),
 'M13_report_not_revoking': ('rtl',
                             [('  assign loss_ev_w = alive_exp_w | commit_exp_w | fail_rep_w | '
                               'alarm_i;\n',
                               '  assign loss_ev_w = alive_exp_w | commit_exp_w | '
                               'alarm_i;\n')]),
 'M14_pending_bit_misses_producer': ('rtl',
                                     [('  assign pend_w        = pend_r | unres_w;\n',
                                       '  assign pend_w        = unres_w;\n')]),
 'M15_pending_bit_misses_open_record': ('rtl',
                                        [('  assign pend_w        = pend_r | unres_w;\n',
                                          '  assign pend_w        = pend_r;\n')]),
 'M17_hold_expiry_voids_capture': ('rtl',
                                   [("                   : (close_w | void_grant_w) ? 1'b0 : "
                                     'cap_valid_r;\n',
                                     '                   : (close_w | void_grant_w | '
                                     "hold_exp_w) ? 1'b0 : cap_valid_r;\n")]),
 'M18_pending_bit_stuck': ('rtl',
                           [('  assign pend_w        = pend_r | unres_w;\n',
                             "  assign pend_w        = 1'b1;\n")]),
 'M19_arm_edge_grant_not_deferred': ('rtl',
                                     [('                     && !((cap_hold_r | arm_ok_w) && '
                                       'mut_req_w);\n',
                                       '                     && !(cap_hold_r && '
                                       'mut_req_w);\n')]),
 'M20_arm_accepted_while_request_deferred': ('rtl',
                                             [('  assign arm_ok_w    = arm_w & img_cfg_w & '
                                               'img_valid_r & ~cap_open_r & ~void_hard_w\n'
                                               '                     & ~mut_defer_r & '
                                               'ld_acc_r;\n',
                                               '  assign arm_ok_w    = arm_w & img_cfg_w & '
                                               'img_valid_r & ~cap_open_r & ~void_hard_w\n'
                                               '                     & ld_acc_r;\n')]),
 'R01_reload_ignores_inflight': ('rtl',
                                 [('               : rebase_w    ? ~inflight_w\n',
                                   "               : rebase_w    ? 1'b1\n")]),
 'R02_reload_ignores_grant_since_rebase': ('rtl',
                                           [("      ld_ok_r <= gnt_opmut_w ? 1'b0\n"
                                             '               : rebase_w    ? ~inflight_w\n',
                                             '      ld_ok_r <= rebase_w    ? ~inflight_w\n')]),
 'R03_reload_not_once_per_reset': ('rtl',
                                   [('  assign reload_ok_w = reload_w & ld_ok_r & ld_pend_r;\n',
                                     '  assign reload_ok_w = reload_w & ld_ok_r;\n')]),
 'R04_rebase_wins_over_same_edge_grant': ('rtl',
                                          [("      ld_ok_r <= gnt_opmut_w ? 1'b0\n"
                                            '               : rebase_w    ? ~inflight_w\n',
                                            '      ld_ok_r <= rebase_w    ? ~inflight_w\n'
                                            "               : gnt_opmut_w ? 1'b0\n")]),
 'R05_boot_load_stays_pending_when_live': ('rtl',
                                           [('      if (reload_ok_w | win_live_w) ld_pend_r <= '
                                             "1'b0;\n",
                                             "      if (reload_ok_w) ld_pend_r <= 1'b0;\n")]),
 'R07_arm_without_accepted_load': ('rtl',
                                   [('                     & ~mut_defer_r & ld_acc_r;\n',
                                     '                     & ~mut_defer_r;\n')])}

#: a rule that lives in TWO files: name -> {source: [(exact, replacement)]}
COMBINED = {'R06_revision_b_load_rule': {'fw': [('\t} else if (milan_read(MILAN_PP_STAT) & '
                                      'MILAN_PP_STAT_RESTORE_DONE) {\n',
                                      '\t} else if (0) {\n')],
                              'rtl': [('      if (reload_ok_w | win_live_w) ld_pend_r <= '
                                       "1'b0;\n",
                                       "      if (reload_ok_w) ld_pend_r <= 1'b0;\n")]}}


def apply(text: str, subs: list[tuple[str, str]], what: str) -> str:
    """`text` with every seam of `subs` replaced. A seam that does not hit
    EXACTLY once refuses: a line that moved must break this file rather than
    let a mutant compile unchanged and report a vacuous pass."""
    for old, new in subs:
        if text.count(old) != 1:
            raise SystemExit(f"mutant {what}: seam hit {text.count(old)} times: {old[:70]!r}")
        text = text.replace(old, new)
    return text


def main() -> int:
    """Plant one named defect in a copy of a shipping source."""
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    kind, name, src, dst = sys.argv[1:]
    if name in COMBINED:
        subs = COMBINED[name].get(kind)
        if subs is None:
            raise SystemExit(f"mutant {name} touches {sorted(COMBINED[name])}, not {kind}")
    elif name in MUTANTS:
        want, subs = MUTANTS[name]
        if want != kind:
            raise SystemExit(f"mutant {name} is a {want} mutant, not {kind}")
    else:
        raise SystemExit(f"unknown mutant {name}; known: {sorted(set(MUTANTS) | set(COMBINED))}")
    out = Path(dst)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(apply(Path(src).read_text(), subs, name))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
