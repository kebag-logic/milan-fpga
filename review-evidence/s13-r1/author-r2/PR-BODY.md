[A815]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN for review (round 2) — 23 commits; R880-1's and R879-1's findings answered; the image identity (now with its operands and a replay), the flip check, the timing floor (best of three directives) and every local gate pass, apart from the recorded CI-environment rows — `s13-flip-default` -> `dev-soft-core`

## Linked Issue / roles

Relates to #665

Executor: `[A815]`
Internal cleared-context reviewer: `[R<n>]` (assigned by the manager)
External reviewer: `[R<n>]` (assigned by the manager)

## Description

The Mark II split flip (#665 S13). The split placement becomes the shipping default for the two AX7101 shapes the
bench gate qualified (1x1/1if and 8x8/1if), and a split image reads VERSION major 3. The all-fabric placement stays
built and gated behind its switch, so the flip reverts in one commit. The processor is deleted only after the full
qualification (NFR-SCOUT-02), not here.

| Piece | Change |
|---|---|
| Version chain | `milan_csr.sv` states `VERSION_SPLIT_MAJOR = 16'h0003` beside `VERSION`; the datapath's `CTRL_SPLIT_P` selects it, so a split image reads `0x0003_0060` and an all-fabric one `0x0002_0060` (one minor, stated once). VERSION reaches the fabric only as the CSR defaults ROM's word for `0x004`. The ENTITY `firmware_version` is derived at the config's placement: 3.96.0 split, 2.96.0 all-fabric |
| Defaults | `configs/endstation_ax7101_1x1_tdm8.yaml` and `_8x8.yaml` state `control: {placement: split}`; the Arty configs stay all-fabric. The tracked AX7101 sweep fragment is regenerated from the 1x1 config, and `sweep.sh`'s AX7101 row carries the split |
| The switch | `endstation_builder.py <config> --placement all-fabric`, and `BUILD_PLACEMENT=all-fabric ./build.sh ax7101` for the release image. Any `--placement` recipe refuses `--write-rtl` and `--write-fragment`, so tracked files follow the config's own placement |
| Identity | The split manifest records the split VERSION; the identity gate reads a manifest's VERSION at the placement it claims, the placement rule holding the datapath to it |
| Simulations | `sim_split.cpp` pins the split datapath's VERSION `0x0003_0060` and major 3, with a planted defect in `split_mutants.py`; `milan_dp/sim_main.cpp` adds the all-fabric major 2 beside its full word; the split stand-ins (split boot, reboot, service hooks, platform unit bus) answer `0x0003_0060`; the UART grader accepts major 2 or 3 at minor ≥ `0x0056` |
| Gates | Builder gates 23n and 23o hold the AX7101 configs at the split and the rest all-fabric, both recipes and the firmware-string difference; 23m, 1e and 23g elaborate the split recipes with a synthetic platform image and keep the all-fabric builds; 24 and 25c read the string per placement; the entity-shape gate checks it per placement; the feature ledger's current version is the shipping split image's; the clock-constraint probe elaborates the split at both shapes and the all-fabric release; the publication census reads each config's all-fabric build; the control-memory test starts from the all-fabric argv. Each new rule carries a planted defect |
| Tools the flip moved | The #649 resource sweep prices the placement its plan names (all-fabric, the recorded figures' placement) and refuses, before any export, an argv naming a platform image the tree does not hold; the CPU-budget harness replaces the split config's image pair with its own instead of appending a second, so its export argv is the measured run's again |
| Docs | Every "which placement ships" statement, the split contract's section 7, the feature ledger rows, the generated register map (its memory map and build parameters labelled as the recorded all-fabric build's, the split's map pointed at), the README's pipeline picture (labelled the all-fabric release flow, the split build stated beside it), the changelog, `BUILDING.md`, the builder key table, and the documentation inventory (D0-001, D0-033 and D0-056 retired: the default they contradicted is now the split) |

## Authoritative references

- NFR-SCOUT-02 ([FR_NFR.md 3.4](docs/reference/FR_NFR.md)).
- [ARCHITECTURE_HW_SW_SPLIT.md section 7](docs/ARCHITECTURE_HW_SW_SPLIT.md#7-version-and-default-flip): major
  `0x0003` only for split images, all-fabric keeps its identity, MINOR flat, the version chain and its simulations.
- #665: the flip plan's item 6 (issuecomment-6799253003); owner decisions issuecomment-6410301079 (the flip changes
  the default and sets VERSION major 3; all-fabric stays built and gated), -6845315282 (8x8/1if a must, 2if
  optional), -6930885185 (#818's floor), -7044585511 (the 1x1/1if rows); the bench re-check issuecomment-7063917242.

## How to get into the same state

```sh
git fetch origin s13-flip-default && git checkout --detach FETCH_HEAD
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml                        # split
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml --placement all-fabric # release
```

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration   # gates 23m-23p among them
python3 scripts/check_entity_shape.py --self-test
python3 scripts/check_feature_status.py --self-test
python3 scripts/check_sweep_shape.py --self-test
python3 scripts/baremetal_uart_smoke.py --self-test
python3 syn/resmap/soc_sweep.py --selftest
python3 tb/verilator/ctrl_service_budget/run.py --self-test
(cd tb/verilator/milan_dp && make split && python3 split_mutants.py)
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria:

- The builder suite prints `ALL GATES PASS EXCEPT 2 NOT RUN` (a make that does not re-read MAKEFLAGS; gate 11's
  calibration report, which is bench-local); the four self-tests and the split leg pass, and `split_mutants.py`
  catches 32 of 32.
- `flip_grade.py --check --point 1x1/1if` and `--point 8x8/1if` print `RESULT: PASS`: 1x1/1if load 0.511 (0.70),
  last queued notice 127.31 ms (tree 130, owner 140), ACMP 29.06 ms (30), txL 47.88 ms (49); 8x8/1if load 0.744
  (0.75). `--check` alone reports 8x8/2if (reported, not held), byte-identical to dev-soft-core's.
- The sweep: every suite PASS (65; at this head's evidence 51 in the sharded sweep and 14 rerun alone after the wall
  clock killed them under host load).

The evidence, with each command, head and receipt, is posted with the review-ready comment on #665: the image
identity of both bench-gated images (only the VERSION word, the firmware string and the integrity words computed
over them change; netlist, placement and routing are the bench images'), the timing floor at every corner, the
release (all-fabric) export, the CPU-budget harness images and the re-measured descriptor groups.

## Known limitations / out of scope

- The processor is not deleted (NFR-SCOUT-02: after the full qualification). NFR-SCOUT-02 and REQUIREMENTS section 1
  tie deletion to "the switch-over"; this PR follows #665 issuecomment-6410301079 (the flip changes the default)
  and restates REQUIREMENTS section 1 to that order. The normative NFR-SCOUT-02 row is not edited: for the owner.
- The Arty configs stay all-fabric: the bench gate covered only the two AX7101 shapes.
- The full CPU-budget harness re-measure (64 parts a point) is not run: the identity packet published with round
  2's review-ready comment holds the 16 image pairs, the 13 re-measured groups' operands and a replay showing they
  differ only in the firmware string and its CRC.
- The register map keeps its recorded all-fabric SoC export; its memory map and build parameters are labelled as
  that build's and point at the split's map. Re-recording it from a split export restates the memory map and the
  0x920 window: a follow-up Issue, to be opened by the manager.
- The resource map (#649) still prices the all-fabric SoC, the placement its figures were recorded at; pricing the
  split SoC is new measurement work, not this PR's.
- #954 (GET_TX_STATE REGISTERING_FAILED at 1x1/1if) is the first PR after this one, as decided.

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
