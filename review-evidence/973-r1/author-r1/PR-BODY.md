[A822]

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

GREEN. The firmware gate passes, its four shards with every planted-defect campaign (the seven new plants caught in all three SRP campaigns). So do fw_coverage, the twin and its plants, the platform ledger at every point, the split boot simulation at both shapes with its self-test, the docs workflow steps (104 of 104) and both builder legs. The CPU budget legs at 1x1/1if and 8x8/1if change no verdict, and the CPU rows' graders are byte-identical to the base's. The images differ in `srp_mbx.o`'s code, +8 to +24 B of ROM, with every RAMB36 count unchanged.

`pf-973-1` -> `dev-soft-core`, on the flip PR's reviewed head `dd163e41` (#960). This change is the eight commits after
`dd163e41`; the final head is `9a71daa9`. The diff touches SRP's adapter and its tests only: no RTL, mailbox contract,
loop, CPU budget bound or harness file.

## Linked Issue / roles

Closes #973
Relates to #665

Executor: `[A822]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**The defect.** On the one-hart split image, the loop takes the event ring's records as a pass starts, and SRP's poll
read the LINK register later in the same pass.
- A link that comes up in between reads up in the register before any LINK record has carried it.
- The poll reset the interface on that level and set `link_seen`.
- The LINK UP dispatched next pass was then a repeated UP, which `on_event` treats as coalesced down/up edges, so it
  reset the interface again.
- A first UP lost the clean startup participants it otherwise keeps (`hold`); a later UP reset the interface twice.
- The one-hart CPU budget harness never showed it, because there the link moves at a pass boundary.

**The fix** (`srp_mbx.c`, `srp_mbx.h`):

| Piece | Change |
|---|---|
| `struct srp_interface` | `link_carried`: the level the last LINK the loop dispatched carried; attach gives it the register's level |
| `on_event` | each LINK sets `link_carried` beside `link` |
| `srp_mbx_attach` | `link_carried` starts at the level attach reads |
| `poll` | `links[n] = mbx_link_up(n) && m->ifs[n].link_carried` |

- A DOWN is still taken from the register, so a link lost while a full ring holds its record back fails closed at
  once.
- An UP is taken only while the last LINK carried one. A register that rose after the pass's events changes nothing
  until its LINK comes, and that LINK is then a first UP.
- An UP whose DOWN record a held ring cancelled is still recovered from the register.
- A reattach to a link already up keeps it without another record.
- The poll still reads the register once per interface.

The second-hart lane's fix for two harts compares the level its loop dispatched (`ctrl_loop_link_up`). That loop
also reads the register after the ring each pass and dispatches a LINK for a moved level, so its level follows a DOWN
at once. The one-hart loop has no such read, so this port keeps the register's DOWN. A first version here recorded
the level in the loop; it put the 8x8/1if platform image at 58.5 RAMB36, past its ledgered 58, so the level lives in
SRP's interface instead.

**Tests and plants.**
- `srp_link_pass.cpp` (new) boots SRP on the real loop and the mailbox model with every link down. It moves interface
  0's link at four phases of a pass: before it, in its events, after its events and before SRP's poll, and after
  SRP's poll.
- It counts the interface's resets by its LICENCE publication writes. The first UP must reset nothing and keep the
  startup participants, and its declarations must leave. A DOWN must reset once, and the next UP once.
- `srp_arms.link_pass_arms` runs it at 1x1/1if and 8x8/1if, each build a process of its own.
- At the test's commit (`406c4a89`, the base firmware) the after-the-events phase fails at both shapes: the first UP
  resets twice and loses the startup participants, and a later UP resets twice. The other phases pass.
- `srp_link_mutants.py` (new) holds seven plants, each caught by its named test's own words in the 1x1/1if, 8x8/1if
  and 1x1/2if SRP campaigns. They are: the fix reverted; a double reset at the first UP; a double reset at a later UP;
  a first UP that resets; the level never carried; attach carrying nothing; and the two-hart form taken whole, which
  loses the fail-closed DOWN.
- The existing `srp-poll-extra-read` plant follows its moved planting site.

**Docs.** The SRP adapter's README states the rule, and the changelog records it.

## Authoritative references

- #973 and its acceptance; #665.
- IEEE 802.1Q-2018 10.7 (MRP participants and a port's operational state) and 35.2 (MSRP).
- [`sw/firmware/ctrl/srp/README.md`](sw/firmware/ctrl/srp/README.md), the link lifecycle.
- [`sw/firmware/ctrl/loop/ctrl_loop.h`](sw/firmware/ctrl/loop/ctrl_loop.h), the pass's order: events, records, polls.

## How to get into the same state

```sh
git fetch origin pf-973-1 && git checkout --detach 9a71daa9aa2379e2a57eb93ccafe83101bcb37f7
git submodule update --init third_party/lwSRP third_party/tsn-c-stack protocol-processor gptp-processor third_party/verilog-axis
```

The pinned RV32 SDK, Verilator 5.050 and the product LiteX environment are as in [QUICKSTART.md](QUICKSTART.md).

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard K/4 --jobs 4   # K = 0..3
python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat
G=srp,adp-link,maap,control,backlog,aecp,aecp-fanout,acmp-cmd,datapath-events,fixture
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/b1 --groups $G --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir /tmp/b8 --groups $G --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
```

