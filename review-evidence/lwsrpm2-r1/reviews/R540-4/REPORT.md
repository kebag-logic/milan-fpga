[R540] NEGATIVE - exact head 0a45695db537badb8d7e9cbf578925fe5b89d647

# R540-4 internal review: kebag-logic/lwSRP PR #12 (issue #10), round 5

- Exact head `0a45695db537badb8d7e9cbf578925fe5b89d647`, tree `6d663f9b08d92b1e1b7202ce159b9e8e391d5f56`.
- Delta reviewed: `82422d6f..0a45695d`. It is one commit with a one-line subject, no body or trailers, the configured identity, and parent `82422d6f` (no rebase or amend).
- I used the full PR range `1401654530ce..0a45695d` for SPDX, braces, anchors and residue checks.
- Scope was read in this order:
  - `CONTRIBUTING.md` (there is no `AGENTS.md`), `README.md`, `doc/` and `doc/tools/README.md`;
  - the issue #10 body and every manager comment, including the Round 5 assignment (comment 6034815912) and the REVIEW READY comment (6035110842);
  - the PR body and the review-start comment (6035127867);
  - interfaces: `src/include/shish_lan/mrp.h`, `msrp.h`, `src/ports/alloc.h`, `src/ports/timer.h`;
  - the diff and history;
  - public evidence. The pinned evidence commit `eb9c5a65` holds only the round-1/2 author packet. The `author-r5/` packet is on milan-fpga branch `lwsrpm2-review-evidence` at `0c632696`. I hashed the five round-5 files I read (`receipts/author-r5-evidence.sha256`, `receipts/evidence-availability.txt`).
- I wrote my verdict and ledger before reading any prior review report (`receipts/own-pass-ledger.md`, 2026-10-07T09:47:24Z). I then read R540-3 (6034569438) and R541-3 (6034811505). I read the earlier rounds' finding headings only to list their IDs.
- After all probes, the clone matches the exact head (`receipts/integrity.txt`):
  - head, tree and index tree match;
  - status is empty, including ignored and untracked files;
  - all 60 tracked blobs match in bytes and mode;
  - there are zero gitlinks, and none are required.

## Verdict

NEGATIVE.

All three Round 5 items are resolved at their root. My own probe and plants confirm each one in both profiles:

- **R541-3-F1 / R540-3-01 (Flush):** a failed Flush reservation now keeps the withdrawal in LV with a 1 cs Leave timer.
  - My probe swept every fault position, one-shot and persistent (held 0 to 3 ticks), from IN and LV, with one and two attributes. That is 114 cases per profile. Each case gives exactly one Leave, MT at the source, withdrawn declarations on both destinations, a correct Join on re-registration, and zero live allocations.
  - The same probe fails 570 Flush checks per profile at `82422d6f`.
  - The named reversal `flush-retry` fails `flush_allocation_failures_retry_withdrawal_on_the_next_tick` (48 failures) in both profiles.
- **R540-3-02 (replacement order):** a failed replacement now stops before the new event.
  - The probe swept faults 0 to 11 in both directions, from IN and LV, one-shot and persistent, with an immediate retry or a tick before the retry. That is 184 cases per profile. Every case has Leave before Join, one indication each, and correct destination state.
  - The same probe fails 48 ordering checks per profile at `82422d6f`.
  - The reversal `replacement-order` fails its named test in both profiles.
- **R540-3-03 (y01, y02, y07):** my own versions are killed by the named tests in both profiles:
  - `y01` by `reservation_failure_stops_later_receive_messages`;
  - `y02` and `y02b` by `propagation_obeys_talker_and_listener_policy_masks`;
  - `y07` and `y07b` by `applications_without_policy_do_not_reserve_propagation`.
  - The coverage table is aligned. The old line 143 claim about topology-dependent masks is gone. A new "Propagation policy" row (`doc/tester.md:146`) states the pinned behaviour.

Both profiles pass, and all 80 reversals are killed in each one.

Three MINOR findings remain open. Each one is reproduced in both profiles.

