[R540] NEGATIVE - exact head a9cd5ef58a2478cb2ce4899b31aa02d5c2072646

# R540-2 internal review: kebag-logic/lwSRP PR #12 (issue #10), round 3

- Exact head `a9cd5ef58a2478cb2ce4899b31aa02d5c2072646`, tree `bc5b80a60d923ce869647e3f3ba95276456864d1`. After all probes I verified the head, the tree, the index tree, an empty status (including ignored files) and zero gitlinks (`receipts/clone-integrity.txt`).
- Delta reviewed: `23d9a817..a9cd5ef5`, one commit. `23d9a817` has the same tree as the earlier reviewed `86a5f74c`. I used the full PR range `1401654530ce..a9cd5ef5` for the braces rule, anchors, SPDX and residue checks.
- Scope read, in this order:
  - `CONTRIBUTING.md` (no `AGENTS.md` exists), `README.md`, `doc/` and `doc/tools/README.md`.
  - The issue #10 body and every manager comment: the assignment, Round 2 and Round 3.
  - Issues #1, #4, #6, #7 and #11, the PR body, and the carried-residue comment on the PR.
  - The diff and history.
  - Public evidence: milan-fpga `eb9c5a65` (`review-evidence/lwsrpm2-r1/author`), and the round-3 author packet `author-r3/` at archive `de6b34ba` (hashes in `receipts/author-r3-evidence.sha256`).
- I wrote and hashed my verdict and ledger before reading any prior review (`receipts/independent-verdict.md`, `receipts/independent-verdict.time`). After that I read the prior public findings (R540-1, R541-1) and give their status below.

## Verdict

NEGATIVE. Every round-2 finding is resolved at this head, and I confirmed each one with my own probes:

- atomic range validation;
- higher-version skipping for VLAN and MAC;
- the switch source in the embedded list;
- retained propagation;
- the Domain clause;
- the braces rule;
- reversal coverage;
- the Table 10-4 LV decision.

Both profiles pass. All 60 author reversals are detected in each profile.

Two round-3 changes add MAJOR regressions, both reproduced in both profiles. Neither is present at `23d9a817`.

- **R540-2-01:** this is a side effect of the correct Table 10-4 change. If a changed MSRP Listener declaration or Talker value arrives while the Registrar is in LV, it is never indicated. The application keeps the old value permanently.
- **R540-2-02:** a later-version unknown MSRP message is no longer skipped by its AttributeListLength. Some such messages now make the parser reject the whole PDU, including the valid declarations that follow.

There is also one MINOR test-coverage gap (R540-2-03). The licence wording carried over from PR #9 has not been applied (two RESIDUE items).

## Findings

### R540-2-01 - MAJOR - Conformance, Robustness, Tests, Docs

- **Where:**
  - `src/core/mrp_mad.c:353` and `:359`: the LV cells of the rJoinIn!/rJoinMt! rows now issue no indication.
  - `src/core/mrp_mad.c:959`: `changed_in` requires the previous Registrar state to be IN.
  - `src/core/mrp_mad.c:997-1001`.
  - `doc/developer.md:191-192` and `doc/manager.md:37`.
- **Authority:**
  - IEEE 802.1Q-2018 Table 10-4: in LV, a received Join stops the leavetimer and enters IN, with no Join indication. The code now does this correctly.
  - The library's own changed-value contract. This PR documents it at `doc/manager.md:37` ("Changed Listeners notify without separate Leave indications") and tests it in IN (`changed-listener-indication` reversal).
  - IEEE 802.1Q-2018 clause 35.2.4: stream propagation and reservation depend on the current Listener declaration type and Talker values.
