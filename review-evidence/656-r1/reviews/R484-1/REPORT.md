[R484] NEGATIVE - exact head d0e29f6dda6f04f3ace1dbb395f57379e58cacaf

# R484-1: internal cleared-context review of PR #662 (issue #656)

- Head `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf`, tree `289f09d8c7151617ffb019f49b5c972924e4fedd`.
- Source base `c0280fc008ef9c5c1650402a58bab3e47a92127b`.
- Diff: two commits, two files.
  - `tb/verilator/milan_dp/sim_ax1x1gptp.cpp`: +16 / -7.
  - `tb/verilator/milan_dp/README.md`: +10.
- Role: internal reviewer. All five lenses were applied at this head.
- Verdict: **NEGATIVE**, for one reason only: one open MINOR, M1.
  - M1 is in the PR body's #396 limitation bullet: a wrong slip-rate coefficient, and a pre-A2-a clause stated more generally than it holds.
  - **The fix is a PR-body edit. It needs no commit.** Every tree artifact is clean.
  - Conformance, RTL, Robustness and Tests are covered CLEAN at this head. Docs is UNCLEAN until M1 is edited and re-read at this head.
- Also recorded: one pre-existing RESIDUE item (R2) and one SUGGESTION (S1).

## Ruling on the TEST-DEFECT claim

**Upheld.** The three `milan_dp_gptp` order failures (139 / 3) are an honest, counted slip between two clocks. The bench caused them, not a datapath defect. Pacing the peer talker on the modeled audio clock is a faithful model of a peer that follows the DUT's INTERNAL media clock. It hides nothing that the leg's order checks are meant to catch.

### (1) Mechanism, recomputed from the RTL and harness constants

The figures below come from the RTL and harness sources at this head, not from the author's handoff. Receipt: `pacing_model.py` and `receipts/pacing_model.out`.

| Quantity | Source at head | Value |
|---|---|---|
| Axis clock | `tb/verilator/nvm_capture_cpu/recipe.py:5` `CPU_HZ` | 50,000,000 Hz |
| Audio = TDM clock | `sim_ax1x1gptp.cpp:321-333`: +782 twice per axis cycle, toggle at 1591; `clk_tdm_i = clk_audio_i` | 24,575,738.529 Hz |
| TDM frame | `milan_datapath.sv:902-908` with defaults `:151,:152,:162` (no override in `configs/generated/endstation_ax7101_1x1_tdm8`): 8 slots x 32 bclk, `BCLK_HALF` 1 | 512 audio cycles |
| FSYNC | audio / 512 | 47,999.489315 Hz = **-10.6393 ppm** |
| Old talker | parent `kAafPeriod = kHz * 6 / 48000` = 6,250 cycles | exactly 48,000 samples/s |
| Excess into the queue | 48,000 - FSYNC | **0.510685 events/s per pair** |
| Slip period | 1 / excess = 3182/1625 s | **1.958154 s** |
| New talker | `kAafAudioEdges = 6 * 512`, `sim_ax1x1gptp.cpp:89,500-505` | 6,250 + 26/391 (= 52/782) cycles per PDU; 47,999.489315 samples/s, exactly FSYNC |

**RTL chain at head.**

- `milan_datapath.sv:5905`: `mga_sel_w = int_clk_selected_r | follow_sel_r`. This is A2-a, introduced in `d676ecfd4`.
- It engages `KL_media_grid_align` at INTERNAL. The aligner's `frame_ev_i` is the TDM capture's last pair of each frame (`:5925-5926`). Its `u_o` trims `KL_media_nco` (`:777-788`), and `mnco_servo_en_w = mga_sel_w` (`:5932`).
- So `media_tick_p` is phase-locked to FSYNC.
- `KL_chan_map_capture.sv:173-228` (LOOP QUEUE) pops one event per pair per media tick, with depth 8 = 6 + 2. It drops the oldest event on a push into a full queue and counts it on `lb_skip_cnt_o` (`SLIP_LB[31:16]`).
- With the old axis-paced talker, the queue therefore loses one event per pair every 1.958 s.
- The published trace's gap spacing (t = 4.513547 to 6.471693 s, 1.958146 s) agrees with this to within one 20.8 us sample period.

**Counterfactual.** Before A2-a, the INTERNAL grid was `KL_media_nco` untrimmed, which is exactly 48 kHz from 50 MHz. That is the old talker's rate, so the 10.64 ppm beat sat at the TDM junction, which this leg does not grade. The mechanism is complete and consistent.

