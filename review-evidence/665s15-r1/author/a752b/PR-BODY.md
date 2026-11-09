[A752b]

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

GREEN locally, review ready: every gate rc 0 on clean clones of the head (136 workflow steps run, 221 not runnable here, each with a reason; the full sweep, 65 of 65 suites; the harness at 1x1/1if, 8x8/2if and 32x32/2if) — `665-s15-32x32` -> `dev-soft-core`, head `5e6c3f62dc19b44b93133cb708920f33aa3044ef`.

## Linked Issue / roles

Relates to #665
Relates to #859

#859 is not closed by this PR: item 5's per-item costs (`item.*` in S2b round 22's projection) are graded by S2b's own head's poll grader, which this base does not carry, so they are listed unmeasured with that reason (see Known limitations).

Executor: `[A752b]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Round 2 of the 32x32 shape (#859, part of #665's Mark II split), under the round 2 ruling on #859 (items 1 to 5): a 32x32 shape on two AVB interfaces, built for simulation only and without saved state, run through S2's CPU budget harness.

| Item | What this PR does |
|---|---|
| 1. Without saved state | `configs/endstation_ax7101_32x32.yaml` declares `simulation_only: true` and `saved_state: none`. The end-station builder refuses `saved_state: none` on any shape that does not declare `simulation_only`, and refuses the simulation shape every routed output (`--write-rtl`, `--write-fragment`, `srp.rtl_table`); its argv carries `--simulation-only`, with which `milan_soc.py` refuses `--build` and `--load`. The firmware links no store, no flash port and no record space (`CTRL_SAVED_STATE_NONE`). The harness reports each save group by name as owed to #823 and grades none; `nvm_split_target --point 32x32` lists them and exits 1. No saved-state format change was needed |
| 2. Contract variant layout | `gen_mailbox.py --variant-interfaces 2 --variant-shape CONFIG` lays the contract out from the shape's per-interface streams, each interface's own by ordinal (17 on the primary, with both CRF streams). The tracked 2.4 outputs are byte-identical. A layout one sink entry short is refused by the generator's self-test and by the firmware's link, each with its words. No major contract version |
| 3. Datapath guards | The five guards are recorded in the census as owed to #640, each with the guard behind it |
| 4. Lifted by a rule | ACMP at 33 sinks and sources through `ACMP_MAX_SINKS` and `ACMP_MAX_SOURCES` from the generated counts; the SRP pool from its formula (144,832 B); a simulation-only memory map in `ctrl_memory.py` (`rom` 256 KiB, `sram` 512 KiB), the shipped map unchanged and every byte over the 56-RAMB36 budget ledgered to #640; each ring and bucket derived at the shape with its clause (census section 5) |
| 5. Run the point | `ctrl_service_budget/run.py --point 32x32`: every non-save group graded; T_svc misses recorded, not graded, beside 1x1/1if and 8x8/2if; measured costs beside S2b round 22's projection with the error |

The 1x1 and 8x8 shapes are unchanged: their generated outputs match a pinned golden equal to the base generators' digests (gate 40), their firmware images link to the base's bytes, and their harness scripts are byte-identical to the base's.

Two harness timing rules scale with a point's streams over the 8x8 shape's 18, rounded up (4 at 32x32, 1 at 1x1 and 8x8). The first is every bounded wait's `within`. The second is the owed row's settle before its composed window, whose defined load needs an empty event ring at the window's first instant. Neither changes a grade, a ceiling or a defined load. At 32x32 with the 8x8 timing, a GET_TX_STATE answered 54.5 ms after its command, past its 20 ms wait, and the owed row's held-response pass ran 65.1 ms, so two of its fifteen grandmaster changes did not fit the ring.

New checks, each with a plant that must fail it: gate 39 (the option and the routed outputs) and gate 40 (the pinned shapes' outputs) in `test_builder.py`; `test_soc_options.py`'s route refusal; two `gen_mailbox.py --selftest` arms; `test_ctrl_memory.py`'s simulation-map arm; six harness self-test checks in `selftest_shape.py`. The firmware boundary lists `test_builder.py` among the programs that compile none of the firmware's control-stack source, because gate 40 runs the three entity-header generators.

The new gate 40's number is already used: the base's builder gate 40 is `sw/builder/test_declarations.py`'s declaration contracts (#400, #403), printed in the same run. Nothing depends on the label. The fix is to relabel the new gate 41 (in `test_builder.py`, the golden's `_what` through `--write-shape-golden`, `ctrl_configs.py` and `check_py_idiom.py`'s inventory reason). It was found after the head's gates had run and is to land with the first review round's fixes.

Results at the head, each on a clean clone:

| Point | Groups graded | Refusals | T_svc misses (probe instances; paths) | Save groups |
|---|---:|---:|---|---|
| 1x1/1if | 18 | 0 | 34 of 141; 13 of 81 | run |
| 8x8/2if | 17 | 0 | 57 of 182; 29 of 129 | run |
| 32x32/2if | 17 | 0 | 89 of 182; 55 of 129 | 10 owed to #823, by name |

Misses are recorded, not graded. The 32x32/2if leg built in 16.3 s (358,732 kB peak process) and ran in 52 min 14 s (52,076 kB peak process; 1.3 GB for its whole unit).

Measured costs at 32x32/2if beside S2b round 22's projection (the most measured plus 5 %, rounded up to 5 us; error is projected less measured):

| Cost | S2b projected, us | measured, us | error, us |
|---|---:|---:|---:|
| `record.srp` | 892.1 | 1085 | -192.9 |
| `record.aecp` | 443.6 | 2245 | -1801.4 |
| `record.acmp` | 944.3 | 2505 | -1560.7 |
| `record.adp` | 658.6 | 1955 | -1296.4 |
| `record.maap` | 245.0 | 615 | -370.0 |
| `centisecond` | 1315.7 | 1470 | -154.3 |
| `rebuild` | 2061.4 | 7240 | -5178.6 |

S2b's line through 1x1/1if and 8x8/2if under-projects every cost measured the same way. The same line through this base's own two points comes within 75 us on SRP, ADP and MAAP. It misses `record.aecp` and `centisecond` high by about 1.1 ms and `rebuild` low by 1.5 ms, so those three do not grow linearly in streams.

Findings, each needing its own issue:

- AECP's face model names one AVB_INTERFACE and places every stream on interface 0, while ACMP, MAAP and SRP place stream n on n mod 2; in the shape's layout the face follows the split's placement (`MBX_STREAM_HOME`). A second AVB_INTERFACE is #394's.
- SRP's participant on each interface declares every source of the entity; in the shape's layout each interface publishes its own sources' bits.
- tsn-c-stack's owed-release mask is 32 bits (`third_party/tsn-c-stack/include/acmp.h:400`, `src/acmp.c:816` and `:871`): at 33 sinks the CRF sink's bit aliases sink 0's, so that sink's change notice is not held behind its owed response (#653). A donor patch for the stack is drafted, not part of this PR; the lane builds the pinned stack.
- ACMP's receive ring holds 12 of its bucket's 16 records and MAAP's 7 of 8 at every shape; at 32x32 ACMP's transmit side holds 20 of a possible 33 probe commands in one pass.
- At 32x32/2if no two consecutive passes are idle (each tick's pass writes the mailbox), so each `wait quiet 3` of the scripts ends at its bound.
- `docs/diagrams/nxn_window_map.gen.py` fails at the base and no gate runs it.

Assumption: the tracked contract holds stream n at entry n of every interface's tables (`sw/mailbox/mailbox.yaml:338-339`), and today's two-interface variant keeps that. The ruling's per-interface ordinals are used by the shape's layout alone (`MBX_ENTRY_ORDINAL`). Whether the 8x8 two-interface variant should move to ordinals is not decided here.

## Authoritative references

- #859: the round 2 ruling (issuecomment-6727773362, items 1 to 5) and the assignment (issuecomment-6723527155).
- [32x32 shape census](docs/design/SHAPE_32X32_CENSUS.md), sections 4 and 5.
- The mailbox contract `sw/mailbox/mailbox.yaml` and [the split mailbox](docs/design/MAILBOX_SPLIT.md).
- [Split control memory](docs/design/SPLIT_CONTROL_MEMORY.md), sections 3 and 8.
- [The CPU budget harness](tb/verilator/ctrl_service_budget/README.md) and FR_NFR.md 3.4.1 (T_svc).
- Milan v1.2 Tables 4.3, 5.26 and 5.50 and 5.4.5.3; IEEE 1722.1-2021 6.2.2.5 and Figure 6-1; IEEE 1722-2016 B.3.4 and Table B.8; IEEE 802.1Q-2018 10.7.4.1 and Table 10-7, for the rings and buckets.
- #823 (the record space at the shape), #640 (the datapath at the shape and the 56-RAMB36 budget), #810 (S2b, which grades the rows), #394 (redundancy and a second AVB_INTERFACE), #653 (the owed-response hold).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s15-32x32
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness needs the [capture prerequisites](tb/verilator/nvm_capture_cpu/README.md#run): the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_32x32.yaml -o /tmp/shape32
python3 sw/builder/test_builder.py --gates test_simulation_shape_option,test_shipped_shape_outputs_unchanged
python3 sw/builder/test_soc_options.py
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/build.py /tmp/budget-32x32 endstation_ax7101_32x32 2
python3 -B tb/verilator/ctrl_service_budget/run.py --point 32x32 --build-dir /tmp/budget-32x32 --reuse-build --record-budget-findings
python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir /tmp/nvm-target-32x32
```