- **Evidence:** `scripts/probes/probe_rx.c`, receipts `receipts/probes/rx-head-milan{0,1}.log` and `rx-prev-milan{0,1}.log`. All of these probes give the same result in both profiles.
  - Case `p1a`: a Listener registers as Ready. Then one PDU carries LeaveAll and JoinIn Asking Failed.
    - At head there is no indication. Five more JoinIn Asking Failed messages give none either: `listener_inds=1`, `last_decl=2` (Ready).
    - At `23d9a817`, Asking Failed is indicated.
  - Case `p1b`: a LeaveAll-only PDU followed by the changed JoinIn gives the same result.
  - Case `p1c`: a Talker MaxFrameSize change from 100 to 200 after LeaveAll is not indicated.
  - Case `p1d`: as a control, the same change in IN is indicated.
  - The first missed change already updates the stored value, so `changed_in` stays false from then on.
  - All 60 tests still pass, so no test pins this behaviour.
- **Impact:** every received or transmitted LeaveAll moves registrations to LV. A Listener or Talker change that arrives in that window is lost for the rest of the registration. The application then makes reservation and propagation decisions on a stale declaration. The manager matrix claim at `doc/manager.md:37` is false in LV, and `doc/developer.md:191-192` omits the changed-value case.
- **Required outcome:**
  - Keep the Table 10-4 LV cell for unchanged values.
  - When a changed value arrives in LV, indicate and propagate it as in IN. For example, use `previous->reg != MRP_REG_STATE_MT`.
  - Add Listener and Talker regressions for both ways of reaching LV: received LeaveAll and transmitted LeaveAll.
  - Add a named reversal that restores the IN-only condition.
  - Update `doc/developer.md` and the 35.2.6 row of `doc/manager.md`.
- **Verification:**
  - `probe_rx.c` cases `p1a` to `p1c` must pass in both profiles, and the new reversal must fail the new named tests.
  - I tested a candidate fix in scratch (`receipts/fixcheck.diff`). It makes every probe case pass, and the author's suites still pass with 3896 and 3884 assertions (`receipts/fixcheck-unit-{OFF,ON}.*`).

### R540-2-02 - MAJOR - Conformance, Robustness, Tests, Docs

- **Where:**
  - `src/core/mrp_pdu.c:145`: an unknown later-version MSRP type now enters the generic vector walk.
  - `src/core/mrp_pdu.c:150-211`: it requires a well-formed generic vector structure and an EndMark inside AttributeListLength. `23d9a817` skipped to the AttributeListLength end instead.
  - `doc/integrator.md:154`, `doc/architecture.md:55`, `doc/manager.md:29`, and the PR body.
- **Authority:**
  - IEEE 802.1Q-2018 clause 10.8.3.5: with a higher ProtocolVersion, a Message with an unrecognised AttributeType is discarded, and processing continues with the next Message.
  - The MSRPDU format (IEEE 802.1Q-2018 clause 35.2.2) carries AttributeListLength. A receiver can therefore find a Message's end without understanding its vectors.
  - The Round 3 assignment requires the following valid declarations to be kept.
- **Evidence:** `probe_rx.c`, with the same receipts as R540-2-01.
  - Case `p2`: a ProtocolVersion 1 PDU contains an unknown type-9 MSRP Message, then a valid Listener. The unknown Message's vector has one extra octet inside its AttributeListLength, as a FourPacked byte would add.
    - At head: rc -22, 0 indications.
    - At `23d9a817`: rc 0, 1 indication.
  - Case `p2b`: two trailing octets inside AttributeListLength give the same result.
  - Case `p2c` (control): the author's generic-structure unknown message is still skipped.
  - The upstream test `later_versions_skip_unknown_messages_in_every_application` uses only that generic shape. Nothing pins the AttributeListLength skip.
- **Impact:**
  - Suppose a later-version stream peer adds an attribute type that does not follow the generic MRP vector layout. The receiver then drops every valid Talker and Listener in the same PDU.
  - This reintroduces the R541-1-F2 failure for the stream application.
  - The three pages that say higher versions skip unknown messages are wrong for these messages.
- **Required outcome:**
  - For an unknown MSRP type in a later version, skip to the AttributeListLength end, as `23d9a817` did.
  - Keep the vector-based skip for VLAN and MAC, and keep the strict rejection for the current version.
  - Add a stream regression with a non-generic unknown Message followed by a valid Listener, and a named reversal.
  - Align the three pages and the PR body.