- **R540-4-01:** a retained Flush changes the Registrar from IN to LV without an observer report.
- **R540-4-02:** replacing an opposite Talker that is in LV has no regression. Two plants survive the enabled profile.
- **R540-4-03:** the round-4 rule that stops receive after a source-instance allocation failure has no test.

## Findings

### R540-4-01 - MINOR - Robustness, Tests

- **Where:**
  - `src/core/mrp_mad.c:644-648`: on a failed Flush reservation, `reg_event` sets `ai->reg = MRP_REG_STATE_LV` and returns an error.
  - `src/core/mrp_mad.c:722-726`: `deliver_event_changed` returns on any error before `observe` (`:738`).
  - Every other failure path restores the previous state. This is the only path that changes state and then returns an error.
- **Authority:**
  - `src/include/shish_lan/mrp.h:387`: "Observe every Applicant/Registrar state change on any port of the app."
  - `doc/integrator.md:146-149`: register the observer "when transition records are needed".
- **Evidence:**
  - `scripts/probe_r3.c` tracks each attribute's last reported Registrar state. It counts a gap when a transition's `reg_from` differs from that state.
  - In both profiles, 45 of 114 Flush cases have a gap: every failed Flush that starts from IN (`receipts/probe/probe-head-m{0,1}.log`).
  - The observer sees IN, and then LV to MT on leavetimer!. The IN to LV change is never reported.
  - Scratch fix-check `receipts/plants/fixcheck-observer.diff` adds one `observe` call on the error path. Then both profiles report zero gaps, the probe passes 5934 checks, and the unit suite passes (`receipts/plants/fixcheck-observer.json`).
- **Impact:**
  - A transition record or debug console sees a registration leave from LV after only ever seeing it IN.
  - A consumer that rebuilds Registrar state from transitions holds IN until the retry. It also misses the event that caused the change.
  - No test pins observer output on this new path.
- **Required outcome:**
  - Report the retained IN to LV change to the observer. For example, call `observe` on the `deliver_event_changed` error path, which reports only real changes.
  - Alternatively, state the exception in `mrp.h:387` and `doc/integrator.md:149`.
  - Add a regression that checks observer continuity for a failed Flush from IN, with a named reversal.
- **Verification:** `scripts/probe_r3.c` must print `cases with observer gaps 0` in both profiles. The new named reversal must fail its test in both profiles.

### R540-4-02 - MINOR - Tests

- **Where:**
  - `src/core/mrp_mad.c:1011`: replacement applies to old registrations that are not MT, so LV is included.
  - `src/core/mrp_mad.c:1015-1018`: leavetimer! is delivered to the old registration after rLv!.
  - `tests/unit/review_test.c:736-777` and `tests/unit/receive_test.c:129-145`: both replacement tests start with the old Talker in IN.
- **Authority:**
  - Round 5 item 2 requires Leave before Join at every fault position in both profiles.
  - Issue #10 acceptance 2 requires that every new behaviour has a test that fails when it is reverted.
  - `doc/manager.md` 35.2.6 row: received Join replaces opposite Talker registrations, and changed values are handled in IN and LV.
- **Evidence** (`receipts/plants/plants-head.json`):
  - `p09` restricts replacement to IN. It survives the enabled-profile suite. In the default profile it is killed only through the fault-retry path.
  - `p06` drops the leavetimer! delivery. It survives the enabled-profile suite.
  - My probe kills both in both profiles: with the old Talker in LV, the new Join is indicated before the old Leave (460 failures per profile).
  - At this head, the probe passes these LV cases in both profiles. The behaviour is correct, but nothing pins it.
  - In the enabled profile, rLv! from IN goes straight to MT. The leavetimer! reservation failure path in replacement is therefore exercised only from LV, and no test covers it.
- **Impact:** in the enabled build, the 35.2.6 ordering for a Talker in LV can regress silently. Examples are a Talker aged by LeaveAll, or a Talker in LV after rLv!. The host would then see the new Talker registered before the old one is withdrawn.
- **Required outcome:**
  - Extend the replacement regression to start with the old Talker in LV, reached by a received LeaveAll. Cover both directions and every fault position, in both profiles.
  - Add a named reversal, for example the IN-only condition, that fails the new test in both profiles.
