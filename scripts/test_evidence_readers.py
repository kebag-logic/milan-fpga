# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Why each inventoried test may read DUT source without deriving its oracle.

The evidence gate owns detection and stale-entry checking. This module owns
only the public dispositions, so extending the inventory does not lengthen
the gate implementation.
"""

DUT_READER_DISPOSITIONS: dict[str, str] = {
    "protocol-processor/tb/pp_top/acmp_mutants.py":
        "mutation campaign; it plants one ACMP listener, validator, top SRP-service, bound-view, "
        "SRP matcher or top timer arm-queue defect from its own table into an isolated copy and "
        "requires every named check to fail in a completed run; no expected value is read from the text",
    "protocol-processor/tb/pp_top/notify_mutants.py":
        "mutation campaign; it plants one notification, identify or inflight defect from its own table "
        "into an isolated copy and requires every named check to fail in a completed run; no expected "
        "value is read from the text",
    "protocol-processor/tb/pp_top/d3_mutants.py":
        "mutation campaign; it plants one D3 saved-state defect from its own table into an "
        "isolated copy and requires every named check to fail in a completed run; no expected "
        "value is read from the text",
    "protocol-processor/tb/acmp_talker/retry_mutants.py":
        "mutation campaign; plants named defects in a scratch copy and requires named assertion "
        "failures from completed cycle-bounded simulations; reads no expected behavior from RTL",
    "protocol-processor/tb/desc_store/test_gen_desc_image.py":
        "unit test of the descriptor packer and its model lint; it imports the generator by path "
        "to call build() and its CLI on synthetic models and on the two models packaged beside it, "
        "passes the packaged model_ids.json in as the recorded digests, and reads no expectation "
        "from source",
    "protocol-processor/tb/pp_top/name_wr_mutant.py":
        "mutation campaign; removes the accepted name-write export in a copy "
        "and requires the named pulse check to fail",
    "tb/verilator/pp_shadow/pending_mutant.py":
        "mutation campaign; restores the late mark trigger in a copy and "
        "requires both K10/K12 durability checks to fail",

    "tb/verilator/mmcm_servo/slew_mutants.py":
        "mutation campaign; copies the servo and requires named failures for "
        "discard removal, tied-low level, partial-tail trust, omitted tally, "
        "boundary step double counting, retained guard streak, streak increment "
        "on slew discard and slew discard counted as a guard trip; "
        "no expectations read from RTL",
    "tb/verilator/aaf_clock_meter/mutants.py":
        "mutation campaign; it plants one of the #629 design's named AAF clock meter "
        "and meter-in-front-of-servo defects into a copy of the meter or the servo and "
        "requires the named check of the meter, servo or unit leg to fail; no expected "
        "value is read from RTL",
    "tb/verilator/capture_coherence/mutants.py":
        "mutation campaign; it plants one TDM frame-handoff, snapshot, counter or grid-aligner "
        "binding defect into a copy of the capture crossbar, the junction wrapper or the datapath, "
        "and requires a named failure from the junction, datapath or chmap_capture harness; no "
        "expected value is read from RTL",
    "tb/verilator/crf_rx/mutants.py":
        "mutation campaign; copies the receiver and servo, requiring named failures "
        "for validation_error_unlocks, validation_error_refreshes_timeout, tu, jump, "
        "refill, accept-edge, ignored-validity and PI-resume defects; "
        "no expectations read from RTL",
    "gptp-processor/tb/check_phc_contract.py":
        "structural boundary check; it asserts required/forbidden tokens, not behavior",
    "gptp-processor/tb/tsngen/mutants.py":
        "mutation campaign; it stages three engine defects and requires failure",
    "protocol-processor/tb/desc_mem_guard/mutate.py":
        "mutation campaign; it removes the guard's two request holds in a copy and "
        "requires the completed late-byte assertion to fail",
    "protocol-processor/tb/nvm_port/measure_figures.py":
        "mutation campaign; it rewrites one RTL arm and requires the suite to fail",
    "protocol-processor/tb/pp_top/gsi_mutants.py":
        "mutation campaign; it plants one GET_STREAM_INFO seam defect from its own table "
        "into an isolated copy and requires the named response check to fail",
    "protocol-processor/tb/srp_admission/mutants.py":
        "mutation campaign; it plants one admission defect into a temporary tree, "
        "requires the named check to fail, and runs clean controls first",
    "tb/verilator/follow_ring/mutants.py":
        "mutation campaign; it plants the #645 ruling's settle-recentre controls (no pulse, "
        "the band in place of 8 LOCKED windows, removed excursion arm) into a copy of the "
        "datapath, overshoot and single-drop into a copy of the capture crossbar, and the "
        "render-only and W1 bindings by define; each must fail its named wire or law check",
    "tb/verilator/gptp_shadow/test_mutant_lifecycle.py":
        "orchestration lifecycle fixture; it identifies the planted mutation and "
        "compares caller bytes/modes/index across interruption. Synthetic commands "
        "grade isolation and cleanup only; RTL behavior still requires the real suite",
    "tb/verilator/milan_dp/crflic_mutants.py":
        "mutation campaign; it plants one of three streaming-licence defects into a copy and requires a "
        "named failure. It is the explicit crflic-mutants target, outside the default sweep",
    "tb/verilator/milan_dp/gsi_mutants.py":
        "mutation campaign; it plants one of eight #508 GET_STREAM_INFO seam defects into a copy of "
        "the datapath or of the processor tree and requires a named failure. It is the explicit "
        "gsi-mutants target, outside the default sweep",
    "tb/verilator/milan_dp/unb_mutants.py":
        "mutation campaign; it plants one of five #653 unbind defects (the response held behind "
        "the push, a CRF unbind that misses, doubles or mislabels its unlock, or arms no push) "
        "into a copy of the processor tree or of the CRF engine and requires named failures "
        "beside named passes. It is the explicit unb-mutants target, outside the default sweep",
    "tb/verilator/milan_dp/gmstep_mutants.py":
        "mutation campaign; it plants #387 re-base and #545 slew-connection defects into a copy and requires a "
        "named failure on the gmstep leg or, for two, the option-off leg. The default sweep plants "
        "the three #387 acceptance names; gmstep-mutants plants all, and --slew selects the three #545 controls",
    "tb/verilator/milan_dp/render_csr_controls.py":
        "mutation campaign; the explicit render-csr-controls target plants wrong-fill "
        "and bit-9 selector defects into copies and requires named failures. Its "
        "absent-stage control removes the instance and requires structural zero "
        "despite accepted ingress; no expected value is derived from source text",
    "tb/verilator/milan_dp/render_mutants.py":
        "mutation campaign; it plants one of four render-law defects into a copy and requires a named failure",
    "tb/verilator/milan_dp_mclk/mclk_mutants.py":
        "mutation campaign; it plants the #629 design's fourteen named root defects as "
        "mutant schemata in copies of the datapath, the AAF clock meter and the CSR "
        "block, selected per run by a plusarg, and requires each short leg to fail its "
        "named check while the schemata at id 0 and the clean legs pass; no expected "
        "value is read from RTL",
    "tb/verilator/milan_dp_render/tdm8_render_mutants.py":
        "mutation campaign; it plants one render-lane defect from its own table into "
        "a copy or runs a leg-side defect arm, and requires the named check to fail. "
        "The suite's default target runs its --leg-defects arms; the gateware and "
        "shape mutants are the explicit tdm8render-mutants target",
    "tb/verilator/mbx/mutants.py":
        "mutation campaign; it plants one packet-mailbox defect from its own table into a scratch "
        "copy of hdl/milan/mailbox, builds the suite with the Makefile's own recipe and requires the "
        "named check to fail; no expected value is read from RTL",
    "tb/verilator/nvm_backend/mutate.py":
        "mutation campaign; it plants one of four backend defects into a copy and requires failure",
    "tb/verilator/nvm_cosim/run_cases.py":
        "co-simulation driver; it reads the SHIPPING backend and the "
        "SHIPPING writer because they ARE the pair under test -- it "
        "compiles that writer for the host and Verilates that backend "
        "behind it, planting a named defect through mutate.py or taking a "
        "pre-contract copy for the non-vacuity control. It grades nothing "
        "from the text: every verdict is a named check in cosim_checks.py "
        "over a dumped journal",
    "tb/verilator/ptp_ts/sva_campaign.py":
        "mutation campaign; it plants one of fifteen axis_mux_rr_2in_1out defects into a "
        "scratch copy and requires the named SVA property, or for one row the scoreboard, "
        "to fail; no expected value is read from the text",
    "tb/verilator/render_setpoint/mutants.py":
        "mutation campaign; it plants one of thirteen setpoint-stage defects into a copy and requires failure",
    "tb/verilator/rx_filter/binding_mutant.py":
        "mutation campaign; it ties a real named binding low and requires failure",
    "tb/verilator/tcam/mutants.py":
        "mutation campaign; it injects three RTL defects and requires failure",
    "tb/verilator/tkdiag/mcr_mutants.py":
        "mutation campaign; it plants one of four restart-engine defects against the #387 "
        "pending-restart merge and its wire boundary into a copy and requires a named failure",
}