- **Verification:**
  - `p2` and `p2b` must pass in both profiles, and the new reversal must fail its named test.
  - The same scratch candidate (`receipts/fixcheck.diff`) passes `p2`, `p2b` and both unit suites.

### R540-2-03 - MINOR - Tests

- **Where:** these new behaviours have no test:
  - `src/core/mrp_mad.c:530-568`: `map_queue` reserves every destination before publishing any, and records `map_error`.
  - `src/core/mrp_mad.c:634-641`: Registrar rollback and the 1 cs leavetimer retry.
  - `src/core/mrp_mad.c:1029`: the receive error return.
  - `src/core/mrp_mad.c:1268` and `:1378`: poll replay and commit replay.
  - `src/core/mrp_mad.c:887-892`: freeing queued work on destroy.
  - `src/core/mrp_mad.c:997-1001`: changed-value propagation.
  - `src/core/mrp_pdu.c:146`: the new rejection of AttributeLength 0.
  - The documented promises in `src/include/shish_lan/mrp.h:268-271` and `doc/integrator.md:206-213`.
- **Authority:** issue #10 acceptance 2 ("every new behaviour has a test that fails when it is reverted"). This PR also publishes a retention contract that promises these behaviours.
- **Evidence:** reviewer plants in `scripts/plants.py`, receipts `receipts/plants-{OFF,ON}.jsonl`.
  - These single changes build and pass all 60 tests in both profiles:
    - `x02`: no poll replay.
    - `x03`: no Registrar rollback.
    - `x04`: no leavetimer retry.
    - `x05`: receive drops the allocation error.
    - `x06`: partial publication on allocation failure.
    - `x07`: AttributeLength 0 accepted.
    - `x12`: destroy leaks queued work. It survives even with leak detection.
    - `x16`: changed-value propagation dropped.
  - `x10` and `x17` also survive, but they are equivalent mutants and need no test.
  - My fault-injecting probe shows the current code behaves as documented (`scripts/probes/probe_map.c` with `probe_alloc.c`, receipts `receipts/probes/map-head-milan{0,1}.log`). This is a coverage gap, not a behaviour defect.
- **Impact:** the published contract for allocation exhaustion, error reporting, retry and teardown can regress silently.
- **Required outcome:** add tests that use a fault-injecting allocation port for each behaviour above. Add a named reversal for each in `tests/check_reversals.py`.
- **Verification:** re-run `scripts/plants.py` in both profiles. Named tests must kill `x02` to `x07`, `x12` and `x16`.

### R540-2-R1 - RESIDUE - Docs

- **Where:** `doc/tools/README.md:31`.
- **Evidence:** the manager's carried residue (PR comment 6033473193, item R538-2-R2) is not applied. The line still reads "The combined tree includes the required [licence](../../LICENSE) and [notice](../../NOTICE)."
- **Exact fix:** replace the line with "The [licence](../../LICENSE) and [notice](../../NOTICE) links are required and must resolve."
- **Why RESIDUE:** this is prose wording only. It changes no measurement, code, test or conformance claim, and it touches no privacy rule.

### R540-2-R2 - RESIDUE - Docs

- **Where:** `doc/manager.md:91-92`. Comment 6033473193 (item R538-2-R3) gives these lines as `:85-87`; this PR has since moved them.
- **Evidence:** the lines still read "The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) requires the separate licence work and documentation before publication." and "The combined tree includes those licence files."
- **Exact fix:** replace them with "The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) required the licence and documentation before publication." and "The [licence issue](https://github.com/kebag-logic/lwSRP/issues/8) added both files."
- **Why RESIDUE:** this is prose wording only, as for R1.

## Prior public findings at this head

