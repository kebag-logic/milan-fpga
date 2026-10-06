[R509] NEGATIVE - exact head a27808375427859dc357f6bfd0a88842062b20ed

External independent review, round R509-1, issue #664 / PR #674.
Tree: `5519813ecda9827ba2f30a15ede5aa9e66bc4bea`.
Base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
All five lenses were applied independently before examining prior public findings.
Two MINOR findings remain open. One separate wording residue is nonblocking.
No source changes were made.

## Findings

### R509-1-F1: MINOR - Conformance, Docs

Artifact: `docs/reference/FR_NFR.md:366` and `:367`; the matching MAAP rows in the PR body's “Requirement text for owner approval”.

Authority/evidence: The new text says B.3.3 defines conflict handling and governs loss/retry. IEEE 1722-2016 B.3.3 defines MAAP constants and introduces Table B.8. The state-dependent conflict, loss and restart transitions are in B.3.2/Table B.7. B.3.5.5 defines the conflicting-PROBE event; B.3.6.6 defines the DEFEND packet action, neither replacing the transition table. This was checked directly against the standard identified in `standards-identities.json`. Assignment 6009584763 and the review scope require each cited clause to support its claim.

Impact: The approval text attributes normative state-machine behavior to a constants clause and omits its actual transition authority. An implementer following that citation cannot reconstruct the required state-dependent conflict handling. The numeric probe/announcement values and retransmission count are correct.

Required outcome: Cite B.3.2/Table B.7 for conflict handling, loss and retry in both rows, retaining B.3.3/Table B.8 only for constants. Correct the matching owner-approval text. This is not RESIDUE because it changes a clause claim.

Verification: Re-read both corrected rows against B.3.2/Table B.7, B.3.3/Table B.8, B.3.5.5 and B.3.6.6; verify the public approval text matches the corrected head.

### R509-1-F2: MINOR - Conformance, Robustness, Tests, Docs

Artifact: `docs/reference/FR_NFR.md:357`, `:401`, `:402`, and `:558`; `docs/design/MAILBOX_SPLIT.md:341`.

Authority/evidence: The new timing table enumerates ADP advertiser startup, DISCOVER, GM/link changes, periodic AVAILABLE and shutdown. H-ADP ends at locally transmitted AVAILABLE/DEPARTING and lists advertiser cases. H-ACMP measures ACMP RX-to-response, originated-command-to-response and timer actions. Neither explicitly defines the received ADP ENTITY_AVAILABLE/ENTITY_DEPARTING path through the listener's discovery state and onward to connection actions. The table also lacks a discovery-aging row for TMR_NO_ADP. Its passing mention of separate aging timers is not a path derivation or hook. Milan v1.2 5.6.4.1, Table 5.54 and 5.6.4.5.1-.4 require per-bound-sink processing, received-valid_time aging, interface/available-index handling and discovered/departed events. F0's design expressly leaves this listener machine to F3. The new trace summary cites 5.6.4, so these paths are part of the promised coverage.

Impact: The general service bound and generic state-commit rule remain present, but the integration team can implement every specifically named ADP hook case without timing receipt-to-listener-state/connection-event handling or detecting delayed discovery aging. A mailbox record that triggers a connection action does not end in the locally generated ADP PDU named by H-ADP, while H-ACMP's originated-command measurement starts after that unmeasured work. This leaves the requested per-path timing and test contract incomplete.

Required outcome: Add an explicit listener-discovery timing row and extend a named hook to cover received AVAILABLE, DEPARTING and original TMR_NO_ADP expiry. Identify completion at the required discovery/connection state commitment and, where applicable, subsequent TX commit, with the same total service allowance and separately accounted normative waits. Cite the received-valid_time rule and 5.6.4 transitions; name available-index restart, interface/GM mismatch, departing and expiration checks. Update the matching approval text.

Verification: Trace each Table 5.54 transition to an explicit start, completion, budget and required check. A deliberately delayed listener receive handler or aging event must fail the specified future integration check even when all advertiser timing checks pass. This PR need not implement that future instrumentation.

