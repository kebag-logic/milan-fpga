[A659]

## Contents

- **[Status](#status)** — Gate tally, the processor prerequisite (the SET_STREAM_INFO gate, ruled), and `632-764-media-phase` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why, rounds 1 to 3b.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Ready for review at `3fdaea3d`. The processor's SET_STREAM_INFO change gate (R677-2-F1) is ruled: option (b)
(issuecomment-6312625146), the stored row once a controller set it and GET_STREAM_INFO's word, the factory offset in
force, before. It is committed in the processor on `632-sinfo-notify-stored` (head `51f88c7e`, on processor main
`08023123`), with its own test and planted defects. That processor PR is a prerequisite: milan-fpga's fourth
processor pin adoption consumes it, and this PR merges after that pin. At the current pin the `[NOTIFY]`
SET_STREAM_INFO case fails its steps 3 and 4 by design; with the processor head's gate applied to the submodule it
passes, and its planted control is caught (Round 3b below). R678-1-F1 (the listener at the pin) is out of this PR by
the [A10] ruling (issuecomment-6306187740) and stays open under #632; the listener keeps the #386 law at the
crossbar grid, its post-grid delays the documented constants of TIME_SYNC.md. `632-764-media-phase` -> `dev`. The
bench proof follows after merge.

## Linked Issue / roles

Relates to #632
Relates to #764

#632's simulation acceptance item is met for the talker and the media clock. R678-1-F1 (the listener at the pin) is
out of this PR by the [A10] ruling (issuecomment-6306187740) and stays open under #632; the listener keeps the #386
law at the crossbar grid, its post-grid delays the documented constants of TIME_SYNC.md. #632's bench item, and
#764's bench proof, follow after merge with the #764 method, so neither Issue is closed by this PR.

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
| R678-1-F2 | Every stream output's presentation offset is applied rounded up to whole media clock periods by `KL_crf_tx`'s own Equation (14) rule (`KL_mtt_round`, new, one round-robin divider), and GET_STREAM_INFO reads back the applied value: 2,010,000 ns applies as 97 periods, 2,020,834 ns, where the raw value sat 0.48 Ps off the CRF timing points. The CRF output stamps the rounder's row too (`KL_crf_tx` `ROUND_MTT_P = 0`, its own converter not elaborated), so one rounding serves every output | 10.7 Eq. (14), 4.3.5, 10.8 |
| R677-1-F1 | The I2S blend now closes each frame on its I2S pair, the last of the frame to reach the crossbar, back-dated by the I2S front end's latency (`close_slot()`, `close_is_i2s()`, `KL_chan_map_capture.TDM_CLOSE_SLOT_P`). Grading it with sample values at both interfaces' pins found a second defect: `KL_aaf_capture_i2s`, and the flat `aaf_talker_i2s` it was split from, copied the crossing FIFO's registered read on the pop edge, so every strobe carried the pair before it. Both now alias that read as the TDM front ends do | 4.3.5, 10.8 |
| R677-1-F2, F3 | Cases and planted defects for the local PHC step hold, the settled flag's timing and its mirror, and the fold-range guard | 10.8 |
| R677-1-F4 | `media_phase`'s budget basis re-measured: the whole default target in 578 s at three case jobs | -- |
| R677-1-F5, R678-1-R1 | The three stale CRF-divider texts corrected as written; the reviewer lines above | -- |

No top-level port and no register-map layout change: `MCSRV_STAT[9]`'s read-only meaning is tightened. Module
changes: `KL_mtt_round` is new; `KL_chan_map_capture` gains `TDM_CLOSE_SLOT_P`, defaulted to its old behaviour;
`close_pair()` loses its blend argument.

**Resources.** route-1x1 under the recipe, checked by `pp_resource_gate.py` against the recorded baseline:

| Figure | Record | Round 1 (`a6ae20f9`) | Round 2 (`f1643214`) | Round 3 (`62ee1a8c`) | Delta to record | Tolerance / floor |
|---|---:|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | 49,709 | 49,733 | +120 | +500 |
| FF | 52,353 | 52,641 | 52,760 | 52,765 | +412 | +600 |
| Slice | 15,725 | 15,785 | 15,797 | 15,804 | +79 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 14 | 13 | 13 | -1 | +0 |
| WNS | +0.215 ns | +0.276 ns | +0.305 ns | +0.282 ns | +0.067 | at least +0.030, fall at most 0.25 |
| WHS | +0.036 ns | +0.032 ns | +0.036 ns | +0.016 ns | -0.020 | at least 0, fall at most 0.25 |

Route complete, no unrouted net; gate exit 0, with "re-baseline recommended" for the DSP the image no longer
uses. **One slice of headroom is left.** The round 3 carry costs about 10 LUTs in its own blocks against the round 2
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
| the current pin (gate reads GET_STREAM_INFO's word) | 0 | 1 | **1** | **0** | 1 | 3 failures |
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

### R678-1-F1: out of this PR (background for the owner's decision)

Taken out of this PR by the [A10] ruling (issuecomment-6306187740) and open under #632. The measured costs, as the
background for the owner's area or RAMB decision:

Presenting each sample at the pin at its presentation time holds it for the presentation offset less its arrival
lead, about 1.9 ms at the 2 ms default, about 96 events: 128 event rows per 8-channel stream where the render stage
keeps 32. Measured by out-of-context synthesis at the AX7101 1x1 parameters: the queue alone grows from 456 to 1,006 LUTs
(LUTRAM 128 to 512), against 404 LUTs and 8 slices of route-1x1 headroom (at `f1643214`); in block RAM it adds two or three RAMB18
(the parity-split rows need a write port each) against a RAMB tolerance of zero. The depacketizer's frame FIFO is
2,048 bytes, about eight shipping PDUs, under the fourteen a 2 ms hold needs. Any form also replaces the #386 render
law (fill 8 events after accept, its rails and the #387 and #645 recentres) that `render_setpoint`, `milan_dp`,
`follow_ring`, `milan_dp_gm_steps` and `milan_dp_render` grade. One pop per stream cannot land two interfaces whose
post-grid delays differ by a frame on one presentation time without a per-interface frame delay, and the Arty DAC
path keeps its own fill law and elastic FIFO. The options:

- (a) a timestamp-snapped render queue, in LUTRAM (about 550 LUTs of storage plus its logic) or in block RAM (two
  or three RAMB18);
- (b) a presentation gate at a deepened depacketizer FIFO (one RAMB36), which also delays the loopback ring and the
  DAC tap by the hold.

Either needs the route-1x1 record re-written by an accepted growth decision, and a ruling on the supported offset
range (the queue depth), on late and too-early PDUs, and on whether the Arty DAC path is in scope.

## Authoritative references

- Milan v1.2 7.6.1 (media clock: frequency and phase), 7.3.2 (CRF timestamp interval).
- IEEE 1722-2016 10.6 to 10.8 (Equations (14), (15), (16)), 4.3.5 (streams of one media clock on whole periods).
- [docs/design/MEDIA_CLOCK_FOLLOWING.md, Phase alignment](docs/design/MEDIA_CLOCK_FOLLOWING.md#phase-alignment): the
  domain event, the per-source contract, the detector and loop, the offsets, the per-interface constants, the
  listener decision, the -0.46 Ps accounting and the proof table.
- [docs/design/TIME_SYNC.md](docs/design/TIME_SYNC.md): the domain event, the servo phase term, the stream offsets
  and the talker capture hand-off.
- The assignment and its two addenda on #632; #764's investigation report; the R678-1 and R677-1 reviews and the
  round 2 rulings on this PR.

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
make -C tb/verilator/crf_tx
make -C tb/verilator/capture_coherence
make -C tb/verilator/milan_dp run ORDINARY_CASES="base crflic dynmap nxn nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"
make -C tb/verilator/milan_dp run-notify
python3 scripts/lint_rtl.py --check
bash scripts/run_all_suites.sh sweep-out
```

Once the processor pin carries the gate fix (the processor PR on `632-sinfo-notify-stored`), `make -C
tb/verilator/milan_dp` and its `gsi-mutants` campaign run whole again.

Expected result / pass criteria:

- `media_phase`: the pins (three synthetic interfaces), the blend (the in-tree I2S + TDM8 shape, six reset phases),
  the offsets (four AAF outputs and the CRF output, six runs, at the 2^32 boundary in reset and at run time), the
  eleven detector cases and the thirteen loop cases each end `failures: 0`.
- `media_phase mutants`: the clean cases pass, then all thirty-three planted defects fail their named checks.
- `milan_dp`: every leg passes except the timed notify leg's `[NOTIFY]` SET_STREAM_INFO steps 3 and 4 (three checks),
  which fail at the current processor pin until it carries the gate fix; `sim_pool.py` then starts no later leg, so
  at this pin each leg is run on its own (`make -C tb/verilator/milan_dp run ORDINARY_CASES="base crflic dynmap nxn
  nxndv nxn8 nxn4c nolpf prune ax1x1 aclk"`, then `make -C tb/verilator/milan_dp run-notify`).
- `aaf`: the golden byte-compare holds with both I2S front ends aligned.
- `capture_coherence`: the `[PIN]` leg and its campaign, every mutant caught.
- The lint gate stays at its ratchet; the full sweep exits 0.

Measured locally at the head `3fdaea3d`, or at the ancestor named where the later commits leave that gate's inputs
untouched (`3fdaea3d` changes one design document only):

| Gate | Result |
|---|---|
| full sweep, `scripts/run_all_suites.sh`, four shards in sequence, at `62ee1a8c` | shard 0: 14 of 15, `milan_dp` failing (the pin case below, and a premise of mine in the N=4 leg fixed in `28510858`; its pool then started no later leg); shard 1 16/16, 331,638 checks (media_phase included); shard 2 17/17, 262,057 (`capture_coherence` run 20,832, dp 447, campaign 35 of 35); shard 3 16/16, 1,540,268. 0 failures outside `milan_dp`. Commits after `62ee1a8c` touch `milan_dp`'s harness and docs only |
| `milan_dp`, every leg, at `32fb8fc2` | all but the notify leg (`make run` with the notify leg out of the pool): 14 tallies, 11,629 checks, 0 failures, 2,415 s; the notify leg: 441 checks, 3 failures, the SET_STREAM_INFO steps 3 and 4 at the current pin. With the processor's gate fix applied uncommitted to the submodule (form (b)): 441 checks, 0 failures, and the planted control (`gsi_mutants.py 9`) caught at step 3 |
| `make -C tb/verilator/media_phase` | at `cf85a578`: 27 tallies, 326 checks, 0 failures, 553 s with five builds; `ofs` again at `62ee1a8c`: 46 checks, 0 failures; the whole suite in the sweep at `62ee1a8c` |
| `make -C tb/verilator/media_phase mutants` | at `cf85a578`, `MUTANT_JOBS=2`: 52 checks, 0 failures, 19 clean controls then 33 of 33 planted defects fail their named checks, 1,396 s; the six on `ofs` (the one harness `62ee1a8c` touches) killed again at `62ee1a8c` |
| route-1x1 and `pp_resource_gate.py check` | exit 0 at `62ee1a8c` (table above) |
| `syn/yosys/run.sh`, the four changed tops | at `32fb8fc2`: `KL_crf_tx`, `KL_mtt_round` (1,215 cells), `KL_aaf_capture_i2s`, `milan_datapath` pass; tied-input and tap-purity pass |
| `python3 scripts/lint_rtl.py --check` | PASS, 89 <= ratchet 89, at `32fb8fc2` |
| the docs workflow's 49 gates | all pass at `3fdaea3d` |
| the notify leg and its control with the processor PR's E_SINFO (`0b097464`, the same `hdl/` as its head `51f88c7e`) applied to the submodule | at `32fb8fc2`: 441 checks, 0 failures; `gsi_mutants.py 9` caught at step 3; the never-set probe pushes once for a SET of 0. Submodule restored to its pin afterwards |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | all gates pass except one not run for its recorded reason (it needs a separate Arty build tree on disk), at `32fb8fc2` |
| `make -C tb/verilator/crf_tx` | 129 checks, 0 failures (in the sweep at `62ee1a8c`) |

## Known limitations / out of scope

- **The listener is not compensated.** R678-1-F1 is out of this PR by the [A10] ruling (issuecomment-6306187740)
  and stays open under #632; the listener keeps the #386 law at the crossbar grid, its post-grid delays the
  documented constants of TIME_SYNC.md.
- **Bench proof.** The #764 method on the bench, after merge; this lane had no bench access.
- **AAF following** keeps the rate loop alone (`ph_en_i` low under an AAF source).
- **Offsets are not idempotent in whole ns.** Equation (14) rounds up to whole periods; a period count that is no
  multiple of three has a ceiling above it in whole ns, so a controller writing back what GET_STREAM_INFO read sets a
  different value, which applies one period more. SET_STREAM_INFO's response echoes the value set (Milan v1.2
  5.4.2.9) and GET_STREAM_INFO reads the value applied (5.4.2.10.2). The values a controller ordinarily sets,
  multiples of 62,500 ns, are exact.
- **Past 2^32 ns.** An offset above 4,294,958,333 ns rounds past 2^32 (0xFFFFFFFF applies as 4,294,979,167 ns). The
  AAF talkers stamp its low 32 bits, which is exact for a 32-bit AVTP timestamp; the CRF output adds the carry into
  its 64-bit timestamp; GET_STREAM_INFO reads it as 0xFFFFFFFF. Only a factory row reaches it: a controller's SET is
  bounded at 0x7FFFFFFF (5.4.2.9).
- **An applied offset that changes without a SET** (a media clock rate change under the same row) changes what
  GET_STREAM_INFO reads with no notification behind it (IEEE 1722.1-2021 7.5.2's normal-operation case). Recorded as
  a follow-up, out of this PR's scope by ruling.
- **The `[NOTIFY]` SET_STREAM_INFO case fails at the current processor pin** (steps 3 and 4) until the pin carries
  the gate fix, the processor PR on `632-sinfo-notify-stored`, which the fourth pin adoption consumes; this PR
  merges after that pin.
- **The gate's factory-offset residue.** Before an output's first SET the processor compares with GET_STREAM_INFO's
  word, the offset as applied, so a factory offset that is not whole periods would push for a SET of exactly that
  value. Every factory offset this repository ships is 2 ms, whole periods. Recorded by the ruling.
- **The blend's two interfaces** start one audio clock cycle (40.7 ns) apart, which the grade measures inside the
  band; it is a property of the two front ends' dividers, not a derived constant.
- **The Arty shapes are retired**; the blend and the I2S capture fix are graded in simulation only.
- **Composition with dev** `78ca9bdf` was not merged in; the candidate merge belongs to the merge turn.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (talker and media clock in simulation; the listener item is out
  of scope by ruling and open under #632; the processor gate is ruled and committed in the processor PR, which
  the pin adoption consumes; bench after merge)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
