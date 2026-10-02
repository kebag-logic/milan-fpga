[R432] NEGATIVE - exact head 57f4b742b504f5e69293aaa3e00d0470aa9b6071

# R432-1: internal cleared-context review of PR #634 (issue #629, lane M2)

- Head under review: `57f4b742b504f5e69293aaa3e00d0470aa9b6071`, tree `499d64f0750f3bc3caf699ee754428dbdeea6e07`, 17 commits on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- Hosted CI validates merge commit `1a5e4b788a399e0c5a7a73128607d477f1fe31bf`, whose tree is the same `499d64f0` (parents `cdf49d1a`, `57f4b742`). So hosted results are results on the head's exact bytes.
- Reconstructed in order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the #629 body, the design-lane rulings (5935520588, 5937449258), the owner decisions (5937643550 D4 = A2-a, 5937848189 oscillator risk), the round-4 loss-rule choice (5938156583), the lane M2 assignment (5942692103), the author's STOP (5946475441) and the ruling accepting its eight deviations (5946491571); `docs/design/MEDIA_CLOCK_FOLLOWING.md`; FR_NFR, REGISTER_MAP, compliance matrix and TESTING; the full diff `cdf49d1a..57f4b742` and its 17 commits; the public evidence at `f7cb2d68:review-evidence/629-m2-r1` (MANIFEST hashes re-verified); the hosted check runs at the head.
- Prior public review findings on PR #634: none exist at this head. The PR has zero reviews; its only manager comments are the two review-start notices. Nothing to resolve or retain.

## Verdict in one paragraph

The RTL is a faithful implementation of the merged design. I re-read the AAF clock meter against every rule of the design and found no functional defect. The format check, mod-16 groups, group mean, 4,096 ns bound, void rule, loss rule (b) with the k = 2 check and midpoint fill, E8 ring, lock, era, `mr` seed and `disrupt_p` rule are all correct. So are the decode, W2, C1, A2-a and the CSR words. I re-ran both new suites and all 40 author mutants: every mutant is killed by its named check. The area figures reproduce exactly. The verdict is NEGATIVE for other reasons. Three gates that are required on the PR fail at this exact head and pass at the base, in an identical environment (F1, F3). The new root suite's own default target fails on the hosted runner, so its 14-mutant campaign never ran in CI (F2). Other findings are below.

## Findings

### F1 - MAJOR - Tests, Robustness, Conformance - the NVM capture-timing receipt is stale; the hosted `docs-check` is red

- **Where:** `scripts/check_nvm_capture.py:51-55` against `tb/verilator/nvm_capture_cpu/measurements.json:24` (`measured_for`). Hosted `docs-check` step 29 "Capture measurement census and clock gate": failure, job 110727522363 of run 36971935308.
- **Evidence.**
  - #629 adds the AAF listeners' CLOCK_SOURCE descriptors. Their NAME records grow the saved-state census:
    - 8x8: 156 to 164 records, 12,634 to 13,210 raw bytes;
    - 1x1 TDM8: 53 to 54 records, 3,218 to 3,290 bytes.
  - The capture-timing receipt was measured for the old census, and the gate refuses that by design ("capture inputs changed; remeasure both arms").
  - Receipts: `receipts/check_nvm_capture_base.txt` is rc 0 at `cdf49d1a` and `receipts/check_nvm_capture_head_scratch.txt` is rc 1 at the head, in the same environment. `receipts/check_nvm_capture_head.txt` is rc 1 in the review clone. `receipts/hosted_docs_check_failed_step.txt` is the hosted failure.
  - The published gate table does not list this gate.
- **Impact.**
  - A required CI context is red at the head, so the PR cannot meet AGENTS section 7.
  - The power-cut capture time of the larger record set (Milan saved state, the 49 ms hold floor) is unmeasured. The old 8x8 maximum was 13.23 ms against the 24.5 ms limit, so a pass is likely, but the receipt is the contract's evidence.
  - Hosted `docs-check` skipped steps 30 to 51 after this failure, so those contexts never executed at the head (see F3).
