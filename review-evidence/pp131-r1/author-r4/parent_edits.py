#!/usr/bin/env python3
"""Apply the declared pin-adoption edits to a SCRATCH parent at dev b5c0f69d.

Each edit is exact text (every old text must occur once). This is the minimal set
that makes the parent consumer set pass with the processor at the PR head; the
pin-adoption lane owns the real change. Usage: parent_edits.py <scratch parent> [ms]
where ms is the B1-B4 give-up window in model milliseconds (default 2000).
"""
import sys

ROOT = sys.argv[1]
B_MS = sys.argv[2] if len(sys.argv) > 2 else "2000"


def edit(rel, pairs):
    path = f"{ROOT}/{rel}"
    s = open(path).read()
    for old, new in pairs:
        assert s.count(old) == 1, (rel, old[:90])
        s = s.replace(old, new)
    open(path, "w").write(s)


# 1. round 1: the five new top ports in the parent glue; pend_i as declared
edit("hdl/milan/KL_pp_shadow.sv", [
    ("""  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w)
                    | aecp_live_wr_w | aecp_live_pend_r;
""", """  logic        d3_unflushed_w, pp_restore_closed_w, pp_restore_rb_w;
  logic [2:0]  pp_rs_cause_w;
  logic [1:0]  pp_restore_cause_w;
  //! the D3 walk's CLOSED, roll-back and causes: the combined restore status
  //! is lane 2's; scratch adoption only connects them
  logic        unused_d3_status_w;
  assign unused_d3_status_w = ^{pp_restore_closed_w, pp_restore_rb_w, pp_rs_cause_w,
                                pp_restore_cause_w};
  assign nvm_pend_w = aecp_dyn_dirty_o | (|nvm_unflushed_w) | d3_unflushed_w
                    | aecp_live_wr_w | aecp_live_pend_r;
"""),
    ("""      .nvm_unflushed_o     (nvm_unflushed_w),
""", """      .nvm_unflushed_o     (nvm_unflushed_w),
      .d3_unflushed_o      (d3_unflushed_w),
      .restore_closed_o    (pp_restore_closed_w),
      .restore_rb_o        (pp_restore_rb_w),
      .rs_cause_o          (pp_rs_cause_w),
      .restore_cause_o     (pp_restore_cause_w),
"""),
])

# 2. nvm_cosim: its direct instances of the binding manager and the dynamic-state
#    store, with the clock-referenced parameters derived as the top derives them
edit("tb/verilator/nvm_cosim/cosim_top.sv", [
    ("""      .dbg_writes_o    (wr_nc_w),
""", """      .dbg_writes_o    (wr_nc_w),
      .wr_chg_o        (),
"""),
    ("""      //! the top's NVM_RS_TMO_CYC_P default, derived the way it derives it
      .RS_TMO_CYC_P (CLK_HZ_P / 32'd50)
""", """      //! the top's NVM_RS_TMO_CYC_P and NVM_RETRY_BACKOFF_CYC_P defaults,
      //! derived the way it derives them: ceil(CLK_HZ_P / 50), ceil(CLK_HZ_P / 2)
      .RS_TMO_CYC_P (CLK_HZ_P / 32'd50 + (((CLK_HZ_P % 32'd50) != 32'd0) ? 32'd1 : 32'd0)),
      .RETRY_BACKOFF_CYC_P ((CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2))
"""),
    ("""      .restore_go_i     (restore_go_i),
""", """      .restore_go_i     (restore_go_i),
      .rs_agg_i         (1'b0),
"""),
])
edit("tb/verilator/nvm_cosim/cosim_cases.cpp", [
    ("""      idle(1500);                      // debounce, three attempts, give-up
""", f"""      idle({B_MS});                      // debounce, three attempts 500 ms apart, give-up
"""),
])

