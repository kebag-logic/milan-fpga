[A767]

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

GREEN. Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers, on clean clones of the merge `8bc1dfc0` with the pinned RV32 SDK: 150 rc 0 (the eleven "Install and verify the pinned RV32 SDK" steps among them), 215 not run with a stated reason, 0 bad. The control mutation campaign caught 586 of 586. Branch `tsn-c-stack-pin-715589c` -> `dev-soft-core`, head `6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c`: the merge of `dev-soft-core` `0fb66211` into round 3's `32b43973`, then one documentation commit, whose docs gates ran at the head (`docs.yml`: 64 rc 0, 31 not run with a stated reason, 0 bad; `git diff --check` against `0fb66211` rc 0).

## Linked Issue / roles

Relates to #665

Executor: `[A767]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

`third_party/tsn-c-stack` moves from `70936b77` to tsn-c-stack `main` `715589c1` (an ancestor check first: `70936b77` is an ancestor of `715589c1`, which is `origin/main`). This is the pin move #859's round 4 ruling (issuecomment-6746289265, item 1) makes its own lane, and the parent consumer bar tsn-c-stack PR #34's round 2 ruling (issuecomment-6789256216, item 3) defers to it. The move adopts:

| tsn-c-stack PR | Issue | What the parent consumes |
|---|---|---|
| [#29](https://github.com/kebag-logic/tsn-c-stack/pull/29) | [#27](https://github.com/kebag-logic/tsn-c-stack/issues/27) | `wire_put_be` packs its value in two 32-bit halves; no field write calls `__lshrdi3` |
| [#30](https://github.com/kebag-logic/tsn-c-stack/pull/30) | — | The stack's one-line message rule exempts the merge of #29; no source change |
| [#28](https://github.com/kebag-logic/tsn-c-stack/pull/28) | [#26](https://github.com/kebag-logic/tsn-c-stack/issues/26) | `acmp_rx` declines, never drops, a command behind the full owed set (ACMP-12) |
| [#33](https://github.com/kebag-logic/tsn-c-stack/pull/33) | [#31](https://github.com/kebag-logic/tsn-c-stack/issues/31) | The owed-release mask is sized from `ACMP_MAX_SINKS`: one word at the firmware's 16 sinks, the same layout |
| [#34](https://github.com/kebag-logic/tsn-c-stack/pull/34) | [#32](https://github.com/kebag-logic/tsn-c-stack/issues/32) | Each ACMP entry walks only the sinks it changed |

Commits, in order:

| Commit | What and why |
|---|---|
| Move the pin and plant the campaign's ACMP defects on the lines it changed | The gitlink. 17 control-campaign plants are copies of the stack's own plants; each is re-anchored on the stack's own `715589c` text of the same plant (the walk's `mark()` calls, the release word, `k + 1u`, `busy_declined`). `ACMP_FINISH` follows the walk-only `finish()`. The full-queue plant's kill moves to the renamed `A19AFullQueueDeclinesTheCommandBeforeItActs`, with `AcmpOwed.HeldEgressDefersTheCommandBehindTheOwedSet` beside it |
| Keep a declined ACMP command and offer it again after the next poll that sends | #28's port contract ("ACMP owed bound"): the ACMP adapter keeps the record the core declines, takes no later acmp record while it holds it (the channel's ready hook), and offers it again after a poll that sent an owed frame, before the next pass's timer service. `acmp_rx_ready` is not used to gate: a port that gates on it gives the core no sign of the waiting command. Tests K1 to K3 and eight plants |
| Refuse the 64-bit shift helper in the split platform's RV32I build | #29's purpose held: the `platrv32` arm fails when the split platform's objects reference `__lshrdi3`; the plant restores the per-byte form of `wire_put_be` |
| Name `715589c` in the submodule reference, its diagram and the firmware's links | `SUBMODULES.md` (pins table, adoption table), the regenerated boundary diagram, the stack links in four READMEs and `MAILBOX_SPLIT.md`; the size fixture's helper list (452 B, no `__lshrdi3`) |
| Record the firmware coverage ratchet | `fw_coverage.py --write`: every file still 100 %; the adapter 93/93 lines and 36/36 branches |
| Ledger the platform's struct at its new size and state each point's plan | `struct ctrl_plat` grows by 152 B with one interface and by 144 B with two, at both shapes (round 1; the round-2 redelivery adds 8 B at the two-interface points), so the platform's ledgered override (keyed on its size) and the memory test's cases are re-measured; `SPLIT_CONTROL_MEMORY.md` section 5 states both images' plans at both pins |
| Hold the owed frames' and kept command's plants in their own table | `acmp_owed_mutants.py`: the same 16 plants, moved unchanged, so `acmp_mutants.py` (961 lines) stays under the Python gate's module length |
| Name the checks the walk leaves to catch two plants | `acmp-timer-port-called-every-time` takes the stack's own A17 words for the same plant; `acmp-admit-on-every-entry`'s adapter kill moves from C1 to C2, because since #32 an entry admits only the sinks it marks and a GET_RX_STATE marks none |
| Redeliver the kept ACMP command and the records waiting behind it after each poll that sends an owed frame, and pin the poll's still-owed return at one frame | The port contract's redelivery rule (PORTING "ACMP owed bound"): after a poll that sent an owed frame, the adapter offers the kept record, then the records waiting in the acmp ring in arrival order, until the core declines one or none is left, before the next timer service. It takes at most a full ring (19 records), in the loop's buffer, counted as the loop counts its own. A command behind frames that need no answer now leaves in pass n + 1 + f (R830's probe: pass 10, not 11). Tests E3 and K4 to K7, six new plants, four re-anchored |
| State the ACMP pass bound with the redelivery | `ACMP_MBX_PASS_MAX` grows from 1,030 to 2,754 accesses (the redelivery: 52 + 19 x (36 + 52) = 1,724). `MAILBOX_SPLIT.md` and the firmware READMEs restate every bound derived from it, and the statements of which bounds fit T_svc and the 20 ms ceiling |
| Record the firmware coverage ratchet | `fw_coverage.py --write`: the adapter 106/106 lines, 42/42 branches |
| Ledger the platform's struct with the redelivery, and the fixture's 1x1/2if at 41.0 | `struct ctrl_plat` grows 8 B at the two-interface points (the loop pointer), so the 8x8/2if override is re-keyed at 21,392 B; `SPLIT_CONTROL_MEMORY.md` section 5 restated. The size fixture's 1x1 with two interfaces takes a fourth `rom` bank, 40.5 -> 41.0 RAMB36, accepted on #665 (issuecomment-6807277620) |
| Label S2's unanswered ACMP commands as measured at `70936b77` | The S2 README finding and `scenario.py`'s comment are stated at `70936b77`; with `715589c` the core declines those commands and the adapter keeps and answers them (the record below) |
| Hold S2's scenario module at the Python gate's module length | `scenario.py` was 1,000 lines; the previous commit's comment took it to 1,003 and the Python idiom gate refused it as a new long module. The comment says the same in two lines |
| Pin the ACMP redelivery's stop at a declined command with a record waiting behind it | Test K8: the owed set full, then three GET_RX_STATEs. The first is kept and two wait behind it. After the egress returns, every command is answered once, in arrival order, and nothing is kept or owed after. Plant `acmp-redelivery-past-a-decline` drops the redelivery's `m->kept.len == 0u` stop; the third command's decline then overwrites the second, which is never answered, and K8 fails by name |
| Merge `dev-soft-core` `0fb66211` | One merge commit. Since this PR's base `1d6bf555`, `dev-soft-core` landed #874 (lane S7's lwSRP transmit path), #880 (the saved-state format for shapes up to 32x32, with the split's KLJ3 stage, #823), #889 (the split image's identity gate) and #888 (the split CPU's region decode). Two files conflicted: `ctrl_memory.py`'s platform key and `SPLIT_CONTROL_MEMORY.md`'s ledger table. Both are resolved from the composed images' measurements, not by picking a side: the platform's key is `nvm_stage` 13,594 B (dev's KLJ3 stage) with `ctrl_plat` 21,392 B (this PR's), at 59.0. The size fixture's 8x8/2if point is ledgered at 58.0, the owner's allowance (#665 issuecomment-6824896581). `coverage.ratchet` is regenerated by `fw_coverage.py --write` on the merged sources. It records dev's current measurement: at `0fb66211` itself the generator, and hosted CI, already measure `nvm_store.c` 459/459 and `ctrl_app_aecp.c` 165/165, one line more in each than `0fb66211`'s committed ratchet. The pin move and the composition change neither |
| State both regions' smallest margins at the merge and dev's four PRs, and hold S2's 8x8 plan to the ledger by name | `SPLIT_CONTROL_MEMORY.md` section 5 states the smallest margin of each region and the four PRs `0fb66211` carries. The S2 harness README names `ctrl_memory.LEDGERED` for its 8x8 plan instead of a stale 57.5 |
| Name the BIND_RX case of the kept command and the adapter's loop pointer in the split pages | `MAILBOX_SPLIT.md`: a BIND_RX with fewer than two owed slots free is declined too. `SPLIT_CONTROL_MEMORY.md` section 5: the `sram` growth is the adapter's pointer to its loop |

### The RV32 SDK every figure here was built with

Every RV32 build in this PR's figures and gates used the pinned SDK, `scripts/ci_rv32_sdk.py`'s Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1` (GCC 14.3.0), verified by `ci_rv32_sdk.py --verify-only` (rc 0). In each gate job its "Install and verify the pinned RV32 SDK" step ran and verified that install ("SDK cache hit: verified"). The builder's RV32 gate (`test_builder.py` gate 1b) finds its compiler under HOME. At this head, builder leg 0 ran with HOME at the pinned SDK's parent: its gate 1b names `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`, and `ci_rv32_sdk.py --verify-only` on that SDK is rc 0 in the same run. Round 2's builder legs ran with the real HOME, whose compiler there is the other GCC 14.3.0 build (Buildroot 2026.05). The previous revision of this description stated the replica's SDK as the pinned one when the round-1 figures were built by another build of GCC 14.3.0. Rebuilt on the pinned SDK, those figures come out byte-identical, at `1d6bf555` and at `50e2a722`, for the size fixture and the platform image.

