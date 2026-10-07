[R540] NEGATIVE - exact head 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9

# R540-1 internal review: kebag-logic/lwSRP PR #12 (issue #10; closes #6, #7, #11)

- Exact head: `86a5f74c028dedec2a0f5bc1c5a258bbd83746b9`, tree `7cf49d0d499d21227764282b9d64c8de86f83758` (verified in the review clone; receipt `receipts/clone-integrity.txt`).
- Reviewed delta: `1a1d6cbe4f971d2d346b948dd2e9716421f211e9..86a5f74c`: the `--no-ff` merge `12a0b77f` of `f4-stack` `ef8a28b9` (19 commits beyond the base; the licence commit `fed1a0d` is already an ancestor of the base) and `86a5f74c` (opt-in Milan rapid withdrawal).
- Scope sources read, in order: CONTRIBUTING.md (no AGENTS.md exists), README.md and doc/, issue #10 body and all comments (assignment, round 2), issues #11, #6, #7 and #1, the PR body, the IEEE 802.1Q-2018 clauses and Milan v1.2 consolidated clause named below, the full diff and history, then the public author packet at milan-fpga `eb9c5a65` (`review-evidence/lwsrpm2-r1`, four files; hashes match its MANIFEST.json).
- Prior public review findings on PR #12: none exist at this head (the PR carries only two review-start notices). The two parent suggestions named in the assignment are resolved or retained below.

## Verdict

NEGATIVE. The Milan option (#11), the LeaveAll scope fix (#7), the MSRP destination (#6), the Domain encoding, PDU splitting, withdrawal/aging and freestanding headers are correct and pass both profiles. Four MINOR findings remain open: a forward-compatibility regression in receive validation, a link regression for embedded builds of the switch interface, silent loss of propagated declarations and withdrawals into a port that holds a refused PDU, and new behaviours whose reversal no test detects (issue #10 acceptance 2).

## Findings

### R540-1-01 - MINOR - Conformance, Robustness, Tests, Docs
- **Where:** `src/core/mrp_pdu.c:133-139` (`parse_pass`); `src/modules/mmrp.c:106-113` (`mmrp_attr_len` returns 0 for unknown types); `doc/manager.md:29`; `doc/integrator.md:151-157`.
- **Authority:** IEEE 802.1Q-2018 10.8.3.5 c) 1): for an MRPDU with a higher protocol version, a Message with an unrecognised AttributeType is discarded and processing continues with the next Message.
- **Evidence:** `scripts/probes/probe_version_mmrp.c`, receipts `probes/version-mmrp-head.log` and `probes/version-mmrp-base.log`. A MAC-application PDU with ProtocolVersion 1, an unrecognised type-9 Message, then a valid MAC Message: head returns -22 with 0 registrations; base `1a1d6cbe` returns 0 and registers the valid MAC. The VLAN application only survives because `mvrp_attr_len` ignores the type; an unknown type with any AttributeLength other than 2 is rejected the same way. Only MSRP skips unknown Messages (through AttributeListLength). No test covers VLAN or MAC unknown types in a later version.
- **Impact:** a later-version VLAN or MAC peer that adds an attribute type causes every valid declaration in the same PDU to be dropped. This is a regression introduced by the new whole-PDU validation. The 10.8.3 matrix row states no such limit.
- **Required outcome:** for ProtocolVersion above the implemented version, skip unrecognised Messages in every application, using the Message's AttributeLength and the vector structure up to the EndMark. Keep version-0 strictness if wanted. Add VLAN and MAC regressions with a planted reversal. Otherwise state the limit on the manager and integrator pages.
- **Verification:** re-run the probe; head must register the valid MAC in the version-1 case, and the new tests must fail on the planted reversal.

### R540-1-02 - MINOR - Robustness, Docs
- **Where:** `CMakeLists.txt:6-14` (embedded module source list); `src/include/shish_lan/switch.h:27-31` (wrappers now out of line); `src/core/switch.c` (new); `doc/integrator.md:294-296` and `doc/integrator.md:332-347`.
- **Authority:** issue #10 scope "the serialized bare-metal integration contract"; integrator guide tells adapters to call `shlan_connect` and friends through the handle.
- **Evidence:** `scripts/probes/module_link.sh` links `scripts/probes/probe_module_switch.c` against exactly the sources named in the embedded module branch. Head: undefined references to `shlan_connect`, `shlan_port_enable`, `shlan_port_disable` and `shlan_disconnect`, rc 1 (`probes/module-switch-head.log`). Base: rc 0, because the wrappers were `static inline` (`probes/module-switch-base.log`). The bare-metal source list on the integrator page also omits `src/core/switch.c`.
- **Impact:** an embedded or bare-metal adapter that uses the switch interface stops linking after this merge.
- **Required outcome:** add `src/core/switch.c` to the module source list, or keep inline wrappers for non-shared builds. Name the file in the bare-metal source list.
- **Verification:** the module-list link probe returns 0; the integrator page lists the file.