**First bad commit (acceptance 1).** `d676ecfd4` is where `wire mga_sel_w = int_clk_selected_r | follow_sel_r;` enters (`git show d676ecfd4`). The published pair logs give:

- `c-0b074298.log`: 139 / 0, 40 / 0.
- `c-d676ecfd.log`: 139 / 3.

The author's control `ctl-dev-noA2a.log` (dev RTL with only that line reverted) passes 139 / 0 + 40 / 0. So the attribution is causal: the select line, not the other changes in that large commit.

### (2) Is the corrected talker faithful, or does it hide a defect?

**It is faithful.**

- Under A2-a the DUT's INTERNAL media clock is the audio clock: its FSYNC drives the aligner, `KL_crf_tx` divides it, and the packet grid locks to it.
- A Milan peer that follows that clock, for example through the DUT's CRF output, emits one six-sample PDU per 6 x 512 audio edges.
- Its AVTP timestamps stay on gPTP time: `audio_frame()` stamps `peer_clock(cyc * kPeriodNs)` at the real send instant.
- The model is an ideal follower, with no recovery jitter or wander. The header's omission list already declares this ("oscillator drift", "CRF recovery").

**It hides nothing.**

- This leg never graded slip accounting: `sim_ax1x1gptp.cpp` reads neither `0x8D4` nor `0x8D8`.
- `SLIP_LB` / `SLIP_TDM` honesty is graded elsewhere, for example `sim_aclk.cpp:1085-1127`.
- The order checks' contract (README "Sample order and packet sequence must remain continuous") is a clock-matched expectation. It held before A2-a only because the INTERNAL grid then ran at the talker's rate.
- Under the new pacing the checks additionally grade that the INTERNAL grid really follows the audio clock: see control C1 below.

**Unchanged by diff.** `git diff c0280fc0..d0e29f6d -- tb/verilator/milan_dp/sim_ax1x1gptp.cpp` touches only:

- the header comment;
- the pacing constant (`kAafPeriod` replaced by `kAafAudioEdges`) and its comment;
- the variable `next_audio` renamed `next_audio_edge`;
- the `schedule()` trigger (`cyc >= next_audio` became `audio_edges >= next_audio_edge`), keeping the same 200-cycle PTP guard;
- the `configure()` initialiser.

No check, label, window, timer, threshold, or `verify_abort.py` line changed. Every run gives 139 physical + 6 / 20 / 14 accounting checks, i.e. 139 + 40.

### (3) Controls: re-run here, exact head plus two planted controls, concurrently

Pinned Verilator 5.050: wrapper sha256 `905795b9...`, `--version` "Verilator 5.050 2026-07-01 rev v5.050". Each run was `make -j4 -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4` in its own scratch copy of this clone.

| Run | Source | Binary sha256 | Physical | Accounting | Wall time |
|---|---|---|---|---|---|
| H | exact head | `e9052849...` | **139 / 0**, all ten windows `bad_order=0` | 6 / 0, 20 / 0, 14 / 0; make rc 0 | 3,377 s sim; 4,042 s driver |
| C1 | head; `milan_datapath.sv:5905` became `wire mga_sel_w = follow_sel_r;` | `3b035d43...` | **139 / 5**: windows acquisition 1, peer loss 3, recovery 1, reset reacquisition 1; cumulative 8 | not reached; make rc 2 | 3,503 s |
| C2 | head RTL; parent's axis-paced harness | `4cd8a8c9...` | **139 / 3**: peer loss 2, recovery 2; cumulative 5 | not reached; make rc 2 | 3,369 s |

- **Binaries.** Each binary is bit-identical to the author's corresponding published build: `fix1`/head `e9052849`, `ctl-fix-noA2a` `3b035d43`, `dev-c0280fc0` `4cd8a8c9`.
- **Transcripts.** Each 274-line simulation transcript, from "ax1x1gptp PHYSICAL" to the tally, is byte-identical to the published log (`receipts/transcript_compare.txt`). C2's equals dev `c0280fc0`'s, whose failure set is the hosted nightly's. The README edit is not compiled.
- **Answer to (3).** The corrected order checks still detect a rate mismatch on the DUT side. C1, an INTERNAL grid that does not follow the audio clock, fails 4 windows and the cumulative check, with duplicates rather than gaps. C2, a talker off the DUT's media clock, fails too.
- **Pass condition.** The check passes only when the two clocks agree.
- **Sensitivity.** The order checks see a residual rate error only if a slip lands in graded time. Over this leg's ~17 s, with the queue's 2-event margin, the floor is a few ppm. That is inherent to a 17 s run, not introduced here.