| Prior finding | State | Evidence at this head |
| --- | --- | --- |
| R541-1-F1 (MAJOR): atomic validation and stream-identity wrap | RESOLVED | See note 1. |
| R541-1-F2 (MAJOR) and R540-1-01: higher-version skipping | RESOLVED for the reported cases. A new stream regression is raised as R540-2-02. | See note 2. |
| R540-1-02 and R541-1-F5: switch source | RESOLVED | See note 3. |
| R540-1-03 and R541-1-F6: retained propagation | RESOLVED | See note 4. |
| R541-1-F3: Domain clause | RESOLVED | See note 5. |
| R541-1-F4 and R540-1-07: braces rule | RESOLVED | See note 6. |
| R540-1-04 and R541-1-F7: six surviving reversals | RESOLVED | See note 7. |
| R540-1-05 and R541-1-S2: Milan scope and LeaveAll restart | RESOLVED | See note 8. |
| R540-1-06, R541-1-S1 and parent R532-1 S2: Join indication for LV/rJoinIn! | RESOLVED. Its side effect is raised as R540-2-01. | See note 9. |
| Parent R532-1 S1 | RESOLVED (unchanged) | The LeaveAll-scope regressions still pass, and the scope reversal is still killed. |
| Carried PR #9 residue R538-2-R2 and R538-2-R3 | RETAINED | Not applied. Carried as R540-2-R1 and R540-2-R2. |

Notes to the table:

1. **R541-1-F1.**
   - Decode errors now reject the whole PDU in the validation pass (`src/core/mrp_pdu.c:190-193`).
   - Each increment now reports overflow:
     - stream IDs and destination addresses: `increment_stream` at `src/modules/msrp.c:291-299`;
     - MAC addresses: the carry check at `src/modules/mmrp.c:105-107`;
     - VLAN IDs: the bound check at `src/modules/mvrp.c:71-74`.
   - My own cases, which are not in the upstream tests, pass in both profiles. `23d9a817` fails them (`receipts/probes/fixes-*`).
     - A valid Listener followed by a three-value vector from unique ID 0xFFFE is rejected, with 0 indications and 0 instances.
     - The same vector from 0xFFFD is accepted, with 4 indications.
     - A Domain class of 251 with six values is rejected atomically.
   - These author reversals fail their named tests: `application-decode-error`, `stream-increment-overflow`, `domain-*-range`, `vlan-range` and `mac-increment-overflow`.
2. **R541-1-F2 and R540-1-01.**
   - My cases pass in both profiles:
     - an unknown VLAN type with AttributeLength 4 is skipped;
     - an unknown MAC type with AttributeLength 3 is skipped;
     - an unknown MAC event vector is skipped, and the following vector is kept;
     - an unknown type at the current version is still rejected.
   - These author reversals fail their named tests: `unknown-event-extension`, `current-version-extension` and `unknown-stream-message`.
3. **R540-1-02 and R541-1-F5.**
   - `CMakeLists.txt:8` lists `src/core/switch.c`, and `doc/integrator.md:367` names it for bare metal.
   - `tests/check_embedded.py` links and executes switch dispatch in both profiles (rc 0, `receipts/checks/embedded.log`).
   - The reversal `embedded-switch-source` fails with 4 undefined references.
4. **R540-1-03 and R541-1-F6.** My probe results (`receipts/probes/map-head-milan{0,1}.log`, rc 0 in both profiles):
   - Three ports, with port 1 retaining output. Port 2 receives the propagated Join at once, and port 1 only after its commit.
   - A timer withdrawal is replayed in order, and both ports end in the same Applicant state (VO).
   - An allocation failure while queueing is all-or-nothing. Receive returns the error, and a retry succeeds.
   - A failed replay is kept and drained at the next poll.
   - Destroying the application with queued work leaks nothing under the sanitizer.
   - The named regressions fail as required under the reversals `propagation-retention` and `propagation-order`.
   - Two of my plants are killed: `x01` (no commit replay) and `x13` (value not copied).
   - The contract is stated in `src/include/shish_lan/mrp.h:268-271` and `doc/integrator.md:206-226`.
5. **R541-1-F3.**
   - `doc/developer.md:290` cites 35.2.2.9 for the Domain increment, separately from 35.2.2.8.
   - `doc/manager.md:32` adds 35.2.2.9.
   - The code checks Domain class and priority ranges (`src/modules/msrp.c:306-314`).
