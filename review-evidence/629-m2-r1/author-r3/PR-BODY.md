[A491]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — What round 2 changed, answering R432-1 and R433-1.
- **[Round 3](#round-3)** — What round 3 changed, answering R433-2 and R432-2, and the hosted jobs replayed under GNU make 4.3.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN after round 3, for the delta review — 59/59 suites, 2,149,266 checks, 0 failures, every hosted job replayed green under GNU make 4.3 — `629-media-clock-impl` -> `dev`, head `0b066b6e66df2a3ba3167805a6a591f8b96fa449`.

The eight design statements that did not hold as written are accepted as
implemented by the [ruling on #629](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946491571)
and listed in the design page's Implementation notes.

## Linked Issue / roles

Relates to #629

Executor: `[A491]` (round 1), `[A494]` (round 2), `[A500]` (round 3)
Internal cleared-context reviewer: `[R432]` (round 1 NEGATIVE; round 2 POSITIVE at `d81198c2`)
External reviewer: `[R433]` (round 1 NEGATIVE; round 2 NEGATIVE at `d81198c2` on one MINOR; delta review pending)

## Description

The end station follows one selected media-clock source: INTERNAL, the CRF
input, or one AAF Stream Input, as `docs/design/MEDIA_CLOCK_FOLLOWING.md`
(PR #631) designs it, with every decision as ruled (D1 = L1, D2, D3 = W2,
D4 = A2-a, D5 = C1, D6, D8 = E8, lost-PDU rule (b)).

| Area | Change |
|---|---|
| Requirements | FR-CLK-03 and FR-CLK-04 and their status row amended to the owner decision |
| Builder and model | `input_stream` admitted again: one INPUT_STREAM CLOCK_SOURCE per AAF listener, located on it, listed INTERNAL 0, CRF 1, AAF input k at 2 + k; the CLOCK_DOMAIN lists them all; per-index kind and STREAM_INPUT tables in the shape header; all five shipping configurations regenerated (each `entity_model_id` moves once); a servo prune that offers only an AAF source is refused |
| AAF clock meter (new) | `KL_aaf_clock_meter`: 48 kHz Base format only (`stream_data_length` = 24 x channels), the mean of each group of 16 by `sequence_num` mod 16, the 4,096 ns jump bound and in-group void, rule (b) with the k = 2 check and the midpoint fill, E8's two-point rate over 4.096 s from an 8-entry LUTRAM ring, lock 8 PDUs in / 100 ms out, era rules, `disrupt_p` on its own timeout only, the received `mr` seeded silently, its largest deviation (`max_dev_ns_o`) and a status word. No DSP, no BRAM |
| Root | the stored index decoded through the generated tables; the meter on the parser bundle with the common-header `tu`; one reference mux, presented unlocked for one cycle on every change (W2); the meter's two pulses ORed into the restart request; C1 counter level `~tu & (~follow | servo LOCKED)`; A2-a (the grid aligner and NCO engaged at INTERNAL too) |
| Servo | `KL_mmcm_drp_servo` takes a one-bit select and one reference (`sel_i`, `ref_*`), adds `locked_o`; state machine and arithmetic unchanged |
| CSR | `AAFM_STAT` 0x8E0 and `AAFM_RATE` 0x8E4, RO live, each with its read-window term; VERSION stays `0x0002_0060` (ruled) |
| Tests | `tb/verilator/aaf_clock_meter` (every meter row, the servo with the meter over 180 s, 35 named mutants); `tb/verilator/milan_dp_mclk` (every root row at the true audio ratio, 16 named mutants as schemata in the default target); `milan_dp` [CLKSRC-WALK] and the pins of the old INTERNAL free run; CSR bench; builder gates |
| Saved state | the capture timing re-measured for the census the CLOCK_SOURCE NAME records grow |
| Docs | register map, changelog (release note on saved state, KNOWN RISK), feature ledger, compliance matrix, descriptor ownership L6, time-sync media boundary, the saved-state sizing pages, the design page's status and Implementation notes |

No top-level port, pin, SoC change, root parameter, processor-boundary port or
protocol-processor change.

## Round 2

Answers [R432-1](https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5946971135)
and [R433-1](https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5946892577),
in the order of the [round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946975634).

| # | Finding | What changed |
|---|---|---|
| 1 | R432-1 F1 = R433-1 F2 (MAJOR): the capture receipt was measured for the old census | Re-measured per `tb/verilator/nvm_capture_cpu/README.md`, both shapes at 50 MHz with aligned edges, traffic ON and OFF, 16 captures each, and the labelled 100 MHz 8x8 point. The 8x8 contract maximum is 13.86484 ms against the 24.5 ms limit (margin 10.63516 ms; it was 13.23352 ms); 1x1 3.96728 ms; the non-contract 100 MHz 8x8 point 10.42973 ms. The census grows from 156 to 164 records and 12,634 to 13,210 bytes at 8x8, 53 to 54 and 3,218 to 3,290 at 1x1; firmware, hold and measured paths are unchanged. The harness now takes the census each row must copy from the generated shape (`nvm_shape.closed_record_census`, shared with the gate) instead of a literal. The first run found a harness defect: the simulator's TX-frame trace shares stdout with the firmware's console and split a CAPTURE row in the 8x8 OFF arm; the trace is now held until the console stands at a line start, and all six arms were re-run (the arms that completed both times reproduce every capture's cycle count). `measurements.json`, the saved-state ownership page's section 18 (and its sections 17 and 20), the harness README and the FASTCONNECT section 4.2 sizes the census drives are refreshed |
| 2 | R432-1 F2 (MAJOR): the root suite's nested source list under GNU make 4.3 | `--no-print-directory` on both nested derivations (`tb/verilator/milan_dp_mclk/Makefile`). Reproduced first under a real GNU make 4.3: the schemata failed with `Cannot find file containing module: 'Entering'`. After the fix the same make 4.3 run builds and runs the campaign, rc 0 |
| 3 | R432-1 F3 and the builder bank: two ratchets and `git diff --check` | `//!` contracts on the meter's `clk_i`, `rst_n` and `subtype_i`; `CLK_FREQ_HZ_P` documented in Hz; `fsh_i` documented by its octets; the largest deviation split out of `status_o` as `max_dev_ns_o` (the root composes `AAFM_STAT` as before, area unchanged); the design page's trailing blank line removed. Both budgets unchanged |
| 4 | R433-1 F1 = R432-1 F4; R432-1 F5 | The root plants "`tu` taken from the `tv` net" (mutant 15) and leg A's followed talker sets, then clears, `tu`: each edge restarts the meter's history with no request. The meter suite now grades where each escaped rule lands: the restart at the step's PDU (M3, M12), a gap breaking the settle run (M6), the lock across a listener change, entry, a `tu` edge and the bind edge (M7), zero channels refused (M4), and the largest deviation (M1). The five probes and the largest-deviation probe are named mutants; a listener change keeping the lock also fails at the root (mutant 16, a switch onto a talker silent past the meter's timeout). `reviewer_meter_probes.py` from R432-1's packet, unmodified: 15 of 15 CAUGHT, F5's five among them |
| 5 | R433-1 F3 = R432-1 F7; R433-1 F4; R432-1 F6 | FR_NFR status row; the 0x8C8 section's sentence now maps `AAFM_STAT` and `AAFM_RATE` and leaves `0x8E8` to `0x8F4` unmapped; the `obj_aclk` row names `milan_dp_mclk` mutant 3 |
| 6 | RESIDUE and suggestions | R433-1 R1 to R3 and R432-1 R1, R2 and R4 taken in the tree; R432-1 R3 in this body. R432-1 S2 taken (FR-CLK-04's `mr` shall qualified). R433-1 S2 taken for `sim_aclk` (two-sided, measured +0.80 ppm), retained for render T30 (see limitations). R432-1 S1 = R433-1 S1 retained (see limitations) |

## Round 3

Answers [R433-2](https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5952528640)
(NEGATIVE on F1) and [R432-2](https://github.com/kebag-logic/milan-fpga/pull/634#issuecomment-5952049290)
(POSITIVE; S1 and R1 taken), in the order of the
[round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5952544402).
Three commits on `d81198c2`, none amended. No RTL change, so the shipping image is not rebuilt.

| # | Item | What changed |
|---|---|---|
| 1 | R433-2 F1 (MINOR): the hosted `docs-check` "Entity shape gate" fails under GNU make 4.3 | **Cause, reproduced.** GNU make 4.4 exports its own flags to `$(shell ...)`, so the inventory's `make -pqrR` database read ran the root suite's nested `$(shell $(MAKE) ... print-srcs)` in question/print mode. print-srcs failed and the parse stopped at the `$(error)` on `tb/verilator/milan_dp_mclk/Makefile:59`, before any rule. The host's 4.4.1 therefore listed no frozen prerequisite and passed with nothing read. GNU make 4.3 read the whole file and listed the `mclk-build` prerequisite expanded, `obj_mclk_aem/endstation_mclk/gen/adp_shape_defaults.svh`. `CLASSIFIED_CONSUMERS` held only the spelled form, which no database token carries. At `d81198c2` the plain mode fails under make 4.3 too (rc 1). **Fix (`bb65ac49`).** `scripts/shape_consumer_inventory.py` matches a makefile's classified reference in its frozen form through make's own expansion (`classified_frozen_targets`), not a second literal. A frozen prerequisite that resolves to the same repo path is that consumer, with its reason. A reference make cannot settle still classifies nothing. The root suite's entry and every other entry are unchanged. `tb/verilator/milan_dp_mclk/Makefile` runs both nested derivations as `$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory ...)`: the nested make takes no flag from its parent, so 4.4.1's parse completes too and the classification is exercised on both makes. `scripts/entity_shape_selftest.py` adds three arms: the frozen form classified (control); the derivation removed, which is the hosted refusal (must fail); a rule that freezes before its variable is defined, a frozen form naming another path (must fail). **Verified** with R433-2's `make43_checks.sh`, unmodified: gate rc=0 under GNU make 4.3 (222/0) and under the host's GNU Make 4.4.1 (222/0). Root suite under make 4.3: rc 0, legs A 55/0, C 32/0, B 50/0, 31/31 |
| 2 | Every hosted job this PR feeds, step by step, under GNU make 4.3 | Each job's steps are read from its workflow file and run verbatim (`bash -e`, the job, step and workflow env with the PR event's expressions resolved) at ``0b066b6e``. GNU make 4.3, built from the GNU release tarball, is first on PATH behind a shim that logs every make invocation per step. Result: every job green, every make invocation GNU make 4.3 (table below). Round 2's replica ran the plain modes under the host make; this replay runs `check_entity_shape.py --self-test` as `docs-check` step 50 does, 222/0 with 363 make calls, all 4.3 |
| 3 | R432-2 S1 = R433-2 S1, taken: `max_dev_ns_o`'s era clear and saturation | M1 (`case_rates`) now grades the field as a level (`7f051b27`). After a +100 ppm era (187.5 ns), each era start onto a 0 ppm talker must read exactly 0: listener change, entry (with the exit window, "reads 0 while not following"), bind edge and the 100 ms timeout. A PDU after a sequence gap is no deviation. Steps of +65,535, +65,536 and +/-100,000 ns at group position 5 each restart the history once and then read min(\|step\|, 65,535), so the data restart keeps the reading. R433-2's three `meter_probes.py` edits are named mutants: `max_dev_not_cleared_at_era_start`, `max_dev_no_saturation`, and `max_dev_includes_gap_pdus`, that run's third survivor at `d81198c2`. Meter suite under make 4.3: 465/0 (+19), servo 6/0, campaign 36/36. R433-2's `meter_probes.py`, unmodified: all five probes CAUGHT. R432-2's `reviewer_meter_probes_r2.py`, unmodified: P1 and P2 CAUGHT on `rates`, P3, P4 and P6 CAUGHT; P5 escapes the meter suite and is caught at the root, as R432-2 recorded |
| 4 | RESIDUE R432-2-R1, taken | The design page's meter "Outputs" bullet carries the reviewer's exact text: the status word without the largest deviation, then `max_dev_ns_o`, and "The root composes the two into `AAFM_STAT`." (`0b066b6e`) |

### Hosted jobs replayed under GNU make 4.3

| Workflow / job | Steps: run verbatim (of them path-mapped) / substituted; actions; skipped by `if:` | make invocations, all GNU make 4.3 | Result |
|---|---|---|---|
| docs.yml `docs-check` | 50: 43 (0) / 3; 4; 0 | 2,947 (steps 19, 25, 26, 31, 50) | 46 of 46 run steps rc 0. Entity shape gate (`--self-test`) 222/0 with 363 make calls; builder gates `ALL GATES PASS EXCEPT 14 NOT RUN`, the LiteX gates, as on the hosted job, which has no LiteX; step 43 not run (below) |
| docs.yml `wire-accountability` | 3: 2 (0) / 0; 1; 0 | 0 | rc 0, 77/0 |
| docs.yml `docs-check-no-git` | 2: 0 / 1; 1; 0 | 0 | rc 0 in an export without `.git` |
| rtl.yml `full-ci-gate` | 5: 4 (0) / 0; 1; 0 | 0 | rc 0; `rtl=true`, `run_full=true` |
| rtl.yml `verilator-shards` 0, 1, 2, 3, 4 | 14 each: 5 or 6 (1) / 0, or 2 on shard 3; 3 or 4; the rest skipped | 41, 276, 173, 55, 34 | 11/11, 23/23, 12/12, 12/12, 1/1 suites; 401,934, 197,119, 1,523,725, 14,649, 11,839 checks, 0 failures. Shard 1 built the pinned tsn-gen oracle, so `tsn_fuzz` ran its field campaigns with no declared skip |
| rtl.yml `verilator-suites` | 5: 3 (0) / 0; 2; 0 | 0 | 59 suites, 2,149,266 checks, 0 failures; target SHA 5 of 5 records |
| rtl.yml `yosys-shards` 0 to 3 | 10 each: 3 (0) / 2; 4; 1 | 0 | rc 0 each |
| rtl.yml `yosys-portability` | 5: 3 (0) / 0; 2; 0 | 0 | 55 of 55 tops and the structural gates; target SHA 4 of 4 |
| rtl-fast.yml `changes`, `verilator-lint`, `bdd-conformance`, `yosys-elaboration`, `rtl-fast` | 2, 6, 4, 10, 1 | 0 | rc 0 each; lint 90 <= 90; 404 scenarios, 1,968 steps; the aggregate reads all four `success` |
| elaborate.yml `elaborate` | 20: 11 (1) / 1; 7; 1 | 1,540 (steps 15, 19) | rc 0. `--require-elaboration --require-rv32` gates `ALL GATES PASS EXCEPT 2 NOT RUN`, both for recorded reasons: gate 1b's `MAKEFLAGS += -e` arm needs a make that re-reads MAKEFLAGS mid-parse, which make 4.3 does not; gate 11 needs the Arty build report. LiteX simulations 4/4 |

`physical-gptp` is not replayed: it runs only on schedule or dispatch and is skipped on a pull request, as on the hosted run.

What could not run here exactly as written, and what stood in for it (each step is marked in its receipt):

- **Runner provisioning** (`sudo apt-get`, `/opt`, `/usr/local/bin`): `librsvg2-bin` and `tclsh` are present here. sv2v is the workflow's pinned v0.0.12 zip, its digest checked, installed into the replay's own bin directory. Verilator is a local 5.050 install mapped at `/opt/verilator`. Yosys is this host's 0.66 package, with external ABC; the tag build bundles ABC. The build-from-source steps skip as on a cache hit.
- **Caches**: the Verilator and Yosys builds count as hits. The pip, Scala, CPU-metadata and RV32 SDK caches start cold in a scratch HOME, so the SDK is the pinned Bootlin archive, freshly downloaded and verified. The Yosys result cache is cold, so every top runs live.
- **Checkout**: the head itself. Live `dev` is still `cdf49d1a`, so the PR merge tree the hosted run checks out is the head's tree.
- **`docs-check-no-git`** runs in a `git archive` export of the head (no `.git`), not by deleting the worktree's metadata.
- **"Assert the repository default branch is dev"** reads `unreadable` without credentials in the scratch HOME. That is informational on a pull_request event, as the step itself prints.
- **`scripts/act_ci.py --selftest`** (`docs-check` step 43) is NOT RUN on this host. AGENTS.md section 5 lets the candidate's runner self-test only inside the disposable CI job. The file is byte-identical to live `dev` `cdf49d1a`. The first replay attempt did run it on the host (rc 0, 3.3 s, offline); the receipt says so.

## Authoritative references

- `docs/design/MEDIA_CLOCK_FOLLOWING.md` and its rulings on #629
- `docs/reference/FR_NFR.md` FR-CLK-03, FR-CLK-04
- IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.5, 4.4.4.6, 4.4.4.7, 7.2.4, 7.3.3, 7.3.5, 10.8
- IEEE 1722.1-2021 6.2.2.8, 7.2.9, 7.2.32, Table 7-16, Table 7-141, 7.4.23.1
- Milan v1.2 5.3.3.6, 5.3.11.1, 6.2, 7.2.2, 7.3.2, 7.4
- `tb/verilator/nvm_capture_cpu/README.md` (the capture measurement's recipe) and `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18
- protocol-processor #141 (no processor RTL change)

## How to get into the same state

```sh
git fetch origin
git switch 629-media-clock-impl
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
make -C tb/verilator/aaf_clock_meter        # meter rows, servo with the meter, 35 mutants
make -C tb/verilator/milan_dp_mclk          # root rows (legs A, B, C) and 16 mutants
MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk   # the same under an inherited print-directory flag
make -C tb/verilator/milan_dp               # [CLKSRC-WALK], A2-a pins, T67
make -C tb/verilator/csr
python3 scripts/check_nvm_capture.py
python3 scripts/measure_naming.py --check
python3 scripts/check_port_contracts.py
python3 sw/builder/test_builder.py
python3 scripts/check_entity_shape.py --self-test   # as docs-check runs it; also with GNU make 4.3 first on PATH
scripts/run_all_suites.sh <outdir> --shard I/5   # I = 0 .. 4
TAG=<tag> sw/litex/build.sh ax7101          # the shipping image
```

Expected result / pass criteria: every suite and gate exits 0, under the
hosted runner's GNU make 4.3 and under a newer make; each mutant runner reports
every named mutant caught; the AX7101 image meets timing with no CRITICAL
WARNING and no #607 constraint refusal. Measured at this head: 59 of 59 suites pass across the five shards, replayed under GNU make 4.3 (2,149,266 checks);
the root suite 31/31 and the meter suite 36/36 in their campaigns;
`check_entity_shape.py --self-test` 222/0 under make 4.3 and 4.4.1;
`check_nvm_capture.py` rc 0 with the 8x8 capture maximum at 13.86484 ms of
24.5 ms. The image (unchanged RTL since round 2): WNS +0.065 ns, WHS +0.036 ns,
0 critical warnings, slices 99.90 %.

## Known limitations / out of scope

- VERSION stays `0x0002_0060`, as for #443's `RENDER_STAT`. Kept by the ruling
  on #629 (comment 5946491571).
- Design statements that did not hold as written, each accepted by that ruling
  with what was done: the listener-only builder shape cannot be built (graded
  at the overlay); the AECP walk cannot see the servo leave IDLE without a
  locked reference (graded at the decode, the servo's select and the meter's
  status word); the root counter row's loss leg is 3 s, not 60 s (suite
  guard); the root counter row needs a `tu` test double in that suite; one
  #386 recentre per switch is graded over 0.8 s gaps; the servo-with-meter row
  lives in the meter suite; the meter's FF count (636) is over the 270 to 420
  estimate. Round 2 adds one placement: the design's "`tu` taken from the
  `tv` net" mutant is planted at the root (the meter takes `tu` as a port).
- Retained suggestion (R432-1 S1 = R433-1 S1): the #386 settle band stays keyed
  on `follow_sel_r`, as the merged design's settle table and TIME_SYNC ("at
  INTERNAL: 2048 ticks after the change") state. Keying it on `mga_sel_w` is a
  behavioural design change that needs its own decision and re-validation (the
  render and `milan_dp` pins, the image); render T30/T31 count no skip or
  underrun at INTERNAL.
- Retained suggestion (R433-1 S2, render T30 only): T30's INTERNAL window is the
  aligner's pull-in after T14's hold, so a bound near zero would grade a
  transient; the settled two-sided bound is T31's |walk| < 5 ppm.
- KNOWN RISK: at INTERNAL the media clock is the MMCM plan; Milan v1.2 7.4's
  +/-50 ppm holds only for a board-oscillator grade of +/-39 ppm or better
  (assumed adequate by owner decision, unconfirmed).
- Slice occupancy of the shipping image is 99.90 % (round 1: 99.98 %), recorded as a headroom note by the ruling.
- Phase alignment of the outputs to the followed stream (IEEE 1722-2016 10.8,
  4.3.5) is #632; the CRF receiver's own rate weakness is #633.
- The bench acceptance (THD+N, following AAF and CRF, through a switch) is a
  later bench lane.
- The capture timing is a simulation measurement (`tb/verilator/nvm_capture_cpu`);
  physical capture timing stays unmeasured (saved-state UNRESOLVED 6).
- Outside #629, for the manager to file if wanted (round 3): the entity shape
  gate's database read (`shape_prereqs_from_database`) counts a make database
  as readable when the parse stopped at an `$(error)`. Under GNU make 4.4+ that
  is what `make -pqrR` does to `tb/verilator/milan_dp_render/Makefile`: its
  nested `$(shell $(MAKE) ...)` inherits the question flag, so its rule lines
  go unread (its only frozen shape token under make 4.3 is arm D's
  `configs/generated` copy, so nothing is lost today). Under the hosted make
  4.3 it parses in full. This PR fixes the pattern only in its own root suite;
  failing closed on a stopped parse would first need `milan_dp_render` to take
  the same `MAKEFLAGS=`. Round 2's note on `milan_dp_render` and
  `pp_shadow` (no `--no-print-directory`) stands.

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