- **Verification:**
  - `python3 scripts/plants_r3.py --only p06-replace-skip-leave-timer,p09-replace-in-only ...` must report KILLED with the new named test in both profiles.
  - `scripts/probe_r3.c` must still pass.

### R540-4-03 - MINOR - Tests

- **Where:**
  - `src/core/mrp_mad.c:982`: the receive stop guard `if (rc->error || priv->map_error)`. The `rc->error` operand covers a failed source-instance allocation (`:999-1001`). This guard was added in round 4.
  - `tests/unit/review_test.c:778-801`: `reservation_failure_stops_later_receive_messages` sweeps faults 2 to 4, the reservations, but not fault 1, the source instance.
- **Authority:**
  - Issue #10 acceptance 2.
  - The Round 5 contract: "Later attributes wait for that retry" (`src/include/shish_lan/mrp.h:275`, `doc/integrator.md:220`).
  - The 35.2.6 event-order comment at `src/core/mrp_mad.c:1004`.
- **Evidence:**
  - Plant `y01b` keeps only `priv->map_error` in the guard. It builds and passes the whole suite in both profiles (`receipts/plants/plants-y-head.json`).
  - My probe case `receive-stop fault=1` fails on it in both profiles. The later Talker is registered and indicated during the failed receive, before the earlier one.
  - The author's `receive-stop` reversal and my `y01` remove the other operand, or the whole guard. Both are killed.
- **Impact:** the stop rule for the first allocation of a receive can regress silently. Indications would then arrive out of payload order after a retry.
- **Required outcome:**
  - Add fault position 1 to the stop regression, or add an equivalent test.
  - Add a named reversal that drops `rc->error` from the guard and fails that test in both profiles.
- **Verification:** `python3 scripts/plants_r3.py --only y01b-stop-map-error-only ...` must report KILLED with the named test in both profiles.

### Suggestions

- **R540-4-S1 (SUGGESTION):** a LeaveAll in a later message of the same payload is still applied after a reservation failure, because `rx_on_leaveall` (`src/core/mrp_mad.c:1047`) has no stop guard.
  - Probe case `later LeaveAll after failure`: a registered Talker enters LV during the failed pass.
  - The identical retry converges to the single-pass state.
  - Consider guarding it, or stating it next to "Later attributes wait for the retry".
- **R540-4-S2 (SUGGESTION):** a peer re-declaration that arrives before the 1 cs retry cancels a retained Flush withdrawal. This is the Table 10-4 LV and rJoin cell, so no Leave or Join pair is indicated.
  - The host view stays consistent: the attribute is registered both ways.
  - The probe records 0 Leaves with "receive before tick" and 1 Leave with "tick before receive" (info lines).
  - Consider one sentence in `doc/integrator.md` after the Flush retention sentence.
- **R540-4-S3 (SUGGESTION):** the Flush request for LeaveAll (`src/core/mrp_mad.c:1118`) predates this PR and has no killing test (plant `p13` survives both profiles).

## Prior public findings at this head

