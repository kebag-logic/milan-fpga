# HANDOFF r1: [A809], #956 and #957 (part of #665)

Status: ROUND 1 COMPLETE. Final head `0d80f0ed2a880c3a3b2429c669f104801203ec05`; code head `8845364d`. The one
`[A809] REVIEW READY` is posted on #956 (issuecomment-7068744003; text: `REVIEW-READY.md`); `PR-BODY.md` is for the manager (base
`dev-soft-core`). Nothing pushed.

Lane: `/data-2/milan/lanes/post-flip-fix`, branch `pf-951-943n-1`, on the flip train's head `15168e14` (PR #945,
reviewed, not yet merged into `dev-soft-core`). Public: `[A809] TAKEN` on #956 (issuecomment-7062425921), posted
after the first edits, not before them (a process slip, said here and in the REVIEW READY).

## Commits (oldest first)

| Commit | What |
|---|---|
| `f15c6e16` | #956 tests and plants restated (fail at the train's value) |
| `0369cbb7` | #956 fix: `SRP_REDECLARE_CS` counts both terms inside the two longest periods |
| `79fd3601` | #957 test, first form (fails at the train's code) |
| `6cbb545a` | #957 test restated: each output's Talker declaration held as it is (fails at the train's code) |
| `e6adad52` | #957 fix, first form (a comparison of what the output shows at each copy) |
| `76dcaac3` | #957 plants, first form |
| `5a0b320f` | #957 fix restated smaller (the declaration lwSRP indicates; a reset's mark), its plants restated |
| `803c014e` | comments and harness texts: the hold-off counts THE TRANSMIT's figure (#956) |
| `998412ff` | #957 final form: the change recorded in #936's `noticed` while the source's DA gate is open; the new delivery loop, the reset mark and `registration_noticed` gone; tests, plants and the SRP and AECP READMEs restated |
| `8845364d` | #957: `declaration[]` moved beside the other per-source byte arrays, so `struct ctrl_plat` keeps its ledgered size (the 1x1/2if `PLAT_1X1_2` KEY finding gone). **Code head: every code gate below ran here.** |
| `0818deb1` | docs: MAILBOX_SPLIT, FR_NFR, SPLIT_CONTROL_MEMORY section 13 |
| `b8890724` | harness: `declaring_outputs.py` expects output 0's Listener notice (the arm's check encoded the pre-#957 behaviour), `order_findings` with three planted orders in the arm's self-test; idiom fixes (`flip_grade.py` docstring rewrapped, `srp_talker_mutants.py`'s hold-off rows into `hold_off_defects`, the same 63 rows) |
| `03d9d519` | docs: the CPU legs in SPLIT_CONTROL_MEMORY section 13 |
| `5d8cfd62` | harness: 8x8/1if's own `record.maap` restated 180 to 185 us by the rule (`load_grade.OWN`, `OWN_MEASURED` 17,259 cycles in `srp-talker-loss`), and its record in the design page |
| `0d80f0ed` | docs: 8x8/1if's THE TRANSMIT row by every source with the restatement, 76.86 of 77 ms (final head) |

Why #957 changed form twice: the first form (a comparison of what the output shows at each copy, its own record and
a delivery loop) added 296 B of text at 8x8/1if and put the CPU budget harness's `declaring-outputs` image there over
its 32 RAMB36 of rom; the second (160 B) then put the target platform's 8x8/1if image over its ledgered 58 RAMB36
(`plat_ledger.py`: rom 139,360 B against 139,264), where the train's head leaves 56 B. The final form adds 40 B of
text there (rom 139,246 B, 18 B left). No budget is changed.

## Scope as implemented

- **#956** (owner decision 2026-11-21). `SRP_REDECLARE_CS` = 2 x `SRP_LEAVEALL_LONGEST_CS` - `SRP_JOIN_CS` -
  ceil(`CTRL_LOOP_TX_MS`/10): 2,977 cs at 1x1/1if, 2,973 at 8x8/1if, 2,970 at two interfaces (#951: 3,023, 3,027,
  3,030). The count still starts at the Leave's request (unchanged mechanism), so the changed destination is declared
  (TALKER_DECL) two longest periods less both terms after the request and is on the wire no later than 30.0 s after it.
  On the model's wire: declared at 29,770 / 29,700 ms after an aligned request, and at the latest (loop held a JoinTime
  and THE TRANSMIT's figure from the tick that ends the count) at 29,995 / 29,995 ms (1x1/1if / 8x8/2if).
