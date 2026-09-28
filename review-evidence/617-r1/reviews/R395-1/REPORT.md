[R395] NEGATIVE - exact head 5546b976161bdfd0611040160df44806a0b95d15

# R395-1: external cleared-context review of PR #618 (issue #617)

- Exact head: `5546b976161bdfd0611040160df44806a0b95d15`, tree `628e40ce5857d0a487839a72ff392069b33392e3`, three commits on source base `ce550952e47fbd92367f0d9b099345100f7f4215`.
- Round: R395-1, external reviewer. All five lenses were applied independently at this head.
- Reconstructed from AGENTS.md, CONTRIBUTING.md and docs/README.md, then:
  - issue #617: body, assignment comment 5872575286, TAKEN and REVIEW READY;
  - the PR #618 body;
  - `git diff ce550952e..5546b976` and the three commits;
  - the public evidence tree `c30997b9…/review-evidence/617-r1` (logs and gate summary).
- Author handoff prose was not used as evidence.
- Receipts: every file below is under this packet (`receipts/`, `scripts/`) and is listed in `MANIFEST.sha256`.

## Verdict summary

The frame-atomic handoff does what issue #617 asks. In every scenario I ran at the head, every AAF sample column carries one TDM frame:

- the committed suite;
- 46 + 28 near-crossing CRF phases at the junction;
- 64 CRF phases through the whole `milan_datapath`;
- an exhaustive 131-offset close sweep across one walk.

