[A516]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- Each R446-1 and R447-1 finding, what answers it and the evidence.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY, round 2: 43/43 touched local gates rc 0 under GNU Make 4.3; gate self-test 113 arms, 84/84 shipped mutants killed by a named arm; both reviewers' mutant probes rerun unchanged, 23/23 and 18/18 killed -- `234-area-baseline` -> `dev`. Head `0feff20fa228d0cb91d507943e6d39495b28b880` (three commits on round 1's `2a765a6c`). No RTL, processor or interface change; no Vivado run in round 2.

## Linked Issue / roles

Relates to #234
Relates to #229

Executor: `[A516]`
Internal cleared-context reviewer: `[R446]`
External reviewer: `[R447]`

## Description

Issue #234's first step under epic #229: the authoritative baseline, the 1x1 ranking, the budget and a resource-regression gate.

| Piece | Change |
|---|---|
| `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` | New. Vivado baseline of the current head (A: dev `1269cdaf`, processor `631eeb34`) and of the next adoption (B: processor `ddb3119d` with the C8 and P2 parent patches, a scratch tree). Integrated 1x1 route, standalone 1x1 and 8x8 synthesis at the build's 50 MHz clock, per-sub-block LUT/FF/RAMB/DSP/CARRY4, storage mapping with source lines, Yosys reconciliation, the 1x1 reduction ranking and run receipts. Round 2: B's standalone movement on one named partition, A's route status recorded as clean, the lever issues #230 and #639. |
| `docs/design/AREA_BUDGET.md` | New section: NFR-RES-01's 60 % LUT target against the measured image, the owner's 2026-10-03 decision, the gate's policy table and where it runs. Contents separator switched to `--` (CONTRIBUTING 6.1). |
| `syn/ooc/pp_resource_gate.py`, `_selftest.py`, `_mutants.py` | New gate. Reads one recipe measurement directory into a record (identity, input digest, figures, sub-blocks) and judges it against the recorded baseline. Exit 0 within tolerance; 1 a material regression, an incomplete route included; 2 not comparable, an unreadable measurement or an unusable baseline, always with its reason and never through a traceback. `check-baseline` holds every endpoint's policy to the budget's policy table. 113 planted arms; 84 enforcement-removal mutants, each killed by a named arm. |
| `syn/ooc/pp_resource_baseline.json` | New. A's three endpoints (`route-1x1`, `ooc-1x1`, `ooc-8x8`), written only by `record --write`, plus policy (tolerances about 1 %, zero for RAMB/DSP, WNS at least +0.030 ns and WHS at least 0, 121.5-tile BRAM ceiling). Unchanged in round 2. |
| `syn/ooc/pp_baseline.py`, `pp_baseline_mutants.py` | `--integrated-clock`: the standalone clock from the bound `CLK_HZ_P` instead of the fixed 10 ns (default unchanged); one self-test function and four killed mutants. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` | The new flag, the elaboration route to 8x8 parameters, and the gate commands and exit-code contract. |
| `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py` | The gate's self-test, mutants and `check-baseline` join the existing OOC step; the pinned step list moves with them. No new job, runner or tool. |
| `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` | Round 2: the gate now reads `docs/design/AREA_BUDGET.md`, so the classifier files it as gate-read (its self-test derives that list and refused the change until it was added). A change to the budget page alone runs the step that checks it. |
| `docs/findings/README.md` | Round 2: indexes `234_PP_SHADOW_AREA_BASELINE.md` and `PP_SHADOW_BASELINE.md`. |

Headline figures (A / B):

| Measurement (A / B) | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Shipping route, whole image | 50,128 / 50,753 | 59,006 / 59,014 | 15,815 / 15,827 | 79 / 27 both | 14 | 3,405 / 3,423 | +0.063 / +0.036; +0.101 / +0.036 |
| Standalone wrapper 1x1, 20 ns | 24,343 / 24,505 | 25,344 / 25,470 | - | 21 / 3 both | 8 | 1,623 / 1,638 | estimate only |
| Standalone wrapper 8x8, 20 ns | 31,562 / 31,390 | 33,929 / 33,844 | - | 26 / 5 both | 8 | 2,001 / 2,016 | estimate only |

The image uses 79.07 % of the LUTs and 99.78 % of the slices (35 free). Two buffers still spill into flops at 1x1: the notification registry (2,048 FF, against its own distributed-RAM attribute) and the SRP timer-arm FIFOs (2,304 FF). Ranked levers (registry, SRP FIFOs, timer-arm queues, #230 sharing, throttle stamps) estimate about 5,600 FF and 3,600 LUT; #233 is not needed for placement headroom.

Gate on real data at this head: A's three endpoints exit 0, and A's route status reads complete (105,566 of 105,566 routable nets fully routed, 0 nets with routing errors). B exits 1 on the route (+625 LUT over the 500-LUT tolerance; 366 of them outside the wrapper, where no RTL changed; its route status is complete too) and 0 on both standalone endpoints (+162 / -172 LUT). A's 1x1 control at 10 ns exits 2 (standalone clock identity).

Decisions (manager rulings 5967852698 and the owner decision 5967924270 on #234):

1. NFR-RES-01 (at most 60 % LUT) is 12,088 LUT short at dev; #229's 30 % non-CPU milestone is exceeded by the wrapper alone. The 121.5-tile ceiling and the gate tolerances are accepted as working policy (manager ruling). The allocation went to the owner, who ruled on 2026-10-03: NFR-RES-01 stays at 60 %, met by a redesign in milestone "Optimisations Mark II" (#640) after Instrument verification; until then the gate holds every resource at its recorded value.
2. Criterion 1 is judged at the declared 50 MHz shipping clock and is met (manager ruling).
3. The Vivado half of the gate runs in the manager's merge bank for every PR that changes RTL, the processor pin or the build recipe (manager ruling).
4. The next adoption needs a reviewed re-baseline of the route, and two `syn/yosys/rom_digests.tsv` rows for `ddb3119d` that its patches do not carry.
5. The child issues are #232 (levers 1 and 5), #230 (levers 4 and 2) and #639 (levers 3 and 6), in that order (manager ruling).

## Round 2

The round answers R446-1 and R447-1 on PR #638, both NEGATIVE on MINOR findings only, under the round-2 assignment on #234 (5968015720). Commits: `9b1d3537` (the gate, its self-test, mutants, recipe and policy table; the classifier) `5c92caca` (the partition, the rulings, the owner decision, the findings index) and `0feff20f` (two findings sentences: the gate reads each route status report at every check rather than storing it). Every probe below is the reviewer's published script from the review evidence branch, rerun unchanged at this head unless marked adapted.

| Finding | Severity, lens | Answer | Evidence at this head |
|---|---|---|---|
| R446-1 F1: a non-finite slack passes the timing floor | MINOR Conformance, Robustness, Tests | `timing()` refuses, with exit 2 and a named reason, a slack that is `inf` or `nan` and a summary whose TNS or THS total endpoints are absent or zero. Arms: WNS `nan`; WNS and WHS `inf`; zero timed endpoints. Mutants `finite slack` and `timed endpoints` killed. | `probe_gate_cli.py`: WNS `nan` rc 2; `inf` with 0 endpoints rc 2. That line prints BAD because the probe's literal expectation is 1; F1 accepts 2 and the assignment requires 2. The other 116 of 117 cases are as expected. |
| R446-1 F2: claimed refusals without an arm | MINOR Tests | Arms for the design, the design state and each of the eight `FLOW` commands; standalone RAMB36 and DSP growth; WNS and WHS at their floors; a fall of exactly the tolerance; BRAM tiles at the ceiling. Each has a shipped mutant. | `probe_gate_mutants.py`: 23 of 23 killed, control passes. |
| R446-1 F3: "net 101 LUTs and 95 FFs" mixes partitions | MINOR Docs | Both pages name one partition: the own logic of every instance the gate record lists outside `u_nvm_port`, 51 terms. Net +79 LUTs and +93 FFs; absolute 391 LUTs and 121 FFs. The processor top's own logic is stated as one of the terms: -23 LUTs, +107 FFs, its `armq_r` timer-arm queues (1,153 to 1,260 flops). | `reconcile.py` unchanged: 2 mismatches, both its hard-coded round-1 sentences; the second asserts +95 FF on a partition whose records give -12, so no prose can satisfy it. Adapted copy (diff published; only those two checks re-pointed at the round-2 sentences): 0 mismatches. |
| R446-1 R1 to R3 | RESIDUE Docs | Taken. R1 and R2 cover the same `AREA_BUDGET.md` lines as R447-1's first RESIDUE in slightly different words; R447-1's line-by-line wording is used and carries all of R446-1's content. R3 taken exactly. | `AREA_BUDGET.md` headroom table and "Where the gate runs"; findings ranking table. |
| R446-1 R4 | RESIDUE Docs | Taken in this body: decisions 1 to 5 above. | This body. |
| R446-1 S1 to S5 | SUGGESTION | All taken: one exit-code contract (S1, item 2); `check-baseline` requires the route ceiling and equals the budget table (S2, item 5); "re-baseline recommended" (S3, item 6; the policy stays growth-only); the findings index (S4); arms for header uniqueness, a single generated top and the decimal count format (S5). | Self-test and mutant campaign. |
| R447-1 MINOR 1: malformed baseline entries exit 1 by traceback | MINOR Robustness, Tests | A missing, non-JSON or endpoint-less baseline, an endpoint without a complete record, a gated figure without a tolerance, a ceiling naming no figure and a wrong-shape image manifest each exit 2 with a named reason. `check-baseline` lists a missing record and an unknown ceiling figure as problems. 13 `check` and 20 `check-baseline` arms run through `main()`. | `probe_cli.py`: 54 of 54 as documented. |
| R447-1 MINOR 2: the self-test misses disabled checks | MINOR Tests | Arms and mutants for standalone RAMB36 and DSP gating, the refusal exit status, the kind read from the directory and the ceiling, floor and fall boundaries. | `extra_mutants.py`: 18 of 18 killed, control passes. |
| R447-1 MINOR 3: the route endpoint never reads routing completion | MINOR Robustness | The route endpoint reads the run's one `*_route_status.rpt`. Unrouted nets, routing errors or routable nets not fully routed exit 1; a missing, duplicated or unreadable report exits 2. Nine route arms and two command-line arms; A's real route status reads complete. | `probe_route_status.py`: clean exit 0, 37 unrouted nets exit 1. |
| R447-1 MINOR 4: the movement figures mix partitions | MINOR Docs | As R446-1 F3. | `partition_check.py`: its complete-partition line (+79 LUT, 391 absolute, +93 FF) and its processor-top line (-23 LUT, +107 FF) equal the prose in both pages; a mechanical comparison reports 0 mismatches. |
| R447-1 RESIDUE 1 | RESIDUE Docs | Taken exactly. | `AREA_BUDGET.md`. |
| R447-1 RESIDUE 2 | RESIDUE Docs | Taken exactly for items 2 and 3 and the limitations bullet. Item 1 states the owner decision of 2026-10-03 instead of "the allocation needs the owner's ruling", which it postdates. | This body. |
| R447-1 suggestions 1 and 2 | SUGGESTION | Taken as items 5 and 4. | As above. |

Also from the assignment: `AREA_BUDGET.md` cites the owner decision where it said the allocation "needs an owner decision". `check-baseline` derives the policy comparison from the budget's table, which now holds one value per cell; no value changed, so the STOP on accepted values did not apply. Other probes rerun at this head: `check_tables.py` 49 groups, 0 mismatches; `replay_records.py` A 0, 0, 0, B 1, 0, 0, the 10 ns control 2; `probe_pr_mutant_reasons.py` 84 of 84 killed by an arm assertion, none by a crash.

## Authoritative references

- #234, its [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5966260488) and [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5968015720); the [manager rulings](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967852698) and the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270); #229 workstream 1; #230, #232, #233, #639, #640.
- NFR-RES-01, `docs/reference/FR_NFR.md`.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, `docs/findings/PP_SHADOW_BASELINE.md` (#231, #587).
- `docs/integration/BUILDING.md` section 5 (WNS at least +0.03 ns, WHS at least 0).
- `syn/yosys/README.md`, "The cells= record" (no checked-in Yosys cell baseline).
- `docs/testing/CI_WORKFLOWS.md`, the gate-read pages of the change classifier.

## How to get into the same state

```sh
git fetch origin 234-area-baseline
git switch --detach 0feff20fa228d0cb91d507943e6d39495b28b880
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

