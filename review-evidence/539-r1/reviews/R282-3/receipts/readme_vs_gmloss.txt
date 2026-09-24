== README:385-390
What the leg does not grade:

- The grid aligner. The TDM clocks are held, so it stays disengaged. By [owner decision on #387](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5810378282) it gets no re-centre of its own: #539 keeps the step out of its reference at the CRF servo, and #545 and #546 close the remaining paths. Option B, an explicit counted re-lock, is revisited only if #545 or #546 cannot close its path.
- The CRF servo. The MMCM DRP answers zero. `Vphc_step` grades its step discard (#539).
- An lwSRP licence. The talker is opened by `AAF_CTRL[1]`; no SRP peer exists here.
- A step that lands while an `mr` restart is pending. Ruling 5802264260 item 2 merges the two; its arm joins the datapath edit.
== GM_LOSS_RECOVERY.md:176-184
- Streams: the talker keeps streaming and the listener stays locked.

It does not grade these:

- The grid aligner: the leg holds the TDM clocks.
- The CRF servo: its DRP answers zero. `Vphc_step` grades its step discard (#539).
- An lwSRP licence: the escape bit opens the talker.
- A step during a pending restart: tested with the edit.
- The physical re-base: the #117 bench measures it.
== Vphc_step target
10:#   sim_phc_step.cpp -> Vphc_step       : the servo at its SILICON defaults
15:#                 (sim_phc_step.cpp names the slew and talker-step traces)
39:.PHONY: all run trace phc_step_build clean
45:phc_step_build:
47:	  -Mdir obj_phc $(COMMON) sim_phc_step.cpp -o Vphc_step
49:trace: phc_step_build
50:	./obj_phc/Vphc_step +trace_step_ns=$(STEP_NS)
63:	$(MAKE) --no-print-directory phc_step_build
65:	./obj_phc/Vphc_step
== sim_gmstep.cpp:10-24
// mr toggles once and the talker's MEDIA_RESET counts once. The counted event
// is the STEP's: the re-base and the toggle land inside a short window after
// the plane's step pulse, and MEDIA_RESET has not moved between the commit and
// the step, so a re-base keyed to the grandmaster identity fails.
//
// What this leg does NOT grade: the grid aligner (the TDM clocks are held),
// the CRF servo (the DRP answers zero; #539), an lwSRP licence (the talker is
// opened by the escape bit), a step that lands inside a pending mr restart
// (the ruling 5802264260 item 2 arm joins with the datapath edit), and the
// physical re-base (#117).
//
// Elaboration: the `gptp` leg's (AX7101 1x1 TDM8 entity, fabric gPTP ON, the
// fabric clock compressed to 2 MHz so the plane's real timers fit a runnable
// window, the PHC programmed at 8 ns per cycle, CLKV quarter-tick 131072
// cycles). Everything below is in fabric cycles and PHC nanoseconds of this
== broader grep step guard / servo gap wording
docs/history/v1/design/TIME_SYNC.md:405:* a **step guard** discards any window whose error exceeds ~1024 ppm (a
docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:335:| Media clock recovery actuator: MMCM fine-phase-shift FLL/PI servo at clock_source==CRF, XAPP888 DRP verify/repair, step guard against PHC slews, HOLDOVER on CRF unlock (frozen trim keeps stepping) | [hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:172-839](../../../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv#L172-L839) | Milan v1.2 7.3.x media clock recovery + Table 5.7 LOCKED/UNLOCKED (clock domain, served via datapath mux per 5.3.11.2); 1722-2016 10.6/10.8; Xilinx UG472/XAPP888/DS181 (vendor docs) | mmcm_servo (40 checks + rails-cease closed loop), mmcm_servo_autorepair 47/47; silicon IDLE-gating confirmed (task #23 audit) | verified-conformant **2026-08-13: the servo can no longer be ARMED.** Its enable term is `clock_source != 0` and the index is pinned at 0, SET_CLOCK_SOURCE having been its only writer, so `KL_mmcm_drp_servo` is structurally off and `A_MCSRV_STAT` 0x8F8 reads its idle. The 40-check suite and the silicon audit stand; the build has no way to reach the state they grade. |
hdl/ieee1722/crf/KL_media_grid_align.sv:21:                observable). The MMCM servo cannot close that gap: it steers
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:37:                  step guard (2026-07-23 silicon): a local ptp_now
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:54:                  PHC step guard (#539): that threshold alone let a
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:292:  //! step guard: |e| beyond this (1024 ppm at 512 units/ppm) is not a
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:598:            //! step guard: an implausible window error (|e| > 1024 ppm
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:604:            //! status tally is counted below, beside the step guard's
hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:650:        //! PHC step guard (#539, see header): the open window straddles
tb/verilator/mmcm_servo/sim_main.cpp:22://       counted as its sample is staged, which only the PHC step guard
tb/verilator/mmcm_servo/sim_main.cpp:138:    //! The PHC step guard counts on the 2nd: its verdict rides with that
tb/verilator/mmcm_servo/sim_main.cpp:379:    //      Since #539 every one of these JUMPS is the PHC step guard's: the
tb/verilator/mmcm_servo/sim_main.cpp:385:    //      count cannot tell the two guards apart. What only the step guard
tb/verilator/mmcm_servo/sim_main.cpp:391:    //      step guard at the silicon window scale.
tb/verilator/mmcm_servo/sim_main.cpp:472:    //      the step guard, so U10 no longer reaches it). A broken rate
tb/verilator/tsn_fuzz/fuzz_ptp_responder.py:474:        # into the BTCA, servo and canary sections while the gap stood,