### (4) The 160-PDU no-TX pin (`verify_abort.py:76`)

Exact replay of the harness clock and `schedule()`: `pacing_model.py`, four `configure()` anchors, one full 391-PDU / 2,443,776-cycle pattern period.

- **Exposure.** A 20 ms window holds 160 PDUs at 99.8298 % of start phases and 159 at **0.1702 %** (4,160 of 2,443,776). A window is 159.998298 PDUs, a deficit of 10.639 cycles. The PR's "about 0.17 %, the last 10.6 cycles of a period" is right.
- **Old pacing.** The strict 6,250-cycle lattice gave 160 at every phase, so the pin was phase-invariant before this PR.
- **Determinism.** The model is deterministic: the Verilated model runs single-threaded and the harness has no randomness. The window phase is fixed by the RTL's boot and CSR latencies.
- **At this head.** Both silent windows count 160. `receipts/H-no-tx-control.log` and `receipts/H-stop-tx-control.log` are byte-identical to the author's.
- **Grading.** This is a defect introduced by this PR, not residue: it is a test-robustness property, not wording. It is graded SUGGESTION (S1) because:
  - it can only produce a loud, deterministic false FAIL, never a false pass;
  - it is reachable only by a later change that moves that phase into a 10.6-cycle zone;
  - it is publicly disclosed in the PR body.

### (5) Docs

- **The README model row and paragraph** (`tb/verilator/milan_dp/README.md:173, 200-207`) are accurate against the RTL:
  - six samples per PDU, one PDU per 3,072 rising audio edges;
  - A2-a holds the grid on FSYNC at INTERNAL, with the TDM feed live;
  - the queue fills from received PDUs and drains on the grid;
  - an axis-paced talker is 10.64 ppm fast, with one drop per 1.958 s counted on `SLIP_LB`;
  - zero duplicate or gap is the right expectation only for a talker on the DUT's media clock.
- **Harness comments** at `sim_ax1x1gptp.cpp:22-27, 82-88` say the same, correctly.
- **Stale counts.** The 137 / 177 counts at `tb/verilator/milan_dp/README.md:297` and `tb/verilator/milan_dp_gptp/README.md:7,9` predate the lane: dev `c0280fc0` already counts 139 / 179. The PR's text does not rely on them, so they are graded as pre-existing RESIDUE (R2).

### (6) The #396 consequence in the PR text

- **README: correct.** The durable text states the right general rule: "No duplicate or gap is the expectation only for a talker on the DUT's media clock".
- **PR body: correct conclusion.** "A zero-glitch run through the loopback lane (#396) needs the DUT to follow the talker, or the talker to follow the DUT" is right.
- **PR body: two incorrect technical statements** in its "Known limitations" bullet, recorded as MINOR M1:
  - "about 0.51/s per 10 ppm" should be 0.48 events/s per 10 ppm. 0.51/s is the figure at plan A's 10.64 ppm.
  - "before A2-a the slip sat at the TDM junction" holds only for this leg's axis-nominal talker. Against any other asynchronous talker, the loopback queue slipped at INTERNAL before A2-a as well.

## Findings

### M1: MINOR, Docs, PR #662 body, "Known limitations / out of scope", bullet "INTERNAL against an asynchronous talker is not graded by this leg"

- **Evidence.**
  - The bullet says the loopback path "still slips about 0.51/s per 10 ppm".
  - `receipts/pacing_model.out`: 48,000 x 10 ppm = 0.480 events/s per fed pair; 0.5107 events/s is the figure at plan A's 10.64 ppm.
  - The same bullet says "before A2-a the slip sat at the TDM junction". Before A2-a the INTERNAL grid ran at axis-nominal 48 kHz (`KL_media_nco` untrimmed). So only a talker at exactly that rate, this bench's old axis-paced talker, had its slip at the TDM junction. Any other asynchronous talker also slipped on the loopback path at INTERNAL before A2-a.
  - The PR body's own Mechanism section states the latter correctly in its narrower context. The same coefficient appears in the issue's REVIEW READY comment, which is not to be edited.