- **#957**. SRP's `listener` indication records, in #936's `noticed`, each change of the Listener declaration lwSRP
  indicates for a source's stream (Ignore at a registration's end) while the source's DA gate is open on that
  interface; the composition and the AECP bridge take it as they take a Talker declaration's change, one unsolicited
  GET_STREAM_INFO of the output to every registered controller. The gate is what the face reports as the output
  declaring, and MAAP opens it on the source's own interface only, so a Listener on another interface, or behind a
  closed gate (where the face shows neither flag), records nothing. Like the release's LISTENER_REG_CHANGE, a Ready
  replaced by a Ready Failed is noticed though the flags are the same. Changed from the TAKEN's stated assumption
  ("does not depend on the output's Talker declaration"): it now depends on the DA gate, the face's declaring, for
  the ROM reason above and because behind a closed gate nothing the output shows changes. A link reset is not
  recorded (it closes the output's declaration, as for the Talker; #936 records nothing there either).

## Changes (file:line at `8845364d`, reason)

- `sw/firmware/ctrl/srp/srp_mbx.c:40-47` - #956: `SRP_REDECLARE_CS` = 2 x `SRP_LEAVEALL_LONGEST_CS` - `SRP_JOIN_CS` -
  ceil(`CTRL_LOOP_TX_MS`/10), its comment stating both terms counted inside the two periods (owner's decision of
  2026-11-21). The count's start (the Leave's request) and mechanism are unchanged.
- `sw/firmware/ctrl/srp/srp_mbx.c:205-214, 228-229` - #957: `listener` records a change of the indicated Listener
  declaration, while the source's DA gate is open on the interface, in `noticed` (#936's record), and copies it.
- `sw/firmware/ctrl/srp/srp_mbx.h:62-65` - #957: `declaration[CTRL_SRP_SOURCES]`, beside the per-source byte arrays
  (padding: no struct grows at any platform point); `:102-104` the `noticed` comment names the Listener change.