# 3. the evidence classifier: the D3 mutation driver's disposition
edit("scripts/measure_test_evidence.py", [
    ("""DUT_READER_DISPOSITIONS = {
""", """DUT_READER_DISPOSITIONS = {
    "protocol-processor/tb/pp_top/d3_mutants.py":
        "mutation campaign; it plants one D3 saved-state defect from its own table into an "
        "isolated copy and requires every named check to fail in a completed run; no expected "
        "value is read from the text",
"""),
])
# 4. the PP_CTRL[1] harness obligation: every parent harness that exercises AECP
#    starts the boot restore walk as the firmware does (AECP is held from reset
#    until the D3 restore reaches its terminal), before its first AECP command
edit("tb/verilator/milan_dp/sim_gmstep.cpp", [
    ("""void GmStepHarness::provision_media() {
""", """void GmStepHarness::provision_media() {
    // pin adoption: PP_CTRL[1] starts the boot restore walk, as nvm_boot() does
    write(0x920, read(0x920) | 0x2u);
    for (int r = 0; r < 400 && !((read(0x924) >> 2) & 1u); ++r) run_cycles(64);
"""),
])
edit("tb/verilator/milan_dp/sim_gptp.cpp", [
    ("""  void grade_the_committed_bank_on_the_aecp_wire(Vmilan_datapath *dut) {
    aecp_scan = tx_frames.size();
""", """  void grade_the_committed_bank_on_the_aecp_wire(Vmilan_datapath *dut) {
    // pin adoption: PP_CTRL[1] starts the boot restore walk, as nvm_boot() does
    axi_write(dut, 0x920, axi_read(dut, 0x920) | 0x2u);
    for (int r = 0; r < 400 && !((axi_read(dut, 0x924) >> 2) & 1u); ++r) run(dut, 64);
    aecp_scan = tx_frames.size();
"""),
])
#    milan_dp_render already starts the walk (boot_the_entity), but its T8 REMOVE
#    opens the collection 639 axis cycles after the REMOVE's answer, less than one
#    commit-to-pin bound: with the D3 walk in the boot the leg reaches T8 272 axis
#    cycles later, and a frame committed before the removal is decoded stale.
#    T8 waits that bound out first.
edit("tb/verilator/milan_dp_render/sim_tdm8_render.cpp", [
    ("""    decoder_reset();
    taps_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    long silent = 0;""", """    // pin adoption: a frame committed before the removal can still reach the
    // pins up to one commit-to-pin bound later; wait it out before collecting
    run_fed(static_cast<long>(kFrameAxis + kCdcFloorAxis + kBitAxis) + 1);
    decoder_reset();
    taps_reset();
    collect = true;
    run_fed(40 * kPduPeriodCycles);
    collect = false;
    long silent = 0;"""),
])
print("parent edits applied, B1-B4 window", B_MS, "ms")

# 5. pp_shadow, which runs only once the round-1 ports are connected (item 1):
#    its pending phases (K, K10, K12) enable the entity without the walk; M2 hands
#    the memory over without the firmware's PP_CTRL[1]; P3 expects the binding
#    walk's raw blank-with-fail, which the combined restore_blank_o never shows
edit("tb/verilator/pp_shadow/sim_main.cpp", [
    ("""        axi_write(A_PP_NVM_STAT, 1);    // live writer
        axi_write(A_PP_CTRL, 1);
        run_idle(2000);
        ck("K control: reset/load permits durable status",""",
     """        axi_write(A_PP_NVM_STAT, 1);    // live writer
        // pin adoption: PP_CTRL[1] starts the boot restore walk before the
        // enable, as nvm_boot() does; AECP is held until it ends. Nothing
        // answers behind the backend's configured window here, so each walk
        // ends on its per-wait deadline (about 4.0 M cycles in all)
        axi_write(A_PP_CTRL, 0x2);
        for (int i = 0; i < 6000 && !((axi_read(A_PP_STAT) >> 2) & 1); ++i) run_idle(1000);
        axi_write(A_PP_CTRL, 1);
        run_idle(2000);
        ck("K control: reset/load permits durable status","""),
    ("""        mem_answering = true;                  // HANDOVER: memory + image now
""", """        mem_answering = true;                  // HANDOVER: memory + image now
        // pin adoption: the firmware starts the restore walk once the image is
        // in place; the D3 writer's LOCATE proves the image the store parked on
        restore_walk_completes();
"""),
    ("""        ck("P3: ...and no record was validated (the #20 blank/refusal collapse)",
           (xstat >> 7) & 1, 1u);""", """        //! pin adoption: the top's combined restore_blank_o never reads 1 with
        //! fail (processor #131); the binding walk's raw blank is not exported
        ck("P3: ...and no record was validated (the #20 blank/refusal collapse)",
           (xstat >> 7) & 1, 0u);"""),
])
print("pp_shadow harness edits applied")