### R509-1-R1: RESIDUE - Docs

Artifact: PR #674 body, “How to get into the same state” and “Known limitations / out of scope”.

Evidence: The published PR still says “The branch is local and has not been pushed” and instructs the manager to make the commits available before using the prepared body. The same body lists no push or PR creation as if that were its current state. The PR already exposes the exact candidate head.

Impact: Stale preparation wording only; it changes no requirement, clause, measurement, test or verdict.

Exact fix: Replace the two opening preparation sentences with: “The candidate is published in PR #674 at `a27808375427859dc357f6bfd0a88842062b20ed`.” In the limitations list, prefix the executor-action statement with “During the executor's local validation phase,” so it is explicitly historical. Retain the no-RTL/firmware/test/VERSION-change statement.

Verification: Read the published body against its head and current public availability. Carry this item on the manager's residue checklist.

## Evidence by lens

Conformance: Reconstructed the frozen body with owner decisions [6009576644](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009576644), assignment [6009584763](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009584763), and budget ruling [6009675758](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009675758). `REQUIREMENTS.md:21`, `FR_NFR.md:321` and the split ownership table correctly move all five functions, including AECP notifications/counter serving; retain framing, timestamps, gPTP, media and filtering in fabric; retain all-fabric shipping until acceptance. `standards-audit.md` records primary-clause checks for every numeric entry. The proposed 10 ms is explicitly project policy and fits all listed 10% ceilings. AECP 240/250 ms, ACMP 200 ms, counter spacing, ADP draws, strict MAAP ranges and Milan MRP overrides were independently checked. Findings F1/F2 prevent clean coverage.

[R509] PASS RTL - `docs/ARCHITECTURE_HW_SW_SPLIT.md:31`, `:67`, `:111`; `docs/design/MAILBOX_SPLIT.md:109`; `docs/reference/MAILBOX_CONTRACT.md:17`; `sw/firmware/ctrl_nvm/README.md:130` - The one-owner rule, mixed-placement ordering, 32-bit ring publication, global TX sequence order, one interrupt, bus/HAL boundaries and F1 boot/apply terminals agree with their authorities. Model validation, binding-before-D3 application, rollback/CLOSED and UNREAD write inhibition remain explicit. The raw source delta is 21 Markdown files; no RTL, firmware, tests, defaults, executable generators or gitlinks changed. No new CDC/reset/width implementation needs approval here. Runtime integration remains future work, explicitly stated at split architecture section 5.

Robustness: `FR_NFR.md:334` and `:389` count backlog, TX backpressure, original event/deadline time, final notification recipient, monotonic clocks and observation error. Required checks include malformed inputs, maximum shapes, CPU stalls, reset, wrap, NVM work and both adapters; wire bounds remain separate. Required spacing cannot be removed from the measurement or replaced by a fresh service allowance. F1 fail-closed boot behavior agrees with its README. F2 leaves the listener-discovery loss/aging cases insufficiently explicit.

Tests: `FR_NFR.md:399`, split architecture `:192` and `:226`, and the F0/F1 READMEs correctly distinguish future integration requirements from existing model/access-count evidence. FT, coverage, public-function/state/error tests and mutation obligations match the two public #665 directives. All eleven focused documentation/interface checks have final rc 0. No simulation was run or needed to establish this documentation-only delta. The five named VERSION assertions exist at `csr/sim_main.cpp:355`, `milan_dp/sim_main.cpp:280`, `sim_nxn.cpp:2681`, `sim_gptp.cpp:816`, and `sim_prune.cpp:334`; they retain major 2. The retired hostplane suite is absent at the base; the plan explicitly carries its major-only assertion into a live suite. F2 remains a test-contract gap.

