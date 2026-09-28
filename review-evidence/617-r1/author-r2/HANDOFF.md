# [A428] Round 2 handoff: issue #617 / PR #618

Status: REVIEW READY at `377d1ac3658feb8d544e6ed1005b186b67127f35` (local branch, not pushed; this lane may not push). All 79 assigned local gates rc 0 at that head.

- Repository: kebag-logic/milan-fpga, origin `https://github.com/kebag-logic/milan-fpga.git`.
- Lane: `$LANES/617-capture-frame-atomic`, branch `617-capture-frame-atomic`.
- Round-2 start: `5546b976161bdfd0611040160df44806a0b95d15`. Branch base: dev `ce550952e47fbd92367f0d9b099345100f7f4215`.
- Head: `377d1ac3658feb8d544e6ed1005b186b67127f35`, three round-2 commits on `5546b976`:
  - `28e34a784` Guard the capture walk's TDM crossing under CRF and count the walk's own slips (RTL).
  - `db37da036` Sweep CRF engagement through the capture crossing and pin the one-pair frame (tests).
  - `377d1ac36` Document the guarded capture crossing and the exact per-pair capture latency (docs).
- Earlier local heads of these same three commits (never pushed):
  - `59c78ab5`: its first gate run found milan_dp's 2 MHz elaboration refusing the fixed 256-cycle keep-off (section 2).
  - `ec0f046b`: 79 of 79 gates rc 0; replaced only to make one documented number measured (section 7).
