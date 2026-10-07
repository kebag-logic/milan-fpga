[R540] POSITIVE - exact head 14c8b364863be49bc222f4913830b79d23dcf173

# R540-6 internal review: kebag-logic/lwSRP PR #12 (issue #10), round 7

- Exact head `14c8b364863be49bc222f4913830b79d23dcf173`, tree `0d2f7e8cfb5f1e2886c7cfabde530b7cf1ed3921`.
- Delta: one commit on `a29f8d13` ("Snapshot pending Flush values across Applicant updates"). It changes `src/core/mrp_mad.c`, `src/include/shish_lan/mrp.h`, `tests/unit/review_test.c`, `tests/check_reversals.py`, `README.md` and five guides. Full PR range: `1401654530ce7d9275de9b901e67df47e5bbc536..14c8b364`.
- Review start: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036527202.
- Assignment: "Round 7 for [A563]" (lwSRP #10 comment 6036261356), including the manager ruling on atomic refusal.
- Public evidence: milan-fpga branch `lwsrpm2-review-evidence` at `271ee8152e1b1ed7f7ab2ca60d1076d3ab037684`. That commit holds `review-evidence/lwsrpm2-r1/author-r7/` and the round-6 reviewer packets. The pinned commit `eb9c5a65` holds only the round-1/2 author packet.
- Receipt paths use `$PACKET` (this packet) and `$CLONE` (the detached review clone).

## Verdict

POSITIVE. No BLOCKER, MAJOR or MINOR finding is open, and no RESIDUE is open.

Both round-7 items are resolved at their root:

- R541-5-F1: the value owed by a failed Flush is now a snapshot inside the attribute instance. Propagation from another ingress port, local declarations and receive on the source port all leave it unchanged.
- R540-5-01: a timer-completed Flush is now covered by a named regression and a discriminating reversal.

**Retained-Flush mechanism: complete.** I listed every read and write of pending storage: `flush_pending`, `flush_value`, `reg`, `attr_val`, and instance release. Each one either keeps the snapshot or completes the withdrawal with it. Differential probes compare every faulted run with its no-fault control. Every path gives exactly one owed Leave, with the original value. I found no further defect in the mechanism, so this review does not trigger the manager's switch to atomic refusal. Four new SUGGESTIONS and two retained ones are listed below; none of them changes the verdict.

## Round-7 items

| Item | State at this head | Evidence |
| --- | --- | --- |
| R541-5-F1 (MAJOR): a propagated update overwrites the owed value | RESOLVED | See the next section. External 48-case probe: 48 of 48 original values per profile. |
| R540-5-01 (MINOR): timer completion not covered | RESOLVED | `timer_completed_flush_keeps_unchanged_registrations_quiet` (`tests/unit/review_test.c:1008-1046`). Reversal `flush-timer-completion` is killed in both profiles. The prior internal probe passes 243 of 243 checks per profile. |

### R541-5-F1 at root

- **Code.**
  - `src/core/mrp_mad.c:70-71` adds an aligned 48-byte `flush_value` to each instance.
  - `:649-656`: the first failed Flush copies `attr_val` into it. The `!ai->flush_pending` guard keeps it unchanged on later failures.
  - `:642-643`: an LV indication with a pending flag selects the snapshot. That value feeds the reservation copy (`:645`), `leave_ind` (`:681`) and policy selection (`map_publish`, `:687`).
  - `:670-672`: any successful LV indication clears the flag, whether it comes from the timer or from receive.
  - `get_or_create_attr` (`:480`) still refreshes only `attr_val`, so Applicant updates stay visible.
- **External probe** (R541-5 `probe.c`, sha256 `0b80866b…`, which matches the author provenance):
  - `cross-port` mode: 48 cases, 2188 checks, 0 value mismatches in both profiles. All 48 lines show `withdrawal` equal to `expected`.
  - Broad mode: 489 cases and 21780 checks pass in both profiles.
  - Both modes also pass under address and undefined-behaviour instrumentation (`receipts/r541-cross-port-*.log`, `receipts/r541-probe-*.log`, `receipts/sanitize-*.log`).
- **Repository regressions.**
  - Three cross-port tests run 16 cases each: four fault settings, IN or LV, and timer or receive completion. Together they make 48 cases.
  - A local-declaration test adds 48 more cases. It also checks a second failed Flush and a failed timer retry.
  - Each case checks the Leave value and one policy call with the original value. It also checks the visible Applicant value, quiet unchanged refreshes, and a fresh snapshot for a later Flush (`tests/unit/review_test.c:897-1007`).
- **Reversals.** All five new reversals are killed in both profiles, with their required named failures (`receipts/new-reversal-named-failures.txt`).
- **Legitimate updates are kept.**
  - `stored_value` sees the Applicant value (`other` or `next`) before and after Leave.
  - My probe's transmit case encodes the propagated frame size 200 from the pending port.
  - Ordinary LV recovery passes `registrar_recovery_stops_aging_without_duplicate_join_or_map`. The R541-5 broad probe covers it too.

### Mechanism completeness: every path that touches pending storage

The inventory is in `receipts/pending-storage-touchpoints.txt`.

| Path | Effect on a pending instance (Registrar LV, flag set) | Evidence |
| --- | --- | --- |
| Another Flush that fails | Snapshot kept; 1 cs timer rearmed | Unit local test; mutant m6 killed |
| Another Flush that succeeds | Leave with the snapshot; flag cleared | Probe S2 `second-flush-ok` |
| Leave timer (fails or succeeds) | Timer rearmed, or Leave with the snapshot | Units; R541-5 deadline cases |
| Receive on the source port, any of the six events | Leave with the snapshot before the refresh; a later Join carries the new value; a failed retry reports NO_MEMORY | Probe S6 (216 cases, every retry fault); R541-5 interleave cases |
| Received LeaveAll (any identity), Re-declare, transmitted LeaveAll | No Registrar change in LV (`:343`, `:372`, `:378`, `:390`); snapshot kept | Probe S1 (24 cases) |
| Propagated Join or Leave from another port; local Join, New or Leave | Applicant only (ignored-Registrar rows `:333-337`); `attr_val` refreshed; snapshot kept | External cross-port probe; unit local test; probe S2 |
| Opposite Talker JoinIn or JoinMt (replacement) | The pending old Talker gets rLv (no change) and then leavetimer, so its Leave uses the snapshot before the new Join | Probe S3; prior internal probe |
| `mrp_reclaim` | Not reclaimed, because reclaim requires MT (`:1113`) | Probe S2 `reclaim` |
| Flush on another port and its withdrawal | Applicant only on the pending port | Probe S2 `remote-leave` |
| Rollback copies in receive (`:1043`, `:1065`) | They restore `attr_val` only | Code inspection; units |
| Destroy | Frees the instance; no live allocations remain | Every probe checks `allocation_live() == 0` |

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open.

### R540-6-S1 - SUGGESTION - Conformance, Tests

- **Where:** `src/core/mrp_mad.c:1030-1031`. Replacement runs only for JoinIn and JoinMt. `:1026-1029` and the 35.2.6 row of `doc/manager.md:37` leave New conflicts to host precedence.
- **Evidence:** probe S3 (`receipts/r540-probe-{OFF,ON}.log`, `NOTE` lines).
  - A pending old Talker receives an opposite-type New on the same port, at faults 1-3.
  - The new Join is indicated first. The owed Leave of the old type follows one tick later.
  - In the no-fault control, the old Leave comes first. JoinIn and JoinMt keep Leave first at every fault.
- **Impact:**
  - The final state matches the control, and the Leave carries the snapshot.
  - The host already has to handle the sequence {old, new} then {new} for a New conflict without faults.
  - The round-6 rule covers the same attribute (type and identity), so this is not a defect. It is an undocumented ordering difference.
- **Suggested outcome:** state in the retry contract that a pending withdrawal of one Talker type does not precede a New of the opposite type. Alternatively, complete pending opposite-type withdrawals before a New.
- **Verification:** the probe S3 New rows.

### R540-6-S2 - SUGGESTION - Docs, Robustness

- **Where:** `observe` reports `ai->attr_val` (`src/core/mrp_mad.c:713`). The interface (`src/include/shish_lan/mrp.h:389-398`) does not say which value it reports.
- **Evidence:** probe S4.
  - After a cross-port refresh, the observer reports the pending LV-to-MT completion with value 200.
  - The Leave indication carries 100.
  - The no-fault control observes 100.
- **Impact:** observer-based diagnostic logs can disagree with the indication for the same transition. Indications and policy are correct.
- **Suggested outcome:** document that observers and `mrp_attr_visit` show the Applicant value. Alternatively, pass the snapshot for the completing transition.
- **Verification:** probe S4.

### R540-6-S3 - SUGGESTION - Docs, RTL (target footprint)

- **Where:** `doc/developer.md:294`: "The snapshot adds 48 value bytes per instance, without a separate allocation."
- **Evidence:** `receipts/attr-instance-size.txt`. The sentence is accurate about value bytes, but alignment to `max_align_t` adds padding.
  - `struct mrp_attr_inst` grows from 96 to 152 bytes (+56) on a freestanding Cortex-M4 compile.
  - It grows from 144 to 208 bytes (+64) on the x86-64 host.
- **Impact:** a reader sizing a bare-metal heap from this sentence could underestimate by 8-16 bytes per attribute.
- **Suggested outcome:** add "plus alignment padding (measured +56 bytes on Cortex-M4)", or state the instance growth.
- **Verification:** re-measure with the method in the size receipt.

### R540-6-S4 - SUGGESTION - Conformance, Docs (inherited)

- **Where:** `get_or_create_attr` (`src/core/mrp_mad.c:475-481`) shares one value slot between Applicant and Registrar for each port and identity. This predates the PR: base `1401654` has the same refresh.
- **Evidence:** probe S5. Propagating 200 into the port before the Flush gives Leave value 200 in the control and at every fault. The snapshot records the slot as it was when the Flush failed, so the mechanism matches an immediate Flush.
- **Impact:** if an identity collides across ports, a withdrawal can carry an Applicant-refreshed value. This is outside the round-7 scope.
- **Suggested outcome:** document the single-slot model in the integration guide, or track the registered value separately in a later change.
- **Verification:** probe S5.

### Retained prior suggestions

- **R540-5-S1 (SUGGESTION, Tests): RETAINED.** Plant `p1-replacement-skips-pending` adds `!old->flush_pending` to the replacement guard. It passes the unit suite in both profiles, and my probe S3 kills it (`receipts/prior-plants.log`). The PR body acknowledges this gap.
- **R540-4-S3 (SUGGESTION, Tests): RETAINED.** Plant `p2-flush-leaveall-request` removes `src/core/mrp_mad.c:1140`. It passes the unit suite in both profiles, and the transmit case in my probe S1 kills it.

## Prior public findings at this head

I read the earlier public reviews only after writing `receipts/independent-verdict.md`.

| Prior finding | State | Evidence |
| --- | --- | --- |
| R541-5-F1 (MAJOR) | RESOLVED | See above. |
| R540-5-01 (MINOR) | RESOLVED | See above. Mutant m4, which skips clearing on the Flush event, is also killed. |
| R540-5-S1 | RETAINED as SUGGESTION | See above. |
| R540-4-S3 | RETAINED as SUGGESTION | See above. |
| R541-4-F1/F2, R540-4-01/02/03, R540-4-S1/S2 | RESOLVED (retained) | Their reversals are killed in both profiles: `pending-flush`, `flush-before-refresh`, `flush-completion`, `flush-deadline`, `flush-observer`, `replacement-lv`, `replacement-leave-timer` and `receive-instance-stop`. |
| R541-3-F1 / R540-3-01..03, R540-2-*, R541-2-*, R541-1-*, R540-1-*, parent R532-1 S1/S2 | RESOLVED (retained) | All 93 repository reversals are killed in both profiles. The restored build and check return 0 (`receipts/reversals-*.log`, `*-commands.json`). |
| R538-2-R2/R3, R540-2-R1/R2, R541-2-R1/R2 (carried residues) | RESOLVED | Those sentences are unchanged, and the documentation checks pass. |

## Lens results

### Conformance - CLEAN

- With allocation available, Flush still follows the Table 10-4 Flush! row: Lv, then MT.
- Under exhaustion, every probed sequence matches an immediate Flush followed by the later event. The only exception is the documented New precedence ordering (S1).
- No Registrar table row, Milan cell (`:626-629`) or parser line changed.
- The exhaustion policy lies outside the standard. It is documented consistently in:
  - `mrp.h:277-285` and `:355-361`;
  - `doc/developer.md:291-301`;
  - `doc/integrator.md:224-235`;
  - the Table 10-4 row of `doc/manager.md`.
- The contribution rules hold:
  - one-line commit subject with no body or trailer, and the configured identity;
  - braces on the changed guard (`:651`);
  - no new enum;
  - the SPDX identifier in all 60 tracked files;
  - a single parent, `a29f8d1`, so there was no rebase or amend.

### RTL - CLEAN

- The repository has no HDL, so the pinned simulator was neither needed nor used.
- I applied this lens to the target-facing build:
  - the embedded source-list links and dispatch probes pass in both profiles (`receipts/embedded.log`);
  - the freestanding checks pass in both settings (`receipts/freestanding-*.log`);
  - the delta adds no allocation.
- Measured footprint: each instance grows by 56 bytes on Cortex-M4 (S3).

### Robustness - CLEAN

- The unit suites pass in both profiles under address, undefined-behaviour and leak instrumentation, with sanitizer recovery disabled. My probe and both modes of the external probe pass the same way (`receipts/sanitize-*.log`).
- Every probe case ends with zero live allocations.
- The copy is bounded by `attr_store_len`, which is capped at 48, and lands in a 48-byte aligned array.
- The completeness table covers repeated refusal, reclaim, destroy, LeaveAll, Re-declare, replacement and receive-retry faults.

### Tests - CLEAN

- Both profiles (`receipts/profile-{OFF,ON}.log`):
  - configure, build, ctest 1/1, the unit runner, behave and the behave dry run all return 0;
  - 86 tests in eight suites: 19885 assertions (default) and 19873 (enabled);
  - 1 feature, 3 scenarios and 10 steps.
- The isolated codec command runs 9 tests with 1690 assertions and returns 0 (`receipts/codec.log`).
- I ran the full repository reversal driver, not a sample. It kills 93 of 93 per profile, and the restored build and check return 0.
- My mutation set has nine mutants (`scripts/mutants.py`, `receipts/mutants.log`, `receipts/mutant-failing-tests.txt`):
  - the unit suite kills eight of them in both profiles;
  - m3 survives. It reserves queued propagation from `attr_val` and is equivalent: `mrp_mad_leave` applies a queued Leave by identity through `find_attr`, so its payload is never observable.
- My internal probe passes 320 scenarios and 3023 checks per profile (`receipts/r540-probe-*.log`).
- The prior internal probe passes 243 of 243 checks per profile (`receipts/r540-5-probe-*.log`). Its source hashes match the author provenance (`receipts/prior-probe-sources.sha256`).

### Docs - CLEAN

- All documentation checks return 0 (`receipts/doc-*.log`, `receipts/graphs.log`):
  - 975 fragments, none over 25 words;
  - 0 unlinked references;
  - 79 self-tests;
  - 354 local links and 20 external URLs, with authenticated repository access;
  - 27 graphs render.
- I rendered and viewed the changed retry graph (`receipts/graph-review.md`).
- All 21 distinct source anchors land on their named code (`receipts/source-anchors.txt`).
- These counts match my runs: README, `doc/manager.md`, `doc/tester.md` (86 tests; 19885 and 19873 assertions; 93 reversals; 48 + 48 cases) and the PR body.
- The interface comment and the four guides agree with the code on snapshot ownership, refresh, completion and retry.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `reg_event`, `rx_on_attr`, the replacement loop, `on_leave_timer` and the Registrar table rows, against Table 10-4 Flush!, leavetimer! and rJoin and against 35.2.6. Interface and guide contracts. Commit format, braces, SPDX. | R540-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| RTL | CLEAN | No HDL. Embedded source-list link and dispatch in both profiles. Freestanding checks. Instance size on Cortex-M4 and on the host. | R540-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Robustness | CLEAN | Every pending-storage path in the completeness table. Instrumented units and three probes in both profiles. Live-allocation checks. Repeated refusal and teardown. | R540-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Tests | CLEAN | In both profiles: ctest, units, behave, dry run and codec. 93 of 93 reversals per profile, with named failures. Nine own mutants and two prior plants per profile. External 48-case and 489-case probes, the prior internal probe, and my 320-scenario probe. The `review_test.c` and `check_reversals.py` deltas. | R540-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Docs | CLEAN | README, CONTRIBUTING, `doc/*.md`, `doc/tools/README.md` and `mrp.h`. Five documentation checks, 27 graphs, the rendered retry graph, 21 anchors, counts and the PR body. | R540-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |

## Real limits

- Hosted CI has zero workflow runs, check runs and statuses at this head, and the repository has no workflow (`receipts/hosted-*.json`). No hosted job ran, and no skipped context was counted. All execution evidence here is local.
- The manager's full source static, builder and native banks are taken from the assignment. I did not rerun them, as assigned.
- The unit framework is cgreen 1.7.0 (commit `feeb85ed`), built in scratch with an explicit revision string.
- I could not read the IEEE or Milan texts. My clause readings follow the frozen assignment and the in-repo tables.
- The probes use handcrafted single-value MSRP payloads and the production stream policy on three ports.
- Mutants and plants are single-change host runs.
- The Cortex-M4 size came from a size-only compile that used a stub string header.
- No Zephyr, target, hardware or network run was done. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Consider S1-S4 and the two retained suggestions. None of them blocks.
- Build and judge the final current-dev merge candidate separately from this source validation. The source base is `1401654530ce7d9275de9b901e67df47e5bbc536`, and live dev is `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- Own hosted and act acceptance; none ran here.
- Cite evidence commit `271ee8152e1b1ed7f7ab2ca60d1076d3ab037684`, or its successor, for `author-r7/`.
- Integrity after all probes (`receipts/integrity.txt`):
  - exact head and tree;
  - all 60 tracked blobs match their bytes and modes;
  - the index equals the tree;
  - zero gitlinks, and none are required;
  - a clean worktree, including ignored files.

R540-6 FINISHED
