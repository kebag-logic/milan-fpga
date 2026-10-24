[R689] NEGATIVE - exact head 13d8f1e84920aac1dc3e76fb6406c44a744d8145

# R689-1: internal cleared-context review of PR #779 (issue #773)

- **Head:** `13d8f1e84920aac1dc3e76fb6406c44a744d8145`, tree `c4df5628be0a6d6823915aa2421e1a96d724e55b`.
- **Base:** dev `a032c6d6e3775f145349d5a495c1e1ad12294936`, which is also live dev.
- **Diff:** six commits, 15 files.
- **Role:** internal, cleared-context reviewer.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - the issue body and its five public comments (the assignment, TAKEN, STOP, the round 1b ruling `issuecomment-6380110812` and REVIEW READY);
  - the PR body;
  - `git diff a032c6d6..13d8f1e8` and each commit;
  - the public evidence tree `review-evidence/773-r1` at `8f1028e5`.
- **Prior findings:** at review start PR #779 had one comment (the review-start notice) and no PR reviews. There were no prior public findings to resolve or retain.

**Verdict:** NEGATIVE, on one open MINOR (F1, Docs). Conformance, RTL, Robustness and Tests are clean at this head.

## Answers to the review focus

1. **The AAF stamp.** The stamp is `ptp_ns_i[31:0] + transit + LEAD_NS_C` (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv:783-785`).
   - The base is M, the frame instant, through `aaf_tbase_w`.
   - LEAD = (6 + `DELAY_PER_C`) periods, rounded up once (`KL_aaf_packetizer.sv:243-258`).
   - `DELAY_PER_C` is the fewest whole periods covering `LATE_NS_C`, which is `IN_LATE_NS_P` plus the packetizer's own `PIPE_CYC_C`.
   - The integration term is `TLK_SPAN_NS_C` (marker latency less floor(Ps)) plus `age_max_cyc` plus `walk_pair_cyc` to slot 4N-1 (`hdl/milan/milan_datapath.sv:1494-1506`, `hdl/ieee1722/crf/KL_media_if_latency_pkg.sv`). No number is mirrored.
   - I elaborated the shipping parameters in a probe copy, which prints the terms ([receipts/probe_1x1_48k.txt](receipts/probe_1x1_48k.txt), [receipts/probe_8x8_48k.txt](receipts/probe_8x8_48k.txt)):
     - 1x1: LATE 23,851 ns, delay 2 periods, LEAD 166,667 ns, spare 17,815 ns.
     - 8x8: LATE 22,755 ns, delay 2 periods, spare 18,911 ns.
     - Marker latency, age, walk and loopback pairs are 20,964 ns / 1,043 / 86 / 4 at 1x1, and 5,308 ns / 1,043 / 811 / 1 at 8x8.
     - These equal the author's figures, give or take 1 ns of spare rounding.
   - `g_lead_delay` refuses a delay above 125 us. The planted control "terms grow by 125 us" is refused with that message.
   - GET_STREAM_INFO reads 125,000 on every output (milan_dp `#773 GET_STREAM_INFO reads 125 us on every output`, [receipts/milan_dp_nxn.log](receipts/milan_dp_nxn.log)).
   - The transit row is not touched.
2. **CRF.** `ts_r <= ev_ns_i + mtt_ofs_r + TC_NS_C` (`hdl/ieee1722/crf/KL_crf_tx.sv:544`).
   - TC is the fewest whole periods covering `EV_LATE_NS_P` (marker latency + 1 cycle) plus `NUM_BEATS + 1` cycles.
   - Probe: 1x1 is 21,164 ns, so TC is 2 periods (41,667 ns) with 20,502 ns spare. 8x8 is 5,508 ns, so TC is 1 period (20,834 ns) with 15,325 ns spare.
   - `KL_mtt_round` and `ROUND_MTT_P = 0` are untouched, so the offset's round-up is unchanged.
   - The dp leg measures the CRF margin at exactly 20,503 ns in every run.
   - Observation, not a finding: TC is rounded separately from the offset. At a fractional-period offset the stamp can sit up to 1 ns above a single rounding. For example, 2,010,000 ns gives 2,020,834 + 41,667 = 2,062,501 ns against an exact 2,062,500. It is still rounded up, as 10.7 requires, and is three orders below 10.8's +/-1,041 ns.
3. **Commit 041b7922.** It drops the arbiters' frame-ahead term from `LATE_NS_C`.
   - This matches the ruling's 23.8 / 22.7 us, which the STOP figures took with "no other frame in flight".
   - At both shipping shapes, counting the term would give the same periods. AAF: 27,811 / 26,715 ns, still 2. CRF: 25,564 / 9,908 ns, still 2 and 1. So no shipping stamp changes.
   - TUmax only enters Equation (1)'s lower bound. The leg holds that bound with margin: AAF at most 59,807 ns and CRF 20,503 ns against 125,000 ns.
   - The upper bound under a frame ahead rests on the spare, by derivation. A CRF PDU plus a 190-beat maximum frame is 3,960 ns, and an AAF PDU plus one maximum frame is 4,400 ns. Against the 17.8 / 18.9 / 20.5 / 15.3 us spares, that is covered.
   - **One maximum-size frame ahead at the MAC, at line rate.** The PR does not claim this; it scopes the MAC out. By my derivation at 1 Gb/s, one 1,542-byte wire slot is 12,336 ns. With the other stream's PDU ahead, about 12.9 us (AAF) or 14.4-14.9 us (CRF) of the spare is used. That leaves roughly 4.8 us (1x1 AAF), 6 us (8x8 AAF), 6.1 us (1x1 CRF) and 0.4-0.9 us (8x8 CRF). So it is covered at 1 Gb/s, thinly for 8x8 CRF, and not at 100 Mb/s. This is derived, not measured (S2).
   - The guard does not see the frame-ahead term: see S1.
4. **capture_coherence dp at head.** 847 checks, 0 failures, over 31 runs: 23 at 2 ms and 8 at 125 us ([receipts/cc_dp.log](receipts/cc_dp.log), [receipts/cc_dp.wire_summary.txt](receipts/cc_dp.wire_summary.txt)).
   - `[WIRE]`: AAF margin 17,823..59,807 ns over 8,013 PDUs, and CRF margin 20,503 ns over 479 PDUs, at both offsets.
   - `[GRID]`: 0 off for AAF and CRF.
   - `[HOLD]`: at most 2,059,807 ns at 2 ms and 184,807 ns at 125 us.
   - `[PIN]`: maximum 15 ns.
   - The suite's own driver ran the 7 new planted controls and both positive controls: 9 PASS, 0 FAIL ([receipts/cc_773_controls.log](receipts/cc_773_controls.log)). Each control failed every check it names.
   - Two probes of my own, each failing `[GRID]` alone (18 failures each, 0 elsewhere): the AAF lead rounded down to 166,666 ns, and the CRF TC rounded down to 41,666 ns ([receipts/probe_pa.run.log](receipts/probe_pa.run.log), [receipts/probe_pc.run.log](receipts/probe_pc.run.log)). So `[GRID]` is exact to the nanosecond.
5. **Phase and presentation.**
   - At this head: `milan_dp_render tdm8render` passes 263/0 ([receipts/tdm8render.log](receipts/tdm8render.log)) and media_phase passes ([receipts/media_phase.log](receipts/media_phase.log)).
   - At `bf2d96f9`, whose difference from the head reaches only the aaf suite: the author's tdm8render-mutants 31/31, gmstep-mutants 23/23 and pull-in (19 legs, 0 failures) receipts carry over.
   - The render-queue margin at the 2 ms default is not 513.3 / 492.4 us for every PDU. The PDU stamped from the live-PHC fallback arrives 2,059,807 ns ahead, which leaves about 492.1 / 487.0 us. That still holds the 2 ms default (F1).
6. **Gates.**
   - **The sweep's head is enough.** `bf2d96f9..13d8f1e8` changes only `tb/verilator/aaf/start_mutants.py`. Its only build reader is `tb/verilator/aaf/Makefile`; the other hits are inventory and digest files ([receipts/clone_integrity.txt](receipts/clone_integrity.txt)). At the head, aaf passes 34,020/0 and its startup mutants are caught 8/8 ([receipts/aaf.log](receipts/aaf.log)). So the other 63 suites' verdicts carry by input identity, and the sweep need not re-run for source evidence. The merge-candidate full bar stays the manager's.
   - **Run at this head:**
     - lint: 89 <= 89, PASS ([receipts/docs_gates.log](receipts/docs_gates.log));
     - 21 docs-gate steps, rc 0 under GNU Make 4.4.1, with the bare-metal gate rerun under a python3 that has pyyaml ([receipts/docs_gates.summary](receipts/docs_gates.summary), [receipts/baremetal.log](receipts/baremetal.log));
     - `cd tests && behave`: 406 scenarios passed ([receipts/behave.log](receipts/behave.log));
     - crf_tx 129/0 and chmap_capture PASS;
     - milan_dp run-nxn and run-nxn8, built and run in one `make -j3`: two verdicts, 2,098/0 and 3,998/0, rc 0. Their output is interleaved in one log.
   - **Accepted from the author's receipts:**
     - route-1x1: SLICE -11, WNS +0.040 ns against the +0.03 floor, route complete. The sub-block LUT movements sit in `u_pp`, not in the changed modules.
     - Yosys 60/60 at `bf2d96f9`.
   - Hosted runs at the exact head were still queued or in progress at review time ([receipts/hosted_check_runs.tsv](receipts/hosted_check_runs.tsv)).
7. **8x8 derivation.** The terms are complete for the datapath port with the MAC ready:
   - the span-to-close term is negative on TDM32;
   - the age is one tick spacing plus 1;
   - the walk runs to slot 31 at 26 cycles a slot, with loopback off on the shipping 8x8;
   - the packetizer takes 60 cycles with the CFG reads.

   The engine serves one talker in 62 cycles against 104-cycle pair spacing, so talkers do not queue on each other. A maximum frame at `adp_tx_mux` delays later talkers by at most 190 cycles. That delay decays by 42 cycles a talker, and the 512-cycle gasket spacing keeps a second frame off talker 7. That is within one frame ahead.

   Not counted: media-clock drift. At +/-1000 ppm it adds about 150 ns (five longer frames and the longer bit time), and the spare covers it. Measured 1x1 minima sit at or above the derived spare.

## Findings

### F1 — MINOR — Docs — the listener-buffer figures leave out the PDU stamped from the live PHC, and one unchanged range statement is now stale

**Where:**
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:1852-1858`, "The listener's buffer";
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:2000-2004`, the supported-range paragraph;
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191`, row 5.3.7.6 / 4.4.2.1.

**Authority:**
- AGENTS.md section 6, Docs: changed contracts are reflected in authoritative docs.
- The PR's own `[HOLD]` evidence.
- `sim_dp.cpp:541-549` states that a PDU whose first pair precedes the grid is stamped from the live PHC.
- `milan_datapath.sv` `aaf_tbase_w` applies the lead to that base too.

**Evidence:**
- **The stated maxima are false for one PDU.** The page says a PDU "arrives at most 2,038,676 ns (1x1) or 2,054,392 ns (8x8) before its timestamp". The compliance matrix says "at most 2,054,392 ns ... (capture_coherence `[WIRE]`, `[HOLD]`)".
  - The cited leg measures `[HOLD]` at 2,059,807 ns in every 2 ms run.
  - That is the fallback PDU: margin 59,807 ns = 166,667 - 106,860. It is the one PDU per run that `[GRID]` excludes.
  - The 8x8 talker 0 fallback derives to the same 2,059,807 ns.
- **The margins follow from the wrong maxima.** The 513.3 / 492.4 us render-queue margins are computed from those figures. With the fallback PDU's last event at 2,163,974 ns after arrival, the margins are about 492.1 us (1x1) and 487.0 us (8x8).
- **The unchanged paragraph is now stale.** It says a PDU's lead at arrival is "the talker's presentation time offset less the PDU's transit (the talker's capture to this listener's depacketizer)". It concludes "at the 2 ms default, any transit under 1,968,881 ns (1x1)".
  - Since #773 this device's own talker stamps its capture instant plus 8 Ps plus the offset. Its lead at arrival is therefore the offset plus 166,667 ns less that transit.
  - So the 1,968,881 ns bound and "offsets up to 2,656,119 ns plus the transit" no longer describe this device's talker. With the lead they would be 2,135,548 ns and 2,489,452 ns plus the transit.

**Impact:** An integrator sizing a listener buffer from these pages, or a reviewer reading the compliance row's evidence, gets a maximum the cited test itself contradicts. Conformance still holds: 2,059,807 ns is inside 2.126 ms, and the queue still holds the 2 ms default.

**Required outcome:**
- The two pages state the bound that includes the live-PHC fallback PDU (2,059,807 ns, measured at 1x1), or qualify the grid-live figure and state the fallback's separately.
- They state the render-queue margin that follows (about 492.1 / 487.0 us).
- The supported-range paragraph either says how this device's talker's 8 periods enter the lead, or limits its statement to the offset plus the talker's own fixed periods.
- The REVIEW READY's "513.3 us / 492.4 us to spare" is corrected where it is restated.

**Verification:** Re-read the pages against `[HOLD]` in the dp leg's log: the stated maximum must be at least every run's `[HOLD]` maximum at 2 ms. Then recheck `docs_check.py`, `check_doc_style.py` and `gen_toc.py --check`.

### R1 — RESIDUE — a header comment in an unchanged file now under-describes the AAF stamp

**Where:** `hdl/ieee1722/crf/KL_media_domain_event.sv:28-31`.

**Problem:** It says "the CRF output adds its offset rounded to whole periods (10.7 Eq. 14), an AAF talker its offset as set". Since #773 each output also adds its whole-period capture-to-wire terms.

**Exact fix:** Replace those lines' tail with "the CRF output adds Equation (14)'s TC and its offset rounded to whole periods (10.7 Eq. 14), an AAF talker its crossing estimate and fixed delay (whole periods, #773) and its offset as set (Milan v1.2 5.4.2.9, #632)."

This is wording only.

### S1 — SUGGESTION — RTL, Robustness — the 125 us guard does not see the frame-ahead wait that 041b7922 removed

**Where:** `KL_aaf_packetizer.sv:243-265`, `KL_crf_tx.sv:302-317`, `milan_datapath.sv:1484-1494`.

**What the probe shows:** The arbiters' wait (198 / 220 cycles at the fixed 50 MHz product clock) is now covered by the spare only by documentation. My elaboration probe of the 1x1 TDM8 master at 192 kHz with 16-bit slots ([receipts/probe_1x1_192k16.txt](receipts/probe_1x1_192k16.txt)) derives 2 periods with 2,206 ns spare. That is under the 3,960 ns frame-ahead wait, and nothing refuses it. The builder can plan that clock: 49.152 MHz.

**Why it is not a finding:** That shape is not a Milan Base-format talker anyway, since the packetizer fixes 6 samples a PDU and 192 kHz needs 24. At 96 kHz the spare is 7,422 ns.

**Option:** an elaboration check that the spare covers one frame ahead whenever `CLK_HZ_P` is the product clock, or a stated condition beside `g_lead_delay`.

### S2 — SUGGESTION — Docs — state the MAC-level bound

Beside "The MAC's own backpressure is outside the datapath", state the 1 Gb/s figure:
- one maximum frame ahead at the MAC uses 12.3 us of the spare;
- by derivation about 0.4-0.9 us remains for 8x8 CRF;
- 100 Mb/s is not covered.

### S3 — SUGGESTION — Tests — measure the contended path

Add one dp scenario that forces a CRF PDU and a maximum control frame ahead of the worst-age AAF PDU. The spare's cover of a frame ahead would then be measured as well as derived. The measured minimum, 17,823 ns, sits 7 ns above the uncontended derived spare, so no run met contention at that moment.

## Clean-lens results

- `[R689] PASS Conformance — KL_aaf_packetizer.sv:243-265,783-785; KL_crf_tx.sv:302-317,544; milan_datapath.sv:1494-1506,1520,7441; dp leg receipts/cc_dp.wire_summary.txt; milan_dp receipts/milan_dp_nxn.log`
  - Checked against IEEE 1722-2016 4.3.3 Eq. (1), 4.3.5 and 10.7 Eq. (14); Milan v1.2 5.3.7.6, 5.4.2.9 and 5.4.2.10.2; and the round 1b ruling.
  - Stamp = M + 8 Ps + offset as set. The fixed delay is 2 Ps, refused above 125 us.
  - CRF TC is 2 / 1 Ps.
  - Equation (1) holds both ways at 2 ms and 125 us for every PDU.
  - GET reads the offset as set.
  - F1's figures are documentation only; the 2.126 ms conformance holds.
- `[R689] PASS RTL — KL_aaf_packetizer.sv:663-785; KL_crf_tx.sv:540-546; KL_media_if_latency_pkg.sv walk_pair_cyc/age_max_cyc; milan_datapath.sv:1255-1290,1457-1530,8654-8960; receipts/probe_*.txt`
  - Widths: 32-bit stamp modulo 2^32, 64-bit CRF.
  - Signed `IN_LATE_NS_P` handles a negative TDM32 span.
  - The default-off parameters leave other instances unchanged.
  - The pipeline cycle counts match the FSM: E_IDLE, E_CRD, E_DRD and E_SEND, with writeback 2.
  - The derived constants at both shapes match the elaborated design.
  - The constants fold into existing adders. route-1x1 SLICE -11, WNS +0.040 ns (author receipt).
- `[R689] PASS Robustness — sim_dp.cpp:541-640 (fallback PDU, 2 ms/125 us); milan_dp offsets 2 ms, 1 ms, 2,010,000 ns, 125 us (receipts/milan_dp_nxn.residuals.txt); receipts/probe_1x1_96k.txt, probe_1x1_192k16.txt`
  - The live-PHC fallback PDU stays inside Equation (1): margin 59,807 ns.
  - The fractional-period offset keeps one whole period count per output.
  - The fixed delay is refused above 125 us.
  - Drift of +/-1000 ppm is within the spare.
  - Non-shipping rates were probed (S1).
- `[R689] PASS Tests — sim_dp.cpp:106-140,550-640,757-766; mutants.py:120-140,269-293; sim_nxn.cpp:8654-8880; tb/verilator/aaf/start_mutants.py:32; receipts/cc_773_controls.log; receipts/probe_pa.run.log, probe_pc.run.log`
  - The constants are stated independently of the RTL.
  - All 7 controls are caught by their named checks, and both positive controls pass.
  - My two 1 ns probes are caught by `[GRID]` alone.
  - The aaf startup pattern is fixed: 8/8.
  - milan_dp's window tightened from -200,000..30,000 to 0..<125,000.
  - The contended path is not exercised (S3).
- Docs is UNCLEAN: F1 is open. R1 and S2 are recorded.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | KL_aaf_packetizer.sv, KL_crf_tx.sv, milan_datapath.sv #773 block; dp leg 31 runs `[WIRE]`/`[GRID]`/`[HOLD]`; milan_dp GET 125 us; ruling (b) | R689-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| RTL | CLEAN | the same RTL plus KL_media_if_latency_pkg.sv, TX arbiter chain, elaboration probes at 1x1/8x8 48 kHz, 1x1 96 kHz and 192 kHz | R689-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Robustness | CLEAN | fallback PDU, offsets 0-path/125 us/1 ms/2 ms/2,010,000 ns, derivation under drift, non-shipping rates | R689-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Tests | CLEAN | sim_dp.cpp, mutants.py (9/9 at head), sim_nxn.cpp, aaf start_mutants.py (8/8), two reviewer probes | R689-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |
| Docs | UNCLEAN (F1) | MEDIA_CLOCK_FOLLOWING.md #773 section and the supported range, MILAN_COMPLIANCE_MATRIX.md rows 191/227, TESTING.md, CHANGELOG.md, PR body; docs gates rc 0 | R689-1 | 13d8f1e84920aac1dc3e76fb6406c44a744d8145 |

## Real limits

- **Not re-run at this head; author receipts accepted:**
  - Vivado (route-1x1, ooc-1x1, ooc-8x8);
  - the full Verilator sweep, accepted from `bf2d96f9` by input identity;
  - the Yosys bank;
  - xvlog;
  - the tdm8render-mutants, gmstep-mutants and pull-in campaigns;
  - the docs builder legs.
- **Docs gates:** run under GNU Make 4.4.1, not 4.3. The em-dash step is my own added-line scan.
- **capture_coherence mutation arm:** of its 41 units I ran the 9 that #773 adds or re-proves: the dp/dp-band positive control and the 7 controls. A first whole-arm attempt ended without a verdict, with no OOM kill recorded, and is not counted.
- **8x8 TDM32:** checked by elaboration and derivation only; no harness runs it at its clocks.
- **The MAC-level figures (focus 3):** derived, not measured.
- **Hardware:** no bench, no physical calibration, no hardware proof. Field skips are not proof.
- **Hosted contexts** at the exact head were mostly queued or in progress at review time. I did not inspect them further.

## Pending manager duties

- Carry F1 to the author and re-review the Docs lens at the corrected head. A docs-only correction does not touch the other four lenses' scope.
- Carry R1 to the residue checklist.
- Own hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate with the builder and native banks.
- Decide whether #773 closes at this merge. The PR says "Relates to #773", because the 8x8 proof is derived only, which the ruling allows. AGENTS section 7 needs the issue closed at merge or by hand.
- Confirm route-1x1 against the eleventh record at the merge candidate, if the candidate's RTL differs.

R689-1 FINISHED
