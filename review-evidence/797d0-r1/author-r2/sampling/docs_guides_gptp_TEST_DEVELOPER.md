# Sampling ledger: docs/guides/gptp/TEST_DEVELOPER.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 21 | row | \| C \| No first-party gPTP harness \| | - | ok: no first-party gPTP C harness (sw/firmware/gtest covers ctrl and ctrl_nvm only) |
| 26 | sentence | C firmware never judges gPTP correctness. | - | policy |
| 28 | sentence | Python models must not mirror implementation blindly. | - | policy |
| 43 | row | \| Parent `gptp_plane` \| Closed-loop PHC steering \| | - | ok: tb/verilator/gptp_plane closed-loop suite |
| 56 | item | Drive only public DUT interfaces. | - | policy |
| 57 | item | Compare accepted transfers only. | - | policy |
| 62 | item | Include reset during activity. | - | policy |
| 66 | item | Record the defects a suite cannot see. | - | policy |
| 70 | item | Confirm that mutation fails. | - | policy |
| 77 | item | Record every exit status. | - | policy |
| 98 | row | \| A1 \| `TxtsHarness::prove_queue_invariance`, which measures the retired capture in the same run and shows it queue dependent \| `make -C tb/verilator/gptp... | command 1 | ok: all named tests exist in tb/verilator/gptp_txts or gptp_shadow (32 names, receipt sampling/gptp-test-names.txt) |
| 99 | row | \| A2 \| `TxtsHarness::prove_pads_are_byte_exact` \| `make -C tb/verilator/gptp_txts` \| | command 1 | ok: same |
| 100 | row | \| A3 \| `TxtsHarness::exchange` builds the isolated and queued stimulus; `check_backpressure_holds_the_lane`, `check_burst_never_laps_the_stamp_ring` and `c... | command 2 | ok: same |
| 101 | row | \| B1 \| `TxtsHarness::prove_launch_reference` \| `make -C tb/verilator/gptp_txts` \| | command 1 | ok: same |
| 102 | row | \| B2 \| `TxtsHarness::prove_bias_over_many_frames` \| `make -C tb/verilator/gptp_txts` \| | command 1 | ok: same |
| 103 | row | \| B3 \| `TxtsHarness::prove_queue_invariance` \| `make -C tb/verilator/gptp_txts` \| | command 1 | ok: same |
| 104 | row | \| B4 \| `check_one_exchange_measures_the_delay`, `check_second_exchange_raises_capability` \| `make -C tb/verilator/gptp_shadow` \| | command 1 | ok: same |
| 105 | row | \| B5 \| `check_equal_sequence_request_collision`, `check_master_emits_all_three_types`, `check_same_type_response_ownership` \| `make -C tb/verilator/gptp_s... | command 1 | ok: same |
| 106 | row | \| B6 \| `check_every_stamp_names_its_own_frame`, `check_a_record_that_is_not_this_frames_is_refused`, `check_an_aged_head_is_not_retired` \| `make -C tb/ver... | command 1 | ok: same |
| 107 | row | \| B7 \| `check_warm_reset_clears_the_request_owner`, `check_warm_reset_clears_the_sync_owner`, `TxtsHarness::prove_recovery_over_the_production_mac` \| `mak... | command 2 | ok: same |
| 108 | row | \| B8 \| `check_backpressure_holds_the_lane`, and the cancellation grading inside `check_torn_frame_is_discarded_and_counted` \| `make -C tb/verilator/gptp_s... | command 1 | ok: same |
| 109 | row | \| B9 \| `check_an_aged_head_is_not_retired`, where the stall diagnostic counts and the claim stays live, and `check_recovery_demand_survives_an_unaccepted_r... | command 1 | ok: same |
| 110 | row | \| B10 \| `check_phc_trajectory_qualification`, `check_held_disable_refuses_every_capture`, `check_non_nominal_increment_refuses_every_capture`, `check_resto... | command 1 | ok: same |
| 111 | row | \| B11 \| `TxtsHarness::prove_fragment_aborts` \| `make -C tb/verilator/gptp_txts` \| | command 1 | ok: same |
| 112 | row | \| B12 \| `check_every_stamp_names_its_own_frame`, `check_torn_frame_is_discarded_and_counted`, `check_the_seal_waits_for_the_echo` \| `make -C tb/verilator/... | command 1 | ok: same |
| 113 | row | \| B13 \| `TxtsHarness::prove_recovery_over_the_production_mac`, `check_disabled_guard_holds_the_seal`, `check_masked_request_keeps_its_demand`, `check_abort... | command 2 | ok: same |
| 114 | row | \| D1 to D5 \| the donor's own labelled sections in `gptp-processor/tb/verilator/engine/sim_main.cpp` \| `make -C gptp-processor` \| | path 1; command 1 | ok: gptp-processor/tb/verilator/engine/sim_main.cpp exists (auto) |
| 115 | row | \| D6 \| the whole donor suite, at the pin this tree consumes \| `make -C gptp-processor` \| | command 1 | ok: gptp-processor/Makefile |
| 127 | sentence | Each suite records the defects it CANNOT see. | - | policy |
