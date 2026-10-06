[A531]

Public STOP: https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994628555

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

BLOCKED — stage-2d timing STOP on `645-ring-slip` -> `dev`.
Head: `b2c81239f686592b224510c9d4f196a6c7aa7f25`.
All functional acceptance commands pass, including physical/accounting/control
197/0. ExtraTimingOpt slow WNS +0.001 ns misses the required +0.030 ns margin;
the ruling requires STOP. This is a prepared PR body, not a published PR.

## Linked Issue / roles

Closes #645
Closes #647

These closure lines cover the implementation; their bench items remain
with the manager and are not discharged by simulation.

Executor: [A531]
Internal cleared-context reviewer: [R474]
External reviewer: [R475]

## Description

A source lock can leave the listener loopback queue close to empty after
the frequency pull-in, causing a later frame slip. An INTERNAL aligner
pull-in can leave a running render stream with a persistent latency shift.
The lane retains the existing at-switch render recentre and adds one
settle recentre to both rings. The loopback depth is sixteen and the
class-A PDU-end target is eleven events.

Stage 2d merges dev `fa450d30` without fast-forward, including the corrected
physical peer pacing. Documentation now states the startup/reset
recentre bound and the steady-state scope of the zero-glitch run.
The physical ordering checker now grades only the declared decision PDU.
Both new controls pass 14 checks with zero failures. The physical leg passes 143 checks and accounting passes 40; including the
14 new control checks, the suite is 197 checks with zero failures.

## Authoritative references

- [Stage-2d ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410)
- [Queue and arrival-envelope ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987852678)
- [Option C ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394)
- REQUIREMENTS.md; docs/design/MEDIA_CLOCK_FOLLOWING.md;
  docs/design/TIME_SYNC.md; docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md.

## How to get into the same state

```sh
git switch 645-ring-slip
git rev-parse HEAD
git log -3 --format='%H %P %s'
```

Expected head `b2c81239f686592b224510c9d4f196a6c7aa7f25`, descending from the required
merge `be3ec6e57a9b22c76daef817c07cae5ade8ca012`.
Processor pin `631eeb342ca1e3fa80e734077a56a943aee76ff1`.
Before any submodule Git command, verify its top-level directory.
Use the pinned simulator and the build recipe's pinned dependencies.

## How to validate

Use the external staging roots described in HANDOFF.md so generated files stay
outside the source tree. Exact argv, dependency setup and source hashes are in
stage2d/. The main integration commands are:

```sh
make -j16 -C "$BROAD/tb/verilator/milan_dp" VERILATOR_JOBS=2 SIM_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_render" VERILATOR_JOBS=2
make -j16 -C "$BROAD/tb/verilator/milan_dp_mclk" VERILATOR_JOBS=2
make -j16 -C "$PHYSICAL/tb/verilator/milan_dp_gptp" VERILATOR_JOBS=4
python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration
bash syn/yosys/run.sh
```

Current merged-head evidence, all rc 0:

- Physical and accounting acceptance: 143 + 40 + 14 = 197 checks, zero failures;
  both startup/reset declared steps match the wire and both counters stay zero.
- Four unchanged arrival campaigns: sixteen phases and 48 decisions each;
  zero post-decision slips, minimum wide-envelope margins 2.565120 empty
  and 2.234880 full ticks.
- INTERNAL: 32 cases, zero post-settle slips; ungradable render windows
  remain explicitly ungraded. All five unchanged controls are caught.
- Capture-map: 408 RTL and 20 synthesized-netlist checks, zero failures.
- Aligner: 45 checks and three caught controls.
- 26 source/documentation gates and the vendor parser pass at the committed harness head.
- Fresh routed own-area bound: 113 LUT / 73 FF, below 120/120; unchanged
  shared functions excluded only after exhaustive equivalence and a caught control.
- ExtraPostPlacementOpt timing: slow WNS +0.120 ns / WHS +0.053 ns;
  fast WNS +1.633 ns / WHS +0.019 ns. All TNS/THS zero.

All three required timing directives completed under the shared lock:

| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Required margin |
|---|---:|---:|---|
| ExtraPostPlacementOpt | +0.120 / +0.053 | +1.633 / +0.019 | PASS |
| AltSpreadLogic_high | +0.142 / +0.065 | +1.483 / +0.026 | PASS |
| ExtraTimingOpt | +0.001 / +0.001 | +1.476 / +0.012 | **FAIL** |

Each fixed timing model was reported at 0 and 85 C, with identical figures at
both power temperatures. All TNS/THS are zero. All runs return 0; ExtraTimingOpt's
required margin grade returns 1. No critical warning or rejected implementation
constraint appears. The failed setup path lies in the processor receive-validator
to transmit-arbiter logic; its location does not waive the bar.

The boundary campaign passes 81/81 checks over 564 windows, with both planted
setpoint controls caught and the nine-cycle ambiguity unchanged. Its 195
NOT GRADABLE windows earn no law credit. The full datapath default passes
11,877 checks. Render, media-clock, processor-shadow and changed units pass;
portability passes 55/55 tops. The builder returns 0 with required elaboration;
one historical Arty area-calibration arm is NOT RUN because its reference report
is absent. The 18-phase render pull-in campaign passes with zero slips; one
render phase is explicitly ungradable.

HANDOFF.md and stage2d/ contain exact commands, results and artifact receipts.
All 134 implementation inputs match at the final head; temporary image links
are removed and the worktree and pinned submodules are clean. Historical
stage-2c results are labeled separately from current-head acceptance.

## Known limitations / out of scope

- No hardware, flashing, physical calibration or bench acceptance.
- No DUT change in stage 2d. A stale capture-module summary at line 360 still
  says depth eight; its detailed contract, constant, tests and design doc say
  sixteen. This documentation inconsistency is recorded for review.
- The four historical render-campaign failures are assigned to #657.
- Timing requires WNS >= +0.030 ns and WHS >= 0 at both fixed corners.
  ExtraTimingOpt misses the setup-margin bar; work stops pending a ruling.
  No recovery change or reroute was attempted.
- No independent review or hosted evidence is claimed.

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
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