6. **R541-1-F4 and R540-1-07.**
   - `scripts/braces.py` checked all 2635 added lines in `1401654530ce..a9cd5ef5` and found 0 unbraced control lines (`receipts/braces-pr.txt`).
   - The remaining unbraced lines all date from the root commit.
7. **R540-1-04 and R541-1-F7.**
   - Each of the six now has a reversal that must fail a named test. Each is killed in both profiles: `committed-local-leaveall`, `omitted-leaveall-event`, `reserved-leaveall-event`, `listener-subtype`, `leaveall-upper-bound` and `reclaim-leaving-observer`.
   - For example, `listener-subtype` fails `changed_listener_redeclares_from_a_quiet_applicant`.
8. **R540-1-05 and R541-1-S2.** Each reversal fails its named test:
   - `milan-redeclare-scope` fails `redeclare_keeps_the_ieee_deadline`;
   - `milan-transmitted-leaveall-scope` fails `transmitted_leaveall_keeps_the_ieee_deadline`;
   - `received-leaveall-restart` fails `received_leaveall_restarts_the_participant_deadline`.
9. **R540-1-06, R541-1-S1 and R532-1 S2.**
   - The LV cells now stop the timer and issue no indication, which matches Table 10-4. This is documented at `doc/developer.md:191-194` and `doc/manager.md:23`.
   - `registrar_recovery_stops_aging_without_duplicate_join_or_map` covers both JoinIn and JoinMt.
   - The `registrar-recovery-indication` reversal is killed, and so is my JoinMt-only plant `x09`.
   - Side effect: changed values in LV are no longer indicated (R540-2-01).

## Lens results

### Conformance

- Table 10-4:
  - The LV/rJoin cells now match the table.
  - The Milan IN/rLv! change still applies to that single cell only, and the scope reversals cover it.
- Clause 10.8.3 receive validation:
  - Whole-PDU validation now covers decoded ranges and vector arithmetic for every application.
  - At the current version, unknown types, unknown events and LeaveAll values 2-7 are rejected.
  - Later-version skipping is correct for VLAN and MAC.
- Clause 35.2.2.9: the Domain clause is cited.
- UNCLEAN because of R540-2-01 and R540-2-02.

### RTL

- The repository and the delta contain no HDL, so I did not use the pinned simulator (`receipts/tools.txt`).
- I applied this lens to the target-facing build instead:
  - the Zephyr and bare-metal source list now includes switch dispatch;
  - `tests/check_embedded.py` passes in both profiles;
  - `tests/check_freestanding.py` passes seven sources per profile, rc 0;
  - the queue entry `struct mrp_map_work` stores at most 48 bytes, the limit that `attr_store_len` enforces;
  - no hosted header was added.
- CLEAN.

### Robustness

- Sanitizer builds (address, undefined behaviour and leak detection) pass all 60 tests in both profiles, with no reports (`receipts/checks/asan-*`):
  - default profile: 3896 assertions, rc 0;
  - Milan profile: 3884 assertions, rc 0.
- The allocation-failure and retention probes pass in both profiles.
- The queue is not re-entered: replayed operations use local Join and Leave events, which the Registrar ignores.
- UNCLEAN because R540-2-01 leaves permanent stale state and R540-2-02 loses whole PDUs.

### Tests

- I ran both profiles from the exact head with out-of-tree builds (`receipts/profiles/`). Configure, build, ctest (1/1), the unit runner and behave all return 0.
  - Default profile: 60 tests, 3896 assertions.
  - Milan profile: 60 tests, 3884 assertions.
  - behave: one feature, three scenarios and ten steps in each profile.
- The other published commands also return 0:
  - the behave dry run;
  - the isolated codec command (1690 assertions);
  - both freestanding commands;
  - the embedded check.
- I ran the author's full reversal driver in both profiles, not just a sample (`receipts/reversals/`).
  - All 60 reversals are detected in each profile, and the restored builds and tests pass.
  - For the nine round-3 reversals I sampled, the per-case logs show failures in exactly the required named tests.
- Reviewer plants, 17 per profile:
  - 7 killed: `x01`, `x08`, `x09`, `x11`, `x13`, `x14`, `x15`;
  - 2 survive as equivalent mutants;
  - 8 survive as real gaps (R540-2-03).
