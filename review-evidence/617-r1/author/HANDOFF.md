# HANDOFF - #617 frame-atomic TDM capture handoff ([A424])

Status: REVIEW READY at `5546b976161bdfd0611040160df44806a0b95d15` (local branch; not pushed - this lane may not push)

- Repository: kebag-logic/milan-fpga, origin `https://github.com/kebag-logic/milan-fpga.git`
- Lane: `$LANES/617-capture-frame-atomic`, branch `617-capture-frame-atomic` (local only, not pushed)
- Base: dev `ce550952e47fbd92367f0d9b099345100f7f4215`
- Head: `5546b976161bdfd0611040160df44806a0b95d15` (3 commits on ce550952):
  - `d8034466a323722f1826bc2b90279b827376b462` Publish whole TDM frames to the capture crossbar walk
  - `964a45b64ca5b45f51a44feb18cc8e3bd96f35a7` Grade Talker AAF column coherence against a drifting TDM frame
  - `5546b976161bdfd0611040160df44806a0b95d15` Document the frame-atomic TDM capture handoff and its latency
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5872575286
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5872598411
- Roles: executor [A424]; internal reviewer [R394]; external reviewer [R395]
- Scope: #617 acceptance 1-3. Acceptance 4 (bench re-run of the #451 DIN capture) follows on the
  next image, so the PR body says "Relates to #617".

## 1. Defect reproduction at ce550952 (torn-state table)

The committed simulation (`tb/verilator/capture_coherence`, section 4) was written first and
built against the ce550952 `KL_chan_map_capture.sv` (and, for the datapath leg, the ce550952
`milan_datapath.sv`), outside the tree (`git show ce550952:<path>` into /tmp). It FAILS there and
reproduces the #451 bench's torn states: pairs never split internally, pairs 1..3 are either
equal to pair 0 or one frame older, in the same four states and the same order.