The measurements follow `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` with Vivado 2026.1 build 6511674; B additionally needs the processor at `ddb3119d` and the two parent-adoption patches applied in a scratch tree.

## How to validate

```sh
python3 syn/ooc/pp_resource_gate.py --selftest
python3 syn/ooc/pp_resource_gate_mutants.py
python3 syn/ooc/pp_resource_gate.py check-baseline
python3 syn/ooc/pp_baseline.py --selftest
python3 syn/ooc/pp_baseline_mutants.py
python3 scripts/ci_scope.py --selftest
python3 scripts/ci_events.py --check
```

Expected result / pass criteria: every command exits 0; the gate self-test reports 113 arms, the mutant campaigns report every mutant failing and the control passing, and `check-baseline` reports 3 endpoints. With Vivado, `pp_resource_gate.py check <dir> --endpoint route-1x1|ooc-1x1|ooc-8x8` on a fresh measurement of this head exits 0, and the route prints "route status: complete".

## Known limitations / out of scope

- No RTL change: every ranked lever is a processor change for its own lane (STOP rule of the assignment).
- The Vivado half of the gate runs in the manager's merge bank for every PR that changes RTL, the processor pin or the build recipe (manager ruling).
- No Yosys-based hosted ratchet is proposed: the Yosys gate's documentation records a deliberate decision against a checked-in cell baseline, Yosys does not predict Vivado and has no timing, and the hosted Yosys top is the 8-stream default, not the shipping shape.
- Savings in the ranking are estimates; only matched before-and-after routes measure them, and no slice saving is claimed.
- B was measured from a scratch tree; its ROM digest rows for `ddb3119d` were recorded only there.
- The raw Vivado reports stay in the scratch run directories; their SHA-256 values are in the run receipts.
- `scripts/act_ci.py --selftest` is not in the local gate table: AGENTS.md section 5 lets the candidate's copy run it only inside the disposable CI job boundary. Round 1's table ran it on the host; round 2 does not. This PR does not change `scripts/act_ci.py`.
- No bitstream, hardware, flashing or bench result.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