- UNCLEAN because of R540-2-01, R540-2-02 and R540-2-03.

### Docs

- The documentation checks match the PR body figures, and all return 0 (`receipts/doc/`):
  - 904 sentence fragments, none over 25 words;
  - 0 unlinked references;
  - 79 of 79 reference self-tests pass;
  - 345 local links and 19 external URLs resolve, with repository URLs checked through authenticated access;
  - 26 graphs render, the largest with 11 nodes.
- All 43 source anchors land on their named code (`receipts/anchors.txt`).
- I rendered and inspected both new graphs, the integrator retention sequence and the architecture receive flow. Both are readable.
- All 58 tracked files carry the SPDX Apache-2.0 identifier.
- The changed pages follow the owner's rules: every reference is a link, sentences are short and graphs are small. The commit subject is one line.
- UNCLEAN because R540-2-01 and R540-2-02 make these claims false or incomplete:
  - `doc/manager.md:37` and `doc/developer.md:191-192` (R540-2-01);
  - `doc/integrator.md:154`, `doc/architecture.md:55` and `doc/manager.md:29` (R540-2-02).
- R540-2-R1 and R540-2-R2 are residue only.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (R540-2-01, R540-2-02) | `src/core/mrp_mad.c`, `src/core/mrp_pdu.c`, `src/modules/{msrp,mvrp,mmrp}.c` and `mrp.h`, checked against IEEE 802.1Q-2018 Table 10-4, 10.8.3/10.8.3.5, 35.2.2.8/35.2.2.9 and 35.2.4, and Milan v1.2 4.2.7.2.2. Probes `probe_rx` and `probe_fixes`, run at head and at `23d9a817`. | R540-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| RTL | CLEAN | No HDL present. Embedded source list, `check_embedded.py` and `check_freestanding.py` in both profiles; queue storage bounds. | R540-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Robustness | UNCLEAN (R540-2-01, R540-2-02) | Propagation queue, rollback, replay and destroy; fault-injecting probe `probe_map` in both profiles; sanitizer suites in both profiles. | R540-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Tests | UNCLEAN (R540-2-01, R540-2-02, R540-2-03) | ctest, unit runner, behave and the dry run in both profiles; the codec command; 60/60 author reversals in each profile; 17 reviewer plants in each profile; `tests/unit/review_test.c` read in full. | R540-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Docs | UNCLEAN (R540-2-01, R540-2-02; residue R540-2-R1, R540-2-R2) | README.md, CONTRIBUTING.md, `doc/*.md` and `doc/tools/README.md`; all five doc checks; 43 anchors; 2 new graphs viewed; SPDX scan; PR body figures; carried PR #9 residue. | R540-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |

## Real limits

- Hosted CI has no check runs and no statuses at this head, because the repository has no workflow (`receipts/hosted-checks.txt`). All execution evidence here is local.
- I built the unit test framework (version 1.6.3, tag commit `abb74b39`) from source in scratch. The host tools are listed in `receipts/tools.txt`.
- I could not read the IEEE text here. My clause readings match the frozen assignment and the prior public reviews. R540-2-01 and R540-2-02 are also shown as regressions against `23d9a817`, which does not depend on clause wording.
- No Zephyr, target, hardware or network interoperability run was done. Physical calibration was NOT RUN.
- The plants and probes are single-change host runs. The scratch candidate fix shows that a fix is feasible; it is not a reviewed patch.

## Pending manager duties

- Build and judge the final current-dev merge candidate separately from this source validation. The source base is `1401654530ce7d9275de9b901e67df47e5bbc536` and live dev is `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
- Own hosted and act acceptance. None ran here.
- Carry R540-2-01, R540-2-02 and R540-2-03 to the author.
- Put R540-2-R1 and R540-2-R2 on the residue checklist, unless the author applies them in the next round.
- Issues #6, #7, #10 and #11 close only through the merge.
- Publish this report with the files listed in `MANIFEST.sha256`.

R540-2 FINISHED