### R540-1-03 - MINOR - Robustness, Tests, Docs
- **Where:** `src/core/mrp_mad.c:527-531` and `src/core/mrp_mad.c:545-549` (`map_apply_join` / `map_apply_leave` ignore the result); `src/core/mrp_mad.c:830` and `src/core/mrp_mad.c:847` (refusal while a port retains a refused PDU); `doc/integrator.md:195-201`; `src/include/shish_lan/mrp.h:258-269`.
- **Authority:** the PR's own retention contract (a refusal "leaves every applicant and registrar unchanged"; hosts queue *their* operations) and IEEE 802.1Q-2018 35.2.4 propagation, which the manager matrix lists as present.
- **Evidence:** two-port stream application, port 1 holding a refused PDU (`probes/map-retained.log`, `probes/map-leave-retained.log`). A Talker registered on port 0 never reaches port 1 after output resumes (0 instances, 0 Talker messages in 300 cs; control run: 1 instance, 4 messages). A Talker withdrawn on port 0 by Leave-timer expiry during retention leaves port 1 declaring it (Applicant AA after 300 cs; control run: VO). The host cannot queue these internal propagations. No test or reversal covers propagation during retention.
- **Impact:** a transient transmit refusal on one port silently loses propagated declarations and, worse, withdrawals, so a stale Talker declaration can persist on another port. Single-port end stations are not affected.
- **Required outcome:** defer and replay propagation into retained ports (or otherwise apply it without losing it), add a multi-port regression with a planted reversal, and state the behaviour in the retention contract.
- **Verification:** both probes match their control runs; the new test fails when the deferral is removed.

### R540-1-04 - MINOR - Tests
- **Where:** issue #10 acceptance 2 ("every new behaviour has a test that fails when it is reverted"); `tests/unit/transmit_test.c:163-178`; `tests/unit/integration_test.c:200-224`; `tests/check_reversals.py`.
- **Evidence:** reviewer campaign `scripts/mutate.py`, receipts `mutation/ieee-results.json` and `mutation/ieee-summary.txt`. These single-change mutants build and pass all 45 tests:
  1. `r-tx-leaveall-no-local-rla`: removes the local rLA! after a committed LeaveAll (`src/core/mrp_mad.c:1281-1285`; required by 10.7.6.6 and 10.7.5.20 a).
  2. `r-no-txlaf`: stops delivering txLAF! to values omitted from a full LeaveAll PDU (`src/core/mrp_mad.c:1264-1266`; Table 10-3).
  3. `r-parse-accept-bad-la`: accepts reserved LeaveAllEvent values 2-7 (`src/core/mrp_pdu.c:157`; 10.8.2.6).
  4. `r-listener-subtype-tx`: always encodes Listener Ready on transmit (`src/core/mrp_mad.c:1166-1169`). The redeclaration test sends Asking Failed but checks only the New event.
  5. `r-leaveall-draw-upper`: widens the LeaveAll draw beyond 1.5 x LeaveAllTime (`src/core/mrp_mad.c:663`); three seeds do not reach the bound.
  6. `r-reclaim-lo`: lets reclamation discard an LO Applicant with a pending message (`src/core/mrp_mad.c:965-966`; Table 10-3 note 11 names only VO, AO and QO).
- **Impact:** items 1-3 are reversions of new behaviour with no failing test, against the frozen acceptance. Items 4-6 leave wire-visible or timing defects in new code undetected.
- **Required outcome:** add a test for each, and a matching case in the reversal runner that fails a named test.
- **Verification:** re-run `scripts/mutate.py`; each listed mutant must be KILLED by a named test.

### R540-1-05 - SUGGESTION - Tests
- Milan scope mutants `r-milan-on-redeclare` and `r-milan-on-txla` survive. Issue #11 acceptance is met as written: delayed IN withdrawal and a restarted LV deadline each fail their own test. A check that Re-declare! and txLA! still enter LV with the option on would pin Milan v1.2 4.2.7.2.2's single-cell scope.
- `r-rx-leaveall-no-la-reset` survives: the received LeaveAll restart of the participant LeaveAll timer (pre-existing behaviour, documented at `doc/developer.md:221`) has no test.

