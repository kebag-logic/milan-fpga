[R533] NEGATIVE - exact head 50d492c12789e1d80bf11f547e7fe53e02b4bdb9

Round R533-1, external independent review of #665 / PR #690. Four findings remain open: one BLOCKER and three MAJOR. All five lenses were applied; none is clean. No source fix, commit, push, GitHub write, merge, or hardware operation was performed.

The reviewed tree is `89b2d8707c3638521d6669f850ae4f8d6c1a666b`. The parent delta is the two commits after `db9aa8c9b135b34ff3d070a979dee70440b37cc6`. The dependency review covers all 20 commits from lwSRP `19f5796b63652eb1151906de73cb827d4980a53f` through `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da`.

Public scope was reconstructed from the issue body, [F4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), the bare-metal/lwSRP, testing and interface directives, #678, and the [linked-size addition](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030870481). Authorities were read directly: REQUIREMENTS.md, FR_NFR.md, the mailbox contract/design, IEEE 802.1Q-2018 and Milan v1.2. Standard identities are in `receipts/standards.json`; their text is not redistributed. In the 2018 edition, Domain's detailed FirstValue definition is 35.2.2.9; 35.2.2.8 describes stream reservations.

The [public author archive](https://github.com/kebag-logic/milan-fpga/tree/fa19435a86a1569f84db12b001a9823694d2736d/review-evidence/665f4-r1) was examined after the independent source pass. No private author material or another reviewer's report was used. The reviewer-owned negative verdict and ledger were written before the final prior-findings query.

**R533-1-F1 — BLOCKER — Conformance, RTL, Robustness, Tests, Docs**

**Artifact:** `third_party/lwSRP/src/core/mrp_mad.c:354`; `sw/firmware/ctrl/test/srp_walk.cpp:47`; `sw/firmware/ctrl/srp/README.md:142`.

**Authority/evidence:** Milan v1.2 4.2.7.2.2 overrides the generic IEEE Table 10-4 IN/rLv transition for MSRP: it issues the leave indication and enters MT immediately. This implementation uses the generic delayed transition for MSRP too. `Srp.R533_MilanWithdrawalInINIsImmediate` registers Ready, receives Lv while IN, and observes the licence still active at receipt; it stops only at 5000 ms. See `receipts/independent-cases-final.log`. D1 deliberately expects this delay and describes it as normative. IEEE is an independent oracle, but its generic rule does not cancel the Milan profile override.

**Impact:** An explicit withdrawal can leave the talker licensed for five seconds; a bound listener also retains a withdrawn Talker registration. The differential passes while enforcing nonconforming behavior.

**Required outcome:** Apply the Milan IN/rLv override to the MSRP participant and correct D1, its expectations, and the conformance claims in the README, PR and handoff. Preserve generic MVRP behavior and the distinct LV/rLv rule: a withdrawal after LeaveAll must not restart the original deadline.

**Verification:** The independent immediate-withdrawal probe must pass for Listener and Talker registrations. Keep the passing `R533_LVWithdrawalKeepsOriginalDeadline` control and the standing #608 cases. Plant defects that separately delay IN withdrawal and restart LV LeaveTime; each must fail its own test.

**R533-1-F2 — MAJOR — Conformance, RTL, Robustness, Tests, Docs**

**Artifact:** `sw/firmware/ctrl/srp/srp_mbx.c:310`, `:491`, `:568`; `sw/firmware/ctrl/loop/ctrl_loop.c` event/RX/poll ordering; `sw/firmware/ctrl/srp/README.md` link-reset contract.

**Authority/evidence:** Milan v1.2 4.2.7.2.1 and IEEE 802.1Q-2018 35.2.2.9.3/.4 require default Domain parameters after Link Up. The adapter registers no link-event consumer and detects loss only by comparing the current link level in `poll()`. Two independent probes fail:

- After adopting priority 4 / VID 3, enqueue Link Down and Link Up before service. Both events exist, but the adapter retains priority 4 / VID 3.
- Queue `CTRL_LOOP_RX_PER_PASS + 1` Ready frames before Link Down. The first pass resets the participant, but a remaining old frame registers into the new participant while down. Link Up enables the talker without a fresh peer declaration.

The raw failures are in `receipts/independent-cases-final.log`.

**Impact:** A short link interruption can preserve an obsolete Domain or reactivate a reservation from the previous link. The existing interface/reset tests service each edge separately and miss both cases.

**Required outcome:** Preserve ordered link lifecycle transitions per interface, restore defaults on a real restart, revoke old permission, and prevent pre-loss queued records from repopulating the new link's state. Retain the other interface's state and owed output. Update the tests and the claimed reset evidence.

**Verification:** Both independent link probes must pass at one and two interfaces, with adjacent down/up events, RX backlog, full TX rings, and an unaffected second interface. No licence may be restored solely by pre-loss traffic.

**R533-1-F3 — MAJOR — Conformance, RTL, Robustness, Tests, Docs**

**Artifact:** `sw/firmware/ctrl/srp/srp_mbx.c:265`, `:389`, `:450`; `third_party/lwSRP/src/modules/msrp.c` StreamID comparison; `sw/firmware/ctrl/srp/README.md` shared-binding contract.

**Authority/evidence:** IEEE 802.1Q-2018 35.1.2.2 requires a Listener declaration when an interested, ready listener has the matching Talker Advertise. The adapter accepts multiple bindings sharing a StreamID and promises to retain their shared declaration. However, each sink independently writes the same StreamID applicant. The probe binds two sinks with that identity and different destinations, first advertises the second destination, then the first. Sink 0 becomes locally `declared=Ready`; sink 1's later loop iteration withdraws the shared applicant. The wire's last Listener event is Lv at 1200 ms, with no subsequent repair during the 1800 ms observation after the change. See `R533_SharedIdentityRetainsAnEligibleBinding` in `receipts/independent-cases-final.log`.

**Impact:** One still-eligible binding loses its reservation while local state claims Ready. The failure depends on sink ordering; periodic processing does not repair it because desired and declared already agree per sink.

**Required outcome:** Reconcile the shared per-interface StreamID declaration across all accepted bindings before changing its applicant. An ineligible binding must not withdraw a declaration still required by another. If any binding combination is unsupported, refuse it atomically and document that contract instead of accepting inconsistent ownership.

**Verification:** Test both sink index orders, matching/nonmatching destination and VID changes, overlapping rebinds, and final-user unbind. Observe the emitted Listener events and registrar result, not only per-sink bookkeeping. Retain the existing identical-binding tests.

**R533-1-F4 — MAJOR — Conformance, Tests, Docs**

**Artifact:** #665 comment `6030870481`; `sw/firmware/ctrl/test/srp_arms.py:93`; public `author/HANDOFF.md` Resource evidence table at archive `fa19435a`; `sw/firmware/ctrl/app/ctrl_app.c`.

**Authority/evidence:** The public acceptance addition requires the linked RV32 image of composed `ctrl_app`, with text, rodata, data, BSS and static pools, for shipping and maximum supported shapes, plus the base delta. The supplied table and executable arm measure unlinked object totals and separately listed caller-owned storage. There is no linked composed image, link map, separated rodata, or corresponding base comparison in the reviewed archive. The ordinary `ctrl_app` does not instantiate F4. Its existing linked or object size therefore cannot measure F4's composed footprint.

**Impact:** The requested block-RAM sizing evidence remains absent. Successful freestanding object checks establish ABI/runtime properties, but cannot establish the linked composition's size. This finding does not assert that the image exceeds the budget.

**Required outcome:** Supply reproducible linked composition measurements for this head and its base, including actual F4 reachability and entity-sized storage, for both required shapes. Clearly distinguish these measurements from routed resource use and physical timing. Record any publicly authorized acceptance change if this obligation is reassigned.

**Verification:** Rebuild the linked artifacts, inspect the map and sections, account for static pools once, and reproduce the head/base delta. Object summation or an image that discards unreferenced F4 does not satisfy the criterion.

**Independent lens results**

Conformance: Compared the Applicant and Registrar tables, transmit/refusal handling and timers with IEEE 802.1Q-2018 10.7, including Table 10-3 notes, Table 10-4 and LeaveAll's per-attribute-type scope in 10.7.5.20. Examined MSRP address `01-80-C2-00-00-0E`, Domain encoding/adoption, Talker Advertise/Failed, FourPacked Listener events, replacement and MVRP VID 2. Startup declarations satisfy the tested Milan 5.5.2.7 behavior. The independent #608 control passes at the original 5000 ms deadline. Findings F1–F4 prevent clean coverage.

RTL and architecture: The parent diff changes no RTL, register map, shipping configuration, default all-fabric source selection or shipping image. Checked the existing FC mailbox interface, RX readiness, bounded loop passes, global timer ownership, per-interface state, static allocation, licence output, link reset, immutable owed frames and commit ordering. The lens includes software/interface architecture; the absence of an RTL diff does not clear F1–F3.

Robustness: Reviewed malformed/truncated vectors, full rings, exhaustion, timer removal, coalesced ticks, repeated/invalid bindings, startup failure, link loss, shared binding, release reentry refusal/counting and debug assertions. Standing tests pass, but the independent probes expose F1–F3. No source was changed to obtain a passing result.

Tests: Reproduced the 100% ratchet with unchanged exclusions; SRP measures 359/359 lines and 342/342 branch arcs. Verified that `srp_reuse.py` extracts the pinned processor's wire builders and Applicant tables. This is honestly described as a selected differential, not an exhaustive state walk. D2's valid Listener subtype on Lv follows 35.2.2.7.2; D1 is wrong under Milan. The source tests omit the link and mixed shared-binding cases. All six reviewer-planted defects compiled and failed the named tests below.

Docs: Compared the README/API contracts, public assignment/acceptance additions, PR body and archived HANDOFF/GATES/TESTS/UPSTREAM claims with source and executable results. F1 changes a conformance claim and test result, and F4 concerns a missing measurement; neither is wording-only RESIDUE. The archive contains prose, inventories and mutation definitions; it does not contain the raw logs it names. Their summaries are treated as author evidence, not as independently executed gates. No RESIDUE or optional suggestion is needed for this verdict.

**Reviewer-owned coverage ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | IEEE 802.1Q-2018 10.7/35; Milan v1.2 4.2.7/5.5.2.7; lwSRP core/modules; srp_mbx.c; independent-cases-final.log; size acceptance | R533-1, applied; F1/F2/F3/F4 open | 50d492c12789e1d80bf11f547e7fe53e02b4bdb9 |
| RTL | UNCLEAN | parent two-commit diff; FC mailbox contract; ctrl_loop.c; srp_mbx.c; timer.c; mailbox-bus.log | R533-1, applied; F1/F2/F3 open | 50d492c12789e1d80bf11f547e7fe53e02b4bdb9 |
| Robustness | UNCLEAN | srp_mbx.cpp; srp_debug.cpp; srp_latency.cpp; lwSRP receive/transmit/timer tests; independent probes | R533-1, applied; F1/F2/F3 open | 50d492c12789e1d80bf11f547e7fe53e02b4bdb9 |
| Tests | UNCLEAN | srp_walk.cpp; srp_reuse.py; srp_arms.py; coverage.ratchet; coverage.log; mutation receipts; independent-cases-final.log | R533-1, applied; F1/F2/F3/F4 open | 50d492c12789e1d80bf11f547e7fe53e02b4bdb9 |
| Docs | UNCLEAN | srp/README.md; ctrl/README.md; public issue/PR; archive fa19435a HANDOFF/GATES/TESTS/UPSTREAM | R533-1, applied; F1/F2/F3/F4 open | 50d492c12789e1d80bf11f547e7fe53e02b4bdb9 |

**Executable receipts**

All disposable source copies and builds live under packet `scratch/`, which is excluded from publication. Commands ran as foreground processes; independent firmware/coverage campaigns and the two mailbox builds ran concurrently. Campaign compilation was capped at four jobs. There were at most two concurrent HDL builds, each with four child build jobs.

| Check | Result | Receipt |
|---|---|---|
| Normal control suites; SRP adapter/debug/timing/differential at IF=1/2; five shapes at IF=1/2; ten SRP RV32 builds | All reported passing before the driver termination | receipts/firmware.log |
| Existing firmware mutations | 97/97 detected before termination | receipts/firmware.log |
| Complete driver invocation | Exit 143 during the later SRP mutation phase; not claimed as a complete pass | receipts/firmware.rc; firmware-termination.txt |
| Separate SRP campaign and dependency-pin controls | 43/43 mutations and both pin controls pass; exit 0 | receipts/srp-campaign.log |
| Coverage | 15 files at 100% after unchanged exclusions; exit 0 | receipts/coverage.log |
| Mailbox generator and shared RV32 controls | Generator current; 17 controls pass; exit 0 | receipts/focused-static.log |
| Mailbox Wishbone / AXI4-Lite | 316 / 361 checks, zero failures; scoped version 5.050; exit 0 | receipts/mailbox-bus.log |
| Pinned lwSRP unit / behavior suites | 24 tests, 1914 assertions; three scenarios, ten steps; exit 0 | receipts/upstream.log |
| Independent behavior probes | Four failures supporting F1–F3; original-deadline control passes | receipts/independent-cases-final.log |
| Final checkout integrity | Exact parent and four required dependency checkouts; all tracked bytes/modes/indexes match | receipts/final-integrity.log |

The upstream suite initially could not build its unit executable because its test dependency was absent. That attempt is retained. A pinned test dependency was built only in packet scratch; the succeeding run is separate. The first port mutation failed compilation and is not counted as a detection; the corrected compiling plant's test failure is retained separately. Receipt drivers for investigation collect failing tests intentionally; the individual `.rc` files and test tallies, rather than the collector's exit zero, carry their results.

| Reviewer-planted defect | Named test that fails | Receipt |
|---|---|---|
| Suppress static-pool exhaustion count | Srp.ExhaustionDuringEachStartupStageReleasesEveryBlock | receipts/mutant-port.log |
| Force TX interface zero | Srp.StartupDeclaresTalkersDomainAndVlan | receipts/mutant-interface.log |
| Declare Domain priority 2 | Srp.StartupDeclaresTalkersDomainAndVlan | receipts/mutant-domain.log |
| Apply received LeaveAll to the wrong attribute types | Srp.LeaveAfterLeaveAllStopsAtOriginalFiveSecondDeadline | receipts/mutant-lw-leaveall.log |
| Remove Domain vector's class increment | MsrpValues.domain_and_vector_offsets_match_wire_fields | receipts/up-domain-vector.log |
| Deliver callbacks during validation pass | Receive.truncation_respects_complete_vectors_and_pdu_end | receipts/up-validation.log |

Positive controls pass on the unmodified source. Mutation definitions, exact failed observables, portable scripts and raw receipts are listed by `MANIFEST.sha256`.

**Timing, scope and remaining duties**

The reviewed timing tests measure mailbox accesses using a 100 ns/access assumption plus one aggregate 1 ms CPU/preemption allowance and 100 ns uncertainty. The maximum reported normal service is 1.0204 ms, below T_svc=10 ms. Domain, Listener and unbind measurements retain a 200 ms Join wait; expiry starts at the original deadline. The 11 ms stall control rejects the original service budget without resetting its origin. JoinTime is 20 cs, LeaveTime 500 cs, periodic 100 cs, and LeaveAll draws are strictly between 1000 and 1500 cs. These desk measurements do not establish target execution, ingress/egress latency, wire departure, arbitrary backlog bounds or whole-call-chain stack use. Raw IF=1/2 timing receipts are included.

The Apache-2.0 licence/NOTICE and 35 source/header/build/test SPDX entries were checked against the public ownership decision. No conflicting notice was found in that review. Broader licence certification is not claimed. Upstream prerequisite publication, its independent reviews and moving the parent pin to integrated lwSRP main remain manager duties.

There were no prior public review findings on PR #690 to resolve or retain: the post-verdict query returned only the two review-start comments, zero submitted reviews and zero inline comments. `receipts/prior-findings-inventory.json` records the query. The other review remains an independent, manager-tracked obligation.

The assigned current-dev conflicts, the eventual integrated dependency pin, and F3 binding composition absent from the base are not findings. Application licence/MAAP composition, current-dev merge construction, hosted/act acceptance, full repository gates, and post-merge containment remain pending. The supplied manager source-validation statement is distinct from validation of the eventual current-dev candidate; this round did not rerun the prohibited parent/processor/gPTP/synthesis/builder banks or inspect hosted jobs. Physical calibration was NOT RUN; field skips and source-bank passes are not hardware proof. No merge approval is granted.

Final integrity verification independently hashed every tracked blob and checked executable/symlink modes, the complete stage-0 indexes, hidden index flags, parent tree and required gitlinks. The parent, protocol processor, gPTP processor, verilog-axis and lwSRP checkouts are clean. All probes changed disposable copies only. The optional `external` checkout remains uninitialized; its gitlink is unchanged. Publish only REPORT.md and files listed in MANIFEST.sha256; scratch is not publishable.

R533-1 FINISHED
