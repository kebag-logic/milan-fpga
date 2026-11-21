[R876] NEGATIVE - exact head 0d80f0ed2a880c3a3b2429c669f104801203ec05

External independent review, R876-1, of issues #956/#957 and PR #958. Tree: `14c4607eaceb3369f6debb279ed83d59ad098846`. Reviewed range: `15168e14..0d80f0ed`. All five lenses were applied. Two MAJOR findings and one MINOR remain open. No source changes were made.

## Findings

### R876-1-F1 - MAJOR - Conformance, RTL, Robustness, Tests

**Artifact:** `sw/firmware/ctrl/srp/srp_mbx.c:228`, `reset_interface` at line 1172; `sw/firmware/ctrl/srp/srp_mbx.h:65`; `reset_probe.cpp`, `reset-1x1-if1.log` and `reset-8x8-if2.log` in this packet.

**Authority/evidence:** #957 requires a notice when a Listener registration appears while the source's interface gate is open. Milan v1.2 5.4.5.2/Table 5.22 names the STREAM_OUTPUT's MSRP Listener registration state; IEEE 1722.1-2021 7.5.2 defines the unsolicited notification path. The new `declaration[]` cache survives `reset_interface`, although that function destroys the participant and clears `listener_present[]`. The next indication is compared with the destroyed registration's declaration.

The independent probe registers Ready, closes the gate, cycles the link, reopens the gate, and waits for ordinary declaration work to finish. It verifies there is no Listener registration and the gate is open, clears earlier notice bits, then receives a new Ready. `listener_present[0]` becomes true, but `noticed & 1` is zero. This fails at both 1x1/one interface and 8x8/two interfaces with unchanged production code. This finding requests no notification for the reset itself; it concerns a later, new registration after recovery.

**Impact:** a controller can retain REGISTERING=0 after a post-reset registration, because the new registration owes no GET_STREAM_INFO. Ready Failed and Asking Failed can suffer the same stale-cache comparison. The ordinary registration test never recreates the participant, so it passes despite the defect.

**Required outcome:** the remembered Listener declaration must match the current participant's registration lifecycle. A new post-reset registration under an open gate must create exactly one notice, including when its declaration equals the old participant's. Preserve silence for the reset itself, unchanged repeats, other interfaces and closed gates.

**Verification:** add reset/re-registration coverage to the SRP and composed AECP tests, including every Listener declaration, repeated/coalesced link events, per-interface isolation and unchanged repeats. The supplied probes must pass, and the composed wire test must verify one correctly flagged response per registered controller. Recheck the unchanged memory budget after correction.

### R876-1-F2 - MAJOR - Conformance, RTL, Robustness, Tests

**Artifact:** `sw/firmware/ctrl/test/srp_talker.cpp:365` and line 379; `sw/firmware/ctrl/srp/srp_mbx.c:1452`; `focused.py` phase probes and `phases-1x1-if1.log`, `phases-8x8-if2.log`, `phases-8x8-if1.log`.

**Authority/evidence:** #956's frozen decision requires the changed destination on the model's wire by 30.0 s, with JoinTime and THE TRANSMIT inside the two nominal longest LeaveAll periods. The new latest-case test deliberately selects a withdrawal phase of 700 ms and asserts that the join timer is idle when the hold-off ends. That excludes an active-timer state from the claimed latest-case evidence.

The independent probe preserves production code, hold-off, hold duration and the absolute 30,000 ms assertion. It varies only the withdrawal phase, removes the idle-timer precondition, and observes for 1,500 ms after resumption to measure late frames. Each phase executes in a fresh process. Results:

| Shape | Withdrawal phase | Changed destination timestamp | Deadline timestamp | Request-to-wire |
|---|---:|---:|---:|---:|
| 1x1/one interface | 300 ms | 31,000 ms | 30,300 ms | **30.700 s** |
| 8x8/two interfaces | 400 ms | 31,000 ms | 30,400 ms | **30.600 s** |