### R540-1-06 - SUGGESTION - Conformance (parent R532-1 S2, retained)
- `src/core/mrp_mad.c:341` and `src/core/mrp_mad.c:347` issue a Join indication for rJoinIn!/rJoinMt! in LV. IEEE 802.1Q-2018 Table 10-4 lists only "Stop leavetimer, IN" for that cell. This is a deviation present since the first commit (`d50ca4f`), not introduced here. The code comment "LV: Stop, Join; IN" also misstates the table.
- Effect, measured in both profiles (`probes/lv-join-ieee.log`, `probes/lv-join-milan.log`): each LeaveAll cycle that re-joins a registration produces one extra `is_new=false` indication, and the stream application re-runs propagation. It is documented at `doc/developer.md:190-193` and `doc/manager.md:23`. No test pins either behaviour (`r-lv-join-indication-removed` survives).
- Suggest aligning with the table (noting that it currently masks part of R540-1-03) or pinning the documented behaviour with a test.

### R540-1-07 - SUGGESTION - code rules
- CONTRIBUTING.md:9-11 requires braces on new and changed lines. These changed lines (errno-to-`SHLAN_ERROR` substitutions and one changed guard) keep single-line bodies: `src/core/mrp_pdu.c:27,34,42,74,79`, `src/core/mrp_mad.c:837`, `src/modules/mmrp.c:69,84,89`, `src/modules/msrp.c:262,268,275`, `src/modules/mvrp.c:45,46,59,60,64`. Behaviour is unaffected.

## Parent review suggestions (R532-1)

- **S1 - RESOLVED.** Upstream regressions exist: `tests/unit/integration_test.c:109` (stream, 4 types, 2 ports) and `:117` (MAC, 2 types). Widening the scope (`a-leaveall-scope`) fails both by name (author runner and reviewer campaign). The VLAN application has one type.
- **S2 - RETAINED as SUGGESTION R540-1-06.** It is a deviation from Table 10-4 with the effect stated above. It predates this PR and is documented.

## Lens results

### Conformance
- Milan v1.2 4.2.7.2.2: `reg_event` (`src/core/mrp_mad.c:554-565`) replaces only IN/rLv! with Lv, MT, and only when `milan_rapid_leave` is set. rLA!, txLA! and Re-declare! keep Table 10-4; LV/rLv! stays -x-, so the original deadline holds (tested at 299 and 300 cs). MSRP takes the option from `LWSRP_MILAN` (default OFF); VLAN and MAC constructors leave it false. Matches #11.
- 10.7.5.20: received LeaveAll reaches only that type's instances on the ingress port; the per-participant LeaveAll machine restarts, as the note to 10.7.5.20 allows. Transmitted LeaveAll carries one empty vector per supported type (NumberOfValues 0 is allowed by the 10.8.2.10 notes).
- Table 10-3 was compared cell by cell, including notes 4, 5, 7, 8 and 11; no difference was found. Table 10-4 differs only in the LV Join indication (R540-1-06).
- 35.2.2.1: the destination is 01-80-C2-00-00-0E, pinned for all three applications. 35.2.2.8: Unique ID and destination_address increment. 35.2.2.9: SRclassID and SRclassPriority increment and the VID is kept, with bounds checks. Stored sizes fit the 48-byte store (`probes/sizes.log`: 40-byte Talker Failed).
- Receive validation: whole-PDU validation precedes indications; the final vector may end at the PDU end (10.8.3.4); reserved packed values are rejected. One regression: R540-1-01.
- Milan 4.2.7.1.3: EndMarks are always sent as 0x0000.
- UNCLEAN because of R540-1-01.

### RTL
- Not applicable. The artifact is a standalone C11 library; there is no RTL, synthesis or simulation content in the delta.

### Robustness
- Two-pass parsing, a transactional transmit with exact-byte retention, the send re-entrancy guard, timer unlinking on destroy and reclaim, and allocation-before-replacement were checked by reading and by probes.
- Address and undefined-behaviour sanitizers with leak detection pass all 45 tests in both profiles (`sanitizers/OFF-unit.log` 2659, `sanitizers/ON-unit.log` 2647; rc 0).
- The freestanding check passes six sources in each profile with gcc, and with clang (`freestanding/*.log`, rc 0).
- UNCLEAN because of R540-1-01, R540-1-02 and R540-1-03.

