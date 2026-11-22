[A809] REVIEW READY
Commit: 1825ba4eaccfe40788391b7af5533fae8c910a85 (`pf-951-943n-1`, for `dev-soft-core`, PR #958). Round 2: the corrections for R876-1 (issuecomment-7069018804) and R875-1 (issuecomment-7069301447).
Code head `847b2e21`. It changes only a plant table after `b4a1dde2`: the firmware gate ran at `847b2e21`, and every other code gate at `b4a1dde2`, whose images are its images. `1825ba4e` is docs.

Findings, each at its cause:

- **R876-1-F1 and R875-1-F1 (MAJOR): a reset left a stale Listener record.**
  - Cause: `reset_interface` destroys the interface's participants and the Listener registrations they hold, with no indication. It cleared `listener_present[]` but not #957's `declaration[]`. So the first registration after the reset was compared with the destroyed one's declaration, and the same declaration recorded nothing.
  - Fix, `04819246` (`srp_mbx.c` `reset_interface`): `declaration[k]` is cleared with `listener_present[k]` (4 B at 8x8). The record then agrees with the answer, no Listener, and the first registration after the reset is recorded whatever it declares.
  - Tests:
    - `Talker.ListenerRegistrationAfterAResetIsNoticed` (`srp_talker.cpp`; 1x1/1if, 8x8/1if, 8x8/2if). It covers each of Asking Failed, Ready and Ready Failed, equal before and after; the link's edges apart, coalesced into one service, and twice over in one; the reset itself silent; an unchanged repeat silent; and the other interface's record kept and silent.
    - `AppOutputs.ListenerRegistrationAfterALinkResetIsItsStreamOutputsNotice` (`test_aecp.cpp`; 1x1/1if, 1x1/2if, 8x8/1if). It follows R875's order: link down, then up, MAAP valid, and the Talker declared again after its hold-off, with the answer showing no Listener. When the Listener returns, output 0 sends one notice to each of the two registered controllers, with REGISTERING and the right REGISTERING_FAILED, and no other output sends any. An unchanged repeat is silent, and the other interface's Listener is kept and silent. Each declaration is run with the edges apart and coalesced.
  - At `0d80f0ed` both fail: the SRP test 9 times at 1x1/1if and at 8x8/1if and 18 times at 8x8/2if, and the composed test with 12 notices missing at each of its three shapes.
  - Plants: `talker-registration-kept-across-a-reset` (both SRP campaigns) and `registration-notice-kept-across-a-reset` (AECP).
  - The reviewers' probes pass at `b4a1dde2`: R876's `reset_probe.cpp` at 1x1/1if, 8x8/1if and 8x8/2if, and R875's link-reset probe (notices 1/1, `flags_ex` 1) at 1x1/1if, 1x1/2if and 8x8/1if.
- **R876-1-F2 (MAJOR): the latest case with lwSRP's join timer running.**
  - Cause, traced at 300 ms, 1x1/1if (THE TRANSMIT builds an interface's two MRPDUs in two slices at both points):
    1. The count's end owes the pass that declares the changed destination.
    2. Its first slice builds the MSRP MRPDU, which lwSRP's join timer holds, since a periodic MRPDU left in the JoinTime before.
    3. The timer's end, among the ticks the held loop dispatches before the second slice, set the interface's due again. The due was already set, and the second slice's end cleared it.
    4. So the declaration waited for the next periodic MRPDU: 31,000 ms on the model's clock.
  - Fix in the code (`04819246`, `b4a1dde2`; `srp_mbx.c` `transmit`, `transmit_aged`, `poll`; `srp_mbx.h`). The timer state is not chosen, nothing is deferred, and the 30.0 s bound does not move.
    - The pause takes the interface's due.
    - The paused build is THE TRANSMIT's due and the poll's owed. `tx_owed` reads the due and `tx_resume` whole, in a union.
    - What came due since the first slice is owed again once the build ends, as after a build made whole. A build with nothing due between its slices ends owing nothing, what its own sends moved included.
    - A frame the ring refuses in the second slice stays the poll's with its interface due (A3). That corner was found in this round's own check and fixed in `b4a1dde2`.
    - At one interface the build's interface is 0 at compile time, as it always was there. That gives back 112 B of 8x8/1if's `rom`.
  - Tests:
    - `EveryPhase/TalkerPhase.ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriods/{Held,Serviced}{10..1000}`: 200 instances, every centisecond of a second with the loop held and with it serviced. It runs at 1x1/1if, 8x8/1if (a new `srp_talker.cpp` arm) and 8x8/2if.
      - It keeps the absolute bound: on the wire no later than 30,000 ms after the request, and no sooner than the hold-off.
      - Held, the destination leaves exactly as the loop resumes: 29,995 ms at 1x1/1if and 8x8/2if, 29,997 at 8x8/1if.
    - `Talker.ChangedDestinationReachesTheWireWithinTwoLongestLeaveAllPeriodsWithTheJoinTimerRunning`: the withdrawal at 340 ms, asserting every interface's join timer is running as the count ends. The 700 ms at-the-latest test keeps its idle-timer precondition.
    - `Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue` (four points): a build is due and owed while paused; a due set between the slices is kept; a build ends owing nothing when nothing came due; and a frame refused in the second slice leaves the interface due.
  - At `0d80f0ed`, the held sweep fails at 270 to 340 ms (1x1/1if), 310 to 380 (8x8/1if, which 100 ms sampling missed) and 340 to 410 (8x8/2if). Each fails at 31,000 ms on the clock, the next periodic MRPDU's: 30,660 ms request-to-wire at 340. The running-timer test and the unit test fail too.
  - Plants:
    - `talker-resume-drops-what-came-due` (the running-timer test) and `talker-resume-drops-what-came-due-at-a-phase` (`.../Held340`), in both SRP campaigns.
    - `build-resumed-drops-what-came-due`, `build-paused-keeps-its-due`, `build-paused-not-aged`, `build-paused-unreported` and `build-refused-second-slice-not-due` (the two-interface campaign).
    - The existing hold-off plants are kept and caught: #951's added terms, the terms dropped or rounded down, and a declaration a centisecond early. The at-the-latest test now uses a helper shared with the sweep, and its words are unchanged.
  - R875's phase probe passes at all three points, phases 100 to 900 held and free: at most 29,995, 29,997 and 29,995 ms. Phase 0 is its setup artifact, as its author says.
  - R876's `focused.py` phases mode cannot apply: it edits the old test body. The sweep runs that case every 10 ms.
- **R876-1-F3 and R875-1-F2 (MINOR): `FR_NFR.md:427`** (`578478bc`). The row now states 2,973 cs at 8x8/1if and the subtraction's direction: a longer row declares sooner, 10 ms sooner at two interfaces than at 99 ms, on the wire no later than 30.0 s. The earlier figures are marked as history (#951's 3,027; 2,026 and 2,027 before #951).
- **R875-1-F3 (MINOR): the SRP README's rom figure.** It now states the ledger's figure, 139,136 B at 8x8/1if with 128 B left (`plat_ledger.py`, which counts `rom_end`).

Changed (round 2):
- `sw/firmware/ctrl/srp/srp_mbx.c` and `.h`:
  - `reset_interface` clears `declaration[]` (#957).
  - `transmit`, `transmit_aged` and `poll`: the kept due, the paused build owed, the refused second slice's due, and the one-interface build's interface fixed at compile time (#956).
  - `tx_due` and `tx_resume` are a union with `tx_owed`. No struct grows at any point.
- Tests:
  - `srp_talker.cpp`: the latest case's `lapse` and `reaches_the_wire` helpers, the running-timer case, the `EveryPhase/TalkerPhase` sweep and the reset test.
  - `srp_arms.py`: an 8x8/1if `srp_talker.cpp` arm.
  - `srp_mbx.cpp`: the paused-build test.
  - `test_aecp.cpp`: the composed link-reset test.
  - `srp_app.cpp` and `srp_feedback.hpp` drive THE TRANSMIT while `tx_owed`, not `tx_due`, is nonzero. A paused build no longer shows in `tx_due`.
- Plants: `srp_talker_mutants.py` (3 rows), `srp_transmit_mutants.py` (5 rows; its anchors re-read for `tx_owed`) and `aecp_registration_mutants.py` (1 row).
- The CPU budget harness: `build.py`'s `transmit-aged` control re-anchored on `tx_owed`.
- Docs: `FR_NFR.md`, `sw/firmware/ctrl/srp/README.md` and `SPLIT_CONTROL_MEMORY.md` section 13.
- No RTL, mailbox-contract, lwSRP, bound or memory-budget change.

Validation (receipts in the author packet `round2/receipts/`; its `INDEX.md` lists them):
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

Acceptance criteria:
#956:
- `SRP_REDECLARE_CS` is derived from the named LeaveAll constant with both terms inside: met (unchanged from round 1).
- The tests are restated, declared at or after 29.x s and at or before 30.0 s on the model's wire: met, now at every withdrawal phase and join timer state.
  - Held: 29,995 ms at 1x1/1if and 8x8/2if, 29,997 at 8x8/1if.
  - Serviced: no sooner than the hold-off.
- A plant putting #951's value back fails by name: met.
- The bench measures 29 to 30 s at 1x1/1if and 8x8/1if: not done. It needs bench access.

#957:
- One unsolicited response with the new flags per registration change, at every output and both shapes, none when nothing changed: met, and now after a reset too. The first registration after a link reset is one notice to every registered controller.
- A test that fails on the current code: met. Both new reset tests fail at `0d80f0ed`.
- The CPU rows at 1x1/1if and 8x8/1if re-measured within their bounds: met on the legs the change reaches. The formal full pass is not run.

Open risks/questions:
- **The formal CPU measurement is not run.** The legs the change reaches are measured, base against head. `item.acmp_declined` sits at its statement at both points, as at `0d80f0ed`.
- **A due set between a build's two slices now owes one more build pass**, as after a build made whole. The legs' groups measure every build pass within its statement, but a group the legs do not run could hold a heavier one.
- **8x8/1if's rom** has 128 B left (16 at `0d80f0ed`).
- **8x8/1if's `record.srp`** measures 35,507 cycles, at its 375 us statement by the rule, about 200 cycles under the next 5 us step (35,273 before, also 375). A group the legs do not run could hold one over it.
- **The `srp-talker-held` leg at 8x8/1if ran twice.** The first run was stopped at a time limit of the author's environment, at about 82%; `srp-talker-loss`, complete in that run, is graded from its log. The held group then ran alone, on the same build, unbooked in its own unit, since no CPU range was bookable.
- R876's `focused.py` phases mode cannot apply to the restructured test. The sweep covers that case.

REVIEW READY 1825ba4eaccfe40788391b7af5533fae8c910a85