| Prior finding | State at this head | Evidence |
| --- | --- | --- |
| R541-3-F1 (MAJOR) / R540-3-01: Flush lost on allocation failure | RESOLVED | 114 probe Flush cases per profile pass. `82422d6f` fails 570 checks. Plants p01-p05 and p15 are killed by the named Flush test. Contract text is updated in `mrp.h:275-278`, `mrp.h:347-348`, `doc/integrator.md:220-224` and `doc/developer.md:285-304`. The Registrar graph claim is qualified (`doc/developer.md:184`). |
| R540-3-02: replacement order | RESOLVED | 184 probe replacement cases per profile pass. `82422d6f` fails 48 ordering checks. Plant p08 and the reversal `replacement-order` are killed in both profiles. The LV-start test gap is raised as R540-4-02. |
| R540-3-03: y01, y02, y07 survive; tester line 143 | RESOLVED | The author's reversals and my y01, y02, y02b, y07 and y07b are killed by named tests in both profiles. The table is aligned (`doc/tester.md:146-147`). The `rc->error` operand gap is raised separately as R540-4-03. |
| R540-3 y03 (equivalent mutant) | Remains equivalent | Code is unchanged. |
| R540-2-01, R540-2-02, R540-2-03, R541-2-F1, R541-2-F2, R541-2-F3 | RESOLVED (retained) | Their reversals (`changed-in-only`, `stream-list-boundary`, `changed-value-rollback`, `registrar-rollback`, `applicant-rollback`, `leave-timer-retry`, `receive-map-error`, `reservation-atomicity`, `poll-replay`, `commit-replay`, `queue-teardown`, `zero-attribute-length`, `changed-value-propagation`, `replay-error-retention`, `callback-order`) are killed in both profiles (`receipts/reversals/`). |
| R540-2-R1, R541-2-R1, R538-2-R2 | RESOLVED | `doc/tools/README.md:31` has the exact text. |
| R540-2-R2, R541-2-R2, R538-2-R3 | RESOLVED | `doc/manager.md:91-92` have the exact sentences. |
| R541-1-F1 to F7, R541-1-S1, R541-1-S2, R540-1-01 to 07 | RESOLVED (retained) | Their range, extension, scope, profile and LeaveAll reversals are killed in both profiles. `switch.c` is in both source lists (`CMakeLists.txt:9`, `:38`), and the embedded check passes. The Domain clause is cited (`doc/developer.md:314`). The round-5 delta adds no unbraced guard. |

## Lens results

### Conformance

- The default Registrar table, the Milan IN and rLv! cell and the parser are unchanged in this delta.
- Under allocation exhaustion, a failed Flush! reaches the Table 10-4 Flush! result (Leave, then MT) one tick later. The developer and manager guides state this deviation.
- Replacement keeps the 35.2.6 order: old Leave before new Join.
- The standard does not define exhaustion behaviour. R540-4-S2 is the Table 10-4 LV and rJoin cell.
- CLEAN.

### RTL

- The repository contains no HDL (`receipts/tools.txt`), so the pinned simulator was neither needed nor used.
- I applied this lens to the target-facing build:
  - the embedded source-list link and dispatch probes pass in both profiles;
  - the freestanding checks pass in the default and Milan settings;
  - the delta adds no allocation beyond the documented reservations;
  - the retained Flush uses the existing per-attribute timer.
- CLEAN.

### Robustness

- Instrumented suites (address, undefined-behaviour and leak checks) pass in both profiles with no reports (`receipts/checks/asan-*.log`).
- The reviewer probe runs with the same instrumentation. It passes 5934 checks per profile, with zero live allocations after every teardown. This covers:
  - one-shot and persistent faults;
  - Re-declare withdrawal under persistent exhaustion;
  - receive stopping at faults 1-9.
- UNCLEAN because of R540-4-01.

### Tests

- Both profiles at the exact head (`receipts/head/`):
  - configure, build, ctest (1/1), the unit runner, behave and the behave dry run all return 0;
  - 75 tests in eight suites: 4745 assertions (default) and 4733 (enabled);
  - behave: one feature, three scenarios and ten steps.
- Other published commands (`receipts/checks/`):
  - the isolated codec command: nine tests, 1690 assertions, rc 0;
  - the embedded check, rc 0;
  - both freestanding commands, rc 0.
- I ran the author's full reversal driver in both profiles, not a sample. The result is 80 of 80 killed, and the restored builds pass (`receipts/reversals/`).
- Each of the five new reversals fails exactly its named test (`receipts/reversals/new-named-failures.txt`).
- Reviewer plants: 21 plants in each profile, 42 runs in total (`receipts/plants/`):
  - 31 runs are killed.
  - These survivors are equivalent:
    - `p07` in the default profile, where rLv! never reserves;
    - `p11`, because `map_error` is still set;
    - `p10`, a transient value that the retry overwrites.
  - `p13` predates this PR (R540-4-S3).
  - The real gaps are `p06` and `p09` in the enabled profile (R540-4-02) and `y01b` in both profiles (R540-4-03).
