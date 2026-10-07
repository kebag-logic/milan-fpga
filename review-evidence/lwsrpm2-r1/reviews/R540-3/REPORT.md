[R540] NEGATIVE - exact head 82422d6ffe38d430576cd9d874a45b9e124e6c63

# R540-3 internal review: kebag-logic/lwSRP PR #12 (issue #10), round 4

- Exact head `82422d6ffe38d430576cd9d874a45b9e124e6c63`, tree `02fda6f08254fc7dd5c259c996cfbb31e76682d7`.
- Delta reviewed: `a9cd5ef5..82422d6f`, one commit with a one-line subject and the configured identity.
- I used the full PR range `1401654530ce..82422d6f` for the braces rule, anchors, SPDX and residue checks.
- After all probes, I verified the clone (`receipts/clone-integrity.txt`):
  - head, tree and index tree match;
  - status is empty, including ignored files;
  - all 60 tracked blobs match in bytes and mode;
  - there are zero gitlinks, and none are required.
- Scope was read in this order:
  - `CONTRIBUTING.md` (no `AGENTS.md` exists), `README.md`, `doc/` and `doc/tools/README.md`;
  - the issue #10 body and every manager comment, including the Round 4 assignment (6033982129);
  - the PR body, the carried-residue comment (6033473193) and the review-start comment (6034322044);
  - the diff and history;
  - the public author packet `author-r4/` at milan-fpga `46780a0e` (hashes in `receipts/author-r4-evidence.sha256`).
- I wrote and hashed my verdict and ledger before reading any prior public finding (`receipts/independent-verdict.md`, `receipts/independent-verdict.time`). After that I read R541-2 (6033978356) and my own R540-2 (6033931109). Their status is given below.

## Verdict

NEGATIVE.

Every Round 4 item is resolved at its root, and my own probes confirm each one:

- R540-2-01: my R540-2 cases `p1a`-`p1d` pass in both profiles. The previous head fails them.
- R540-2-02: my cases `p2`, `p2b` and `p2c` pass in both profiles.
- R541-2-F1 and R541-2-F2: my fault-position sweep and policy-order probe pass at head and fail at `a9cd5ef5`.
- R541-2-F3, R540-2-03 and all four residues are resolved.

Both profiles pass. All 75 author reversals are killed in each profile.

Three MINOR findings remain. Each is reproduced in both profiles.

- **R540-3-01:** a Flush! that fails its propagation reservation is silently dropped. It is not reported and not retried.
- **R540-3-02:** a Talker replacement that fails its reservation indicates the new Join before the old Leave.
- **R540-3-03:** three new round-4 behaviours can be reverted without any test failing.

R540-3-01 and R540-3-02 are also present at `a9cd5ef5`. They fall under the Round 4 requirement that no propagation is lost after an allocation failure.

## Findings

### R540-3-01 - MINOR - Robustness, Tests, Docs

- **Where:**
  - `src/core/mrp_mad.c:1095-1100`: `mrp_port_role_change` broadcasts Flush! and returns `void`.
  - `src/core/mrp_mad.c:744-749` and `:740`: `broadcast_event` uses `deliver_event`, which discards the `reg_event` error.
  - `src/core/mrp_mad.c:642-648`: on failure the Registrar returns to IN. The leave timer is re-armed only for `MRP_EVENT_LEAVETIMER`.
  - The contract omits this path: `doc/integrator.md:217-220`, `doc/developer.md:285-287`, `src/include/shish_lan/mrp.h:272-275` and `:341-345`.
- **Authority:**
  - The Round 4 assignment, item 3: no propagation is lost after an allocation failure. The work is deferred and replayed, or refused atomically.
  - IEEE 802.1Q-2018 Table 10-4, Flush! row: IN and LV enter MT with a Leave indication.