INT-true scenario: the true 391/1591 plan (fsync -10.64 ppm against the NCO's 48 kHz), 1x1 TDM8
shape, 50 MHz axis clock, one whole beat (96,000 AAF columns), INTERNAL:

| Offset of pairs 1, 2, 3 against pair 0 | ce550952 sim: columns | share | #451 bench (PR #616 page) share | Meaning |
|---|---:|---:|---:|---|
| 0, 0, 0 | 32,545 | 33.9% | 32.5% | coherent |
| -1, -1, -1 | 21,152 | 22.0% | 22.2% | pairs 1 to 3 one frame older |
| 0, 0, -1 | 21,152 | 22.0% | 22.7% | pair 3 one frame older |
| 0, -1, -1 | 21,151 | 22.0% | 22.7% | pairs 2 and 3 one frame older |
| total torn | 63,455 of 96,000 | 66.1% | 67.5% | |

Why the shares: at 50 MHz a TDM8 pair period is 260.4 axis cycles and the walk reads successive
TDM pairs 26 cycles apart, so each torn state spans 260.4 - 26 = 234.4 of the 1041.7-cycle frame
(22.5%) and the coherent state the remainder (32.5%). The bench's 32.5/22.7/22.7/22.2 is that
geometry; the sim's 33.9/22.0 differs by the model's CDC/pipeline offsets.

Other ce550952 failures of the same harness (junction leg):

| Scenario | ce550952 torn columns | note |
|---|---:|---|
| INT-slow (-1000 ppm, 3.2 beats) | 2,160 / 3,204 (67.4%) | same four states |
| INT-fast (+1000 ppm, 3.2 beats) | 2,025 / 3,204 (63.2%) | same four states |
| CRF-true-01 .. -11 (lock in a torn region) | 100% (61.9% for -01, which settles across a boundary) | CRF freezes the phase: a lock in a torn region tears every column |
| CRF-true-00, -12 .. -15 (lock in the coherent region) | 0 | but -00 fails [W]: a frame completing mid-walk is read |
| CRF-50-0 .. -2, CRF+50-1 .. -3 | 85.6% to 100% | |

Datapath leg (whole `milan_datapath`, shipping 1x1 TDM8, frames read at the MAC), final harness,
against the ce550952 crossbar AND datapath: 7 of 118 checks fail. DP-INT-slow 1,483 / 2,202
torn (67.3%), DP-INT-fast 1,350 / 2,202 (61.3%), DP-CRF-1..5 100% torn, DP-CRF-0/6/7 0%.

Final-harness re-run of the junction leg against the ce550952 crossbar: 47 of 456 checks fail
(INT-true 63,456 / 96,000 torn = 66.1%, states 0,0,0 33.9% and 22.0% each torn state; CRF-true
01..11 torn, 02..11 100%; CRF-50 0..2 and CRF+50 1..3 torn). Logs:
`evidence/ce550952-junction-leg.log` (23.7 KB) and `evidence/ce550952-datapath-leg.log` (4.2 KB).

Mechanism confirmed: `KL_chan_map_capture.sv:486-487` at ce550952 writes `tdm_hold_r[slot]` on
each pair's own strobe; the walk reads `tdm_hold_r[idx]` at each slot's inject (`:959-960`). The
TDM8 master strobes pair k at the end of slot 2k+1, so a tick landing between pair k's and pair
k+1's strobes reads pairs 0..k new and k+1..3 old.

## 2. Design of the frame-atomic handoff (file:line at the head)

Files: `hdl/ieee1722/aaf/KL_chan_map_capture.sv`, `hdl/milan/milan_datapath.sv`.

- Banner paragraph "TDM FRAME HANDOFF (#617)" - `KL_chan_map_capture.sv:63-95`.
- New parameter `TDM_FRAME_PAIRS_P` (default N_TDM_P/2) - `KL_chan_map_capture.sv:314-317`;
  elaboration guard `g_tdm_frame_guard` (1..N_TDM_P/2) - `:518-524`.
- Three banks (`:526-566`, `source_latch`):
  - STAGE `tdm_stage_r[p]`: written by pair p's own strobe (the old hold).
  - FRAME `tdm_frame_r[p]` (public_flat_rd, keeps the 0x0042 tie-off tap): on the strobe of pair
    `TDM_FRAME_PAIRS_P-1` (the frame's last) every entry loads in one edge - the closing pair from
    the input, the others from the stage. The select is an elaboration constant per entry: no mux.
  - WALK `tdm_walk_r[p]` (`:1013-1027`, `tdm_walk_snapshot`): loaded from FRAME on the pre-walk's last cycle
    (`st_r == CM_POP_S && pop_idx_r == LB_PAIRS_C`, the edge before CM_STEP_S reads slot 0) and
    held for the whole walk. The resolver reads it (`:1052-1053`).
- Why the walk bank is needed: at the 8x8 shape a walk takes 866 cycles; the gap from a frame's
  last pair to the next frame's first is 2 TDM slots (260 cycles at 50 MHz). Deferring the publish
  to the walk's end would let the next frame overwrite the stage.
- `milan_datapath.sv:1208-1223`: `CMAP_TDM_SLOTS_C = 8`, `CMAP_TDM_FRAME_PAIRS_C = min(AIF_PAIRS_C, 4)`
  passed as `TDM_FRAME_PAIRS_P`. AIF_PAIRS_C is the front end's per-frame supply (1 I2S capture;
  S/2 TDM master or slave; S/2+1 blend). Shipping 1x1 TDM8: 4 (closes on pair 3). I2S shapes: 1.
  Arty blend (I2S at slot 0, TDM pairs at 1..4): 4, closing on slot 3 (TDM pair 2); the I2S pair
  is published with each TDM close (same audio clock, so a fixed offset below one frame).
- Unchanged: the render (DOUT) path; the channel-map semantics (entry encoding, routing, silence,
  LOOP queue); the #74 junction slip counters (slot-0 marker vs tick) and the aligner's marker;
  every port of `KL_chan_map_capture` and `milan_datapath`; no processor or firmware change.

## 3. Latency effect against TIME_SYNC.md

- Render tables (Listener render latency, Interface after the grid): unchanged; the render path
  does not pass through `KL_chan_map_capture`.
- Loop facts: the slip RATE is unchanged (one sample per 1.958 s beat at INTERNAL; 0 under CRF).
  A beat now slips one whole frame where it used to slip each pair at its own phase.
- New subsection `docs/design/TIME_SYNC.md` "Talker capture handoff" tables the capture side.
  Measured over one beat of the true plan, 1x1 TDM8, 50 MHz (sample age = walk's tick minus the
  cycle the pair entered the crossbar):

| Pair | ce550952 mean / min..max (cycles) | head mean / min..max (cycles) | mean change |
|---|---|---|---|
| 0 | 519.4 / -6..1035 | 1307.1 / 776..1817 | +787.7 cycles = +15.75 us |
| 1 | 488.5 / -32..1009 | 1046.7 / 515..1557 | +558.2 cycles = +11.16 us |
| 2 | 457.6 / -58..983 | 786.3 / 255..1297 | +328.7 cycles = +6.57 us |
| 3 | 426.7 / -84..957 | 525.8 / -5..1036 | +99.1 cycles = +1.98 us |

- Interpretation: pair 3 (the frame's last) changes only by the read instant moving from slot 3's
  inject to the snapshot before slot 0 (about 79 cycles plus the negative tail). Pairs 0..2 add
  (3 - p) pair periods of 5.208 us: the wait for their own frame to complete, which is what frame
  atomicity requires. Frame-level age at the tick: one frame (-5..1036 cycles), uniform over a beat.
  No added whole sample: the walk always reads the NEWEST complete frame, graded per walk by the
  [W] "older than the newest frame closed by the tick" check.
- AAF_LATENCY_TAPS.md: TX0 CAP is the front-end strobe `aafcap_pv_w`, before the crossbar; D0
  (CAP to PKT_SOF) stays inside its one-6-sample-window envelope. Not edited.

## 4. Simulation table (INTERNAL and CRF, drift cases)

Suite `tb/verilator/capture_coherence` (new). `make` = junction leg (`run`), datapath leg (`dp`),
mutation arm (`mutants`). Junction leg: real `KL_tdm_capture_master` + `KL_media_nco` +
`KL_media_grid_align` + `KL_chan_map_capture` + `KL_aaf_packetizer` wired as milan_datapath wires
them (1x1 TDM8, 50 MHz axis clock); SoC model shifts the #451 pattern into `tdm_data_i` off the
master's bclk/fsync (dsp_a, one-bit delay). CRF = the aligner engaged (sel_crf_i, the net
milan_datapath resolves from the stored CLOCK_SOURCE).

Checks per scenario: [A] valid tags / L-R split / columns mixing two frames (acceptance);
[W] walks torn / older than the newest frame closed by the tick / reading a frame closed after
their first inject; [C] continuity steps, slip clusters net one frame in the drift direction, one
cluster per beat crossing (INTERNAL), no slip in the CRF tail; [V] front end captured the pattern,
columns decoded, 16 phase bins visited (INTERNAL), aligner engaged and phase held (CRF).

| Scenario | Source | TDM plan | Columns | ce550952 torn | head torn | head result |
|---|---|---|---:|---:|---:|---|
| INT-true | INTERNAL | true 391/1591 (-10.64 ppm), one whole beat | 96,000 | 66.1% | 0 | PASS |
| INT-slow | INTERNAL | -1000 ppm, 3.2 beats | 3,200 | 67.4% | 0 | PASS |
| INT-fast | INTERNAL | +1000 ppm, 3.2 beats | 3,200 | 63.2% | 0 | PASS |
| CRF-true-00..15 | CRF | true plan, 16 lock phases | 2,000 each | 100% in 11 of 16 | 0 | PASS |
| CRF-50-0..3 | CRF | -50 ppm, 4 lock phases | 6,000 each | 85.6-100% in 3 of 4 | 0 | PASS |
| CRF+50-0..3 | CRF | +50 ppm, 4 lock phases | 6,000 each | 86.3-100% in 3 of 4 | 0 | PASS |
| DP-INT-slow | INTERNAL | -1000 ppm, 2.2 beats, whole datapath | 2,200 | 67.3% | 0 | PASS |
| DP-INT-fast | INTERNAL | +1000 ppm, 2.2 beats, whole datapath | 2,200 | 61.3% | 0 | PASS |
| DP-CRF-0..7 | CRF (stored CLOCK_SOURCE poked) | true plan, 8 lock phases | 1,500 each | 100% in 5 of 8 | 0 | PASS |

Totals at the head (committed-head run, `make -C tb/verilator/capture_coherence`, 366 s, rc 0):
junction leg 456 checks 0 failures; datapath leg 118 checks 0 failures; mutants 8/8.
At ce550952 with the same final harness: junction 47/456 fail, datapath 7/118 fail (section 1).

`tb/verilator/chmap_capture` also gained [F]: one t1 PDU whose six columns each have one right
answer (whole frame A; still A after a partial B; B after its close; still B when C closes between
the walk's TDM slots; C; D). 254 checks, 0 failures. [F] fails under the per-pair-stage law
(14 failures) and under an unsnapshotted walk (4 failures). Lane B now elaborates a one-pair frame
(`TDM_FRAME_PAIRS_P=1`, the I2S shapes' value); [A]/[LB5] deliver whole frames.

## 5. Mutant table

`python3 mutants.py` (the suite's `mutants` target, part of the default `make`):

| # | Leg | Mutant | Named check that must fail | Result |
|---|---|---|---|---|
| C1 | junction | clean control (unmutated crossbar, --quick) | none | PASS |
| C2 | dp | clean control (unmutated datapath) | none | PASS |
| M1 | junction | the walk reads the per-pair stage (the ce550952 latest-sample law) - the removed-atomicity mutant | [A] AAF columns mixing two TDM frames AND [W] walks reading two TDM frames | caught |
| M2 | junction | no walk snapshot: the walk reads the frame bank live | [A] AAF columns mixing two TDM frames | caught |
| M3 | junction | the frame is closed by its first pair | [A] AAF columns mixing two TDM frames | caught |
| M4 | junction | the frame is published whole but one pair late (at the next frame's first pair) | [W] walks older than the newest frame closed by the tick | caught |
| M5 | junction | the stage is never written | [V] every requested column was decoded | caught |
| M6 | dp | milan_datapath tells the crossbar a one-pair TDM frame | [A] AAF columns mixing two TDM frames | caught |

8 checks, 8 PASS, 0 FAIL (4 min 26 s).

## 6. Resource comparison (1x1 TDM8)

`KL_chan_map_capture` standalone, `syn/yosys/ooc.sh` recipe (sv2v, `synth_xilinx -family xc7
-flatten`, stat), chparam N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8 (the shipping 1x1
TDM8 shape: one talker, backed loopback lane), TDM_FRAME_PAIRS_P default 4. Head row from
`OOC_CHPARAM=... syn/yosys/ooc.sh KL_chan_map_capture`; ce550952 row from the identical recipe
replayed on the ce550952 file (the replay reproduces ooc.sh's head row exactly).
Yosys 0.66 (CI pin) with its ABC; sv2v v0.0.13 locally (CI pins v0.0.12).

| Shape | Version | LUT | LUTRAM | LUT_TOT | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 | ce550952 | 1292 | 32 | 1324 | 1048 | 0 | 0 | 0 | 34 |
| 1x1 TDM8 | head | 1263 | 32 | 1295 | 1384 | 0 | 0 | 0 | 34 |
| 1x1 TDM8 | delta | -29 | 0 | -29 | +336 | 0 | 0 | 0 | 0 |
| 8x8 (N_SLOTS_P=32, LB 1x2) | ce550952 | 2062 | 32 | 2094 | 1595 | 0 | 0 | 0 | 34 |
| 8x8 | head | 2103 | 32 | 2135 | 1931 | 0 | 0 | 0 | 34 |
| 8x8 | delta | +41 | 0 | +41 | +336 | 0 | 0 | 0 | 0 |

- +336 FF = stage 3x48 (pair 3's stage is never read and is pruned) + frame 4x48 + walk 4x48
  - the old 4x48 hold. The loads are clock-enabled flop copies; no read-mux width changes.
- LUT moves -29 (1x1) and +41 (8x8): mapping noise of the order the ooc README warns about.
  BRAM 0 both.
- In-context `milan_datapath` delta not measured (a flattened datapath synth exceeds this
  session's single-command limit); placed Vivado utilization remains the release authority
  (docs/design/AREA_BUDGET.md).

## 7. Gate table

All at head `5546b976161bdfd0611040160df44806a0b95d15`, clean tree (`git status --porcelain` empty
before and after), physical path `$LANES/617-capture-frame-atomic`, every command in
the foreground or (when it outran one tool call) with its exit status written to a file and
waited for; nothing piped. Markdown gates with the pinned environment
`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. Full list with each command:
`evidence/gate-summary-5546b976.txt` (78 entries, all rc 0). `GIT_CONFIG_*` set
core.commitGraph=false for git-reading gates, because this worktree's git prints a commit-graph
warning on stderr that `gen_hdl_reference.py` otherwise reads as dirty HDL.

| Gate | Command | rc | Result |
|---|---|---:|---|
| Builder bank | `python3 sw/builder/test_builder.py --require-rv32` (RV32 SDK at the pinned install) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a local Arty mf48 build report, absent here (763 s) |
| Lint ratchet | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90, no crossbar finding |
| Verilator `capture_coherence` | `make -C tb/verilator/capture_coherence` | 0 | 582 checks in 3 tallies (456 junction + 118 datapath + 8 mutation), 0 failures (366 s) |
| Verilator `chmap_capture` | `make -C tb/verilator/chmap_capture` | 0 | 254 checks + netlist pin 20 checks, 0 failures |
| Verilator `media_grid_align` | `make -C tb/verilator/media_grid_align` | 0 | PASS; its 3 negative controls RED as required |
| Verilator `tdm` | `make -C tb/verilator/tdm` | 0 | 58 checks, 0 failures |
| Verilator `pair_fill` | `make -C tb/verilator/pair_fill` | 0 | 41 checks, 0 failures |
| Verilator `pp_shadow` | `make -C tb/verilator/pp_shadow` | 0 | 2,120 checks in 4 tallies, 0 failures |
| Verilator `milan_dp_render` | `make -C tb/verilator/milan_dp_render` | 0 | 222 checks in 3 tallies (tdm8render 152, multi 65, leg defects 5/5), 0 failures (348 s) |
| Verilator `milan_dp` | `make -C tb/verilator/milan_dp` | 0 | 11,206 checks, 0 failures, 16 tallies (1519 s) |
| Suite tally | `scripts/suite_tally.py` over the 8 suite logs, and `--verdict` per log | 0 | 14,548 checks, 0 in-suite failures |
| Markdown: docs_check | `$MDPY scripts/docs_check.py` | 0 | 0 findings |
| Markdown: em dash | `$MDPY scripts/check_em_dash.py --base ce550952...` and `--selftest` | 0 | PASS |
| Markdown: contents | `$MDPY scripts/gen_toc.py --check`, `--verify-anchors`, `--selftest` | 0 | PASS |
| Markdown: style | `$MDPY scripts/check_doc_style.py` and `--selftest` | 0 | 22 documents OK |
| Markdown: doc paths, feature status, matrix, gptp/solution/submodule docs, DOC_MAP, archive | `$MDPY ...` (see summary file) | 0 | PASS |
| Code quality | sv/cpp/py/sh idiom, hygiene, naming, port contracts, fail-fast, test evidence, TODO ownership, cohesion/control-flow self-tests, each with its `--selftest` | 0 | PASS (test evidence: `capture_coherence` armed, its reader disposition registered) |
| Source lists and scope | rtl source lists, SoC sources, pp_srcs, wire accountability, CI events, ci_scope self-test, bare-metal, NVM record space, diagrams | 0 | PASS |
| HDL reference | `gen_hdl_reference.py --selftest` and `--output <tmp>` (pinned pyslang in a throwaway venv) | 0 | built, crossbar page present |
| Yosys | `syn/yosys/run.sh --top KL_chan_map_capture`, `--top milan_datapath` | 0 | both PASS; tied-input and tap-purity PASS |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, 0 in hdl/ |

Not run: the whole-tree sweep `scripts/run_all_suites.sh` (only the affected suites above were
assigned); the act replica and hosted CI (nothing pushed; this lane may not push).

## 8. Open risks / observations for the manager (no issue filed: this lane may only post on #617)

- CRF lock at the frame-close crossing: under CRF the aligner parks the slot-0 marker at its
  engagement phase, kept 1/128 sample off the TICK. The new crossing that decides a column is the
  frame close (pair 3) against the walk snapshot (tick + LB_PAIRS_C + 3). An engagement that lands
  within the lock's dither (a few cycles) of that crossing would alternate repeat/skip until
  re-engagement. Pre-existing and reduced: the per-pair holds had one such crossing per pair
  (four); now there is one. Not hit by the 16+8+8 CRF phases simulated. A follow-up could key the
  aligner's keep-off on the frame close.
- Arty blend shapes: the crossbar's 4-pair TDM bucket keeps slot 0 (I2S) and TDM pairs 0..2;
  TDM pair 3 (blend slot 4) was already unreachable through the crossbar before this change.
- The I2S bucket (`i2s_hold_r`) is still written by every front-end strobe (all slots), as at
  ce550952; unchanged.

## 9. Log

- 17:00 CEST: confirmed origin and HEAD ce550952; read #617, PR #616 findings "DIN frame
  coherence", R392-1.
- 17:02 posted TAKEN.
- 17:30 junction harness first; fails at ce550952 (reproduction). RTL fix. Junction leg passes.
- 17:40 datapath leg; fails at ce550952, passes at the fix.
- 17:50 mutants.py 8/8.
- 17:55 chmap_capture updated ([F], whole frames, lane B one-pair frame): 254/0.
- 18:00 docs, matrix regeneration, evidence registration, resources.
- 18:05 committed d8034466, 964a45b6, 5546b976 (one-line subjects, no body, no trailers).
- 18:10-19:05 gates at 5546b976: 78 entries, all rc 0 (section 7); ce550952 re-runs with the
  final harness recorded (section 1).
- 19:07 posted REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5874747373
- Stopped here: no push, no PR, no further comment (lane contract).
