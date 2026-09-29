[A424]

## Contents

- **[Status](#status)** -- Local gates, branch and head.
- **[Linked Issue / roles](#linked-issue--roles)** -- Relates to #617; executor and reviewers.
- **[Description](#description)** -- The frame-atomic TDM handoff, the new suite, the docs.
- **[Round 2](#round-2)** -- The guarded CRF crossing, exact slip counters, the one-pair frame check, exact latency.
- **[Round 3](#round-3)** -- The media NCO keeps its ticks, the derived keep-off, the measured envelope and the settled lock to +/-100 ppm.
- **[Authoritative references](#authoritative-references)** -- The issue, the bench evidence, the clause.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- Reviewer commands and expected results, including the defect at `ce550952`.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this does not do.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN locally at `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b` -- `617-capture-frame-atomic` ->
`dev`, ten commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215` (three from round 1, three
from round 2, four from round 3). Every assigned local gate returned rc 0 at that head (85
entries; gate table in the evidence comment). Hosted checks have not run on this head.

## Linked Issue / roles

Relates to #617

This PR covers #617 acceptance 1 to 3. Acceptance 4, a bench re-run of the #451 DIN capture
showing zero torn frames, follows on the next image, so this PR does not close the issue.

Executor: `[A424]` (round 1), `[A428]` (round 2), `[A431]` (round 3)
Internal cleared-context reviewer: `[R394]`
External reviewer: `[R395]`

## Description

On the #451 bench, 67.5% of the talker's AAF columns mixed two adjacent TDM frames: pairs 1 to 3
one frame older than pair 0, in four states cycling once per 1.958 s beat. The capture crossbar
held each TDM pair in its own latest-sample register, written by that pair's strobe, and the
media-tick walk read each register at its own slot's inject.

| Piece | Change |
|---|---|
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | The TDM bucket becomes three banks. STAGE is written by each pair strobe, as before. FRAME is published in one edge by the strobe of the frame's last pair (new parameter `TDM_FRAME_PAIRS_P`, with an elaboration guard). WALK is loaded from FRAME at the walk's snapshot and held for the whole walk, so a frame closing mid-walk waits for the next tick. The walk bank is required: an 8x8 walk (866 cycles) outlasts the two TDM slots between a frame's last pair and the next frame's first (260 cycles at 50 MHz). Round 2 moves the snapshot to the tick's own cycle and keys the junction counters on it (see [Round 2](#round-2)). |
| `hdl/milan/milan_datapath.sv` | Passes `TDM_FRAME_PAIRS_P = min(AIF_PAIRS_C, 4)`, the front end's per-frame pair supply clipped to the four pairs the bucket keeps: 4 on the shipping 1x1 TDM8 shape, 1 on the I2S shapes, 4 on the Arty blend (closing on its TDM pair 2). Round 2 rebinds the grid aligner (see [Round 2](#round-2)). |
| `tb/verilator/capture_coherence` (new) | Junction leg: the real TDM8 master, media NCO, grid aligner, crossbar and packetizer at the shipping 1x1 TDM8 shape and a 50 MHz axis clock. The #451 pattern is shifted into the TDM data pin off the master's own bclk and fsync, and every AAF column is decoded. INTERNAL runs one whole beat of the true 391/1591 plan (-10.64 ppm) and several beats at +/-1000 ppm; CRF runs locks and, since round 2, dense placed sweeps of the engagement phase; since round 3 a sub-cycle sweep at -50 ppm and the settled lock at +/-80 and +/-100 ppm, with the aligner keep-off taken from `milan_datapath`'s own declaration. Datapath leg: the same bench through the whole `milan_datapath` on the shipping shape, frames read at the MAC. `mutants.py`: the mutation arm, the first mutant being the `ce550952` per-pair law. |
| `tb/verilator/chmap_capture` | `[F]` section: columns of one PDU, each with one right answer, including a frame that closes between two of a walk's TDM slots and, since round 2, closes on the tick cycle itself. `[A]`/`[LB5]` deliver whole frames; lane B elaborates the one-pair frame of the I2S shapes, graded by `[F1]` since round 2. `[Q]` (round 3) queues a tick behind a running walk. |
| `hdl/ieee1722/crf/KL_media_nco.sv` (round 3) | The terminal compare is monotone (`>=`), so a trim update on any cycle keeps one tick per period; the contract comment states the guarantee (see [Round 3](#round-3)). |
| `tb/verilator/media_nco` (round 3) | Check 10 moves the trim on every cycle around the terminal count, every end move, both shapes. |
| Docs | `TIME_SYNC.md`: "Talker capture handoff" with the exact latency change and "The guarded crossing". `CHANNEL_MAP_64.md` section 4 and section 7. `REGISTER_MAP.md` (SLIP_TDM). `FPGA_DESIGN.md`. `TESTING.md` suite index. `CHANGELOG.md`. The traceability matrix is regenerated. |

Unchanged: the render (DOUT) path, the channel-map semantics and every port of
`KL_chan_map_capture` and `milan_datapath`. There is no processor, firmware or parent-interface
change.

Latency, exact, against `ce550952` (sample age at the walk's tick, 1x1 TDM8, 50 MHz):

| Pair | Frame atomicity | Guarded crossing (round 2) | Change |
|---|---|---|---|
| 0 | +782.3 cycles, +15.65 us | +5 cycles | +787.3 cycles, +15.75 us |
| 1 | +547.8 cycles, +10.96 us | +5 cycles | +552.8 cycles, +11.06 us |
| 2 | +313.4 cycles, +6.27 us | +5 cycles | +318.4 cycles, +6.37 us |
| 3 | +79.0 cycles, +1.58 us | +5 cycles | +84.0 cycles, +1.68 us |

`ce550952` read pair p's strobe up to tick + 6 + 26p. The head reads a frame closed by the tick
cycle, and pair p's strobe comes (3 - p) pair periods of 260.42 cycles before its frame's close:
change = 6 + 26p + (3 - p) x 260.42 cycles. The earlier pairs wait for their frame to complete,
which is what atomicity requires; pair 3's change is the read moving to the tick. The round-1
body tabled sampled means (787.7/558.2/328.7/99.1 cycles), which carry up to 20 cycles of phase
bias; the figures above are exact and are checked by the measured minimum ages (-6/-32/-58/-84
cycles at `ce550952`, 781/520/260/0 at the head).

## Round 2

Round 2 answers R394-1 (internal) and R395-1 (external), both NEGATIVE at `5546b976`, and the
#617 ruling that the CRF band be fixed in this PR.

**R394-1 F1 = R395-1 F1, the CRF repeat/skip band: fixed.** The frame-atomic handoff has one
crossing, a frame's close against the walk's snapshot. The grid aligner's keep-off guarded the
slot-0 strobe, three pair periods away, so a CRF lock could sit on the crossing and repeat and
skip frames while `SLIP_TDM`, keyed on that same slot-0 strobe, read static. Now all three meet
at one instant:

| Piece | Round 2 |
|---|---|
| Walk snapshot | in the media tick's own cycle (was the pre-walk's last cycle); a tick queued behind an overrunning walk snapshots at that walk's start |
| Coincidence | a close landing on the snapshot's cycle with no frame pending is the one the tick takes (the #74 counter law), so the walk bank loads it one cycle late |
| `SLIP_TDM` counters | marker = the frame close, consume = the snapshot: they count exactly the talker's own repeated and skipped frames |
| Aligner marker | the frame close (the slot-0 strobe on the one-pair I2S frame, as before) |
| Aligner tick | `media_tick_p` one cycle late, which puts its lock-target split on the walk's crossing: no engagement is pulled across it |
| Aligner keep-off | 256 cycles, capped at a quarter sample (`MGA_KEEPOFF_CYC_C`); the 1/128-sample default guards a settled lock but not the acquisition transient, which moves the close 149 cycles at 50 ppm (round 3 restates the envelope as a relative rate, TDM frame against the local axis clock) |

`KL_media_grid_align` itself is unchanged: its binding and a parameter only, so the ruling's
fallback (a redesign of the aligner) was not needed.

**Committed dense CRF sweep.** Each sweep calibrates where the engagement close lands and places
it at chosen offsets from the crossing:

| Sweep | Engagements | `5546b976` | Head |
|---|---:|---|---|
| true plan, every cycle across +/-32 of the crossing | 65 | 19 phases slip, 8 in the tail | 0 torn, no tail slip; one net-zero pair (below) |
| true plan, every 16 cycles round the frame | 65 | 1 phase slips | 0 torn, 0 slips |
| -50 ppm, every 4 cycles from -176 to +32 | 53 | 36 phases slip, 10 in the tail | 0 torn, 0 slips |
| +50 ppm, every 4 cycles from -32 to +176 | 53 | 37 phases slip, 10 in the tail | 0 torn, 0 slips |
| whole datapath, true plan, every 2 cycles from -20 to +4 | 13 | 7 phases slip, 4 in the tail; `SLIP_TDM` saw none | 0 torn, 0 slips, `SLIP_TDM` 0/0 |

The one engagement that still moves a frame is one whose close lands exactly on the crossing: it
may repeat and skip one frame while the pull clears the close's one-cycle jitter, net zero,
counted on `SLIP_TDM`. No settled lock slips. Removing the guard reproduces the band: the round-1
aligner binding, in the junction wrapper and in `milan_datapath`, each fail
`[C] slips while the CRF lock held`. (Round 3 corrects two claims made here. Before the NCO fix
that engagement could also lose two media ticks, and "within 64 columns" holds only within
+/-50 ppm of relative rate; see [Round 3](#round-3).)

**R395-1 F2, the one-pair frame: fixed.** `chmap_capture` `[F1]` drives lane B's pair 0 alone
(`TDM_FRAME_PAIRS_P = 1`) with a fresh value per walk; each column must carry its own frame.
RM1 (the close on the bucket's last pair whatever the frame length) fails it.

**R395-1 F3 = R394-1 S1, the latency table: fixed** as above, in `TIME_SYNC.md`, the pair-3
sentence and `CHANGELOG.md`.

**Suggestions taken.** The counters and the aligner no longer key on slot 0, and the suite, the
crossbar banner, the `media_grid_align` wrapper and `REGISTER_MAP.md` say so (R394-1 S2, R395-1
S3). The Arty blend's I2S pair waits for the TDM close, up to a frame (R395-1 S1, `TIME_SYNC.md`).
The stale `tdm_hold_r` comment in `milan_dp`'s `sim_nxn.cpp` now names the port the check reads
(R395-1 S2).

**Cost.**

- Latency: +5 cycles (0.1 us) on the 1x1 shape, 2 on the 8x8 product shape, from reading at the
  tick.
- Area: `KL_chan_map_capture` OOC at 1x1 TDM8, LUT 1263 -> 1265, FF 1384 -> 1384, BRAM 0; at the
  8x8 product shape LUT 2103 -> 2132, FF 1931 -> 1931 (Yosys 0.66). `milan_datapath` adds one
  flop.
- Engagement: a CRF capture within 256 cycles of the tick (half of engagements at 50 MHz) is
  pulled out to 256 cycles at up to 64 ppm of NCO trim before it locks, and the #386 settled-grid
  trigger waits for that pull. A probe of the head's datapath at 50 MHz measured the recentre
  682.7 ms after the selection for a fully pulled engagement (the trigger's 32,768-tick ceiling)
  and 486.9 ms for an unpulled one. `milan_dp_render` T30 and `milan_dp` aclk pass unchanged; T30's
  CRF residual walk now measures -0.5339 ppm (was -0.8009), recorded in `TIME_SYNC.md`.

## Round 3

Round 3 answers R394-2 (internal) and R395-2 (external), both NEGATIVE at `377d1ac3`, under the
[round-3 rulings](https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5879911799).
Four commits on `377d1ac3`: the NCO fix with its direct test, the capture and crossbar tests,
the documents, and an em-dash spelling fix to one table row.

**Ruling 1 (R395-2 F1), the lost media ticks: fixed in `KL_media_nco`.** `end_w` follows the
registered trim live, and the #74 aligner moves that trim on every TDM frame, at whatever phase
the frame holds. A trim update landing on the cycle the count sat at the old end, and lowering
the end, put the count one past it; the `==` terminal compare then ran the count to its 11-bit
wrap and the grid lost two ticks (a 3,089-cycle period at 50 MHz). The period now ends on the
first cycle the count reaches or passes the end. The contract comment states the guarantee:

- one tick per period whatever cycle an update lands on, never lost or doubled, no wrap;
- an update that lowers the end below the count ends the period on that cycle, one cycle past
  the new end (two only for a step larger than the servo's authority can make): a one-time
  phase step the loop absorbs, never a lost sample or a rate change;
- at a steady trim the grid is bit-for-bit what it was, so INTERNAL is unchanged.

No port or parameter changed. The checks:

| Check | At the head | At `377d1ac3` |
|---|---|---|
| `media_nco` check 10: every move of the period's end, landing on each cycle from three before the terminal count to the next period's first, both shapes | 410 checks, 0 failures | 10 failures, exactly the trials that land past the new end (3,089-cycle period at 50 MHz) |
| `capture_coherence` `CRF-fine-50`: -50 ppm, the crossing and the side before it, every quarter cycle at 64 sub-step phases (768 engagements) | 0 failures; 141 on-crossing engagements repeat and skip once, net zero, last at column 57 | 27 failures: 9 engagements repeat once and skip twice |
| R395-2's `run_fine.sh -50 -1 2`, their probe re-derived from this head by their own scripts | 0 failures in 20,544 checks | 9 failures (R395-2's receipt, reproduced byte for byte) |
| R395-2's `run_fine.sh -60 -1 2`, likewise | 0 failures in 20,544 checks | 98 failures |
| Mutant: the `==` compare restored | killed in `media_nco` (check 10) and in `CRF-fine-50` (`[C] CRF slips net zero`) | - |

One correction to the premise, stated so it can be checked: **the -60 ppm failures were not the
NCO race.** With only the NCO compare changed, R395-2's packaged -60 ppm probe log is byte for
byte the same (98 failures). Every one is a single net-zero repeat and skip of an on-crossing
engagement that clears slowly, because the net departure at 60 ppm is only 64 - 60 = 4 ppm (last
slip at column 181). That is the 64-column window being wrong beyond +/-50 ppm, which ruling 3
corrects. The -60 ppm run passes with the corrected window.

NCO area (`KL_media_nco` alone, the `ooc.sh` recipe, Yosys 0.66): at 50 MHz LUT 101 -> 106,
FF 46 -> 46, CARRY4 35 -> 37; at 100 MHz LUT 103 -> 104, FF 47 -> 47, CARRY4 35 -> 37; one
DSP48E1 and no BRAM either way. Every suite that instantiates the NCO passes (below).

**Ruling 2 (R395-2 F2 = R394-2 S2), the keep-off constant: taken.** The junction wrapper no
longer restates 256. At build time `mga_keepoff.py` copies `milan_datapath`'s own
`MGA_SAMPLE_CYC_C` and `MGA_KEEPOFF_CYC_C` declarations out of the datapath source into the build
directory. The wrapper elaborates them against its own clock. A datapath mutant therefore reaches
the junction leg. The mutation arm's new `band50` leg runs the placed +/-50 ppm bands (every 32
cycles) against that binding. RM5 (keep-off 128 in `milan_datapath`) is killed there by
`[C] slips while the CRF lock held`.

**Ruling 3 (R394-2 F2 = R395-2 F3), the envelope: measured.** The envelope is a relative rate at
the aligner: the TDM frame against the local axis clock. A +/-50 ppm Milan source does not bound
it, because the local oscillator may run +/-100 ppm off.

| Term | Value |
|---|---|
| Pull on a raced engagement | 64 ppm: the proportional term at one 256-cycle keep-off |
| Pulled-engagement margin | 256 - 4 x the rate cycles: 56 at 50 ppm, 16 at 60, none at 64 |
| On-crossing engagement limit | about 63 ppm below nominal and 67 above (net zero at -62 and +66, carried across at -63 and +68) |
| Unpulled transient | about 3 cycles per ppm: 149 at 50 ppm, 238 at 80, 299 at 100 |
| Transient limit | about 86 ppm (no crossing at 86; crossings at -88 and +90) |
| Settled lock | no slip, measured to +/-100 ppm |

| Relative rate | Engagement on the crossing | Unpulled engagement | Settled lock |
|---|---|---|---|
| within +/-50 ppm | one repeat and one skip, net zero, by column 57 (every sub-cycle phase) | transient under the keep-off, 107 cycles clear | no slip |
| 50 ppm to the on-crossing limit | one repeat and one skip, net zero, later as the rate nears the pull: column 87 at 55 ppm, 181 at 60, 294 at 62 | under the keep-off | no slip |
| on-crossing limit to about 86 ppm | carried across and back: one repeat and one skip by column 6,300 at 80 ppm | under the keep-off | no slip |
| beyond about 86 ppm | carried across and back, by column 11,100 at 100 ppm | crosses and returns: one repeat and one skip by column 13,100 at 100 ppm | no slip, measured to +/-100 ppm |

Every slip is acquisition, nets zero and is counted on `SLIP_TDM`. The settled lock is
committed: `CRF-settle` at -80, +80, -100 and +100 ppm, two engagements each (on the crossing,
and 256 cycles off on the side the transient crosses), 30,000 columns. No slip in any lock
tail, and `[V]` holds. A recorded run of 52 engagements across the whole frame at 60,000 columns
has no tail slip. So the settled lock is guarded to +/-100 ppm, and there was no STOP.

The `kEngageColumns` derivation is corrected. At the Milan bound the net departure is
(64 - 50) ppm, 0.0146 cycles per frame. The close moves a cycle, its jitter, in 68 frames, and
the first column comes about four frames after the engagement: 64 columns (measured 57). Beyond
the bound the window stretches as (64 - 50)/(64 - rate): 224 columns at 60 ppm. It has no bound
at the pull. A CRF run's lock tail never starts inside its window. For every committed scenario
that is still the second half. For R395-2's 300-column -60 ppm probe it starts at column 224. The
latency table is scoped to the 1x1 TDM8 shape at 50 MHz with TDM pairs 0 to 3 on talker slots
0 to 3, and the change for other clocks and slot mappings is stated (R394-2 S3).

**Ruling 4 (R394-2 F1 vs R395-2 S1), the aligner banner: comment only.** The settle-band sentence
is scoped to the module default. A pointer names the `milan_datapath` binding: 256 cycles, the
tick one cycle late, and the #386 recentre waiting for the pull, up to its 32,768-tick ceiling.

**Ruling 5 (R394-2 S1), the queued-tick snapshot: taken.** `chmap_capture` `[Q]` delivers a
frame, ticks, then closes a frame mid-walk. A second tick queues behind the running walk and a
third frame closes after it. The walk must keep its frame on every pair. The queued tick's walk
must take the frame closed last. The counters must show one skip and no dup. RM7 (no late
snapshot) fails `Q: col 2 pair 0 L is frame 4` and the skip count. RM8 (a snapshot at the tick)
tears column 1 and fails `Q: col 1 pair 2 L is frame 2`.

**Ruling 6, the documents.** `TIME_SYNC.md` "The guarded crossing" (the tables above), the
loop-fact row for the NCO, the `SLIP_TDM` reading in `REGISTER_MAP.md`, the crossbar banner
(`KL_chan_map_capture.sv`), the `milan_datapath` binding comment, `CHANGELOG.md`, `TESTING.md` and
the `media_nco` README state the corrected guarantee and envelope. "One repeat and one skip, net
zero, within 64 columns" was re-measured at every sub-cycle phase at -50 ppm (`CRF-fine-50`,
last slip column 57) and +50 ppm (recorded, column 8), and it is now stated for +/-50 ppm only.

**Mutation arm:** 27 of 27, 8 clean controls and 19 mutants. The new ones are RM5 (`band50`),
the `==` compare (`nco` and `fine`), and RM7 and RM8 (`chmap`).

**Cost.** RTL: the NCO's compare (area above); comments elsewhere. No latency change: at a steady
trim the grid is bit-for-bit what it was, and the keep-off value is unchanged. Suite time:
`capture_coherence` now takes about 21 minutes locally (1,236 s in the gate run; run alone, the
junction leg takes 241 s and the mutation arm 862 s), against about 15 in round 2.

## Authoritative references

- #617 body, the round-1, round-2 and round-3 assignments (manager decisions: frame-atomic
  handoff at the crossbar input; no added sample of latency; render path and channel-map
  semantics unchanged; committed simulation in INTERNAL and CRF with drift; removed-atomicity
  mutant; resources on 1x1 TDM8; the CRF band fixed in this PR with a dense sweep and a
  guard-removal mutant; round 3: the NCO fixed in this PR, the derived keep-off, the envelope as
  measured with the settled lock to +/-100 ppm).
- R394-1, R395-1, R394-2 and R395-2 on this PR.
- PR #616, `docs/findings/451_TDM8_FIRST_LIGHT.md` section "DIN frame coherence", and its
  review R392-1 (F2, the re-derivation against `KL_chan_map_capture.sv:486-487,959-960`).
- IEEE 1722-2016 7.3.5: AAF-PCM carries sample events in order, one sample per channel per
  event. Milan v1.2 7.4: media clock source tolerance.
- `docs/CHANNEL_MAP_64.md` section 4; `docs/design/TIME_SYNC.md` "Media boundary" and "Talker
  capture handoff"; `docs/reference/REGISTER_MAP.md` `0x8D8` `SLIP_TDM`.

## How to get into the same state

```sh
git fetch origin
git checkout 617-capture-frame-atomic
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
make -C tb/verilator/capture_coherence      # junction leg, datapath leg, mutation arm (about 21 min)
make -C tb/verilator/chmap_capture
make -C tb/verilator/media_nco
python3 scripts/lint_rtl.py --check
OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture
```

Expected result / pass criteria:

- `capture_coherence: checks: 20832 failures: 0` (junction leg), `capture_coherence_dp: checks:
  332 failures: 0` (datapath leg), and the mutation arm's `27 checks: 27 PASS, 0 FAIL`: eight
  clean controls and nineteen mutants, each caught by its named check.
- `KL_chan_map_capture: 371 checks, 0 failures` and the netlist pin `20 checks, 0 failures`.
- `media_nco: 410 checks: 410 PASS, 0 FAIL`.
- Every CRF settled lock is slip-free, measured to +/-100 ppm relative rate. Acquisition slips
  net zero, inside the engagement window. Within +/-50 ppm the only such engagements are those
  landing on the crossing, last slip by column 57.
- The NCO race reproduces at `377d1ac3`: build `media_nco` and the junction harness with
  `NCO_SRC` set to that commit's `KL_media_nco.sv`. `media_nco` then reports 10 failures, all in
  check 10, and the junction's `--fine` run 27 failures in 9 engagements. At the head R395-2's
  `run_fine.sh -50 -1 2` and `-60 -1 2` report 0 failures each, with their probe re-derived from
  this head by their own scripts.
- The defect reproduces at `ce550952`, measured in round 2 with the round-2 harness. Build it
  with that commit's `KL_chan_map_capture.sv` and `milan_datapath.sv`. Set the wrapper's aligner
  binding back to that commit's (slot-0 marker, `tick_w`, default keep-off) and drop its
  `TDM_FRAME_PAIRS_P` line. The junction leg then reports 386 failures in 5,240 checks, with
  INT-true 66.1% torn in the #451 states 0,0,0 33.9%, -1,-1,-1 / 0,-1,-1 / 0,0,-1 22.0% each. The
  datapath leg reports 7 failures in 311 checks.
- The band reproduces at `5546b976` (that commit's crossbar, datapath and aligner binding; round-2
  harness): 414 failures in 5,240 junction checks and 25 in 311 datapath checks, the placed sweeps
  slipping as tabled in [Round 2](#round-2).

## Known limitations / out of scope

- Bench acceptance 4 (#617) needs the next image.
- A CRF engagement may slip while it acquires, inside a measured envelope of relative rate: the
  TDM frame against the local axis clock, which a +/-50 ppm Milan source does not bound. Within
  +/-50 ppm only an engagement landing on the crossing does: one repeat and one skip, net zero,
  by column 57. Beyond that its window grows as the rate nears the 64 ppm pull. Past the
  on-crossing limit (about 63 ppm below nominal, 67 above) a raced engagement is carried across
  and back. Past the transient limit (about 86 ppm) an unpulled one is too. Each is one repeat and
  one skip, net zero, counted on `SLIP_TDM`. No settled lock slips, measured to +/-100 ppm.
- The on-crossing and transient limits come from recorded probe runs, not committed sweeps. The
  +/-50 ppm behaviour and the +/-80 and +/-100 ppm settled lock are committed.
- On the Arty blend shapes the crossbar's four-pair TDM bucket keeps the I2S pair and TDM pairs
  0 to 2. TDM pair 3 was already unreachable through the crossbar before this change.
- Area is the standalone OOC estimate; the in-context datapath delta and placed Vivado
  utilization are not measured here.
- `capture_coherence` now takes about 21 minutes locally (15 in round 2, 6 in round 1). That is
  within the sweep's 1,800 s per-suite guard, with less margin; the hosted duration is not yet
  observed.

## Definition of Done

- [x] Linked Issue acceptance criteria 1 to 3 are satisfied (4 follows on the next image)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (gate table in the evidence comment)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
