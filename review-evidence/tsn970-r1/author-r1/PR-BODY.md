[A820]

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

GREEN. The firmware gate passes, its four shards at the final head with every planted-defect campaign. So do fw_coverage, the twin and its plants, the split boot simulation at both shapes with its self-test, the platform ledger at every point, the docs workflow steps (104 of 104) and both builder legs. The CPU budget legs at 1x1/1if and 8x8/1if change no verdict. The images differ in `adp.o` alone. The tsn-c-stack change passes its own validation and bare-metal gates.

`pf-970-1` -> `dev-soft-core`, on the flip PR's reviewed head `dd163e41` (#960). This change is the five commits after `dd163e41`; the final head is `27495a06`.

**Dependency.** The ADP core is the pinned tsn-c-stack submodule. This branch's gitlink names `5d14a6d8`, two commits on tsn-c-stack `715589c1` (branch `970-first-advertise`). That change goes through tsn-c-stack's own review first. Once it merges, the pin moves to the merge commit. The repository's rule is in [SPLIT_CONTROL_MEMORY.md, "What is left"](docs/design/SPLIT_CONTROL_MEMORY.md): the stack's changes arrive only through the stack's review, then a pin move. If the merge keeps these `src/` and `include/` bytes, the images do not change. Five records move with the pin:

- the `SUBMODULES.md` row and paragraph;
- the submodule diagram, through its generator;
- the `adp.h` links in `MAILBOX_SPLIT.md`;
- the `adp.h` link in the firmware README;
- the change log's pin line.

## Linked Issue / roles

Closes #970
Relates to #665