The other six phases at each shape pass. All seven sampled phases at 8x8/one interface pass. The shipped 700 ms test passes at all three sampled shapes. The failure is consistent with `transmit` clearing an interface's `tx_due` when its resumed slice finishes, after an intervening tick made that interface due again. The author's public limitation acknowledges the two-interface symptom; the independent run also demonstrates the one-interface 1x1 case.

**Impact:** the stated model acceptance is not established over the timer states the adapter can hold. A changed destination can wait until the next periodic opportunity and exceed the frozen deadline. These are executable model counterexamples, not physical measurements or proof of production-load reachability.

**Required outcome:** cover an active join timer and retain the absolute 30.0 s assertion. Preserve newly owed transmission work across sliced builds, or provide an independently checkable admissible timing model proving why these sequences cannot occur and exercising the real worst case. Selecting only an idle timer, deferring the defect to another issue, or raising the owner bound does not resolve this finding.

**Verification:** the supplied phase probes and composed conflict test must pass under a justified timing model at 1x1/one interface, 8x8/one interface and both interface shapes. Keep plants for the train's added-terms value, omitted/rounded-down terms and premature declaration. Recheck pending-work retention across the slice boundary.

### R876-1-F3 - MINOR - Conformance, Docs

**Artifact:** `docs/reference/FR_NFR.md:427`, the modified SRP/MRP requirements row.

**Authority/evidence:** the row now correctly states 2,977 / 2,973 / 2,970 cs, but later still says the hold-off "stays 2,027" at 8x8/one interface and that changing the two-interface transmit figure declares the destination "10 ms later". The implemented subtraction gives 2,973 cs and makes the count end 10 ms **earlier** when its transmit term grows from 10 to 11 cs. The surrounding explanation still describes the former added-terms protection of the Leave's departure.

**Impact:** the authoritative timing register contradicts the new formula and its direction of change. This is a numerical and contract claim, so it is MINOR rather than wording-only RESIDUE.

**Required outcome:** restate the affected explanation using #956's subtraction, current values and the changed declaration's deadline. Clearly mark retained old figures as historical. The current 8x8/one-interface count is 2,973 cs, and the two-interface count is 2,970 cs; its count ends earlier when the reserved transmit allowance increases.

**Verification:** compare the row against `srp_mbx.c:47`, generated shape constants and timing tests; run the documentation gates. No implementation bound needs to change.

## Independent examination and evidence

