[A424]

## Contents

- **[Status](#status)** -- Local gates, branch and head.
- **[Linked Issue / roles](#linked-issue--roles)** -- Relates to #617; executor and reviewers.
- **[Description](#description)** -- The frame-atomic TDM handoff, the new suite, the docs.
- **[Authoritative references](#authoritative-references)** -- The issue, the bench evidence, the clause.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and submodules.
- **[How to validate](#how-to-validate)** -- Reviewer commands and expected results, including the defect at `ce550952`.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this does not do.
- **[Definition of Done](#definition-of-done)** -- The merge bar.

## Status

GREEN locally at `5546b976161bdfd0611040160df44806a0b95d15` -- `617-capture-frame-atomic` -> `dev`, three
commits on dev `ce550952e47fbd92367f0d9b099345100f7f4215`. Every assigned local gate returned
rc 0 at that head (gate table in the evidence comment). Hosted checks have not run yet.

## Linked Issue / roles

Relates to #617

This PR covers #617 acceptance 1 to 3. Acceptance 4, a bench re-run of the #451 DIN capture
showing zero torn frames, follows on the next image, so this PR does not close the issue.

Executor: `[A424]`
Internal cleared-context reviewer: `[R394]`
External reviewer: `[R395]`

## Description

On the #451 bench, 67.5% of the talker's AAF columns mixed two adjacent TDM frames: pairs 1 to 3
one frame older than pair 0, in four states cycling once per 1.958 s beat. The capture crossbar
held each TDM pair in its own latest-sample register, written by that pair's strobe, and the
media-tick walk read each register at its own slot's inject.

| Piece | Change |
|---|---|
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | The TDM bucket becomes three banks. STAGE is written by each pair strobe, as before. FRAME is published in one edge by the strobe of the frame's last pair (new parameter `TDM_FRAME_PAIRS_P`, with an elaboration guard). WALK is loaded from FRAME on the pre-walk's last cycle and held for the whole walk, so a frame closing mid-walk waits for the next tick. The walk bank is required: an 8x8 walk (866 cycles) outlasts the two TDM slots between a frame's last pair and the next frame's first (260 cycles at 50 MHz). |
| `hdl/milan/milan_datapath.sv` | Passes `TDM_FRAME_PAIRS_P = min(AIF_PAIRS_C, 4)`, the front end's per-frame pair supply clipped to the four pairs the bucket keeps: 4 on the shipping 1x1 TDM8 shape, 1 on the I2S shapes, 4 on the Arty blend (closing on its TDM pair 2). |
| `tb/verilator/capture_coherence` (new) | Junction leg: the real TDM8 master, media NCO, grid aligner, crossbar and packetizer at the shipping 1x1 TDM8 shape and a 50 MHz axis clock. The #451 pattern is shifted into the TDM data pin off the master's own bclk and fsync, and every AAF column is decoded. INTERNAL runs one whole beat of the true 391/1591 plan (-10.64 ppm) and several beats at +/-1000 ppm. CRF locks at 16 phases on the true plan and 4 phases at each of +/-50 ppm. Datapath leg: the same bench through the whole `milan_datapath` on the shipping shape, frames read at the MAC; INTERNAL at +/-1000 ppm, CRF at 8 phases. `mutants.py`: six mutants, the first being the `ce550952` per-pair law. |
| `tb/verilator/chmap_capture` | New `[F]` section: six columns of one PDU, each with one right answer, including a frame that closes between two of a walk's TDM slots. `[A]`/`[LB5]` deliver whole frames; lane B elaborates the one-pair frame of the I2S shapes. |
| Docs | `TIME_SYNC.md`: new "Talker capture handoff" subsection with the measured latency change. `CHANNEL_MAP_64.md` section 4 and section 7. `REGISTER_MAP.md` (SLIP_TDM wording). `FPGA_DESIGN.md`. `TESTING.md` suite index. `CHANGELOG.md`. The traceability matrix is regenerated. |

Unchanged: the render (DOUT) path, the channel-map semantics, the #74 junction slip counters and
the aligner's marker. No port of `KL_chan_map_capture` or `milan_datapath` changed. There is no
processor, firmware or parent-interface change.

Latency, measured over one beat of the true plan (sample age at the walk's tick, 50 MHz cycles):

| Pair | `ce550952` mean | head mean | Change |
|---|---:|---:|---|
| 0 | 519.4 | 1307.1 | +15.75 us |
| 1 | 488.5 | 1046.7 | +11.16 us |
| 2 | 457.6 | 786.3 | +6.57 us |
| 3 | 426.7 | 525.8 | +1.98 us |

Pair 3 is the frame's last sample. Its change is the read instant moving to before slot 0. The
earlier pairs wait for their frame to complete, which is what atomicity requires. Every walk
reads the newest complete frame, and a check grades that per walk.

Resources: `KL_chan_map_capture` alone at the 1x1 TDM8 parameters, using the `syn/yosys/ooc.sh`
recipe (Yosys 0.66). LUT 1292 -> 1263, LUTRAM 32 -> 32, FF 1048 -> 1384 (+336 = 7 x 48 bits),
BRAM 0 -> 0. At the 8x8 parameters: LUT 2062 -> 2103, FF 1595 -> 1931, BRAM 0 -> 0.

## Authoritative references

- #617 body and the assignment comment (manager decisions: frame-atomic handoff at the crossbar
  input; no added sample of latency; render path and channel-map semantics unchanged; committed
  simulation in INTERNAL and CRF with drift; removed-atomicity mutant; resources on 1x1 TDM8).
- PR #616, `docs/findings/451_TDM8_FIRST_LIGHT.md` section "DIN frame coherence", and its
  review R392-1 (F2, the re-derivation against `KL_chan_map_capture.sv:486-487,959-960`).
- IEEE 1722-2016 7.3.5: AAF-PCM carries sample events in order, one sample per channel per
  event.
- `docs/CHANNEL_MAP_64.md` section 4; `docs/design/TIME_SYNC.md` "Media boundary".

## How to get into the same state

```sh
git fetch origin
git checkout 617-capture-frame-atomic
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
make -C tb/verilator/capture_coherence      # junction leg, datapath leg, mutation arm (about 6 min)
make -C tb/verilator/chmap_capture
python3 scripts/lint_rtl.py --check
OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture
```

Expected result / pass criteria:

- `capture_coherence: checks: 456 failures: 0`, `capture_coherence_dp: checks: 118 failures: 0`.
- `mutants.py`: 8 checks, 8 PASS: two clean controls and six mutants, each caught by its named
  check.
- `KL_chan_map_capture: 254 checks, 0 failures` and the netlist pin `20 checks, 0 failures`.
- The defect reproduces at `ce550952`: build the same harness with that commit's
  `KL_chan_map_capture.sv` (drop the wrapper's `TDM_FRAME_PAIRS_P` line). The junction leg then
  reports 47 failures in 456 checks, with INT-true 66.1% torn in the #451 states 0,0,0 33.9%,
  -1,-1,-1 / 0,0,-1 / 0,-1,-1 22.0% each. The datapath leg with that commit's
  `milan_datapath.sv` reports 7 failures in 118 checks. The committed mutation arm's first mutant
  is the same per-pair law.

## Known limitations / out of scope

- Bench acceptance 4 (#617) needs the next image.
- Under CRF the aligner keeps the slot-0 marker 1/128 sample off the tick. The crossing that now
  decides a column is the frame close against the walk snapshot. An engagement landing within
  the lock's few-cycle dither of it would alternate repeat and skip until re-engagement. The
  per-pair holds had four such crossings; there is now one, and none of the 32 simulated CRF
  phases hit it. Keying the aligner's keep-off on the frame close is possible follow-up work
  (not filed from this lane).
- On the Arty blend shapes the crossbar's four-pair TDM bucket keeps the I2S pair and TDM pairs
  0 to 2. TDM pair 3 was already unreachable through the crossbar before this change.
- Area is the standalone OOC estimate; the in-context datapath delta and placed Vivado
  utilization are not measured here.

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
