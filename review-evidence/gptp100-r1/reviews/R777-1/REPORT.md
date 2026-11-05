[R777] POSITIVE - exact head 3e3f0418ad081e5906d02d872614fe3a81e148e5

# R777-1 independent review: Mister-M-alt/FPGA-gPTP PR #101 (issue #100)

- Exact head `3e3f0418ad081e5906d02d872614fe3a81e148e5`, tree `1b7c2e558ce0597caa07af63e00200b76a09109d`.
- Diff reviewed: `3e3a4e7695ce66eed609089f280c2fba45b24d36..3e3f0418ad081e5906d02d872614fe3a81e148e5`, nine commits, 19 files.
- Inputs, in order: repository README and docs map (this repository has no AGENTS.md or CONTRIBUTING.md); the issue #100 body with its 2026-11-05 maintainer decisions and acceptance list; the PR body; the clause text of IEEE 802.1AS-2011 (10.2.3, 10.2.8.2.1, 10.2.9 / Figure 10-6, 10.3.9.1, 10.5.2.2.11, 10.6.3.2, 11.2.15.3 / Figure 11-8, 11.4.4.3, 11.5.3, 8.6.2.3, Annex B.1.1, B.1.2 and B.2.3, Annex D), IEEE 1588-2008 7.6.2.5 Table 6, and Milan v1.2 4.2.6.1.1 and 4.2.6.2.2 to 4.2.6.2.6; then the diff and history; then the public evidence at `kebag-logic/milan-fpga@d64b2aae163c496c2fbb445b14ff6c2d6a6c9eea` `review-evidence/gptp100-r1`; then the parent `dev` at `604899c08ff1cd1830e1dd08b733109ef852400c` (public sparse checkout) for item 6.
- Prior public review findings on this PR were checked only after this verdict and ledger were written (see "Prior public findings").

## Verdict

POSITIVE. All five lenses are clean. There are no BLOCKER, MAJOR or MINOR findings. Five SUGGESTIONs and two RESIDUE items are recorded below. None of them changes a measurement, figure, verdict, test outcome or clause claim of this head.

The reviewer's own runs at the exact head (pinned Verilator 5.050) are:
- the engine suite: 2,098 checks in each of the three shipping passes and 61 in the fourth, 0 FAIL;
- the full engine mutation arm: 160 of 160, with all 24 #100 controls caught by name;
- every other repository gate: rc 0;
- a 16,208-vector extremes probe of the TLV frequency datapath: 0 FAIL;
- a boundary probe of the aging-at-the-instant reading: 2,108 checks, 0 FAIL.

## Findings

### S1 - SUGGESTION - Tests
- **Artifact**: `tb/verilator/engine/sim_main.cpp:7654` and `:7670` (`grade_the_tlv_of_this_mastership`).
- **Authority**: 802.1AS-2011 11.4.4.3.9 ("truncated to the next smaller signed integer"). The PR body and the engine comment at `hdl/top/KL_gptp_engine.sv:942` say "floored".
- **Evidence**: the grade accepts `|freq - want| <= 1 + |units|/2^17`. That is ±1 LSB for the settled case, whose value is −791,675. A disposable mutant that truncates toward zero instead (`32'(tlv_prod_w / 64'sd65536)`) SURVIVED the full harness (`receipts/runs/extra.log`). The RTL itself floors correctly at both signs: `receipts/tlv_mul_probe.log` shows RTL == floor(dlt × TLV_K_C / 2^16) on all 16,208 vectors at 2, 100, 125 and 250 MHz.
- **Impact**: none at this head. A future 1 LSB (2^-41) floor regression would go undetected.
- **Suggested outcome**: grade the field exactly, against floor(units × TLV_K_C / 2^16) with the 2 MHz TLV_K_C 17,179,869. Optionally add the truncation mutant and one positive-change case.
- **Verification**: rerun the arm with the added control and confirm it is caught by name.