### The ROM/RAM ledger against `dev-soft-core` `0fb66211`

Planned by `ctrl_memory.plan` at `0fb66211` and at the merge head, each image built with the pinned SDK and linked with one runtime. The platform image is linked against the merge's own split SoC export and flash map:

| Point | Fixture `rom` / `sram` B (change) | Fixture RAMB36 | Platform `rom` / `sram` B (change) | Platform RAMB36 |
|---|---:|---:|---:|---:|
| 1x1, one interface | 105,696 (+528) / 46,784 (+160) | 37.5 | 110,760 (+488) / 47,680 (+144) | **39.5** (was 39.0) |
| 1x1, two interfaces | 107,264 (+512) / 58,160 (+144) | 41.0 | 112,352 (+440) / 59,104 (+160) | 42.0 |
| 8x8, one interface | 119,400 (+520) / 87,568 (+144) | 51.0 | 124,504 (+488) / 88,480 (+144) | 52.5 |
| 8x8, two interfaces | 121,064 (+520) / 113,728 (+144) | **58.0** (was 57.5), ledgered | 126,208 (+448) / 114,672 (+160) | 59.0, ledgered |

- Two plans move against `0fb66211`.
  - The fixture's 8x8/2if needs 232 B of `rom` past dev's five banks and plans 58.0. The owner allows 58.0, at most 58.5, as named ROM debt owed to S14 (#665 issuecomment-6824896581). `ctrl_memory.LEDGERED` holds it at 58.0.
  - The platform's 1x1/1if needs 168 B past its four banks and plans 39.5, within 56.
- Every other point is at or under 56. The platform's 8x8/2if keeps its 59.0, within the owner's 60.0.
- `nvm_stage` is dev's (3,454 / 13,594 B) and `struct ctrl_plat` this PR's (18,584 / 20,080 / 19,240 / 21,392 B): `nm` of each image.
- On `1d6bf555`, before the merge, this PR moved the fixture's 1x1/2if from 40.5 to 41.0 (accepted, issuecomment-6807277620). `0fb66211` plans that point at 41.0 already, with its KLJ3 stage.
- The smallest margins at the merge are 288 B of `rom` (the platform's 1x1/2if) and 16 B of `sram` (the platform's 8x8/2if). One byte past those 16 B plans 59.5, within the owner's 60.0, but past the 59.0 its override holds, so that image would be refused until the ledger is measured again. `__lshrdi3` leaves every image.
- 32x32: no such shape on `dev-soft-core`; S15 rebuilds it on this pin.

### S2's CPU budget harness at both pins (recorded, not graded)

Both pins on the pinned SDK, `run.py --point 1x1|8x8 --record-budget-findings`, every group, measured on `1d6bf555` before the merge (at `8ffcf2fc` and `bfe7a9d6`). At the merge head only S2's `run.py --self-test` was run (0 failures); the full harness was not re-run:

| Point | T_svc misses at `70936b77` | with the move | "an ACMP command behind the owed input" |
|---|---|---|---|
| 1x1/1if | 34 of 141 instances, 13 of 81 paths | 34 of 141, 13 of 81 | never answered (at least 362.726 ms) -> all four answered, worst 104.568 ms |
| 8x8/2if | 63 of 182, 31 of 129 | 59 of 182, 31 of 129 | never answered (at least 370.366 ms) -> all four answered, worst 138.526 ms |

Both answers are over the harness's 20 ms ceiling and within Milan v1.2 Table 5.26's 200 ms. At 1x1, ENTITY_DEPARTING now fits T_svc (15.328 -> 7.128 ms) and GET_TX_STATE crosses it (9.454 -> 10.319 ms). At 8x8 the two ENTITY_AVAILABLE rows and the last MAAP record move from MISS ceiling to MISS T_svc (22.883 / 24.163 / 59.158 -> 18.437 / 18.925 / 48.246 ms). S2b (#810) grades these.

### The long-window load (`load_grade.py`, `flip_grade.py`; recorded, not graded)

The flip check is not this PR's gate (#665 issuecomment-6811790762). Neither grader is on `dev-soft-core`. They ran on S2b's head (#810) with this PR's firmware delta and the pin at `715589c`, using S2b's donor-leg groups, its parsers and its round-27 rule for the donor column:

| Point | Committed pin column | Committed donor column | With `715589c` and the redelivery | Ceiling |
|---|---:|---:|---:|---|
| 1x1/1if | 0.463 | 0.450 | 0.483 | 0.70, within |
| 8x8/2if | 0.815 | 0.719 | 0.767 | 0.75, over |

- The rise is ACMP's owed-frame item: the adapter's poll now carries the kept command's handling, 40 -> 165 us at 8x8.
- The heaviest 8x8 poll is 15,550 CPU cycles: the core's poll 3,990, two nested `acmp_rx` calls 9,248, the ring take 2,312.
- With the nested `acmp_rx` attributed to its record (`rec.acmp` already charges it), 8x8/2if reads 0.730.
- #890 carries that accounting rule, the 0.75 ceiling and their controls (#665 issuecomment-6811790762).

## Authoritative references

- IEEE 1722.1-2021 8.2.4 and 8.2.5 (every received command is answered through `txResponse`), Table 8-3 (no status for a full output queue), Table 8-1 (command timeouts).
- Milan v1.2 5.5.3.5 and 5.5.3.5.3 (a BIND_RX owes its response and its first PROBE_TX), Table 5.26 (200 ms command timeouts), Table 5.32 (BIND_RX_RESPONSE), Table 5.34 (GET_RX_STATE in UNBOUND answers SUCCESS).
- tsn-c-stack `docs/PORTING.md` "ACMP owed bound" and requirement ACMP-12, at `715589c`.
- #859 round 4 ruling, issuecomment-6746289265, item 1; tsn-c-stack PR #34 round 2 ruling, issuecomment-6789256216, item 3; #495's residue row for tsn-c-stack PR #34 (issuecomment-6792448720).
- [Split placement control memory](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 3 and 5; the ACMP adapter's header, `sw/firmware/ctrl/acmp/acmp_mbx.h` (THE KEPT COMMAND).

## How to get into the same state

```sh
git fetch origin tsn-c-stack-pin-715589c
git checkout --detach 6eacd76d5f596a88a537dcb4fb5b39a5a2284c3c
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git -C third_party/tsn-c-stack rev-parse HEAD
git -C third_party/tsn-c-stack merge-base --is-ancestor 70936b77 715589c1
```

The pinned RV32 SDK (`scripts/ci_rv32_sdk.py`), GoogleTest and GoogleMock, Verilator 5.050 and the product LiteX environment are needed, as for `rtl-fast.yml`.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/litex/test_ctrl_memory.py
python3 docs/diagrams/submodule_boundaries.gen.py --check
python3 scripts/check_submodule_docs.py
```

Expected result / pass criteria: every command exits 0. The control campaign reports every mutant caught, the nine adapter plants and `wire-put-be-shifts-64-bits` among them.

On clean clones of the merge `8bc1dfc0` with the pinned RV32 SDK (HOME at its install, so every "Install and verify the pinned RV32 SDK" step runs), every gate exits 0. The head `6eacd76d` changes two documentation pages only. Its docs gates and `git diff --check` ran on a clean clone of it (`docs.yml`: 64 rc 0, 31 not run with a stated reason, 0 bad; `git diff --check` against `0fb66211` rc 0); every other row is the merge's:

| Gate | Result |
|---|---|
| every `run:` step of `docs.yml`, `rtl-fast.yml`, `elaborate.yml`, `rtl.yml` | 150 rc 0, 215 not run with a stated reason, 0 bad. On this shared, loaded host, `elaborate-gates-1`'s LiteX simulation aggregate ran with `LITEX_SIM_TIMEOUT=3600`, the runner's own per-script wall clock (default 900 s): all 8 pass, `test_ctrl_memory` among them |
| the Python idiom gate | long modules 10, at the ratchet's 10 |
| control mutation campaign | 586 of 586 caught |
| `fw_coverage.py --check` | PASS, 35 files; the adapter 106/106 lines, 42/42 branches |
| `ctrl_boundary.py`, both forms | PASS (3,284 and 1,101 compiled sources judged) |
| `ctrl_plat_image.py` and the size fixture, all four points | every link rc 0; plans as in the ledger table |
| `test_builder.py --require-rv32`, both legs, HOME at the pinned SDK's parent | leg 0 all gates, gate 1b on `riscv32-linux-gcc.br_real (Buildroot 2021.11-18033-g83947c7bb6) 14.3.0`; leg 1, which compiles no RV32 code, all but one arm that needs a placed hardware build's report |
| `behave` | 508 scenarios passed |
| the sweep's `mbx` suite, the one suite that builds the adapter | 2,810 checks, 0 failures; mutants 12 of 12 (the full sweep was 65 of 65 at `50e2a722`) |
| S2's `run.py --self-test` | 0 failures (the full harness is recorded above, on `1d6bf555`) |
| `git diff --check` against the merge base `0fb66211` | rc 0 |

## Known limitations / out of scope

- The redelivery takes acmp records from the adapter's poll, outside the loop's own receive service. Its work is a term of `ACMP_MBX_PASS_MAX` (1,724 of 2,754 accesses), and the loop itself is not changed. With every term at its maximum, the bound behind a full acmp ring and the owed-frame bound now exceed the 20 ms ceiling at F0's 1 us per access (`MAILBOX_SPLIT.md`). The measured backlogs stay far below.
- The split image's hot list (`plat/ctrl_split_hot.txt`, `ctrl_hot.py`) is not on `dev-soft-core`; it is on S2b's line (#810), which drops its `__lshrdi3` entry when it syncs onto this pin. Here `__lshrdi3` is absent from every split image and the `platrv32` arm refuses it.
- The 32x32 shape is not on `dev-soft-core`; S15 adds it and rebuilds its image on this pin (#859 round 4 ruling, item 1).
- S2b's sync onto this pin owes three updates, measured here on S2b's head with this PR's firmware (#665 issuecomment-6811790762, item 4): its 8x8/2if size fixture's ledger (122,984 B of `rom`, measured on S2b's head; this head's ledger holds that point at 58.0, so S2b restates the key only if its image's symbols or tiles differ); its split hot list's `__lshrdi3` entry, which nothing links since tsn-c-stack#27; and `poll_grade.py`'s 1x1 ACMP item (6,500 cycles stated; the redelivery's poll measured 10,974).
- S2's CPU budget harness is run and recorded at both pins, not graded: S2b (#810) owns the grade and the service loop. `load_grade.py` and `flip_grade.py` are not on `dev-soft-core`; they were run on S2b's head with this PR's firmware delta (above).
- `ci/image/exec-audit-receipt.json` keeps `70936b77`: it is the receipt of an earlier audit of a recorded source tree, not a statement of the current pin.
- The harness READMEs (S2's, S11's) record measurements at the old pin; their owners re-measure.

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