- Assignment: issue #617 comment 5875511547 (round 2) and the CRF-band ruling 5875206178.
- Reviews answered: R394-1 (PR #618 comment 5875199285) and R395-1 (PR #618 comment 5875505042).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5875526464
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5879271133
- Roles: executor [A428]; internal reviewer [R394]; external reviewer [R395].
- Simulator: Verilator 5.050 (the CI pin), `$VALIDATION_TOOLS/verilator-v5.050/bin` first on PATH, for every run below.
- Synthesis: Yosys 0.66, sv2v v0.0.13 (CI pins v0.0.12).

## 1. Defect reproduction at ce550952 (torn-state table)

Method: the committed round-2 harness, built against the RTL of `ce550952`.

- A scratch tree outside the lane: `git archive` of the head.
- `KL_chan_map_capture.sv` and `milan_datapath.sv` replaced by `git show ce550952:<path>`.
- The junction wrapper's aligner binding set back to `ce550952`'s: slot-0 marker, the tick itself, the default keep-off. Its `TDM_FRAME_PAIRS_P` line was dropped, because the base crossbar has no such parameter.
- The datapath leg's placement tap read the base's pair-3 hold (`tdm_hold_r[3]`), which changes at the same strobe as the frame close, because the base has no frame bank.
- These are probe-only edits in the scratch tree; nothing was committed.

Result at `ce550952`:

- Junction leg: 386 of 5,240 checks fail (log `evidence/base-ce550952-junction.log`).
- Datapath leg: 7 of 311 fail (`evidence/base-ce550952-dp.log`).

INT-true (the true 391/1591 plan, fsync -10.64 ppm, one whole beat, 1x1 TDM8, 50 MHz, INTERNAL), frame offset of pairs 1..3 against pair 0:

| Offset of pairs 1, 2, 3 | `ce550952` columns | Share | #451 bench share | Meaning |
|---|---:|---:|---:|---|
| 0, 0, 0 | 32,544 | 33.9% | 32.5% | coherent |
| -1, -1, -1 | 21,152 | 22.0% | 22.2% | pairs 1 to 3 one frame older |
| 0, -1, -1 | 21,152 | 22.0% | 22.7% | pairs 2 and 3 one frame older |
| 0, 0, -1 | 21,152 | 22.0% | 22.7% | pair 3 one frame older |
| total torn | 63,456 of 96,000 | 66.1% | 67.5% | |

The same four states and shares that round 1 and both reviewers measured.

| Scenario at `ce550952` | Torn columns | Notes |
|---|---:|---|
| INT-slow (-1000 ppm, 3.2 beats) | 2,160 / 3,204 (67.4%) | same four states |
| INT-fast (+1000 ppm, 3.2 beats) | 2,025 / 3,204 (63.2%) | |
| CRF-true-01 | 1,307 / 2,004 (65.2%) | settles across a boundary |
| CRF-true-02 .. -11 | 100% each | a lock in a torn region tears every column |
| CRF-true-00, -12 .. -15 | 0 | a lock in the coherent region |
| CRF-50-0 / -1 / -2 / -3 | 90.9% / 100% / 100% / 0 | 9,000 columns each |
| CRF+50-0 / -1 / -2 / -3 | 0 / 100% / 100% / 90.6% | |
| CRF-frame-true (65 placed phases) | 45 phases torn, 87,856 columns | |
| CRF-band-50 / CRF-band+50 (53 each) | 23 phases torn each | |
| DP-INT-slow / DP-INT-fast | 1,483 / 2,202 (67.3%); 1,350 / 2,202 (61.3%) | whole `milan_datapath` |
| DP-CRF-1 .. -5 | 100% each | |

Base minimum sample ages at the tick (INT-true), pairs 0..3: -6, -32, -58, -84 axis cycles: pair p's strobe was read up to tick + 6 + 26p (section 3).

The round-2 defect at the round-1 head. The same harness against `5546b976`'s crossbar, datapath and aligner binding (slot-0 marker, the tick itself, the default keep-off):

- Junction leg: 414 of 5,240 fail (`evidence/r1-5546b976-junction.log`).
- Datapath leg: 25 of 311 fail (`evidence/r1-5546b976-dp.log`).

| Sweep at `5546b976` | Phases | With slips | Repeats / skips | Tail slips (the band) |
|---|---:|---:|---:|---:|
| CRF-band-true | 65 | 19 | 483 / 464 | 8 phases |
| CRF-frame-true | 65 | 1 | 20 / 19 | 0 |
| CRF-band-50 | 53 | 36 | 320 / 284 | 10 phases |
| CRF-band+50 | 53 | 37 | 324 / 359 | 10 phases |
| DP-band-true (whole datapath) | 13 | 7 | 144 / 137 | 4 phases; `SLIP_TDM` missed all 7 |

This is R394-1 F1 and R395-1 F1 reproduced by the committed sweep: the lock sits on the frame-close/snapshot crossing and repeats and skips frames, while `SLIP_TDM` reads static. The INTERNAL scenarios there also fail the new exact checks:

- `[W] walks newer than the frame their tick takes`: the round-1 snapshot read closes up to tick + 5.
- `[C] walks whose repeat or skip the junction counters did not count`: the round-1 counters keyed on slot 0.

## 2. Design (file:line at the head)

The round-1 handoff stays: STAGE, FRAME, WALK. Round 2 guards the one crossing it created.

Files: `hdl/ieee1722/aaf/KL_chan_map_capture.sv` (crossbar), `hdl/milan/milan_datapath.sv` (aligner binding).

Crossbar, `KL_chan_map_capture.sv`:

- Banner `TDM FRAME HANDOFF (#617)` `:63`, `ONE CROSSING` `:89`, `LATENCY` `:100`.
- Unchanged from round 1:
  - `TDM_FRAME_PAIRS_P` `:331`, guard `g_tdm_frame_guard` `:535-538`;
  - close `tdm_close_w` `:558`;
  - STAGE/FRAME `source_latch` `:561-580`.
- Snapshot instant: `tdm_snap_w` `:971`.
  - The media tick's own cycle when the walk is idle.
  - A tick queued behind an overrunning walk snapshots at that walk's start (`tick_late_r` `:810`, set `:1197`).
  - Was: the pre-walk's last cycle, tick + `LB_PAIRS_C` + 2.
- TDM junction counters moved beside the snapshot, `tdm_slip_count` `:974-1039`.
  - Marker = `tdm_close_w`, the publish; consume = `tdm_snap_w`.
  - The #74 law itself is unchanged, including the coincidence carry-over.
  - Was: the slot-0 write against `tick_i`.
- WALK with the coincidence law, `tdm_walk_snapshot` `:1053-1068`, `tdm_snap_take_w` `:1055`.
  - A close landing on the snapshot's own cycle with no frame pending is the frame the counters say the tick takes.
  - The walk bank then loads one cycle late to take it; the slot walk first reads the bank after the `LB_PAIRS_C` + 1-cycle pre-walk.
  - So the walk and the counters count one crossing, exactly.
- Resolver reads WALK only, `:1094` (unchanged).

Aligner binding, `milan_datapath.sv` (`:5658` banner, `:5706-5724`):

- `frame_ev_i` = the frame close: `aafcap_pv_w && aafcap_slot_w == CMAP_TDM_FRAME_PAIRS_C - 1` (`:5722`).
  - Was the slot-0 strobe; on I2S shapes the frame is one pair, so it still is.
- `tick_i` = `media_tick_q_r`, `media_tick_p` one cycle late (`mga_tick_delay` `:5710`, bound `:5724`).
  - The aligner pulls a capture just before its tick early and one on it late.
  - With the tick one cycle late, that split is the walk's crossing, so no engagement is pulled across it.
- `LOCK_KEEPOFF_CYC_P` = `MGA_KEEPOFF_CYC_C` = min(256, a quarter sample) (`:5706-5708`).
  - 256 at 50 MHz and at 100 MHz.
  - About 10 on milan_dp's 2 MHz compressed-clock gPTP legs, where 256 leaves no lock target and the aligner's own elaboration guard refused it (found by the first gate run at `59c78ab5`, fixed before the gates below).

Why 256 and not the 1/128-sample default (8 cycles at 50 MHz):

- The default guards a settled lock, but the loop's acquisition transient moves the close before the lock settles.
- MEASURED by the committed harness (`CRF-50-1/2`, `CRF+50-1/2`, engagements the keep-off does not pull): 149 cycles at +/-50 ppm (Milan v1.2 7.4's media clock tolerance). The furthest point is at column 7,067 to 7,145 of a 9,000-column run, after which the close returns, so this is the peak. On the true plan the close moves 18 cycles within 2,000 frames and is still moving there.
- A loop model matches the harness's tail spreads (8 cycles true plan, 39 cycles at +/-50 ppm) and gives about 32 cycles peak on the true plan and 178 to 197 cycles at +/-60 ppm.
- Probe evidence at an intermediate RTL (marker = close, snapshot at the tick, before the walk's coincidence law; throwaway sweeps, logs not kept in the tree), CRF junction:

| Keep-off | True plan, 261 phases, 2,000 cols | -50 ppm, 131 phases, 6,000 cols | +50 ppm, 131 phases, 6,000 cols |
|---|---|---|---|
| default (8 cycles) | 2 tail-slip, 5 with slips | 5 tail-slip, 18 with slips | 5 tail-slip, 19 with slips |
| 256 cycles | 0 | 0 | 0 |

- The committed mutation arm keeps this measurable: the default keep-off, restored in the wrapper, fails `[C] slips while the CRF lock held` (section 5).

Engagement cost of the 256-cycle keep-off (the lock itself is unchanged):

- A capture within 256 cycles of the (delayed) tick is pulled out to 256 at up to 64 ppm of NCO trim (u = 4 x err at 1/16 ppm per LSB).
- That is half of engagements at 50 MHz, a quarter at 100 MHz.
- The #386 settled-grid trigger waits for that pull as for any aligner movement; its 32,768-tick ceiling still bounds it.
  - PROBE (the head's datapath leg in a scratch copy, 40,000 columns, true plan, 50 MHz; not committed): the recentre fired 682.7 ms after the CRF selection for an engagement placed on the crossing (fully pulled; that is the ceiling). It fired 486.9 ms after for one placed 400 cycles away (not pulled; the true-plan transient itself keeps the error outside the 1/64-sample band that long).
  - The pull therefore costs about 196 ms of recentre delay at worst, inside the existing bound.
- Render side: `milan_dp_render` T30 and `milan_dp aclk` pass unchanged.
  - T30's CRF window: commit-to-pin 1175..1178 cycles, walk -0.5339 ppm at the head; 1174..1177 cycles, -0.8009 ppm with the round-1 binding (same lock, one cycle later; a different loop residual).
  - `TIME_SYNC.md`'s CRF walk row now carries -0.5339 ppm, and the old value beside it.

Unchanged:

- the render (DOUT) path RTL;
- the channel-map semantics;
- every port of `KL_chan_map_capture` and `milan_datapath`;
- `KL_media_grid_align.sv` itself (its binding and a parameter only);
- the processor and the firmware.

## 3. Latency effect against TIME_SYNC.md

Deterministic per-pair change against `ce550952` (sample age at the walk's tick, 1x1 TDM8, 50 MHz), re-derived:

- `ce550952` read pair p at slot p's inject: a pair-p strobe was read up to tick + 6 + 26p.
  - The tick is consumed a cycle after it, and the pre-walk takes `LB_PAIRS_C` + 1 = 5 cycles.
  - Slot 0 reads in cycle tick + 7, and each later slot 26 cycles (`GAP_CYC_P` + 2) after the one before.
- Round 1 read a close up to tick + 5 (the pre-walk's last cycle).
- The head reads a close up to the tick cycle itself (the coincidence law; tick - 1 only when a frame is already pending).
- Pair p's strobe comes (3 - p) pair periods before its frame's close; a TDM8 pair period is 64 bit clocks = 5.2084 us = 260.42 cycles at 50 MHz.

| Pair | Frame atomicity (round 1) | Guarded crossing (round 2) | Change against `ce550952` |
|---|---|---|---|
| 0 | 1 + 0 + 3 x 260.42 = 782.3 cycles, 15.65 us | +5 cycles | 787.3 cycles, 15.75 us |
| 1 | 1 + 26 + 2 x 260.42 = 547.8 cycles, 10.96 us | +5 cycles | 552.8 cycles, 11.06 us |
| 2 | 1 + 52 + 1 x 260.42 = 313.4 cycles, 6.27 us | +5 cycles | 318.4 cycles, 6.37 us |
| 3 | 1 + 78 + 0 = 79.0 cycles, 1.58 us | +5 cycles | 84.0 cycles, 1.68 us |

- The round-1 column is R395-1 F3's figure, re-derived identically.
- The round-2 column is the read moving from tick + 5 to the tick: `LB_PAIRS_C` + 1 cycles, 5 on the 1x1 shape (0.1 us), 2 on the 8x8 product shape (loop lane off, `LB_PAIRS_C` = 1).
- It is what makes the crossing coincide with the aligner's split. It is not a sample.
- Check, MEASURED (INT-true minimum pair ages, pairs 0..3):
  - `ce550952`: -6, -32, -58, -84.
  - Head: 781, 520, 260, 0.
  - Differences 787, 552, 318, 84, matching the table to the quantization of 260.42.
  - Maxima: 1035/1009/983/957 at the base, 1823/1563/1302/1042 at the head.
- Frame age at the tick:
  - INTERNAL: 0 to 1,042 cycles, uniform over a beat (was -5 to 1036 in round 1).
  - CRF: 256 to 785 cycles, fixed for a lock (the aligner keeps the close 256 cycles from the crossing).
- `TIME_SYNC.md` "Talker capture handoff" (the section, its latency table and a new "The guarded crossing" subsection) now tables this.
  - The sampled-mean table (787.7/558.2/328.7/99.1) is gone, and the pair-3 sentence now says the read moves to the tick.
  - `CHANGELOG.md` states "Pair delay grows by 1.68 to 15.75 us".
  - The phrase "+2 to +16 us" did not occur in `CHANGELOG.md` at `5546b976` (grep); it came from the PR body's mean table, which the PR-BODY round-2 section corrects.
- Arty blend shapes (R395-1 S1): the I2S pair is bucket pair 0 there and is published with the TDM close, up to a frame after its own strobe. `TIME_SYNC.md` says so.
- The listener render tables are unchanged. The render path does not pass through `KL_chan_map_capture`. Section 2 covers the aligner's effect on the render side.
- `docs/AAF_LATENCY_TAPS.md`: TX0 CAP is the front-end strobe, before the crossbar. D0 (CAP to PKT_SOF) moves by the same per-pair change and stays inside its 6-sample window envelope. Not edited.

## 4. Simulation table (INTERNAL and CRF, drift cases, dense CRF sweep)

Suite `tb/verilator/capture_coherence`, `make` = junction leg, datapath leg, mutation arm. At the head (gate run, section 7): junction 5,240 checks, 0 failures; datapath 311 checks, 0 failures; mutation arm 19 of 19; rc 0 in 928 s.

Checks per scenario:

- `[A]`: tags, L/R split, columns mixing two TDM frames.
- `[W]`: walks torn; walks older or newer than the frame their tick takes, which is now the exact handoff law.
- `[C]`: continuity steps. INTERNAL: slip clusters netting one frame in the drift direction. CRF: net-zero slips only inside the first 64 columns, and no tail slip. The junction counters against each walk's own repeat or skip, walk by walk.
- `[V]`: pattern, columns decoded, INTERNAL phase bins and counter activity, CRF engagement and lock, each placed engagement within 2 cycles of its placement, and each sweep window covered with no gap wider than its step + 2.

Placement: each CRF sweep calibrates where the first close lands against its tick with the TDM clock unheld. It then holds the TDM clock 4 steps per cycle of offset: 0 = the close on the tick cycle, positive = after it.

| Scenario | Source | TDM plan | Columns | `ce550952` | `5546b976` (round 1) | Head |
|---|---|---|---:|---|---|---|
| INT-true | INTERNAL | true 391/1591, one whole beat | 96,000 | 66.1% torn | 0 torn; `[W]`/`[C]` exact-law failures | 0 torn; one slip, counted once (round 1 chattered 21 repeats / 20 skips) |
| INT-slow / INT-fast | INTERNAL | -1000 / +1000 ppm, 3.2 beats | 3,200 | 67.4% / 63.2% torn | 0 torn | 0 torn; 3 / 4 slips, each counted exactly |
| CRF-true-00..15 | CRF | true plan, 16 held offsets | 2,000 | 100% torn in 10, 65% in 1 | 0 torn, 0 slips | 0 torn, 0 slips |
| CRF-50/+50-0..3 | CRF | +/-50 ppm, 4 offsets | 9,000 | 90-100% torn in 6 of 8 | 0 torn | 0 torn, 0 slips; unpulled close moves 149 cycles, furthest at column 7,067-7,145 |
| CRF-band-true | CRF | true plan, every cycle -32..+32 | 2,000 | 0 torn (the per-pair crossings sit elsewhere) | 19 phases slip, 8 in the tail | 0 torn; no tail slip; 1 phase (engaged on the crossing) repeats and skips once, net zero |
| CRF-frame-true | CRF | true plan, every 16 cycles, whole frame | 2,000 | 45 phases torn | 1 phase slips | 0 torn, 0 slips |
| CRF-band-50 | CRF | -50 ppm, every 4 cycles -176..+32 | 6,000 | 23 phases torn | 36 phases slip, 10 in the tail | 0 torn, 0 slips |
| CRF-band+50 | CRF | +50 ppm, every 4 cycles -32..+176 | 6,000 | 23 phases torn | 37 phases slip, 10 in the tail | 0 torn, 0 slips |
| DP-INT-slow / -fast | INTERNAL | +/-1000 ppm, whole datapath | 2,200 | 67.3% / 61.3% torn | 0 torn | 0 torn |
| DP-CRF-0..7 | CRF | true plan, 8 held offsets | 1,500 | 100% torn in 5 | 0 torn | 0 torn, 0 slips, `SLIP_TDM` 0/0 |
| DP-band-true | CRF | true plan, every 2 cycles -20..+4 | 1,500 | 0 torn | 7 phases slip, 4 in the tail; `SLIP_TDM` missed them | 0 torn, 0 slips, `SLIP_TDM` 0/0 |

Placement coverage at the head: CRF-band-true landed -32..+33 (widest gap 2 cycles); CRF-frame-true -512..+512 (17); CRF-band-50 -177..+32 (5); CRF-band+50 -32..+178 (6); DP-band-true -21..+3 (2). Every window passed its coverage check.

The CRF law in `[C]` is stricter than the round-1 CRF grading, not weaker:

- Round 1 applied its two INTERNAL drift-cluster checks to CRF runs too. They accepted any acquisition cluster netting one frame in the plan's direction; round 1's CRF+50-0 had 6 repeats and 7 skips and passed.
- Under CRF there is no drift for a cluster to net. The CRF law allows only a net-zero pair inside the first 64 columns (an engagement on the crossing). Every other CRF scenario must have zero slips anywhere, not only in the tail.

Of the 281 CRF scenarios at the head (260 junction, 21 datapath), exactly one slipped: CRF-band-true+0, engaged on the crossing itself, with 1 repeat and 1 skip, net zero, inside the first columns.

`tb/verilator/chmap_capture` (R395-1 F2 and the coincidence law at L0): 318 checks + netlist pin 20 checks, 0 failures at the head (254 + 20 in round 1).

- `[T0]` re-keyed to the frame close (pair 3 of lane A's frame) against the snapshot. Same expected counts; "pairs before the closing one are not frame markers".
- `[F]` gains a second PDU, one right answer per column:
  - a close on the tick cycle with nothing pending is that walk's;
  - with one pending, the pending frame is taken and the coincident one waits;
  - the junction counters move 0 across the PDU.
- `[F1]` (new, lane B, `TDM_FRAME_PAIRS_P = 1`): pair 0 driven alone, a fresh value per walk; each of six columns must carry its own frame. RM1 fails it (section 5).
- `[SAT]` feeds the TDM half through the closing pair.

## 5. Mutant table

`python3 mutants.py` (the suite's `mutants` target). Five legs, each with a clean control, 14 mutants. At the head (gate run): 19 checks, 19 PASS, 0 FAIL.

| # | Leg (mode) | Mutant | Named check that must fail |
|---|---|---|---|
| C1-C5 | junction `--quick`, band `--band`, dp `--quick`, dp-band `--band`, chmap | clean controls | none |
| M1 | junction | the walk reads the per-pair stage (the `ce550952` law, the removed-atomicity mutant) | `[A] AAF columns mixing two TDM frames` and `[W] walks reading two TDM frames` |
| M2 | junction | no walk snapshot | `[A]` torn |
| M3 | junction | frame closed by its first pair | `[A]` torn |
| M4 | junction | published whole but one pair late | `[W] walks older than the frame their tick takes` |
| M5 | junction | stage never written | `[V] every requested column was decoded` |
| M6 | junction | the walk ignores the coincidence law (no late load) | `[C] walks whose repeat or skip the junction counters did not count` and `[W] walks older than the frame their tick takes` |
| M7 | junction | snapshot back on the pre-walk's last cycle (the round-1 instant) | `[W] walks newer than the frame their tick takes` |
| M8 | junction | counters keyed on the slot-0 write against the tick (the round-1 law) | `[C] walks whose repeat or skip the junction counters did not count` |
| M9 | band (wrapper) | the round-1 aligner binding: slot-0 marker, the tick itself, the default keep-off (the guard removed) | `[C] slips while the CRF lock held` |
| M10 | band (wrapper) | keep-off back to the 1/128-sample default | `[C] slips while the CRF lock held` |
| M11 | band (wrapper) | the aligner sees the tick itself | `[C] CRF slips net zero` |
| M12 | dp | `milan_datapath` tells the crossbar a one-pair frame | `[A]` torn |
| M13 | dp-band | `milan_datapath`'s round-1 aligner binding (the guard removed) | `[C] slips while the CRF lock held` |
| M14 | chmap | RM1: the frame closes on the bucket's last pair whatever the frame length | `F1: col 0 carries its own pair-0 frame (L)` |

- M9 and M13 are the ruling's "a mutant that removes the new guard reproduces the band". M13 is on the real datapath binding.
- M14 is R395-1 F2's RM1 class, killed by a named check.
- Per-leg evidence before committing:
  - M9 --band: 17 net-zero failures and 7 tail slips.
  - M10: 42 failures.
  - M11: 1 (the engagement on the crossing is pulled across).
  - M13: 3 tail-slip phases and 7 net-zero failures.

## 6. Resource comparison

`KL_chan_map_capture` alone, the `syn/yosys/ooc.sh` recipe (sv2v, `synth_xilinx -family xc7 -flatten`, stat), Yosys 0.66, sv2v v0.0.13. The head row is `ooc.sh` itself; the other rows replay its recipe on `git show <rev>:` copies, and the recipe reproduces `ooc.sh`'s head row exactly.

| Shape | Version | LUT | LUTRAM | FF | BRAM | CARRY4 |
|---|---|---:|---:|---:|---:|---:|
| 1x1 TDM8 (`N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8`) | `ce550952` | 1292 | 32 | 1048 | 0 | 34 |
| 1x1 TDM8 | `5546b976` (round 1) | 1263 | 32 | 1384 | 0 | 34 |
| 1x1 TDM8 | head | 1265 | 32 | 1384 | 0 | 34 |
| 8x8 product, loop lane off (`N_SLOTS_P=32 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=2`) | `ce550952` | 2062 | 32 | 1595 | 0 | 34 |
| 8x8 | `5546b976` | 2103 | 32 | 1931 | 0 | 34 |
| 8x8 | head | 2132 | 32 | 1931 | 0 | 34 |

- Round 2 against round 1: LUT +2 (1x1) and +29 (8x8), FF +0 in both.
- The late-tick flag and the one-cycle late-load flag are two flops; synthesis finds no net FF change. The +29 LUT at 8x8 is the snapshot and late-load decode, within the mapping noise the ooc README warns about.
- `milan_datapath` adds one flop (`media_tick_q_r`); the keep-off is a parameter.
- The in-context datapath delta and placed Vivado utilization are not measured, as in round 1.

## 7. Gate table

All at head `377d1ac3658feb8d544e6ed1005b186b67127f35`:

- The tree was clean (`git status --porcelain` empty before and after), with the suite build directories cleaned first.
- Every gate ran from the physical path `$LANES/617-capture-frame-atomic`, unpiped, with its log and exit status written to files.
- Commands that outran one tool call were waited for; two streams ran side by side (milan_dp alone in one).
- Markdown gates used the pinned environment `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`. The HDL reference used a throwaway venv built from `tools/hdl_reference/requirements.txt` (pyslang 11.0.0, hash-locked).
- `GIT_CONFIG_*` set core.commitGraph=false for every gate, as in round 1, because this worktree's git prints a commit-graph warning on stderr.
- Full list with each command: `evidence/gate-summary-377d1ac3.txt` (79 entries, all rc 0).

| Gate | Command | rc | Result |
|---|---|---:|---|
| Builder bank | `python3 sw/builder/test_builder.py --require-rv32` (RV32 cross compiler found at its pinned home location) | 0 | ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs a local Arty mf48 build report, absent here (689 s) |
| Lint ratchet | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| Verilator `capture_coherence` | `make -C tb/verilator/capture_coherence` | 0 | 5,570 checks in 3 tallies (5,240 junction + 311 datapath + 19 mutation), 0 failures (928 s) |
| Verilator `chmap_capture` | `make -C tb/verilator/chmap_capture` | 0 | 318 checks + netlist pin 20, 0 failures |
| Verilator `media_grid_align` | `make -C tb/verilator/media_grid_align` | 0 | 45 checks, 0 failures; its negative controls red as required (172 s) |
| Verilator `tdm` | `make -C tb/verilator/tdm` | 0 | 58 checks, 0 failures |
| Verilator `pair_fill` | `make -C tb/verilator/pair_fill` | 0 | 41 checks, 0 failures |
| Verilator `pp_shadow` | `make -C tb/verilator/pp_shadow` | 0 | 2,120 checks in 4 tallies, 0 failures |
| Verilator `milan_dp_render` | `make -C tb/verilator/milan_dp_render` | 0 | 222 checks in 3 tallies, 0 failures (322 s) |
| Verilator `milan_dp` | `make -C tb/verilator/milan_dp` | 0 | 11,206 checks in 16 tallies, 0 failures (1,407 s) |
| Suite tally | `scripts/suite_tally.py` over the 8 suite logs, and `--verdict` per log | 0 | 19,600 checks, 0 in-suite failures |
| Markdown | `docs_check`, `check_em_dash --base ce550952...` and `--selftest`, `gen_toc --check/--verify-anchors/--selftest`, `check_doc_style` and `--selftest`, `check_doc_paths`, `check_feature_status` and `--self-test`, `gen_module_matrix --check`, gptp/solution/submodule docs, `DOC_MAP.gen --check`, `check_archive` | 0 | PASS (doc style: 22 current documents OK) |
| Code quality | sv/cpp/py/sh idiom, hygiene, naming, port contracts, fail-fast, test evidence, TODO ownership, cohesion/control-flow self-tests, each with its `--selftest` | 0 | PASS |
| Source lists and scope | rtl source lists, SoC sources, `pp_srcs`, wire accountability, CI events, ci_scope self-test, bare-metal, NVM record space, diagrams | 0 | PASS |
| HDL reference | `gen_hdl_reference.py --output <tmp>` and `--selftest` | 0 | built |
| Yosys | `syn/yosys/run.sh --top KL_chan_map_capture`, `--top milan_datapath` | 0 | both PASS |
| OOC | `OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture` | 0 | LUT 1265, LUTRAM 32, FF 1384, BRAM 0 |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, 0 in `hdl/` (Vivado present) |

History of the gate runs:

- `59c78ab5`: the fixed 256-cycle keep-off failed milan_dp's 2 MHz gPTP elaboration (the aligner's own guard); the cap was added.
- `ec0f046b`: 79 of 79 rc 0.
- `377d1ac3` differs from `ec0f046b` only in `TIME_SYNC.md`, `REGISTER_MAP.md` and the junction harness's printed "furthest at column". That made the 149-cycle transient peak a measured statement. The full bank was rerun.

Not run:

- the whole-tree sweep `scripts/run_all_suites.sh` (only the affected suites were assigned);
- the act replica and hosted CI (nothing pushed; this lane may not push);
- bench acceptance 4.

Local sv2v is v0.0.13; CI pins v0.0.12.

## 8. Round-2 finding disposition

| Finding | Disposition | Where |
|---|---|---|
| R394-1 F1 = R395-1 F1 (CRF repeat/skip band at the close/snapshot crossing) | FIXED in RTL per the ruling | section 2; sweeps section 4; mutants M9, M13 |
| | The crossing is guarded: the aligner keys on the close, sees the tick one cycle late, keep-off 256 | |
| | The counters count exactly the walk's slips | |
| | Dense committed sweeps pass at every phase | |
| | Suite comments state the coverage | `sim_main.cpp` header, `sim_dp.cpp` header, `Makefile` header |
| | Docs state the guarded crossing | `TIME_SYNC.md` "The guarded crossing", `REGISTER_MAP.md` SLIP_TDM paragraph and reading table |
| | No redesign of `KL_media_grid_align` was needed: its binding and a parameter only | |
| R395-1 F2 (one-pair frame not load-bearing) | FIXED | `chmap_capture` `[F1]`; mutant M14 |
| R395-1 F3 = R394-1 S1 (latency table) | FIXED: the deterministic per-pair change, re-derived and extended by the guard's 5 cycles; pair-3 sentence corrected; `CHANGELOG.md` states the range | section 3 |
| R394-1 S2, R395-1 S3 (slot-0 counters and marker notes) | TAKEN | counter banner, `sim_main.cpp` header, `media_grid_align_wrap.sv` comment, `REGISTER_MAP.md` |
| | The counters and the aligner no longer key on slot 0 | |
| | Staged-since-close bits (S2's optional idea) were not added: every front end restarts at slot 0 and re-stages before the next close | |
| R395-1 S1 (Arty blend I2S latency note) | TAKEN | `TIME_SYNC.md` |
| R395-1 S2 (stale `tdm_hold_r` name) | TAKEN | `tb/verilator/milan_dp/sim_nxn.cpp` comment now names the port the check reads |

## 9. Open risks

- An engagement whose close lands exactly on the crossing (the tick cycle) can repeat and skip one frame while the aligner's pull clears the close's one-cycle jitter.
  - It is net zero, within 64 columns, counted on `SLIP_TDM`, and documented. It is 1 of 256 simulated CRF engagements.
  - No lock phase slips.
- The 256-cycle keep-off changes #74's engagement behaviour for half of engagements at 50 MHz: a pull of up to a quarter sample at up to 64 ppm of NCO trim, and a later #386 render recentre, bounded by its 32,768-tick ceiling.
  - `milan_dp aclk` and `milan_dp_render` T30 pass unchanged, but the settle time of a maximally pulled engagement is not measured separately.
  - The `KL_media_grid_align.sv` banner's sentence "a raced one is pulled at most the keep-off, 1/128 sample by default ... so a raced engagement starts inside [the settle band]" holds for the module default, not for the datapath instance. The module file was not edited; the datapath banner and `TIME_SYNC.md` state the instance's behaviour.
- The guarantee covers sources within about +/-75 ppm (the transient scales about 3.3 cycles per ppm). Beyond that, an engagement near the crossing can still slip during acquisition.
  - The aligner's authority is +/-200 ppm; Milan v1.2 7.4 bounds media clock sources at +/-50 ppm.
- Suite run time grows. `capture_coherence` now runs about 15 minutes locally (junction 2.7 min, datapath 1.8 min, mutation arm about 10 min), against 6 minutes in round 1. It stays inside run_all_suites' 1,800-second per-suite guard, but lengthens its CI shard.
- On the Arty blend shapes TDM pair 3 remains unreachable through the crossbar (unchanged from round 1).
- Not run: the whole-tree sweep, the act replica and hosted CI (nothing is pushed), and bench acceptance 4.
- The optional test-evidence ratchet lowering (77 to 75) was left for a separate change.

## 10. Log (2026-09-28, CEST)

- 19:52: confirmed origin and HEAD `5546b976`. Read #617 in full (round-1 assignment, ruling, round-2 assignment) and R394-1 / R395-1. Posted TAKEN.
- 20:10-21:00: modelled the aligner's PI transient. Probed two guard designs with a throwaway CRF sweep (section 2 table). Checked `milan_dp_render` and `milan_dp aclk` against the wide keep-off (both pass unchanged).
- 21:00-21:40: found that the walk and the #74 counters disagree at coincidence. Added the walk's late load, the delayed aligner tick, the calibrated placed sweeps, the CRF law, the per-walk counter check, the dp band, and the chmap `[F]` coincidence PDU and `[F1]`. Wrote the 14-mutant arm (19/19).
- 21:40-21:50: docs (`TIME_SYNC.md`, `REGISTER_MAP.md`, `CHANNEL_MAP_64.md`, `FPGA_DESIGN.md`, `TESTING.md`, `CHANGELOG.md`), OOC area, lint, fast gates. Committed.
- 21:52: first gate run at `59c78ab5`: milan_dp's 2 MHz gPTP elaboration refused the fixed keep-off. Capped it at a quarter sample and re-committed.
- 21:59-22:47: gate run at `ec0f046b`, 79/79 rc 0. Base (`ce550952`) and round-1 (`5546b976`) reproductions ran in scratch trees, and the #386 settle probe.
- 22:47-23:40: made the 149-cycle peak a measured statement (junction prints the furthest column), re-committed as `377d1ac3`, reran all 79 gates: rc 0. Suite tally 19,600 checks, 0 failures.
- 23:45: posted REVIEW READY (https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5879271133). Stopped: no push, no PR edit, no other comment.

