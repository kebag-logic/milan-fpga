<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP test-developer guide

Use this page for verification changes.

## Contents

- **[Choose a language](#choose-a-language)** -- Match tools with observable boundaries.
- **[Choose a suite](#choose-a-suite)** -- Start with the smallest useful layer.
- **[Build an oracle](#build-an-oracle)** -- Detect failures independently.
- **[Publish evidence](#publish-evidence)** -- Make every result reproducible.
- **[Acceptance evidence for the egress launch timestamp](#acceptance-evidence-for-the-egress-launch-timestamp)** -- Map each contracted acceptance item to the named check and command that proves it

## Choose a language

| Language | Current gPTP role |
|---|---|
| Python | Microcode generation, models, fuzzing, gates |
| C | No first-party gPTP harness |
| C++ | Verilator clocks, stimulus, and assertions |
| SystemVerilog | DUT wrappers and production RTL |
| Make | Reproducible suite entry points |

C firmware never judges gPTP correctness.

Python models must not mirror implementation blindly.

Read the [engine test guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/TEST_DEVELOPER.md).

## Choose a suite

| Suite | Boundary |
|---|---|
| Donor `ucpu` | Arithmetic and instruction execution |
| Donor `parser` | Byte parsing and refusal paths |
| Donor `engine` | Protocol behavior and servo |
| Donor `gaskets` | Bench MII gasket loopback and FIFO wedge |
| Parent `ptp` | PHC accumulator arithmetic |
| Parent `ptp_ts` | Stand-alone record stamper, absent from the product |
| Parent `gptp_shadow` | Transport, pairing, publication, ledger laws |
| Parent `gptp_plane` | Closed-loop PHC steering |
| Parent `gptp_txts` | Egress launch time over the converted product MAC |
| Parent `clkvalid` | Discontinuity and holdover |
| Parent `milan_dp` | Product wiring and public consumers |
| Parent `tsn_fuzz` | Independent wire-model campaigns |

Begin with the narrowest failing suite.

Finish with complete donor and parent gates.

## Build an oracle

- Name one requirement or defect.
- Drive only public DUT interfaces.
- Compare accepted transfers only.
- Build expected protocol fields independently.
- Include positive controls.
- Include malformed and truncated inputs.
- Include backpressure and timeouts.
- Include reset during activity.
- Convert product software rather than modelling it.
- Then prove the conversion behaves like its source.
- `sw/litex/test_gptp_tx_timestamp.py` is that proof.
- Record the defects a suite cannot see.
- `tb/verilator/gptp_shadow/mutants.py` carries such a record.
- Withhold and reorder timestamp returns.
- Plant one deliberate mutation.
- Confirm that mutation fails.
- Restore production code afterward.

## Publish evidence

- Record the exact commit.
- Record each complete command.
- Record every exit status.
- Preserve the first failure log.
- Separate simulation from physical evidence.
- State uncovered boundaries explicitly.

Use the [traceability table](../../traceability/ieee8021as.md).

## Acceptance evidence for the egress launch timestamp

Each contracted acceptance item resolves to a named check.

Each check is in the source, under one command.

The checks carry the item as an `ACCEPTANCE` comment.

So the mapping is greppable from either end.

Try `grep -rn "ACCEPTANCE B5" tb/`.

| Item | Named check | Command |
|---|---|---|
| A1 | `TxtsHarness::prove_queue_invariance`, which measures the retired capture in the same run and shows it queue dependent | `make -C tb/verilator/gptp_txts` |
| A2 | `TxtsHarness::prove_pads_are_byte_exact` | `make -C tb/verilator/gptp_txts` |
| A3 | `TxtsHarness::exchange` builds the isolated and queued stimulus; `check_backpressure_holds_the_lane`, `check_burst_never_laps_the_stamp_ring` and `check_torn_frame_is_discarded_and_counted` carry the stall, occupancy and torn-frame shapes | `make -C tb/verilator/gptp_txts`, `make -C tb/verilator/gptp_shadow` |
| B1 | `TxtsHarness::prove_launch_reference` | `make -C tb/verilator/gptp_txts` |
| B2 | `TxtsHarness::prove_bias_over_many_frames` | `make -C tb/verilator/gptp_txts` |
| B3 | `TxtsHarness::prove_queue_invariance` | `make -C tb/verilator/gptp_txts` |
| B4 | `check_one_exchange_measures_the_delay`, `check_second_exchange_raises_capability` | `make -C tb/verilator/gptp_shadow` |
| B5 | `check_equal_sequence_request_collision`, `check_master_emits_all_three_types`, `check_same_type_response_ownership` | `make -C tb/verilator/gptp_shadow` |
| B6 | `check_every_stamp_names_its_own_frame`, `check_a_record_that_is_not_this_frames_is_refused`, `check_an_aged_head_is_not_retired` | `make -C tb/verilator/gptp_shadow` |
| B7 | `check_warm_reset_clears_the_request_owner`, `check_warm_reset_clears_the_sync_owner`, `TxtsHarness::prove_recovery_over_the_production_mac` | `make -C tb/verilator/gptp_shadow`, `make -C tb/verilator/gptp_txts` |
| B8 | `check_backpressure_holds_the_lane`, and the cancellation grading inside `check_torn_frame_is_discarded_and_counted` | `make -C tb/verilator/gptp_shadow` |
| B9 | `check_an_aged_head_is_not_retired`, where the stall diagnostic counts and the claim stays live, and `check_recovery_demand_survives_an_unaccepted_request` | `make -C tb/verilator/gptp_shadow` |
| B10 | `check_phc_trajectory_qualification`, `check_held_disable_refuses_every_capture`, `check_non_nominal_increment_refuses_every_capture`, `check_restored_excursion_still_refuses`, `check_settime_reloads_the_guard` | `make -C tb/verilator/gptp_shadow` |
| B11 | `TxtsHarness::prove_fragment_aborts` | `make -C tb/verilator/gptp_txts` |
| B12 | `check_every_stamp_names_its_own_frame`, `check_torn_frame_is_discarded_and_counted`, `check_the_seal_waits_for_the_echo` | `make -C tb/verilator/gptp_shadow` |
| B13 | `TxtsHarness::prove_recovery_over_the_production_mac`, `check_disabled_guard_holds_the_seal`, `check_masked_request_keeps_its_demand`, `check_aborted_episode_is_not_a_completion`, `check_held_firmware_reinit_holds_the_seal`, `check_stopped_eth_clock_holds_the_seal` | `make -C tb/verilator/gptp_txts`, `make -C tb/verilator/gptp_shadow` |
| D1 to D5 | the donor's own labelled sections in `gptp-processor/tb/verilator/engine/sim_main.cpp` | `make -C gptp-processor` |
| D6 | the whole donor suite, at the pin this tree consumes | `make -C gptp-processor` |

Two suites answer for most of this.

`gptp_txts` owns what an independent pad oracle grades.

That oracle runs over the converted product MAC.

`gptp_shadow` owns the ledger, pairing, guard and PHC laws.

A stand-in MAC is enough there.

Each suite records the defects it CANNOT see.

`tb/verilator/gptp_shadow/mutants.py` and `tb/verilator/gptp_txts/mutants.py` carry those records.

Each names the structural pin that holds it instead.