- UNCLEAN because of R540-4-01, R540-4-02 and R540-4-03.

### Docs

- All documentation checks return 0 (`receipts/docs/`), and the results match the PR body:
  - 941 sentence fragments, none over 25 words;
  - 0 unlinked references;
  - 79 reference self-tests pass;
  - 352 local links and 20 external URLs pass with authenticated repository access;
  - 27 graphs render, the largest with 12 nodes.
- I viewed the new Flush retry diagram after rendering. It has seven nodes with readable labels, and it matches the code path. The counter reports six because it does not count the decision node.
- All 21 changed anchor links (nine distinct lines) land on their named code: `mrp_transmit`, `mrp_reclaim`, `deliver_event`, `rx_on_leaveall`, `la_event`, `leaveall_draw`, `pt_event`, `mrp_set_periodic` and `mrp_app_destroy`.
- All 60 tracked files carry the SPDX Apache-2.0 identifier.
- The counts are correct in the README, `doc/manager.md`, `doc/tester.md` and the PR body:
  - 75 tests, with 4745 and 4733 assertions;
  - 80 reversals.
- The new text keeps the owner's rules.
- CLEAN.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `reg_event`, `rx_on_attr` and the Flush and replacement paths in `src/core/mrp_mad.c`, against Table 10-4 and 35.2.6. Both profiles. Probe cases at head and at `82422d6f`. | R540-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| RTL | CLEAN | No HDL (0 files). Embedded source-list link and dispatch in both profiles. Freestanding checks. Allocation and timer use of the delta. | R540-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Robustness | UNCLEAN (R540-4-01) | Flush retention, repeated exhaustion, replacement stop, receive stop, Re-declare retry, observer continuity, teardown. Reviewer probe 5934 checks per profile. Instrumented suites. | R540-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Tests | UNCLEAN (R540-4-01, R540-4-02, R540-4-03) | ctest, unit, behave and dry run in both profiles. Codec, embedded and freestanding commands. 80/80 reversals per profile with named failures. 42 plant runs. `tests/unit/review_test.c` and `fault_alloc.c` read in full. | R540-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Docs | CLEAN | README.md, CONTRIBUTING.md, `doc/*.md`, `doc/tools/README.md` and `mrp.h` contract comments. Five doc checks. Changed anchors. Rendered retry diagram. SPDX. PR body figures. Carried residues. | R540-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |

No RESIDUE is open at this head.

## Real limits

- Hosted CI has zero check runs, zero statuses and zero workflow runs at this head. The repository has no workflow (`receipts/hosted-checks.txt`). All execution evidence here is local.
- The assignment states that the manager's full source static, builder and native banks passed at this head. I did not rerun them, as assigned.
- I built the unit framework (1.6.3, commit `abb74b39`) from source in scratch. Host tools are listed in `receipts/tools.txt`.
- I could not read the IEEE or Milan texts. My clause readings follow the frozen assignment and the in-repo tables.
- My probe uses its own handcrafted MSRP payloads and the real stream application on three ports. It does not run the other reviewer's probe or its counts (2289 and 532 in the PR body). The author packet records that probe passing.
- Plants are single-change host runs. Persistent exhaustion is probed, but only up to three held ticks.
- No Zephyr, target, hardware or network run was done. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Carry R540-4-01, R540-4-02 and R540-4-03 to the author. Each needs a regression and a named reversal in both profiles.
- Consider R540-4-S1, R540-4-S2 and R540-4-S3.
- Build and judge the final current-dev merge candidate separately from this source validation. The source base is `1401654530ce7d9275de9b901e67df47e5bbc536` and live dev is `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- Own hosted and act acceptance. None ran here.
- The pinned evidence commit `eb9c5a65` does not contain `author-r5/`. Cite the evidence branch commit `0c632696` (or its successor) when publishing.
- Issues #6, #7, #10 and #11 close only through the merge.
- Publish this report with the files listed in `MANIFEST.sha256`. The scripts take the clone path as an argument (`SRC`). The unit framework prefix must contain the 1.6.3 build.

R540-4 FINISHED