- **Evidence:**
  - Probe `scripts/probes/probe_r3.c`, case `f1`, run on a three-port stream bridge.
  - Receipts: `receipts/probes/r3-head-milan{0,1}.log` and `r3-prev-milan{0,1}.log`.
  - Control (no fault): Flush! indicates Leave at once, and the Registrar is MT.
  - Faults 1-3 hit the reservation, with identical results in both profiles:
    - there is no Leave indication;
    - the Registrar stays IN, with no timer;
    - there is no error and no retry.
  - Even with every port polled and ticked, Leave arrives only after 60 ticks. That is the participant LeaveAll followed by the full LeaveTime.
  - `a9cd5ef5` behaves the same way.
- **Impact:**
  - Under allocation exhaustion, a topology Flush! keeps the stale registration and its propagated declarations for a full LeaveAll and LeaveTime.
  - With the Mark II Leave of 500 cs, that is at least five seconds.
  - The host gets no signal, and the documented contract does not describe this path.
  - If the host stops polling that port, nothing withdraws the registration.
- **Required outcome:**
  - Pick one of these:
    - report the failure from `mrp_port_role_change` and document a retry;
    - or keep the work and retry it, for example by entering LV with a 1 cs leave timer, so the existing timer retry withdraws it.
  - Add a fault-port regression and a named reversal.
  - State the Flush! behaviour in the contract text listed above.
- **Verification:** `probe_r3` case `f1` must pass for faults 1-3 in both profiles.

### R540-3-02 - MINOR - Robustness, Tests

- **Where:**
  - `src/core/mrp_mad.c:977`: `priv->map_error` stops processing only at the next attribute.
  - `src/core/mrp_mad.c:1004-1011`: the old Talker's Leave (RLV, then LEAVETIMER) can fail inside `deliver_event`.
  - `src/core/mrp_mad.c:1025`: the new Talker's Join is still delivered in the same call. The comment at `:999` says registrations change "atomically in event order".
- **Authority:**
  - IEEE 802.1Q-2018 clause 35.2.6 and this PR's 35.2.6 row (`doc/manager.md:37`): received Join replaces the opposite Talker registration.
  - The Round 4 contract (`src/include/shish_lan/mrp.h:272-275`): a failure preserves prior state for retry, and only earlier events may remain applied.
- **Evidence:**
  - Probe `probe_r3.c`, case `f2`: Talker Advertise is IN on port 0, then Talker Failed for the same StreamID arrives. I swept the fault position from 0 to 8.
  - Normal order, and faults 1 and 5-8: Leave(Talker Advertise), then Join(Talker Failed).
  - Faults 2-4, in both profiles: receive returns -12, but Join(Talker Failed) is indicated first. Leave(Talker Advertise) follows only on the next tick (default profile) or on the receive retry (Milan profile).
  - The final state matches the control in every case.
- **Impact:** a host that keys stream state by StreamID sees the new Talker registered and then the stream withdrawn. Its table can end up empty while the library holds Talker Failed IN, and nothing re-indicates it.
- **Required outcome:**
  - Stop the current attribute when a replacement reservation fails, before the new event is delivered. The identical retry then replays it in order.
  - Add a fault-port regression and a named reversal.
- **Verification:** `probe_r3` case `f2` must report Leave before Join for every fault position in both profiles.

### R540-3-03 - MINOR - Tests, Docs

- **Where:** these new round-4 lines have no test:
  - `src/core/mrp_mad.c:977`: the receive stops after a reservation failure (`priv->map_error`).
  - `src/core/mrp_mad.c:573`: `map_publish` queues only the ports that policy selects.
  - `src/core/mrp_mad.c:536-538`: an application without policy reserves nothing.
  - `doc/tester.md:143` now lists only "topology-dependent" propagation masks as a gap. That implies core mask handling is covered.
- **Authority:**
  - Issue #10 acceptance 2: every new behaviour has a test that fails when it is reverted.
  - The Round 4 contract (`doc/integrator.md:215`): only indications with propagation policy reserve entries.
