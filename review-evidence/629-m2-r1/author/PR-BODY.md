[A491]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOPPED FOR A RULING, otherwise GREEN — 59/59 suites, 2,148,251 checks, 0 failures — `629-media-clock-impl` -> `dev`, head `57f4b742b504f5e69293aaa3e00d0470aa9b6071`.

Named design statements that did not hold as written are listed under
[Known limitations](#known-limitations--out-of-scope) and in the design page's
Implementation notes; they wait on a decision on #629.

## Linked Issue / roles

Relates to #629

Executor: `[A491]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The end station follows one selected media-clock source: INTERNAL, the CRF
input, or one AAF Stream Input, as `docs/design/MEDIA_CLOCK_FOLLOWING.md`
(PR #631) designs it, with every decision as ruled (D1 = L1, D2, D3 = W2,
D4 = A2-a, D5 = C1, D6, D8 = E8, lost-PDU rule (b)).

| Area | Change |
|---|---|
| Requirements | FR-CLK-03 and FR-CLK-04 and their status row amended to the owner decision |
| Builder and model | `input_stream` admitted again: one INPUT_STREAM CLOCK_SOURCE per AAF listener, located on it, listed INTERNAL 0, CRF 1, AAF input k at 2 + k; the CLOCK_DOMAIN lists them all; per-index kind and STREAM_INPUT tables in the shape header; all five shipping configurations regenerated (each `entity_model_id` moves once); a servo prune that offers only an AAF source is refused |
| AAF clock meter (new) | `KL_aaf_clock_meter`: 48 kHz Base format only (`stream_data_length` = 24 x channels), the mean of each group of 16 by `sequence_num` mod 16, the 4,096 ns jump bound and in-group void, rule (b) with the k = 2 check and the midpoint fill, E8's two-point rate over 4.096 s from an 8-entry LUTRAM ring, lock 8 PDUs in / 100 ms out, era rules, `disrupt_p` on its own timeout only, the received `mr` seeded silently, a status word. No DSP, no BRAM |
| Root | the stored index decoded through the generated tables; the meter on the parser bundle with the common-header `tu`; one reference mux, presented unlocked for one cycle on every change (W2); the meter's two pulses ORed into the restart request; C1 counter level `~tu & (~follow | servo LOCKED)`; A2-a (the grid aligner and NCO engaged at INTERNAL too) |
| Servo | `KL_mmcm_drp_servo` takes a one-bit select and one reference (`sel_i`, `ref_*`), adds `locked_o`; state machine and arithmetic unchanged |
| CSR | `AAFM_STAT` 0x8E0 and `AAFM_RATE` 0x8E4, RO live, each with its read-window term; VERSION stays `0x0002_0060` (see limitations) |
| Tests | `tb/verilator/aaf_clock_meter` (every meter row, the servo with the meter over 180 s, 26 named mutants); `tb/verilator/milan_dp_mclk` (every root row at the true audio ratio, 14 named mutants as schemata in the default target); `milan_dp` [CLKSRC-WALK] and the pins of the old INTERNAL free run; CSR bench; builder gates |
| Docs | register map, changelog (release note on saved state, KNOWN RISK), feature ledger, compliance matrix, descriptor ownership L6, time-sync media boundary, the design page's status and Implementation notes |

No top-level port, pin, SoC change, root parameter, processor-boundary port or
protocol-processor change.

## Authoritative references

- `docs/design/MEDIA_CLOCK_FOLLOWING.md` and its rulings on #629
- `docs/reference/FR_NFR.md` FR-CLK-03, FR-CLK-04
- IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7, 7.2.4, 7.3.3, 7.3.5, 10.8
- IEEE 1722.1-2021 6.2.2.8, 7.2.9, 7.2.32, Table 7-16, Table 7-141, 7.4.23.1
- Milan v1.2 5.3.3.6, 5.3.11.1, 6.2, 7.2.2, 7.3.2, 7.4
- protocol-processor #141 (no processor RTL change)

## How to get into the same state

```sh
git fetch origin
git switch 629-media-clock-impl
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
make -C tb/verilator/aaf_clock_meter        # meter rows, servo with the meter, 26 mutants
make -C tb/verilator/milan_dp_mclk          # root rows (legs A, B, C) and 14 mutants
make -C tb/verilator/milan_dp               # [CLKSRC-WALK], A2-a pins, T67
make -C tb/verilator/csr
python3 sw/builder/test_builder.py
python3 scripts/check_entity_shape.py
scripts/run_all_suites.sh <outdir>
TAG=<tag> sw/litex/build.sh ax7101          # the shipping image
```

Expected result / pass criteria: every suite and gate exits 0; each mutant
runner reports every named mutant caught; the AX7101 image meets timing with no
CRITICAL WARNING and no #607 constraint refusal. Measured at this head: 59 of 59 suites pass across the five shards (2,148,251 checks); the root suite 27/27 and the meter suite 27/27 in their campaigns;
image WNS +0.107 ns, WHS +0.014 ns, 0 critical warnings.

## Known limitations / out of scope

- VERSION stays `0x0002_0060`, as for #443's `RENDER_STAT`; the design's
  Registers row says VERSION moves. Needs a decision on #629.
- Design statements that did not hold as written, each with what was done:
  the listener-only builder shape cannot be built (graded at the overlay);
  the AECP walk cannot see the servo leave IDLE without a locked reference
  (graded at the decode, the servo's select and the meter's status word);
  the root counter row's loss leg is 3 s, not 60 s (suite guard); the root
  counter row needs a `tu` test double in that suite; one #386 recentre per
  switch is graded over 0.8 s gaps; the servo-with-meter row lives in the
  meter suite; the meter's FF count (636) is over the 270 to 420 estimate.
- KNOWN RISK: at INTERNAL the media clock is the MMCM plan; Milan v1.2 7.4's
  +/-50 ppm holds only for a board-oscillator grade of +/-39 ppm or better
  (assumed adequate by owner decision, unconfirmed).
- Slice occupancy of the shipping image is 99.98 %.
- Phase alignment of the outputs to the followed stream (IEEE 1722-2016 10.8,
  4.3.5) is #632; the CRF receiver's own rate weakness is #633.
- The bench acceptance (THD+N, following AAF and CRF, through a switch) is a
  later bench lane.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
