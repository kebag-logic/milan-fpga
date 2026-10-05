# New mutation audit at 7f8dc1b1

24 added controls and one removed control account for the change from 46 to 69. All 69 built and executed; every named grading function returned a failure. Build failures were not counted as kills. These conclusions were checked against the replacement seams and raw failure output, not only the campaign return code.

| Added control | Named checks | Observed effect |
|---|---|---|
| [binding_fault_aborts_d3](receipts/campaign/binding_fault_aborts_d3.log) | binding_walk | A binding failure wrongly ends D3 DEFAULTS and removes D3 values. |
| [binding_fault_keeps_preloads](receipts/campaign/binding_fault_keeps_preloads.log) | binding_walk | A binding preload survives the failed binding walk; undo is not called. |
| [bindings_in_d3_walk](receipts/campaign/bindings_in_d3_walk.log) | binding_walk, golden_restore | Binding-after-D3 order violation (sm_order=2), also wrong fault isolation. |
| [blankcheck_first_stretch_only](receipts/campaign/blankcheck_first_stretch_only.log) | blankcheck_tail | Tail stuck byte reaches verify: verdict 13 instead of erase verdict 11. |
| [blankcheck_read_fail_ignored](receipts/campaign/blankcheck_read_fail_ignored.log) | media_verdicts | A failed blank-check read produces success without a failed attempt. |
| [budget_rearmed_by_capture](receipts/campaign/budget_rearmed_by_capture.log) | dr2c_unchanged_set | Unchanged set drives 63 erases, with no abandonment retained. |
| [budget_rearmed_by_change](receipts/campaign/budget_rearmed_by_change.log) | dr2c_unchanged_set | Repeated identical notifications drive 40 erases, exceeding three. |
| [capture_leaves_window_armed](receipts/campaign/capture_leaves_window_armed.log) | debounce | Later change erases after 1,703 us instead of the 1,000 ms window. |
| [clock_not_accumulated](receipts/campaign/clock_not_accumulated.log) | time_base | Counter wrap advances an erase to 451,365 us after the change. |
| [commit_now_ignores_backoff](receipts/campaign/commit_now_ignores_backoff.log) | dr2c_console | Retry occurs 183,703 us after failure, violating 1,000 ms spacing. |
| [commit_now_overrides_exhaustion](receipts/campaign/commit_now_overrides_exhaustion.log) | dr2c_console | Console case produces 11 failures and 9 erases, withholding zero attempts. |
| [d3_rollback_takes_bindings](receipts/campaign/d3_rollback_takes_bindings.log) | apply_fault_rolls_back, settle_fault_rolls_back | D3 failure invokes binding rollback and loses restored bindings. |
| [open_unbounded](receipts/campaign/open_unbounded.log) | port_stall | Drain exceeds the model escape threshold: ls_hung=1. |
| [phc_time](receipts/campaign/phc_time.log) | time_base | Backward PHC step leaves no erase in the measured debounce interval. |
| [program_refusal_ignored](receipts/campaign/program_refusal_ignored.log) | media_verdicts | Program refusal is hidden until verify (13 rather than 12). |
| [select_on_unchecked_reread](receipts/campaign/select_on_unchecked_reread.log) | read_flip_boot | Bit 3 of sequence byte 8 makes older A=5 displace B=6. |
| [slot_read_fail_ignored](receipts/campaign/slot_read_fail_ignored.log) | read_fail_boot | Failed container read reports CRC (4), not read/length failure (3). |
| [stage_seq_unchecked](receipts/campaign/stage_seq_unchecked.log) | read_alias_at_stage | Aliased re-stage publishes 5 for selected slot A whose validated sequence was 6. |
| [stall_ignored](receipts/campaign/stall_ignored.log) | port_stall | Stalled program is hidden until verify (13 rather than 12). |
| [success_forgives_exhaustion](receipts/campaign/success_forgives_exhaustion.log) | recovers_after_failure, dr2c_unchanged_set | Success clears abandoned to zero despite a prior exhausted work set. |
| [tie_picks_b](receipts/campaign/tie_picks_b.log) | newer_wins | Equal-sequence case selects B, while the test demands A. Mechanically detected; normative defect status is unresolved (R501-2-F3). |
| [verify_read_fail_ignored](receipts/campaign/verify_read_fail_ignored.log) | media_verdicts | Failed verify read produces success without a failed attempt. |
| [verify_skips_last_stretch](receipts/campaign/verify_skips_last_stretch.log) | verify_tail | Dropped trailer page still reports successful promotion. |
| [xfer_unbounded](receipts/campaign/xfer_unbounded.log) | port_stall | TX/RX wait exceeds the model escape threshold: ls_hung=1. |

The removed `attempts_kept` control represented the old policy of resetting the budget on every change notification. The new controls instead require staged-byte comparison and an exhaustion record surviving later success. Existing `no_crc_check`, `no_crc_anywhere`, rollback and sequence controls were also rerun at this head.

The unbounded-loop controls are finite only because the model records a hang after 1,000,000 reads and releases it; the actual mutated port loops have no limit. Their explicit hang and latency assertions fail. This is defect detection, not a process timeout counted as a successful test.
