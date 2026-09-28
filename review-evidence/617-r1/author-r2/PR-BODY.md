[A424]

## Contents

- **[Status](#status)** -- Local gates, branch and head.
- **[Linked Issue / roles](#linked-issue--roles)** -- Relates to #617; executor and reviewers.
- **[Description](#description)** -- The frame-atomic TDM handoff, the new suite, the docs.
- **[Round 2](#round-2)** -- The guarded CRF crossing, exact slip counters, the one-pair frame check, exact latency.
- **[Authoritative references](#authoritative-references)** -- The issue, the bench evidence, the clause.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- Reviewer commands and expected results, including the defect at `ce550952`.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this does not do.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN locally at `377d1ac3658feb8d544e6ed1005b186b67127f35` -- `617-capture-frame-atomic` -> `dev`,
six commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215` (three from round 1, three from
round 2). Every assigned local gate returned rc 0 at that head (79 entries; gate table in the
evidence comment). Hosted checks have not run on this head.

## Linked Issue / roles

Relates to #617

This PR covers #617 acceptance 1 to 3. Acceptance 4, a bench re-run of the #451 DIN capture
showing zero torn frames, follows on the next image, so this PR does not close the issue.

Executor: `[A424]` (round 1), `[A428]` (round 2)
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
| `tb/verilator/capture_coherence` (new) | Junction leg: the real TDM8 master, media NCO, grid aligner, crossbar and packetizer at the shipping 1x1 TDM8 shape and a 50 MHz axis clock. The #451 pattern is shifted into the TDM data pin off the master's own bclk and fsync, and every AAF column is decoded. INTERNAL runs one whole beat of the true 391/1591 plan (-10.64 ppm) and several beats at +/-1000 ppm; CRF runs locks and, since round 2, dense placed sweeps of the engagement phase. Datapath leg: the same bench through the whole `milan_datapath` on the shipping shape, frames read at the MAC. `mutants.py`: the mutation arm, the first mutant being the `ce550952` per-pair law. |
| `tb/verilator/chmap_capture` | `[F]` section: columns of one PDU, each with one right answer, including a frame that closes between two of a walk's TDM slots and, since round 2, closes on the tick cycle itself. `[A]`/`[LB5]` deliver whole frames; lane B elaborates the one-pair frame of the I2S shapes, graded by `[F1]` since round 2. |
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
| Aligner keep-off | 256 cycles, capped at a quarter sample (`MGA_KEEPOFF_CYC_C`); the 1/128-sample default guards a settled lock but not the acquisition transient, which moves the close 149 cycles against a 50 ppm source (Milan v1.2 7.4's tolerance) |

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
within 64 columns, counted on `SLIP_TDM`. No lock phase slips. Removing the guard reproduces the
band: the round-1 aligner binding, in the junction wrapper and in `milan_datapath`, each fail
`[C] slips while the CRF lock held`.

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

## Authoritative references

- #617 body, the round-1 assignment and the round-2 assignment (manager decisions: frame-atomic
  handoff at the crossbar input; no added sample of latency; render path and channel-map
  semantics unchanged; committed simulation in INTERNAL and CRF with drift; removed-atomicity
  mutant; resources on 1x1 TDM8; the CRF band fixed in this PR with a dense sweep and a
  guard-removal mutant).
- R394-1 and R395-1 on this PR.
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
make -C tb/verilator/capture_coherence      # junction leg, datapath leg, mutation arm (about 15 min)
make -C tb/verilator/chmap_capture
python3 scripts/lint_rtl.py --check
OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture
```

Expected result / pass criteria:

- `capture_coherence: checks: 5240 failures: 0` (junction leg), `capture_coherence_dp: checks:
  311 failures: 0` (datapath leg), and the mutation arm's `19 checks: 19 PASS, 0 FAIL`: five
  clean controls and fourteen mutants, each caught by its named check.
- `KL_chan_map_capture: 318 checks, 0 failures` and the netlist pin `20 checks, 0 failures`.
- Every CRF scenario (281, placed and fixed) holds its lock slip-free; the one engagement placed
  on the crossing itself repeats and skips one frame at engagement, net zero.
- The defect reproduces at `ce550952`: build the same harness with that commit's
  `KL_chan_map_capture.sv` and `milan_datapath.sv`, and set the wrapper's aligner binding back to
  that commit's (slot-0 marker, `tick_w`, default keep-off) and drop its `TDM_FRAME_PAIRS_P`
  line. The junction leg then reports 386 failures in 5,240 checks, with INT-true 66.1% torn in
  the #451 states 0,0,0 33.9%, -1,-1,-1 / 0,-1,-1 / 0,0,-1 22.0% each. The datapath leg reports
  7 failures in 311 checks.
- The band reproduces at `5546b976` (that commit's crossbar, datapath and aligner binding): 414
  failures in 5,240 junction checks and 25 in 311 datapath checks, the placed sweeps slipping as
  tabled in [Round 2](#round-2).

## Known limitations / out of scope

- Bench acceptance 4 (#617) needs the next image.
- A CRF engagement whose frame close lands exactly on the walk's crossing may repeat and skip one
  frame, net zero, before the aligner pulls it clear; no lock phase slips.
- The keep-off guarantee covers media clock sources within about +/-75 ppm of the local grid;
  Milan v1.2 7.4 bounds them at +/-50 ppm.
- On the Arty blend shapes the crossbar's four-pair TDM bucket keeps the I2S pair and TDM pairs
  0 to 2. TDM pair 3 was already unreachable through the crossbar before this change.
- Area is the standalone OOC estimate; the in-context datapath delta and placed Vivado
  utilization are not measured here.
- `capture_coherence` now takes about 15 minutes locally (6 in round 1), within the sweep's
  per-suite guard.

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
