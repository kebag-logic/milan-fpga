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

GREEN — every `run:` step of the four workflows a pull request to `dev-soft-core` triggers: 139 rc 0, 226 not run with a stated reason, 0 bad; the full sweep 65 of 65 suites — `tsn-c-stack-pin-715589c` -> `dev-soft-core`, head `50e2a722ef2671b3f5b017f97b1c7d41705c4f32`.

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
| Ledger the platform's struct at its new size and state each point's plan | `struct ctrl_plat` grows 144 to 152 B at every point, so the platform's ledgered override (keyed on its size) and the memory test's cases are re-measured; `SPLIT_CONTROL_MEMORY.md` section 5 states both images' plans at both pins |
| Hold the owed frames' and kept command's plants in their own table | `acmp_owed_mutants.py`: the same 16 plants, moved unchanged, so `acmp_mutants.py` (961 lines) stays under the Python gate's module length |
| Name the checks the walk leaves to catch two plants | `acmp-timer-port-called-every-time` takes the stack's own A17 words for the same plant; `acmp-admit-on-every-entry`'s adapter kill moves from C1 to C2, because since #32 an entry admits only the sinks it marks and a GET_RX_STATE marks none |

### The ROM/RAM ledger against `70936b77`

Planned by `ctrl_memory.plan`, each pin's image linked with one runtime:

| Point | Fixture `rom` / `sram` B (change) | Fixture RAMB36 | Platform `rom` / `sram` B (change) | Platform RAMB36 |
|---|---:|---:|---:|---:|
| 1x1, one interface | 104,856 (+400) / 46,416 (+144) | 37.5 | 109,920 (+360) / 47,328 (+160) | 39.0 |
| 1x1, two interfaces | 106,408 (+368) / 57,792 (+144) | 40.5 | 111,504 (+304) / 58,736 (+144) | 42.0 |
| 8x8, one interface | 118,568 (+392) / 86,992 (+144) | 50.5 | 123,672 (+368) / 87,904 (+144) | 52.0 |
| 8x8, two interfaces | 120,216 (+384) / 113,152 (+144) | 57.5, ledgered | 125,360 (+312) / 114,080 (+144) | 59.0, ledgered |

- No point's RAMB36 plan moves; every bank is the one it was at `70936b77`. `__lshrdi3` leaves every image.
- The +132 B over-granule ROM effect named in tsn-c-stack PR #34's body is the 8x8/2if `answering-every-port` arm of S2b's harness (#665 issuecomment-6778599191, item 5). That arm is not on `dev-soft-core`; S2b owes its figure at its sync onto this pin. Here the tightest margin is the fixture's 1x1 with two interfaces, 88 B of `rom` before its next granule.
- 32x32: no such shape on `dev-soft-core`; S15 rebuilds it on this pin.

### S2's CPU budget harness at both pins (recorded, not graded)

| Point | T_svc misses at `70936b77` | at `715589c` | "an ACMP command behind the owed input" |
|---|---|---|---|
| 1x1/1if | 34 of 141 instances, 13 of 81 paths | 35 of 141, 14 of 81 | never answered (at least 362.726 ms) -> answered, worst 104.915 ms |
| 8x8/2if | 63 of 182, 31 of 129 | 59 of 182, 31 of 129 | never answered (at least 370.366 ms) -> answered, worst 137.688 ms |

Both answers are over the harness's 20 ms ceiling and within Milan v1.2 Table 5.26's 200 ms. One path crosses T_svc at 1x1: GET_TX_STATE, 9.454 to 10.384 ms. S2b (#810) grades these; `load_grade.py` is not on `dev-soft-core`.

## Authoritative references

- IEEE 1722.1-2021 8.2.4 and 8.2.5 (every received command is answered through `txResponse`), Table 8-3 (no status for a full output queue), Table 8-1 (command timeouts).
- Milan v1.2 5.5.3.5 and 5.5.3.5.3 (a BIND_RX owes its response and its first PROBE_TX), Table 5.26 (200 ms command timeouts), Table 5.32 (BIND_RX_RESPONSE), Table 5.34 (GET_RX_STATE in UNBOUND answers SUCCESS).
- tsn-c-stack `docs/PORTING.md` "ACMP owed bound" and requirement ACMP-12, at `715589c`.
- #859 round 4 ruling, issuecomment-6746289265, item 1; tsn-c-stack PR #34 round 2 ruling, issuecomment-6789256216, item 3; #495's residue row for tsn-c-stack PR #34 (issuecomment-6792448720).
- [Split placement control memory](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 3 and 5; the ACMP adapter's header, `sw/firmware/ctrl/acmp/acmp_mbx.h` (THE KEPT COMMAND).

## How to get into the same state

```sh
git fetch origin tsn-c-stack-pin-715589c
git checkout --detach 50e2a722ef2671b3f5b017f97b1c7d41705c4f32
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

On a clean clone of the head, every gate exits 0:

| Gate | Result |
|---|---|
| every `run:` step of `docs.yml`, `rtl-fast.yml`, `elaborate.yml`, `rtl.yml` | 139 rc 0, 226 not run with a stated reason, 0 bad |
| the full sweep, four shards | 65 of 65 suites, 2,192,899 checks, 0 failures |
| control mutation campaign | 579 of 579 caught |
| `fw_coverage.py --check` | PASS, 35 files |
| `ctrl_boundary.py`, both forms | PASS (3258 and 1019 compiled sources judged) |
| `test_builder.py --require-rv32`, both legs | PASS (with the LiteX interpreter: leg 0 all gates; leg 1 all but one arm that needs a placed hardware build's report) |
| `behave` | 508 scenarios passed |
| S2's harness, 1x1/1if and 8x8/2if | rc 0 at both pins |
| `git diff --check` against the merge base | rc 0 |

## Known limitations / out of scope

- After an accepting poll the adapter offers only the kept record; the records behind it are offered by the next passes' receive service, after their timer service. Where the kept command leaves a slot free (a BIND_RX that is only answered), a timer probe owed at that service can take it and delay the next kept command one pass, as the stack's port contract says of a port that offers fewer frames. Offering the waiting records from the poll would take receive records outside the loop's per-pass budget (`ctrl_loop.h`, A1), which this lane does not change. The adapter's header states it.
- The split image's hot list (`plat/ctrl_split_hot.txt`, `ctrl_hot.py`) is not on `dev-soft-core`; it is on S2b's line (#810), which drops its `__lshrdi3` entry when it syncs onto this pin. Here `__lshrdi3` is absent from every split image and the `platrv32` arm refuses it.
- The 32x32 shape is not on `dev-soft-core`; S15 adds it and rebuilds its image on this pin (#859 round 4 ruling, item 1).
- S2's CPU budget harness is run and recorded at both pins, not graded: S2b (#810) owns the grade and the service loop. `load_grade.py` is not on `dev-soft-core`.
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