The defect reproduces exactly at `ce550952` (junction 47/456 failures, INT-true 66.1% torn in the #451 states; datapath 7/118). The resource figures reproduce exactly.

The verdict is NEGATIVE for three findings:

- **F1 (MAJOR):** the handoff moves the junction's only data crossing to the frame close. Nothing keeps a CRF lock off that crossing, and the SLIP_TDM counters cannot see it. In a band of CRF engagement phases the talker repeats and skips whole frames continuously while locked, with SLIP_TDM reading 0/0. At those same phases the base was clean.
- **F2 (MINOR):** no check depends on the one-pair frame length that the I2S-capture shapes elaborate.
- **F3 (MINOR):** the latency table in TIME_SYNC.md states biased sampled means as the handoff's latency change. The deterministic change is up to 20 cycles smaller.

## Findings

### F1 - MAJOR - RTL, Robustness, Tests, Docs - CRF locks can sit on the frame-close/snapshot crossing: sustained whole-frame repeat/skip, invisible to SLIP_TDM

- **Artifacts:**
  - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:544-545` (close), `:1018` (snapshot) and `:594` (the slip marker is still the slot-0 strobe);
  - `hdl/ieee1722/crf/KL_media_grid_align.sv:72-88` (the keep-off is applied to the slot-0 marker);
  - `docs/reference/REGISTER_MAP.md:1833-1840`;
  - `docs/design/TIME_SYNC.md:467`;
  - `tb/verilator/capture_coherence/sim_main.cpp:31-33,420-432`.
- **Authority and evidence:**
  - **The crossing.** At the head a walk takes a frame only if its closing-pair strobe lands by tick+5. A close at tick+6 or later waits for the next walk (`receipts/probe-phase-sweep-head.log`, 131 offsets, one transition). On TDM8 the close is about 781 axis cycles after the slot-0 marker.
  - **The keep-off protects the wrong event.** `KL_media_grid_align` locks wherever it engaged and keeps only the slot-0 marker at least 1/128 sample from the tick. So a lock can place the close on the snapshot, and the lock's dither of about 10 cycles then alternates the frame the walk reads.
  - **Junction, true 391/1591 plan, CRF** (`receipts/probe-crf-zone-head.log`, `-lower.log`):
    - Phases from hold 4032 to 4072 steps (about 10 axis cycles of lock phase, about 1% of the frame) fail the suite's own check "[C] slips while the CRF lock held". They show 34 to 115 slips per 2000 locked columns.
    - Holds up to 4138 (about 26 cycles, about 2.5%) show 18 to 58 repeat/skip pairs during acquisition.
    - Every one has 0 torn columns and `tdm_dup_cnt_o`/`tdm_skip_cnt_o` = 0/0.
  - **Base at the same 46 phases** (`receipts/probe-crf-zone-base-ce550952.log`): 0 torn, 0 repeats, 0 skips. Its only failures are the per-pair-law `[W]` check.
  - **Whole datapath** (`receipts/probe-crf-zone-datapath-head.log`): a 64-phase CRF sweep hits the band at DPZ-63, with 41 slips while locked and 0 torn.
  - **The committed suite cannot see the band.** Its CRF grid is 16 phases about 65 cycles apart plus 8 on ±50 ppm. `sim_main.cpp:31-33` claims "a lock lands in every region the INTERNAL sweep crosses", but a 10-cycle band falls between those phases.
  - **The docs claim otherwise.** `REGISTER_MAP.md:1833-1840`, edited by this PR, says `KL_chan_map_capture` "counts every slip at each junction … the TDM frame bank", and that under CRF "both pairs stop climbing". The counters no longer observe the crossing the walk has.
  - **The PR's own risk note.** The PR body calls this "pre-existing and reduced" and "within the lock's few-cycle dither". At these phases it is new, not pre-existing: the crossing was relocated, not reduced, and no issue was filed.
- **Impact:** under CRF, the Milan media-clock mode, roughly 1 engagement in 100 produces audible frame repeat/skip every 17 to 60 samples until re-engagement, and a further ~1.5% glitch during acquisition. The silicon evidence the docs name, SLIP_TDM static under CRF, reads healthy throughout.
- **Required outcome:** a CRF lock cannot sit within its dither of the walk's snapshot crossing (for example, a keep-off keyed to the frame close relative to the snapshot, or an equivalent). The junction slip evidence counts the crossing the walk actually has. A CRF phase sweep dense enough to resolve the band (a step of 2 cycles or less across it) proves zero slips under lock. REGISTER_MAP, TIME_SYNC and the suite header describe the result accurately. If the maintainer instead records a deferral, the documents must still stop claiming the counters see this crossing. Under AGENTS.md §7 the four lenses stay open while the code is unchanged.
- **Verification:** `scripts/probe_crf_zone/run_zone.sh <clone> junction 3940 4140 2` and `… dp` at the fix head show 0 slips while locked at every phase and counters consistent with the columns. The committed suite gains the dense sweep.

### F2 - MINOR - Tests, Robustness - the one-pair frame (I2S-capture shapes) is not load-bearing in any check

- **Artifacts:**
  - `tb/verilator/chmap_capture/chmap_wrap.sv:208-213` and `sim_main.cpp:37-38`;
  - `hdl/milan/milan_datapath.sv:1216-1218` (`CMAP_TDM_FRAME_PAIRS_C` = 1 when `AUDIO_IF_SLOTS_P == 0`, for example `configs/endstation_arty_current.yaml`, `kind: i2s_philips`, and the default elaboration).
- **Evidence:**
  - Reviewer mutant RM1 closes on pair `N_TDM_P/2-1` regardless of `TDM_FRAME_PAIRS_P`. It passes `capture_coherence` (456/0) and `chmap_capture` (254/0) (`receipts/r395-mutants/SUMMARY.txt`, `rm1.diff`).
  - With RM1, a one-pair front end never publishes, and the TDM bucket stays silent: probe instance u1 fails 3/3 (`receipts/probe-phase-sweep-rm1.log`; the head passes).
  - Lane B's comment says it exercises the one-pair frame. Its stimulus is whole four-pair frames on shared pins, so pair 3 closes the frame either way.
  - The I2S-shape legs of milan_dp never map a capture channel to SRC=TDM (`sim_nxn.cpp` CHMAP_WORD writes 0x8011, 0x8003, 0x9005, 0x5000, 0xC000). I did not run milan_dp against RM1.
- **Impact:** a regression that silences the TDM bucket on every I2S-capture shape would pass the suites this PR adds and changes.
- **Required outcome:** a check fails when a one-pair-frame build does not publish on each pair-0 strobe, for example lane B mapping SRC=TDM idx 0 and driving pair 0 only. A mutant of the RM1 class is killed by a named check.
- **Verification:** RM1, or the mutation arm's equivalent, is caught.

### F3 - MINOR - Docs - TIME_SYNC.md states sampled-mean differences as the handoff's latency change

- **Artifact:** `docs/design/TIME_SYNC.md:470-482`, the "Change" column and "Its change is the read moving to slot 0's instant". The CHANGELOG and PR repeat "+2 to +16 us".
- **Evidence:**
  - Measured directly, the base read pair p's strobe up to tick+6+26p, and the head reads a close up to tick+5 (`receipts/probe-read-instant-{base,head}.log`).
  - The harness's own minimum ages agree: -6/-32/-58/-84 → 776/515/255/-5.
  - So the deterministic per-pair change is 1 + 26p + (3-p)·260.4 cycles: pair 0..3 = 782.3 / 547.8 / 313.4 / 79.0 cycles = 15.65 / 10.96 / 6.27 / 1.58 us.
  - The table's 787.7 / 558.2 / 328.7 / 99.1 cycles are differences of phase-sampling-biased means. At the base the INT-true means are spaced 30.9 cycles apart and the INT-fast means 40.5 apart, although the reads are 26 cycles apart; INT-true runs 1.02 beats.
  - The pair-3 sentence describes a 79-cycle move while the row says +99.1 cycles.
- **Impact:** the latency authority overstates the handoff's cost by up to 20 cycles (+25% on pair 3) and fixes noisy numbers as the contract.
- **Required outcome:** the table states the deterministic change, or labels the means as sampled estimates with their bias, and the pair-3 sentence and row agree. The "Read" row could also state the inclusion bound: a close strobed by tick + `LB_PAIRS_C` + 1 is read.
- **Verification:** the doc values match the probe and min-age derivation above.

### Suggestions (do not affect coverage)

- **S1 (Docs):** on the Arty blend, the I2S pair at crossbar slot 0 now reaches the walk only at a TDM close (`milan_datapath.sv:1214`), so it can wait up to one frame longer. The TIME_SYNC handoff section tables only the 1x1 TDM8 shape and could mention this.
- **S2 (Docs):** `tb/verilator/milan_dp/sim_nxn.cpp:7874` still names `tdm_hold_r`, which this PR renamed.
- **S3 (Tests):** the TDM-bucket slip counters and the aligner marker remain slot-0 based. Note the relation in the suite, whatever F1's resolution.

### Prior findings

There are no prior-round review findings on this PR. A same-head internal round (R394-1) was published during this round. It was not read before this verdict and ledger were written, and nothing here depends on it.

## Checks performed (all at the exact head unless marked base)

| Item | Result | Receipt |
|---|---|---|
| Junction leg | 456 checks, 0 failures; INT-true 0 torn, 21 repeats / 20 skips, 1 cluster | `receipts/head-junction-leg.log` |
| Datapath leg | 118 checks, 0 failures | `receipts/head-datapath-leg.log` |
| Committed mutation arm | 8/8 PASS: two clean controls and six mutants, each caught by its named check | `receipts/head-mutants.log` |
| chmap_capture incl. `[F]` and netlist pin | 254/0 and 20/0 | `receipts/head-chmap_capture.log` |
| Base reproduction (head harness, base RTL) | junction 47/456 (INT-true 66.1% torn: 33.9% coherent, 22.0% each of -1-1-1 / +0-1-1 / +0+0-1); datapath 7/118 | `receipts/base-ce550952-*.log` |
| Reviewer mutants | RM2 (close on pair 2), RM3 (snapshot one cycle late) and RM4 (closing pair not bypassed) are each killed by the junction harness (54 failures). RM1: see F2 | `receipts/r395-mutants/` |
| Exhaustive close sweep, one walk, 131 offsets | never mixed; one transition at tick+6 (coincident-edge close → previous frame, next walk reads the new frame whole); RM3 fails 261 checks | `receipts/probe-phase-sweep-*.log` |
| Elaboration guard | TDM_FRAME_PAIRS_P = 0 or 5 → `$error`, rc 1; 1 or 4 → rc 0 | `receipts/elab-guard.log` |
| OOC 1x1 TDM8 (sv2v + `synth_xilinx -family xc7 -flatten`) | LUT 1292 → 1263 (-29), FF 1048 → 1384 (+336 = 7×48; the closing pair's stage register is pruned), RAM32M 8 → 8, BRAM 0 | `receipts/ooc-1x1tdm8-*.txt` |
| Scope | only `KL_chan_map_capture.sv` and `milan_datapath.sv` change behaviour in `hdl/`; no port lines change; the render crossbar, slip-counter block, processor, firmware and all gitlinks are unchanged; README-tests / MODULE_MATRIX changes are regenerated rows | `git diff --name-status` (recorded in the ledger artifacts) |
| Frame length per shape | I2S 1, TDM8 solo 4, blend 5→4 (closes on TDM pair 2), TDM16 8→4, TDM32 (8x8) 16→4; all front ends deliver pairs in order through a gray FIFO (`KL_tdm_capture*.sv`, `KL_pair_blend.sv`) | source reading |
| IEEE 1722-2016 7.3.5 | an AAF PCM sample event carries one sample per channel for one instant; a TDM frame is one instant for all its slots, so one column = one TDM frame is the correct invariant | clause reading |
| Clone restoration | HEAD, tree, index tree and worktree identical to `628e40ce…`; 0 untracked or ignored entries; submodules clean; gitlinks unchanged | `receipts/restore-verification.txt` |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #617 acceptance 1-3 and assignment decisions against: `KL_chan_map_capture.sv:541-566,1013-1053`; `milan_datapath.sv:1205-1223`; base reproduction and head results; the read-instant probe (no whole frame of latency added: a close by tick+5 is read); IEEE 1722-2016 7.3.5 | R395-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| RTL | UNCLEAN (F1) | `KL_chan_map_capture.sv` (banks, close, snapshot, guard, FSM `:1079-1153`); `KL_media_grid_align.sv:72-117`; front ends' pair order; OOC; elaboration guard | R395-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Robustness | UNCLEAN (F1, F2) | CRF phase sweeps (junction 74 phases, datapath 64), close-offset sweep including the coincident edge, reset and first walk, one-pair frame, per-shape frame lengths | R395-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Tests | UNCLEAN (F1, F2) | `tb/verilator/capture_coherence/*`, `mutants.py`, `tb/verilator/chmap_capture/{chmap_wrap.sv,sim_main.cpp}`; reruns; four reviewer mutants | R395-1 | 5546b976161bdfd0611040160df44806a0b95d15 |
| Docs | UNCLEAN (F1, F3) | `TIME_SYNC.md:453-495`, `REGISTER_MAP.md:1823-1850`, `CHANNEL_MAP_64.md:324-345,405-410`, `FPGA_DESIGN.md:258`, `TESTING.md:490`, `CHANGELOG.md`, PR body | R395-1 | 5546b976161bdfd0611040160df44806a0b95d15 |

## Real limits

- **Simulator path.** The assigned simulator path did not exist. I used Verilator 5.050 (the CI pin) from a local source build, through a wrapper that caps builds at 8 jobs (`receipts/tool-identity.txt`).
- **OOC tools.** sv2v 0.0.13 (CI pins 0.0.12) and Yosys 0.66 were used only for the OOC estimate. My script mirrors `ooc.sh`'s synthesis command, not its ledger machinery. The 8x8 area figures were not reproduced.
- **Suites not run by me** (manager-run per the public gate summary): milan_dp, milan_dp_render, tdm, pair_fill, media_grid_align, pp_shadow, the builder bank, lint, and the Markdown and code-quality gates. RM1 was not run against milan_dp.
- **Band estimates.**
  - The phase-to-hold mapping (about 0.25 axis cycles per 5 ns step) comes from the committed CRF data.
  - The band widths are ±2 cycles, measured on the true plan at 50 MHz only; the ±50 ppm plans were not swept for the band.
  - Slip counts vary by a few between runs because scenario order changes the oscillator phase.
- **No hardware.** Physical calibration was NOT RUN. Simulation is not silicon proof, and bench acceptance 4 is out of scope.
- **Hosted checks at the head, as observed:**
  - `rtl-fast` success.
  - Verilator shards 0, 2 and 3 success; shards 1/5 and 4/5 still in progress.
  - Yosys shards success.
  - "Physical gPTP (nightly and manual)" skipped, which is a skipped context, not an executed pass.

## Pending manager duties

- Decide F1: a fix in this lane, or a recorded deferral with a filed issue. The PR's proposed follow-up, keying the keep-off to the frame close, is not filed. A deferral leaves the lenses open under §7.
- Acceptance of the hosted and act checks at the exact head.
- Candidate-merge validation against live dev `7390b43627032c71c470e2aa8d0845eb5b740663`.
- Bench acceptance 4 on the next image.
- Publication of this packet.

R395-1 FINISHED
