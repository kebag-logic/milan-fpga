[A659]

## Contents

- **[Status](#status)** — Round 7c's test-only repair of a GM-step control that dev's own campaign fails too, the re-recorded resource gate under the owner's area decision, the gate tally, and `632-764-media-phase` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why, rounds 1 to 7.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Round 7c at `c2c996fa`: every gate of the local bar passes.** The head `417ec528` adds one comment and docs commit on it: the grandmaster-change citations name IEEE 802.1AS-2011, the edition Milan v1.2 profiles, and the doc style, gPTP docs and docs checks pass on it.
Round 7 (the [A10] assignment issuecomment-6351804497) merges dev `e5b480a3`, the fourth pin adoption (#771), into
this branch: `dc9cda7d`, a merge commit, with the seven conflicted files resolved hunk by hunk. Processor `93fb0b2d`
carries processor PR #199's stored-offset gate, so the `[NOTIFY]` SET_STREAM_INFO case passes at the merged head (461
checks, 0 failures) and `gsi-mutants` catches all eleven controls. Round 7 stopped on the route's slice growth against
#771's record (+107, tolerance 80). The owner accepted this PR's area (round 7b, the [A10] comment
issuecomment-6357449062): it extends the block-RAM exception (#632 issuecomment-6309313685) to the measured +500 LUT,
+376 FF and +107 slices, and Mark II (#640) recovers the area. Round 7b re-records the three endpoints under both
exceptions (`17280d2d`, documented in `d835ba12`) and runs the local bar. It stopped on `gmstep-mutants`, 21 of 22:
the control "the grandmaster change stops the talker for good" failed the leg, but not its named check, and dev
`e5b480a3`'s own campaign fails it the same way.

Round 7c (the [A10] ruling issuecomment-6360257772) settles that. The adopted gPTP pin (FPGA-gPTP #82) makes the station
its own grandmaster from boot, and leaving its own identity for GM A is a grandmaster change (IEEE 802.1AS-2011 9.6.2.1,
10.2.3.13, the edition Milan v1.2 profiles), so the datapath's detector is right to pulse there and nothing in the RTL changes. **This PR repairs dev's
`gmstep-mutants` campaign** (`c2c996fa`, test-only): the control's planted stop now takes effect at the leg's own GM A ->
GM B event, the driver names the failed checks of every control, and the clean leg records the boot pulse, with a new
control that must fail that record. At `c2c996fa` `gmstep-mutants` passes 23 of 23, and the firmware boundary gate, the
docs gates, lint and `check-baseline` pass; the full sweep passes 63 of 64 suites (2,190,061 checks, 0 failures), and the 64th, `capture_coherence`, stopped by the runner's 2,400 s wall clock, passes when run alone (exit 0 in 2,402 s, its campaign 35 of 35).

Round 6, at `d40e2ee8` before the merge (the [A10] assignment issuecomment-6341411985, answering R677-3
and R678-3), puts the listener's late rule per event in the RTL: a PDU stamped before the latest domain event presents its
events still ahead and refuses only the ones already past, as the stage, the design page and the harness model always
said; one stamped more than the late reach (504 frames) behind is late in every event, since no PDU the depacketizer
passes carries more. route-1x1: LUT -26, FF +389, slices +72 against #708's record (round 5: +309, +343, +68), RAMB18 +2
as budgeted, WNS +0.163 ns; the fix takes 4 of the 12 slices round 5 left. The three explicit campaigns the reviews
named are run whole on the head's RTL and tests (`2700584e`; the head adds one design-page paragraph): the shipping
TDM8 render inventory 31 of 31, its 18-phase pull-in and history leg, the GM-step inventory 22 of 22. T26 can fail
again, the retired render law is out of the time and recovery pages, and
the stale figures are corrected.

Round 5 (the [A10] ruling issuecomment-6320617745, with the owner decision issuecomment-6320453361) revised round 2's
offset rounding: an AAF talker applies its presentation time offset exactly as set (Milan v1.2 5.4.2.9), and only the
CRF output keeps IEEE 1722-2016 10.7 Equation (14)'s round-up, with its 33-bit carry. GET_STREAM_INFO reads an AAF
output's offset as set and the CRF output's as applied (5.4.2.10.2). The listener's queue stays sized for the 2 ms
default offset, and its supported range is stated exactly per shape.

Round 4 brought the listener's presentation at the pin, R678-1-F1, into this PR: each sample reaches its interface's
pins at its AVTP presentation time, through a presentation stage indexed by the timestamp, in block RAM; the #386
render law is retired. The processor's SET_STREAM_INFO change gate (R677-2-F1, option (b), issuecomment-6312625146)
is merged in the processor (`51f88c7e`, processor PR #199); the fourth pin adoption (#771, processor `93fb0b2d`)
brought it to `dev`, and round 7 merges that here. `632-764-media-phase` -> `dev`. The bench proof follows after
merge.

## Linked Issue / roles

Relates to #632
Relates to #764

#632's simulation acceptance items are met: the talker, the media clock and, since round 4, the listener at the pin
(R678-1-F1, brought back into this PR by the round 4 assignment after the [A10] ruling issuecomment-6306187740 had
scoped it out). #632's bench item, and #764's bench proof, follow after merge with the #764 method, so neither Issue
is closed by this PR.

Executor: `[A659]`
Internal cleared-context reviewer: `[R677]`
External reviewer: `[R678]`

## Description

### Round 1

The media servo locked frequency only, so each engagement kept whatever phase its pull-in left. #764 measured the
DUT's own CRF output and its AAF stream off the followed CRF stream's timing points, with a constant -0.46 Ps between
the two. This PR phases the one media-clock master, `KL_mmcm_drp_servo`, to the followed CRF stream, against one
phase reference per clock domain, and gives each media interface its own derived latency constants relative to it.

| Piece | Change | Clause |
|---|---|---|
| Domain media event (`KL_media_domain_event`, new) | Each frame's instant at the media interface: the frame-timing owner's closing-pair strobe, back-dated by that owner's marker latency. One per clock domain. Every consumer of the domain takes its instant from it | IEEE 1722-2016 4.3.5 |
| Per-interface constants (`KL_media_if_latency_pkg`, new) | Marker latency counted to the closing pair's last bit, plus the front end's FIFO write and the read side; slot k's MSB offset. Derived from each interface's own parameters, never mirrored | 4.3.5, 10.8 |
| Phase detector and loop (`KL_mmcm_drp_servo`) | Per accepted, consumed CRF PDU, the domain event less its timestamp, folded exactly into +/-Ps/2 in 1/3 ns (Ps = 62,500/3 ns), summed over the 512 ms window's nominal 256 PDUs. It enters the integrator one window late, clamped: type 2 against phase, the rate loop as its damping, the pull slew-limited to 0.5 ppm. The integrator keeps 8 fractional bits, so odd errors are carried (the #764 floor leak, up to 1.95 ns/s) | Milan v1.2 7.6.1; IEEE 1722-2016 10.7 Eq. (14), 10.8 Eq. (15) |
| Hold conditions | Outside LOCKED, an `mr` toggle, a broken reference history, a local PHC step (#539) or policy slew (#545): the term lets go and the open window is spoiled | 10.8 |
| Window cap | A window keeps at most 264 samples (256 + 1/32) | 10.8 |
| Settled status | `MCSRV_STAT[9]`, a previously reserved read-only bit | 10.8 |
| CRF output (`KL_crf_tx`) | Every 96th domain event is a timing point, stamped with its instant plus the Equation (14) offset; the free-running /512 /96 divider and its clock crossing are retired | 10.7 Eq. (14), 4.3.5 |
| CRF receive (`KL_crf_rx`) | Publishes each consumed PDU's timestamp (`ts_p_o`, `ts_o`) | 10.8 |
| AAF talkers (`KL_chan_map_capture`, `milan_datapath`) | The capture crossbar banks each frame's instant beside the frame and loads it into the walk with it; the talkers stamp that instant, so capture age and pair offset leave the timestamp | 4.3.5, 10.8 |

The -0.46 Ps is accounted for in full ([accounting](docs/design/MEDIA_CLOCK_FOLLOWING.md#the-measured--046-ps)).
Two `milan_dp` fixtures were re-timed for the CRF talker's domain-event cadence; their checks are unchanged.

### Round 2

Answers R678-1 and R677-1 under the [A10] round 2 rulings on this PR.

| Finding | Change | Clause |
|---|---|---|
| R678-1-F3 | The phase is circular: each folded sample is unwrapped against a tracking reference (the last counted window's phase, or the first sample since a hold) before it is summed, and the window phase is re-folded once. Samples either side of +/-Ps/2 now sum as the half-period phase they are and pull at the slew limit; folded alone, alternate +/-10,416 ns samples summed to zero and read settled. Settled now needs the window phase and every sample of four full windows inside the band, so no mean of out-of-band samples settles. The no-stall wording is corrected | 10.8 Eq. (15); Milan v1.2 7.6.1 |
| R678-1-F4 | The window snapshot reads the hold on its own edge, so a hold on the very edge a window closes starts no correction from the invalidated era; a window that closed a cycle earlier still commits, as the rate update does | 10.8 |
| R678-1-F2 (revised in round 5: AAF offsets as set, the rounding the CRF output's alone) | Every stream output's presentation offset is applied rounded up to whole media clock periods by `KL_crf_tx`'s own Equation (14) rule (`KL_mtt_round`, new, one round-robin divider), and GET_STREAM_INFO reads back the applied value: 2,010,000 ns applies as 97 periods, 2,020,834 ns, where the raw value sat 0.48 Ps off the CRF timing points. The CRF output stamps the rounder's row too (`KL_crf_tx` `ROUND_MTT_P = 0`, its own converter not elaborated), so one rounding serves every output | 10.7 Eq. (14), 4.3.5, 10.8 |
| R677-1-F1 | The I2S blend now closes each frame on its I2S pair, the last of the frame to reach the crossbar, back-dated by the I2S front end's latency (`close_slot()`, `close_is_i2s()`, `KL_chan_map_capture.TDM_CLOSE_SLOT_P`). Grading it with sample values at both interfaces' pins found a second defect: `KL_aaf_capture_i2s`, and the flat `aaf_talker_i2s` it was split from, copied the crossing FIFO's registered read on the pop edge, so every strobe carried the pair before it. Both now alias that read as the TDM front ends do | 4.3.5, 10.8 |
| R677-1-F2, F3 | Cases and planted defects for the local PHC step hold, the settled flag's timing and its mirror, and the fold-range guard | 10.8 |
| R677-1-F4 | `media_phase`'s budget basis re-measured: the whole default target in 578 s at three case jobs | -- |
| R677-1-F5, R678-1-R1 | The three stale CRF-divider texts corrected as written; the reviewer lines above | -- |

No top-level port and no register-map layout change: `MCSRV_STAT[9]`'s read-only meaning is tightened. Module
changes: `KL_mtt_round` is new; `KL_chan_map_capture` gains `TDM_CLOSE_SLOT_P`, defaulted to its old behaviour;
`close_pair()` loses its blend argument.

**Resources.** route-1x1 under the recipe, checked by `pp_resource_gate.py` against the recorded baseline:

| Figure | Record | Round 1 (`a6ae20f9`) | Round 2 (`f1643214`) | Round 3 (`62ee1a8c`) | Round 4 (`bb9a9200`) | Round 5 (`5b502a05`) | Delta to record | Tolerance / floor |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | 49,709 | 49,733 | 50,077 | 49,922 | +309 | +500 |
| FF | 52,353 | 52,641 | 52,760 | 52,765 | 52,775 | 52,696 | +343 | +600 |
| Slice | 15,725 | 15,785 | 15,797 | 15,804 | 15,801 | 15,793 | +68 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 74 / 25 | 74 / 27 | 74 / 27 | 0 / +2 | +0 (RAMB18 +2 budgeted by the owner, round 4) |
| DSP | 14 | 14 | 13 | 13 | 13 | 13 | -1 | +0 |
| WNS | +0.215 ns | +0.276 ns | +0.305 ns | +0.282 ns | +0.123 ns | +0.108 ns | -0.107 | at least +0.030, fall at most 0.25 |
| WHS | +0.036 ns | +0.032 ns | +0.036 ns | +0.016 ns | +0.036 ns | +0.015 ns | -0.021 | at least 0, fall at most 0.25 |

Rounds 1 to 3: route complete, no unrouted net; gate exit 0, with "re-baseline recommended" for the DSP the image
no longer uses; one slice of headroom at round 3. Rounds 4 and 5: see their Area paragraphs. The round 3 carry costs about 10 LUTs in its own blocks against the round 2
route (`pres_round` +1 LUT / +3 FF, `KL_crf_tx` +1 / +1, the datapath's GET_STREAM_INFO word +8 / +1) and no block
RAM; the rest of the movement is placement in unchanged RTL. `81f09d06`, the carry's first form, routed to the same
figures. Round 2's per-block account: against a route of the recorded inputs the servo grew by 382 LUTs and 200 FFs, the offset rounder adds 148 and
190, and `KL_crf_tx`, its own converter and multiplier block no longer elaborated, shrank by 109 and 142. The worst
setup path is the SoC's write-beat counter into a block RAM enable, outside this PR. The first rounder used a
multiplier block against a DSP tolerance of zero; the shipped one divides by shifted adds and serves the CRF row too.

### Round 3

Answers R678-2 and R677-2 under the [A10] round 3 assignment (issuecomment-6306591168).

| Finding | Change | Clause |
|---|---|---|
| R678-2-F1 | The rounder keeps each row's bit 32 (`KL_mtt_round` `ofs_c_o`): rounding up can pass 2^32 - 1 ns, and 0xFFFFFFFF applies as 206,159 periods, 4,294,979,167 ns. The CRF output adds it into its 64-bit timestamp (`KL_crf_tx` `transit_c_i`), so it no longer stamps 2^32 ns early (about 8,962 ns off its grid modulo Ps). The AAF talkers keep the low word, exact for a 32-bit timestamp. GET_STREAM_INFO reads a row through the rounder (`rb_row_i`, `rb_ns_o`), as 0xFFFFFFFF past 32 bits, never its low word. One rounder, one readback | IEEE 1722-2016 10.4.13.1 Eq. (13), 4.4.4.9 Eq. (6), 10.7 Eq. (14); Milan v1.2 5.4.2.10.2 |
| R678-2-F1, tests | `media_phase` `ofs` grades every row on all 33 bits and GET_STREAM_INFO's word, and every CRF timestamp on all 64 bits against an independent Equation (14) result and the frame grid, at 4,294,958,333 ns (the largest that rounds under 2^32), 4,294,958,334 ns (the first past it) and 0xFFFFFFFF, from factory rows in reset, from rows set at reset, and at run time both ways. The grader's 32-bit cast and its skip past 2^31 are gone. Planted: the carry dropped at the conversion, the reset load, the readback and the CRF output's sum (the truncation), each killed at its named check | as above |
| R677-2-F1 | `milan_dp` `[NOTIFY]` grades SET_STREAM_INFO's push in R677-2's four steps (the held 2,000,000 ns; 2,010,000; the same again; the write-back of 2,020,834), each with the push's value and GET's applied value. Its planted control, the gate comparing with the applied readback again, is a microcode mutant in `gsi_mutants.py`. The docs scope "what a controller reads" to GET_STREAM_INFO and state the SET echo against the applied readback. The processor gate itself is the open decision: see Status and below | Milan v1.2 5.4.2.9, 5.4.2.10.2, 5.4.5.1, 5.4.5.2; IEEE 1722.1-2021 7.5.2 |
| R677-2-F2 | `det afterhold`: settled near 0, an `mr` hold, then samples straddling +/-Ps/2; the window phase reads the half-period phase and the committed correction is the slew limit's. Planted: the hold keeping the old reference (theta 0) | 10.8 |
| R677-2-F3 | This body's figures: 404 LUTs and 8 slices; the campaign's count | -- |
| R677-2-R1..R5, R678-2-R1, R2 | Review labels out of every source comment; the datapath fold comment; the listener scope in the design doc, TIME_SYNC.md, CHANGELOG and this body | -- |
| Found here | The first form of the carry wrote `{carry, low word}` as one indexed concatenation target. Verilator and Vivado took it, but Yosys dropped it: the rounder synthesized to 0 cells while the open-synthesis gate still printed PASS. Each row's low word and carry are now two indexed writes, the reset values from an elaboration-time table (1,215 cells). The gate accepting a zero-cell top is a follow-up outside this PR | -- |

**The processor gate (the decision).** Measured on the real datapath and processor, the committed case, the 1x1
notify leg, with the microcode applied uncommitted to the pinned submodule:

| Processor | step 1 (held) | step 2 | step 3 (same) | step 4 (write-back) | SET 0 on a never-set row (probe) | leg |
|---|---|---|---|---|---|---|
| processor `2cbed0a9`, then the pin (gate reads GET_STREAM_INFO's word) | 0 | 1 | **1** | **0** | 1 | 3 failures |
| (a) as ruled: one read of the stored row | **1** | 1 | 0 | 1 | **0** | 2 failures |
| (b) the stored row once a controller set it, GET_STREAM_INFO's word before (the E_SCFG idiom of #178) | 0 | 1 | 0 | 1 | 1 | 0 failures |
| expected | 0 | 1 | 0 | 1 | 1 | |

The processor's store reads a row no controller has written as 0 with its valid bit clear, while the integrator
serves the factory 2 ms. So (a) pushes for a SET of the factory value and stays silent for a SET of 0, which moves
the offset in force from 2 ms to 0. (b) is five more microcode words. With (b), the planted control is caught at step
3. Ruled (b) (issuecomment-6312625146): Round 3b below.

### Round 3b

The [A10] ruling (issuecomment-6312625146) chose option (b) and kept R677-2's four-step case as specified.

- **The processor change** (protocol-processor `632-sinfo-notify-stored`, `175a5a15`, `0b097464` and `51f88c7e` on
  processor main `08023123`). E_SINFO compares the commanded offset with the stored row once a controller or a
  restore has set it (the store's valid bit, E_SCFG's idiom for #178), and with the integrator's GET_STREAM_INFO
  word while the row is unset: five more microcode words. `51f88c7e` keeps a D3 test's latency measurement on the
  arm its timed SET takes, the two arms reaching the store a cycle apart. Its processor-level test, `tb/pp_top` section NS, runs against a face that
  answers GET_STREAM_INFO's word as this repository's integrator does (whole 48 kHz periods once set, the factory 2 ms
  before): an identical SET pushes nothing, a changed SET pushes once, a SET of 0 on a row never set pushes once, and
  a first SET equal to the factory value pushes nothing. Two planted defects each fail their named checks: the
  GET_STREAM_INFO compare restored on the set arm (fails the identical SET and the write-back) and the never-set arm
  dropped (fails the factory SET and the SET of 0).
- **The consumer, measured here** with the processor head's E_SINFO applied uncommitted to the submodule at its pin
  (the ROM byte-identical to round 3's option (b) ROM), then the submodule restored to its pin:

| Measure | Result |
|---|---|
| `[NOTIFY]` SET_STREAM_INFO, the timed leg (`make -C tb/verilator/milan_dp notify`) | 441 checks, 0 failures; pushes 0, 1, 0, 1 over steps 1 to 4 |
| its planted control (`python3 tb/verilator/milan_dp/gsi_mutants.py 9`) | caught at step 3, 3 failures of 441 |
| a SET of 0 on the CRF output's never-set row (a disposable probe, never committed) | one push; GET then reads 0; a SET of 2 ms back pushes once |

- **Docs** (`3fdaea3d`): the design doc states both arms of the gate, the SET of 0 on an output never set, and the
  factory-offset residue below.
- **The residue** (recorded by the ruling, not a finding): before an output's first SET, the gate compares with
  GET_STREAM_INFO's word, the offset as applied, so a factory offset that is not whole periods compares as applied
  and a SET of exactly that value pushes. Every factory offset this repository ships is 2 ms, whole periods.

### Round 4

The [A10] round 4 assignment (issuecomment-6316458183), with the owner decisions on #632 (issuecomment-6309219099,
issuecomment-6309313685): every listener sample reaches its interface's pins at its presentation time (R678-1-F1).

| Piece | Change | Clause |
|---|---|---|
| Presentation stage (`KL_render_queue`, new; replaces `KL_render_setpoint`) | A queue of media events per stream, indexed by presentation frame. At each PDU's header the stage divides d = `avtp_timestamp` - E_n exactly by Ps (in thirds of a ns: long division of 3d, one quotient bit per cycle, the remainder rounding to the nearest) and writes the PDU's first event in frame n + round(d / Ps), event k k frames later, for a PDU of any length; on domain event n each interface reads frame n + K_i. Rows modulo 128 at 48 kHz in two inferred block-RAM banks (bank = lane[0] ^ row[0]), synchronous read, block-RAM style, no device primitive; the consumed frame's rows are written all zero after its reads, and a flushing stream's read resets the banks' output register | IEEE 1722-2016 4.4.4.9, 7.5 |
| Supported range (the depth) | Derived, never mirrored: 2.126 ms plus the event latency, plus two frames, rounded up to a power of two: 128 rows at 48 kHz. Written for every interface from 31.1 us to 2.656 ms ahead of its presentation time at arrival (1x1) | Milan v1.2 4.4.2.1 |
| Late, too early, untimed | A PDU with an event on a frame every interface has read (late) or past the queue (too early), or without `tv`, or whose payload starts before its frame is known (untimed): those events dropped, the PDU counted once (`late_o`, `early_o`, `untimed_o`); late and too-early PDUs counted together in `refused_o`, `RENDER_STAT[31:16]`. Gaps and overlaps in `slips_o` | 1722-2016 4.4.4.5, 4.4.4.9 |
| Out-leads (`KL_media_if_latency_pkg`: `out_pipe_ns`, `out_lead_frames`, `out_lead_ok`) | K_i, the whole frames from the event's frame instant to the frame start at interface i's pins that adopts the read, derived from the event latency and the interface's read-to-adoption path: 2 on the 1x1 TDM8, 1 on the 8x8 TDM32. The datapath refuses at elaboration an out-lead its shortest and longest paths would put on different frame starts | 10.8, 4.3.5 |
| Depacketizer | Its read side parses `tv` and the timestamp (`hdr_p_o`, `hdr_ts_o`, `hdr_tv_o`) and holds the payload `PAY_LEAD_CYC_P` = 16 cycles behind them (the frame is known after 11) | 4.4.4.5, 4.4.4.9 |
| Stream start, gPTP step, media-clock hold | A fresh stream starts at its first presentation time, silence before, no prefill. A step moves E_n and the talkers' timestamps together: queued frames keep their rows, the frame count does not step, nothing re-centres; a PDU placed across the two time bases is refused or slips, counted. A frame-grid hold delays the frames already queued by the hold; later PDUs, placed on the moved grid, take over within the lead, with one counted slip | 10.8; Milan v1.2 7.6.1 |
| What replaces #386's and #387's recentres | Nothing needs them: every PDU carries its own presentation time against the domain event, which steps with the PHC and follows the frame grid through every source change. #386's prefill, rails and at-switch recentre and #387's render re-base are retired; #645's settle recentre stays, for the capture crossbar's LOOP queues only. The builder's census pins the stage's flush to the bind wipe and refuses a new reader of the PHC strobes | -- |
| `RENDER_STAT` (`0x8DC`) | Fields re-defined: `[7:0]` the frames queued past the consumed one, `[8]` idle, `[9]` converged (presenting 100 ms running), `[31:16]` refused PDUs; reset `0x100`, selection and structural zero unchanged | -- |
| `KL_i2s_playback` (the Arty I2S DAC) | Unchanged, out of scope by the owner's decision | -- |

**Tolerance.** With the timestamps on the domain's frame grid, every sample is at its presentation time inside 10.8's
+/-5 % of Ps (1,042 ns at 48 kHz); at any other phase at the frame instant nearest it, within Ps / 2.

**At the pins (item 3).** `tb/verilator/media_phase` `render`: one `KL_render_queue` reads two render interfaces of
one domain, a TDM8 (A, K = 2) and a TDM4 a frame-long output hold behind it (B, K = 3), and the existing slot-MSB
decoder reads every slot of both interfaces' pins. 13 checks, 0 failures: every sample at its presentation time
inside +/-5 % of Ps with the timestamps up to 4 % off the grid (the largest error 833.5 ns at A, 874.2 ns at B,
the planted phase itself); at the nearest frame at every phase to +/-0.45 Ps (pin less (presentation time - phase):
0.2 ns at A, 40.9 ns at B); every sample of a presented PDU at holds of 0.1 to 2.6 ms; the late, too-early and
untimed PDUs counted once each and presented nowhere. The planted controls, each killed by its named check: B's
constant dropped, the queue read untimed, every PDU a frame off, the late rule removed (and the early rule). On the
shipping datapath, `milan_dp_render` decodes the 1x1 TDM8 pins the same way: the feed's first event at +0.6 ns from
its presentation time, then every slot within 15.1 ns over 22 windows (the serial window, INTERNAL, CRF, the
deselect and eighteen fresh `[LAW]` streams); 263 checks on the shipping leg.

**Re-graded (item 1).**

| Suite | Until #632 | Now |
|---|---|---|
| `render_setpoint` -> `render_queue` | the fill law per PDU | the stage byte-exact against a model of the law on two shapes (two streams, two interfaces, 8 lanes; one stream at 7 lanes), every rule, the lap, the flush, the slips, the 2^32 wrap, PDUs of 40 and 300 events, `refused_o`; 22 planted defects, all caught |
| `milan_dp` (`aclk`, true clock ratio) | the fill law, the PHC-step and source-change recentres | at the stage's output, every event once, in order, at its presentation time (largest 13.1 ns): from the stream's first event, three ticks of arrival shift each way, a 65,536 ns adjtime and an absolute settime under the stream (the talker's time moved with them), the late, too-early and untimed PDUs, the CRF selection and the deselect; `RENDER_STAT`'s fields against the stage's taps; 182 checks. Controls: each PDU placed by its arrival, the untimed PDU placed, a step that resets the stage, a source change that flushes it (4 of 4); the CSR controls (3 of 3) |
| `milan_dp_gm_steps` | one counted re-base at the step | the 1.5 s grandmaster change: the PDUs stamped in the new time before this listener stepped refused and counted (2), their frames one slip, every other PDU at one send-to-presentation offset (3,945 cycles) before and after; 195 checks. Controls re-planted: the stage emptied on the identity or on the step; the refusals uncounted; a gap uncounted |
| `follow_ring` | the render ring re-centred by the settle recentre | the presentation stage on the domain event: after and across each settle (b8's set and switches, the pull-in, B17's binds) every event once, in order, at its nearest frame, no slip; the settle recentre on the loopback ring alone (48, 19, 30 checks). Controls remapped and SETTLE-FLUSH added (6 of 6 run) |
| `milan_dp_render` | the fill law at the pins | every slot at its presentation time (above); `[LAW]`'s eighteen fresh streams; the source changes; `[PULLIN]`'s nearest frame after the hold |
| `milan_dp_mclk` | one #386 recentre per switch | never more than one #645 settle recentre per switch; the 0.8 s row grades the request and the toggles (55, 32, 49 checks; 31 of 31 controls) |

**Area (item 4).** Vivado out of context (`-directive AreaOptimized_high`), `KL_render_queue` alone with every tap: at
1x1 (one 8-channel stream, 48 kHz, 2.126 ms) 2 RAMB18, 0 LUTRAM, 553 LUTs, 228 FFs; at 8x8, 6 RAMB36, 0 LUTRAM, 890
LUTs, 387 FFs. The #386 stage it replaces took 456 LUTs (128 of them LUTRAM) and 185 FFs at 1x1, 2,041 (1,024 LUTRAM)
and 390 at 8x8. Inside the budget of one RAMB36 per 8-channel stream; no LUTRAM.

route-1x1 at `bb9a9200` (the Resources table under Round 2): LUT +464, FF +422, slices +76 against +500, +600 and
+80; RAMB36 unchanged; RAMB18 +2, the budget; DSP 13; WNS +0.123 ns, WHS +0.036 ns; route complete, no unrouted net.
`pp_resource_gate.py check` exits 1 on RAMB18 alone, the budgeted growth, until the record takes it. Four slices of
headroom are left. The stage's first route (`6631b0b2`) read LUT +582: the stage then took 596 LUTs in the datapath's
view, and blocks this PR does not touch moved by up to 150 LUTs between that route and round 3's (+275 at synthesis,
+462 after placement). `2d786e8b` and `bb9a9200` cut the stage to 494 in that view, its behaviour unchanged: the frame
by long division of 3d against the constant Ps (a 16-bit remainder), rounded from the remainder in an eleventh cycle;
the write data steered by the bank bit; the flush mask moved into the banks' read reset (an invalidated word is all
zero); one refused counter for `RENDER_STAT` in place of the datapath's adder; frame numbers two bits past the row
index (bounded at elaboration); and the walk's frame kept in F0's own register.

**Found here (Robustness).** The stage's first form indexed a PDU's events with three bits, so a PDU of more than eight
events (not a Milan one; the depacketizer bounds a PDU by its frame FIFO alone, at 504 one-channel events) wrote its later events over its first
frames, where the #386 stage, a FIFO, had no such limit. `bb9a9200` keeps the walk's frame per event from F0, and once
an event is past the queue the PDU's later events are refused with it, before a frame number could wrap; the unit
suite's `[long]` phase places a 40-event PDU (the last ten past the queue) and a 300-event one, and two planted
defects (the three-bit index; the hold removed) fail it.

### Round 5

The [A10] ruling issuecomment-6320617745 (AAF talkers apply the presentation time offset exactly as set; only the CRF
output keeps the Equation (14) round-up), with the owner decision issuecomment-6320453361 (the render queue is sized
for the 2 ms default offset; state the supported range exactly).

| Piece | Change | Clause |
|---|---|---|
| AAF talkers | Each stamps its offset row as set: `aecp_pres_offset` straight into the packetizer. An AAF timestamp is its frame's instant plus the offset, to the ns, modulo 2^32 | Milan v1.2 5.4.2.9; IEEE 1722-2016 4.4.4.9 |
| CRF output | `KL_mtt_round` rounds the CRF output's row alone (`g_pres_crf`, one row; no instance at a shape without a CRF output) up to whole media clock periods, all 33 bits into `KL_crf_tx`'s 64-bit timestamp | 10.7 Eq. (14), 10.4.13.1 |
| GET_STREAM_INFO word 3 | An AAF output's row as set; the CRF output's through the rounder's readback, 0xFFFFFFFF past 32 bits | Milan v1.2 5.4.2.10.2 |
| Write-back | Not idempotent on the CRF output alone (2,010,000 ns reads 2,020,834; writing that back applies 2,041,667); an AAF output reads back what was set | 5.4.2.9, 5.4.2.10.2 |
| Supported range | 31,119 ns to 2,656,119 ns ahead of the presentation time at arrival on the 1x1 shape, 25,942 ns to 2,650,942 ns on the 8x8; outside it the too-early or late rule refuses and counts the PDU; a talker accepts any offset from 0 to 0x7FFFFFFF ns; every shipping STREAM_INPUT declares `buffer_length` 2,126,000 ns, which the queue backs (IEEE 1722.1-2021 7.4.77.1) | Milan v1.2 4.4.2.1, 5.3.7.6, 5.4.2.9 |

**Re-graded.** `media_phase` `ofs`: four AAF outputs and the CRF output, eleven cases, the ruled offsets 0, 1, 20,833,
20,834, 62,500, 2,000,000, 2,010,000 and 0xFFFFFFFF ns each on AAF rows and on the CRF row (4,294,958,333 and
4,294,958,334 on the CRF row too), set at reset and at run time: every AAF timestamp a frame instant plus its row as
set, to the ns; GET_STREAM_INFO reading each AAF row as set and the CRF row as applied; the CRF row on all 33 bits and
every CRF timestamp on all 64 against an independent Equation (14) result and the frame grid; each AAF output's
phase against the CRF timing points equal to its row as set less the CRF row as applied, modulo Ps (largest 0.33 ns).
93 checks, 0 failures. On the shipping datapath, `milan_dp`'s output walk (nxn legs, 4x4 and 8x8) now requires every
stamp of every output to be a domain media event's instant plus the offset GET_STREAM_INFO reads, at 2 ms, 1 ms and
2,010,000 ns (AAF as set, CRF applied), with the frame grid live. `[NOTIFY]`: the four SET_STREAM_INFO steps keep
their pushes (0, 1, 0, 1) on AAF output 0, where GET_STREAM_INFO now reads each value as set and step 4 is a plain
change; the same four steps run on the CRF output, where the readback is applied, so the processor gate's planted
control is still caught (on an AAF output the readback equals the stored value, and that control would have nothing
to catch).

**Planted defects.**

| Defect | Where | Named check that fails |
|---|---|---|
| the AAF rows stamped rounded (round 2's binding) | `media_phase` `ofs_wrap` | `[ofs A] every AAF timestamp is a frame instant plus its row as set, to the ns` |
| the AAF rows read back rounded | same | `[ofs A] GET_STREAM_INFO reads every AAF row as set` |
| the CRF row stamped as set; the carry dropped at the conversion, the reset load, the readback and the CRF sum | `KL_mtt_round`, `KL_crf_tx`, `ofs_wrap` | the `[ofs B]`/`[ofs H]`/`[ofs A]` CRF checks |
| GET_STREAM_INFO reads the CRF row as set | `milan_datapath` (`gsi_mutants.py`) | `[NOTIFY] SET_STREAM_INFO CRF step 2: GET_STREAM_INFO reads the offset applied, whole periods` |
| GET_STREAM_INFO reads every row rounded (round 4's binding) | same | `[NOTIFY] SET_STREAM_INFO step 2: GET_STREAM_INFO reads the offset as set` |
| the processor gate compares with GET_STREAM_INFO's word | processor microcode (`gsi_mutants.py`) | `[NOTIFY] SET_STREAM_INFO CRF step 3: 2,010,000 ns again modifies nothing` |
| the CRF output stamps its row as set; the AAF talkers stamp theirs rounded | `milan_datapath`, planted once on the nxn leg | `#632 every CRF timestamp, all 64 bits, is a domain media event's instant plus its offset applied`; `#632 every AAF timestamp is a domain media event's instant plus its offset as set, to the ns` |

**Area.** route-1x1 at `5b502a05` (the Resources table under Round 2): LUT +309, FF +343, slices +68 (twelve left),
RAMB18 +2 as budgeted, DSP 13, WNS +0.108 ns, WHS +0.015 ns, route complete; the gate exits 1 on RAMB18 alone. Against
round 4: LUT -155, FF -79, slices -8. The rounder, post-place: 149 LUTs and 193 FFs at two rows, 131 and 159 at one.
Out of context (`AreaOptimized_high`): `KL_mtt_round` takes 215 LUTs and 193 FFs at two rows (round 4's 1x1), 386 and
427 at nine (round 4's 8x8), 182 and 159 at one: removing the AAF rows saves 33 LUTs and 34 FFs at 1x1 and 204 and
268 at 8x8 in the rounder, the AAF readback becoming a mux on the rows as set. An identity mode would keep the AAF
rows' registers, so removal is the cheaper. Untouched blocks moved by up to 150 LUTs between the two routes. Yosys:
`milan_datapath` 1,770,334 cells (round 4: 1,771,134).

**Spec text, published.** IEEE 1722-2016 4.3.5 (whole periods between streams of one media clock) and 10.8 Equation
(15) (a CRF-following talker within +/-5 % of a period of the timing points) hold for AAF offsets of whole periods, the
factory 2 ms among them. With any other offset the AAF stream sits the offset's fraction of a period off the CRF
timing points (2,010,000 ns: 0.48 of a period); the ruling takes the offset as set (5.4.2.9) there, and a listener that
presents each sample at its own timestamp absorbs it. The design page and the compliance matrix say so.

### Round 6

The [A10] round 6 assignment (issuecomment-6341411985), answering R677-3 (issuecomment-6341403630) and R678-3
(issuecomment-6339307135).

| Item | Finding | Outcome |
|---|---|---|
| 1 | R677-3-F1: a PDU stamped before the latest domain event lost its on-time events | Fixed in the RTL to the per-event rule; the six texts and the model state that one rule; `[behind]` on both queue shapes, with the whole-PDU refusal planted and killed on each |
| 2 | R678-3-F3, R677-3-F3: full campaigns at the final head; T26 could not fail | All three campaigns run whole at `2700584e`, receipts below; T26 can fail again (the two-stream leg) and kills `ungated commit` |
| 3 | R678-3-F1: the retired render law in the authoritative pages | TIME_SYNC, GM_LOSS_RECOVERY and MEDIA_CLOCK_FOLLOWING corrected; the bind measurement marked pre-#632 |
| 4 | R678-3-F2, R677-3-F2: stale figures | Corrected with provenance, and re-measured where this round changed them |
| 5 | R678-3-R1: residue | The three comments name behaviour, not rounds |

**The per-event rule (item 1).** IEEE 1722-2016 4.4.4.9 and 7.5: event k of a PDU is presented k periods after the
PDU's timestamp, and each event is judged on its own frame. The stage now divides the signed difference: at each
header it takes d + LATE x Ps, LATE = 504 frames (10.5 ms at 48 kHz, a multiple of three so the bias is whole ns), and
F0 = n - LATE + round((d + LATE x Ps) / Ps). Every d from 504 frames behind the latest event to past the queue divides
the same way, and the walk judges each event late (F <= R), too early or written. A PDU stamped more than 504 frames
behind is late in every event: no PDU walks more than 504 events (`MAX_EV_P`, which the datapath derives from the
depacketizer's 2048-byte frame FIFO: 252 payload beats, two samples each), so its last event is at or before the
latest event's frame, which every interface has read. The quotient grows to 10 bits (the frame is known 13 cycles
after the header; the depacketizer holds the payload 16) and frame numbers to 10 bits, sized at elaboration from the
reach (`g_chk_wrap`). The wrapped difference is read from 2^31 ns plus the reach behind to 2^31 ns less the reach
ahead. A PDU with both a late and a too-early event (only one longer than the queue) counts once in `refused_o`,
`RENDER_STAT[31:16]`, and once in each of `late_o` and `early_o`.

The texts that disagreed now say that rule: the stage banner, the design page's rule table (now "per event"), TIME_SYNC's
late row (and a "late reach" row), `REGISTER_MAP.md` `RENDER_STAT[31:16]` ("PDUs with a refused event, once per PDU;
a counted PDU's other events may still be presented"), the datapath's comment, this body, and the harness model (it
now reads the difference in the stage's window and counts `refused_o` once per PDU).

**The check (item 1).** `render_queue` `[behind]`, on both shapes (two streams and two interfaces at 8 lanes; the
shipping one stream at 7 lanes): the reviewer's probe PDUs (a frame behind; 0.3 Ps behind; the control 0.3 Ps ahead
with the same frames late), 250 frames behind with its last 47 events ahead, the longest PDU 200 frames behind (late,
presented and past the queue in one PDU), the longest 500 behind with its last event ahead, the longest exactly at the
reach (divided, every event late), and one frame past the reach (refused whole, every event late). Every presented
beat byte-exact against the model; the late, early and refused counts equal both the model's and the counts the
phases declare for their own PDUs (R677-3-S3: the hard-coded 2 and 4 are gone). 39 and 38 checks, 0 failures.

| Planted defect | Shape | Named check that fails |
|---|---|---|
| a PDU stamped behind the latest event refused whole (the former rule) | both | `[behind] every event presented to every interface is the frame the law names` |
| the late reach short of the longest PDU | two-interface | same |
| a PDU with both a late and a too-early event counted twice in `refused_o` | two-interface | `[refused] PDUs with a late or too-early event counted once each in refused_o` |

The queue campaign is 26 planted defects, all caught (28 of 28 with the two clean shapes). Two harness repairs came
with the phase: `[wrap]` now checks that it starts before its frames cross 2^32 ns (the longer refusal phases had
moved the crossing out of it, which the 31-bit-difference control caught by surviving; the crossing moved to frame
3200), and `[long]` adds a 504-event PDU, so the past-the-queue hold still has a PDU whose frame numbers would pass
half their wrap without it. The reviewer's probe, re-run: its patch on `ee5ece60` reproduces 32 and 20 mismatched
beats; the same three PDUs on this head present every on-time event, 0 mismatched.

**Area (item 1).** route-1x1 at `0ffcd7f0` (RTL as the head), against the unchanged record:

| Figure | Record | Round 5 (`5b502a05`) | Round 6 (`0ffcd7f0`) | Round 6 vs round 5 | Bar |
|---|---|---|---|---|---|
| LUT | 49,613 | 49,922 (+309) | 49,587 (-26) | -335 | +500 |
| FF | 52,353 | 52,696 (+343) | 52,742 (+389) | +46 | +600 |
| Slices | 15,725 | 15,793 (+68) | 15,797 (+72) | +4 (8 left) | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 27 | 74 / 27 | 0 | RAMB18 +2 budgeted; the gate exits 1 on it alone |
| DSP | 14 | 13 | 13 | 0 | -- |
| WNS / WHS | 0.215 / 0.036 ns | 0.108 / 0.015 | 0.163 / 0.017 | +0.055 / +0.002 | met; route complete |

The fix takes 4 of the 12 slices round 5 left. The stage alone, synthesised out of context with the route's
directive and a 20 ns clock, both RTLs under the same script: 538 LUTs and 228 FFs before, 527 and 236 now (-11, +8);
without the clock, at 1x1 531/236 (round 4's measurement of the stage it replaces: 553/228) and at 8x8 883/402
(890/387), 2 RAMB18 and 6 RAMB36, no LUTRAM. In the routed image the datapath moves -42 LUTs and +48 FFs at
synthesis; the per-instance view moves logic across the hierarchy between the two routes (the stage +272 LUTs and the
CSR block -424 at synthesis, the CSR block unchanged), so the totals and the stage's own synthesis are the figures.
Worst setup path: the SoC bus's AXI-Lite bridge to the SPI flash PHY (100 MHz), outside this change.

**T26 (item 2).** Since #632 a bind fall or reset also empties the stage's queue for its stream, so on the one-stream
shape the crossbar a closed epoch re-seeds holds silence, and T26 could not see an ungated commit. The ship leg keeps
T26 as the end-to-end property (held by the flush and the epoch together). The multi-stream leg now grades it where the
epoch alone holds it: stream 1's loss holds the epoch closed (its freshness waits for stream 1's post-flush event)
while stream 0 keeps feeding, so the crossbar offers live samples, and a map write re-seeds slot 0 with another live
stream-0 channel; no slot may carry a sample, and the adapter's gate stays closed (120 stream-0 events presented to the
crossbar in the window, 0 nonzero slots). `ungated commit` runs on that leg and fails `T26 MAP WRITE IN A CLOSED EPOCH:
the re-seeded crossbar value never reaches a slot, though the other rendered stream still feeds it` (833 nonzero slots
in its replay before the commit; the campaign at the head catches it by that name). The clean leg at the head: 79
checks, 0 failures, the window 119 frames, 120 stream-0 events, 0 nonzero slots.

**Campaigns (item 2).** Run whole, each in its own clean clone, with its command, head, start and end and exit
status in the receipts; every named kill reconciled one-for-one with the inventories by the external review's own
audit script, pointed at these receipts (20 of 20, 3 of 3, 3 of 3, 20 of 20; every pull-in phase).

| Campaign | Command | Head | Result |
|---|---|---|---|
| shipping TDM8 render, the full inventory | `make -C tb/verilator/milan_dp_render tdm8render-mutants` | `2700584e` | exit 0, 31 checks, 31 PASS: the five clean modes (ship serial, epoch, law, pull-in; the multi leg whole), the three leg-side defects caught (stopped render clock, one changed sample, INTERNAL selected), the three clean controls passing (the two arrival-skew models and gray under bit skew), and all 20 gateware and shape mutations caught by their named checks, `ungated commit` by the two-stream T26 |
| shipping render pull-in, 18 boot phases and the standing phase after the serial, CRF and LAW history | the Makefile's `tdm8render-pullin` recipe, four legs at a time | `2700584e` | every leg exit 0: each of the 18 phases 28 checks, 0 failures, one settle recentre for the LOOP queues after the hold; the history leg 272 checks, 0 failures. The legs ran on the clean shipping binary the TDM8 campaign's `tdm8render-build` made at the same head (sha256 recorded), so no third build ran beside the two campaigns |
| GM steps, the full inventory | `make -C tb/verilator/milan_dp_gm_steps gmstep-mutants` | `2700584e` | exit 0, 22 checks, 22 PASS: the clean gmstep leg (195 checks, the #621 small-step phase included) and the option-off leg, then all 20 controls, each on the whole leg, caught by their named checks |
| `follow_ring` controls | `make -C tb/verilator/follow_ring mutants SWEEP_JOBS=1` | `d40e2ee8` | exit 0, 16 of 16 caught |
| `milan_dp` render controls | `render_mutants.py`; `make -C tb/verilator/milan_dp render-csr-controls` | `d40e2ee8` | 6 of 6 (two clean legs, four controls); 3 of 3 (two controls caught, the absent stage passing) |

`d40e2ee8` differs from `2700584e` in one design-page paragraph. The local-bar line of the Definition of Done is
checked again on this evidence (it was not supported before it).

**Retired law out of the pages (item 3).** TIME_SYNC: a PHC step re-bases no render queue; PHC steps keep `tu` and
holdover, and presentation sees a step only as the queue's refusals and slips; the pending-area passage now states the
implemented law, the owner's block-RAM decision and the remaining bench proof (the #764 method, with #117).
GM_LOSS_RECOVERY: the default render controls empty the queue on the identity change or the step and fail `render:
every PDU not presented was refused by the stage and counted once`; the 20-control inventory listed; the simulation
table row reads the queue's refusals, slip and offset. MEDIA_CLOCK_FOLLOWING: the bind measurement is marked as taken
before #632, its render recentre the #386 stage's; the harness now grades the settle recentre on the LOOP queue and the
stage on its law. The compliance matrix's 4.4.4.3 row no longer names a render re-base.

**Figures (item 4).** The design page's stage figures are this round's measurement, with round 4's (553/228,
890/387) named as the stage it replaces; its proof table and `TESTING.md` read 26 queue defects, and
`measure_test_evidence_readers.py` twenty-six; `TESTING.md` reads sixteen `follow_ring` controls (twice); "once an
event lies past the queue". The CHANGELOG's media_phase count reads forty.

Two controls in other suites patch the divider and kept their meaning through the bias: `media_phase`
`render_read_untimed` (the first frame every interface still reads, now `LATE_C + K_max + 1` from the biased base)
and `milan_dp` `render_mutants.py`'s arrival-placed PDU (a constant 1,875,000 ns, plus the bias).

### Round 7

The [A10] round 7 assignment (issuecomment-6351804497) composes this PR with the fourth pin adoption (#771, dev
`e5b480a3`).

| Item | Outcome |
|---|---|
| 1. Merge dev `e5b480a3` | `dc9cda7d`, a merge commit on `d40e2ee8` (no rebase, no amend); protocol-processor at `93fb0b2d`, gptp-processor at `55680bff`. Seven files conflicted: CHANGELOG, MEDIA_CLOCK_FOLLOWING, BAREMETAL_FIRMWARE, MILAN_COMPLIANCE_MATRIX, TESTING, `sw/builder/test_builder.py` and the `milan_dp_mclk` README. Each hunk was resolved from the three versions. Dev's facts are kept: #761's per-output CRF request and `mr` wording, its `mcr_restart_p_w` on both edges of the selected CRF's lock, #637's map-record campaign row and #771's changelog section. This PR's are kept too: the retired #386/#387 render re-base, the queue's bind-wipe-only flush and the presentation law. The builder bank passes at the merge, so the resolved PHC-net census rows match the RTL |
| 2. `[NOTIFY]` SET_STREAM_INFO | Passes at the merged head: 461 checks, 0 failures, all eight steps. `gsi-mutants` catches 11 of 11; the three #632 controls fail 3 checks of 461 each. The "fails at the current pin" statements are gone from the design page, the `milan_dp` README, the CHANGELOG and this body (`5282b8b6`) |
| 3. Resource gate | Measured at the merge: route-1x1 exits 1 on SLICE +107 (tolerance +80) and RAMB18 +2 (excepted); ooc-1x1 and ooc-8x8 exit 0 with the record's figures. Round 7 stopped there; the owner accepted the area, and round 7b re-records all three (below) |
| 4. Gates | Round 7b, at `d835ba12`: all pass but `gmstep-mutants` (21 of 22, STOP, below). Round 7c, at `c2c996fa`, after the test-only repair (below): `gmstep-mutants` 23 of 23, the boundary gate, the docs gates, lint, `check-baseline` and the full sweep (the sweep's 64th suite, `capture_coherence`, passing when run alone after the runner's wall clock stopped it) |

**route-1x1 against #771's record.** dev `e5b480a3`'s synthesis inputs differ from the record's measured commit
(`d664cf54`) by one comment block in `milan_datapath.sv`, so the record is dev's own route and these are this PR's
share on the current dev:

| Figure | Record | Merge `dc9cda7d` | Delta | Tolerance |
|---|---:|---:|---:|---:|
| LUT | 50,759 | 51,259 | +500 | 500 |
| FF | 52,832 | 53,208 | +376 | 600 |
| Slice | 15,728 | 15,835 (15 of 15,850 left) | **+107** | 80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 27 | 0 / +2 | 0 / 0, RAMB18 excepted |
| DSP | 14 | 13 | -1 | 0 |
| WNS / WHS ns | +0.291 / +0.036 | +0.236 / +0.028 | -0.055 / -0.008 | 0.25 |

The route is complete. Its worst setup path is in the SoC, outside the datapath: 13 levels on the 10 ns clock. In the
post-place hierarchy against the record's own route (LUT / FF), `milan_datapath` moves by +516 / +379. The media
servo's phase loop accounts for +380 / +200 and the CRF row's Equation (14) rounder for +130 / +159. The presentation
stage nets -36 / +33 against the setpoint stage it retires, and `crf_tx` -59 / -141. Blocks this PR leaves unchanged
move by up to about 100.
Round 6's +72 slices compared with #708's record, which was not dev's own route at this lane's base. Against dev's own
route the share is about 500 LUTs larger.

**Found in the merge, fixed.** The design page's switch-row control said the meter's raw lock-fall edge is wired "as the
CRF term is"; since #761 the CRF term takes both raw lock edges, and the row says so.

#### Round 7b

The [A10] round 7b assignment (issuecomment-6357449062) carries the owner's decision on the round 7 STOP: this PR's
route growth is accepted beyond the +80 slice tolerance, extending the block-RAM exception (#632
issuecomment-6309313685) to the measured +500 LUT, +376 FF, +107 slices and +2 RAMB18, with Mark II (#640) to recover
the area. It leaves 15 of 15,850 slices on the shipping image, so the next growth there needs its own owner decision.

**The re-record.** The three endpoints were measured again at `5282b8b6` with the recipe unchanged, one Vivado run at
a time. Each printed record equals round 7's at the merge `dc9cda7d` in every field: figures, input digest, identity
and every sub-block scope. So the route-difference STOP does not apply. Each endpoint was written with
`pp_resource_gate.py record --write`, its note citing both decisions (`17280d2d`). `check` then exits 0 at all three
against the new record, and `check-baseline` passes. `d835ba12` documents the eleventh record, following #771's
pattern: the area budget's headroom table and history, the Mark II plan's anchor, and a new section on the #234
findings page.

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | WNS / WHS ns | Against #771's record |
|---|---:|---:|---:|---:|---:|---:|---|
| route-1x1 | 51,259 | 53,208 | 15,835 (15 free) | 74 / 27 | 13 | +0.236 / +0.028 | +500, +376, **+107**, 0 / **+2**, -1, -0.055 / -0.008 |
| ooc-1x1 | 23,828 | 20,000 | - | 16 / 3 | 8 | +3.337 / +0.159 | every figure equal |
| ooc-8x8 | 32,467 | 28,220 | - | 21 / 5 | 8 | +1.139 / +0.159 | every figure equal |

The two RAMB18 are the render queue's. The DSP fall is `crf_tx`'s retired free-running divider. Both standalone
digests move because their scripts read the shipping export's whole source list; the wrapper's own sources are
unchanged. Correction to round 7's wording: dev `e5b480a3` differs from the record's measured commit in comment lines
of three files (the AS_PATH count notes), not one block of one file. The record still measures dev's own design.

**The STOP.** `gmstep-mutants` (`--all`) exits 2 at `d835ba12`: 22 checks, 21 PASS, 1 FAIL. The control "the
grandmaster change stops the talker for good" (dev's, `gmstep_mutants.py:195-203`) latches a stop on the datapath's
GM-change detector `gm_recentre_p_r` and names "licence: the talker never pauses beyond four of its intervals". It
fails the leg, but not that check:

- Planted alone, the driver's own way, it fails 14 checks, among them "baseline: the talker streams". The talker never
  sends, so the pause check has nothing to measure.
- Dev `e5b480a3`'s own tree fails it identically (the same 14 checks), so the failure predates this PR. Round 6, on the
  old gPTP pin `e4869fd0`, caught it 22 of 22.
- A display on the detector's input on the clean leg shows the published grandmaster going 0 -> this station's own
  identity (FPGA-gPTP #82's boot grandmaster, adopted by #771) -> GM A at acquisition. The detector exempts only
  0 -> id, so it pulses at acquisition, before the baseline.

So the control's named check no longer fits the pin. This PR leaves the control alone (a test is not weakened to
pass). The options for the decision are in the STOP comment: a test-only fix here that keeps the stop at the leg's
grandmaster event; the same fix on dev first, then a merge; or a ruling on whether the detector should pulse on the
boot change. In this PR the detector's only reader is `KL_i2s_playback`'s re-centre; on dev it also drives the #387
render re-base.

#### Round 7c

The [A10] ruling issuecomment-6360257772 answers the round 7b STOP.

- **(c) The detector is right, and the RTL is unchanged.** Since the adopted gPTP pin the station is grandmaster-capable
  and is its own grandmaster at boot, so it publishes its own identity. IEEE 802.1AS-2011 9.6.2.1 makes gmIdentity the
  current grandmaster's ClockIdentity whenever gmPresent (10.2.3.13) is TRUE, so the step from that identity to GM A is a
  grandmaster change, and a media re-centre there is correct and harmless before the talker streams. Only 0 -> id is
  acquisition.
- **(a) The fix is test-only and in this PR.** Dev's own `gmstep-mutants` fails the same way at `e5b480a3`, so this PR
  repairs dev's campaign when it merges.

`c2c996fa` (`git diff --stat d835ba12 c2c996fa -- hdl syn configs` is empty):

| Change | File |
|---|---|
| The control "the grandmaster change stops the talker for good" latches its stop on `gm_recentre_p_r && (\|aaf_stream_en_raw_w)`: the first detector pulse while the talker's gate is open. The leg opens the gate after acquisition, so the boot pulse cannot latch it and the GM A -> GM B pulse does. It counts no pulses, so a boot sequence with more or fewer of them before the talker opens leaves it on the same event. Its meaning and its named check are unchanged | `tb/verilator/milan_dp_gm_steps/gmstep_mutants.py` |
| The driver prints the failed checks of every control and of a failing clean leg, not only of a catch | same |
| The clean leg records the adopted behaviour: "boot grandmaster: the detector pulsed once, at this station's own identity -> GM A, and the baseline talker streams after it". The harness logs every detector pulse with the identity it left and the one it names | `tb/verilator/milan_dp/sim_gmstep.cpp` |
| The detector's pulse and register are opened to the harness, read only, through a probe file on the leg's recipe | `tb/verilator/milan_dp/gmstep_probes.vlt`, `tb/verilator/milan_dp/Makefile` |
| A new `--all` control, "the detector exempts this station's own boot identity" (the behaviour the ruling rejects), must fail that check and leave "baseline: the talker streams" passing | `gmstep_mutants.py` |
| The control inventory and the leg's phases | `tb/verilator/milan_dp/README.md`, `docs/testing/TESTING.md`, `docs/design/GM_LOSS_RECOVERY.md`, `CHANGELOG.md` |

**The proof, planted alone** (the driver's own plant, build and run, on the whole leg), at the head's test files and on a
clean clone of dev `e5b480a3` with only the test fix applied:

| Control | Head | Dev `e5b480a3` + the test fix |
|---|---|---|
| the grandmaster change stops the talker for good | caught: "baseline: the talker streams" passes, the boot record passes, 12 checks fail, "licence: the talker never pauses beyond four of its intervals" among them (0 talker PDUs over the 825,871-cycle window) | the same 12 checks |
| the detector exempts this station's own boot identity | caught: exactly one check fails, the boot record; the baseline streams | the same |

The clean leg passes with 196 checks (195 before, plus the boot record) and logs one detector pulse before GM B, at
`02a1b2fffec3d4e5 -> 00aaccfffe010203`.

## Authoritative references

- Milan v1.2 7.6.1 (media clock: frequency and phase), 7.3.2 (CRF timestamp interval), 4.4.2.1 (the presentation
  time offset the listener must hold).
- IEEE 1722-2016 4.4.4.5 (`tv`), 4.4.4.9 (`avtp_timestamp`, the presentation time), 7.5 (AAF events in a PDU).
- IEEE 1722.1-2021 Table 7-157 (STREAM_INPUT counters, unchanged).
- IEEE 1722-2016 10.6 to 10.8 (Equations (14), (15), (16)), 4.3.5 (streams of one media clock on whole periods).
- Milan v1.2 5.4.2.9 (SET_STREAM_INFO sets the offset to the commanded value), 5.4.2.10.2 (GET_STREAM_INFO reads the
  offset in use), 5.3.7.6 (the 2 ms default); IEEE 1722.1-2021 7.4.77.1 (Max Transit Time and the listener's
  buffering).
- [docs/design/MEDIA_CLOCK_FOLLOWING.md, Phase alignment](docs/design/MEDIA_CLOCK_FOLLOWING.md#phase-alignment): the
  domain event, the per-source contract, the detector and loop, the offsets, the per-interface constants, the
  listener's presentation at the timestamp (round 4), the -0.46 Ps accounting and the proof table.
- [docs/design/TIME_SYNC.md](docs/design/TIME_SYNC.md): the domain event, the servo phase term, the stream offsets,
  the talker capture hand-off and the listener render latency.
- [docs/reference/REGISTER_MAP.md](docs/reference/REGISTER_MAP.md) `0x8DC` `RENDER_STAT`, re-defined.
- The assignment and its two addenda on #632; #764's investigation report; the R678-1 and R677-1 reviews and the
  round 2 rulings on this PR; the round 5 ruling (issuecomment-6320617745) and owner decision
  (issuecomment-6320453361); the round 6 assignment (issuecomment-6341411985) and the R677-3 and R678-3 reviews;
  the round 7 assignment (issuecomment-6351804497) and the owner's block-RAM decision on #632 (issuecomment-6309313685);
  the round 7b assignment with the owner's area decision (issuecomment-6357449062).
- [docs/design/AREA_BUDGET.md](docs/design/AREA_BUDGET.md) and the [#234 findings page](docs/findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-23-issues-632-and-764): the eleventh resource record.

## How to get into the same state

```sh
git clone https://github.com/kebag-logic/milan-fpga.git
cd milan-fpga
git switch 632-764-media-phase
git submodule update --init --recursive
```

Verilator 5.050, as pinned by the workflows.

## How to validate

```sh
make -C tb/verilator/media_phase
make -C tb/verilator/media_phase mutants MUTANT_JOBS=2
make -C tb/verilator/render_queue
make -C tb/verilator/crf_tx
make -C tb/verilator/capture_coherence
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp gsi-mutants
make -C tb/verilator/milan_dp render-csr-controls
make -C tb/verilator/milan_dp_render tdm8render
make -C tb/verilator/milan_dp_render tdm8render-mutants
make -C tb/verilator/milan_dp_render tdm8render-pullin PULLIN_JOBS=4
make -C tb/verilator/milan_dp_gm_steps
make -C tb/verilator/milan_dp_gm_steps gmstep-mutants
make -C tb/verilator/follow_ring
make -C tb/verilator/follow_ring mutants
make -C tb/verilator/milan_dp_mclk
python3 scripts/lint_rtl.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
syn/yosys/run.sh
bash scripts/run_all_suites.sh sweep-out
```

Expected result / pass criteria:

- `media_phase`: the pins (three synthetic interfaces), the blend (the in-tree I2S + TDM8 shape, six reset phases),
  the offsets (four AAF outputs and the CRF output, eleven cases over the ruled offsets, every AAF stamp exact, the
  CRF row at the 2^32 boundary in reset and at run time), the render case (two interfaces a frame apart at their
  pins), the eleven detector cases and the thirteen loop cases each end `failures: 0`.
- `media_phase mutants`: the clean cases pass, then all forty planted defects fail their named checks.
- `render_queue`: both shapes end `failures: 0`, `[behind]` among their phases; its campaign catches all twenty-six
  planted defects.
- `milan_dp_render`: both legs pass; `tdm8render-mutants` exits 0 with every mutation caught by its named check and
  every clean control passing (31 checks); `tdm8render-pullin` passes every one of its 19 legs.
- `milan_dp_gm_steps`: the leg passes, its baseline recording one GM-change detector pulse at this station's own
  identity -> GM A; `gmstep-mutants` exits 0 with 23 checks: both clean legs and all 21 controls caught by their named
  checks on the whole leg.
- `follow_ring`, `milan_dp_mclk`: every leg passes; `follow_ring mutants` catches all sixteen.
- `milan_dp`: every leg passes, the timed notify leg's `[NOTIFY]` SET_STREAM_INFO case among them (461 checks, 0
  failures, at processor `93fb0b2d`); `gsi-mutants` catches all eleven. `render_mutants.py` catches its four controls
  and `render-csr-controls` its two.
- `aaf`: the golden byte-compare holds with both I2S front ends aligned.
- `capture_coherence`: the `[PIN]` leg and its campaign, every mutant caught.
- The lint gate stays at its ratchet; the full sweep passes every suite.

Measured in round 7c at the head `c2c996fa`, a test-only commit on `d835ba12` (no file under `hdl`, `syn` or
`configs` changes, so the Vivado bank, Yosys and the tdm8 campaigns below stand):

| Gate | Result |
|---|---|
| `gmstep-mutants` | exit 0: 23 checks, 23 PASS. The clean gmstep leg (196 checks) and the option-off leg pass; all 21 controls are caught by their named checks; "the grandmaster change stops the talker for good" breaks 12 checks, the new control 1 |
| the campaign audit (the R678-3 script) | `gmstep_mutants.py`: 21 of 21 recorded |
| the firmware boundary gate (`ctrl_boundary.py --require-rv32 --selftest`, the LiteX interpreter) | exit 0, "ctrl_boundary: PASS" |
| the docs workflow's gate steps, as in round 7b | 42 of 44 run and pass, 2 skipped by rule; builder leg 1 with LiteX all but gate 11; the five markdown gates on 3.12.3 and the no-git pair pass |
| `python3 scripts/lint_rtl.py --check` | PASS, 89 <= ratchet 89 |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | "baseline PASS: 3 endpoints" |
| full sweep, `scripts/run_all_suites.sh`, four shards in sequence | 63 of 64 suites pass, 2,190,061 checks, 0 in-suite failures: shard 0 15/15 (54,917 checks; `milan_dp` whole, the notify leg among it), shard 1 16/16 (331,530), shard 2 16 of 17 (262,031; `capture_coherence` stopped by the runner's 2,400 s wall clock, result unknown, not a failure), shard 3 16/16 (1,541,583). `capture_coherence` was then run again alone, the suite's own target as the runner invokes it on the same two CPUs: exit 0 in 2,402 s, 20,832 and 447 checks, 0 failures, its campaign 35 of 35, the runner's tally verdict clean. 11:40 to 17:19 CEST |

Measured in round 7b at the head `d835ba12`, which adds the record and its documentation to `5282b8b6`, or at
`5282b8b6` for the Vivado bank, whose synthesis inputs the two later commits do not touch; the notify leg and
`gsi_mutants.py` at the merge `dc9cda7d` (round 7), whose RTL, processor and tests the later commits leave unchanged:

| Gate | Result |
|---|---|
| route-1x1, ooc-1x1, ooc-8x8 (recipe, one Vivado run at a time), at `5282b8b6` | rc 0 x4 (41.9, 12.6, 1.2, 24.7 min; route peak 8,406 MB). Against #771's record route-1x1 exits 1 (SLICE +107, RAMB18 +2) and both ooc exit 0, every printed record equal to round 7's in every field. Re-recorded under the two exceptions; `check` exits 0 at all three against the new record, and `check-baseline` and `--selftest` pass |
| `python3 scripts/lint_rtl.py --check` | PASS, 89 <= ratchet 89 |
| `syn/yosys/run.sh` | exit 0 in 21.4 min: 60 of 60 tops (`milan_datapath` 1,778,837 cells, `KL_render_queue` 655,590), tied-input and tap-purity pass |
| the docs workflow's gate steps, their `run:` bodies under GNU Make 4.3 and CPython 3.12.3 | 42 of 44 run and pass, both builder legs among them (leg 1 with the LiteX interpreter: every gate but gate 11, not run). Two are skipped by rule: gate 42 runs the candidate's act runner on the host, and the no-git step deletes `.git`, so its two gates ran on an archive export and pass. The five markdown gates also pass on 3.12.3 |
| the builder bank (`sw/builder/test_builder.py --require-elaboration --require-rv32`) | exit 0: every gate passes but gate 11, not run (the Arty calibration build tree is not on this host) |
| the firmware gate set (`CI_WORKFLOWS.md`'s firmware block, `--jobs 4`), but its boundary gate | all exit 0: `fw_rv32_selftest`, `tally_selftest.py --mutants`, `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp` PASS, the shard check, `test_ctrl_nvm.py --require-rv32 --self-test`, `fw_coverage.py --selftest` (29 of 29) and `--check` |
| `tdm8render-mutants` | exit 0; 31 checks, 31 PASS |
| `tdm8render-pullin` (the Makefile recipe on the campaign's clean binary, `PULLIN_JOBS=4`) | 19 legs, each exit 0 (18 phases at 28 checks, the history leg 272), 0 failures |
| `gmstep-mutants` | **exit 2: 22 checks, 21 PASS, 1 FAIL** ("the grandmaster change stops the talker for good" fails 14 checks, not its named one; dev `e5b480a3` the same) |
| the campaign audit (the R678-3 script) | `tdm8_render_mutants.py`: 20 of 20, 3 of 3, 3 of 3 recorded; `gmstep_mutants.py`: 19 of 20 (the failing control); 19 pull-in logs PASS |
| the notify leg (`make build-notify exec-notify`), at `dc9cda7d` | 461 checks, 0 failures, exit 0; all eight SET_STREAM_INFO steps pass |
| `gsi_mutants.py`, every control, at `dc9cda7d` | exit 0; the clean leg passes, then 11 of 11 caught (the three #632 controls 3 failures of 461 each) |
| the firmware boundary gate (`ctrl_boundary.py --require-rv32 --selftest`), the full sweep | not run: the round 7b STOP comes first |

Measured in round 6 at `d40e2ee8`, before the merge, or at the ancestor named where the later commits leave that
gate's inputs untouched (`f98d00dd` is the last RTL change, `0ffcd7f0` carries it; `2700584e` is the last test
change; `d40e2ee8` changes one design-page paragraph); the processor was then at `2cbed0a9`:

| Gate | Result |
|---|---|
| full sweep, `scripts/run_all_suites.sh`, four shards in sequence, at `d40e2ee8` | Shard 0: 14 of 15, 47,447 checks, `milan_dp` failing only the notify leg's CRF-output steps 3 and 4 at processor `2cbed0a9` (three checks; its pool ran base, notify, crflic, dynmap, nxn and nxndv, all others 0 failures, then started no later leg, so every leg is also run on its own, below). Shard 1: 16/16, 331,526 checks (`render_queue` 39/0, 38/0, 28 of 28; `media_phase`, `follow_ring`, `milan_dp_mclk`). Shard 2: 16 of 17 passed, 262,027 checks, 0 in-suite failures; `capture_coherence` was stopped by the runner's 2,400 s wall clock mid-campaign (exit 92, result unknown: the host was loaded by other work), so it was run again uncontended, the suite's own target as the runner invokes it on the same two CPUs: exit 0 in 2,312 s, 20,832 and 447 checks, 0 failures, its campaign 35 of 35, the runner's tally verdict clean. Shard 3: 16/16, 1,540,273 checks (`milan_dp_render`: ship 263, multi 79, leg defects 5 of 5). 18:26 to 22:52 CEST |
| `tdm8render-mutants`, at `2700584e` | exit 0; 31 checks, 31 PASS (above) |
| `tdm8render-pullin`, at `2700584e` | 19 legs, each exit 0 (18 phases at 28 checks, the history leg 272), 0 failures |
| `gmstep-mutants`, at `2700584e` | exit 0; 22 checks, 22 PASS; the clean leg 195 checks with the #621 phase |
| `follow_ring mutants`, at `d40e2ee8` | exit 0; 16 of 16 caught |
| `make -C tb/verilator/render_queue` (run, odd, mutants), at `0ffcd7f0` (the suite as at the head) | 39 and 38 checks, 0 failures; 28 of 28 (two clean shapes, 26 defects caught) |
| the reviewer's partial-late probe | its patch on `ee5ece60`: 32 and 20 mismatched beats; the same PDUs on `0ffcd7f0`: 0 and 0, 41 and 40 checks pass |
| `make -C tb/verilator/media_phase render` and its five controls, at `2700584e` | 13 checks, 0 failures; 5 of 5 caught |
| `milan_dp`, every leg, at `d40e2ee8` | built and run one by one: base 236, crflic 416, dynmap 162, nxn 2,009, nxndv 2,011, nxn8 3,817, nxn4c 2,009, nolpf 236, prune 33, ax1x1 233, aclk 182 checks, 0 failures; `render_mutants.py` 6 of 6; `render-csr-controls` exit 0 |
| the notify leg at processor `2cbed0a9`, at `d40e2ee8` | 459 checks, 3 failures: CRF-output steps 3 and 4, as ruled for that pin |
| route-1x1 and `pp_resource_gate.py check`, at `0ffcd7f0` | LUT 49,587 (-26), FF 52,742 (+389), slices 15,797 (+72), RAMB36 74, RAMB18 27 (+2, budgeted; exit 1 on it alone), DSP 13, WNS +0.163 ns, WHS +0.017 ns, route complete |
| Vivado out of context, the stage | at `2700584e`: 1x1 2 RAMB18, 531 LUTs, 236 FFs; 8x8 6 RAMB36, 883, 402; no LUTRAM. With a 20 ns clock, `ee5ece60` against `2700584e`: 538/228 and 527/236 |
| `syn/yosys/run.sh`, the changed tops, at `2700584e` | `KL_render_queue` (655,590 cells), `KL_aaf_rx_depacketizer` (60,880), `milan_datapath` (1,770,851) pass; tied-input and tap-purity pass |
| `python3 scripts/lint_rtl.py --check`, at `d40e2ee8` | PASS, 89 <= ratchet 89 |
| the docs workflow's 49 gates, at `d40e2ee8` | all pass |
| the builder bank (`sw/builder/test_builder.py --require-elaboration --require-rv32`), at `d40e2ee8` | exit 0: every gate passes but gate 11, not run (the Arty calibration build tree is not on this host), as in round 4 |

Not re-run this round, their inputs unchanged since: the notify leg and `gsi_mutants.py` with the processor's gate
spliced (round 5, `d5b516f6`: 459 checks, 0 failures; 11 of 11), and the full `media_phase` campaign (round 5,
`ee5ece60`: 40 of 40; this round re-ran the render case and its five controls, the only ones the queue reaches).

## Known limitations / out of scope

- **The listener's supported range.** The queue is sized for the 2 ms default offset (Milan v1.2 5.3.7.6), with no
  deeper option: a sample is written for every interface from 31,119 ns to 2,656,119 ns ahead of its presentation
  time at arrival on the 1x1 shape, 25,942 ns to 2,650,942 ns on the 8x8 (the depth holds Milan v1.2 4.4.2.1's 2.126
  ms plus the event latency); outside it the PDU is refused, late or too early, and counted. Nothing re-centres. A
  talker offset is presented whole when the offset less the PDU's transit lies in that range. The builder accepts a
  `buffer_length_ns` above 2,126,000 ns, which no shipped shape declares; the queue's depth does not grow with it.
- **The late reach.** Each event of a PDU is judged on its own frame; the divider takes the timestamp difference from
  504 frames (10.5 ms at 48 kHz) behind the latest domain event. A PDU stamped further behind is refused whole, which
  is the per-event result for every PDU the depacketizer passes (at most 504 one-channel events, its 2048-byte frame
  FIFO): its last event is already presented. A deeper FIFO would need a longer reach (`MAX_EV_P`, derived in the
  datapath from the FIFO depth). The 32-bit timestamp difference is read from 2^31 ns plus the reach behind to 2^31 ns
  less the reach ahead: a timestamp 2.137 to 2.147 s ahead counts as late, not too early (refused either way).
- **AAF offsets that are not whole periods.** Applied as set (the round 5 ruling): such a stream's timestamps sit the
  offset's fraction of a period off the CRF timing points, so IEEE 1722-2016 4.3.5's whole periods and 10.8 Equation
  (15)'s +/-5 % hold for AAF offsets of whole periods only. A listener presenting each sample at its timestamp absorbs
  it.
- **A listener grid off the talker's rate.** At INTERNAL, or through a media-clock hold, the listener's frame grid
  does not run at the talker's media rate: the timestamps cross the frame instants and the stage counts one slip (a
  gap or an overlap) at each crossing, graded in `milan_dp_render` `[LAW]` and `[PULLIN]` and in `follow_ring`.
- **A step of this listener's PHC alone.** When the listener's gPTP time steps and its talker's does not follow, later
  PDUs land on frames off by the step (a counted overlap or gap) or are refused when it reaches past the queue. That
  follows from the law and is not graded by its own case; the graded steps move the talker's time with the
  listener's (`milan_dp` aclk) or straddle a grandmaster change (`milan_dp_gm_steps`).
- **`KL_i2s_playback`** (the Arty I2S DAC path) keeps its own fill law and elastic FIFO, unchanged by the owner's
  decision.
- **The shipping image's slice room.** This PR's route growth against #771's record (+500 LUT, +376 FF, +107 slices,
  +2 RAMB18) is recorded under the owner's block-RAM exception (#632 issuecomment-6309313685) and its extension to the
  LUT, FF and slice growth (PR #770 issuecomment-6357449062). 15 of 15,850 slices remain, so the next growth on the
  shipping image needs its own owner decision; Mark II (#640) recovers the area.
- **Bench proof.** The #764 method on the bench, after merge; this lane had no bench access.
- **AAF following** keeps the rate loop alone (`ph_en_i` low under an AAF source).
- **The CRF output's offset is not idempotent in whole ns.** Equation (14) rounds up to whole periods; a period
  count that is no multiple of three has a ceiling above it in whole ns, so a controller writing back what
  GET_STREAM_INFO read for the CRF output sets a different value, which applies one period more. SET_STREAM_INFO's
  response echoes the value set (Milan v1.2 5.4.2.9) and GET_STREAM_INFO reads the value applied (5.4.2.10.2). The
  values a controller ordinarily sets, multiples of 62,500 ns, are exact. An AAF output reads back what was set.
- **Past 2^32 ns.** A CRF offset above 4,294,958,333 ns rounds past 2^32 (0xFFFFFFFF applies as 4,294,979,167 ns); the
  CRF output adds the carry into its 64-bit timestamp, and GET_STREAM_INFO reads it as 0xFFFFFFFF. An AAF offset is
  never rounded and stays 32 bits. Only a factory row reaches 2^31 or more: a controller's SET is bounded at
  0x7FFFFFFF (5.4.2.9).
- **An applied offset that changes without a SET** (a media clock rate change under the same row) changes what
  GET_STREAM_INFO reads with no notification behind it (IEEE 1722.1-2021 7.5.2's normal-operation case). Recorded as
  a follow-up, out of this PR's scope by ruling.
- **Processor PR #199's own harness** models the integrator rounding every Stream Output's GET_STREAM_INFO offset;
  after round 5 only the CRF output's is rounded, which leaves its gate test valid (it needs one row whose readback
  differs from the stored value).
- **The gate's factory-offset residue.** Before the CRF output's first SET the processor compares with
  GET_STREAM_INFO's word, the offset as applied, so a factory CRF offset that is not whole periods would push for a
  SET of exactly that value. Every factory offset this repository ships is 2 ms, whole periods. Recorded by the
  ruling.
- **The blend's two interfaces** start one audio clock cycle (40.7 ns) apart, which the grade measures inside the
  band; it is a property of the two front ends' dividers, not a derived constant.
- **The Arty shapes are retired**; the blend and the I2S capture fix are graded in simulation only.
- **Composition with dev** `e5b480a3` is merged (round 7); a candidate merge with any later dev belongs to the merge turn.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (talker, media clock and the listener at the pin in simulation;
  the processor gate is in the pinned processor `93fb0b2d`; bench after merge)
- [x] New or changed behavior has self-checking tests
- x Required local verification bar passes (round 7c at `c2c996fa`: `gmstep-mutants` 23 of 23 after the test-only repair, the boundary gate, the docs gates, lint, the full sweep (the sweep's 64th suite, `capture_coherence`, passing when run alone after the runner's wall clock stopped it))
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
