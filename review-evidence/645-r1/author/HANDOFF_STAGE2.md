# #645 / #647 implementation lane (stage 2): [A531] handoff

Status: **STOP** at head `ff6b28b0f56656271a61c7b3a075046922441366`. The
ruled option C is implemented, tested and documented. One ruled acceptance
does not hold: with the rare arrival-lateness tail, the loopback ring still
slips once after the settle recentre at 2 of 16 set phases (section 4.3).
That needs a ruling (section 8). Two failures in the render mutation
campaign predate this change and are out of its scope (section 4.8).

- Branch: `645-ring-slip`, on stage 1's head `6ca6d6686a69f2b053652149d21af63987479b4b`
  (dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`, processor pin `631eeb34`)
- Ruling implemented: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394
- Stage-1 handoff (diagnosis, options, area prototypes): `HANDOFF_STAGE1.md`
- Executor [A531]; reviewers [R474] (internal), [R475] (external)
- Local and not pushed. STOP posted: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985966478

## Contents

1. What the ruling asks, and how this lane reads it
2. The RTL change
3. Tests
4. Results
5. Area
6. Documentation
7. Gates
8. The open finding, its options and the recommendation
9. Reproduction commands and evidence

## 1. What the ruling asks, and how this lane reads it

Three readings are material. Each is stated in the PR body and in the STOP.

1. **Two recentres per switch, not one moved.** Ruling 1 says "the
   post-switch recentre fires once the servo has reported LOCKED for 8
   consecutive windows", and ruling 3 says "keep the existing at-switch
   #386 render recentre as it is. Add no second recentre at the switch."
   Read together: the #386 trigger is unchanged (it still fires about 43 ms
   after a switch, to the render stage only, with its 32,768-tick ceiling),
   and a new **settle recentre** follows it once the plane has settled, to
   both rings, with the ruled 2^20-tick ceiling. Moving the #386 recentre
   instead would also have turned T30 CRF red: that bench has no servo
   plant, never reads LOCKED, and grades one recentre within 120 ms of the
   CRF selection, against the ruling's "T30 stays green".
2. **The loopback ring's recentre input is an internal port.** Option C as
   ruled sends the pulse to the loopback ring, which needs one input on
   `KL_chan_map_capture` (`lb_recentre_i`, defaulted `'0` like
   `lb_flush_i`, so no other instance changes). No port of
   `milan_datapath`, no register field and no parameter of any module
   changes. The servo instance now names its existing `WIN_LOG2_P` at its
   default value (9) through `MCSRV_WIN_LOG2_C`, so the settle derives the
   window length instead of mirroring 512 ms.
3. **Every source change arms one settle recentre**, a change to INTERNAL
   included. There it fires once the aligner rests in its band; in the
   render bench that is the #386 dwell's own cycle, so the stage still
   executes one recentre (T31). At INTERNAL the same rule (the aligner's
   band, with an excursion arm) is ruling 1's "keyed on the aligner's band,
   fires once after a pull-in settles".

## 2. The RTL change

Commit `775764063`, two files.