- **Evidence:**
  - My plants are in `scripts/plants_r3.py`, with receipts `receipts/plants-{OFF,ON}.jsonl`. The status comes from the unit runner's exit code.
  - Each of these builds and passes all 70 tests in both profiles:
    - `y01`: processing continues after a failure;
    - `y02`: publication ignores the policy mask;
    - `y07`: applications without policy still reserve.
  - `scripts/probes/probe_plants.c` passes at head and fails on each plant, in both profiles (`receipts/probes/plantsprobe-*`):
    - `y01`: a later Talker in the same payload is indicated and propagated after the error;
    - `y02`: a Talker is declared back on its source port, and a Listener is sent to a port with no Talker;
    - `y07`: a VLAN registration is refused under one allocation fault, although VLAN has no policy.
  - `y03` (no `pending_tx` rollback) also survives, but it is an equivalent mutant. Only transmit events set `pending_tx`, and those never indicate.
- **Impact:** the core's honouring of the propagation mask, the stop-on-failure rule and the no-policy path can all regress silently. `y02` reverts the basic MAP contract (`mrp.h:158-166`).
- **Required outcome:**
  - Add regressions that kill `y01`, `y02` and `y07`, with named reversals in `tests/check_reversals.py`.
  - Alternatively, for `y01`, state the intended rule. Either way, align `doc/tester.md:143`.
- **Verification:** re-run `scripts/plants_r3.py` in both profiles. Named tests must kill `y01`, `y02` and `y07`.

## Prior public findings at this head

| Prior finding | State | Evidence at this head |
| --- | --- | --- |
| R540-2-01 (MAJOR): changed value in LV | RESOLVED | See note 1. |
| R540-2-02 (MAJOR): later-version MSRP skip | RESOLVED | See note 2. |
| R540-2-03 (MINOR): allocation and teardown tests | RESOLVED | See note 3. |
| R541-2-F1 (MAJOR): no lost propagation after allocation failure | RESOLVED for receive and timer paths. The Flush! path is raised as R540-3-01. | See note 4. |
| R541-2-F2 (MINOR): callback ordering | RESOLVED | See note 5. |
| R541-2-F3 (MINOR): suite count | RESOLVED | `doc/integrator.md:19` says eight suites. The runner registers and runs eight (`receipts/profiles/*-unit.log`). |
| R540-2-R1 and R541-2-R1 | RESOLVED | `doc/tools/README.md:31` has the exact text. |
| R540-2-R2 and R541-2-R2 | RESOLVED | `doc/manager.md:91-92` have the exact two sentences. |

Notes to the table:

1. **R540-2-01.**
   - `src/core/mrp_mad.c:984-985` now tests `previous->reg != MRP_REG_STATE_MT`.
   - `reg_event` raises the indication to Join only for a changed rJoinIn or rJoinMt (`:628-632`). Unchanged LV recovery keeps the Table 10-4 cell.
   - My `probe_rx.c` passes in both profiles (`receipts/probes/rx-head-milan{0,1}.log`):
     - `p1a`: Asking Failed is indicated in the LeaveAll payload;
     - `p1b`: a LeaveAll-only payload, then the change;
     - `p1c`: Talker MaxFrameSize 100 to 200;
     - `p1d`: the IN control.
   - `a9cd5ef5` fails these (`rx-prev-*`).
   - The new tests cover received and transmitted LeaveAll, Listener and Talker, and JoinIn and JoinMt.
   - The reversal `changed-in-only` fails both named tests in both profiles (`receipts/reversals/sampled-named-failures.txt`).
   - The documentation is updated at `doc/developer.md:191-194` and in the 35.2.6 row of `doc/manager.md:37`.
2. **R540-2-02.**
   - `src/core/mrp_pdu.c:146-150` skips an unknown later-version MSRP Message to its AttributeListLength end.
   - VLAN and MAC keep the vector walk. At the current version the PDU is still rejected (`:151`).
   - Cases `p2` and `p2b` (non-generic vectors) and the `p2c` control pass in both profiles.
   - The reversal `stream-list-boundary` fails `unknown_stream_layout_uses_attribute_list_length`. That test also rejects the same payload at version 0.
   - The three pages and the PR body are aligned.
