[A659]

## Contents

- **[Status](#status)** — Gate tally, the one open decision, and `632-764-media-phase` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why, round 1 and round 2.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED on one decision: R678-1-F1, the listener presenting each sample at the pin at its presentation time, which
no form fits inside the route-1x1 gate the same ruling holds (Round 2 below). Every other Round 2 item is done at
`2ff30f0d`, where every local gate passes (table below), the full sweep included; route-1x1 stays within the resource gate with one DSP fewer. `632-764-media-phase` -> `dev`. The bench proof follows after merge.

## Linked Issue / roles

Relates to #632
Relates to #764

#632's simulation acceptance item is met for the talker and the media clock. The listener item ruled in by
R678-1-F1 waits on the decision below. #632's bench item, and #764's bench proof, follow after merge with the #764
method, so neither Issue is closed by this PR.

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
| R678-1-F2 | Every stream output's presentation offset is applied rounded up to whole media clock periods by `KL_crf_tx`'s own Equation (14) rule (`KL_mtt_round`, new, one round-robin divider), and GET_STREAM_INFO reads back the applied value: 2,010,000 ns applies as 97 periods, 2,020,834 ns, where the raw value sat 0.48 Ps off the CRF timing points. `KL_crf_tx` keeps its raw row and rounds it the same way, so the CRF row read back is the one it stamps | 10.7 Eq. (14), 4.3.5, 10.8 |
| R677-1-F1 | The I2S blend now closes each frame on its I2S pair, the last of the frame to reach the crossbar, back-dated by the I2S front end's latency (`close_slot()`, `close_is_i2s()`, `KL_chan_map_capture.TDM_CLOSE_SLOT_P`). Grading it with sample values at both interfaces' pins found a second defect: `KL_aaf_capture_i2s`, and the flat `aaf_talker_i2s` it was split from, copied the crossing FIFO's registered read on the pop edge, so every strobe carried the pair before it. Both now alias that read as the TDM front ends do | 4.3.5, 10.8 |
| R677-1-F2, F3 | Cases and planted defects for the local PHC step hold, the settled flag's timing and its mirror, and the fold-range guard | 10.8 |
| R677-1-F4 | `media_phase`'s budget basis re-measured: the whole default target in 578 s at three case jobs | -- |
| R677-1-F5, R678-1-R1 | The three stale CRF-divider texts corrected as written; the reviewer lines above | -- |

No top-level port and no register-map layout change: `MCSRV_STAT[9]`'s read-only meaning is tightened. Module
changes: `KL_mtt_round` is new; `KL_chan_map_capture` gains `TDM_CLOSE_SLOT_P`, defaulted to its old behaviour;
`close_pair()` loses its blend argument.

**Resources.** route-1x1 under the recipe, checked by `pp_resource_gate.py` against the recorded baseline, at the head:

| Figure | Record | Round 1 (`a6ae20f9`) | Round 2 (`f1643214`) | Delta to record | Tolerance / floor |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | 49,709 | +96 | +500 |
| FF | 52,353 | 52,641 | 52,760 | +407 | +600 |
| Slice | 15,725 | 15,785 | 15,797 | +72 | +80 |
| RAMB36 / RAMB18 | 74 / 25 | 74 / 25 | 74 / 25 | 0 | +0 |
| DSP | 14 | 14 | 13 | -1 | +0 |
| WNS | +0.215 ns | +0.276 ns | +0.305 ns | +0.090 | at least +0.030, fall at most 0.25 |
| WHS | +0.036 ns | +0.032 ns | +0.036 ns | 0 | at least 0, fall at most 0.25 |

Route complete, no unrouted net; gate exit 0, with "re-baseline recommended" for the DSP the image no longer
uses. Against a route of the recorded inputs the servo grew by 382 LUTs and 200 FFs, the offset rounder adds 148 and
190, and `KL_crf_tx`, its own converter and multiplier block no longer elaborated, shrank by 109 and 142. The worst
setup path is the SoC's write-beat counter into a block RAM enable, outside this PR. The first rounder used a
multiplier block against a DSP tolerance of zero; the shipped one divides by shifted adds and serves the CRF row too.

### The decision R678-1-F1 needs

Presenting each sample at the pin at its presentation time holds it for the presentation offset less its arrival
lead, about 1.9 ms at the 2 ms default, about 96 events: 128 event rows per 8-channel stream where the render stage
keeps 32. Measured by out-of-context synthesis at the AX7101 1x1 parameters: the queue alone grows from 456 to 1,006 LUTs
(LUTRAM 128 to 512), against 469 LUTs and 20 slices of route-1x1 headroom; in block RAM it adds two or three RAMB18
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
make -C tb/verilator/media_phase mutants MUTANT_JOBS=4
make -C tb/verilator/aaf
make -C tb/verilator/capture_coherence
make -C tb/verilator/milan_dp
python3 scripts/lint_rtl.py --check
bash scripts/run_all_suites.sh sweep-out
```

Expected result / pass criteria:

- `media_phase`: the pins (three synthetic interfaces), the blend (the in-tree I2S + TDM8 shape, six reset phases),
  the offsets (four AAF outputs and the CRF output, four runs), the ten detector cases and the thirteen loop cases
  each end `failures: 0`.
- `media_phase mutants`: the clean cases pass, then all twenty-seven planted defects fail their named checks.
- `aaf`: the golden byte-compare holds with both I2S front ends aligned.
- `capture_coherence`: the `[PIN]` leg and its campaign, every mutant caught.
- The lint gate stays at its ratchet; the full sweep exits 0.

Measured locally at the head `2ff30f0d` or an ancestor the later commits leave untouched for that gate:

| Gate | Result |
|---|---|
| `make -C tb/verilator/media_phase` | pins 11, blend 24, ofs 15, ten detector cases 46, thirteen loop cases, every one `failures: 0`: 26 tallies, 291 checks, about 533 s in the sweep at `2ff30f0d` |
| `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` | 46 checks, 0 failures: 18 clean controls, then 28 of 28 planted defects fail their named checks, 751 s (at `f1643214`; `2ff30f0d` changes a Makefile comment and one doc paragraph) |
| full sweep, `scripts/run_all_suites.sh`, four shards, at `2ff30f0d` | 64 of 64 suites, 2,187,770 checks, 0 failures: shard 0 15/15, 53,842 (the `tsn_fuzz` field campaigns ran: 164 and 677 pass); shard 1 16/16, 331,603; shard 2 17/17, 262,057 (`capture_coherence` inside its window: run 20,832, dp 447, campaign 35 of 35); shard 3 16/16, 1,540,268 |
| `python3 scripts/lint_rtl.py --check` | PASS, 89 <= ratchet 89 (at `44508dd8`; the RTL since changes the servo's unwrap to an identical mapping, linted clean before commit) |
| the docs workflow's 49 gates | all pass (at `f1643214`; `2ff30f0d`'s paragraph passes `docs_check` and `check_doc_style`) |
| `syn/yosys/run.sh` | 60 of 60 tops pass at `dd256343`, tap-purity and tied-input pass; the six tops changed since pass at `f1643214` |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | all gates pass except one not run for its recorded reason (it needs a separate Arty build tree on disk), at `f1643214` |
| `make -C tb/verilator/aaf`, `make -C tb/verilator/crf_tx` | pass (the golden byte-compare with both I2S front ends aligned; 129 crf_tx checks) |
| route-1x1 and `pp_resource_gate.py check` | exit 0 at `f1643214` (table above) |

## Known limitations / out of scope

- **The listener is not compensated; R678-1-F1 waits on the decision above.**
- **Bench proof.** The #764 method on the bench, after merge; this lane had no bench access.
- **AAF following** keeps the rate loop alone (`ph_en_i` low under an AAF source).
- **Offsets are not idempotent in whole ns.** Equation (14) rounds up to whole periods; a period count that is no
  multiple of three has a ceiling above it in whole ns, so writing back a read value of that kind applies one period
  more. The values a controller ordinarily sets, multiples of 62,500 ns, are exact. An offset above 4,294,958,333 ns
  rounds past 2^32 and is stamped and read back modulo 2^32.
- **The blend's two interfaces** start one audio clock cycle (40.7 ns) apart, which the grade measures inside the
  band; it is a property of the two front ends' dividers, not a derived constant.
- **The Arty shapes are retired**; the blend and the I2S capture fix are graded in simulation only.
- **Composition with dev** `78ca9bdf` was not merged in; the candidate merge belongs to the merge turn.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (talker and media clock in simulation; the listener item waits
  on the decision; bench after merge)
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