# 6. milan_dp's pool legs, which run only once gmstep and gptp pass (item 4). The
#    image-less benches (sim_main.cpp: main, nolpf, ax1x1; sim_aclk.cpp: aclk)
#    start the walk only to release the listener: with no AEM image the restore
#    ends CLOSED, so either terminal ends their wait. The sim_nxn.cpp legs
#    (notify, nxn, nxndv, nxn8, nxn4c) served AECP with no image and let the image
#    arrive later: AECP is now held from reset until the restore, which needs the
#    image in place before PP_CTRL[1], so the walk starts once the memory answers,
#    the no-image arm grades the hold, and the wedged-response-memory arm runs
#    after the restore.
for rel, tag in (("tb/verilator/milan_dp/sim_main.cpp",
                  'ck("PP_STAT[2] the restore walk sequenced", done, 1);'),
                 ("tb/verilator/milan_dp/sim_aclk.cpp",
                  'ck("[RENDER-BIND] PP_STAT[2] the restore walk sequenced", done, 1);')):
    edit(rel, [("""        for (int r = 0; r < 400 && !done; r++) {
            for (int c = 0; c < 64; c++) step();
            done = (axi_read(A_PP_STAT) >> 2) & 1u;
        }
        """ + tag, """        for (int r = 0; r < 400 && !done; r++) {
            for (int c = 0; c < 64; c++) step();
            //! pin adoption (processor #131): with no AEM image in place the
            //! restore ends CLOSED (busy 0, done 0, fail 1) and the listener
            //! is released all the same, so either terminal ends the walk
            const uint32_t st = axi_read(A_PP_STAT);
            done = ((st >> 2) & 1u) | (((st >> 3) & 1u) & ~((st >> 1) & 1u) & 1u);
        }
        """ + tag)])
edit("tb/verilator/milan_dp/sim_nxn.cpp", [
    ("""    prove_the_identity_and_provision_the_entity_id();
    start_the_boot_restore_walk();
    prove_read_descriptor_degrades_with_no_descriptor_memory();
    prove_a_wedged_response_memory_reports_and_heals();
    if (prove_the_shipped_descriptor_image_enumerates()) return fails ? 1 : 0;
""", """    prove_the_identity_and_provision_the_entity_id();
    prove_aecp_is_held_until_the_restore();
    if (prove_the_shipped_descriptor_image_enumerates()) return fails ? 1 : 0;
    prove_a_wedged_response_memory_reports_and_heals();
"""),
    ("""    void prove_read_descriptor_degrades_with_no_descriptor_memory() {
""", """    //! pin adoption (processor #131): AECP is held from reset until the D3
    //! restore reaches its terminal, and the restore needs the image in place
    //! before PP_CTRL[1] (parent D3 section 8.1). With no image and no walk,
    //! a READ_DESCRIPTOR is held, never answered.
    void prove_aecp_is_held_until_the_restore() {
        dm_answering = false;
        std::vector<uint8_t> pl = {0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00};
        auto r = aecp_xact(0x0004, 0x4000, pl);
        ck("[AECP] before the restore READ_DESCRIPTOR is held, not answered",
           static_cast<long>(r.empty()), 1);
    }

    void prove_read_descriptor_degrades_with_no_descriptor_memory() {
"""),
    ("""        dm_answering = true;

        //! THE SIDE PORT FIRST, so that a zero out of word 34 later can""",
     """        dm_answering = true;
        //! pin adoption: the image is in place, so PP_CTRL[1] starts the
        //! restore walk (the firmware's order); the D3 writer proves the image
        start_the_boot_restore_walk();
        //! the one AECP command held from before the restore is served at the
        //! release (the hold admission); take its answer off the wire here
        {
            const auto held = await_aecp();
            ck("[AECP] ...and the held READ_DESCRIPTOR is answered at the release",
               static_cast<long>(held.size() >= 38 && ((held[34] << 8) | held[35]) == 0x4000), 1);
        }

        //! THE SIDE PORT FIRST, so that a zero out of word 34 later can"""),
    ("""            ck("[AECP-WTMO] the station HEALS when the memory returns (no reset)",
               static_cast<long>(r2.size() >= 38 && aecp_status(r2) == 7), 1);""",
     """            //! pin adoption: this arm now runs after the restore proved the
            //! image, so the healed READ_DESCRIPTOR answers SUCCESS
            ck("[AECP-WTMO] the station HEALS when the memory returns (no reset)",
               static_cast<long>(r2.size() >= 38 && aecp_status(r2) == 0), 1);"""),
])
print("milan_dp harness edits applied")
