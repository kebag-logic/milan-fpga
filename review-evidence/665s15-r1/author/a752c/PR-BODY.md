[A752c]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Sync with dev-soft-core 1d6bf555](#sync-with-dev-soft-core-1d6bf555)** — The merge, its two conflicts and what shows the shipped shapes unaffected.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally, review ready: every gate rc 0 on clean clones of the head — `665-s15-32x32` -> `dev-soft-core`, head `7aa6ef0c0312818fc8da36d39bbc468f54ac265b`.

- Workflows: 139 steps run, 226 not runnable here, each with a reason.
- The full sweep: 65 of 65 suites, 2,192,899 checks, 0 failures. Shard 2's first run stopped one suite at its wall clock, with none failed, so that shard was re-run alone with the timeout unchanged and ended rc 0. Both results are recorded.
- The harness at 1x1/1if, 8x8/2if and 32x32/2if.
- S6b's twin.

## Linked Issue / roles

Relates to #665
Relates to #859

#859 is not closed by this PR: item 5's per-item costs (`item.*` in S2b round 22's projection) are graded by S2b's own head's poll grader, which this base does not carry, so they are listed unmeasured with that reason (see Known limitations).

Executor: `[A752c]` (rounds 1 and 2: `[A752]`, `[A752b]`)
Internal cleared-context reviewer: `[R807]`
External reviewer: `[R808]`

## Description

The 32x32 shape (#859, part of #665's Mark II split), under the round 2 ruling on #859 (items 1 to 5): a 32x32 shape on two AVB interfaces, built for simulation only and without saved state, run through S2's CPU budget harness.

| Item | What this PR does |
|---|---|
| 1. Without saved state | `configs/endstation_ax7101_32x32.yaml` declares `simulation_only: true` and `saved_state: none`. The end-station builder refuses `saved_state: none` on any shape that does not declare `simulation_only`, and refuses the simulation shape every routed output (`--write-rtl`, `--write-fragment`, `srp.rtl_table`); its argv carries `--simulation-only`, with which `milan_soc.py` refuses `--build` and `--load`. The firmware links no store, no flash port and no record space (`CTRL_SAVED_STATE_NONE`). The harness reports each save group by name as owed to #823 and grades none; `nvm_split_target --point 32x32` lists them and exits 1. No saved-state format change was needed |
| 2. Contract variant layout | `gen_mailbox.py --variant-interfaces 2 --variant-shape CONFIG` lays the contract out from the shape's per-interface streams, each interface's own by ordinal (17 on the primary, with both CRF streams). The tracked 2.4 outputs are byte-identical. A layout one sink entry short is refused by the generator's self-test and by the firmware's link, each with its words. No major contract version |
| 3. Datapath guards | The five guards are recorded in the census as owed to #640, each with the guard behind it |
| 4. Lifted by a rule | ACMP at 33 sinks and sources through `ACMP_MAX_SINKS` and `ACMP_MAX_SOURCES` from the generated counts; the SRP pool from its formula (144,832 B); a simulation-only memory map in `ctrl_memory.py` (`rom` 256 KiB, `sram` 512 KiB), the shipped map unchanged and every byte over the 56-RAMB36 budget ledgered to #640; each ring and bucket derived at the shape with its clause (census section 5) |
| 5. Run the point | `ctrl_service_budget/run.py --point 32x32`: every non-save group graded; T_svc misses recorded, not graded, beside 1x1/1if and 8x8/2if; measured costs beside S2b round 22's projection with the error |

The 1x1 and 8x8 shapes are unchanged: their generated outputs match a pinned golden (builder gate 41) equal to the base generators' digests, their firmware images link to the base's bytes, and their harness scripts are byte-identical to the base's.

Two harness timing rules scale with a point's streams over the 8x8 shape's 18, rounded up (4 at 32x32, 1 at 1x1 and 8x8). The first is every bounded wait's `within`. The second is the owed row's settle before its composed window, whose defined load needs an empty event ring at the window's first instant. Neither changes a grade, a ceiling or a defined load. At 32x32 with the 8x8 timing, a GET_TX_STATE answered 54.5 ms after its command, past its 20 ms wait, and the owed row's held-response pass ran 65.1 ms, so two of its fifteen grandmaster changes did not fit the ring.

New checks, each with a plant that must fail it: gate 39 (the option and the routed outputs) and gate 41 (the pinned shapes' outputs) in `test_builder.py`; `test_soc_options.py`'s route refusal; two `gen_mailbox.py --selftest` arms; `test_ctrl_memory.py`'s simulation-map arm; six harness self-test checks in `selftest_shape.py`. The firmware boundary lists `test_builder.py` among the programs that compile none of the firmware's control-stack source, because gate 41 runs the three entity-header generators.

The harness at the head, each point on its own clean clone (misses are recorded, not graded):

| Point | Groups graded | Refusals | T_svc misses (probe instances; paths) | Save groups | Build | Run |
|---|---:|---:|---|---|---|---|
| 1x1/1if | 18 | 0 | 34 of 141; 13 of 81 | run | 33.6 s, 352 MB peak | 41 min 58 s, 50 MB peak |
| 8x8/2if | 17 | 0 | 63 of 182; 31 of 129 | run | 33.8 s, 352 MB | 45 min 0 s, 47 MB |
| 32x32/2if | 17 | 0 | 90 of 182; 56 of 129 | 10 owed to #823 by name | 17.2 s, 359 MB | 55 min 21 s, 51 MB |

The 8x8/2if figure was 57 before the sync. The base `1d6bf555` prints the same 64 `BUDGET`, `OWED` and summary lines at 8x8/2if as this head, so that change came with `dev-soft-core`, which changes two firmware sources (`ctrl_app_aecp.c`'s `available_index`, `ctrl_plat.c`), not from this branch.

Findings, each needing its own issue:

- AECP's face model names one AVB_INTERFACE and places every stream on interface 0, while ACMP, MAAP and SRP place stream n on n mod 2; in the shape's layout the face follows the split's placement (`MBX_STREAM_HOME`). A second AVB_INTERFACE is #394's.
- SRP's participant on each interface declares every source of the entity; in the shape's layout each interface publishes its own sources' bits.
- tsn-c-stack's owed-release mask is 32 bits (`third_party/tsn-c-stack/include/acmp.h:400`, `src/acmp.c:816` and `:871`): at 33 sinks the CRF sink's bit aliases sink 0's, so that sink's change notice is not held behind its owed response (#653). A donor patch for the stack is drafted, not part of this PR; the lane builds the pinned stack.
- ACMP's receive ring holds 12 of its bucket's 16 records and MAAP's 7 of 8 at every shape; at 32x32 ACMP's transmit side holds 20 of a possible 33 probe commands in one pass.
- At 32x32/2if no two consecutive passes are idle (each tick's pass writes the mailbox), so each `wait quiet 3` of the scripts ends at its bound.
- `docs/diagrams/nxn_window_map.gen.py` fails at the base and no gate runs it.

Assumption: the tracked contract holds stream n at entry n of every interface's tables (`sw/mailbox/mailbox.yaml:338-339`), and today's two-interface variant keeps that. The ruling's per-interface ordinals are used by the shape's layout alone (`MBX_ENTRY_ORDINAL`). Whether the 8x8 two-interface variant should move to ordinals is not decided here.

## Sync with dev-soft-core 1d6bf555

`dev-soft-core` `1d6bf555` (S6a #853, the placement switch; S6b #861, the twin co-simulation) is merged into the branch with a merge commit (`df362e7c`); nothing was rebased. Two commits follow it, and nothing else changed:

- **Conflict 1 (textual), `sw/builder/endstation_builder.py` `emit_soc_argv`.** Both sides appended one conditional after `--cpu-count`: this branch's `--simulation-only` and S6a's split placement (`--ctrl-mailbox --ctrl-firmware <image>`). Both arms are kept, this branch's first, no line of either changed. They are independent: every tracked config is all-fabric and not simulation-only, and a split variant's argv is the config's with the split flags last, as builder gate 23n requires.
- **Conflict 2 (semantic), `load_config` in the same file.** Git merged it cleanly, but the result is 102 lines, over `scripts/check_py_idiom.py`'s 100-line rule: S6a added two lines (97) and this branch five (100). `7aa6ef0c` has `_load_streams` read its stream bound from the config's `saved_state` itself, so `load_config` calls it exactly as the base does and is 100 lines. No line of S6a's changed and every generated output is unchanged.
- **The byte-identity gate is renumbered from builder gate 40 to 41** (`c81640ad`), the next free builder gate: `sw/builder/test_declarations.py` already holds builder gate 40 (#400, #403). The golden's description was rewritten by its generator (`--write-shape-golden`) and its digests are unchanged.

What shows S6a's placement key and S6b's twin unaffected at 1x1 and 8x8:

- **The placement key.** Builder gate 41's inventory of the 1x1 and 8x8 shapes covers 33 outputs: every builder output, the three entity headers and the 8x8 two-interface mailbox variant. Each tree's own builder and generators computed it. At this head it equals `1d6bf555`'s twice: as tracked (all-fabric), and with `control: {placement: split}` added to each config. It also equals the head's golden. Builder gates 23n (the placement key) and 23m (the instance's parameters, split cases included) pass beside gates 39 and 41.
- **The firmware images** at 1x1/1if, 8x8/1if and 8x8/2if are byte-identical to `1d6bf555`'s, and the 32x32 image links.
- **The twin.** `make -C tb/verilator/milan_dp twin` exits 0 at this head with "twin: 0 finding(s)". Its notes are the six `LEDGER` rows, the six `OWED` rows and one `[TAIL]` note: an ADP frame past the other half's last, whose next frame was not yet due at the run's end, which `twin_compare.py` does not count as a difference. Its `obj_twin/report.json` is byte-identical to the one `1d6bf555` writes.
- **The 32x32 simulation shape still builds.** The builder writes its outputs and no routed output, and its argv ends `--cpu-count 1 --simulation-only`.

## Authoritative references

- #859: the round 2 ruling (items 1 to 5) and the assignment.
- [32x32 shape census](docs/design/SHAPE_32X32_CENSUS.md), sections 4 and 5.
- The mailbox contract `sw/mailbox/mailbox.yaml` and [the split mailbox](docs/design/MAILBOX_SPLIT.md).
- [Split control memory](docs/design/SPLIT_CONTROL_MEMORY.md), sections 3 and 8.
- [The CPU budget harness](tb/verilator/ctrl_service_budget/README.md) and FR_NFR.md 3.4.1 (T_svc).
- [The two-placement simulation](tb/verilator/milan_dp/README.md#the-two-placement-simulation-obj_twin_-665) (S6b, #861) and the control placement key ([`docs/ENDSTATION_BUILDER.md`](docs/ENDSTATION_BUILDER.md), S6a, #853).
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
python3 sw/builder/test_builder.py --gates test_control_placement_key,test_simulation_shape_option,test_shipped_shape_outputs_unchanged
python3 scripts/check_py_idiom.py
python3 sw/builder/test_soc_options.py
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/build.py /tmp/budget-32x32 endstation_ax7101_32x32 2
python3 -B tb/verilator/ctrl_service_budget/run.py --point 32x32 --build-dir /tmp/budget-32x32 --reuse-build --record-budget-findings
make -C tb/verilator/milan_dp twin
python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir /tmp/nvm-target-32x32
```

Expected result / pass criteria: every command exits 0 except the last. The builder writes the 32x32 shape's outputs and no routed output. Its report lists the board's sweep fragment path, as every build's report does, but the fragment is written only with `--write-fragment`, which the shape refuses, so the tree stays clean. The `test_builder.py` subset prints "ALL GATES PASS" for its 3 of 108 gates, gates 39 and 41 each with its plant turned red. `check_py_idiom.py` exits 0. `test_soc_options.py` and `test_ctrl_memory.py` print "RESULT: PASS". `gen_mailbox.py --selftest` prints "selftest: 0 arm(s) failed". The harness self-test prints "self-test: 0 failures". The 32x32 run ends "17 groups graded, 0 refusals, 90 T_svc misses (90 of 182 probe instances, 56 of 129 paths), 10 save groups owed to #823". The twin prints "twin: 0 finding(s)", with only the ledger, owed and tail notes above. The last command lists the 10 save groups owed to #823 and exits 1, building nothing.

The full local bar passed at the head: every `run:` step of the four workflows a pull request to `dev-soft-core` triggers, the full sweep in four shards, the firmware self-test and every mutant driver, `fw_coverage.py --check`, `test_builder.py --require-rv32`, `cd tests && behave`, and `git diff --check` against the merge base.

## Known limitations / out of scope

- The shape is for simulation only: no route, no bitstream, no flash. The image build refuses to route or load it.
- The record space at 32x32 is #823's: no save group runs at the shape, and each is reported by name as owed to #823.
- The datapath at 32x32 and the 56-RAMB36 budget are #640's: the five guards and every byte over budget are recorded as owed to #640.
- S2b round 22's `events`, `events_none`, `polls_least`, `base`, `event.*` and `item.*` costs are not measured here. The first three cut a pass at `ctrl_loop`'s `service_rx`, which this base's image inlines; the rest are graded by S2b round 22's own head's event and poll graders, which this base does not carry. The costs this base measures the same way (`record.*`, `rebuild`, `centisecond`) were compared in round 2, on round 2's firmware: `1d6bf555` changes two firmware sources (`ctrl_app_aecp.c`, `ctrl_plat.c`), so the 32x32 image differs from the one those costs were measured on, and they were not re-measured in the sync.
- The tsn-c-stack mask fix is a donor patch for the stack, not part of this PR.
- The twin runs at the shipping 1x1 shape only (its config is fixed in `tb/verilator/milan_dp/Makefile`); it does not take the 32x32 shape.

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