- `sw/firmware/ctrl/app/ctrl_app_aecp.c:236-239` - comment: the bridge's notice also covers the Listener change.
- `sw/firmware/ctrl/loop/ctrl_loop.h:349-351, 495` - comments: the hold-off counts THE TRANSMIT's figure.
- Tests: `srp_talker.cpp:52-65` (constants), `:301` `ChangedDestinationWaitsTwoLongestLeaveAllPeriods` (restated),
  `:362` `ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest` (replaces
  `...AfterTheLatestLeave`), `:403` `DestinationChangeWhileValidWithdrawsTheOld` and `:504`
  `ResetKeepsAnUnchangedSourceAndHoldsAMovedOne` (restated bounds), `:788` `ListenerRegistrationChangeIsNoticed`
  (new); `srp_gate.hpp:318` `F895ARangeLost...` (held at 29 s, on the model's wire by 30 s); `test_aecp.cpp:966`
  `AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice` (new; the fixture's entity claims a MAAP address of
  every output).
- Plants: `srp_talker_mutants.py` (hold-off rows restated, five new #956 rows, five #957 rows),
  `aecp_registration_mutants.py` (new, three rows) wired into `aecp_mutants.py`.
- Docs: `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, harness texts (`flip_grade.py`,
  `shape_costs.py`, `talker_notice.py`, `ctrl_service_budget/README.md`); pending commit: `docs/design/MAILBOX_SPLIT.md`,
  `docs/reference/FR_NFR.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` (new subsection under section 13).

## New checks (planted mutant, failing words)

#956 (srp_talker_mutants.py; SRP campaign, 1x1/1if and 8x8/2if, all caught in the scratch campaign):
- `talker-hold-off-adds-its-terms` (#951's value) -> `Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriods`:
  "the changed destination reaches the wire no later than two of the longest LeaveAll periods after the withdrawal"
- `talker-hold-off-adds-its-terms-at-the-latest` (#951's value) ->
  `Talker.ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsAtTheLatest`: "... after the withdrawal, at
  the latest"
- `talker-hold-off-adds-its-terms-after-a-conflict` (#951's value) -> `SrpGate.F895ARangeLost...`: "the new range's
  destination reaches the wire within two of the longest LeaveAll periods of the conflict"
- `talker-hold-off-a-centisecond-short` -> CHANGED: "TALKER_DECL holds a changed destination withdrawn while it waits"
- `talker-hold-off-takes-its-terms-twice` -> CHANGED: "no Talker of a changed destination is declared before the
  hold-off ends"
- restated: `-drops-the-transmit-term`, `-rounds-the-transmit-term-down` (LATEST, "... at the latest"),
  `-drops-the-join-and-transmit-terms` (CHANGED, "a changed destination is declared two of the longest LeaveAll periods
  less a JoinTime and THE TRANSMIT's term after its Leave's request"), `-two-leavealltime-periods[-after-a-conflict]`
  (now the pre-#951 value as it was, both terms added), `talker-lapse-starts-no-hold-off` (new words).

#957 (srp_talker_mutants.py, SRP campaign at 1x1/1if and 8x8/2if; aecp_registration_mutants.py, AECP campaign at
1x1/2if):
- `talker-registration-unrecorded` -> `Talker.ListenerRegistrationChangeIsNoticed`: "a Listener Ready appearing is noticed"
- `talker-registration-unchanged-recorded` -> same: "a Listener declared New again unchanged is not noticed"
- `talker-registration-declaration-uncopied` -> same: "a Listener declared New again unchanged is not noticed"
- `talker-registration-reset-unrecorded` -> same: "a reset with a Listener registered notices it going"
- `talker-registration-reset-declaration-kept` -> same: "a Listener registering again after a reset is noticed"
- `talker-registration-reset-every-source` -> same: "a reset with no Listener registered notices nothing"
- `registration-notice-not-taken` -> `AppOutputs.ListenerRegistrationChangeIsItsStreamOutputsNotice` and
  `App.NoPassIsIdleWhileAListenerRegistrationNoticeIsOwed`
- `registration-notice-any-interface` -> both: "a Listener on another interface notifies nothing" / "a record on
  another interface than its source's notifies nothing"
- `registration-notice-record-kept` -> AppOutputs: "a Listener registration change is one notice of its STREAM_OUTPUT
  to every registered controller"
- `registration-notice-owed-unreported` -> App: "no pass is idle while a Listener registration's notice is owed"

## Gate table

| Gate | Head | Result | Receipt |
|---|---|---|---|
| #956 tests fail at the train's value | `f15c6e16` | FAIL as required (4 Talker tests at both shapes, the composed test) | `956-tests-fail-at-train-value.txt` |
| #957 test fails at the train's code | `79fd3601` / `6cbb545a` | FAIL as required (1x1 1if, 1x1 2if, 8x8 1if) | `957-test-fails-at-train-code.txt` |
| #957 final tests fail at the train's firmware | `8845364d` tests, train's `srp_mbx.c/h` | FAIL as required (AppOutputs 1x1 1if/2if, 8x8 1if; Talker 1x1/1if, 8x8/2if) | `957-final-tests-fail-at-train-firmware.txt` |
| Firmware gate shard 0 (suites) | `8845364d` | PASS, 75 verdicts | `fw-gate-shard0-8845364d.txt` |
| Firmware gate shard 1 (control plants) | `8845364d` | PASS, 826 caught, 0 escaped | `fw-gate-shard1-8845364d.txt` |
| Firmware gate shard 2 (AECP plants) | `8845364d` | PASS, 388 caught, 0 escaped (the 3 #957 rows among them) | `fw-gate-shard2-8845364d.txt` |
| Firmware gate shard 3 (SRP plants, pins) | `8845364d` | PASS, 563 caught, 0 escaped (36 hold-off and registration rows: 18 at each campaign) | `fw-gate-shard3-8845364d.txt` |
| fw_coverage --selftest, --check | `8845364d` | PASS (29 of 29 planted cases; 40 files) | `fw-coverage-8845364d.txt` |
| twin, twin-plants, twin-maps, twin-maps-plants | `8845364d` | PASS (rc 0 each) | `twin-8845364d.txt` |
| platform ledger and the size fixture's images | `8845364d` | PASS (0 findings; 8x8/1if rom 139,248 B of 139,264) | `images-15168e14-vs-8845364d.txt` |
| image diff, 20 images | `15168e14` vs `8845364d` | `listener` +40 B only; at 8x8 three objects differ in field offsets | `images-...txt`, `imgdiff/` |
| release (all-fabric) image | `15168e14` vs `8845364d` | byte-identical but LiteX's per-run time stamps and CPU netlist name | `release-image-15168e14-vs-8845364d.txt` |
| docs workflow steps | `0818deb1` | one step FAILED: `check_py_idiom.py` (a long function, an over-long line), fixed at `b8890724` | (superseded) |
| docs workflow steps | `03d9d519` | PASS, 104 of 104 (superseded) | |
| docs workflow steps | `0d80f0ed` | PASS, 104 of 104, tracked files unchanged | `docs-steps-0d80f0ed.txt` |
| end-station builder legs 0 and 1 | `5d8cfd62` (and `03d9d519`) | PASS each: `ALL GATES PASS EXCEPT 1 NOT RUN` (leg 0's MAKEFLAGS mutation arm; leg 1's calibration gate, no real report on this host). First try refused before any gate: the clone's submodule origins were local, synced to `.gitmodules` | `builder-legs-5d8cfd62.txt` |
| CPU budget harness self-test (`run.py --self-test`) | `5d8cfd62` (and `b8890724`) | PASS, 0 failures (the 3 new order controls among them) | `harness-selftest-5d8cfd62.txt` |
| CPU budget, the legs the change reaches, base vs head, 1x1/1if | `8845364d` (regrade at `b8890724`) | PASS: 68 probes paired, 0 verdicts changed, the 7 known misses each side, 66 statements within | `cpu-1x1-legs-15168e14-vs-8845364d.md` |
| CPU budget, the same at 8x8/1if | `8845364d` (regrade at `b8890724`) | PASS: 85 probes paired, 0 verdicts changed, the 7 known misses each side, 66 statements within, the largest legal notice within | `cpu-8x8-1if-legs-15168e14-vs-8845364d.md` |
| CPU budget, `srp-talker-loss` (the train's `record.maap` maximum at 8x8/1if came from it), both points | head rebuilt at `b8890724`, image identical | PASS legs (0 verdicts changed); 8x8/1if `record.maap` 17,259 cycles, 185 us by the rule over its 180: restated at `5d8cfd62` (a statement, not a bound; load 0.744/0.75 and tx row 76.86/77 ms still pass) | in the two `cpu-*` receipts |
| tree checks: `load_grade.py --check`, `flip_grade.py --check --point 1x1/1if` and `8x8/1if`, `shape_costs.py --check` | `5d8cfd62` | PASS (and `flip_grade.py --check` at every point FAIL at base and head alike, 8x8/2if reported, owed to #872) | `tree-checks-5d8cfd62.txt` |
| CPU budget, the formal measurement (every arm and group) | - | NOT RUN: about 70 core-hours a point at the host's load, no range bookable for it; started, then stopped | |

## Found beside it (not changed; for a new Issue)

- In the model, with the loop held across the tick that ends the hold-off while lwSRP's join timer still ran,
  THE TRANSMIT's resume slice (CTRL_LOOP_BUILD_MOST 1, 8x8/2if) cleared interface 0's due after its MSRP build had been
  refused by lwSRP's join timer, and the join timer's expiry, dispatched between the slice and its resume, was lost:
  the changed destination waited for the next periodic transmission (over 400 ms). Seen only under the burst of
  caught-up ticks a held loop gives; not shown reachable in real time. The at-the-latest test places its withdrawal so
  the join timer is idle as the count ends, and asserts that precondition.

## Where the evidence is

- Receipts: `receipts/` (INDEX.md generated from the files present). Per-image diffs: `receipts/imgdiff/`.
- Scratch (not public): the measurement trees, logs and tools are in the lane's scratch directory; nothing in the
  packet depends on them.

## Open risks / questions

- The lower bound "two longest periods less both terms" holds from a Leave request made on a centisecond; a request
  mid-centisecond makes the count's first centisecond partial, so the count can end up to 1 cs sooner (the mechanism
  is #895's, unchanged). The tests align the request and state this.
- T_egress (1 ms) is not one of the terms; the round-up of THE TRANSMIT's term leaves 5, 3 and 5 ms at the three
  shapes, and wire to wire it cancels.
- The formal CPU measurement (every arm and group) is not run: about 70 core-hours a point at the host's load, no
  range bookable. Three measured stated costs sit at their statement by the rule: `centisecond` 1x1/1if 170/170,
  `record.srp` 8x8/1if 375/375, `item.acmp_declined` 8x8/1if 30/30.
- The 8x8/1if product image has 16 bytes of rom left in its ledgered 58 RAMB36.
- #957 follows the DA gate (the face's "declaring"), changed from the TAKEN's "whatever the Talker's declaration".
- The bench measurement of #956's acceptance (29 to 30 s at both points) is not done (no bench access).
