[A809]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `pf-951-943n-1` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `0d80f0ed` (15 commits on the flip train's head `15168e14`), `pf-951-943n-1` -> `dev-soft-core`.

- One gate is not run: the CPU budget harness's formal measurement (every arm and group at a point). The legs the
  change reaches are measured base against head at 1x1/1if and 8x8/1if instead (below).
- One stated cost is restated by the rule: 8x8/1if's own MAAP record, 180 to 185 us. That is a statement; no bound
  changes.

The branch sits on the flip train's head `15168e14` (PR #945, reviewed, not yet merged). When the train merges, this
PR's base is `dev-soft-core` and its diff is this branch's commits only. It touches the split firmware, its tests and
plants, the CPU budget harness (one check, one statement, texts) and docs. No RTL, mailbox-contract, lwSRP, bound or
memory-budget change.

Code head `8845364d`: every code gate ran there. The commits after it change no image:
- `b8890724`: the harness's `declaring-outputs` check, and the plant table's grouping (the same 63 rows).
- `5d8cfd62`: the harness's 8x8/1if MAAP statement.
- `0818deb1`, `03d9d519`, `5d8cfd62` and `0d80f0ed`: docs.

- **Firmware gate**, `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`, all four shards: PASS.
  - Shard 0: 75 verdicts, none failed.
  - Plants: the control campaign catches 826, the AECP campaign 388 and the SRP campaigns 563 (with the pin
    controls). None escaped.
  - The new rows are among them: 13 hold-off and 5 registration rows at each SRP campaign, and 3 registration-notice
    rows in the AECP campaign.
- **The new and restated tests fail on the train's code.** The #956 tests fail at the train's value, at 1x1/1if,
  8x8/2if and in the composed test. The #957 tests fail with the train's `srp_mbx.c` and `.h`: AppOutputs at 1x1 at
  one and two interfaces and at 8x8 at one, the Talker test at 1x1/1if and 8x8/2if.
- **`fw_coverage.py`**: `--selftest` 29 of 29, `--check` PASS (40 files).
- **The twin**: `twin`, `twin-plants`, `twin-maps` and `twin-maps-plants` each rc 0.
- **`plat_ledger.py`**: PASS, 0 findings. The 8x8/1if product image is 139,248 B of rom against 139,264; the train's
  head is 139,208. `struct ctrl_plat` keeps its ledgered size at every point.
- **Images**, base `15168e14` against `8845364d`, 20 images (the platform's 4, the size fixture's 4 and the CPU budget
  harness's 12). `listener` grows by 40 B and nothing else changes size. At 1x1, `srp_mbx.o` alone differs. At 8x8,
  `ctrl_app_aecp.o`, `ctrl_app_srp.o` and `ctrl_plat.o` (the fixture's `ctrl_aecp_image.o`) differ only in field
  offsets, 8 bytes.
- **Release (all-fabric) image**, base and head exported back to back in one clone path: byte-identical but for
  LiteX's generation-time comments and the CPU netlist's per-run name. `bios.bin`, `bios.elf` and its disassembly,
  `libmilan_baremetal.a` and its member, and the rom, mem and sram init files are equal.
- **CPU budget harness self-test** (`run.py --self-test`): 0 failures at `5d8cfd62` (and at `b8890724`), the `declaring-outputs` arm's three new order
  controls among them.
- **CPU budget harness, the legs the change reaches**, base against head with the formal measurement's options.
  - The legs: arm A's `srp`, `backlog-owed`, `aecp` and `datapath-events` (and `aecp-largest-notice` at 1x1/1if),
    `valid-destinations`' `srp-talker-held` and `srp-talker-loss`, and `declaring-outputs`' `aecp-outputs`.
  - 1x1/1if: 71 probes paired, no verdict changed. Each side has arm A's seven known `backlog-owed` misses
    (tsn-c-stack #26) and no other, and no pass is over the share. All 66 stated costs measured are within by the
    rule.
  - 8x8/1if: 95 probes paired, no verdict changed, the same seven misses. All 66 stated costs measured are within at
    the final head's tables, and so is the largest legal notice.
  - One of them is restated. 8x8/1if's own MAAP record measures 17,259 cycles in `srp-talker-loss`, 185 us by the
    rule, over its 180 (16,176 on the base in the same group, the train's full-pass maximum). So
    `load_grade.OWN` states 185, with its measurement in `OWN_MEASURED`.
    - The record runs none of the change's code. The 8 bytes each 8x8 interface's SRP state grew move the data after
      it; at 1x1, where nothing grew, it measures 10,001 on both sides.
    - `load_grade.py --check`, `flip_grade.py --check --point 8x8/1if` and `--point 1x1/1if`, and
      `shape_costs.py --check` pass. 8x8/1if's load stays 0.744 of 0.75, and THE TRANSMIT's row by every source is
      76.86 ms of its 77 (76.81 before).
    - `flip_grade.py --check` at every point fails at base and head alike (the 8x8/2if rows reported, owed to #872);
      the two outputs differ in that row and the `tx_held` wording alone.
  - The head's `declaring-outputs` legs pass with the arm's restated check, regraded on byte-identical rebuilds.
- **Docs workflow steps** at `0d80f0ed`: 104 of 104 rc 0, tracked files unchanged after them. Installs are skipped, and the candidate's own `act_ci.py`
  self-test runs only inside the CI job (AGENTS.md).
- **End-station builder legs** at `5d8cfd62`: both `ALL GATES PASS EXCEPT 1 NOT RUN`: leg 0's MAKEFLAGS mutation arm, which the tree declares has nothing to detect under this make, and leg 1's calibration gate, whose real report needs a build tree this host does not hold.
- Not run here: the full Verilator suite sweep (no RTL change), act and the hosted gates (they follow the push).

## Linked Issue / roles

Closes #956
Closes #957
Relates to #665

Executor: `[A809]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

Both defects were found on the flip bench's re-check of 2026-11-21 at 8x8/1if.

**#956: the MAAP-conflict hold-off.** After a MAAP conflict the split re-declared the moved Talker 30.26 s after its
Leave. #951's `SRP_REDECLARE_CS` was two longest LeaveAll periods **plus** a JoinTime and THE TRANSMIT's term. By the
owner's decision of 2026-11-21 both terms are now counted **inside** the two periods:

| Point | #951 (cs) | This PR (cs) |
|---|---:|---:|
| 1x1/1if (THE TRANSMIT 35 ms) | 3,023 | 2,977 |
| 8x8/1if (77 ms) | 3,027 | 2,973 |
| two interfaces (105 ms) | 3,030 | 2,970 |

The count still starts at the Leave's request (the mechanism is #895's, unchanged). So the changed destination is
declared two longest periods less both terms after the request, and it reaches the wire no later than 30.0 s after
it. On the model's wire, with the request on a centisecond, it is declared at 29,770 ms (1x1/1if) and 29,700 ms
(8x8/2if). With the loop held a JoinTime and THE TRANSMIT's figure from the tick that ends the count, it leaves at
29,995 ms at both. The bench should measure about 29.7 s Leave to Talker at 8x8/1if (it measured 30.26 s with
#951's).

**#957: a STREAM_OUTPUT's Listener registration notice.** When the Listener registered for a running output's stream
changed (Ready, Ready Failed or Asking Failed appearing, replacing another or going), the split sent no unsolicited
GET_STREAM_INFO. lwSRP indicates every Listener registration's start and end (Ignore at the end) and every change of
a registered Listener's declaration. So `listener` now records each change of the declaration it copies in #936's
`noticed` record, while the source's DA gate is open on the interface. The composition and the AECP bridge then take
it as they take a Talker declaration's change: one unsolicited GET_STREAM_INFO of that output to every registered
controller, with the new flags (#943's REGISTERING and REGISTERING_FAILED).

- The DA gate is what the datapath's face reports as the output declaring. MAAP opens it on the source's own
  interface only, so a Listener on another interface records nothing. Behind a closed gate the face shows neither
  flag, so nothing is recorded there either.
- A Listener declared again unchanged (JoinIn or New) records nothing. A registration kept over a LeaveAll is not
  indicated.
- A Ready replaced by a Ready Failed is noticed although the flags are the same, as the release processor's
  LISTENER_REG_CHANGE follows the registration state.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c` | `SRP_REDECLARE_CS` restated (#956); `listener` records the Listener declaration's change under the gate (#957) |
| `sw/firmware/ctrl/srp/srp_mbx.h` | `declaration[CTRL_SRP_SOURCES]`, beside the other per-source byte arrays, in their padding (no struct grows at any platform point); the `noticed` comment |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c`, `sw/firmware/ctrl/loop/ctrl_loop.h` | comments only |
| `sw/firmware/ctrl/test/srp_talker.cpp` | the hold-off tests restated: declared (TALKER_DECL) exactly at two longest periods less both terms after an aligned request, never sooner, on the wire by the two periods, at the latest too (`...AtTheLatest` replaces `...AfterTheLatestLeave`), the destination change while valid and the reset case; `ListenerRegistrationChangeIsNoticed` (new) |
| `sw/firmware/ctrl/test/srp_gate.hpp` | the composed MAAP conflict test: held at 29 s, declared and on the model's wire by 30 s after the conflict |
| `sw/firmware/ctrl/test/test_aecp.cpp` | `AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice` (new): every output of the 1x1 shape at one and two interfaces and of the 8x8 at one, real Listener MRPDUs, the notices read on the wire |
| `sw/firmware/ctrl/test/srp_talker_mutants.py`, `aecp_registration_mutants.py` (new), `aecp_mutants.py` | plants: below |
| `tb/verilator/ctrl_service_budget/declaring_outputs.py` | the arm's check: output 0's declared Talker notice to every registration, then its Listener's, before the first GET's response (`order_findings`, three planted orders in its self-test); REGISTERING required from the Listener's notices on. Before #957 the check required no notice there. |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 8x8/1if's own `record.maap` restated 180 to 185 us by the rule, its measurement recorded |
| `tb/verilator/ctrl_service_budget/flip_grade.py`, `shape_costs.py`, `talker_notice.py`, its README | texts: the hold-off counts THE TRANSMIT's figure |
| docs | `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/reference/FR_NFR.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (a new subsection in section 13) |

**New plants and their failing words.**

- #956, all at 1x1/1if and 8x8/2if (SRP campaign):
  - `talker-hold-off-adds-its-terms` (#951's value back), `...-at-the-latest` and `...-after-a-conflict`: "the changed
    destination reaches the wire no later than two of the longest LeaveAll periods after the withdrawal" (and ", at the
    latest"), and "the new range's destination reaches the wire within two of the longest LeaveAll periods of the
    conflict".
  - `talker-hold-off-a-centisecond-short`: "TALKER_DECL holds a changed destination withdrawn while it waits".
  - `talker-hold-off-takes-its-terms-twice`: "no Talker of a changed destination is declared before the hold-off ends".
  - The existing hold-off plants are restated on the new terms. The two pre-#951 ones now put back the value as it
    was, both terms added.
- #957, SRP campaign at 1x1/1if and 8x8/2if:
  - `talker-registration-unrecorded` and `-of-source-zero`: "a Listener Ready appearing is noticed".
  - `-unchanged-recorded` and `-declaration-uncopied`: "a Listener declared New again unchanged is not noticed".
  - `-ungated`: "a Listener of a source whose DA gate is closed is not noticed".
- #957, AECP campaign at 1x1/2if:
  - `registration-notice-unrecorded`: "a Listener registration change is one notice of its STREAM_OUTPUT to every
    registered controller".
  - `-ungated`: "a Listener on another interface notifies nothing".
  - `-unchanged-recorded`: "a Listener declared New again unchanged notifies nothing".

**The rom.** The target platform's 8x8 image at one interface, a product image, had 56 bytes of its 34 RAMB36 of `rom`
left at the train's head (139,208 of 139,264 B). Two earlier forms of #957 did not fit:

- a comparison of what the output shows at each copy, with its own record and delivery loop: +296 B at 8x8/1if, over
  the CPU budget harness's `declaring-outputs` image there;
- a smaller one: +152 B, over the platform image's ledgered 58 RAMB36.

This form adds 40 bytes, all in `listener` (128 to 168 B at 8x8/1if): 139,248 B, 16 left. No budget moved.

## Authoritative references

- #956's owner decision of 2026-11-21; #951 (its derivation, #665's ruling of 2026-11-19, item 2).
- IEEE 802.1Q-2018 35.2.2.8 (a changed FirstValue on a StreamID), 10.7.4.3 (the leavealltimer's draw), Table 10-7;
  Milan v1.2 Table 4.3.
- Milan v1.2 5.4.5.1 and 5.4.5.2, Table 5.22 (a Stream Output's MSRP Listener attribute registration state), Tables 5.8,
  5.11 and 5.12 (REGISTERING, REGISTERING_FAILED); IEEE 1722.1-2021 7.5.2; IEEE 802.1Q-2018 35.2.2.7.2.
- #943 (the flags), #936 (the STREAM_OUTPUT notice record), #895 (the hold-off's mechanism).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, `sw/firmware/ctrl/srp/README.md`.

## How to get into the same state

```sh
git fetch origin pf-951-943n-1
git checkout pf-951-943n-1
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the pinned toolchain, Verilator 5.050 and the RV32 SDK (sw/firmware/gtest/README.md, docs/testing/CI_WORKFLOWS.md);
# the CPU budget harness's prerequisites (tb/verilator/ctrl_service_budget/README.md)
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <out>
# the CPU budget harness's legs the change reaches, base 15168e14 and this head, at 1x1 and 8x8-1if:
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> \
  --groups srp,backlog-owed,aecp,datapath-events,aecp-largest-notice --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant valid-destinations \
  --groups srp-talker-held --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant declaring-outputs \
  --groups aecp-outputs --record-budget-findings --record-share-findings
```

Expected result / pass criteria: every shard `test_ctrl_firmware: PASS` with no `ESCAPED` line (the new plants among
the `[ok]` lines); coverage `firmware coverage: PASS (40 files)`; every twin target rc 0; `plat_ledger: PASS (0
finding(s))`; every harness leg rc 0 with no row over its bound and its stated costs held.

## Known limitations / out of scope

- **The formal CPU measurement is not run.** At this host's load, a full pass of every arm and group at a point
  is about 70 core-hours, and no CPU range was bookable for it; one was started, then stopped. The legs the change
  reaches are measured instead, base against head. Their figures are within at the final head's tables, but four of
  them sit at their statement by the rule, so a group not run could hold one over it:
  - `centisecond` at 1x1/1if: 16,064 cycles, 170 of 170 us (15,672 on the base in the same group, the train's
    full-pass maximum).
  - `record.srp` at 8x8/1if: 35,273, 375 of 375 (base and the train's maximum 34,803, from the same group).
  - `item.acmp_declined` at 8x8/1if: 2,386, 30 of 30.
  - `record.maap` at 8x8/1if: 17,259, 185 of 185, as restated.
  The full re-measure belongs to the next formal pass.
- **The rom at 8x8/1if** has 16 bytes left in its ledgered 34 RAMB36 (58 in all), a product image.
- **#957 depends on the DA gate.** The notice is raised while the output's DA gate is open, the face's "declaring".
  The `[A809] TAKEN` comment said it would not depend on the Talker's declaration. It changed for the rom, and because
  behind a closed gate the answer shows neither flag. Still as the release: a Ready replaced by a Ready Failed is
  noticed though the flags are the same.
- **A link reset records no Listener change.** It closes the output's declaration as for the Talker; #936 records
  nothing there either.
- **#956's lower bound** holds from a Leave request made on a centisecond. A request mid-centisecond makes the count's
  first centisecond partial, so the count can end up to 1 cs sooner (#895's mechanism, unchanged).
- **T_egress (1 ms) is not one of the hold-off's terms.** The round-up of THE TRANSMIT's term leaves 5, 3 and 5 ms at
  the three shapes, and from Leave to Talker on the wire it cancels.
- **Seen beside it, not changed** (for a new Issue if the maintainer wants one). With the model's loop held across
  the tick that ends the hold-off while lwSRP's join timer ran, at 8x8/2if (one MRPDU a slice), THE TRANSMIT's resume
  slice cleared the interface's due after its MSRP build had been refused. The join timer's expiry, dispatched between
  the slice and its resume, was lost, and the declaration waited for the next periodic transmission. Seen only under a
  held loop's burst of ticks, not shown reachable in real time. The at-the-latest test places its withdrawal so the
  join timer is idle as the count ends, and asserts that.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