Expected result / pass criteria:

| Gate | Expected at the head |
|---|---|
| Firmware gate, 4 shards | PASS each. Suites 77 of 77 verdicts, `srp-srp_link_pass-if1-*` at 1x1 and 8x8 among them; control 826 of 826; AECP 385 `[ok]`; SRP 564 `[ok]`; 0 escaped |
| `fw_coverage.py` | `--selftest` PASS; `--check` PASS (40 files) |
| Twin and its plants | 0 findings; every plant refused |
| `plat_ledger.py` | PASS at every point: RAMB36 45 / 46 / 58 / 63 as at the base; ROM +16 / +24 / +8 / +16 B; SRAM unchanged |
| CPU budget legs, the 10 groups, 1x1/1if and 8x8/1if | 0 refusals, 0 budget misses, no pass over THE SHARE; base and head pair on every probe (88 and 86) with no verdict changed |
| `flip_grade.py --check --point 1x1/1if` and `--point 8x8/1if` | PASS, byte-identical to the base: 1x1/1if load 0.511 (0.70), last queued notice 127.31 ms, ACMP 29.06 ms, txL 47.88 ms; 8x8/1if load 0.744 (0.75) |
| Split boot simulation | 1x1 ready 27.973 ms, 8x8 67.224 ms; self-test 6 of 6 native controls and 6 of 6 plants |
| Docs workflow steps; builder legs 0 and 1 | 104 of 104; PASS and PASS, each with the one NOT RUN arm the tree declares |

At the test's own commit, `406c4a89` (the base firmware), `SrpLinkPass.AfterTheEventsBeforeSrpsPoll` fails at both
shapes ("a first UP resets nothing": 2 resets; "a first UP keeps the startup participants"; "a later UP resets the
interface once": 2), and the other three phases pass.

## Known limitations / out of scope

- A DOWN inside a pass still resets twice: the poll takes it from the register (fail closed), and the LINK DOWN
  record resets again. Both come before the participants are rebuilt, so nothing clean is lost; the rebuild waits
  one more pass. #973's acceptance is the link-up.
- A LINK that SRP's sink drops on a re-entry (counted in `reentries`, asserted in debug builds) is not carried. A
  dropped DOWN still comes from the register; a dropped UP waits for the next LINK.
- The 8x8/1if platform image is now 48 B of ROM below its next half-tile (139,216 of 139,264 B).
- The second-hart lane (#872) changes the same poll line on two harts; the merge of the two is that lane's.
- No bench run: the bench scenarios are re-run after merge.

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
