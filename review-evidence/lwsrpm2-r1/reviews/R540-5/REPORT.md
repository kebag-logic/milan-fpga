[R540] NEGATIVE - exact head a29f8d13ff4869e54997d9adf05d83a4ace4b8bd

# R540-5 internal review: kebag-logic/lwSRP PR #12 (issue #10), round 6

- Exact head `a29f8d13ff4869e54997d9adf05d83a4ace4b8bd`, tree `dfff72e82034986739d9f8641a820a0d76ea6dd1`.
- Delta: one commit on `0a45695d` ("Preserve pending Flush withdrawals across receive dispatch"). Full PR range `1401654530ce7d9275de9b901e67df47e5bbc536..a29f8d13`.
- Review start: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035919431.
- Assignment: "Round 6 for [A563]" (lwSRP #10 comment 6035585910).
- Paths in receipts use `$PACKET` (this packet) and `$CLONE` (the detached review clone).

## Verdict

NEGATIVE: one MINOR finding (Tests) is open.

All five round-6 items are resolved at their root:

- R541-4-F1: the pending Flush is kept across receive dispatch.
- R541-4-F2: the next-tick regression now rejects a two-tick delay.
- R540-4-01: the observer sees the retained IN to LV change.
- R540-4-02: replacement from LV is tested in both directions, at all nine allocation positions, in both profiles.
- R540-4-03: fault position 1 and the `rc->error` reversal are present.

The production code behaves correctly in every case I probed.

The remaining finding is a coverage gap in the new pending-flag lifecycle. The flag has two completion routes: receive and timer. Only the receive route is pinned. A mutant that clears the flag only on the Flush event builds and passes all 81 tests and all 88 reversals in both profiles. It causes a spurious Leave and Join on the first refresh after a timer-completed Flush.

## Findings

### R540-5-01 - MINOR - Tests

- **Where:**
  - `src/core/mrp_mad.c:663-665`: `reg_event` clears `flush_pending` on any successful Leave indication.
  - `src/core/mrp_mad.c:864-873`: `on_leave_timer` completes a pending Flush on the default first-tick route through `MRP_EVENT_LEAVETIMER`.
  - `tests/unit/review_test.c:646-692` (`flush_allocation_failures_retry_withdrawal_on_the_next_tick`) and `:955-986` (`failed_flush_reports_continuous_observer_transitions`, `receive=0`): after timer completion, they deliver at most one received registration and then stop.
  - `tests/unit/review_test.c:849-915` (`flush_before_receive`): it completes the withdrawal through receive, not through the timer, before its follow-up receive.
  - `tests/check_reversals.py:173` (`flush-completion`): it removes clearing on both routes, so tests on the receive route alone kill it.
- **Authority:**
  - Issue #10 acceptance 2: every new behaviour has a test that fails when it is reverted.
  - Round 6 item 1: keep ordinary unchanged LV recovery intact, with named fault-port regressions and a discriminating reversal.
  - `src/include/shish_lan/mrp.h:281-282`: "Once Leave succeeds, the new registration can issue its own indication." "Ordinary LV recovery without pending Flush retains the table behavior."
  - `doc/developer.md:295` and `doc/integrator.md:229` say the same.
- **Evidence:**
  - Plant `clear-only-on-flush-event` changes `if (e->ind == REG_IND_LV) {` to `if (e->ind == REG_IND_LV && ev == MRP_EVENT_FLUSH) {`. Both profiles build it, and all 81 tests pass (16314 and 16302 assertions). See `receipts/plants/clear-only-on-flush-event.unit-{OFF,ON}.log` and `receipts/plants_r5.json`.
  - None of the 88 repository reversals is this mutation.
  - Reviewer probe case `timer_completion` (`scripts/probe_r5.c`): fail the Flush, then tick once, then receive three unchanged JoinIn refreshes. It covers all three stream types, from IN and from LV.
    - At head, port 0 indicates exactly `L J`, and all 243 checks pass in both profiles (`receipts/probe-head-{0,1}.log`).
    - Under the plant, all six cases fail in both profiles with `L1:100 J1:100 L1:100 J1:100` (`receipts/plants/clear-only-on-flush-event.probe-{OFF,ON}.log`).
  - Mechanism: after a timer-completed Flush the flag stays set. The next receive delivers Flush to MT, which has no effect, and then Join. The refresh after that delivers Flush to IN, which indicates Leave, and then a new Join.
- **Impact:**
  - The default recovery route of the new mechanism can regress silently.
  - The host would then see an extra stream withdrawal and re-registration on the first refresh after any recovered Flush. That withdrawal also propagates to the destination ports.
  - The code at this head is correct. The finding concerns regression coverage only.
- **Required outcome:**
  - Add a regression that completes a failed Flush on the timer. It should then receive at least two registrations of the same attribute and assert exactly one Leave and one Join, with no later indication. Cover both profiles.
  - Add a named reversal that fails this regression in both profiles. Example: `('flush-timer-completion', MAD, '    if (e->ind == REG_IND_LV) {', '    if (e->ind == REG_IND_LV && ev == MRP_EVENT_FLUSH) {', 'unit')`.
  - Align the `doc/tester.md` coverage sentences and counts with the added test.
- **Verification:**
  - `python3 scripts/plants_r5.py --only clear-only-on-flush-event ...` must report a unit rc of 1 with the new named test in both profiles.
  - `scripts/run_probe.sh` must still pass at the new head.
  - The repository reversal driver must report the new case KILLED in both profiles.

### Suggestions

- **R540-5-S1 (SUGGESTION, Tests):** opposite-Talker replacement is not pinned while the old Talker has a pending Flush.
  - Plant `replacement-skips-pending` adds `!old->flush_pending` to the replacement condition at `src/core/mrp_mad.c:1026`. It passes all unit tests in both profiles.
  - The reviewer probe fails 20 of 20 cases per profile under this plant: the new Join is indicated before the old Leave (`J2:100 L1:100`). See `receipts/plants/replacement-skips-pending.probe-*.log`.
  - At head, all 20 cases, both directions and faults 0-9, give Leave before Join.
  - Consider starting one replacement case from a Flush-pending LV.
- **R540-4-S3 (SUGGESTION, retained):** the Flush LeaveAll request (`src/core/mrp_mad.c:1133`) predates this PR and still has no killing test. Plant `flush-leaveall-request` passes in both profiles. The PR body acknowledges this gap.

No RESIDUE is open at this head.

## Round-6 items verified at root

| Item | Result | Evidence |
| --- | --- | --- |
| R541-4-F1: a failed Flush stays pending across receive, and Leave precedes a later Join | RESOLVED | See below. |
| R541-4-F2: the retry regression rejects a two-tick delay | RESOLVED | See below. |
| R540-4-01: the observer sees the retained IN to LV change | RESOLVED | See below. |
| R540-4-02: replacement from LV, both directions, every fault, both profiles | RESOLVED | See below. |
| R540-4-03: fault 1 in the stop regression and the `rc->error` reversal | RESOLVED | See below. |

### R541-4-F1

- **Code:**
  - On a failed Flush reservation, `src/core/mrp_mad.c:645-650` sets `flush_pending` and LV and arms 1 cs.
  - On receive, `:995-1003` delivers Flush with the saved value before `get_or_create_attr` can refresh it. On failure, it sets `rc->error` and stops.
- **Reviewer probe** (243 checks per profile, both profiles, address and undefined-behaviour instrumentation, zero live allocations). These sequences all give one Leave with the old value before the Join or New:
  - New, JoinIn and JoinMt;
  - LeaveAll and JoinIn in one message;
  - Mt, Lv and In events;
  - a second Flush;
  - Re-declare;
  - reclaim;
  - opposite-Talker Join at faults 0-9;
  - a Join reservation failure followed by a stale timer;
  - two pending attributes in one payload.
- **Allocation bounds:** the Flush uses exactly 3 reservations. A pending receive uses 6. Replacement from IN or LV uses 9. Fault positions above these bounds inject nothing, so the sweeps are complete (`bounds()`).
- **Prior external probes at this head:**
  - `probe_r4.c` passes 6576 checks with 0 failures and 0 live allocations per profile.
  - `probe_r4_native.c` reports 0 interleave failures per profile.
  - Both files match the provenance hashes (`receipts/prior-probes/`).
- **Reversals:** `pending-flush`, `flush-before-refresh` and `flush-completion` fail their named tests in both profiles (`receipts/new-reversal-named-failures.txt`).
- **Ordinary LV recovery is intact:**
  - `registrar_recovery_stops_aging_without_duplicate_join_or_map` passes.
  - Plant `flush-every-lv-recovery` is killed by it and by 14 other tests.

### R541-4-F2

- Reversal `flush-deadline` arms 2 cs on Flush. It fails `flush_allocation_failures_retry_withdrawal_on_the_next_tick` in both profiles.
- My plant `timer-path-two-tick` arms 2 cs on the leave-timer retry. It is killed by the same test, which asserts `allocation_failures() == 1` on every failed tick.
- My plant `flush-no-timer` is also killed.

### R540-4-01

- `src/core/mrp_mad.c:730` now calls `observe` on the error path.
- Reversal `flush-observer` fails `failed_flush_reports_continuous_observer_transitions` in both profiles.
- `probe_r3.c` from R540-4 reports 114 Flush cases with 0 observer gaps and 5934 checks with 0 failures per profile.
- My `observers()` cases cover timer, receive, and failed-receive recovery, at faults 1-3. They show zero gaps.

### R540-4-02

- `replacement_from_lv_keeps_leave_before_join_at_every_allocation` (`tests/unit/review_test.c:803`) enters LV through a received LeaveAll. It runs both directions at faults 0-9 and asserts that each fault is reached. Nine is the full allocation count.
- `replacement-lv` and `replacement-leave-timer` fail that named test in both profiles. In the enabled profile, it is the only failing test, so it discriminates.

### R540-4-03

- `reservation_failure_stops_later_receive_messages` (`:987`) now sweeps faults 1-4 and asserts that each is reached.
- `receive-instance-stop` fails it in both profiles.

## Prior public findings at this head

I read the earlier public reviews after my independent pass.

| Prior finding | State at this head | Evidence |
| --- | --- | --- |
| R541-4-F1 (MAJOR) | RESOLVED | See the R541-4-F1 section above. |
| R541-4-F2 | RESOLVED | See the R541-4-F2 section above. |
| R540-4-01, R540-4-02, R540-4-03 | RESOLVED | See the sections above. |
| R540-4-S1: LeaveAll applied after a failed pass | RESOLVED (documented) | `doc/developer.md:288` and `doc/integrator.md:221` state it. `probe_r3` info line: the identical retry converges. |
| R540-4-S2: receive before tick cancels the retained Flush | Superseded by F1 and RESOLVED | The pending flag yields Leave then Join. |
| R540-4-S3: Flush LeaveAll request | RETAINED as SUGGESTION | Plant `flush-leaveall-request` survives. |
| R541-3-F1 / R540-3-01, R540-3-02, R540-3-03, R540-2-*, R541-2-*, R541-1-*, R540-1-* | RESOLVED (retained) | Every corresponding reversal is still killed: 88/88 per profile, and the restored build and check return 0 (`receipts/jobs/rev-*.log`, `receipts/reversals-*-commands.json`). |
| R538-2-R2 and R538-2-R3 (carried residues) | RESOLVED | `doc/tools/README.md:31` and `doc/manager.md:91-92` contain the exact text. |

## Lens results

### Conformance - CLEAN

- The default Registrar table, the Milan IN and rLv cell, and the parser are unchanged.
- With allocation available, Flush follows Table 10-4 Flush!: Lv, then MT.
- Under exhaustion, the delivered sequence equals the table result of an immediate Flush followed by the received event. That is Leave, then Join or New, with the saved value.
- 35.2.6 replacement keeps Leave before Join in both profiles. This includes a Flush-pending old Talker.
- The exhaustion policy is outside the standard. It is documented in `mrp.h:278-282` and `:351-356`, `doc/developer.md:291-298`, `doc/integrator.md:224-230` and the 10.7.8 row of `doc/manager.md:23`.
- The contribution rules hold:
  - one-line commit subject with no body or trailer, and the configured identity;
  - braces on every changed C guard;
  - no typedef enum;
  - the SPDX identifier in all 60 tracked files.

### RTL - CLEAN

- The repository has no HDL (0 files, `receipts/tools.txt`), so the pinned simulator was not needed or used.
- I applied this lens to the target-facing build:
  - the embedded source-list link and dispatch probes pass in both profiles (`receipts/jobs/embedded.log`);
  - the freestanding checks pass in the default and Milan settings (`receipts/jobs/free-*.log`);
  - the delta adds one `bool` per attribute instance and no allocation;
  - the retry reuses the existing per-attribute timer.

### Robustness - CLEAN

- The unit suites pass in both profiles with address, undefined-behaviour and leak instrumentation, and report nothing (`receipts/asan/`).
- The reviewer probe runs with the same instrumentation. It has zero live allocations after every teardown, including destroy with a pending Flush.
- A Flush-pending attribute is not reclaimed.
- A stale 1 cs timer after a receive-completed Leave produces no duplicate.
- Repeated refusal keeps the saved value and state.

### Tests - UNCLEAN (R540-5-01)

- Both profiles at head (`receipts/profile-{OFF,ON}/`):
  - configure, build, ctest (1/1), the unit runner, behave and the behave dry run all return 0;
  - 81 tests in 8 suites: 16314 assertions (default) and 16302 (enabled);
  - behave: 1 feature, 3 scenarios, 10 steps.
- The isolated codec command: 9 tests, 1690 assertions, rc 0 (`receipts/codec.txt`).
- I ran the full repository reversal driver in both profiles: 88/88 killed, and the restored build and check return 0.
- The 8 new reversals fail their required named tests (`receipts/new-reversal-named-failures.txt`).
- Reviewer plants: 18 plants, each in both profiles, for 36 runs (`receipts/plants_r5.json`).
  - 28 runs are killed by the suite.
  - These survive:
    - `clear-only-on-flush-event`, a real gap (R540-5-01);
    - `replacement-skips-pending`, a gap (R540-5-S1);
    - `retry-only-declarations`, equivalent under the contract: non-declaring events neither refresh nor register, and the withdrawal still completes on the next tick;
    - `flush-leaveall-request`, which predates this PR (R540-4-S3).
- The prior internal and external probes pass at head in both profiles.
- UNCLEAN because of R540-5-01.

### Docs - CLEAN

- All documentation checks return 0 (`receipts/docs/`):
  - 960 sentence fragments, none over 25 words;
  - 0 unlinked references;
  - 79 reference self-tests pass;
  - 354 local links and 20 external URLs pass with authenticated repository access;
  - 27 graphs render, the largest with 12 nodes.
- I rendered and viewed the changed retry graph. Its labels are readable and its layout is clear. It matches the code: the flag is cleared before the Leave indication, and retry happens on a tick or a receive.
- All 43 source-anchor occurrences land on their named code: `mrp_transmit`, `mrp_reclaim`, `deliver_event`, `rx_on_leaveall`, `la_event`, `leaveall_draw`, `pt_event`, `mrp_set_periodic`, `mrp_app_destroy`, the table rows, `msrp.c` L138 and L415, and the step lines.
- These counts are correct: README, `doc/manager.md` and `doc/tester.md` (81 tests; 16314 and 16302 assertions; 88 reversals), and the PR body validation list.
- The new prose follows the owner's rules. The interface comment and the guides agree on the pending-flag contract.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `reg_event`, `deliver_event_changed`, `rx_on_attr`, `on_leave_timer` and the replacement loop, against Table 10-4 Flush!, leavetimer! and rJoin rows and 35.2.6. Interface contract and guides. Commit format, braces, enums, SPDX. | R540-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| RTL | CLEAN | No HDL (0 files). Embedded source-list link and dispatch in both profiles. Freestanding checks in both settings. Storage and timer use of the delta. | R540-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Robustness | CLEAN | Pending Flush across receive, timer, second Flush, Re-declare, reclaim, destroy and replacement. Repeated refusal, saved values, stale timers, observer continuity. Instrumented unit suites and probe in both profiles. Prior internal and external probes. | R540-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Tests | UNCLEAN (R540-5-01) | ctest, unit, behave and dry run in both profiles. Codec, embedded and freestanding commands. 88/88 reversals per profile, with named failures for the new cases. 36 plant runs. Reviewer probe with 243 checks per profile. `tests/unit/review_test.c` delta, `fault_alloc.{c,h}`, `tests/check_reversals.py`. | R540-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Docs | CLEAN | README.md, CONTRIBUTING.md, `doc/*.md`, `doc/tools/README.md`, `mrp.h` contract comments. Five doc checks, rendered retry graph, 43 anchors, SPDX, PR body figures, carried residues. | R540-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |

## Real limits

- Hosted CI has zero check runs and zero statuses at this head, and the repository has no workflow (`receipts/hosted-checks.txt`). All execution evidence here is local.
- The assignment states that the manager's full source static, builder and native banks passed at this head. I did not rerun them, as assigned.
- I built the unit framework (1.6.3, commit `abb74b39`) from source in scratch. Host tools are listed in `receipts/tools.txt`.
- I could not read the IEEE or Milan texts. My clause readings follow the frozen assignment and the in-repo tables.
- My probe uses handcrafted MSRP payloads and the real stream application on three ports with a fixed propagation mask.
- One case is out of scope. A local `mrp_mad_join` with the same identity overwrites the shared value slot, including on a Flush-pending attribute. This predates the delta and was not probed.
- Plants are single-change host runs.
- No Zephyr, target, hardware or network run was done. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Carry R540-5-01 to the author: add a regression and a named reversal in both profiles. Consider R540-5-S1 and R540-4-S3.
- Build and judge the final current-dev merge candidate separately from this source validation. The source base is `1401654530ce7d9275de9b901e67df47e5bbc536` and live dev is `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- Own hosted and act acceptance. None ran here.
- The pinned evidence commit `eb9c5a65` does not contain `author-r6/`. I read the round-6 packet at evidence commit `efd32b2a79d19f1e6dc672049b4dbcf3f25ff73b`, branch `lwsrpm2-review-evidence`. Cite that commit, or its successor, when publishing.

R540-5 FINISHED