3. **R540-2-03.**
   - Each of my R540-2 plants now has a matching author reversal. Each is killed in both profiles, and the required tests fail (`receipts/reversals/sampled-named-failures.txt`):
     - `x02` matches `poll-replay`;
     - `x03` matches `registrar-rollback`;
     - `x04` matches `leave-timer-retry`;
     - `x05` matches `receive-map-error`;
     - `x06` matches `reservation-atomicity`;
     - `x07` matches `zero-attribute-length`;
     - `x12` matches `queue-teardown`;
     - `x16` matches `changed-value-propagation`.
   - The fault port (`tests/unit/fault_alloc.c`) also counts live allocations around every boundary test.
4. **R541-2-F1.**
   - `scripts/probes/probe_prior.c` changes a Talker from 100 to 200 under each fault position.
   - At head, in both profiles, the identical retry delivers 200 to the destination.
   - At `a9cd5ef5`, fault 1 leaves the destination at 100.
   - The `probe_r3` case `f3` (a multi-message payload, faults 1-11, retry) converges to the control in both profiles. `a9cd5ef5` fails it.
   - My R540-2 `probe_map` (m1-m5) still passes.
5. **R541-2-F2.**
   - The indication now precedes policy (`src/core/mrp_mad.c:656-670`), which matches `mrp.h:158-163`.
   - In `probe_prior.c`, a policy that enables port 1 only after the host indication now propagates. `a9cd5ef5` does not.
   - The reversal `callback-order` fails `propagation_policy_observes_completed_host_indications`.

## Lens results

### Conformance

- Table 10-4:
  - Unchanged LV Join recovery issues no indication.
  - Changed values in IN or LV indicate and propagate.
  - The Milan IN/rLv! cell is unchanged.
- Clause 10.8.3.5: unknown later-version stream messages are bounded by AttributeListLength, and VLAN and MAC use vectors. The current version is strict, and AttributeLength 0 is rejected for generic unknown messages.
- The PR body cites "35.2.2.6" for the list-length boundary. I could not read the IEEE text here. That number fits the subclause sequence the pages already use (35.2.2.4, 35.2.2.7.2, 35.2.2.8, 35.2.2.9).
- The callback order matches the public interface.
- CLEAN. R540-3-01 and R540-3-02 concern behaviour under resource exhaustion, which the standard does not define. I attribute them to Robustness.

### RTL

- The repository and the delta contain no HDL, so I did not use the pinned simulator (`receipts/tools.txt`).
- I applied this lens to the target-facing build:
  - `tests/check_embedded.py` links and runs dispatch in both profiles (rc 0);
  - `tests/check_freestanding.py` passes in the default and Milan settings (rc 0);
  - the new `fault_alloc.c` is test-only, and `CMakeLists.txt` adds it only to the unit target;
  - the worst case is 32 transient reservations per indication, as documented.
- CLEAN.

### Robustness

- Instrumented suites (address, undefined-behaviour and leak checks) pass in both profiles with no reports (`receipts/checks/asan-*`):
  - default profile: 70 tests, 4215 assertions;
  - Milan profile: 70 tests, 4203 assertions.
- My fault sweeps over receive, timer, replay, commit and teardown pass (`probe_r3` f3, `probe_prior`, `probe_map`).
- UNCLEAN because of R540-3-01 and R540-3-02.

### Tests

- Both profiles, built out of tree from the exact head (`receipts/profiles/`):
  - configure, build, ctest (1/1), the unit runner and behave all return 0;
  - 70 tests in each: 4215 assertions (default) and 4203 (Milan);
  - behave: one feature, three scenarios and ten steps in each.
- The other published commands also return 0 (`receipts/checks/`):
  - the behave dry run;
  - the isolated codec command (1690 assertions);
  - both freestanding commands;
  - the embedded check.
- I ran the author's full reversal driver in both profiles, not a sample. The result is 75 of 75 killed in each, and the restored builds pass (`receipts/reversals/`).
- I sampled twelve round-4 reversals per profile. Each fails exactly the required named tests.
- Reviewer plants, 14 per profile:
  - 10 killed;
  - 1 equivalent (`y03`);
  - 3 real gaps (R540-3-03).