### Tests
- From an exported copy of the exact head, both profiles: configure, build, ctest (1/1), the unit runner and behave all return 0 (`suites/*.rc`).
  - Default profile: 45 tests, 2659 assertions.
  - Milan profile: 45 tests, 2647 assertions.
  - behave: 1 feature, 3 scenarios, 10 steps in each profile.
- Other published commands, rc 0: the dry run (3 scenarios and 10 steps untested by design), and the isolated codec build and run (9 tests, 1690 assertions). These match the PR body and README.
- The author's reversal runner was re-run on that copy: 39/39 detected, restored build and ctest rc 0 (`reversals/author-runner.log`).
- The reviewer sample of 10 author reversals each fails its named tests. This includes the four Milan reversals, which fail exactly `talker_/listener_leave_in_is_immediate`, `leave_in_lv_keeps_the_original_deadline`, and the VLAN/MAC/disabled tests.
- Of 26 reviewer-owned plants, 15 are killed, including `r-milan-on-rla`, `r-milan-from-lv-too` and `r-milan-no-indication`. One of the killed plants (`r-destroy-leave-timer`) was detected by a hang, not by a named test.
- UNCLEAN because of R540-1-01, R540-1-03 and R540-1-04.

### Docs
- Doc checks pass at head: 860 sentence fragments, none over 25 words; 0 unlinked references; 79/79 reference self-tests; 331 local links and 19 external URLs, with repository URLs authenticated; 25 graphs render, maximum 11 nodes (`docs/*.log`, rc 0).
- All 43 source-line anchors point at the intended code (`docs/anchors.txt`).
- The nine new or changed graphs were rendered and inspected; their labels are readable and no edge crosses a node.
- The four reader guides, links-only references and short sentences are kept. The "planned" notes and the #6 and #7 deviation notes are gone.
- The Milan option links Milan v1.2 4.2.7.2.2 and Table 10-4.
- 55/55 tracked files carry SPDX Apache-2.0.
- No host paths, private names, or tool or model names appear in the tree. Commit subjects are single lines.
- UNCLEAN because of R540-1-01, R540-1-02 and R540-1-03, whose required outcomes include page changes.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (R540-1-01) | `src/core/mrp_mad.c`, `src/core/mrp_pdu.c`, `src/modules/{msrp,mvrp,mmrp}.c`, headers, against 802.1Q-2018 10.7.5-10.7.10, Tables 10-3/10-4/10-5, 10.8.2-10.8.3.5, 35.2.2.1/35.2.2.8/35.2.2.9, and Milan v1.2 4.2.7.1-4.2.7.2.2; probes `version*`, `lv-join*`, `sizes` | R540-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| RTL | N/A (no RTL in artifact) | Whole tree: C11 library, CMake, Zephyr module files | R540-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Robustness | UNCLEAN (R540-1-01, -02, -03) | Transmit/retention, parser, reclaim, timers, MAP paths, module source list; sanitizers both profiles; freestanding gcc/clang both profiles; probes `map-*`, `module-switch-*` | R540-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Tests | UNCLEAN (R540-1-01, -03, -04) | ctest, unit runner and behave in both profiles; codec command; dry run; author runner 39/39; reviewer campaign of 36 mutants | R540-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Docs | UNCLEAN (R540-1-01, -02, -03) | README.md, CONTRIBUTING.md, doc/*.md, doc/tools; all doc checks; 43 anchors; 9 changed graphs rendered and viewed; SPDX and hygiene scan; PR body figures | R540-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |

## Real limits

- No hosted CI exists for this repository at this head: 0 check runs and 0 statuses. All execution evidence here is local.
- The unit dependency (cgreen 1.6.3, tag commit `abb74b39`) was built from source in scratch, because no system copy was available. Host: GCC 16.2.1, CMake 4.4.3, behave 1.3.3.
- The embedded module was not built with Zephyr. R540-1-02 is shown by linking the module's source list with the host compiler.
- No target, hardware or network interoperability was exercised. Physical calibration was NOT RUN.
- The reviewer mutation campaign ran in the default profile. The Milan mutants select the option explicitly, so they do not depend on the profile.
- The other reviewer's report was not read.

## Pending manager duties

- Build and judge the final current-dev merge candidate (source base `1a1d6cbe`, live dev `09f1841b`) separately from this source validation.
- Own hosted and act acceptance. None ran here.
- Carry R540-1-01 to R540-1-04 back to the author round. Confirm R540-1-05 to R540-1-07 dispositions.
- Issues #6, #7 and #11 are open now; they close only through the PR merge.
- Publish this report with the files listed in MANIFEST.sha256.

R540-1 FINISHED
