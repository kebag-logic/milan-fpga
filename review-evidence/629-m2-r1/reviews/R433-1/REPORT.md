[R433] NEGATIVE - exact head 57f4b742b504f5e69293aaa3e00d0470aa9b6071

# [R433] Round R433-1: external review of PR #634 (issue #629, lane M2)

- Exact head: `57f4b742b504f5e69293aaa3e00d0470aa9b6071`, tree `499d64f0750f3bc3caf699ee754428dbdeea6e07`, 17 commits on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`.
- Reviewer role: cleared-context external independent reviewer. Round start: https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5946504629.
- Verdict: **NEGATIVE**. One MAJOR and three MINOR findings are open. Three RESIDUE items and two SUGGESTIONs are recorded.
- Verdict and ledger were written after an independent pass and before any prior review report was read. The prior-findings section was added after them.

## Contents

- [Scope reconstructed](#scope-reconstructed)
- [Findings](#findings)
- [Residue](#residue)
- [Suggestions](#suggestions)
- [Per-lens results](#per-lens-results)
- [Ledger](#ledger)
- [Prior public review findings](#prior-public-review-findings)
- [Real limits](#real-limits)
- [Pending manager duties](#pending-manager-duties)
- [Clone integrity](#clone-integrity)
- [Receipts](#receipts)

## Scope reconstructed

Read in order: AGENTS.md, the issue #629 body, the lane M2 assignment (#629 comment 5942692103), the rulings (5935520588, 5937449258), the owner decisions (5937643550 D4 = A2-a; 5937848189 the oscillator-grade known risk), the author's STOP (5946475441) and the manager's ruling accepting the eight named deviations (5946491571), `docs/design/MEDIA_CLOCK_FOLLOWING.md` at the head, then `git diff cdf49d1a..57f4b742` and its history, then the public evidence tree `review-evidence/629-m2-r1` at `f7cb2d68` (MANIFEST.json, author/PR-BODY.md, author/HANDOFF.md) and the exact-head hosted check runs.

The eight accepted deviations were taken as ruled and not re-litigated. They are: VERSION kept at `0x0002_0060`; listener-only ordering graded on the builder function; the AECP walk's servo check; the 3 s root loss leg with the 60 s run in the meter suite; the `KL_ptp_clock_validity` test double; per-switch-type recentre; the servo-with-meter row in the meter suite; the meter's 636 FF.

## Findings

### R433-1-F1 - MINOR - Tests, Conformance - the design-named "tu from the tv net" mutant is planted nowhere, and the root never drives an AAF `tu` edge

- **Where:** `hdl/milan/milan_datapath.sv:5689` (`.tu_i (avtprx_tu_bit)`, the only wiring of the meter's `tu`); `tb/verilator/aaf_clock_meter/mutants.py` (26 entries, none for it); `tb/verilator/aaf_clock_meter/sim_main.cpp:491-492`, whose comment claims the mutant; `tb/verilator/milan_dp_mclk/sim_mclk.cpp:369`, where every AAF frame has `tu` clear.
- **Authority:** the design's test plan (`docs/design/MEDIA_CLOCK_FOLLOWING.md`, Simulation, the "History restarts" row) names two failing mutants. The second is: "`tu` taken from the `tv` net (the CRF wiring): the `tu` case fails". The design's input table also calls this out as the trap to avoid. Lane M2's assignment item 4 requires "every row of the design's test plan, each shown failing under its named mutant". This mutant is not among the eight accepted deviations. The public evidence (author/HANDOFF.md, "Test rows", M7) lists "tu from the tv net" as a graded mutant, and the PR body says "every meter row".
- **Evidence:** the reviewer planted exactly that mutant at the root (`scripts/plant_tu_from_tv.sh`, one edit, `.tu_i (avtprx_tv_bit)`). The mutated build was confirmed elaborated. The root suite's three clean legs then all pass: leg A 50/50, leg B 44/44, leg C 32/32 (`receipts/mut_tu_from_tv_leg{A,B,C}.log`). The meter suite cannot express the mutant, because the meter takes `tu` as a port. No other suite references `avtprx_tu_bit`.
- **Impact:** a regression to the CRF-style wiring would go unseen. The meter would then see `tu` stuck at 1 (only `tv`-set PDUs are consumed), so it would never restart its history on a followed talker's IEEE 1722-2016 4.4.4.7 `tu` edge. One acceptance item is unmet, and the published evidence over-claims it.
- **Required outcome:** a check that fails under this mutant. One option is a root leg that drives a `tu` edge on the followed AAF stream and observes the meter's restart (for example `AAFM_STAT[15:8]` and `[1]`), with the mutant added to the root campaign. Alternatively, record a ruled deviation. The harness comment and the evidence must match what is graded.
- **Verification:** `scripts/plant_tu_from_tv.sh` (or the campaign's new id) must make the named check fail. The clean legs must still pass.

### R433-1-F2 - MAJOR - Tests, Docs, Robustness, Conformance - the PR turns a hosted gate red: the NVM capture census changed and the capture measurement was not re-taken

- **Where:** `scripts/check_nvm_capture.py`, run by `.github/workflows/docs.yml:224` (job `docs-check`, step "Capture measurement census and clock gate"). The capture receipt under `tb/verilator/nvm_capture_cpu` is unchanged. `tb/verilator/nvm_backend/records_endstation_ax7101_8x8.txt` and `records_endstation_ax7101_1x1_tdm8.txt` do change.
- **Evidence:** the hosted `docs-check` concluded **failure** at the exact head (run 36971935308; `receipts/hosted_docs_check_failed_step.log`, `receipts/hosted_checks_57f4b742.txt`). The output is "FAIL: capture inputs changed; remeasure both arms": 8x8 now has 164 records and 13,210 raw bytes against a receipt measured for 156 and 12,634, and 1x1 TDM8 has 54 and 3,290 against 53 and 3,218. The reviewer reproduced it locally: rc 1 at the head (`receipts/check_nvm_capture_head.log`), and rc 0 at the base `cdf49d1a`, "PASS: capture census, clocks, both timing arms and receipt agree" (`receipts/check_nvm_capture_base.log`). The extra records are the new CLOCK_SOURCE descriptors' NAME records (8x8 NAME 99-106; 1x1 NAME 38).
- **Impact:** a repository gate on the PR head is red, so the completion bar (AGENTS.md section 7: required gates pass; acceptance "Gates: ... the docs gates") is not met. The STOP comment's "the docs gates ... all exit 0" did not include this gate. Also, the saved-state capture timing, graded against its off-time limit, is unmeasured for the larger shipping record census. That is the property the gate exists to keep honest.
- **Required outcome:** re-measure both capture arms for the new census (the gate's own instruction), update the receipt, and have `check_nvm_capture.py` and hosted `docs-check` pass at the new head. Alternatively, obtain a ruling that explicitly accepts the gate state.
- **Verification:** `python3 scripts/check_nvm_capture.py` exits 0 at the new head, and hosted `docs-check` succeeds there.

### R433-1-F3 - MINOR - Docs - FR_NFR's status row still says AAF following is "implementation in progress"

- **Where:** `docs/reference/FR_NFR.md:156`, status cell "AAF following required by the #629 owner decision, implementation in progress". The same file's ledger table at `:135` (`aaf.media-clock-following` `implemented`), `docs/reference/milan_feature_status.json` and the design page's status ("Implemented by lane M2") all say implemented at this head.
- **Authority:** AGENTS.md section 6 (Docs: changed contracts are reflected in authoritative docs). The row is the requirement register's status verdict, so this is not purely wording.
- **Impact:** the authoritative requirement register contradicts itself on FR-CLK-03/04's status.
- **Required outcome:** the status cell states the head's state, for example "implemented and graded in simulation (#629, PR #634); bench acceptance open", consistent with the ledger.
- **Verification:** reading `FR_NFR.md:156` against `:135` and `milan_feature_status.json`.

### R433-1-F4 - MINOR - Docs - REGISTER_MAP still says `0x8E0` to `0x8F4` are unmapped and read zero

- **Where:** `docs/reference/REGISTER_MAP.md:1837`, "`0x8E0` to `0x8F4` remain unmapped and read zero". This contradicts `:2056-2072` (`AAFM_STAT` 0x8E0, `AAFM_RATE` 0x8E4, RO live) and `hdl/common/csr/milan_csr.sv` (`A_AAFM_STAT`/`A_AAFM_RATE` and their read-window terms).
- **Authority:** the design's change list (`MEDIA_CLOCK_FOLLOWING.md:1246`) names this exact sentence (`REGISTER_MAP.md:1833` at the design base) as the place the two words land.
- **Impact:** the register map states a wrong read behaviour for two live words, and a reader of the 0x8C8 section is told they read zero.
- **Required outcome:** the sentence names the new pair and the remaining unmapped range (`0x8E8` to `0x8F4`).
- **Verification:** reading the two sections against `milan_csr.sv`. The CSR bench already grades `0x8E8` as reading zero.

## Residue

These are purely wording defects (owner rule 2026-10-02). They do not make the verdict NEGATIVE and do not leave a lens unclean.

- **R433-1-R1** - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1463`, "Where" cell "HANDOFF area table". This names an artifact that is not in the repository. Exact fix: replace it with `[#629 STOP, item 8](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946475441)`.
- **R433-1-R2** - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1456`, "Open for a decision on #629". Exact fix: "Kept by the [ruling on #629](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946491571)".
- **R433-1-R3** - `docs/design/TIME_SYNC.md:203`, "HOLDOVER for one cycle, then ACQUIRE". Exact fix: "HOLDOVER for at least one cycle, until the new reference reads locked, then ACQUIRE".

## Suggestions

- **R433-1-S1 (RTL)** - `hdl/milan/milan_datapath.sv:6271` (`src_grid_ok_w = !follow_sel_r || ...`). Under A2-a the aligner is engaged at INTERNAL, but the #386 settle there is declared without waiting for it. After a deselect to INTERNAL, the servo's IDLE removes the trim, and the aligner absorbs that step while the recentre may already fire. The behaviour is documented (`TIME_SYNC.md`, "at INTERNAL: 2048 ticks after the change"), so this is optional: consider gating the settle on `mga_sel_w`.
- **R433-1-S2 (Tests)** - `tb/verilator/milan_dp/sim_aclk.cpp` "INTERNAL: the plan's -10.64 ppm drift is gone (more than 5 ppm from it)" and `sim_tdm8_render.cpp` T30 INTERNAL (`|walk - plan| > 4`) are one-sided. They are backed by bounded `mga_err`, RING-INT's discriminating window and T31's `|walk| < 5 ppm`. A two-sided bound near zero would be stronger.

## Per-lens results

### Conformance - UNCLEAN (F1, F2)

Checked against the issue, the assignment, the design and the clauses:

- **The AEM set on the regenerated 8x8 model** (`receipts/aem_8x8_clock_descriptors.txt`):
  - CLOCK_SOURCE 0 is INTERNAL (type 0x0000);
  - CLOCK_SOURCE 1 is CRF, INPUT_STREAM 0x0002 on STREAM_INPUT 8;
  - CLOCK_SOURCE 2-9 are INPUT_STREAM on STREAM_INPUT 0-7, in the D1 = L1 order;
  - every descriptor is 86 octets with flags 0x0002 (LOCAL_ID; IEEE 1722.1-2021 Table 7-16);
  - CLOCK_DOMAIN 0 lists 0..9 (identity list, 7.2.32) with `clock_source_index` 0.
  - Milan v1.2 5.3.3.6 (the CRF source as a minimum; INTERNAL with outputs) holds.
- **Selection and refusal:** SET_CLOCK_SOURCE membership is the processor's unchanged range check, and the protocol-processor gitlink is unchanged.
- **FR-CLK-03/04 and the #389 record** are amended to the owner decision.
- **The meter matches the design's statements**, by RTL reading and simulation: the 48 kHz Base format with `stream_data_length` = 24 x channels; the mod-16 groups and group mean; the 4,096 ns bound and void; rule (b) with the k = 2 check at 5,120 ns and the midpoint fill; E8.
- **The design's desk-model claims, re-run against the RTL** (`receipts/probe_meter.log`, 54/54 agree):
  - random loss at p = 1e-4, 1e-3 and 2e-3 over 300 s against e^(-4.096 x 500 q^2) and 500 q^2 (1 - q);
  - runs of 255, 256, 257 and 512 lost PDUs from PDU 0 and PDU 5 each restart once;
  - 1 to 33 whole lost groups restart 0 or 1 time as designed;
  - the tolerance edges (random sign +/-1,700 ns at +/-300 ppm, independent +/-1,740 ns at +/-300 ppm, +/-2,000 ns at 0 ppm) show no restart;
  - the cold-start rate is valid at PDU 32,783.
- **`mr` (IEEE 1722-2016 4.4.4.3):** a source change raises one request, the meter's timeout and the followed toggle raise one each, and an era start raises none. The root campaign grades this (`receipts/mclk_suite.log`).
- **Holdover** has no fallback, and C1 behaves as ruled.
- F1 leaves one acceptance item unmet. F2 leaves the gate acceptance unmet.

### RTL - CLEAN

Examined at the head, each against the design:

- `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:1-597`:
  - the operand widths: `grp_sum_r` 20-bit for 15 x 4,096; `grp_off_r` 21-bit for 1,875,000; modulo-2^32 picks and differences; `NOM_SPAN` 4.096e9 < 2^32;
  - the floor arithmetic of `>>>`;
  - the k decode and bounds;
  - the ring read-old/write-new and its fill guard;
  - era and lock-clear precedence, and pulse gating on `en_i`;
  - the per-PDU spacing assumption, which holds because TDATA_WIDTH 64 gives at least 8 cycles between parses against a 3-stage per-PDU and 6-stage group-end path.
- `hdl/milan/milan_datapath.sv`:
  - the `media_clk_table` loop over the generated tables;
  - `media_clk_resolve`;
  - `ref_src_chg_w`, the one-cycle W2 presentation;
  - the reference mux;
  - the `mcr_restart_p_w` terms;
  - the C1 level `~clkv_tu_w & (~follow_sel_r | mcsrv_locked_w)`;
  - A2-a's `mga_sel_w`;
  - the meter generate and its tie-offs.
- `KL_mmcm_drp_servo.sv`: the port renames and `locked_o` from `state_r` on `clk_i` = `axis_clk`, so there is no new crossing.
- `milan_csr.sv`: the two RO words and their read-window terms.
- `KL_media_grid_align.sv` and `KL_media_nco.sv`: comment-only changes.
- No top-level, SoC or processor-boundary port changed. The `protocol-processor`, `gptp-processor`, `external` and `third_party/verilog-axis` gitlinks are unchanged.
- Out-of-context area reproduced exactly: meter 574 LUT (16 LUTRAM), 636 FF, 0 RAMB, 0 DSP; servo 865 LUT, 792 FF (`receipts/ooc_meter_servo.log`).
- S1 is optional.

### Robustness - UNCLEAN (F2)

The meter's robustness paths were exercised in simulation:

- reordered pairs, duplicates and `tv`-clear PDUs restart nothing (P4);
- STOPPED, wrong-subtype, other-listener and wrong-format streams are not consumed (M4, M13);
- the 32-bit timestamp wrap and the 8-bit sequence wrap are handled (M5, M7);
- silence, unbind and rebind behave as designed (M14);
- loss within and beyond the bound behaves as designed (M8-M12, P1, P2);
- the feature-disabled shape elaborates no meter and ties its outputs to zero;
- a servo-pruned config with `input_stream` is refused.

F2: the saved-state capture timing for the grown record census is unmeasured, and its gate is red.

### Tests - UNCLEAN (F1, F2)

- **Meter suite**, re-run at the head:
  - cases 308 checks, 0 failures;
  - servo with meter 6/6, worst |e| 717 ns, LOCKED at 8.70 s, trim moved +4.013 ppm on the 4 ppm step;
  - all 26 named mutants killed by their named checks (`receipts/meter_cases.log`, `meter_servo.log`, `meter_mutants.log`).
- **Root suite**, re-run: legs A 50/50, B 44/44, C 32/32; the 14 named mutants caught; 27/27 campaign checks (`receipts/mclk_suite.log`).
- **Changed tests**, read for weakening: builder gates 33, 15, 25 and 28; render T14, T30 and T31 and the `--defect-internal-select` arm; milan_dp aclk, nxn `[AECP-MODEL]`, `[CLKSRC-WALK]`, `[CLKSRC-RANGE]` and T67, plus main and gmstep anchors; the mmcm_servo unit with U16 W2; crf_rx; the CSR bench. Each change reads as a correct consequence of D1 or A2-a, or as a port rename, with new positive and negative arms. None is a weakened oracle beyond S2.
- F1 is an unplanted named mutant. F2 is a red gate.

### Docs - UNCLEAN (F2, F3, F4)

- **Read:** FR_NFR, the compliance matrix (5.4.2.15/.16, 5.3.11.1, 7.2.2, 7.2.3, 7.4 with the KNOWN RISK, 4.4.4.3, 4.3.5/10.8), PP_DESCRIPTOR_OWNERSHIP L6, the feature ledger and JSON, REGISTER_MAP, TIME_SYNC, CHANGELOG (the release note on saved state, the KNOWN RISK, VERSION), TESTING, the design page's status and Implementation notes, and the module READMEs.
- **Oscillator-grade risk:** recorded in the compliance matrix 7.4, TIME_SYNC, CHANGELOG and the design's Limits.
- **Generated files:** all five `configs/generated/*/gen/adp_shape_defaults.svh`, `hdl/common/gen/adp_shape_defaults.svh` (via `--write-rtl`) and `avdecc/aem_rom.json` regenerate byte-identically through the builder and `gen_aem_store.py`, so there are no hand edits (`receipts/regen.log`).
- **Open:** F2 (a stale measurement receipt), F3, F4, plus residue R1 to R3.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #629 body and rulings; the design; regenerated 8x8 AEM descriptors; FR_NFR FR-CLK-03/04; meter RTL against the design statements; probe_meter 54/54; root `mr` and C1 legs | R433-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| RTL | CLEAN | `KL_aaf_clock_meter.sv:1-597`; `milan_datapath.sv` decode, mux, W2, restart, C1, A2-a and generate; `KL_mmcm_drp_servo.sv` ports and `locked_o`; `milan_csr.sv` 0x8E0/0x8E4; aligner and NCO diffs; gitlinks; OOC area | R433-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Robustness | UNCLEAN (F2) | meter M4-M14 and P1-P4 under loss, reorder, duplicate, wrap, silence, bind, STOPPED and format; the no-meter shape; servo-prune refusal; `check_nvm_capture.py` head against base | R433-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Tests | UNCLEAN (F1, F2) | aaf_clock_meter cases, servo and 26 mutants; milan_dp_mclk legs and 14 mutants; tu-from-tv probe; diffs of test_builder, render, milan_dp, mmcm_servo, crf_rx and csr; hosted docs-check | R433-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |
| Docs | UNCLEAN (F2, F3, F4) | FR_NFR, the compliance matrix, PP_DESCRIPTOR_OWNERSHIP, the feature ledger, REGISTER_MAP, TIME_SYNC, CHANGELOG, TESTING, the design page; regeneration of every tracked generated file | R433-1 | `57f4b742b504f5e69293aaa3e00d0470aa9b6071` |

## Prior public review findings

This section was read after the verdict and ledger above were written, at 06:43 UTC.

PR #634 had no prior review finding to resolve or retain:

- It had no review and no review comment.
- Its only issue comments were the two round-start notices: 5946503850 (R432-1, the internal round) and 5946504629 (this round). Neither carries a finding.
- Issue #629 had no comment after the ruling 5946491571.

Nothing above changed after this reading.

## Real limits

- **Shipping image not rebuilt.** Its timing and area (WNS +0.107 ns, WHS +0.014 ns, 0 critical warnings, #607 clean, LUT 80.58 %, slices 99.98 %) are taken from the public evidence (author/HANDOFF.md), not reproduced. Only the out-of-context meter and servo areas were reproduced.
- **Hosted contexts not owned by this round.** At 06:39 UTC, Verilator shards 1/5, 2/5 and 4/5 were still in progress, and "Physical gPTP" was skipped (not executed). The manager owns hosted and act acceptance.
- **Banks not re-run.** The full source banks were not re-run: `run_all_suites.sh`, `test_builder.py` in full, the full `milan_dp`, `milan_dp_render`, `mmcm_servo` and `csr` suites, and Yosys `run.sh`. The changed tests in those suites were reviewed by reading. The meter and root suites, the meter mutants, the root mutants, regeneration and the NVM capture gate were re-run.
- **Clause texts.** IEEE 1722-2016, IEEE 1722.1-2021 and Milan v1.2 were applied as quoted in the design and from the reviewer's reading of the cited clauses. No standards text was re-opened in this round.
- **No physical evidence.** No bench, hardware or physical calibration was run, so this round says nothing about silicon behaviour, the INTERNAL oscillator grade, or THD+N.
- **Scope of the probes.** They exercise the meter in isolation at a compressed clock. Root behaviour is covered only by the lane's root suite and the one reviewer mutant.

## Pending manager duties

- Disposition of F1 to F4: fix, or record a ruling.
- The NVM capture re-measurement (F2) and hosted `docs-check` at the new head.
- Hosted Verilator shards 1, 2 and 4 to completion; the act replica.
- The final current-dev candidate build and validation at the merge turn.
- Carrying R1 to R3 to the residue checklist.
- The later bench lane: B AAF, B CRF, the switch, lock loss, A2 at INTERNAL, and the INTERNAL accuracy observation against the oscillator-grade known risk.

## Clone integrity

Every probe ran in disposable copies under the packet's `scratch/`, and the review clone was never edited. Checked at the end of the round:

- HEAD is `57f4b742b504f5e69293aaa3e00d0470aa9b6071`, tree `499d64f0750f3bc3caf699ee754428dbdeea6e07`.
- `git status --porcelain` is empty.
- The worktree and the index both equal HEAD.
- Every index entry's mode and blob matches `git ls-tree -r HEAD`.
- The gitlinks are unchanged, and each checked-out submodule is clean: `external` efeb541a (not initialised), `gptp-processor` 5dce647a, `protocol-processor` b2db3a97, `third_party/verilog-axis` 48ff7a7e.

## Receipts

Listed in `MANIFEST.sha256`. The scripts are portable: they take a checkout path and use `VERILATOR` for the pinned simulator.

- `scripts/run_meter_mutants_parallel.py` runs the suite's own mutant list unchanged, with at most 8 workers.
- `scripts/probe_meter.cpp` and `scripts/probe_meter.sh` are the independent desk-model probes.
- `scripts/plant_tu_from_tv.sh` is the F1 mutant at the root.
- `receipts/*.log` and `receipts/*.txt` are the raw outputs named above.

R433-1 FINISHED