**`hdl/milan/milan_datapath.sv`, `g_settle_recentre`** (beside the
unchanged #386 block `g_src_recentre`):

| Term | Value |
|---|---|
| Armed by | a change of the selected index (`media_clk_src_r` against the #386 block's registered copy), the aligner's re-engagement, and, while not pending, an aligner excursion past four settle bands (`SETTLE_EXC_ERR_C`, 1/16 sample) |
| Fires under following | `mcsrv_locked_w` held for `SETTLE_LOCK_TICKS_C` = 8 windows x 2^`MCSRV_WIN_LOG2_C` ms x 48 = 196,608 media ticks (4.096 s) running |
| Fires at INTERNAL | the aligner inside its settle band (`SRC_SETTLE_ERR_C`, 1/64 sample) for `SRC_SETTLE_TICKS_C` = 2,048 ticks running, or not engaged at all |
| While pending | an excursion restarts the run; the ceiling counts on |
| Ceiling | 2^`SETTLE_CEIL_LOG2_C` = 2^20 media ticks (21.8 s) from the arming |
| Output | `settle_recentre_p_r` (one cycle), ORed into `render_recentre_p_w` and replicated onto `KL_chan_map_capture`'s `lb_recentre_i` for every kept stream |

The net is declared at the capture crossbar's instance (`:1215`), where it
is first used, as the file already does for nets driven far below.

**`hdl/ieee1722/aaf/KL_chan_map_capture.sv`, the LOOP queue's RECENTRE**
(the banner states it in full):

- `lb_recentre_i[s]` arms stream `s` if it is primed (`rc_arm_r`).
- At the stream's next PDU start (the first accepted beat after any tlast,
  `lb_sof_r`), the events its first pair has left of the previous PDU
  decide for every pair of the stream: none, hold one pop; one, nothing;
  two or more, drop the oldest before the pop. The target is
  `LB_TARGET_C` = `LB_QDEPTH_C - 1` = 7 at a class-A PDU end
  (`LB_LEFT_C` = 1 left when the next PDU lands).
- The decision is staged (`rc_dec_r`) and handed to every pair at the next
  walk start (`act_hold_r`, `act_drop_r`), so all pairs act in one walk and
  stay in lockstep. A drop reads past the dropped event and composes with a
  same-cycle push.
- Neither `lb_dup_cnt_o` nor `lb_skip_cnt_o` moves: it is the declared
  discontinuity (`REGISTER_MAP.md`'s `SLIP_LB` row says so).
- An unprimed stream ignores the pulse; a flush cancels it; a pulse on a
  PDU's first beat arms for the next PDU.

**Why the decision is taken as a PDU starts.** The first version decided at
the PDU end, on the fill. The standing B8 leg showed it wrong: a walk that
falls inside the PDU's own beats (1.8 us at 4 channels, 3.8 us at 8, so 9
to 18 % of phases) pops an event of the PDU before its end, the fill reads
one low, and one hold under-corrects. Counted as the PDU starts, what is
left of the previous PDU is exact, and one held or dropped pop always
reaches the target.

## 3. Tests

Commits `6572896de` (follow_ring), `20c9b46ef` (chmap_capture),
`540d7f65e` (milan_dp_render), `8ba27663b` (builder pin, gmstep anchors).

**`tb/verilator/follow_ring`** (stage 1's harness, now grading). `dp_glue.py`
also copies the servo window line, the settle block and the three-term
render recentre set out of `milan_datapath.sv`; the wrapper binds the
servo's `locked_o` and the settle pulse into the LOOP bucket's
`lb_recentre_i`, as the datapath binds it. Every leg grades each transient
on `check_settle`:

| Check | What |
|---|---|
| one settle recentre | exactly one pulse from the transient to the hold's end |
| 8 windows after LOCKED | under following, `t_settle - t_LOCKED` = 4.096 s +/- 2 ms |
| the render stage executed it | its `recentres_o` moves within 1 ms of the pulse |
| no loopback slip after it | dups and skips from the pulse + 1 ms to the hold's end |
| the loopback ring centred | the margin's maximum after it in (1, 2] ticks, plus the run's uniform lateness |
| the render stage on its law | fill 14 and delay (8, 9] after the pulse + 50 ms, on runs with on-time arrivals (the law's own precondition); a window #643's ambiguity window cannot grade fails a standing leg and is reported in a sweep |

and the B8 leg adds: LOCKED within 15 s, at most the declared transient's
slips before the settle (`kPreSettleSlips` = 3); each stream-to-stream
switch adds: re-locks, no slip across it, and the ring's phase moved less
than 0.1 tick from before the switch to before its settle recentre (W2).

| Target | Runs |
|---|---|
| `make` | `b8` (set phase 0.0, a 16 s hold, two 15 s switch holds), `pullin` (52 us hold, feed latency 210.42 us, the phase the pull moves off the law), then `mutants.py` |
| `mutants.py` | NO-SETTLE (the pulse planted to 0 in a copy of the datapath, on `pullin`): fails the render law after the settle. RENDER-ONLY (`FR_MUT_RENDER_ONLY`, on `b8`): fails the loopback centring. EARLY (the following settle planted to the aligner's band, on `b8`): fails the render law after the settle. W1 (`FR_MUT_W1`): fails the 0.1-tick drift across AAF to CRF |
| `make sweep-b8` | 16 set phases over one INTERNAL beat, no lateness and 0 to 5 us uniform, 40 s hold, 20 s switch holds |
| `sweep.py b8 --jitter-us 2 --tail-us 24 --tail-p 1e-4` | the same 16 phases with the rare tail |
| `make sweep-pullin` | 16 feed phases over one tick, 52 us and 56 us holds |

**`tb/verilator/chmap_capture` `[LRC]`**: one 4-channel stream at one beat
per cycle; an unprimed stream ignores the pulse; none left holds one pop
(e6 repeats); two left drop the oldest on both pairs (e5 never plays) and
act once; one left moves nothing; a flush cancels; a pulse on a PDU's first
beat acts at the next PDU; both pairs carry one event per tick throughout;
neither counter moves. The wrapper binds lane A's `lb_recentre_i`; lane B
keeps the port's default, so its 30 other legs prove the default inert.

**`tb/verilator/milan_dp_render` `[PULLIN]`**: a fresh stream at a `[LAW]`
feed phase, on the law for 60 graded PDUs, then T14's 5,200-cycle
serial-clock hold under it; the wait for the settle recentre; one settle
recentre, the one render recentre pulse and the one stage recentre since the
hold; `SLIP_LB` static after it; the law again on a fresh instrument record
over 124 PDUs. The full leg runs the standing phase +1562; `make
tdm8render-pullin` runs all 18 `[LAW]` phases, one leg each.
`tdm8_render_mutants.py` gains "the settle recentre never pulses" on
`--pullin`.

**`sw/builder/test_builder.py`**: the exact `render_recentre_p_w`
initializer becomes `media_rebase_p_w | settle_recentre_p_r |
src_recentre_p_r`; a new pin requires `chan_map_capture`'s `lb_recentre_i`
to be `{LB_STREAMS_C{settle_recentre_p_r}}`, with a mutant that ties it to
`'0`; the ADP and GM-identity mutants move to the three-term text.
**`tb/verilator/milan_dp/gmstep_mutants.py`**: `RENDER_TRIGGER` and its
three controls move to the three-term text. `scripts/measure_test_evidence.py`
records follow_ring's `mutants.py` as a mutation campaign that reads the
datapath source.

## 4. Results

All follow_ring figures are from one build of head `cb42cc073` (the docs
commit after it changes no code), binary sha256
`827e3c94ef924596cc6a7e50c713bc1e31d02dec28303e238c260fc218483fc6`.
Tables: `stage2/sweeps/`.

### 4.1 The standing legs

`make -C tb/verilator/follow_ring` at `6bbdb57f4`: `b8` 26 checks, 0
failures; `pullin` 6 / 0; `mutants.py` 4 of 4 caught (NO-SETTLE by the
pull-in's render law after the settle; EARLY by B8's render law after the
settle; RENDER-ONLY by B8's loopback centring; W1 by the AAF-to-CRF 0.1-tick
drift). The B8 leg at set phase 0.0: 1 slip before the settle, 0 after,
loopback margin +1.55 ticks, render delay 8.46 ticks after each of the three
settle recentres.

### 4.2 The set and the switches, no lateness and 0 to 5 us (32 runs, all pass)

| Lateness | Slips, set to settle | Slips after the settle | Loopback margin after | Render after the settle | Switches |
|---|---|---|---|---|---|
| none | 1 at 9 phases, 2 at 7 | **0 at 16 of 16** | +1.06 to +2.00 ticks (the margin's maximum) | on the law at 15, not gradable at 1 | 0 slips at 32 of 32; the ring's phase moved -0.046 to +0.023 tick before each settle; render on the law at 30, not gradable at 2 |
| uniform 0 to 5 us | 1 at 9, 2 at 7 | **0 at 16 of 16** | +1.23 to +2.17 (2 ticks plus the 0.24-tick spread) | not graded (lateness); 11 on the law, 5 not gradable | 0 slips at 32 of 32; -0.038 to +0.023 tick |

Every settle recentre fired once, 4.096 s after LOCKED: 10.75 s after the set
(LOCKED 6.66 s), about 7.04 s after AAF to CRF and 9.96 s after CRF to AAF.

### 4.3 The rare tail (16 runs, 14 pass)

2 us uniform plus, on one PDU in 10,000, a further 0 to 24 us.

| Phase | Slips, set to settle | After the settle | Margin the recentre left | Then |
|---|---|---|---|---|
| 14 phases | 1 to 3 | 0 | 1.39 to 1.97 ticks | 0 slips across both switches |
| 0.25 | 1 | **1** | about 1.16 | AAF to CRF's settle re-centres it to the same place and it slips once more in that hold; CRF to AAF's leaves 1.16 and holds |
| 0.8125 | 2 | **1** | about 1.20 | AAF to CRF's settle leaves 1.19 and holds; CRF to AAF's leaves it near 1.2 and it slips once more |

The declared pre-settle bound holds at every phase: 3 at most (phases
0.875 and 0.9375), 2 without the tail.

### 4.4 The phase-aware target, prototyped out of the tree, on the same tail

`stage2/area/optB_KL_chan_map_capture.diff`, the same harness and seeds:
**0 slips after any settle recentre at 16 of 16 phases**, 0 across every
switch, pre-settle slips unchanged (1 to 3). Its only failures are the
harness's 7-event centring check, at the 5 phases where it chose 8 events,
which is the change it makes.

The same prototype through the set and switch campaign, no lateness and
5 us (`stage2/sweeps/optB_b8_j0_j5.md`, 32 runs, 96 settle recentres): 0
slips after any settle recentre, 0 across any switch. Again every failing
check (43, in 16 runs) is the 7-event centring check. Through the 32
pull-ins (`stage2/sweeps/optB_pullin.md`): 0 slips after the settle
recentre, 1 before it at 3 runs, render on the law at 27 and not
gradable at 5, as with option C; its 16 failures are that check too. **But the
prototype is not right at the tick's edge.** At phase 0.5625, where the
PDU lands on a pop, 2 of the 96 settles chose one event and left about 1.0
tick (0.99 at CRF to AAF without lateness, 0.97 to 1.22 at AAF to CRF with
5 us). That is option C's own worst case, not the 1.5 the design aims for.
The likely cause, not traced: its half-tick test counts from the media
tick, but the margin counts to the pair's pop, which comes later in the
walk. A PDU landing in that gap, just before its pop, reads as the tick's
early half. A real option B must reference its test to the pop and grade
that edge; the prototype does not prove it.

### 4.5 INTERNAL pull-ins (follow_ring, 32 runs, all pass)

| Hold | Pull | Settle recentre after the hold | On the law after it | Not gradable | Off the law | Loopback slips before / after it |
|---|---|---|---|---|---|---|
| 52 us | +0.53 tick | 0.854 s, one per run | 14 | 1 before, 1 after | **0** | 0 / 0 |
| 56 us | -0.33 tick | 0.190 s, one per run | 13 | 1 before, 2 after | **0** | 1 at 3 phases / 0 |

Stage 1, with no settle recentre, left the law at 7 of 13 and 4 of 14
gradable phases. The 52 us hold takes four times as long to settle: a
2.50-frame step folds to almost exactly half a sample, and the aligner
rests in its 1/64-sample band only after its slow tail.

### 4.6 The render law suite (`milan_dp_render`)

- Default target at `6bbdb57f4`: the shipping leg 259 checks, 0 failures
  (T30 INTERNAL and CRF, T31, `[LAW]` at 18 phases, and `[PULLIN]` at
  +1562); the two-stream leg 65 / 0; `--leg-defects` 5 of 5.
- `[PULLIN]` in the full leg: the settle recentre 512.3 ms after the hold.
  After the `[CRF]` history the aligner pulls the 0.5-sample step in by
  about 112 ms, overshoots to -65 cycles (outside its 32-cycle band) and
  decays back through 512 ms; on the law after it (delay 8.73 ticks), 0
  loopback slips. The first version of the leg waited 400 ms and failed
  here; the wait is now up to 2 s with the instrument's record renewed.
- `tdm8render-pullin` at `6bbdb57f4`: 18 of 18 legs pass, each settle
  recentre 152.6 ms after the hold from a fresh boot, 0 loopback slips
  during the pull or after it; the law after the settle graded at 17 phases
  (fill 14, first event 8.05 to 8.94 ticks) and +1042 not gradable
  (`stage2/legs/render_pullin/`).
- `tdm8render-law-boundary` at `6bbdb57f4`: 81 checks, 81 PASS, rc 0
  (`stage2/legs/render_law_boundary.log`). The unmutated gateware and both
  setpoint defects scan +1986..+2066 ascending (not gradable at
  +2015..+2035) and descending (+2016..+2036), then each phase alone over
  +2014..+2038; the largest walk is 3 cycles over 564 windows, against the
  leg's stated 5.
- `tdm8render-mutants` at `6bbdb57f4`: 34 checks, 30 PASS, 4 FAIL, rc 2
  (`stage2/legs/render_mutants.log`). The new row, "the settle recentre
  never pulses", is caught on `--pullin` by "T647 PULLIN +1562 after the
  settle: every PDU's first event is inside the law band from its PDU
  end", and the `--pullin` positive control passes. Every other mutant
  is caught, including the render recentre set's own ("the clock-source
  trigger dropped from the recentre set") and the three `--law-only`
  rows. The 4 failures predate this change (section 4.8): the
  unmutated `--epoch-only` leg, the two arrival-skew clean controls that
  run in that mode, and the "uncounted repeat" survivor. `TESTING.md`'s
  inventory now counts 22 mutants and 34 checks (`ff6b28b0f`).

### 4.7 Other suites

| Suite | Head | Result |
|---|---|---|
| `chmap_capture` (with `[LRC]` and the netlist leg) | `8ba27663b` (its sources unchanged since) | 399 checks, 0 failures; `[NC]` 20 / 0 |
| `milan_dp` (with `render_mutants.py` and `gmstep_mutants.py`) | `8ba27663b` | rc 0, 0 `[FAIL]` |
| `milan_dp_mclk` | `8ba27663b` | rc 0, 0 `[FAIL]` |
| `media_grid_align` | `8ba27663b` | rc 0 (its three `[FAIL]` lines are negative controls, RED as required) |
| `pp_shadow` | `23657429c` | 311 checks, 0 failures |
| `capture_coherence` | `cb42cc073` | rc 0; its mutation arm 30 of 30 |
| `syn/yosys/run.sh` | `6bbdb57f4` | 55 of 55 tops; tied-input and tap-purity gates PASS |
| `sw/builder/test_builder.py` | `a98543b27` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, environmental; section 7) |
| `scripts/xvlog_gate.py --check` | `6bbdb57f4` | PASS: 0 `hdl/` findings, 4 pinned-processor findings at the ratchet |

No commit after the one named touches a file the suite reads: the later
ones change the render bench, follow_ring's harness and docs only.
`milan_dp_gptp`, the scheduled physical suite outside the default sweep,
was not run.

### 4.8 Found on the way: two failures in the mutation campaign that predate this change

The explicit campaign (`make tdm8render-mutants`) runs short legs the
default target does not. 4 of its checks fail, from two causes, at this
lane's base (`6ca6d668`) as at its head. They are out of this lane's scope, so they are
recorded here for a new Issue and not fixed.

1. **`--epoch-only` fails T30 CRF.** That leg skips `[SERIAL]`, so `[CRF]`
   runs straight from boot, before the aligner's boot pull-in is done. The
   #386 trigger then never fires: four checks fail (fired once, one render
   recentre pulse, one executed recentre, no second recentre). `--crf-only`
   dwells `kBootPullInCycles` for this reason (#629 A2-a); `--epoch-only`
   does not. The campaign then reads its unmutated control as failing,
   and both arrival-skew clean controls fail in that mode with it.
2. **The "uncounted repeat" mutant survives `--serial-only`.** The leg's one
   underrun lands before its T6 window opens ("underruns before 1"), and the
   window grades 0 repeats, so "T6 ORDER: every repeat is a counted
   underrun" holds with the counter frozen.

Evidence (`stage2/legs/base_probe/`): the shipping bench built against the
base `milan_datapath.sv`, unchanged apart from two stub lines for the two
signals the bench now reads (`base_stub_lines.txt`), against the same
build at the head. Each mode's output is byte-identical at both: 114
checks with the same 4 failures under `--epoch-only`; 53 checks, 0
failures, under `--serial-only` with the mutant (`uncounted_repeat_mutant.diff`)
planted.

## 5. Area

Vivado 2026.1, out of context, xc7a100tfgg484-2 at 20 ns (the shipping
50 MHz axis clock), the shipping AX7101 1x1 parameters
(`KL_chan_map_capture`: `N_SLOTS_P=4 N_TDM_P=8 TDM_FRAME_PAIRS_P=4
N_LB_STREAMS_P=1 N_LB_CH_P=8`), the base taken from `6ca6d668`, one Vivado
process per configuration under the shared lock, 0 critical warnings.

| Block | Base | This change | Delta |
|---|---|---|---|
| The settle logic: the #386 block alone (base) against it plus `g_settle_recentre` and the render OR (standalone wrapper of the datapath's own lines) | 41 LUT, 51 FF, 16 CARRY4 | 67 LUT, 92 FF, 32 CARRY4 | **+26 LUT, +41 FF** |
| `KL_chan_map_capture` at 1x1 | 1,076 LUT, 1,336 FF, 1 BRAM tile | 1,086 LUT, 1,344 FF, 1 BRAM tile | **+10 LUT, +8 FF** |
| **Total** | | | **+36 LUT, +49 FF**, under the ruling's 120 / 120 |

Timing out of context: WNS +15.70 ns (settle) and +13.61 ns (capture) at
20 ns.

**The integrated route** (`stage2/route/`): the #638 recipe (the AX7101 1x1
LiteX export, `baseline_integrated.tcl`), Vivado 2026.1, the two runs one
after the other under the shared lock, nothing else of this lane's beside
them. The
two differ only in `milan_datapath.sv` and `KL_chan_map_capture.sv`,
frozen copies of `6ca6d668` and of the head (`rtl_sha256.txt`).

| | Base | This change | Delta |
|---|---|---|---|
| LUT | 50,767 | 50,819 | +52 |
| FF | 59,634 | 59,798 | **+164** |
| BRAM tiles / DSP | 92.5 / 14 | 92.5 / 14 | 0 / 0 |
| WNS / WHS (all constraints met; no negative path at Slow 85C or Fast 0C) | +0.193 / +0.024 ns | +0.112 / +0.018 ns | |

**The FF delta is over the ruling's 120, and this change's own registers
are 48 of it.** Every flip-flop of the four checkpoints, listed by register
name (`ff_attribution.txt`, `ffdump.tcl`): the settle logic's 41
(`settle_ceil_ticks_r` 21, `settle_run_ticks_r` 18, `settle_pend_r`,
`settle_recentre_p_r`) and the capture crossbar's 7, as out of context.
The rest is RTL this change does not touch, kept differently by the two
runs. After synthesis (+131): the audio-map edit registers
`amap_edit_iclaim_*` +43 (78 bits kept at the base, 120 here); LiteX's
`errd0` / `errd1` +32; and a 64-bit swap between `ptp_clock_validity/gm_r`
and `gsi_gm_q_r`, which nets to 0. After the route (+164), `avtp_rx_parser`'s
`hdr` adds 30. Unchanged instances moved from -103 to +113 LUT between the
runs, so the +52 LUT is not attributable either. Which figure the ruling's
120 applies to is for the ruling (section 8).

## 6. Documentation

Commits `6bbdb57f4`, `a98543b27`, `ff6b28b0f`.

- `docs/design/MEDIA_CLOCK_FOLLOWING.md`: "Switching sources" (`:1043`)
  names the settle recentre and the transient from INTERNAL; a new
  "Settle recentre" section (why, the trigger table with the 2^20-tick
  ceiling and the pruned-servo case, measured timings, the loopback lane's
  +20.8 us stated as the diagnostic loopback, not the presentation path, so
  the latency = presentation-time rule is unaffected); "The declared
  transient" (at most 3 frames before the settle at 5.92 ppm, 2 without the
  tail, the pull-in case); the open tail case; three test-plan rows; the
  #647 open-gap paragraph closed; an implementation note.
- `docs/design/TIME_SYNC.md` (`:384-385` and the prose under the render
  table): the recentre set gains the settle recentre; the at-switch settle
  row is named as #386's; a new settle-recentre row; three short lines.
  Held to the page's ten-word sentence and twenty-word paragraph limits.
- `docs/reference/REGISTER_MAP.md` `SLIP_LB`: the settle recentre's held
  pop or dropped event counts in neither half.
- `docs/testing/TESTING.md`: the follow_ring row (grading, mutants,
  campaigns, the red tail case) and the render row (`[PULLIN]`,
  `tdm8render-pullin`, and the mutation inventory: 22 mutants, 34 checks).
- In the RTL: `KL_chan_map_capture`'s banner gains RECENTRE and the `[LRC]`
  verification line; the datapath's block comment states the trigger.

## 7. Gates

Every command unpiped, its output to a file, rc 0 except the two named at
the end of this section. Receipts: `stage2/gates/`.

- **Static, at `a98543b27`** (26): `check_cpp_idiom` and `--selftest`,
  `check_py_idiom` and `--selftest`, `check_hygiene --check`,
  `check_todo_ownership`, `check_sv_idiom`, `measure_test_evidence --check`
  (0 unexplained DUT-source readers; follow_ring's `mutants.py` recorded as a
  campaign) and `--selftest`, `measure_fail_fast --check`, `measure_naming
  --check`, `check_rtl_source_lists` and `--selftest`, `suite_shards
  --selftest`, `ci_scope --selftest`, `check_feature_status --self-test`,
  `check_baremetal_only --check`, `lint_rtl.py --check` (90 <= 90), and in
  the pinned Markdown environment `docs_check`, `check_doc_style`, `gen_toc
  --check` and `--verify-anchors`, `check_em_dash --base fea346e7`,
  `check_doc_paths`, then `git diff --check fea346e7` and `git diff --check`.
- **`scripts/xvlog_gate.py --check`** under the Vivado lock, at
  `6bbdb57f4`: 0 findings in `hdl/` (the settle pulse's declaration ahead
  of its driver is accepted), 4 pinned-processor findings at the ratchet.
- **`syn/yosys/run.sh`** at `6bbdb57f4`: 55 of 55 tops, the tied-input and
  tap-purity gates PASS.
- **`sw/builder/test_builder.py`** at `a98543b27`: ALL GATES PASS EXCEPT 1
  NOT RUN (gate 11, the Arty calibration report, needs a build tree this
  host does not have; environmental, as at dev).
- **Doc gates at `ff6b28b0f`** (the inventory count in `TESTING.md`):
  `docs_check`, `check_doc_style`, `gen_toc --check` and
  `--verify-anchors`, `check_em_dash`, `check_doc_paths`, `check_hygiene
  --check`, and both `git diff --check`, all rc 0.
- **Suites**: the eight touched suites' default targets (section 4.7 and
  4.6), 36,195 checks, 0 failures by `scripts/suite_tally.py`, each log
  `--verdict` rc 0; the follow_ring and render campaigns of section 4.
- **Not rc 0, both reported above:** the tail campaign (2 of 16 phases,
  the open finding, section 4.3) and `tdm8render-mutants` (rc 2, the 4
  failures that predate this change, section 4.8).
- **Not run:** `milan_dp_gptp` (the scheduled physical suite), `act` and
  the hosted contexts (nothing is pushed), the full `run_all_suites.sh`
  sweep (the 52 suites this change does not touch).

## 8. The open finding, its options and the recommendation

**The finding.** The ruling asks for "#645: after the settle recentre, no
slip across the 16 switch timings and the lateness tail". With stage 1's
rare tail (2 us of uniform lateness, plus, on one PDU in 10,000, a further
0 to 24 us), 14 of 16 set phases hold; at phases 0.25 and 0.8125 the
loopback ring slips once after the INTERNAL-to-AAF settle recentre, and
again after a later switch's settle recentre (section 4.3).

**Why, from the ring's arithmetic.** The ring is `LB_QDEPTH_C` = 8 events:
one 6-event PDU and two events of slack. A PDU's first event pops `m` ticks
after it lands, and a PDU later than `m` ticks finds the queue empty. The
7-event target puts `m` at 1 + `p`, where `p` in (0, 1] is where the
stream's PDUs fall against the media tick; no event count can move `p`. So
at the worst phase the ring tolerates one tick (20.8 us) of lateness, and
the tail reaches 26 us (1.25 ticks). The two failing phases are the two
whose recentred margin came out under 1.25 ticks (1.16 and 1.19 to 1.22).
Arrivals within 5 us of each other slipped nothing (section 4.2). The bench's
arrival distribution is not measured, so whether this tail is real is open;
stage 1 chose it to reproduce the bench's 15 to 45 s slip times.

**Options** (none implemented in the tree):

| Option | What | Effect on the tail case | Cost |
|---|---|---|---|
| A. Declare it | the settle recentre's loopback ring tolerates arrivals up to one tick later than the PDU it read; a later one slips it once, after which it is a tick further from the edge | none; documents the 2 of 16 | 0; the ruling says anything after the settle must not happen, so this reverses ruling 3 for one case |
| **B. Phase-aware target (recommended)** | as the stream's next PDU starts, the LOOP queue also reads how far into the media tick it landed (a 12-bit tick-age counter and the tick's period, both counted from `tick_i`): in the tick's late half it keeps two events of the previous PDU, in its early half one. Aimed at a margin in (1.5, 2.5] ticks: 1.5 ticks (31 us) of lateness tolerance, 0.5 tick of earliness | the prototype (`area/optB_KL_chan_map_capture.diff`, out of the tree) gave 0 post-settle slips at 16 of 16 tail phases and in 32 set and switch runs, but left about 1.0 tick at 2 of 96 settles at the tick's edge, so its test needs referencing to the pop (section 4.4) | `KL_chan_map_capture` at 1x1 out of context: 1,118 LUT, 1,375 FF, +32 / +31 over option C's (+42 / +39 over the base), so +68 / +80 in all with the settle logic, under 120 / 120; WNS +13.62 ns; the loopback lane's latency is 7 or 8 events by phase (+20.8 or +41.7 us over today's edge, against the ruled +20.8); `[LRC]` grows phase cases |
| C. A deeper ring | `LB_QDEPTH_C` 8 to 10 (a localparam), target 8: two ticks each side | removes it | the queue law and its L0 legs change (`[LQ*]`), +41.7 us on the loopback lane, a wider queue RAM per pair |
| D. Keep as is | the B-lane repeat measures the bench's real arrival spread first | none until measured | 0 |

**Recommendation: B.** It keeps the depth and the queue law, acts as
option C does but may hold up to two pops per pair (one per walk) where
C holds one, costs a few dozen LUTs, and met the ruled acceptance under
the tail in the prototype. It needs a ruling because it changes the ruled
"7-event target" to "7 or 8 by phase". It also needs the edge fixed and
graded before it is evidence: the prototype left option C's worst margin
at 2 of 96 settles (section 4.4).

**A second item for the ruling: the area limit.** The ruling sets "OOC 1x1
plus the route delta; STOP if over 120 LUT or 120 FF". Out of context the
change is +36 LUT / +49 FF. The integrated route's total is +52 LUT / +164
FF, over 120 FF, but by register name this change's own flip-flops are 48
of the 164 (section 5). This lane reads the limit as applying to the
change's own logic, which is under it, and asks for that reading to be
confirmed. Option B would add about +32 LUT / +31 FF to the out-of-context
figure.

## 9. Reproduction commands and evidence

From the lane worktree, with the pinned Verilator 5.050 first on PATH:

```sh
make -C tb/verilator/follow_ring                      # standing legs + 4 mutants
make -C tb/verilator/follow_ring sweep-b8 sweep-pullin SWEEP_JOBS=8
cd tb/verilator/follow_ring
python3 sweep.py b8 --exe obj_dir/Vfollow_ring --out obj_dir/sweep_tail --jobs 8 \
  --jitter-us 2 --tail-us 24 --tail-p 1e-4 --hold-s 40 --switch-hold-s 20 --extra --dwell-s 1.0
cd ../../..
make -C tb/verilator/chmap_capture
cd tb/verilator/milan_dp_render && make && make tdm8render-pullin PULLIN_JOBS=4 \
  && make tdm8render-law-boundary && make tdm8render-mutants; cd ../../..
make -C tb/verilator/milan_dp && make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/media_grid_align && make -C tb/verilator/pp_shadow \
  && make -C tb/verilator/capture_coherence
```

**The prototype (option B), out of the tree.** Apply
`stage2/area/optB_KL_chan_map_capture.diff` to a copy of
`hdl/ieee1722/aaf/KL_chan_map_capture.sv`, build follow_ring with that copy
in place of the tracked file (the build log's `verilator` line, with the
source path and `-Mdir` changed), and run the tail command above with that
executable.

**The base probe (section 4.8).** From `tb/verilator/milan_dp_render`,
build the bench through its own recipe against a copy of the base
datapath, `git show 6ca6d668:hdl/milan/milan_datapath.sv` with the two
lines of `stage2/legs/base_probe/base_stub_lines.txt` inserted before
"#443: packed listener words":
`make tdm8render-build TDM8R_MDIR=<dir> DP_SRC=<that copy>`, then run
`<dir>/Vmilan_dp_tdm8r --epoch-only` from the suite directory. For the
survivor, add `TDMRM_SRC=<a copy of KL_tdm_render_master.sv with
uncounted_repeat_mutant.diff applied>` and run `--serial-only`. Do the same
without `DP_SRC` for the head.

**Area.** `stage2/area/`: `ooc_s2.tcl` and `run_ooc_s2.sh` (one Vivado
process per configuration under `flock $VIVADO_LOCK`), the
standalone settle wrappers and the datapath extracts they include, the
utilisation and timing reports, and the sha256 of the five source copies
synthesised (`sources_sha256.txt`).

**Evidence in this directory** (`stage2/`): `sweeps/` (the B8 table, no
lateness and 5 us; the tail table at the head and for the prototype; the
pull-in table; the prototype's B8 and pull-in tables), `route/` (both
integrated routes' utilisation, hierarchy, route status and timing
summaries, the flip-flop attribution and its Tcl, the frozen RTL's
sha256, and the sha256 and size of the checkpoints and full timing
reports kept outside), `legs/base_probe/` (section 4.8), `legs/` (the touched suites' small logs, the render pull-in
campaign's 18 legs), `gates/` (static gate exit codes, the suite tally with
each `--verdict`, the lint, evidence, xvlog, Yosys and builder tails, and
the sha256 and size of every suite log, the large ones kept outside).
