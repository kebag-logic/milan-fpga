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

GREEN at `1825ba4e` (20 commits on the flip train's head `15168e14`), `pf-951-943n-1` -> `dev-soft-core`. Round 2
answers R876-1 and R875-1 (both NEGATIVE at `0d80f0ed`). Every finding is fixed at its cause; the round's
`[A809] REVIEW READY` on #956 states each one's cause, fix commit, test and receipt.

- One gate is not run: the CPU budget harness's formal measurement (every arm and group at a point). The legs the
  change reaches are measured base against head at 1x1/1if and 8x8/1if instead (below).
- No statement or bound changes this round.

The branch sits on the flip train's head `15168e14` (PR #945, reviewed, not yet merged). When the train merges, this
PR's base is `dev-soft-core` and its diff is this branch's commits only. It touches the split firmware, its tests and
plants, the CPU budget harness (one check, one statement, one control's anchor, texts) and docs. No RTL,
mailbox-contract, lwSRP, bound or memory-budget change.

Code head `847b2e21`; images and every code gate but the firmware gate's at `b4a1dde2`, whose only later change is a
plant table the firmware gate's SRP campaigns read (and which the firmware gate ran again at `847b2e21`).

Round 2's gates (the author packet's receipts; the REVIEW READY on #956 lists them):
- **Firmware gate**, `test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --shard k/4`, k = 0 to 3, at `847b2e21`: PASS, none escaped.
  - Shard 0 (suites): 76 verdicts PASS. That is round 1's 75 plus the new 8x8/1if Talker arm.
  - Control plants: 826 caught.
  - AECP plants: 389 caught (388 + 1).
  - SRP plants: 574 caught with the pins (563 + 11 new rows across both campaigns).
  - Earlier runs: the gate's run at `04819246` was stopped when this round's own check found the refused-second-slice corner (fixed in `b4a1dde2`). The run at `b4a1dde2` caught `talker-unchanged-held` escaping: my plant table had named a new anchor `AGAIN`, over the module's `AGAIN` test name. `847b2e21` renames it, and all four shards ran again there.
- **Each new test fails at `0d80f0ed`** (`new-tests-fail-at-0d80f0ed.txt`).
- `fw_coverage.py --selftest` (29 of 29) and `--check` (40 files) at `b4a1dde2`: PASS.
- Twin, twin-plants, twin-maps and twin-maps-plants at `b4a1dde2`: each rc 0.
- **`plat_ledger.py`** at `b4a1dde2`: PASS, 0 findings.
  - rom: 126,360 / 128,112 / 139,136 / 140,864 B at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if.
  - 8x8/1if has 128 B left of its 34 RAMB36 (16 at `0d80f0ed`).
  - Every CPU budget harness image, all eight arms at three points, links within its budget.
- **Images**, `0d80f0ed` against `b4a1dde2`: only `srp_mbx.o` differs.
  - `transmit`: −116, +40, −112 and +36 B at the four points.
  - `reset_interface`: +4 at 8x8.
- **Release (all-fabric) image**: byte-identical but for LiteX's generation times, the CPU netlist's per-run name, and LiteX's per-run order of the CPU ISA string's extensions. The last is in the BIOS and the library's debug strings, and the same revision exported three times gives both orders.
- CPU budget harness `run.py --self-test` at `b4a1dde2`: 0 failures. `build.py`'s mutation anchors each match once.
- The grade checks on the stated tables (no statement changed this round):
  - `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if` and `--point 8x8/1if`, and `shape_costs.py --check`: pass. THE TRANSMIT's row by every source is 76.86 of 77 ms at 8x8/1if.
  - The full `flip_grade.py --check` fails on 8x8/2if's reported rows, as at `0d80f0ed` (owed to #872).
- **CPU budget harness, the legs the change reaches**: base (round 1's head runs, images equal to `0d80f0ed`'s) against `b4a1dde2`.
  - The legs: arm A's `srp`, `backlog-owed`, `aecp`, `datapath-events` (and `aecp-largest-notice` at 1x1/1if), `srp-talker-held`, `srp-talker-loss` and `aecp-outputs`.
  - 1x1/1if: 71 probes paired, no verdict changed, the seven known misses each side and no other. No pass is over the share and no group has a finding. All 66 stated costs are within by the rule.
    - A build of one is at most 52,531 cycles (735 us stated).
    - `centisecond` is 14,213 cycles, 150 of 170 us.
    - `item.acmp_declined` sits at its statement, 20 of 20 us, as before.
  - 8x8/1if: 95 probes paired, no verdict changed, the same seven misses each side and no other. No pass is over the share and no group has a finding. All 66 stated costs are within by the rule.
    - A build of one is at most 126,644 cycles in `srp-talker-held` (1,475 us stated).
    - Two sit at their statement by the rule: `item.acmp_declined`, 30 of 30 us as before, and `record.srp`, 35,507 cycles in `srp-talker-held`, 375 of 375 us (35,273 before, also 375).
    - `record.maap` is 17,014 cycles, 180 of 185 us (185 of 185 before).
- Docs workflow steps at `1825ba4e`: 104 of 104 steps rc 0, tracked files unchanged after them (installs skipped; the candidate's own `act_ci.py` self-test runs only inside the CI job, AGENTS.md).
- End-station builder legs at `b4a1dde2`: both `ALL GATES PASS EXCEPT 1 NOT RUN`, the same arm not run as in round 1.
- The reviewers' probes at `b4a1dde2`: see each finding above.
- Not run: the formal CPU measurement, the Verilator suite sweep (no RTL change), act and the hosted gates.

## Linked Issue / roles

Closes #956
Closes #957
Relates to #665

Executor: `[A809]`
Internal cleared-context reviewer: R875
External reviewer: R876

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
| `sw/firmware/ctrl/srp/srp_mbx.c` | `SRP_REDECLARE_CS` restated (#956); `listener` records the Listener declaration's change under the gate (#957); round 2: `reset_interface` clears `declaration[]` (#957), and `transmit`, `transmit_aged` and `poll` keep owed what came due between a sliced build's slices, the paused build owed and a refused second slice's interface due (#956) |
| `sw/firmware/ctrl/srp/srp_mbx.h` | `declaration[CTRL_SRP_SOURCES]`, beside the other per-source byte arrays, in their padding (no struct grows at any platform point); the `noticed` comment; round 2: `tx_due` and `tx_resume` in a union with `tx_owed`, read whole |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c`, `sw/firmware/ctrl/loop/ctrl_loop.h` | comments only |
| `sw/firmware/ctrl/test/srp_talker.cpp` | the hold-off tests restated: declared (TALKER_DECL) exactly at two longest periods less both terms after an aligned request, never sooner, on the wire by the two periods, at the latest too (`...AtTheLatest` replaces `...AfterTheLatestLeave`), the destination change while valid and the reset case; `ListenerRegistrationChangeIsNoticed` (new); round 2: the latest case with the join timer running, `EveryPhase/TalkerPhase.*` (every centisecond of a second, held and serviced) and `ListenerRegistrationAfterAResetIsNoticed`, at 1x1/1if, 8x8/1if (a new arm, `srp_arms.py`) and 8x8/2if |
| `sw/firmware/ctrl/test/srp_gate.hpp` | the composed MAAP conflict test: held at 29 s, declared and on the model's wire by 30 s after the conflict |
| `sw/firmware/ctrl/test/test_aecp.cpp` | `AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice` (new): every output of the 1x1 shape at one and two interfaces and of the 8x8 at one, real Listener MRPDUs, the notices read on the wire; round 2: `AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` |
| `sw/firmware/ctrl/test/srp_mbx.cpp` | round 2: `Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue` |
| `sw/firmware/ctrl/test/srp_app.cpp`, `srp_feedback.hpp` | round 2: THE TRANSMIT driven while `tx_owed`, not `tx_due`, is nonzero |
| `sw/firmware/ctrl/test/srp_talker_mutants.py`, `aecp_registration_mutants.py` (new), `aecp_mutants.py` | plants: below; round 2: `srp_transmit_mutants.py` too |
| `tb/verilator/ctrl_service_budget/build.py` | round 2: the `transmit-aged` control's anchor on `tx_owed` |
| `tb/verilator/ctrl_service_budget/declaring_outputs.py` | the arm's check: output 0's declared Talker notice to every registration, then its Listener's, before the first GET's response (`order_findings`, three planted orders in its self-test); REGISTERING required from the Listener's notices on. Before #957 the check required no notice there. |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 8x8/1if's own `record.maap` restated 180 to 185 us by the rule, its measurement recorded |
| `tb/verilator/ctrl_service_budget/flip_grade.py`, `shape_costs.py`, `talker_notice.py`, its README | texts: the hold-off counts THE TRANSMIT's figure |
| docs | `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/reference/FR_NFR.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (a new subsection in section 13) |

**Round 2, the corrections for R876-1 and R875-1** (both NEGATIVE at `0d80f0ed`):

- **A reset left a stale Listener record** (R876-1-F1, R875-1-F1). `reset_interface` destroys the participants and
  their Listener registrations with no indication, and kept `declaration[]`, so a registration after it that declared
  what the destroyed one did was not noticed. It now clears `declaration[k]` with `listener_present[k]`.
- **The latest case with lwSRP's join timer running** (R876-1-F2). THE TRANSMIT builds an interface's two MRPDUs in two
  slices at both points.
  - The count's end owes the pass that declares the changed destination. The join timer holds its MSRP MRPDU, and the
    timer's end, among the ticks a held loop dispatches before the second slice, set the interface's due again.
  - That due was set already, and the second slice's end cleared it. The declaration then waited for the next periodic
    MRPDU: 30.6 to 30.7 s after the request.
  - Now the pause takes the interface's due, and the paused build is THE TRANSMIT's due and the poll's owed (`tx_owed`,
    the due and `tx_resume` read whole). What came due since the first slice is owed again once the build ends, as after
    a build made whole.
  - A frame the ring refuses in the second slice keeps its interface due (A3).
  - At one interface the build's interface is 0 at compile time, as it always was there, which gives back 112 B of
    8x8/1if's `rom`.
  - At every withdrawal phase, each centisecond of a second, with the loop held or serviced, the changed destination
    is on the model's wire no later than 30.0 s after the request: held, at 29,995 ms (1x1/1if, 8x8/2if) and 29,997
    (8x8/1if).
- **Docs** (R876-1-F3, R875-1-F2 and -F3): FR_NFR's SRP row states the hold-off inside its two periods and its earlier
  figures as history; the SRP README states the ledger's rom figure.

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
- Round 2, SRP campaigns:
  - `talker-registration-kept-across-a-reset`: "the first Listener registration after a reset is noticed, whatever the
    one before it declared".
  - `talker-resume-drops-what-came-due` and `...-at-a-phase` (the sweep's `Held340`): "the changed destination reaches
    the wire no later than two of the longest LeaveAll periods after the withdrawal, at the latest".
  - `build-resumed-drops-what-came-due`: "a due set between a build's slices is owed once the build ends";
    `build-paused-keeps-its-due`: "a build with nothing due between its slices ends owing nothing";
    `build-paused-not-aged`: "a build resuming in the next slice is THE TRANSMIT's due"; `build-paused-unreported`:
    "the poll reports a build resuming in the next slice owed"; `build-refused-second-slice-not-due`: "a frame the
    ring refuses in a build's second slice leaves its interface due" (the two-interface campaign).
- Round 2, AECP campaign: `registration-notice-kept-across-a-reset`: "a Listener's return after a link reset is one
  notice of its STREAM_OUTPUT to every registered controller".
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

This form adds 40 bytes, all in `listener` (128 to 168 B at 8x8/1if): 139,248 B, 16 left. Round 2 adds the reset's
clear (4 B) and the sliced build's kept due; read as two bytes in `transmit_aged` and the poll it put the image over
its 58 RAMB36 (139,280 B), so they read `tx_owed` whole, and the one-interface build's interface fixed at compile time
leaves 139,136 B, 128 left. No budget moved.

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
# the CPU budget harness's legs the change reaches, base 0d80f0ed (round 1: 15168e14) and this head, at 1x1 and 8x8-1if:
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> \
  --groups srp,backlog-owed,aecp,datapath-events,aecp-largest-notice --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant valid-destinations \
  --groups srp-talker-held,srp-talker-loss --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --variant declaring-outputs \
  --groups aecp-outputs --record-budget-findings --record-share-findings
```

The round's new tests alone, at a point (the gate runs them at 1x1/1if, 8x8/1if and 8x8/2if, and AppOutputs at 1x1 at one
and two interfaces and 8x8 at one): `--gtest_filter='EveryPhase/*:Talker.ChangedDestinationReachesTheWire*:Talker.ListenerRegistrationAfterAResetIsNoticed'`
on `srp_talker.cpp`, `Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue` on `srp_mbx.cpp`, and
`AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` on the AECP app arm.

Expected result / pass criteria: every shard `test_ctrl_firmware: PASS` with no `ESCAPED` line (the new plants among
the `[ok]` lines); coverage `firmware coverage: PASS (40 files)`; every twin target rc 0; `plat_ledger: PASS (0
finding(s))`; every harness leg rc 0 with no row over its bound and its stated costs held.

## Known limitations / out of scope

- **The formal CPU measurement is not run.** At this host's load, a full pass of every arm and group at a point
  is about 70 core-hours, and no CPU range was bookable for it; one was started, then stopped. The legs the change
  reaches are measured instead, base against head (`author-r2/receipts/cpu-*-legs-0d80f0ed-vs-b4a1dde2.md`). At the
  final head, three measured costs sit at their statement by the rule, so a group not run could hold one over it:
  - `item.acmp_declined` at 1x1/1if and at 8x8/1if: 30 of 30 us.
  - `record.srp` at 8x8/1if: 35,507 cycles, 375 of 375 us.

  The others the change reaches are below their statements: `centisecond` at 1x1/1if 14,213 cycles, 150 of 170 us;
  `record.maap` at 8x8/1if 17,014 cycles, 180 of 185 us. (Round 1's head had `centisecond` 16,064 cycles at 170 of
  170 us, `record.srp` 35,273 and `record.maap` 17,259 at 185 of 185: history, superseded.) The full re-measure
  belongs to the next formal pass.
- **The rom at 8x8/1if** has 128 bytes left: the aligned `rom_end` is 139,136 of its ledgered 139,264 B (58 RAMB36 in
  all), a product image (`author-r2/receipts/rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt`; round 1's head had 16).
- **#957 depends on the DA gate.** The notice is raised while the output's DA gate is open, the face's "declaring".
  The `[A809] TAKEN` comment said it would not depend on the Talker's declaration. It changed for the rom, and because
  behind a closed gate the answer shows neither flag. Still as the release: a Ready replaced by a Ready Failed is
  noticed though the flags are the same.
- **A link reset itself records no Listener change.** It closes the output's declaration as for the Talker; #936
  records nothing there either. It clears each source's Listener declaration with the registrations it destroys, so
  the first registration after it is recorded whatever it declares (round 2, R876-1-F1 and R875-1-F1).
- **#956's lower bound** holds from a Leave request made on a centisecond. A request mid-centisecond makes the count's
  first centisecond partial, so the count can end up to 1 cs sooner (#895's mechanism, unchanged).
- **T_egress (1 ms) is not one of the hold-off's terms.** The round-up of THE TRANSMIT's term leaves 5, 3 and 5 ms at
  the three shapes, and from Leave to Talker on the wire it cancels.

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

