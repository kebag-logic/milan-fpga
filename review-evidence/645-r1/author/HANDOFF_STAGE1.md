# #645 / #647 diagnosis lane: [A531] handoff

Status: **STOP with options.** The cause is established in simulation (section
4); the fix waits on a ruling (section 6). Head `6ca6d6686a69f2b053652149d21af63987479b4b`,
one commit on dev `fea346e7`, local and not pushed.

- Branch: `645-ring-slip` from dev `fea346e76c2a57ed5cd131af8fc68dfeff57f877`
- Processor pin: `631eeb34`
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5981976917
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5981985858
- STOP: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982557846
- Executor [A531]; reviewers [R474] (internal), [R475] (external)
- No RTL change. Option prototypes for the area estimates live outside the
  tree; their diffs are in `area/`.

## Contents

1. The reproduction harness
2. #645 reproduced: the INTERNAL-to-AAF set and the stream-to-stream switches
3. #647 reproduced: an INTERNAL aligner pull-in under a running stream
4. Classification
5. Fix options, with area, protocol-visible effect and test plan
6. Recommendation
7. Reproduction commands
8. Commits, gates and evidence hashes

## 1. The reproduction harness

`tb/verilator/follow_ring/` (new). It binds the media-clock plane and the two
listener rings the plane paces, as `milan_datapath` binds them on the
shipping AX7101 1x1 TDM8 shape:

| Block | Source | Role |
|---|---|---|
| `KL_aaf_clock_meter` | real RTL | the followed AAF stream's rate (E8) |
| `KL_crf_rx` | real RTL | the CRF stream's rate |
| `KL_mmcm_drp_servo` | real RTL | the frequency-only servo, its silicon loop (512 ms windows, KI 1/2, KP 1/4, 2 ppm lock over 4 windows) |
| `KL_media_nco`, `KL_media_grid_align` | real RTL | the packet grid, aligned to the physical grid at every source (A2-a) |
| `KL_chan_map_capture` LOOP bucket | real RTL | the loopback ring `SLIP_LB` counts (#645) |
| `KL_render_setpoint` | real RTL | the render ring the #386 recentre re-centres (#647) |
| decode, reference mux with W2, A2-a aligner select with keep-off and late tick, #386 settled-grid trigger | `milan_datapath.sv:1579-1616`, `:5728-5749`, `:5905-5916`, `:6264-6311`, `:6321-6323`, copied verbatim at build time by `dp_glue.py` | the datapath's own glue, never restated |
| MMCM | `tb/verilator/mmcm_servo/mmcm_model.h` | the fine phase shift moves the audio clock's edges |
| the reference peer | `sim_main.cpp` | an AAF talker (4 channels, 6 events per PDU) and a CRF talker on one media clock |

**Which ring #645 is.** `SLIP_LB` (`0x8D4`) is the dup count of the capture
crossbar's LOOP bucket (`KL_chan_map_capture.sv:213-220`, `:828-831`): the
rx-to-talker loopback lane, 8 events deep per pair, popped one event per
media tick, a dup when a tick finds a pair empty. It has no setpoint, no
prefill beyond the first PDU, and no recentre input: only a bind flush
(`:221-227`) re-primes it. The #386 recentre reaches `KL_render_setpoint`
only (`milan_datapath.sv:6321-6323`, `:6477`). A 4-channel stream fills two
pairs, so one slipped frame is 2 on `SLIP_LB`, as lanes B7 and B8 read it.

**The ring's margin**, the quantity the traces print: for each PDU, the time
from its first event landing in pair 0's queue to the pop that takes it, in
media ticks. By the ring's law it lives in (0, 3]: below 0 a tick finds the
queue empty (a dup, and the margin gains a tick), above 3 a push finds it
full (a skip, and it loses one). Nothing moves it otherwise.

### Time and clock scaling

Nothing is time-compressed. A 512 ms servo window is 512 ms of simulated time,
the meter's E8 history is 4.096 s, and the INTERNAL beat is the bench's
3.52 s. Only clock rates that no loop measures in are reduced:

- **Axis clock 6.25 MHz**, an eighth of the shipping 50 MHz. The servo, meter
  and CRF receiver measure on gPTP time, which the harness gives exactly, so
  the clock rate changes none of their rates. The servo's window endpoints are
  sampled at 160 ns instead of 20 ns; the endpoints telescope in the
  integrator, so this adds bounded phase noise (the post-LOCKED trim wanders
  -5.75 to -6.06 ppm, the bench's B8 hold read -5.81 to -6.06), not drift.
- **The aligner** is the one loop whose arithmetic is in axis cycles. Its gains
  are scaled by the same factor of 8 (KP_LOG2 2 + 3 = 5, KI_LOG2 12 - 3 = 9),
  so its proportional and integral gains in sample units are the shipping
  ones (32 x 130 = 4,160 against 4 x 1,041 = 4,164; 130 / 512 = 0.254 against
  1,041 / 4,096 = 0.254). Its keep-off (a quarter sample, 32 cycles) and the
  #386 settle band (1/64 sample, 2 cycles) come from the datapath's own copied
  declarations and are the shipping values in sample units. The NCO's integer
  `PPM_LSB_P` (6 against 6.25) leaves the aligner's actuator gain 4 % low: 4 %
  of loop bandwidth, no settled-phase effect.
- **Audio clock** 24.576 MHz / 32 with `TICK_CYC_P` 768 and `GAIN_NUM_P` 1, as
  `tb/verilator/aaf_clock_meter/meter_servo_wrap.sv` runs the servo's silicon
  loop. One physical frame is 16 audio cycles: the physical 48 kHz grid.
- **PSCLK** 1 MHz, PSDONE 2 PSCLK cycles after PSEN (`milan_dp_mclk`'s choice).
- **Payload beats** one axis cycle apart, 160 ns: silicon's 8 cycles at 50 MHz.
- The capture crossbar's slot walk is cut to two slots with a one-cycle gap.
  Only its LOOP bucket is read, and that bucket's pre-walk pop is unchanged.
- The talkers start at 0.6 s, after the aligner's boot pull-in.

### Calibration to the bench (B7/B8, `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`)

| Quantity | Bench | Harness |
|---|---|---|
| Peer's media clock against gPTP | meter and CRF sink +11.02 ppm ("positive means slow") | `--peer-ppm -11.02`; the meter reads 5,642 ns / 512 ms = +11.02 ppm |
| DUT INTERNAL against gPTP | about -5.1 ppm | `--dut-ppm -5.10` |
| DUT INTERNAL against the peer | +5.92 ppm, one slip per 3.52 s, 342 dups in 600 s (B0) | +5.92 ppm, beat 3.519 s |
| The boards' oscillators | about 16.5 ppm apart | (-5.10 + 10.64) - (-11.02) = 16.56 ppm |
| Meter rate valid after the INTERNAL-to-AAF set | 4.14 to 4.64 s (B8) | first PI window 4.61 s after the set |
| Servo LOCKED after the INTERNAL-to-AAF set | 6.6 to 7.1 s (B7), 6.64 to 7.14 s (B8) | 6.66 s at every phase |
| LOCKED after AAF to CRF / CRF to AAF | 2.62 to 3.12 s / 5.96 to 6.48 s (B8) | 2.98 s / 6.02 s |

## 2. #645 reproduced

### The case

Lane B8's SW case: the peer's AAF stream on STREAM_INPUT 0 (feeding both
rings) and its CRF stream on STREAM_INPUT 1, the DUT on INTERNAL, then
SET_CLOCK_SOURCE 2 (AAF), held; then 1 (CRF) and 2 again. The set is placed at
16 phases across one INTERNAL beat, counted from an INTERNAL slip, so the
ring's margin at the set runs once round its range. Arrival lateness: none,
uniform 0 to 5 us, and 2 us uniform plus a rare queueing tail (probability
1e-4 per PDU of a further 0 to 24 us; one 1,500-octet frame is 12 us at
1 Gb/s).

### The mechanism, in one run

Set phase 0.5625, uniform 0 to 5 us lateness, then AAF to CRF and CRF to AAF
(`traces/b8_phase0.5625_j5.log`; the 0.25 s table of the whole run is
`traces/b8_phase0.5625_j5_table.csv`). Times from the INTERNAL-to-AAF set;
each row is the half second ending there (rows abridged); the servo columns
are its last window.

| t, s | Ring margin, ticks | Ring slips | Render fill / first-event delay, ticks | Servo | PI ran | e, ns per 512 ms | Trim, ppm | Meter rate valid |
|---|---|---|---|---|---|---|---|---|
| -0.50 | +0.584..+0.960 | 0 | 12 / 6.490..6.866 | IDLE | 0 | 0 | 0 | 0 |
| +0.00 | +0.438..+0.814 | 0 | 12 / 6.344..6.728 | IDLE | 0 | 0 | 0 | 0 |
| +0.50 | +0.299..+0.668 | 0 | 12..14 / 6.336..8.571 (the recentre at +0.043) | IDLE | 0 | 0 | 0 | 0 |
| +1.00 | +0.154..+0.538 | 0 | 14 / 8.064..8.440 | ACQUIRE | 0 | 2,560 | 0 | 0 |
| +1.50 | +0.015..+0.392 | 0 | 13..14 / 7.918..8.302 | ACQUIRE | 0 | 2,720 | 0 | 0 |
| +2.00 | +0.008..+1.236 | **1** | 13..14 / 7.780..8.156 | ACQUIRE | 0 | 2,560 | 0 | 0 |
| +3.00 | +0.584..+0.960 | 0 | 13 / 7.496..7.872 | ACQUIRE | 0 | 2,720 | 0 | 0 |
| +4.00 | +0.299..+0.683 | 0 | 13 / 7.204..7.588 | ACQUIRE | 0 | 2,560 | 0 | 0 |
| +5.00 | +0.092..+0.399 | 0 | 13 / 6.997..7.304 | ACQUIRE | 1 | -3,082 | -4.562 | 1 |
| +5.50 | +0.061..+0.330 | 0 | 12..13 / 6.966..7.242 | ACQUIRE | 1 | -682 | -4.062 | 1 |
| +6.00 | +0.031..+0.299 | 0 | 12..13 / 6.935..7.204 | ACQUIRE | 1 | -1,002 | -5.188 | 1 |
| +6.50 | +0.015..+0.269 | 0 | 12..13 / 6.920..7.181 | ACQUIRE | 1 | -362 | -5.188 | 1 |
| +7.00 | +0.008..+1.244 | **1** (+6.83, LOCKED +0.17) | 12..13 / 6.912..7.165 | LOCKED at +6.66 | 1 | -362 | -5.562 | 1 |
| +8.00 | +0.991..+1.236 | 0 | 12..13 / 6.897..7.142 | LOCKED | 1 | -202 | -5.875 | 1 |
| +9.50 | +0.983..+1.229 | 0 | 12..13 / 6.889..7.135 | LOCKED | 1 | -42 | -5.938 | 1 |

Before the window that closes at +4.61 s the PI does not run (`e` there is the
local error alone, the rate being invalid), and the ring's margin falls at
the INTERNAL beat's 0.284 tick a second. After the second slip the margin is
above one tick, and the ring holds for the rest of the 60 s hold and through
both stream-to-stream switches (LOCKED 2.98 s and 6.02 s after them, 0 slips).
The render ring, re-centred at +0.043 s, follows the same walk down to fill 12
or 13 and a first event about 7 ticks after its PDU end, against the law's 14
and (8, 9].

What every run shows:

1. **At INTERNAL the ring sits within one tick of its empty edge.** The DUT
   reads 5.92 ppm faster than the peer writes, so the margin falls 0.284 tick
   a second and the ring dups whenever it reaches 0, which adds one tick. With
   no setpoint and no recentre, that sawtooth is its whole state: margin in
   (0, 1] of its (0, 3] range.
2. **The set does not stop the walk for about 4.6 s.** The meter's E8 rate is
   valid 4.1 s after its era starts at the set, so the servo's PI first runs
   on the window that closes 4.61 s after the set. Until then the trim is 0
   and the DUT keeps reading 5.92 ppm fast: 1.31 ticks of walk.
3. **The PI then stops the frequency, not the phase.** It adds about 0.12 tick
   more before LOCKED (6.66 s) and about 0.03 after it: 1.43 ticks from the
   set to LOCKED in every run. A frequency-only loop holds whatever phase the
   walk left (`KL_mmcm_drp_servo.sv:22-34`).
4. **So the ring slips 1 or 2 times between the set and LOCKED and is left at
   a margin uniform in (0, 1) tick at LOCKED.** Nothing re-centres it.
5. **A slip after LOCKED needs the margin at LOCKED to be within reach of
   what follows**: the PI's 0.03-tick tail with ideal arrivals, or a PDU later
   than the margin. A slip adds a tick of margin, and then the ring holds
   through every later stream-to-stream switch, as B7 (570 s) and B8 (428 s)
   saw.

### The sweep: 16 set phases, no arrival jitter

| Set phase (of one 3.52 s beat) | Slips set to LOCKED | Slips after LOCKED (when) | Ring margin at LOCKED, ticks | Render ring at the hold's end: fill / first-event delay, ticks |
|---|---|---|---|---|
| 0.0000 | 1 | 0 | +0.568..+0.584 | 13 / 7.457..7.465 |
| 0.0625 | 1 | 0 | +0.507..+0.522 | 13 / 7.396..7.404 |
| 0.1250 | 1 | 0 | +0.445..+0.453 | 13 / 7.327..7.342 |
| 0.1875 | 1 | 0 | +0.384..+0.392 | 13 / 7.265..7.281 |
| 0.2500 | 1 | 0 | +0.323..+0.330 | 13 / 7.204..7.219 |
| 0.3125 | 1 | 0 | +0.261..+0.269 | 13 / 7.142..7.158 |
| 0.3750 | 1 | 0 | +0.192..+0.207 | 13 / 7.081..7.096 |
| 0.4375 | 1 | 0 | +0.131..+0.146 | 13 / 7.020..7.027, not gradable |
| 0.5000 | 1 | 0 | +0.061..+0.084 | 12 / 6.950..6.966 |
| 0.5625 | 1 | **1 (+0.42 s)** | +0.008..+1.014 (the slip) | 12 / 6.889..6.904 |
| 0.6250 | 2 | 0 | +0.937..+0.960 | 12 / 6.828..6.843 |
| 0.6875 | 2 | 0 | +0.876..+0.891 | 12 / 6.766..6.781 |
| 0.7500 | 2 | 0 | +0.814..+0.829 | 12 / 6.705..6.720 |
| 0.8125 | 2 | 0 | +0.753..+0.768 | 12 / 6.643..6.659 |
| 0.8750 | 2 | 0 | +0.691..+0.707 | 12 / 6.582..6.589 |
| 0.9375 | 2 | 0 | +0.630..+0.645 | 13 / 7.519..7.526 |

Every run: LOCKED 6.66 s after the set; the #386 render recentre at 42.7 ms
after the set, 6.61 s before LOCKED. The render law is fill 14 at the PDU end
and a first event in (8, 9] ticks of it; a window whose PDU ends lie within 3
axis cycles of a pop is not gradable (#643's ambiguity window at this clock).

### With arrival lateness

| Lateness model | Phases that slip after LOCKED | When, after LOCKED | Slips set to LOCKED |
|---|---|---|---|
| none | 1 of 16 (phase 0.5625) | +0.42 s | 1 at phases 0 to 0.5625, 2 at 0.625 to 0.9375 |
| uniform 0 to 5 us | 1 of 16 (phase 0.5625) | +0.17 s | as above |
| 2 us, plus a 1e-4 per PDU tail of 0 to 24 us | **8 of 16** | +2.04, +3.02, +5.26, +8.35, +9.23, +9.95, +11.72, +20.70 s | 1 to 3; the tail adds slips before LOCKED too |

(`sweeps/b8_no_jitter.md`, `sweeps/b8_uniform_5us.md`, `sweeps/b8_tail_24us.md`.)
LOCKED was 6.66 s after the set in all 48 runs.

With a rare tail the slip after LOCKED lands at a random time, seconds to tens
of seconds after it, from a margin a tail event exceeds; then the ring holds.
That is the bench's shape: one slip 2.0 to 3.0 s after LOCKED in B8 and 14.7
to 44.9 s after it in B7, each followed by hundreds of seconds of hold. The
bench's arrival-time distribution is not measured, so which of the two causes
(the PI tail or lateness) produced each bench slip is not established; with
an ideal network the PI tail alone gives one phase in 16.

### Stream-to-stream switches and the controls

| Run | Result |
|---|---|
| AAF to CRF, CRF to AAF, after the INTERNAL-to-AAF set (the suite's `b8` leg, phase 0.5, no lateness; and the representative run) | LOCKED 3.04 s and 5.96 s after each (2.98 s and 6.02 s in the representative run); the trim carried; 0 ring slips. The ring's margin moved -0.02 then +0.01 tick across the two switches (0.061..0.084, then 0.046..0.061, then 0.054..0.084): below its 0.06-tick margin here, so a ring left within about 0.02 tick of its edge would slip at a stream-to-stream switch too. Each switch's recentre re-centres the render ring; after CRF to AAF its first event sits at 8.96..8.99 ticks, inside the ambiguity window (not gradable) |
| Control: the peer on the DUT's own INTERNAL clock (no offset to pull in) | 0 slips after the set; the render ring on the law throughout (fill 14, delay 8.24..8.26) |
| Control: one extra render recentre injected 4.1 s after LOCKED (harness-only input) | the render ring back on the law for the rest of the hold (fill 14, delay 8.46..8.47); the loopback ring unchanged (no recentre reaches it) |

## 3. #647 reproduced

### The case

The DUT on INTERNAL, a talker on the DUT's own clock (so nothing drifts), the
stream running and on the render law, then the TDM serial clock held, as T14
holds it in `milan_dp_render`: the physical frame divider stops, the aligner
(engaged at INTERNAL under A2-a) sees the phase step, folds it to the nearest
sample and pulls the packet grid back. Two hold lengths, folding opposite ways:
52 us (2.50 frames, +0.53 tick) and 56 us (2.69 frames, -0.33 tick). The
stream's arrival latency runs over 16 phases of one media tick.

### The mechanism, in one run (52 us hold, latency 210.42 us)

| From the hold, ms | Aligner error, cycles (1/130 sample) | Aligner trim, 1/16 ppm | #386 settle pending | Render fill at PDU end | First-event delay, ticks | Loopback ring margin, ticks |
|---|---|---|---|---|---|---|
| -10 | 0 | -83 | 0 | 14 | 8.748 | +0.837 |
| +1 | 64 | -2,136 | 0 | 14 | 8.755 | +0.853 |
| +10 | 58 | -1,996 | 0 | 14 | 8.801 | +0.899 |
| +40 | 39 | -1,522 | 0 | 14 | 8.947 | +1.037 |
| +60 | 29 | -1,266 | 0 | 15 | 9.024 | +1.121 |
| +100 | 15 | -898 | 0 | 15 | 9.132 | +1.229 |
| +160 | 1 | -490 | 0 | 15 | 9.239 | +1.336 |
| +200 | -3 | -357 | 0 | 15 | 9.277 | +1.367 |
| +300 | -8 | -134 | 0 | 15 | 9.316 | +1.405 |
| +900 | -1 | -80 | 0 | 15 | 9.262 | +1.352 |

The aligner pulls the grid half a sample in about 170 ms, at up to 133 ppm on
the packet grid. The #386 trigger never arms: the hold is neither a change of
the selected index nor a re-engagement (`milan_datapath.sv:6292-6293`), and at
INTERNAL its settle is a dwell anyway (`:6276`). The running stream keeps the
pull: fill 15 and a first event at 9.26 ticks, for good.

### The sweep: 16 feed phases, two fold directions

| Hold | Shift | On the law after | Left the law (fill / delay after) | Not gradable | Recentres |
|---|---|---|---|---|---|
| 52 us (2.50 frames) | +0.53 tick | 6 | **7 of 13 gradable**: phases 5 to 11 (15 / 9.06..9.49) | 3 (phase 4 before; 12, 13 after) | 0 in every run |
| 56 us (2.69 frames) | -0.33 tick | 10 | **4 of 14 gradable**: phases 0 to 3 (13 / 7.71..7.93) | 2 (phase 4 before; 15 after) | 0 in every run |
| Control: both, with one recentre injected 0.3 s after the hold | | **every gradable phase** (13 of 13; 14 of 14) | 0 | the same | 1 per run |

This is #643's mechanism 2 in a harness of its own: #643 measured the 0.32-tick
remainder of the same pull after T30's window opened and 23 to 30 of 66 phases
off the law; here the whole pull is graded. The loopback ring takes the same
shift (+0.56 tick in the run above); a pull toward its empty edge slips it
when its margin is smaller than the pull.

## 4. Classification

**#645 is (a), with a structural cause beside it, and not (b).**

- **(a) holds.** The servo locks frequency only. A set from INTERNAL starts
  from a 5.92 ppm offset, and the meter's 4.1 s E8 latency plus the PI's
  settling carry 1.43 ticks of phase walk from the set to LOCKED and about
  0.03 after it, in every run. Nothing removes it: the loopback ring keeps
  whatever margin the walk leaves, uniform in (0, 1) tick at LOCKED across
  set phases, and slips once after LOCKED when that margin is within the PI's
  tail (1 phase in 16 with ideal arrivals) or within a late PDU's reach (a
  rare 24 us lateness tail slips 8 of 16 phases, 2.0 to 20.7 s after LOCKED,
  from margins up to 1.1 ticks).
- **The structural cause: the loopback ring is outside every recentre.** It
  has no setpoint, so at INTERNAL the beat parks it inside one tick of its
  empty edge, and the walk of any switch from INTERNAL then slips it. The
  #386 recentre, the design's one declared discontinuity for a source change
  (`MEDIA_CLOCK_FOLLOWING.md:1044-1050`, `TIME_SYNC.md:384-385`), never
  reaches it (`milan_datapath.sv:6321-6323` feeds `KL_render_setpoint`
  alone).
- **(b) is not #645's cause**, since that recentre does not touch the ring.
  But **(b) does hold for the render ring at the same switch**: its one
  recentre fires 42.7 ms after the set, when the aligner (engaged at INTERNAL
  since A2-a) has been inside its band for 2,048 ticks, 4.6 s before the
  servo even starts and 6.6 s before LOCKED. The 1.43-tick walk then lands in
  the render latency: fill 12 or 13 and a first event at 6.58 to 7.53 ticks
  at every gradable phase, for the rest of the hold. That is #647's defect
  on a source change, which #647's acceptance names ("after any source
  change").
- **Why only from INTERNAL** (B8: no slip at AAF to CRF or CRF to AAF): a
  stream-to-stream switch passes HOLDOVER with the trim kept (W2), so there is
  no offset to pull in; its HOLDOVER and ACQUIRE windows move the phase about
  0.02 tick, against 1.43 from INTERNAL. The same-rate control confirms it: no
  offset, no walk, no slip, render on the law.

**#647 is the same family**: an aligner transient at INTERNAL moves the grid
by the folded phase step (+0.53 / -0.33 tick here), and the only recentre is
armed by an index change or a re-engagement, neither of which happens. The
render ring keeps the shift and leaves the law at 7 of 13 gradable feed phases
for a +0.53-tick pull and 4 of 14 for a -0.33-tick one.

**The common cause**: the media plane re-centres its rings once, keyed on the
aligner's band (or a dwell), after a source change only; the walk that moves
a running stream comes from the servo's frequency pull-in or from an aligner
transient, and neither is what the trigger waits for. One of the two rings,
the loopback ring, has no recentre at all.

Not observed in simulation and left open: lane B8's two slips within 1.94 s of
the binds at INTERNAL, before the set (the beat allows one per 3.52 s). A late
PDU at the stream's start would do it; the harness's start is clean.

## 5. Fix options

Area: Vivado 2026.1 synthesis out of context, xc7a100tfgg484-2 at 20 ns (the
shipping 50 MHz), the shipping 1x1 shape's parameters, each option's added
logic prototyped outside the tree (`area/*.diff`) against the module as
shipped. 0 errors and 0 critical warnings in all seven runs. The prototypes
are for area only: none is simulated or verified.

| Block | Shipped | Prototype | Delta |
|---|---|---|---|
| #386 settle block (`milan_datapath.sv:6264-6311`, standalone) | 40 LUT, 51 FF | B: 49 LUT, 52 FF; C: 56 LUT, 75 FF | B +9 / +1; C +16 / +24 |
| `KL_chan_map_capture` (4 slots, TDM8, one 8-channel LOOP stream) | 1,076 LUT, 1,336 FF, 1 BRAM tile | C: a per-stream recentre with a 7-event target: 1,115 LUT, 1,345 FF | +39 / +9 |
| `KL_mmcm_drp_servo` | 1,031 LUT, 812 FF | A: a phase term: 1,200 LUT, 941 FF | +169 / +129 |

### A. A phase term in the servo

- **What:** each window, a phase error (the followed stream's timestamp
  against local gPTP time at its arrival, folded into +/-1 ms) against a
  target captured at LOCKED, added into the window error.
- **Effect on #645:** holds the phase at its LOCKED value, so the PI's
  0.03-tick tail stops; the 1.43 ticks before LOCKED and the slips there stay,
  and the ring is still left inside one tick of its edge, where lateness still
  slips it. With a talker-relative target instead it would pull the phase to
  the talker's (the #632 / IEEE 1722-2016 10.8 work), which walks further
  during acquisition. It does nothing for the render ring's shift or for #647.
- **Area:** +169 LUT, +129 FF in the servo (the meter's phase export
  included), plus a 32-bit reference mux in the datapath.
- **Protocol-visible:** the DUT's media phase against the followed talker is
  held after LOCKED; the servo's loop and LOCKED behaviour change, so every
  servo suite and the bench lock times are re-qualified. A talker-relative
  target changes the DUT talker's presentation-time phase (#632).
- **Test plan:** the follow_ring sweep at every phase and lateness model: no
  ring slip later than one window after LOCKED with ideal arrivals; the phase
  error at the hold's end inside a stated bound; mutant: phase gain 0 (the
  tail returns at phase 0.5625). `mmcm_servo`, `aaf_clock_meter` and
  `milan_dp_mclk` re-run with their mutants.
- **Verdict:** does not remove #645 and leaves #647. Not recommended for this
  issue; it belongs with #632.

### B. A recentre keyed on the aligner's band rather than a fixed dwell

- **What:** at INTERNAL too, the settle waits for the aligner inside its band
  for 2,048 ticks (drop the `!follow_sel_r ||` term at `milan_datapath.sv:6276`),
  and an aligner excursion past four times the band, once settled, arms a
  recentre.
- **Effect:** fixes #647 for the render ring: after a pull the stream is
  re-centred once the aligner is back in band. The planted control shows one
  recentre puts every gradable phase back on the law. **It does nothing for
  #645**: at an INTERNAL-to-AAF set the aligner never leaves its band. In the
  representative run its error stays within -1..+2 cycles (the band is 2, a
  sample 130) through the set, the servo's first PI step and both
  stream-to-stream switches, because it follows the physical grid as the
  servo moves it. So the recentre still fires 42.7 ms after the set, before
  the walk, and it still reaches only the render ring.
- **Area:** +9 LUT, +1 FF.
- **Protocol-visible:** one more declared render discontinuity (one snap or
  re-prefill, up to one PDU of events at the TDM output) after each aligner
  excursion, instead of a permanent latency offset. TIME_SYNC's settle row at
  INTERNAL changes from "2048 ticks after the change" to the band rule, and the
  recentre table gains the excursion trigger. Nothing on the wire.
- **Test plan:** the follow_ring pull-in sweep at both fold directions: every
  gradable phase on the law 0.5 s after the hold, exactly one recentre per
  hold; mutant: the excursion arm removed (7 of 13 and 4 of 14 phases stay
  off, as today). `milan_dp_render`'s `[LAW]` and boundary legs unchanged
  (they grade fresh streams after the settled report); T30's INTERNAL window
  could grade the law again after the hold's recentre.

### C. A later recentre: keyed on the servo's settle, delivered to both rings

- **What:** (1) under following, the source-change settle also waits until
  the servo has held LOCKED for 8 windows (4.1 s: the PI's tail falls 0.64 a
  window, so 3 % of the post-LOCKED residual is left), with a ceiling of 2^20
  ticks (21.8 s) in place of 32,768; (2) B's INTERNAL band and excursion arm;
  (3) the same pulse to a new recentre input on the loopback ring, which
  re-centres each pair at its stream's next PDU end to a 7-event target (one
  event of the previous PDU left at every push), so its margin sits in (1, 2]
  of its (0, 3] range, a tick of tolerance each side.
- **Effect:** at an INTERNAL-to-AAF set both rings are re-centred after the
  walk has stopped: the render ring returns to the law (the planted control
  injected exactly this pulse: fill 14, delay 8.46) and the loopback ring
  moves to its centre, out of the reach of the PI's tail and of lateness up
  to a tick. Slips during the pull-in itself, before the settle, remain (1
  or 2 at the bench's 5.92 ppm; about 0.24 tick per ppm of INTERNAL-to-source
  offset at this servo's timing) and are declared as part of the switch. With
  (2) it also fixes #647.
- **Area:** +55 LUT, +33 FF at 1x1 (settle +16 / +24, loopback ring +39 / +9).
  The ring term grows with the LOOP pairs: the 8x8 shape does not build the
  loopback lane (`LOOPBACK_P = 0`).
- **Protocol-visible:** the declared switch behaviour changes: one recentre
  after a source change once the servo has settled (about 11 s after a set
  from INTERNAL at the bench's offset, against 43 ms today), the ceiling, and
  the loopback ring's recentre (one dup or drop of up to its depth on the
  DUT's transmitted loopback audio, at that instant). The loopback lane's
  latency grows by one event, 20.8 us, from the 7-event target. The render law
  itself is unchanged. TIME_SYNC's recentre and settle rows, the design's
  "Switching sources" and the loopback banner change.
- **Test plan:** the follow_ring sweep at all 16 phases and all three
  lateness models: no loopback slip after the settle recentre, the render ring
  on the law after it at every gradable phase, exactly one recentre per
  switch; the pull-in sweep as B; the stream-to-stream switches unchanged
  (their recentre also waits for 8 LOCKED windows). Mutants: the servo dwell
  removed (recentre at 42.7 ms, render off the law at every phase, as today);
  the loopback recentre input tied low (slips after LOCKED under the tail
  model); the target at 6 (margin back to (0, 1]). `milan_dp_mclk`'s
  one-recentre-per-switch rows and `milan_dp`'s true-ratio recentre count
  re-graded against the new instant.

### D. Declare a bounded behaviour

- **What:** no RTL. Declare that a switch from INTERNAL to a followed source
  at an offset of d ppm slips the loopback ring up to ceil(0.24 x d) + 1
  frames before LOCKED, and that the ring may slip once at any later time
  while a PDU arrives later than its margin; and that the render ring's
  latency after such a switch sits up to 0.24 x d events below the setpoint
  until the next recentre (a rail past 6 events, d above about 25 ppm). Grade
  the bounds in follow_ring across offsets and phases.
- **Effect:** removes nothing. The bound on the late slip is in time
  unbounded, because nothing ever re-centres the ring.
- **Area:** 0.
- **Protocol-visible:** the declared render law no longer holds for a running
  stream after a switch from INTERNAL, which needs a ruling; an audible
  discontinuity seconds to tens of seconds after LOCKED stays in the product.
- **Test plan:** a standing follow_ring sweep against the declared bounds,
  with mutants that move the PI gains or the meter's latency past them.
- **Verdict:** only as an interim declaration while C is built.

## 6. Recommendation

**C, with B's INTERNAL band and excursion arm folded into it.** It answers the
common cause of both issues: arm one recentre on every transient that moves a
running stream (a source change, a re-engagement, an aligner excursion), fire
it once both loops have settled (the aligner in band for 2,048 ticks and,
under following, the servo LOCKED for 8 windows), and deliver it to both rings,
the loopback ring gaining the recentre and the centred target it lacks. About
55 LUT and 33 FF at 1x1, no change to the servo's loop or to the render law.

It needs a ruling on three declared things before an implementation lane:

1. the settle instant and ceiling under following (8 LOCKED windows, 2^20
   ticks) and the INTERNAL band rule with its excursion trigger;
2. the loopback ring's 7-event target (+20.8 us on the loopback lane);
3. whether the pull-in slips before the settle recentre are declared as part
   of a switch from INTERNAL (they are about 0.24 tick per ppm of offset), or
   the loopback ring is also re-centred at the set itself, which saves them up
   to its tick of tolerance.

## 7. Reproduction commands

From the lane worktree, with the pinned Verilator first on PATH:

```sh
make -C tb/verilator/follow_ring            # the standing legs and the W1 arm
cd tb/verilator/follow_ring
make build
./obj_dir/Vfollow_ring --case b8 --dwell-s 1.0 --set-phase 0.5625 --hold-s 60 \
  --switch-hold-s 20 --trace pdu.csv --servo-trace servo.csv --grid-trace grid.csv
python3 trace_table.py <run.log> pdu.csv servo.csv --step-s 0.5 --from-s -1 --to-s 12
make sweep-b8 SWEEP_JOBS=8                  # 16 phases x {no jitter, 0-5 us}
python3 sweep.py b8 --exe obj_dir/Vfollow_ring --out obj_dir/sweep --jobs 8 \
  --jitter-us 2 --tail-us 24 --tail-p 1e-4 --extra --dwell-s 1.0
make sweep-pullin SWEEP_JOBS=8              # 16 feed phases x {52, 56 us}
python3 sweep.py pullin --exe obj_dir/Vfollow_ring --out obj_dir/sweep_ctl --jobs 8 \
  --hold-us 52 56 --extra --inject-recentre-s 0.3
./obj_dir/Vfollow_ring --case b8 --peer-ppm -5.10 --dwell-s 1.0 --hold-s 30
./obj_dir/Vfollow_ring --case b8 --dwell-s 1.0 --hold-s 30 --set-phase 0 --inject-recentre-s 4.1
```

A 60 s B8 run takes about 5 to 10 minutes of wall time on a loaded 16-CPU
host; a pull-in run about 30 s.

**Which build ran what.** The sweeps of sections 2 and 3 ran on builds taken
before the harness's last clean-ups: result structs instead of out-parameters,
the pull-in talker defaulting to the DUT's clock, the aligner's gains derived
from the clock ratio instead of stated, the per-millisecond trace. Each is
behaviour-preserving, and the committed harness reproduces the sweep rows:
- its `b8` leg (phase 0.5, no lateness) prints 1 slip set to LOCKED, 0 after,
  a margin at LOCKED of +0.061..+0.084 ticks and LOCKED at 6.66 s, as the
  sweep's phase 0.5 row;
- its `pullin` leg prints the 52 us, latency 200 us verdict line
  byte-for-byte as the sweep's phase 0;
- a pull-in run before and after the struct refactor printed an identical
  line;
- the derived gains are the earlier constants, 5 and 9.

The representative traces (section 2's table, section 3's table, both
controls) ran on the build with the per-millisecond trace, after the set-phase
fix that every reported sweep used.

## 8. Commits, gates and evidence hashes

### The commit

`6ca6d6686a69f2b053652149d21af63987479b4b`, parent `fea346e7`, one-line subject,
no body, no trailers. It adds `tb/verilator/follow_ring/` (`Makefile`,
`follow_ring_wrap.sv`, `sim_main.cpp`, `dp_glue.py`, `mutants.py`, `sweep.py`,
`trace_table.py`, `.gitignore`) and the suite's row in
`docs/testing/TESTING.md`. No RTL, configuration, generated or processor file.

The suite is a standing check because its default target passes on the
current RTL and grades only declared behaviour:

- `b8`: LOCKED within 15 s of the INTERNAL-to-AAF set; both stream-to-stream
  switches re-lock; no loopback slip across either. The set phase is 0.5,
  where the ring is left 0.06 tick from its empty edge, so a walk at a
  stream-to-stream switch would slip it.
- `pullin`: the stream is on the render law, or not gradable, before the hold.
- `mutants.py`: W1, a switch passing servo IDLE (the design's rejected
  option), built by a compile-time define on a copy, must fail "[SW] no ring
  slip across the AAF to CRF switch". It does.

The defects themselves are printed as `RESULT-645` / `RESULT-647` lines and
swept by `make sweep-b8` / `make sweep-pullin`, which grade nothing: a fix
lane turns them into checks.

### Gates at the head (each unpiped, its output to a file, all rc 0)

- `make -C tb/verilator/follow_ring`, a clean build with the pinned Verilator
  5.050: B8 leg 5 checks / 0 failures, pull-in 1 / 0, W1 caught; about 7
  minutes on a 16-CPU host at load 60. `scripts/suite_tally.py` reads 6
  checks over 2 tallies from its log, and `--verdict` passes. Receipt:
  `gates/suite_follow_ring.txt`; the full log is 15,539 bytes,
  sha256 `af63e058e9b16c437f190adda29e3bd886426be2b4a1f939d1e2c0d9c8ff45d2`.
- `check_cpp_idiom.py` and `--selftest`, `check_py_idiom.py` and `--selftest`,
  `check_hygiene.py --check`, `check_todo_ownership.py`, `check_sv_idiom.py`.
- `measure_test_evidence.py --check` (the new suite counted with its
  `mutants` driver; 72 <= 77 suites without an arm; 0 unexplained DUT-source
  readers) and `--selftest`; `measure_fail_fast.py --check`;
  `measure_naming.py --check`.
- `check_rtl_source_lists.py` and `--selftest`, `suite_shards.py --selftest`,
  `ci_scope.py --selftest`, `check_feature_status.py --self-test`,
  `check_baremetal_only.py --check`; `run_all_suites.sh --list` discovers
  `follow_ring` (60 default suites).
- In the pinned Markdown environment: `docs_check.py`, `check_doc_style.py`,
  `gen_toc.py --check` and `--verify-anchors`,
  `check_em_dash.py --base fea346e7` (0 findings over the 1 added line),
  `check_doc_paths.py`.
- `git diff --check fea346e7 HEAD` and `git diff --check`.

List: `gates/gates_at_head.txt`. The tree is clean after `make clean`.

Not run: no RTL changed, so no lint, Yosys or Vivado image gate; `act` and the
hosted contexts, because nothing is pushed.

### Option area runs

`area/`: the out-of-context script (`ooc_all.tcl`, `run_ooc.sh`), the
standalone settle block, the three option diffs against the shipped files,
and the seven utilisation reports. Vivado 2026.1, one process per
configuration under the shared lock, run alone.

### Evidence in this directory, and the raw traces kept outside it

| File | Bytes | Content |
|---|---|---|
| `sweeps/b8_no_jitter.md`, `b8_uniform_5us.md`, `b8_tail_24us.md` | 3,028 / 3,028 / 3,222 | the 48 B8 runs' result lines |
| `sweeps/b8_render_ring.txt` | 4,686 | each B8 run's render ring at the hold's end and its recentre instant |
| `sweeps/pullin.md`, `pullin_control_injected_recentre.md` | 6,660 / 6,638 | the 64 pull-in runs' verdicts |
| `traces/b8_phase0.5625_j5.log`, `_table.csv`, `_servo.csv` | 2,268 / 27,474 / 8,602 | the representative B8 run: its log, a 0.25 s table, every servo window |
| `traces/b8_control_same_rate.log`, `b8_control_injected_recentre.log` | 1,415 / 1,601 | the two B8 controls |
| `traces/pullin_h52_lat210.42.log`, `_grid.csv` | 894 / 135,903 | the representative pull-in run, its per-millisecond aligner and settle trace |

Raw per-PDU traces, too large to keep here (regenerate with section 7):

| Trace | Bytes | sha256 |
|---|---|---|
| representative B8 run, per PDU | 29,503,804 | `d4f603b2e96b2814bb89048efbbb9fc52247980255533a86afb1c99fcf4c0ecb` |
| representative B8 run, per millisecond | 2,718,791 | `bd5c528cf16cc775d4c75afa94f653944632a828e5e1650e51f9ce3819762641` |
| representative pull-in run, per PDU | 1,308,906 | `9994af775c38d8c2340f463a049f115dfcdf39bf41f2ad19926bb140f47e39d6` |
| same-rate control, per PDU | 8,493,670 | `893bb81dc74ee2e15599447bda286b6dddfb8be8dc0a99f0a873de77d95aa5f4` |

Bench evidence read (read-only, through the hosting service's API): lane
B8's switch-case events, `review-evidence/629-b8-r1/author/runs/sw/events.jsonl`
on branch `629-b8-review-evidence`, 43,104 bytes, sha256
`9082adeb40c7bd8b7f2d830937581f693ab1d23963091111b8180cb71465ead4`: the set,
LOCKED and the DUT's `0x8E4` / `0x748` rate words (+11.04 ppm). The 0.5 s
console poll of that case is not published, so the bench figures above are
the findings page's.