- **Required outcome:** remeasure both arms at every required point for the new census, through the harness's own recipe. The gate must then pass at the new head.
- **Verification:** `python3 scripts/check_nvm_capture.py` rc 0 at the new head. Hosted `docs-check` must be green with steps 29 to 51 executed.

### F2 - MAJOR - Tests, Conformance - the root suite's default target fails on the hosted runner; its 14 named mutants never compiled in CI

- **Where:** `tb/verilator/milan_dp_mclk/Makefile:51` and `:59`, the `$(shell $(MAKE) -s -C $(DP) print-srcs)` and `print-dp-vflags` calls. They lack `--no-print-directory`.
- **Evidence.**
  - Hosted "Verilator shard 2/5" (run 36971935590, merge tree = head tree) reports `FAIL milan_dp_mclk` and "NOCOUNT ... printed no tally line at all".
  - The suite log shows the schemata build fed make's chatter to the simulator as sources: `%Error: Cannot find file containing module: 'Entering'`, `'directory'`, `'Leaving'`, then `[FAIL] the schemata did not compile; no mutant proves anything`.
  - Cause: GNU make 4.3 hands a recipe of `make -C` the flag `MAKEFLAGS=w`. `mclk_mutants.py`'s nested `make mclk-build` inherits it, and the derived source list captures "Entering/Leaving directory".
  - Reproduced locally: with `MAKEFLAGS=w MAKELEVEL=1`, `SRCS_DP` contains `make[2]: Entering directory ...` tokens; at top level it is clean (`receipts/mclk_makefile_print_directory_probe.txt`).
  - The repository already records this exact defect and its fix: `tb/verilator/capture_coherence/Makefile:92-105` (`--no-print-directory`, "#617 R394-3 F1").
  - The local passes (the author's, and mine: `receipts/mclk_suite.txt`, 27/27, all 14 mutants caught) ran the driver without a parent make, or under GNU make 4.4.1.
  - Receipts: `receipts/hosted_shard2_summary.txt`, `receipts/hosted_milan_dp_mclk_log_excerpt.txt`.
- **Impact.**
  - Assignment item 4 is not met in CI: "Add the campaign to the PR gate within the suite time guards". Every root row's named mutant (decode, reference mux, A2-a, W2, switch, C1, CSR, stale table) is unproven on the gate that protects dev.
  - The PR body's "How to validate" (`make -C tb/verilator/milan_dp_mclk`) fails on the reference runner.
- **Required outcome:** the suite's default target builds its schemata and passes on the hosted runner. The nested source-list and flag derivations must be immune to an inherited print-directory flag.
- **Verification:**
  - hosted "Verilator shard 2/5" green with `milan_dp_mclk` tallied and 14/14 mutants caught;
  - locally, `MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk` rc 0.

### F3 - MINOR - RTL, Docs - two port-contract ratchets fail at the head on the meter's boundary

- **Where:**
  - `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:108` `CLK_FREQ_HZ_P`, `:137` `fsh_i`, `:152` `status_o`, against the naming ratchet (`scripts/naming.budget:22`, 95 candidates);
  - `:113` `clk_i`, `:114` `rst_n`, `:130` `subtype_i`, with no `//!` contract, against `scripts/port_docs.budget:23` (`undocumented hdl 217`).
- **Evidence.**
  - `scripts/measure_naming.py --check`: "NAMING RATCHET: FAIL (3 new, 0 stripped)", naming these three boundaries.
  - `scripts/check_port_contracts.py`: "PORT-DOC RATCHET: FAIL (hdl: 220 undocumented > ratchet 217)". `receipts/port_docs_attribution.txt` attributes the +3 to the meter's `clk_i`, `rst_n` and `subtype_i`.
  - Both gates pass at `cdf49d1a` and fail at the head in the same scratch clone (`receipts/ratchets_base.txt`, `receipts/ratchets_head.txt`).
  - Both are hosted `docs-check` steps 33 and 34, skipped there because of F1. They are absent from the published gate table.
  - CONTRIBUTING section 1: "Ports documented inline with `//!` - the port list IS the spec".
- **Impact:** two more required gates are red at the head. The new module's boundary is not reviewable from its port list alone.
- **Required outcome:** both ratchets pass, without raising either budget, by documenting and naming the meter's boundary per CODE_QUALITY rules 4 and 5.
- **Verification:** `python3 scripts/measure_naming.py --check` and `python3 scripts/check_port_contracts.py` rc 0 at the new head.

### F4 - MINOR - Tests, Conformance - the design-named mutant "`tu` taken from the `tv` net" exists in neither campaign

- **Where:**
  - design `docs/design/MEDIA_CLOCK_FOLLOWING.md:1299`, the meter restarts row: "Separately, `tu` taken from the `tv` net (the CRF wiring): the `tu` case fails";
  - `tb/verilator/aaf_clock_meter/mutants.py:46-150`, which has no such mutant;
  - `tb/verilator/milan_dp_mclk/mclk_mutants.py`, ids 1 to 14, none of them this one;
  - `tb/verilator/milan_dp_mclk/sim_mclk.cpp:369`, `f[17] = 0x00; // tu clear` on every AAF frame;
  - `tb/verilator/aaf_clock_meter/sim_main.cpp:491-492`, whose comment claims "Mutants: ... tu read from the tv net."
- **Evidence.**
  - The wiring at `hdl/milan/milan_datapath.sv:5689` (`.tu_i (avtprx_tu_bit)`) is correct. I checked it against the parser outputs at `:5524-5527`.
  - That wiring is the trap the design calls out: `KL_crf_rx` takes `tv` at `:5622`.
  - No root stimulus ever sets an AAF `tu` bit, and the meter suite drives the meter's `tu_i` port directly. So a root miswiring of `tu_i` to `avtprx_tv_bit` would pass every check.
  - This deviation is not among the eight named in the STOP, nor in the design's Implementation notes.
- **Impact:** assignment item 4 ("every row ... each shown failing under its named mutant") is unmet for this row. A regression to the CRF wiring, the exact trap the design warns of, would ship silently.
- **Required outcome:** a root check that a followed AAF stream's `tu` edge restarts the meter's history, shown failing with `tu_i` bound to `avtprx_tv_bit`. Alternatively, a ruling that records the deviation. The meter harness comment must match what exists.
- **Verification:** the new check fails under the named mutant and passes clean.

### F5 - MINOR - Tests, Robustness - meter rules stated by the design that no test can fail

- **Where:**
  - `tb/verilator/aaf_clock_meter/sim_main.cpp:670-694` (M12) against design `:1304`;
  - `KL_aaf_clock_meter.sv:246` (`lock_clr_w`), `:457` (gap breaks settle) and `:269` (`channels_per_frame` nonzero);
  - design `:968-976` and `:986-993`.
- **Evidence:** reviewer-own mutants (`scripts/reviewer_meter_probes.py`, `receipts/reviewer_meter_probes.txt`). Each one passes all 308 meter checks.
  - (a) **Round 4's rule restored:** the deviation verdict is deferred to PDU 15, so a loss-voided group is never checked (`deviation_verdict_deferred_to_pdu15`). The design row's pass criterion says positions 1 to 14 of placement (b) restart "at the step's PDU, by the deviation check before the gap". M12 counts restarts but never where they occur. Rule 1 of round 5 ("the deviation check up to the gap") therefore has no failing test.
  - (b) **A change of the followed listener keeps a held lock** (`listener_change_keeps_lock`). It also passes the root suite's `--switch` leg and the full leg B (`receipts/root_probe_listener_change_keeps_lock.txt`).
    - The design makes this silent clear part of "one request per switch".
    - With the lock kept, a switch onto a talker silent for at least 100 ms would time out while "locked" and pulse `disrupt_p`, a second request.
    - Switch case (ii) starts the new talker after 5 ms, so it cannot see this.
  - (c) **A sequence gap no longer breaks the settle run** (`gap_does_not_break_settle`).
  - (d) **The bind edge clears a held lock**, which the design says it must not do (`bind_edge_clears_lock`).
  - (e) **`channels_per_frame == 0` accepted** (`cpf_zero_accepted`).
  - For contrast, the probes on nsr, format, sp, tv, STOPPED, the mean arithmetic, the k = 2 count, the restart count and the settle count are all caught.
  - The `max_dev_not_tracked` probe escapes the meter suite but is graded at the root (`sim_mclk.cpp:731`), so it is not part of this finding.
- **Impact:** regressions in these design rules, (b) above all, would ship undetected.
- **Required outcome:** each listed rule has a check that fails under the corresponding probe. For (a), the restart's PDU or cycle is graded.
- **Verification:** re-run `reviewer_meter_probes.py` (published here). Each listed probe must then be CAUGHT, and (b) must also fail at the root.

### F6 - MINOR - Docs, Tests - the `obj_aclk` row cites a mutation script that does not exist

- **Where:** `tb/verilator/milan_dp/README.md:74`: "`aclk_a2a_mutants.py` disengages it at INTERNAL and requires the phase to fail".
- **Evidence:** no such file is tracked (`git ls-files` finds none). `sim_aclk.cpp`'s banner instead points to `milan_dp_mclk` mutant 3, which does exist and is caught (`receipts/mclk_suite.txt`).
- **Impact:** a suite README states verification evidence that does not exist. A cold reviewer would look for a negative arm that is not there.
- **Required outcome:** the row names the campaign that actually grades A2-a's disengagement (mclk mutant 3), or the named script exists and runs.
- **Verification:** every artifact the row names exists and runs.

### F7 - MINOR - Docs, Conformance - the FR register's status row contradicts the feature ledger at this head

- **Where:** `docs/reference/FR_NFR.md:156`, which reads "AAF following required by the #629 owner decision, implementation in progress". Against it stand `:137` (`aaf.media-clock-following` `implemented`) and `docs/reference/milan_feature_status.json`.
- **Evidence:** the status row was written in the first commit (`baa0a8a1`), before the implementation, and was never updated. At the head the implementation is present, and the same file marks the feature implemented.
- **Impact:** the requirements register gives two status verdicts for one feature.
- **Required outcome:** one status, consistent with the ledger. For example: "AAF following implemented in simulation (#629); bench probe open".
- **Verification:** read `FR_NFR.md:137` and `:156` together.

### RESIDUE (owner rule 2026-10-02: wording only; no effect on verdict or lens)

- **R1.** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1456`, Implementation notes, VERSION row.
  - Replace "Open for a decision on #629" with "Kept by the ruling on #629 (comment 5946491571)".
- **R2.** `docs/design/MEDIA_CLOCK_FOLLOWING.md:1463`, Where column.
  - Replace "HANDOFF area table" with "`syn/yosys/ooc.sh KL_aaf_clock_meter` (Yosys out-of-context: 574 LUT including 16 LUTRAM, 636 FF, 0 RAMB18, 0 DSP)".
  - Reason: the pointer names no artifact in the repository. I reproduced the figure exactly (`receipts/ooc_meter_direct.txt`).
- **R3.** PR #634 body.
  - Status line: replace "STOPPED FOR A RULING, otherwise GREEN" with the post-ruling state.
  - Known limitations: replace "Needs a decision on #629" with "Kept by the ruling on #629 (comment 5946491571)".
- **R4.** `docs/testing/TESTING.md:517`.
  - Replace "`mclk_mutants.py` runs both legs beside fourteen named mutants" with "`mclk_mutants.py` runs the three legs (A, B, C) beside fourteen named mutants".

### SUGGESTION (optional)

- **S1.** `hdl/milan/milan_datapath.sv:6271`, `src_grid_ok_w = !follow_sel_r || ...`
  - Under A2-a the aligner is now engaged at INTERNAL too, but INTERNAL still counts as always inside the settle band. So a #386 recentre armed at INTERNAL (boot engagement, or a returned TDM feed) fires 2,048 ticks later whether or not the pull-in has finished.
  - This matches the design's settle table (`follow_sel_r`) and TIME_SYNC's "at INTERNAL: 2048 ticks after the change". The render pins show no counted skip or underrun at INTERNAL (`milan_dp_render` T30/T31).
  - Consider keying the band test on `mga_sel_w`, or record why the pre-A2-a dwell stays adequate.
- **S2.** `docs/reference/FR_NFR.md`, FR-CLK-04: "`mr` MUST toggle ... on a disruption of the followed stream (IEEE 1722-2016 4.4.4.3)".
  - The design's (d) item 5 notes that the literal shall names CRF only, and that the AAF case is the PICS AAF-5 reading. The compliance matrix 4.4.4.3 row states this carefully.
  - Consider the same qualifier in FR-CLK-04.

## Focus checks that came out clean (evidence)

- **Builder and model.** All five shipping configurations declare `[internal, crf, input_stream]`. The generated tables:
  - 1x1 shapes: INTERNAL 0, CRF 1 on SI 1, AAF on SI 0;
  - 4x4 and 8ch: CRF on SI 4, AAF 2..5 on SI 0..3;
  - 8x8: CRF on SI 8, AAF 2..9 on SI 0..7.

  `check_entity_shape.py` reports 166 checks with 0 failures, and states for each of the five that "configs/generated copy is current", so there are no hand edits (`receipts/check_entity_shape.txt`). Its self-test also passes. CLOCK_DOMAIN uses the identity list. `clock_source_flags` 0x0002 is relabelled LOCAL_ID; IEEE 1722.1-2021 Table 7-16 puts LOCAL_ID at bit 14, so the value is unchanged. arty_current's pinned model id moves; the hash-derived ids move with the model (IEEE 1722.1-2021 6.2.2.8). `crf_sink` still requires `crf`, so the `n_crf` to `'crf' in srcs` change drops nothing. Builder tests carry the D1 order on every shape, the no-INTERNAL order graded at `_overlay_clock_sources`, and the planted-L2 negative control.
- **Meter RTL** (`KL_aaf_clock_meter.sv`, read line by line):
  - format fields at the right bit positions of `fsh` bytes o+16..o+23 (`avtp_stream_parser.sv:176`), per IEEE 1722-2016 Figure 26 and Tables 9 and 11;
  - `stream_data_length` = 24 x cpf, as a shift-add;
  - group open, void and mean; floor division; 20-bit sum headroom;
  - k from `seq[7:4]` mod 16, with k = 1 at 4,096 ns, k = 2 at 5,120 ns, and every other k restarting;
  - the midpoint fill only when the voided group is a snapshot point;
  - the E8 read-old, write-new ring, valid after 2,048 intervals;
  - era and lock clears, and `disrupt_p` only on the meter's own timeout while locked;
  - silent `mr` seed, and the enable gating every output;
  - the pipeline spacing assumption holds at TDATA_WIDTH 64 (8 cycles at least).
- **Simulation, re-run with the pinned 5.050 simulator.**
  - Meter suite: 308/0 and servo-with-meter 6/0 (`receipts/aaf_clock_meter_run.txt`).
  - All 26 author meter, servo and unit mutants killed by their named checks (`receipts/meter_mutants_batch1.txt`, `batch2.txt`).
  - Root suite: legs A 50/0, B 44/0, C 32/0; 10 controls pass; 14/14 mutants caught (`receipts/mclk_suite.txt`, run without a parent make; see F2).
  - Reviewer probes: 9 of 15 caught, analysed in F5.
- **Root integration.**
  - The decode loops over the table, never indexes it, and is registered.
  - W2: `ref_src_chg_w` gives a one-cycle unlocked presentation, and the servo goes LOCKED or ACQUIRE to HOLDOVER on `!ref_locked_i`, then to ACQUIRE with `win_skip` 2 and the lock count cleared.
  - Restart request: the CRF terms, plus the meter's `disrupt_p` and `mr_toggle_p`, with no other gate.
  - C1 level: `~tu & (~follow_sel | servo LOCKED)`. The servo cannot be pruned with a stream source; the builder refuses that.
  - A2-a: `mga_sel_w = int | follow`, which also drives the NCO.
  - CSR 0x8E0 and 0x8E4 each have a read-window term, and their fields match REGISTER_MAP.
  - No processor-boundary port change and no protocol-processor edit: the diff touches no gitlink.
  - The `clkv_double.sv` substitution is confined to the `milan_dp_mclk` Makefile.
- **The eight accepted deviations** are each implemented as ruled:
  - VERSION is 0x0060 in the CSR, with an Unreleased entry in the changelog;
  - builder gate 33;
  - `[CLKSRC-WALK]` grades all four observables for every index;
  - the root loss leg is 3 s, and the meter suite's S2 loss leg is 60 s with its mutant caught;
  - the test double is test-only;
  - one recentre per switch type over 0.8 s gaps;
  - the servo-with-meter row is in the meter suite;
  - 636 FF.
- **Changed pre-existing tests are consequences, not weakenings.**
  - Check-site counts did not fall in any changed harness.
  - INTERNAL free-run pins became A2-a pins: zero junction slips, aligner engaged, no walk at the plan rate.
  - T67 holds the 1:1 audio clock so the aligner's watchdog restores the NCO's own rate.
  - `[CLKSRC-RANGE]` drops NSTREAMS + 1, which is now a listed index.
  - The gmstep anchors moved with the request expression.
  - The render INTERNAL-select leg defect is now graded at the resolve, because the walk test can no longer tell the two apart.
- **Area and timing.**
  - Re-measured: meter 574 LUT (558 logic + 16 LUTRAM), 636 FF, 102 CARRY4, 0 RAMB, 0 DSP (`receipts/ooc_meter_direct.txt`).
  - The image built at `dfa8f360` is the head's image: nothing under `hdl`, `sw/litex`, `syn`, `configs`, `avdecc`, `sw/builder` (except `test_builder.py`) or the submodules changed after it.
  - WNS +0.107 ns, WHS +0.014 ns, LUT 80.58 %, slice 99.98 % are from the published evidence; I did not rebuild them.
- **Clauses.**
  - Milan v1.2 5.3.3.6 is read as a minimum. IEEE 1722.1-2021 7.2.9.2 permits the location, and 7.2.32 allows up to 216 sources with no order rule.
  - BAD_ARGUMENTS for an unlisted index is credited to 7.2.32 and Table 7-141, with 7.4.23.1 for the carried current index.
  - Holdover with no fallback is consistent with Milan v1.2 5.4.2.15 and 5.3.11.1.
  - 1722-2016 4.4.4.3: a source-change toggle held for 8 PDUs (`KL_media_clock_restart` unchanged), and only the followed stream's `mr` echoed.
  - 4.4.4.6 sequence wrap; 4.4.4.7: `tu` as an edge restart only.
  - Milan v1.2 7.4: the owner's oscillator risk is recorded in the compliance matrix, TIME_SYNC, the design Limits and the CHANGELOG.
- **Lint and static gates.** `lint_rtl.py --check` PASS (90 <= 90). 20 of the 24 hosted-skipped `docs-check` commands pass locally (`receipts/docs_check_steps_30_51.txt`). The failing ones are F3's two ratchets, and `gen_toc` could not run here (environment; see Limits).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F4, F7) | #629 acceptance and rulings; FR_NFR FR-CLK-03/04; the generated shape headers and AEM model (`check_entity_shape.py` 166/0); `KL_aaf_clock_meter.sv` against the design and IEEE 1722-2016 Fig. 26, Tables 9 and 11, 4.4.4.3/.5/.6/.7, 10.8; IEEE 1722.1-2021 7.2.9, 7.2.32, Table 7-16; Milan v1.2 5.3.3.6, 5.4.2.15, 7.4; hosted check runs | R432-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| RTL | UNCLEAN (F3) | `hdl/ieee1722/crf/KL_aaf_clock_meter.sv` (all 597 lines); `hdl/milan/milan_datapath.sv` diff (decode, reference mux, W2, request, C1, A2-a, settle); `KL_mmcm_drp_servo.sv` diff; `milan_csr.sv` diff; `KL_media_grid_align.sv`/`KL_media_nco.sv` (comments only); lint, naming and port-doc gates; OOC area | R432-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Robustness | UNCLEAN (F1, F5) | meter format, loss, wrap, timeout, bind, STOPPED, enable and era paths; reviewer probes; saved-state census growth (`check_nvm_capture.py`) | R432-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Tests | UNCLEAN (F1, F2, F4, F5, F6) | `tb/verilator/aaf_clock_meter` (re-run, 26 mutants re-run in parallel); `tb/verilator/milan_dp_mclk` (re-run with its 14 mutants; hosted failure analysed); reviewer probes at meter and root; diffs of `milan_dp` (`sim_aclk`, `sim_main`, `sim_nxn`, gmstep), `milan_dp_render`, `mmcm_servo`, `crf_rx`, `csr`, `test_builder.py` | R432-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Docs | UNCLEAN (F3, F6, F7) | design page diff and Implementation notes; FR_NFR; CHANGELOG; REGISTER_MAP 0x8E0; compliance matrix; PP_DESCRIPTOR_OWNERSHIP L6; feature ledger; TESTING; TIME_SYNC; milan_dp and milan_dp_mclk READMEs; PR body; public evidence `f7cb2d68` | R432-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |

## Real limits of this review

- **Not run:** physical calibration, the bench, hardware, Vivado (timing and area of the image are taken from the published evidence), the full suite sweep, the full builder bank, Yosys portability, the gPTP and processor banks, Docker/act, `act_ci.py` and its self-test.
- `syn/yosys/ooc.sh` refused in my scratch export, which has no superproject gitlink (`receipts/ooc_aaf_clock_meter.txt`). I reproduced its per-top recipe directly (`sv2v` then `synth_xilinx -family xc7 -flatten`) with Yosys 0.66.
- `gen_toc.py --check/--verify-anchors` could not run: the pinned Markdown renderer is not installed here. The docs-wording gates were likewise not run by me.
- The hosted-runner failure in F2 is diagnosed from the hosted log and reproduced by setting `MAKEFLAGS=w`. I did not run GNU make 4.3 itself.
- The root reviewer probe ran the `--switch` mode and leg B only.

## Pending manager duties

- **Hosted acceptance.** At 06:48Z, `docs-check` was failure (F1, with steps 30 to 51 skipped) and Verilator shard 2/5 was failure (F2). Shards 1/5 and 4/5 were still in progress. "Physical gPTP" was skipped (not executed).
- **Processor ordering.** The ruling 5935520588 says protocol-processor #141 "lands before, or with, the parent change", and the design adds a submodule pin bump. #141 and its PR #142 are OPEN (`receipts/pp141_state.txt`), and this head moves no gitlink. That is a merge precondition.
- **Merge and bench.** The final current-dev candidate build and validation. The bench lane: following AAF and CRF, a switch, lock loss, A2 at INTERNAL, and INTERNAL accuracy as an observation. Carry R1 to R4 to the residue checklist.

R432-1 FINISHED
