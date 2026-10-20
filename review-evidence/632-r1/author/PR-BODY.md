[A659]

## Contents

- **[Status](#status)** — Gate tally, and `632-764-media-phase` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout and dependency commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN: every local gate passes at `f1fda3f1` (64 of 64 suites, 17 of 17 phase mutants, route-1x1 within the resource gate and the timing floor, lint, Yosys, the docs gates). `632-764-media-phase` -> `dev`. The bench proof follows after merge.

## Linked Issue / roles

Relates to #632
Relates to #764

#632's simulation acceptance item is met. Its bench item, and #764's bench proof, follow after merge with the #764
method, so neither Issue is closed by this PR.

Executor: `[A659]`
Internal cleared-context reviewer: `[R<n>]`, to be assigned
External reviewer: `[R<n>]`, to be assigned

## Description

The media servo locked frequency only, so each engagement kept whatever phase its pull-in left. #764 measured the
DUT's own CRF output and its AAF stream off the followed CRF stream's timing points, with a constant -0.46 Ps between
the two. This PR phases the one media-clock master, `KL_mmcm_drp_servo`, to the followed CRF stream, against one
phase reference per clock domain, and gives each media interface its own derived latency constants relative to it.

| Piece | Change | Clause |
|---|---|---|
| Domain media event (`KL_media_domain_event`, new) | Each frame's instant at the media interface: the frame-timing owner's closing-pair strobe, back-dated by that owner's marker latency. One per clock domain. Every consumer of the domain takes its instant from it | IEEE 1722-2016 4.3.5 |
| Per-interface constants (`KL_media_if_latency_pkg`, new) | Marker latency counted to the closing pair's last bit (the crossbar closes a frame on the last pair it keeps, an inner pair on a bus wider than TDM8), plus the front end's FIFO write and the read side; slot k's MSB offset. Derived from each interface's own parameters, never mirrored | 4.3.5, 10.8 |
| Phase detector and loop (`KL_mmcm_drp_servo`) | Per accepted, consumed CRF PDU, the domain event less its timestamp, folded exactly into +/-Ps/2 in 1/3 ns (Ps = 62,500/3 ns); the window phase is the sum over the 512 ms window's nominal 256 PDUs. It enters the integrator one window late, clamped: type 2 against phase, the rate loop as its damping, the pull slew-limited to 0.5 ppm. The integrator keeps 8 fractional bits, so odd errors are carried (the #764 floor leak, up to 1.95 ns/s) | Milan v1.2 7.6.1; IEEE 1722-2016 10.7 Eq. (14), 10.8 Eq. (15) |
| Hold conditions | Outside LOCKED, an `mr` toggle, a broken reference history, a local PHC step (#539) or policy slew (#545): the term lets go and the open window is spoiled; re-acquisition pulls at most Ps/2, the short way | 10.8 |
| Window cap | A window keeps at most 264 samples (256 + 1/32), so a talker sending faster than its declared interval cannot wrap the 16-bit window phase | 10.8 |
| Settled status | `MCSRV_STAT[9]`, a previously reserved read-only bit: inside +/-5 % of Ps for four windows running | 10.8 |
| CRF output (`KL_crf_tx`) | Every 96th domain event is a timing point, stamped with its instant plus the Equation (14) offset; the free-running /512 /96 divider and its clock crossing are retired | 10.7 Eq. (14), 4.3.5 |
| CRF receive (`KL_crf_rx`) | Publishes each consumed PDU's timestamp (`ts_p_o`, `ts_o`) | 10.8 |
| AAF talkers (`KL_chan_map_capture`, `milan_datapath`) | The capture crossbar banks each frame's instant beside the frame and loads it into the walk with it; the talkers stamp that instant, so capture age and pair offset leave the timestamp | 4.3.5, 10.8 |

The -0.46 Ps is accounted for in full: the old AAF stamp's distance from its own frame (the marker latency and the
frame's age at the tick, 0.536 Ps, about 559 axis cycles, the only solution inside the recorded 256 to 785 band).
Both outputs now stamp the frame instant, so no aligner target moves
([accounting](docs/design/MEDIA_CLOCK_FOLLOWING.md#the-measured--046-ps)).

**Two `milan_dp` fixtures re-timed.** The CRF talker's cadence now follows the domain event rather than a divider of
`clk_audio_i`. These fixtures toggle the audio and TDM clocks with `axis_clk`, so the cadence differs by shape there,
where in hardware every shape's frame is 48 kHz. The #726 counters leg runs its TX wrap for `400000 x slots / 8`
cycles, because the 8x8's TDM32 frame is four times the TDM8 frame in that fixture. The nxn legs wait 200,000 clocks
for a CRF PDU, the media-tick fallback on nxn4c, whose TDM master that fixture leaves unclocked. The checks
themselves are unchanged.

No top-level port and no register-map layout changes. Module ports change on `KL_mmcm_drp_servo` (phase inputs,
`phase_o`, `ph_settled_o`), `KL_crf_tx` (`ev_p_i`/`ev_ns_i` replace `clk_audio_i`/`ptp_ns_i`), `KL_crf_rx`
(`ts_p_o`/`ts_o`) and `KL_chan_map_capture` (`tdm_close_ns_i`, defaulted, and `tdm_walk_ns_o`).

**Resources.** route-1x1 under the recipe, checked by `pp_resource_gate.py` against the recorded baseline (dev
`e26f1816` differs from the record's inputs only in firmware tests and docs):

| Figure | Record | Head | Delta | Tolerance / floor |
|---|---:|---:|---:|---|
| LUT | 49,613 | 49,644 | +31 | +500 |
| FF | 52,353 | 52,641 | +288 | +600 |
| Slice | 15,725 | 15,785 | +60 | +80 |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 0 | +0 |
| WNS | +0.215 ns | +0.276 ns | +0.061 | at least +0.030, fall at most 0.25 |
| WHS | +0.036 ns | +0.032 ns | -0.004 | at least 0, fall at most 0.25 |

Route complete, no unrouted net; gate exit 0. Against a route of the recorded inputs, the servo grew by 264 LUTs and
180 FFs, the domain event by 79 FFs and the CRF receiver and capture crossbar by about 33 and 64 FFs; `KL_crf_tx`
shrank. The worst setup path is the servo's existing reset synchroniser into its 200 MHz phase-shift domain, whose RTL
this PR does not touch.

The first draft failed this gate (LUT +716, FF +719), so the detector was made smaller before review: each sample
folds on its own (no PDU-to-PDU unwrap), the window phase is a shift of the window sum rather than a division, and
the detector works on the low 32 bits of each instant. Yosys out-of-context, `KL_mmcm_drp_servo`: 865 LUT / 792 FF
at the base, 1,457 / 1,183 in the first draft, 1,168 / 982 now. Across this lane's three routes the processor
wrapper, whose RTL none of them changed, moved between -106 and +384 LUTs against the record, so the route's LUT
figure carries placement-dependent movement of that order.

**Re-baseline: a decision for the merge.** The area budget asks a merge that moves the shipping image to re-record
its endpoints on the merge result. That record, and the AREA_BUDGET and #234 findings text that accompanies it, lie
outside the media-clock chain this lane is confined to, so it is not written here.

## Authoritative references

- Milan v1.2 7.6.1 (media clock: frequency and phase), 7.3.2 (CRF timestamp interval).
- IEEE 1722-2016 10.6 to 10.8 (Equations (14), (15), (16)), 4.3.5 (streams of one media clock on whole periods).
- [docs/design/MEDIA_CLOCK_FOLLOWING.md, Phase alignment](docs/design/MEDIA_CLOCK_FOLLOWING.md#phase-alignment): the
  domain event, the per-source contract, the detector and loop, the per-interface constants, the listener decision,
  the -0.46 Ps accounting and the proof table.
- [docs/design/TIME_SYNC.md](docs/design/TIME_SYNC.md): the domain event, the servo phase term and the talker
  capture hand-off.
- The assignment and its two addenda on #632; #764's investigation report.

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
make -C tb/verilator/capture_coherence
make -C tb/verilator/chmap_capture
make -C tb/verilator/milan_dp
python3 scripts/lint_rtl.py --check
bash scripts/run_all_suites.sh sweep-out
```

Expected result / pass criteria:

- `media_phase`: the three-interface pins check and ten cases (`engage`, `engage2`, `step`, `ramp`, `holdover`,
  `internal`, `mr`, `slew`, `burst`, `carry`) each end `failures: 0`; every case is pulled into +/-5 % of Ps and
  held, and every event case sees the phase term let go at its event.
- `media_phase mutants`: the clean cases pass, then all seventeen planted defects fail their named checks.
- `capture_coherence`: the `[PIN]` leg grades the shipping talker's stamps at the TDM8 pins; its campaign kills
  every mutant, the five #632 ones included.
- The lint gate stays at its ratchet; the full sweep exits 0.
- route-1x1 under `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: `pp_resource_gate.py check` exits 0.

Measured locally at the head `f1fda3f1` (the RTL is identical since `a6ae20f9`):

| Gate | Result |
|---|---|
| `make -C tb/verilator/media_phase` | pins and the ten cases pass (in the sweep) |
| `make -C tb/verilator/media_phase mutants MUTANT_JOBS=4` | 27 checks, 0 failures: 10 clean cases, then 17 of 17 planted defects fail their named checks (at `e85df091`; no media_phase or RTL file changed since) |
| full sweep, `scripts/run_all_suites.sh`, four shards | shard 0: 15/15, 52,903 checks (with the tsn-gen field campaigns: 164 + 677 pass); shard 1: 16/16, 331,441 checks (at `e85df091`; the later commits change three `milan_dp` fixture files that no shard-1 suite compiles); shard 2: 17/17, 262,022 checks plus `capture_coherence` (its 25-mutant campaign hit the sweep's 2,400 s wall clock on the two CPUs that keep it at two builds, so it was re-run alone inside the same budget: run 20,832, dp 447, campaign 35 of 35); shard 3: 16/16, 1,540,268 checks |
| `python3 scripts/lint_rtl.py --check` | PASS, 89 <= ratchet 89 |
| the docs workflow's 49 gates | all pass |
| `syn/yosys/run.sh` | 59 of 59 tops pass, tap-purity pass |
| route-1x1 and `pp_resource_gate.py check` | exit 0 (table above) |

## Known limitations / out of scope

- **Bench proof.** The #764 method on the bench, after merge; this lane had no bench access.
- **The listener is not compensated; a decision is needed.** The render path presents by fill, 8 events after
  accept (#386), not at the `avtp_timestamp`, so there is no presentation time to count the post-grid pin delay
  against. Its constants are derived and documented; making the render present at the timestamp changes the listener
  datapath, outside the media-clock chain.
- **AAF following** keeps the rate loop alone (`ph_en_i` low under an AAF source): a phase reference for it needs a
  decision on presentation offsets that are not whole periods.
- **An AAF offset that is not a whole number of periods** moves that stream off the grid by its fraction; every whole
  millisecond is one, and the 2 ms default is 96 periods.
- **Stale comments outside the chain**: four builder and configuration comments still name the retired `KL_crf_tx`
  /512 divider. The builder and configurations are outside the media-clock chain; a follow-up Issue is proposed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (simulation yes; bench after merge)
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