Scope was reconstructed from `AGENTS.md`, `CONTRIBUTING.md`, `docs/README.md`, the [#956 contract and public comments](https://github.com/kebag-logic/milan-fpga/issues/956), [#957](https://github.com/kebag-logic/milan-fpga/issues/957), requirements and interface authorities, then the 21-file diff and its 15 commits. The initial takeover's unconditional notice description was superseded publicly by the gate-dependent REVIEW READY scope. The [review start](https://github.com/kebag-logic/milan-fpga/pull/958#issuecomment-7068805976) names this external round.

The primary standard texts were examined directly: Milan v1.2 Stream Destination MAC Address rule, Table 4.3 and 5.4.5.2/Table 5.22; IEEE 802.1Q-2018 10.7.4.3 and 35.2.2.8; IEEE 1722.1-2021 7.5.2. Two nominal longest periods mean 30 s here under the owner's decision. The 15.5 s tolerance edge would give 31 s and is explicitly excluded by that decision; no bound changed during review.

- **Conformance:** checked the derived subtraction in `srp_mbx.c:47`, its 16-bit guard, tick countdown, withdrawal/start point and wire assertions. Shape values are 2,977, 2,973 and 2,970 cs. Mid-centisecond requests can shorten the count by under 10 ms, still above the accepted 29 s floor. Checked the Listener indication and Ignore-on-leave path against pinned lwSRP callbacks, gate/interface selection, STREAM_OUTPUT flag completion, and shared notification delivery. F1/F2 prevent clean coverage; F3 contradicts the documented contract.
- **RTL:** no HDL, mailbox ABI, CDC primitive or submodule pin changes exist in the delta. Examined firmware state ownership: `srp_interface`, `listener`, `reset_interface`, `count_held`, `transmit`, `ctrl_app_srp.c` delivery and `ctrl_app_aecp.c` completion/notification. Bit indexing fits supported source counts; notices use #936's shared bit per source. F1/F2 leave lifecycle and pending-work correctness unclean.
- **Robustness:** examined closed/open gates, wrong interfaces, New/JoinIn repeats, LeaveAll re-registration, Ignore/leave, same/different destinations, allocation refusal, refused withdrawal, link reset and active-timer/sliced-build ordering. Existing suites pass, but independent reset and phase probes fail.
- **Tests:** read all changed tests and eight #957 plants (five SRP, three AECP), plus #956's revised plants. Negative controls still demand the named failure, rather than accepting any nonzero exit. `declaring_outputs.py` requires two ordered sets of output-0 notices and REGISTERING from the second set; this corrects pre-#957 silence. Its missing/extra/wrong-output controls remain. Reset lifecycle and active-timer cases are missing from the new passing acceptance tests.
- **Docs:** examined both firmware READMEs, `MAILBOX_SPLIT.md`, `FR_NFR.md`, `SPLIT_CONTROL_MEMORY.md` section 13, changed harness texts, PR body and public evidence. New source comments name behavior, reasons, issue and requirement IDs; no new prohibited bench/reviewer identifier was found. F3 remains open. No RESIDUE or SUGGESTION finding is needed.

## Executed checks and public receipts

Independent builds and probes used at most 16 concurrent compile jobs, with disposable files beneath this packet's `scratch/`. Commands stayed attached to the session. No source fix, commit, push, GitHub write, hardware operation, container run or full verification bank was performed.

`focused.py <repo> <kind> <shape> <interfaces> --jobs 4` reproduces SRP, composed, AECP, reset and phase checks. `rerun.py` runs existing notification tests from those executables. Each publishable execution has a `.log` and `.rc` receipt. Independent probe failures are review findings, not passing gate results.

- Existing Talker suite: 17/17 at 1x1/one interface, 8x8/one interface and 8x8/two interfaces.
- Composed SRP/ACMP/MAAP suite: 9/9 at 8x8/two interfaces, including conflict timing and #936 delivery tests.
- Existing AECP output and Talker-notice checks: 4/4 at 1x1/one interface, 1x1/two interfaces and 8x8/one interface. This includes every output's new registration test and both existing #936 notification/delivery tests.
- Independent reset probes: fail at 1x1/one interface and 8x8/two interfaces.
- Independent phase probes: 6/7, 7/7 and 6/7 at 1x1/one interface, 8x8/one interface and 8x8/two interfaces respectively.
- Load, flip checks at both product points, and shape check: exit 0. The 8x8/one-interface tx row is 76.86 ms against 77 ms. `ceil((17259 / 100 * 1.05) / 5) * 5 = 185 us`; the revised MAAP cost follows the existing rule, with load 0.744 below 0.75. No budget is raised.
- The independent harness self-test did not finish within its 500-second execution limit. `harness-selftest.log` preserves its partial output; `.rc` is 124 for the review runner timeout, not a harness verdict. No completed self-test result is claimed. The other grading checks completed successfully.
- Final raw-byte audit: exit 0. All 1,936 superproject tracked blobs, file modes and index entries match the exact head. All five required submodule gitlinks and their tracked bytes, modes and indexes match: protocol processor (868 blobs), time processor (115), stream primitives (214), network stack (100) and registration library (65). `audit.log` records full pins and checks. No review execution remains running.

The [public author evidence](https://github.com/kebag-logic/milan-fpga/tree/a58b1c37af70d774b69f6741bb50d3a1b020aa0a/review-evidence/956-r1) was examined after the independent diff pass. All 41 published manifest hashes match. `audit.log` records verification. Four firmware receipts at code head `8845364d` report 75 passing normal verdicts and 826/388/563 caught campaign entries; the eight new registration plants and restored train-value plants are present. Train-failure receipts demonstrate rejection of the earlier implementation. These are author executions, not an independent rerun of the full banks.

Examined the 20-image comparison and platform ledger receipts: the 8x8/one-interface payload ends at 139,246 B (18 B spare); the aligned ledger charge is 139,248 B (16 B spare), against 139,264 B ROM capacity within 58 total RAMB36. These are different accounting boundaries, not a budget change. `PLAT_1X1_2` remains 19,712 B; other platform struct sizes match the unchanged ledger. Production code and image-generation inputs are identical from `8845364d` through the reviewed head; later commits change docs, mutation grouping and Python grading only.

CPU receipts pair 71 probes at 1x1 and 95 at 8x8/one interface. They retain seven known held-egress misses on each side and no new miss; they are a focused sample, not the full formal measurement. Four stated costs sit at their rounded statement. The documentation receipt is 104 steps at `0d80f0ed`; it does not cure F3. Builder receipts explicitly retain NOT RUN arms, including physical calibration. Release-image and twin receipts were read as published evidence, not rerun here.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2, F3 | #956/#957; primary clauses; `srp_mbx.c:47,228`; `FR_NFR.md:427`; phase/reset receipts | R876-1 (applied; no clean covering round) | 0d80f0ed2a880c3a3b2429c669f104801203ec05 |
| RTL | UNCLEAN: F1, F2 | 21-file diff; `srp_mbx.h:65`; `srp_mbx.c:1172,1420`; application delivery/completion; image ledger | R876-1 (applied; no clean covering round) | 0d80f0ed2a880c3a3b2429c669f104801203ec05 |
| Robustness | UNCLEAN: F1, F2 | `srp_talker.cpp`; `srp_gate.hpp`; `test_aecp.cpp`; `reset_probe.cpp`; phase probes | R876-1 (applied; no clean covering round) | 0d80f0ed2a880c3a3b2429c669f104801203ec05 |
| Tests | UNCLEAN: F1, F2 | Changed tests/plant tables; `declaring_outputs.py`; focused execution and public gate receipts | R876-1 (applied; no clean covering round) | 0d80f0ed2a880c3a3b2429c669f104801203ec05 |
| Docs | UNCLEAN: F3 | SRP/AECP READMEs; three changed design/register pages; harness texts; PR and public receipts | R876-1 (applied; no clean covering round) | 0d80f0ed2a880c3a3b2429c669f104801203ec05 |

## Limits and pending manager duties

This verdict and ledger were written before the prior-public-findings check. That check found zero review submissions, zero inline review threads and two PR comments, both review-start announcements. There are no prior public findings to resolve or retain. `public-review-state.json` records the query time, comment URLs and the independent report's pre-check hash. No private author material or another reviewer's report or packet was used.

There is no manager source-bank execution at this head, and none is claimed. The manager still owns the current-dev merge-candidate builder/native banks and their published receipts, hosted/act acceptance, independent review bar, merge authorization and post-merge containment. Source-head evidence is distinct from a merge candidate against live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. This review neither ran nor accepted that candidate.

The manager's post-merge bench measurements at 1x1/one interface and 8x8/one interface remain 29-30 s on the wire; their pending status is not a finding. Physical calibration NOT RUN, skipped contexts and model checks provide no hardware proof. No full parent, processor, synthesis or builder bank was run. Hosted job execution versus skipping was not independently audited here. Late model frames do not establish field occurrence.

Publishable files are listed in `MANIFEST.sha256`; disposable `scratch/` content is excluded.

R876-1 FINISHED