Docs: `audit_documents.py` independently reproduced the published contradiction search: 617 base and 643 candidate query/line records. Reviewed the public handoff's per-file dispositions and expanded searches for categorical ownership restrictions. Current-implementation pages, generated module inventory, persistence/reset contracts and dated history legitimately retain fabric-specific descriptions. Added placement scopes cover the architecture/integration pages; no remaining categorical “never on firmware” prohibition for a moved path was found. This does not turn current implementation inventory into split acceptance. Generated matrix checks pass unchanged. `approval-text.json` verifies old/new text for all eight changed FR/NFR rows, REQUIREMENTS section 1 and both new timing/hook sections, normalizing link labels, table escaping and whitespace only. The body reproduces F1/F2's incomplete requirements and must be updated with their fixes. R1 is wording residue only.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #664 decisions; REQUIREMENTS section 1; FR_NFR sections 3.4.1/3.4.2; four primary standards, identified in standards-identities.json | R509-1, applied; no clean covering round | a27808375427859dc357f6bfd0a88842062b20ed |
| RTL | CLEAN | Split architecture sections 1-5; F0 mailbox design/generated contract; F1 boot/state contract; documentation-only raw diff and unchanged gitlinks | R509-1 | a27808375427859dc357f6bfd0a88842062b20ed |
| Robustness | UNCLEAN (F2) | FR_NFR service timing and seven hooks; Milan 5.6.4/Table 5.54; F0 backpressure/coalescing and F1 failure terminals | R509-1, applied; no clean covering round | a27808375427859dc357f6bfd0a88842062b20ed |
| Tests | UNCLEAN (F2) | FR_NFR hook requirements; split architecture sections 6-7; focused checks; five unchanged VERSION assertions; public validation summaries | R509-1, applied; no clean covering round | a27808375427859dc357f6bfd0a88842062b20ed |
| Docs | UNCLEAN (F1, F2); R1 nonblocking | All 21 changed documents; reproduced ownership sweep/dispositions; generated traceability; PR approval text | R509-1, applied; no clean covering round | a27808375427859dc357f6bfd0a88842062b20ed |

## Validation and real limits

`scope.json`, `ownership-search.json`, `approval-text.json`, `standards-identities.json`, `standards-audit.md` and the focused logs provide the review receipts. The initial TOC, anchor and em-dash runs refused missing pinned Markdown dependencies (rc 2). A private scratch environment installed the hash-locked dependencies; the three reruns passed. Those initial refusals are retained, not relabelled as passes. Other focused checks passed on their first execution. The foreground driver joined every process and used at most four concurrent checks.

The fixed public [evidence commit](https://github.com/kebag-logic/milan-fpga/tree/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1) contains the author's handoff and prepared body, including command results and artifact digests. Those are public validation claims, not independent review verdicts. Raw bank logs are not included in that directory. The assignment separately states that the manager's complete source static/builder and native banks passed; they were not rerun or claimed as independently executed here. Historical placement calibration NOT RUN, field skips and physical-test skips are not hardware proof.

`hosted-summary.json` is an exact-head observation, not hosted acceptance: several digital jobs succeeded, others were still running, and the physical job was skipped. The manager owns current hosted/local-replica acceptance. No hosted completion is inferred from a skipped context.

`integrity-final.json` verifies 1,105 root blobs and all 876 required-submodule blobs directly against committed bytes and executable modes, together with complete indexes and pinned revisions. All comparisons pass. The unused external gitlink remains unchanged and uninitialized. No candidate mutation was necessary for this documents-only review; no source edits, commits, pushes, GitHub writes, hardware operations or prohibited banks occurred.

## Prior public findings

The independent verdict and all-five-lens ledger were written before the lookup recorded in `prior-public-findings.json`. The final lookup found zero PR reviews, zero inline review comments, two public review-start comments and seven issue comments. No prior public review findings were present to resolve or retain. No other reviewer report was read.

## Pending manager duties

Resolve F1/F2 at a corrected published head and obtain independent re-review of affected lenses; carry R1 to the residue checklist. Obtain owner approval of the exact corrected requirement text and proposed budget. Publish/accept the source-bank and hosted evidence with skips intact. Validate the final current-dev merge candidate separately from this source review, obtain the complete independent-review bar, and follow authorized merge/post-merge containment and issue-state procedures. The future default flip still owes F2-F5 suites, full stream/counter/audio bench acceptance and the coordinated version chain.

R509-1 FINISHED