### S2 - SUGGESTION - RTL, Robustness
- **Artifact**: `hdl/top/KL_gptp_engine.sv:945-946` and `:962`.
- **Evidence**: `TLV_K_C = round(CLK_HZ_P × 2^33 / 1e9)` is multiplied as `{1'b0, TLV_K_C[31:0]}`. For `CLK_HZ_P` ≥ 500 MHz, TLV_K_C ≥ 2^32 and the truncation silently zeroes or corrupts scaledLastGmFreqChange. No elaboration check guards it, and `docs/INTEGRATION.md:900` only says to set `CLK_HZ_P` to the actual frequency.
- **Impact**: unreachable on the target. Timing closes at 10 ns with +2.043 ns, and every parent configuration runs at or below 125 MHz. The case is latent only.
- **Suggested outcome**: use `{1'b0, TLV_K_C[32:0]}` with a widened product, or add an elaboration-time assertion on `CLK_HZ_P`.
- **Verification**: lint, plus the multiply probe (`scripts/tlv_mul_probe.py`) at 500 MHz.

### S3 - SUGGESTION - RTL, Robustness, Tests
- **Artifact**: `hdl/top/KL_gptp_engine.sv:492` (`ANN_RTO_MS_C = 3000`) against `hdl/ucode/gen_gptp_ucode.py:1925-1928` (BTCA's `MOVE ... imm=3000`).
- **Evidence**: the engine replaces any nonzero slot-2 arm from an Announce handler with `ANN_RTO_MS_C × 2^logMessageInterval`. The generator's literal therefore only matters for being nonzero. Nothing checks that the two values agree, and the generator comment "scales this arm" reads as if the literal were used.
- **Impact**: none today. A later edit of either literal would diverge silently.
- **Suggested outcome**: one cross-check, for example in the contract check or the engine suite, that BTCA's arm equals `ANN_RTO_MS_C`. Alternatively, a comment at the generator literal stating that the engine substitutes its own constant.
- **Verification**: the gate fails when either literal is mutated.

### S4 - SUGGESTION - Docs (code hygiene)
- **Artifact**: `hdl/ucode/gen_gptp_ucode.py:553` (`CLOCK_ACCURACY_UNKNOWN_C = 0xFE`).
- **Evidence**: the constant is defined and never referenced anywhere in the repository.
- **Suggested outcome**: use it, for example in the `--clock-accuracy` help text, or drop it.
- **Verification**: grep.

### S5 - SUGGESTION - Conformance, Docs (parent-side; pending manager decision)
- **Artifact**: parent `sw/builder/endstation_builder.py` at `604899c0`, lines 3561-3563, 4150-4170 and 5935-5939, with the companion patch.
- **Evidence**:
  - The parent builder derives AVB_INTERFACE clockAccuracy by parsing `CQ_C` from the pinned generator.
  - It refuses any config whose `gptp.clock_accuracy` differs from that value.
  - It invokes the generator with only `--mac`, `--p1` and `--clk-hz`.
- **Consequence**: with this gitlink every parent build announces 0x22, including the Arty configurations whose model-id hashes the companion patch re-pins. No parent build can select the 0xFE that issue #100 item 5 keeps available "for a build with no characterised oscillator" (8.6.2.3 b). This is consistent and correct for the boards the maintainers characterised. Whether every parent board, the Arty bench boards included, is covered by that decision is not established by any evidence here, and physical calibration is NOT RUN (parent #64 and #488 are open).
- **Suggested outcome**: the manager confirms that the 0x22 decision covers every parent configuration. If any is not characterised, a parent follow-up passes `gptp.clock_accuracy` to `--clock-accuracy` and relaxes the pin for that field. Optionally, `docs/MANAGER.md` open risks notes that the 0x22 claim rests on the maintainer decision while the physical calibration risks stay open.
- **Verification**: the parent builder test with a 0xFE config.

### R1 - RESIDUE - Docs
- **Artifact**: `docs/HDL_DEVELOPER.md:320`: "Region 6 serves all three fields as ScaledNs and scaled."
- **Exact fix**: "Region 6 serves gmTimeBaseIndicator, lastGmPhaseChange as ScaledNs and scaledLastGmFreqChange scaled by 2^41."
- This is wording only.

### R2 - RESIDUE - Docs (parent companion)
- **Artifact**: parent `sw/builder/endstation_builder.py:3561` comment, `:4153` comment and `:4165-4168` message.
- **Problem**: they state the engine generator "consumes only" priority1, MAC and clock frequency, and "announces this field from a constant". From this gitlink on, the generator also accepts `--clock-accuracy`; the builder simply does not pass it.
- **Exact fix**: in each place, add "(the generator's `--clock-accuracy`, FPGA-gPTP #100, is not passed by this builder, so clockAccuracy is `CQ_C`'s octet)".
- This is wording only. Builder behaviour is consistent: the parsed `CQ_C` equals the image.

## Clause checks against the focus items

### 1. Follow_Up information TLV (802.1AS-2011 10.2.8.2.1 i) to l), 10.2.9 / Figure 10-6, 11.4.4.3.6 to 11.4.4.3.9)

**Layout.** Region 6 serves {tbi, phase[95:48]}, {phase[47:0], freq[31:16]} and freq[15:0]. `prog_leg_syncfu` emits them as Q, Q and W after a zero cumulativeScaledRateOffset (D). That is 4 + 2 + 12 + 4 octets, matching Table 11-10. A grandmaster's rateRatio is 1.0, so the zero is correct under 10.2.8.2.1 i) and 11.4.4.3.6.

**gmTimeBaseIndicator.** It increments on BECOME's PHC word-3 write. That is the only `RG_PHC | 3` write in the generator (`gen_gptp_ucode.py:1990`), once per mastership. It wraps as UInteger16.

**lastGmPhaseChange.** It is the last offset written to publish word 4 as a slave, `RA = local - master` (`gen_gptp_ucode.py:1052-1055`), sign-extended to 80 bits and shifted by 16 as ScaledNs. That equals Figure 10-6's `sourceTime - syncReceiptTime`, and 11.4.4.3.8's "current grandmaster minus previous grandmaster" with this plane as the new grandmaster. Disposable mutants confirm the sign extension and high word are load-bearing (caught).

**scaledLastGmFreqChange.**
- Inputs: `phc_addend_o` is the applied trim, `-(P+I)`, saturated to ±ilim (`gen_gptp_ucode.py:1132-1139`). BECOME's word 3 is `-I`.
- Value: dlt = `-P`, or 0 when the slew applies word 3, or 0 when no rate has been written since reset. The sign is (kept − estimate), which is new relative to old as 11.4.4.3.9 requires.
- Width: the generator asserts `2*ilim + 1 < 2^24` (`:662`), so dlt fits 25 bits signed at any clock.
- Extremes probe (`scripts/tlv_mul_probe.py`): the RTL lines are lifted verbatim and refused if absent; the corners ±ilim × ±ilim, ±1 and 0 are driven along with 4,000 random pairs, at 2, 100, 125 and 250 MHz.
  - RTL equals floor(dlt × TLV_K_C / 2^16) on every vector, with correct sign and no overflow.
  - The maximum |value| is 879,624,192, below 2^31.
  - The deviation from the exact 2^41 value is 1 LSB at 100 MHz and 0 at 125 and 250 MHz. At the 2 MHz simulation clock it is 10 LSB, which is TLV_K_C rounding: about 4.5e-12 fractional, against B.2.4's 0.1 ppm.
- The latent ≥ 500 MHz case is S2.

**Harness.** Phase 52 grades the first mastership, a post-warm-reset mastership, a settled loss and a slewing loss, each by name. The floor-versus-truncation strength gap is S1.

### 2. Announce receipt timeout (10.3.9.1, 10.6.3.2, Figure 10-13, Milan v1.2 Table 4.2)
- **Interval source.** The interval comes from the context Announce's bank word 0 [7:0], which is logMessageInterval (`KL_gptp_rx_parser.sv:74`). That word is written at octet 33, before the word-8 context reservation, so the value belongs to that Announce.
- **Watch length.** `3000 << lg` for lg in 0..18, saturating at 2^19; `3000 >> -lg` down to lg = −11; 1 ms below that.
- **Anchoring.** The watch counts from the Announce's last octet.
- **Mirror.** The mirror's deadline uses the same `ms_now` edge as `KL_gptp_timer`'s `deadline_r` for a delta arm (`KL_gptp_timer.sv:91-93`). For an anchored arm the timer's deadline can only be later. An expiry that is no longer due is dropped at the queue head, and a dispatched expiry consumes the watch.
- **Granularity.** The early granularity is under 1 ms: aging lands 2.999 to 3.000 s after a 1 s peer's last Announce, inside Table 4.2's 2.7 to 4.5 s. The engine suite measured 5,999.74 ms for logMessageInterval 1 and 1,499.74 ms for −1 (`receipts/runs/engine-run.log`).
- **Other slot-2 arms.** The only Announce-handler slot-2 arms are BTCA `same_gm` (3000) and BECOME's stop (0, which is never anchored). BECGATE's `held` arm cannot run from an Announce handler, because the handler runs only on an asCapable port. Boot, init, BECGATE and the asCapable-fall arms keep their own delta.

### 3. The three stricter readings stay inside their clauses

**Aging at the instant.** Annex D: "The order of execution of state blocks in different state machines is undefined", and simultaneous exit conditions resolve arbitrarily. The reading is therefore permitted, and it stays inside Table 4.2.

The reviewer's boundary probe (`receipts/probe3-boundary-trials.diff`, `receipts/runs/probe3.log`: 2,108 checks, 0 FAIL) adds five trials to phase 54:
- 2.999 s apart with the last octet on the tick cycle, one clock before it, and two clocks before it: not aged;
- 3.0 s apart on the tick cycle and one clock before it: aged.

This confirms the documented claim that an Announce received before the deadline is always queued ahead of its expiry.

**Late Pdelay responses.**
- `PD_LATE_NS_C` = ⌈(15,000,000 + 2 × 800) × 1.0003⌉ + 80 = 15,006,181 ns, which is 15.006181 ms (`receipts/pd-late-bound.txt`).
- The exact multiplicative tolerance 1.0001 × 1.0002 gives the same ceiling.
- B.2.3 measures the turnaround relative to the TAI frequency. The local stamps are PHC stamps, which run at most 100 ppm (B.1.1) plus the 200 ppm whole-trim clamp off TAI. B.1.2 allows ≤ 40 ns per stamp.
- So no response whose turnaround meets Milan v1.2 4.2.6.2.6's 15 ms "shall" is ever counted lost. The unsigned 32-bit CMP (`KL_gptp_ucpu.sv:200-204`) also counts a t4 earlier than t1 as late.
- A late pair ends before any write with `S_PDGOT` clear. Figure 11-8 RESET then increments lostResponses while it is ≤ allowedLostResponses (3, 11.5.3). The fifth consecutive loss clears asCapable, and the harness shows four keeping it and the fifth clearing it.
- Only the 4.2.6.2.6 "should not" is declined, by maintainer decision.
- Exchanges that span a PHC step bypass PDPAIR through PDEPOCH, so a servo step is never counted late.

**clockAccuracy.** `CQ_C = 0xF822436A`. Per IEEE 1588-2008 Table 6, 0x22 means "accurate to within 250 ns". `--clock-accuracy` replaces only bits 23:16, and both the BMCA vector and the Announce body read `RUNTIME["cq"]`. The fourth pass's 0xFE image is graded by name. The parent-side reachability is S5.

### 4. Harness rows and the mutation arm
- Every acceptance row has named checks and planted controls. All 24 #100 controls were caught through every check they name, in the reviewer's run of the arm's own `run_mutant` (`receipts/runs/arm.log`, `160 checks: 160 PASS, 0 FAIL`).
- The published author arm receipt at this head also tallies 160 of 160.
- The reviewer's three disposable extra mutants:
  - zero-extended difference: caught;
  - unextended phase sign: caught;
  - truncation toward zero: survived. This is S1.

### 5. Area figures
Re-extracted from the published `ooc-3e3a4e7` and `ooc-3e3f041` Vivado 2026.1 reports (`receipts/ooc-reextract.txt`):

| Top | Run | LUT (logic + LUTRAM) | FF | DSP | WNS | Failing endpoints |
|---|---|---:|---:|---:|---:|---:|
| Engine | base | 4,926 (4,436 + 490) | 3,459 | 4 | +2.249 ns | 0 of 12,006 |
| Engine | head | 5,425 (4,935 + 490) | 3,618 | 6 | +2.043 ns | 0 of 12,372 |
| µCPU | base and head | 1,643 | 733 | 4 | +1.941 ns | 0 |

- The engine delta is +499 LUT, +159 FF and +2 DSP. These figures match the PR body.
- The head reports are bound to the head by the author's `repo-gates-3e3f041` runner summary (`make ooc` rc 0).
- The reviewer did not rerun Vivado (see limits).

### 6. Parent consumer gates and the companion change
- The author's `parent-A-3e3f041` and `parent-B-3e3f041` receipts ran at parent head `94a9f186`, a local commit on dev `604899c0`. The `xvlog_gate` log (`parent-A .../11.log:3`) binds the superproject gitlink to `gptp-processor@3e3f0418`. All gates are rc 0:
  - gptp_shadow: 325 checks;
  - milan_dp `gptp`: 210 checks;
  - milan_dp `gptp-lat`: 210 checks;
  - milan_dp_gptp: rc 0 after 6,107 s;
  - gptp_plane, gptp_txts, gptp_tables and milan_dp_gm_steps: rc 0;
  - the idiom, xvlog, source-list, port, naming, evidence, docs and lint gates: rc 0;
  - test_builder: rc 0, with gate 11 NOT RUN (it needs a LiteX place report);
  - `tsn_fuzz ptp`: its field campaign was skipped, which is not a pass of that campaign.
- The companion patch changes:
  - two board configs;
  - the built-in AEM gptp spec;
  - two model-id hash pins in test_builder.
- That is the minimum the builder's derive-and-refuse rule requires, because AVB_INTERFACE clock_accuracy is descriptor content (IEEE 1722.1 6.2.2.8). No parent harness needs a change: every parent peer announces priority1 ≤ 100 or 255 against the engine's 248, so priority1 decides BMCA before clockAccuracy, and the old peer clockQuality 0xF8FE436A never decides a contest.
- Parent-only observations are S5 and R2.

## Lens results

- **Conformance - CLEAN.** Covered by items 1 to 3 above, with each claim checked against the clause text. Every cited clause number was verified: 11.5.3 allowedLostResponses is 3; 10.5.2.2.11; 1588-2008 7.6.2.5 Table 6 gives 0x22 as 250 ns; Annex D ordering. S5 is advisory.
- **RTL - CLEAN.**
  - `KL_gptp_engine.sv` #100 blocks: `ann_watch`, `ann_arrival`, queue-head stale-drop and force, dispatch exclusivity, `tlv_become` and the region-6 mux.
  - Exclusivity: force needs an Announce at the head, `pdreq_block_w` a PDREQ at the head, and txts and pe have their own guards.
  - Timer and mirror deadline equality was checked against `KL_gptp_timer.sv`. `e_hdr` emits the same octets, by inspection and by the tsngen independent decode (288 checks).
  - In PDPAIR, `RW` holds turn while nrr uses `RA`, `RB` and `RD_` = t4.
  - Lint and every build are free of warnings. S2 and S3 are advisory.
- **Robustness - CLEAN.**
  - Warm reset: the mirror and arrival registers reset, tbi deliberately has no reset, and phase and frequency read zero when unknown.
  - Wrap-safe 32-bit millisecond compares.
  - Saturating interval clamp.
  - A stalled transmitter holding an Announce past its deadline still refreshes the watch (named check, and the stale-expiry controls are caught).
  - A step-spanning Pdelay goes through PDEPOCH.
  - The extremes probe passes.
- **Tests - CLEAN.**
  - Exact-head engine suite: 2,098 × 3 + 61, 0 FAIL.
  - Full arm: 160 of 160.
  - ucpu 768; parser 378 + 16; gaskets 81 + 5; tsngen 288 + 4; bench PASS; contract PASS.
  - Probes as above. S1 is advisory.
- **Docs - CLEAN.**
  - INTEGRATION (watch, late response, TLV, `--clock-accuracy` and the constants rows), HDL guide (region 6, watch, TLV), MANAGER ROM budget (1,015 and 1,016 of 1,024; `FUTO@509`) and TEST guide bullets match the code.
  - SOURCE_EVIDENCE anchors pass (`source evidence: 20 exact, 0 findings`).
  - The synthesis table is dated (`5dce647a`) and `MANAGER.md:49` says later RTL has landed, which is the existing convention.
  - Comment rule: no lane labels, lane names, review rounds, reviewer IDs or comment IDs appear among the added source lines.
  - The `scripts/check_docs*.py` blobs are byte-identical to main `5184fb3` (PR #99).
  - `git merge-tree` against `5184fb3` conflicts only in `docs/SOURCE_EVIDENCE.md` (`receipts/merge-tree.txt`), as the PR states.
  - R1 is residue.

## Executed evidence (reviewer, this head, pinned Verilator 5.050)

| Run | Result | Receipt |
|---|---|---|
| `make contract` | PASS, rc 0 | `receipts/runs/contract.log` |
| `make -C tb/verilator/ucpu` | 768 checks, 0 FAIL | `receipts/runs/ucpu.log` |
| `make -C tb/verilator/parser` | 378 checks + arm 16, 0 FAIL | `receipts/runs/parser.log` |
| `make -C tb/verilator/engine run` | 2,098 / 2,098 / 2,098 / 61, 0 FAIL | `receipts/runs/engine-run.log` |
| Engine mutation arm (`mutants.run_mutant`, 12 at a time) | 160 checks: 160 PASS, 0 FAIL; 24 of 24 #100 controls caught by name | `receipts/runs/arm.log`, `scripts/run_engine_arm_parallel.py` |
| `make -C tb/verilator/gaskets` | 81 + arm 5, 0 FAIL | `receipts/runs/gaskets.log` |
| `make -C tb/tsngen` | 288 + arm 4, 0 FAIL | `receipts/runs/tsngen.log` |
| `make -C bench/arty test` | PASS | `receipts/runs/bench.log` |
| `make lint` | rc 0, no warnings | `receipts/runs/lint.log` |
| `make docs`, `make diagrams-check` | PASS (127 selftest arms, 20 exact evidence rows) | `receipts/runs/docs.log`, `receipts/runs/diagrams.log` |
| TLV multiply extremes probe | 16,208 vectors, 0 FAIL | `receipts/tlv_mul_probe.log`, `scripts/tlv_mul_probe.py` |
| Extra disposable mutants | 2 caught, 1 survived (S1) | `receipts/runs/extra.log`, `scripts/probe_extra_mutants.py` |
| Aging-boundary harness probe | 2,108 checks, 0 FAIL | `receipts/runs/probe3.log`, `receipts/probe3-boundary-trials.diff` |
| Trial merge with main `5184fb3` | conflict only in `docs/SOURCE_EVIDENCE.md` | `receipts/merge-tree.txt` |
| Clone integrity after probes | exact head and tree; clean; 115 blobs rehash; 0 gitlinks | `receipts/verify-clone.txt` |

- The runs above executed in disposable `git archive` copies of the exact head.
- The `receipts/runs/index.md` seconds column is not valid for `engine-run`, `arm` and `extra`: their start stamps were overwritten by a duplicate launch that was stopped and discarded before it produced results. The original runs' logs and rc files are the receipts.
- Heavy concurrent load from unrelated work on the host lengthened wall times. It did not affect verdicts.

## Prior public findings

This was checked after the verdict and ledger above were written. PR #101 has:
- no review submissions;
- no inline review comments;
- issue comments that are only the manager's two review-start notices (this review, and a second independent review whose report is not published).

Issue #100 has only the author's taken and review-ready notices. There is no prior public finding to resolve or retain at this head.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #100 decisions; 802.1AS-2011 10.2.8.2.1, 10.2.9, 10.3.9.1, 10.6.3.2, 11.2.15.3, 11.4.4.3, 11.5.3, 8.6.2.3, B.1.1, B.1.2, B.2.3, Annex D; 1588-2008 7.6.2.5; Milan v1.2 4.2.6.x; `gen_gptp_ucode.py`; `KL_gptp_engine.sv`; parent builder (S5) | R777-1 | 3e3f0418ad081e5906d02d872614fe3a81e148e5 |
| RTL | CLEAN | `KL_gptp_engine.sv` #100 blocks, `KL_gptp_timer.sv`, `KL_gptp_ucpu.sv` compare, `KL_gptp_rx_parser.sv` bank map, ROM images, lint, extremes probe | R777-1 | 3e3f0418ad081e5906d02d872614fe3a81e148e5 |
| Robustness | CLEAN | warm reset, wraps, clamps, stall and stale-expiry paths, step-spanning Pdelay, boundary probe | R777-1 | 3e3f0418ad081e5906d02d872614fe3a81e148e5 |
| Tests | CLEAN | `sim_main.cpp` phases 52 to 56, `p100_mutants.py`, `mutants.py`, Makefile fourth pass, tsngen expectation; full suite and arm runs; extra mutants | R777-1 | 3e3f0418ad081e5906d02d872614fe3a81e148e5 |
| Docs | CLEAN | README, docs map, INTEGRATION, HDL_DEVELOPER, MANAGER, TEST_DEVELOPER, SOURCE_EVIDENCE, `check_source_evidence.py`, source comments (comment rule), PR body, merge note | R777-1 | 3e3f0418ad081e5906d02d872614fe3a81e148e5 |

Open: S1 to S5 (SUGGESTION) and R1 and R2 (RESIDUE, carried to the residue checklist). None leaves a lens unclean.

## Real limits
- No manager source bank ran at this head, and none is claimed. Source-head execution evidence here is the reviewer's own runs above plus the author's published receipts.
- Vivado OOC was not rerun. The area and timing figures are checked against the published reports only.
- The parent consumer gates were not rerun. The parent `94a9f186` commit is local and unpublished, so its gitlink binding rests on the author's `xvlog_gate` receipt line.
- `tsn_fuzz ptp`'s field campaign was skipped in the author's run (no packet generator), and builder gate 11 was NOT RUN. Neither is a pass.
- Physical calibration is NOT RUN, and nothing here is hardware proof. In particular, the 0x22 "within 250 ns" claim rests on the maintainer decision (S5).
- Hosted and act acceptance were not inspected or claimed. The manager owns them.

## Pending manager duties
- At the merge turn, build and validate the current-dev merge candidate (source base `3e3a4e7`, live dev `604899c0`) with the builder and native banks, and link the receipts on the PR.
- Apply the recorded `docs/SOURCE_EVIDENCE.md` resolution against main `5184fb3` (keep this branch's file and take main's two parser anchors), then run `check_source_evidence.py`.
- Apply the companion parent change with the gitlink, and decide S5: does the 0x22 default cover every parent configuration, including Arty?
- Carry R1 and R2 to the residue checklist.
- Own hosted and act acceptance, and the second independent review.

## Receipts
- Every publishable file is listed in `MANIFEST.sha256`, with paths relative to the packet.
- Host paths in the logs are replaced by placeholders.
- Disposable trees under `scratch/` are not published.

R777-1 FINISHED