- **Why MINOR and not RESIDUE.**
  - This round first graded the item RESIDUE. On resolving the external reviewer's identical finding (see "Prior public review findings"), it is re-graded MINOR.
  - Both defects are technical claims, not phrasing: a numeric coefficient, and a statement about the DUT's pre-A2-a behaviour. The owner's residue rule excludes defects that change a figure or a technical claim, and sends any doubt to MINOR.
- **Impact.**
  - A reader sizing #396's zero-glitch run from this bullet scales the slip rate about 6 % high.
  - The reader would also wrongly infer that INTERNAL never slipped on the loopback path before A2-a.
  - No tracked file, test, code, measurement or verdict is affected. The README (`:200-207`) and the code comment state 10.64 ppm / 1.958 s correctly.
- **Required outcome.** The PR body states:
  - the loopback slip as about 0.48 events/s per fed pair per 10 ppm, or 0.51/s at plan A's 10.64 ppm; and
  - the pre-A2-a clause restricted to a talker at the nominal packet-grid rate (this bench's old pacing), or dropped.
  - Suggested text: "It still slips about 0.48 events/s per fed pair per 10 ppm on the loopback path (0.51/s at plan A's 10.64 ppm), counted on `SLIP_LB`. For this leg's old axis-paced talker the slip sat at the TDM junction before A2-a; a talker on any other clock slipped on the loopback path at INTERNAL before A2-a too."
- **Verification.** A reviewer re-reads the edited PR body at the same head `d0e29f6d`. No tree change is needed, so the other four lenses' coverage at this head is unaffected.

### R2: RESIDUE, pre-existing, Docs, `tb/verilator/milan_dp/README.md:297`; `tb/verilator/milan_dp_gptp/README.md:7,9`; `tb/verilator/milan_dp/README.md:287`

- **Evidence.**
  - The leg counts 139 physical / 179 total at both dev `c0280fc0` (`dev-c0280fc0.log`, run C2) and head (run H). The prose still says 137 / 177.
  - The trimmed-scenario duration at `:287` reads 16.992496440 s / 849,624,822 cycles. The measured value is 16.992510280 s / 849,625,514 cycles, identical at dev and head, so this PR did not change it. The `:359` line is a dated historical measurement and stays.
- **Impact.** Prose figures that predate this lane. No test reads them.
- **Required outcome.**
  - `milan_dp/README.md:297`: "The physical harness contributes 139 checks."
  - `milan_dp_gptp/README.md:7`: "The normal total is 179 checks: 139 physical, 40 accounting."
  - `milan_dp_gptp/README.md:9`: "... with 139 checks."
  - Optionally `:287`: "16.992510280 simulated seconds over 849625514 cycles".
  - These may be carried on the residue checklist rather than in this PR.
- **Verification.** `grep -n '13[79]\|17[79]' tb/verilator/milan_dp/README.md tb/verilator/milan_dp_gptp/README.md`.

### S1: SUGGESTION, Tests, Robustness, `tb/verilator/milan_dp_gptp/verify_abort.py:76`; `tb/verilator/milan_dp/README.md:275`

- **Evidence.** See (4).
  - The exact pin `windows[-1] == ("160", "0", "0")` was phase-invariant under 6,250-cycle pacing.
  - At 6,250 + 26/391 cycles per PDU, it holds at 99.83 % of window phases. It holds at this head's deterministic phase.
  - README `:275`'s "covers 160 PDUs" is true at this phase and nominally 159.998.
- **Impact.** A later, unrelated change to boot or CSR latency has a 0.17 % chance of producing a deterministic, loud false FAIL of "silent window has RX traffic and zero TX or samples". It can never produce a false pass. The explanation currently lives only in the PR body.
- **Optional outcome.** Either:
  - record the phase dependence beside the pin and at README `:275`; or
  - let the pin accept the lattice's two possible counts (159 or 160) with that reason stated, keeping the TX and sample zeros exact.
- **Verification.** `python3 verify_abort.py` still gives 20 / 0. With the relaxed pin, a planted 158 or a nonzero TX count still fails.

There are no BLOCKER or MAJOR findings. One MINOR (M1) is open.

## Lens coverage, with artifacts

- **`Conformance`: CLEAN.**
  - Issue #656 acceptance:
    - 1 met, by the merge bisect plus the mechanism, with `d676ecfd4` and the causal A2-a-only revert.
    - 2 met: the check graded a wrong bench model, and is corrected with planted controls C1 and C2 on both sides, re-run here.
    - 3 met locally: 139 / 0 + 40 / 0 at the exact head with pinned 5.050, run H. The hosted half is open: at this head the hosted "Physical gPTP (nightly and manual)" context is **skipped**, not executed. So "Relates to #656" is correct.
  - A2-a behaviour checked against `docs/design/MEDIA_CLOCK_FOLLOWING.md:1133-1145,1504-1515` (D4 row, known risk) and `milan_datapath.sv:5880-5932`.
  - Plan A is the right model for this TDM8 shape: `sw/litex/milan_soc.py:335-356`, where plan B applies only with `audio_tdm_hz`.
  - M1 and R2 are documentation statements, outside the tree's conformance claims.
- **`RTL`: CLEAN.**
  - No RTL in the diff.
  - Examined: `milan_datapath.sv:750-790` (`KL_media_nco`), `:902-908` (TDM frame), `:1017-1038` (TDM master), `:5880-5932` (A2-a select, aligner, trim enable), and `KL_chan_map_capture.sv:173-228` (LOOP QUEUE depth, pop, drop-oldest, counters).
  - The mechanism's rate and period were recomputed exactly (table above). Removing A2-a flips the outcome (C1).
- **`Robustness`: CLEAN.**
  - Examined `sim_ax1x1gptp.cpp:483-506` (`schedule()`: fixed-increment edge target, so there is no long-term drift; backlog catch-up as before; the 200-cycle PTP guard still exceeds a 230-byte PDU's 116 cycles).
  - Examined `:671-746` (the reset epoch re-anchors `next_audio_edge` on the continuing `audio_edges`; warm-up still excludes order comparisons), and the four control switches. Every switch uses the same pacing.
  - The exact pin's new phase dependence is quantified (S1, SUGGESTION, no false pass).
- **`Tests`: CLEAN.**
  - Diff-confirmed: check code, windows, timers and counts are unchanged.
  - H passes 139 / 0 + 40 / 0. C1 fails 139 / 5. C2 fails 139 / 3.
  - All three binaries and transcripts are bit-identical to the published evidence.
  - `sw/builder/test_clock_contract.py` rc 0: its `test_sim_clock` reads this harness.
  - `scripts/check_cpp_idiom.py` rc 0.
- **`Docs`: UNCLEAN.**
  - M1 (PR body) is open.
  - The tracked documentation is accurate: `tb/verilator/milan_dp/README.md:173,200-207` and `sim_ax1x1gptp.cpp:22-27,82-88`.
  - `docs_check.py`, `check_doc_style.py` and `check_doc_paths.py` all rc 0.
  - R2 is pre-existing RESIDUE.
  - The commit subjects are one line with no trailers.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #656 acceptance 1-3; `MEDIA_CLOCK_FOLLOWING.md` D4/A2-a; `milan_datapath.sv:5905`; `d676ecfd4`; runs H/C1/C2; head check runs (Physical gPTP skipped) | R484-1 | `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` |
| RTL | CLEAN | `milan_datapath.sv:750-790,902-908,1017-1038,5880-5932`; `KL_chan_map_capture.sv:173-228`; `pacing_model.py` | R484-1 | `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` |
| Robustness | CLEAN (S1 SUGGESTION only) | `sim_ax1x1gptp.cpp:483-506,671-746`; `verify_abort.py:59-98`; exact phase replay | R484-1 | `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` |
| Tests | CLEAN (S1 SUGGESTION only) | diff of `sim_ax1x1gptp.cpp`; runs H / C1 / C2; transcript and binary identity; `test_clock_contract.py`; `check_cpp_idiom.py` | R484-1 | `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` |
| Docs | UNCLEAN (M1 MINOR open; R2 RESIDUE) | `milan_dp/README.md:173,200-207,275,287,297`; `milan_dp_gptp/README.md:7,9`; the PR #662 body as fetched at 02:09:42Z (last update); doc gates | R484-1 | `d0e29f6dda6f04f3ace1dbb395f57379e58cacaf` |

## Prior public review findings on this PR

- **When they were read.** This round's own pass, verdict and ledger were written first. The PR's public review state was then read: no formal reviews, no review comments, and one review verdict, `[R485] NEGATIVE` (issue comment 5986909374, 02:09:42Z, exact head `d0e29f6d`).
- **What was found.** All three of its findings were found independently in this round. Each is resolved or retained at this head below.

| Prior finding | Severity there | Status at `d0e29f6d` | This round |
|---|---|---|---|
| R485 F2: PR body #396 bullet, "0.51/s per 10 ppm" and the pre-A2-a clause | MINOR, Docs | **Retained, open.** The PR body is unchanged (last update 02:09:42Z, both phrases still present) | Same defect as M1. This round's first grading was RESIDUE; it is re-graded MINOR on the residue rule's doubt clause (see M1) |
| R485 F1: `verify_abort.py:76` exact 160 pin | SUGGESTION, Tests, Robustness | **Retained as SUGGESTION.** The pin is unchanged | Same as S1. The external probe's measured margin (window 299-313 cycles from the 159 band) agrees with this round's 0.1702 % exact replay |
| R485 RES-1: stale 137 / 177 counts | RESIDUE, pre-existing | **Retained as residue.** The lines are unchanged | Same as R2, which adds the stale duration at `milan_dp/README.md:287` |

There is no disagreement on the mechanism, the TEST-DEFECT ruling, the controls or the lens results, apart from the M1 severity, which now agrees.

## Real limits

- **Simulation only.** No hardware, bench, physical calibration or field run. Field skips are not hardware proof.
- **Not run here:**
  - the full parent / PP / gPTP / Yosys / builder banks;
  - `act` / `act_ci`;
  - `check_em_dash.py --base c0280fc0`. Its pinned Markdown renderer (html5lib) is not installed, and installing it is outside this unit. A grep of the diff finds zero em-dash characters.
  - `gen_toc.py` and the hygiene / naming gates (manager evidence only);
  - the `--extended` arm and `--negative-control`.
- **One unmodelled case.** The ideal-follower talker has no recovery jitter or wander. The queue's 2-event margin against a real follower's jitter is not exercised by this leg.
- **The hosted Physical gPTP context at this head was skipped.** Acceptance 3's hosted half needs the merged head or a dispatch.
- **Clone state.** It was left at exact head bytes (`receipts/clone_integrity.txt`):
  - zero tracked, untracked or ignored deltas;
  - the index tree equals HEAD's tree `289f09d8...`;
  - gitlinks `gptp-processor 5dce647a`, `protocol-processor 631eeb34`, `third_party/verilog-axis 48ff7a7e`; `external` is not initialised, as on arrival.

## Pending manager duties

- Carry M1 to the executor as a PR-body edit only, with no commit. A reviewer re-read of the edited body at `d0e29f6d` can then bank Docs. The other four lenses remain covered at this head.
- Carry R2 (pre-existing stale counts) to the residue checklist. Record S1 as optional.
- Final current-dev candidate build and validation at the merge turn: source base `c0280fc0`, live dev `506d91db`.
- Hosted / act acceptance, including exact-head `verilator-suites`.
  - At 02:12:46Z, Verilator shard 1/5 was still in progress (`receipts/hosted_checks_at_head.txt`).
  - Every other executed context had succeeded. Physical gPTP was skipped.
- The hosted Physical gPTP run that closes acceptance 3. Switch to "Closes #656" only after it reports 139 / 0.
- The second (external) positive review. Merge only on maintainer authorization.

## Receipts

Every receipt is listed in `MANIFEST.sha256`, with paths relative to the packet root.

- `pacing_model.py`: the exact rate and phase replay.
- `summarize_runs.sh` and `run_controls.sh`: the run reproduction.
- `receipts/`:
  - `pacing_model.out`;
  - `run-H.log`, `run-C1.log`, `run-C2.log` (private paths redacted), and `runs_summary.txt`;
  - `H-no-tx-control.log`, `H-stop-tx-control.log`, `H-no-pdelay-control.log`;
  - `transcript_compare.txt`, `C1-plant.diff`, `C2-harness-revert.stat`, `lane.diff`;
  - `hosted_checks_at_head.txt` and `clone_integrity.txt`;
  - the gate outputs `test_clock_contract.out`, `check_cpp_idiom.py.out`, `docs_check.py.out`, `check_doc_style.py.out`, `check_doc_paths.py.out`, and `check_em_dash.out` (renderer absent).

R484-1 FINISHED