Executor: `[A820]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

**The cause.** In the split firmware, an interface's first ENTITY_AVAILABLE after a link-up waits on its TMR_DELAY alone. That delay was drawn from 0 to 4,000 ms on LINK_UP (Milan v1.2 5.6.3.5.3) and from 0 to 2,000 ms at a startup with the link up (5.6.3.5.2). Nothing else holds the first advertise:
- not asCapable, which the firmware never reads;
- not the grandmaster. A GM_CHANGE in DELAY is ignored (Table 5.51), and the frame samples the grandmaster when it is built (IEEE 1722.1-2021 6.2.2.16);
- not a settle timer or a debounce in the adapter;
- not the loop's passes, which take milliseconds;
- not the PHY poll, which publishes the link within its 125 ms period.

On the base, the new host test measures the first ENTITY_AVAILABLE up to 3,990 ms after LINK_UP. With a grandmaster change inside the delay it is up to 3,649 ms; with one 4.5 s after the link-up, up to 3,364 ms.

**The fix.** An interface leaving DOWN now draws from 0 to 500 ms, both at startup with the link up and on LINK_UP. That is a random value within both clauses' ranges (0 to 2 s, 0 to 4 s), and it leaves the 1 s bound half a second for the PHY poll's publication, the LINK event's pass and the frame's pass. DISCOVER, TMR_ADVERTISE and a grandmaster change in WAITING keep the 0 to 4 s draw. A grandmaster change after the first ENTITY_AVAILABLE still sends a new one, with the new gptp_grandmaster_id and the next available_index (5.6.3.5.7, 6.2.2.15).

| Piece | Change |
|---|---|
| tsn-c-stack `include/adp.h`, `src/adp.c` | `ADP_DELAY_STARTUP_MAX_MS` 2000 -> 500; new `ADP_DELAY_LINK_UP_MAX_MS` 500 and `ADP_DRAW_LINK_UP` kind; `adp_link_change` draws it |
| tsn-c-stack tests, plants, docs | A0, A3, A9 (three kinds, against literals), A18, A20; 2 plants restated, 5 new; porting guide, MFDISC-01, generated requirement, traceability and test tables, change log |
| gitlink | `third_party/tsn-c-stack` `715589c1` -> `5d14a6d8` |
| `sw/firmware/ctrl/test/test_adp.cpp` | group G on the mailbox model: G1/G5 (64 LINK_UPs), G2 (32 startups), G3 (grandmaster change inside the delay), G4 (the bench's order, 4.5 s after LINK_UP) |
| `adp_walk.cpp` | the LINK_UP x DOWN cell draws the LINK_UP kind, the firmware's one difference from the processor's T-ADP-DELAY |
| `adp_first_mutants.py` (new), `ctrl_mutants.py`, `ctrl_mutant.py` | 6 new plants, 2 restated, 1 new kill for `gm-change-ignored` |
| docs | `MAILBOX_SPLIT.md` (the ADP slice), `sw/firmware/ctrl/README.md`, `SUBMODULES.md` and the diagram, `FR_NFR.md` (the derivation rows: the split's 0.5 s windows give 50 ms, above ADP's 30 ms row bound, which does not move), `CHANGELOG.md` |

The images change in `adp.o` alone: `.text.enter_delay` grows from 176 to 180 bytes, and the canonical listings differ in five lines, the draw's range and the LINK_UP kind. Every ledger point keeps its RAMB36 count.

## Authoritative references

- Milan v1.2 5.6.3: Tables 5.49 to 5.51; 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.5, 5.6.3.5.7 and 5.6.3.5.9.
- IEEE 1722.1-2021 6.2.2.15 and 6.2.2.16, 6.2.4 (6.2.4.2.2) and 6.2.5.
- tsn-c-stack's porting guide, ADP callbacks: `timer_start` "delivers adp_timer_expired once after delay_ms". This is why the change is the core's: an adapter that shortened the delay would break that contract.
- [MAILBOX_SPLIT.md, the ADP slice](docs/design/MAILBOX_SPLIT.md#the-adp-slice).

Reading for review: Milan's TMR_DELAY is "a random value between 0 and 4 seconds" (Table 5.50), and a value drawn from 0 to 0.5 s is one. IEEE 1722.1-2021 6.2.4.2.2's uniform 0 to valid_time/5 belongs to randomDeviceDelay in the Advertising Entity machine, which Milan 5.6.3's machine replaces for a PAAD-AE.

## How to get into the same state

```sh
git fetch origin pull/<this PR>/head:pf-970-1
git switch pf-970-1
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
git -C third_party/tsn-c-stack rev-parse HEAD   # 5d14a6d816a43a49299172a34e3eeaea44c267c6
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --selftest && python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <dir>/plants --self-test
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <dir>/plat
# in third_party/tsn-c-stack, with its pinned tools:
python3 scripts/validate.py --work <dir>/v --jobs 16 --graphs
python3 scripts/baremetal.py --work <dir>/rv32 --jobs 16
```

Expected result / pass criteria:
- Every firmware shard ends `test_ctrl_firmware: PASS`; the `adp` arm prints the G1 to G4 figures, the latest first ENTITY_AVAILABLE at most 502 ms after its LINK_UP or startup.
- The control campaign catches every plant, the six new ones among them, each by its named test and words.
- fw_coverage PASS; the twin and its plants pass; the boot simulation passes at both shapes and its self-test catches its plants; `plat_ledger: PASS`.
- The stack's gates rc 0, with `{"CAUGHT": 482, "ESCAPED": 0, "ERROR": 0}`.
- The reproduction: with the stack at `715589c1`, G1, G2, G3 and G4 fail by their own words.

Evidence at the final head `27495a06`: the firmware gate, the docs steps and the builder legs. The twin, the boot simulation, the images and the CPU legs ran at `b000faa5`, and no image input has changed since:

| Gate | Result |
|---|---|
| Firmware gate, four shards | PASS: 75 of 75 suite verdicts; control campaign 832 of 832 caught (826 at the base, 6 new); AECP and SRP campaigns, 0 escaped |
| The new tests on the base stack `715589c1` | G1, G2, G3 and G4 FAIL by their own words: the first ENTITY_AVAILABLE up to 3,990 ms after LINK_UP, 1,981 ms after a startup |
| The new tests on the head | PASS: the latest first ENTITY_AVAILABLE 499 ms after LINK_UP, 496 ms after a startup, 457 ms with a grandmaster change inside the delay, 421 ms with one 4.5 s after LINK_UP; the new grandmaster announced within 3,994 ms of its change |
| fw_coverage | PASS, 40 files |
| Twin and its plant and map legs | PASS, 0 findings; the split's first ENTITY_AVAILABLE 91 ms after boot |
| Split boot simulation | 1x1 and 8x8 PASS (ready 27.961 and 67.161 ms; the base 27.952 and 67.223 ms); self-test 6 of 6 plants |
| Platform ledger, base and head | PASS; RAMB36 45 / 46 / 58 / 63 on both |
| Image diff, platform and size-fixture images | only `adp.o`: `.text.enter_delay` 176 -> 180 bytes; 5 canonical lines |
| CPU budget legs, 9 groups, base against head | 63 of 63 probes paired at each point; 0 verdicts changed; 0 misses; largest difference −0.074 ms (1x1/1if), +0.097 ms (8x8/1if) against 20 ms |
| First ENTITY_AVAILABLE after LINK_UP on the CPU budget harness | 91.142 ms at 1x1/1if and 89.366 ms at 8x8/1if (the base 730.108 and 719.315 ms) |
| CPU table graders | byte-identical at base and head |
| Docs workflow steps | 104 of 104 |
| Builder legs 0 and 1 | PASS, each with its one NOT RUN arm the tree declares |
| tsn-c-stack `validate.py --graphs`, `baremetal.py` | rc 0, rc 0; 482 of 482 plants caught |

## Known limitations / out of scope

- The bench re-run of the affected scenarios is the manager's, after merge.
- Part of #970's 5.76 to 6.82 s comes before ADP's LINK_UP, since it is past the 4 s draw, so this change may not remove all of it. From the code, the candidate is the boot path. The published link word resets to up, so the datapath transmits on a link the PHY formed before the first poll. The poll then restarts autonegotiation at every boot (#840), which drops that link. ADP's LINK_UP comes only after the renegotiation. This cannot be measured without the bench, and it is not changed here; a separate issue is recommended.
- The all-fabric placement's ADP engine (protocol-processor) is unchanged: it still draws 0 to 4 s on LINK_UP.
- The startup draw is nearly the same at every boot of one entity, because its seed is the entity ID and the clock at enable. This is pre-existing and noted only.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench re-run is pending, after merge)
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