Expected result / pass criteria: every command exits 0 except the last. The builder writes the 32x32 shape's outputs and no routed output. Its report lists the board's sweep fragment path, as every build's report does, but the fragment is written only with `--write-fragment`, which the shape refuses; the tree stays clean. The `test_builder.py` subset prints "ALL GATES PASS" for its 2 of 107 gates, each with its plant turned red. `test_soc_options.py` and `test_ctrl_memory.py` print "RESULT: PASS". `gen_mailbox.py --selftest` prints "selftest: 0 arm(s) failed". The harness self-test prints "self-test: 0 failures". The 32x32 run ends "17 groups graded, 0 refusals, 89 T_svc misses (89 of 182 probe instances, 55 of 129 paths), 10 save groups owed to #823". The last command lists the 10 save groups owed to #823 and exits 1, building nothing.

The full local bar (every `run:` step of the four workflows a pull request to `dev-soft-core` triggers, the full sweep in four shards, the firmware self-test and every mutant driver, `fw_coverage.py --check`, `test_builder.py --require-rv32`, `cd tests && behave`, `git diff --check` against the merge base) passed at the head.

## Known limitations / out of scope

- The shape is for simulation only: no route, no bitstream, no flash. The image build refuses to route or load it.
- The record space at 32x32 is #823's: no save group runs at the shape, and each is reported by name as owed to #823.
- The datapath at 32x32 and the 56-RAMB36 budget are #640's: the five guards and every byte over budget are recorded as owed to #640.
- S2b round 22's `events`, `events_none`, `polls_least`, `base`, `event.*` and `item.*` costs are not measured here. The first three cut a pass at `ctrl_loop`'s `service_rx`, which this base's image inlines; the rest are graded by S2b round 22's own head's event and poll graders, which this base does not carry. The costs this base measures the same way (`record.*`, `rebuild`, `centisecond`) are compared, with the error.
- The tsn-c-stack mask fix is a donor patch for the stack, not part of this PR.
- The branch is on `dev-soft-core` `a9d69c77`, which has since moved. A merge with today's tip has one textual conflict, in `sw/builder/endstation_builder.py` `emit_soc_argv`: this branch's `--simulation-only` arm and the tip's split-placement arm are both appended after `--cpu-count`, as independent conditionals. The candidate merge result is not validated here.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