- UNCLEAN because of R540-3-01, R540-3-02 and R540-3-03.

### Docs

- The documentation checks return 0 and match the PR body (`receipts/doc/`):
  - 925 sentence fragments, none over 25 words;
  - 0 unlinked references;
  - 79 reference self-tests pass;
  - 347 local links and 20 external URLs pass with authenticated repository access. The first run hit one transient HTTP 502 from an external site; the retry returned 0 (`links-retry.*`).
  - 26 graphs render, the largest with 12 nodes.
- All 43 source anchors land on their named code (`receipts/anchors.txt`).
- The two changed graphs are the architecture receive flow and the integrator receive sequence. Both render with rc 0. I read their source; they show the code's order: reserve, then indicate, then policy, then queue. I did not view the rendered images this round.
- All 60 tracked files carry the SPDX Apache-2.0 identifier.
- The changed text keeps the owner's rules.
- These counts are correct in the README, `doc/manager.md`, `doc/tester.md` and the PR body:
  - 70 tests, with 4215 and 4203 assertions;
  - eight suites;
  - 75 reversals.
- UNCLEAN because of R540-3-01 (the contract omits Flush!) and R540-3-03 (`doc/tester.md:143` implies mask coverage).

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `src/core/mrp_mad.c` (`reg_event`, `rx_on_attr`), `src/core/mrp_pdu.c` (`parse_pass`) and `mrp.h`, against Table 10-4, 10.8.3.5, 35.2.2 and 35.2.6. Probes `probe_rx`, `probe_fixes` and `probe_prior` at head and at `a9cd5ef5`, both profiles. | R540-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| RTL | CLEAN | No HDL present. Embedded and freestanding checks in both profiles; build list; reservation bound. | R540-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Robustness | UNCLEAN (R540-3-01, R540-3-02) | Reservation, rollback, publication, replay and teardown. Fault sweeps `probe_r3` and `probe_prior` and the `probe_map` rerun; instrumented suites in both profiles. | R540-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Tests | UNCLEAN (R540-3-01, R540-3-02, R540-3-03) | ctest, unit runner, behave and dry run in both profiles; codec command; 75/75 reversals per profile with sampled named failures; 14 reviewer plants per profile; `tests/unit/review_test.c` and `fault_alloc.c` read in full. | R540-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Docs | UNCLEAN (R540-3-01, R540-3-03) | README.md, CONTRIBUTING.md, `doc/*.md`, `doc/tools/README.md` and `mrp.h` comments. All five doc checks; 43 anchors; changed graphs; SPDX; PR body figures; four residues. | R540-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |

## Real limits

- Hosted CI has no check runs, statuses or workflow runs at this head, and the repository has no workflow (`receipts/hosted-checks.txt`). All execution evidence here is local.
- The assignment states that the manager's source banks passed at this head. I found no exact-head bank receipt in the public evidence tree I examined.
- I built the unit framework (1.6.3, tag commit `abb74b39`) from source in scratch. The host tools are listed in `receipts/tools.txt`.
- I could not read the IEEE text. My clause readings follow the frozen assignment.
- R540-3-01 and R540-3-02 are shown against the documented contract and the no-fault control. They do not depend on clause wording.
- I did not count the author's "27 published commands" independently. I ran every command in the README and the tester guide.
- No Zephyr, target, hardware or network run was done. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The probes and plants are single-change host runs with one injected allocation fault each.

## Pending manager duties

- Build and judge the final current-dev merge candidate separately from this source validation. The source base is `1401654530ce7d9275de9b901e67df47e5bbc536` and live dev is `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- Own hosted and act acceptance. None ran here.
- Carry R540-3-01, R540-3-02 and R540-3-03 to the author.
- Residues: no open residue remains from this head.
- Issues #6, #7, #10 and #11 close only through the merge.
- Publish this report with the files listed in `MANIFEST.sha256`. The scripts expect `SRC` to be set to an exact-head clone.

R540-3 FINISHED
