[R508] NEGATIVE - exact head a27808375427859dc357f6bfd0a88842062b20ed

R508-1, internal independent review of issue #664 / PR #674. All five lenses were applied. One MINOR clause-reference defect remains open under Conformance and Docs. One separate wording RESIDUE does not affect coverage. No executable defect is alleged.

Tree: `5519813ecda9827ba2f30a15ede5aa9e66bc4bea`. Source base: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`. The two source commits change 21 Markdown files only. VERSION, firmware, RTL, tests, build scripts and gitlinks are unchanged.

## Findings

**[R508] MINOR Conformance, Docs - R508-1-F1 - docs/reference/FR_NFR.md:366 and :367; PR approval table at receipts/pr-body.md:126 and :127 - Wrong MAAP state-machine authority.**

- **Authority/evidence:** The first MAAP row attributes conflict handling to B.3.3; the second explicitly says B.3.3 governs loss and retry. IEEE 1722-2016 B.3.3 is headed "MAAP constants" and points to Table B.8. B.3.2, "State machine", and Table B.7 define conflicting-input actions and INITIAL/Restart transitions. B.3.5.5 defines the conflicting PROBE event; B.3.6.6 defines the DEFEND action. Those latter citations are valid, but do not make B.3.3 the state-machine clause. `receipts/maap-citation.log` records the source identity and exact candidate claims; printed standard pages 158-160 distinguish the sections. The assignment requires each clause to support its claim.
- **Impact:** Following the requirement's loss/retry authority reaches constants rather than mandatory transitions. The normative audit and owner-approval text are inaccurate. The correct numeric intervals and proposed 10 ms budget are unaffected.
- **Required outcome:** Cite B.3.2 and Table B.7 for conflict-state behavior and loss/retry. Preserve B.3.3/Table B.8 only as the constants authority and retain the valid event/action references. Synchronize the mirrored owner-approval text.
- **Verification:** Re-read the corrected rows against B.3.2/Table B.7, B.3.3/Table B.8, B.3.5.5 and B.3.6.6; repeat approval-text parity and applicable documentation checks at the corrected head. Both affected lenses require re-review. This is MINOR, not RESIDUE, because it changes a clause claim.

**[R508] RESIDUE Docs - R508-1-R1 - PR body, receipts/pr-body.md:200 - Unpublished-branch preparation text remains in the published PR.**

- **Authority/evidence:** The checkout paragraph says the branch has not been pushed and asks the manager to make its commits available. The public PR already advertises this commit; `receipts/source-identity.json` records its identity.
- **Impact:** Stale publication guidance only. No requirement, measurement, test result, generated artifact or conformance claim changes.
- **Exact fix:** Replace the paragraph beginning "The branch is local" with: "The published review candidate is `a27808375427859dc357f6bfd0a88842062b20ed`. Check out that exact commit before reproducing the validation."
- **Verification:** Read the resulting paragraph and confirm its commit matches the public head. Carry this to the manager's residue checklist; it does not make a lens unclean.

## Contract and conformance examination

Reconstruction used AGENTS.md, CONTRIBUTING.md and docs/README.md, then the [issue](https://github.com/kebag-logic/milan-fpga/issues/664), [owner decisions](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009576644), [assignment](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009584763) and [budget ruling](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009675758). Relevant standards and interface contracts preceded the diff/history examination. Published handoff evidence followed the independent diff pass. No private implementation material or other reviewer's report was read.

`REQUIREMENTS.md:23`, `docs/reference/FR_NFR.md:318` and `docs/ARCHITECTURE_HW_SW_SPLIT.md:31` consistently move ADP, ACMP, AECP including notifications/counter serving, MAAP and SRP to selectable owners. Mark II defaults to the core. All-fabric remains supported and remains the shipping default until F2-F5 suite and all-stream/counter/audio-soak acceptance. Framing, timestamps, ingress filtering, gPTP and media remain in fabric. Counter observation and media admission enforcement remain fabric responsibilities even when firmware serves their protocol views.

The single cacheless control hart, static entity-sized state and capacity checks remain. The later hard-core adapter is a porting contract, not an implemented release CPU profile. The [bare-metal directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-5992455815) and [unit-test directive](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6008744385) are reflected in the event loop, static pools, upstream SRP reuse, FT prerequisite, coverage and mutation obligations.

Direct reading used the four standards identified in `receipts/standards-identity.txt`. Numeric and ordering audit of `docs/reference/FR_NFR.md:329`:

| Path | Authority and checked result | 10% comparison |
|---|---|---|
| ADP startup/advertise | Milan 5.6.3.5.2: 0-2 s startup; .3/.4/.5/.7/.9 and Table 5.50: 0-4 s subsequent draw and 5 s advertise timer. Milan 5.6.2 plus IEEE 1722.1 6.2.2.5: valid_time 10 means 20 s. | Smallest positive window extent 2 s gives 200 ms; zero draws are expressly not positive intervals. |
| ADP shutdown | Milan 5.6.3.5.8/.11 requires DEPARTING without a numeric shutdown-response maximum. | Related ADP window gives 200 ms; 10 ms remains project policy. |
| ACMP | Milan 5.5.2.3/Table 5.26 sets all five listed command timeouts to 200 ms. | 20 ms ceiling; retry/probe waits retain separate obligations. |
| AECP AEM/MVU | IEEE 1722.1 9.3.2.6 and Milan 5.4.3.4 distinguish 240 ms response from 250 ms transaction timeout. | 24 ms ceiling; hypothetical 120 ms IN_PROGRESS cadence gives 12 ms. Existing no-IN_PROGRESS policy remains. |
| Notifications/counters | Milan 5.4.5.2/Table 5.22 and IEEE 1722.1 7.5.2 retain response-before-notification and asynchronous triggers. Counter pushes are spaced at least one second per descriptor; stream-counter updates take at most one second under Milan 5.3.7.7/5.3.8.10. Solicited GET_COUNTERS remains a command response. | Spacing gives 100 ms; shared AECP response relation gives 24 ms. No one-second maximum notification-delivery claim is made. |
| Liveness/unlock/Identify | Milan 5.4.5.3: 30-60 s monitor; 5.4.2.2/Table 5.22: one-minute unlock. IEEE 1722.1 7.5.1.2.1: three Identify transmissions separated by 150 ms. | Optional Identify gives 15 ms; this change does not enable it. |
| MAAP | IEEE 1722 B.3.4.1/.2 and Table B.8 support strict 500-600 ms probes, three retransmissions, and strict 30-32 s announcements. | 50 ms ceiling. Numbers pass; state-machine citations fail as F1 records. |
| SRP/MRP | IEEE 802.1Q-2018 10.7.4/10.7.11/Table 10-7, overridden by Milan 4.2.7.1.1/Table 4.3: join 180-240 ms, leave 4500-7500 ms, periodic 900-1500 ms, LeaveAll 9.5-15.5 s. Point-to-point transmit opportunities and centisecond resolution also match. | 18 ms from shortest allowed join interval; timer precision remains separate. |

`T_svc = 10 ms` is proposed project policy requiring owner approval, below every tabulated ceiling. Required/selected normative waits are separately recorded; combined pre/post-wait software overhead gets one budget. Egress and timer tolerances still constrain wire behavior, including draws near MAAP's strict upper bound. F1 is the sole open Conformance finding.

## Other lens results

**[R508] PASS RTL - docs/ARCHITECTURE_HW_SW_SPLIT.md:31, :68, :111; docs/design/MAILBOX_SPLIT.md:102, :169; docs/reference/MAILBOX_CONTRACT.md:10, :256; sw/firmware/ctrl_nvm/README.md:130 - Placement and interface contracts agree.**

Checked single ownership, mixed-placement ordering, coherent fabric snapshots, complete-record publication, 32-bit accesses, no DMA, rings/doorbells/one interrupt, modular SEQ ordering and the bus/HAL/YAML seam. Existing bus adapters are distinguished from a future hard-core adapter. F0's unconnected inputs and default-off switch remain explicit. The F1 summary preserves binding-before-D3 application, rollback, CLOSED refusal, COMPLETE/DEFAULTS/BLANK release and UNREAD write-back hold. F0 access counts and F1 modeled bounds are not promoted to target timing. There is no RTL, CDC, reset, width or executable change in this diff.

**[R508] PASS Robustness - docs/reference/FR_NFR.md:336, :391; docs/ARCHITECTURE_HW_SW_SPLIT.md:53, :123; sw/firmware/ctrl_nvm/README.md:130 - Adverse-path requirements preserve bounds and failure semantics.**

Examined H-ADP, H-ACMP, H-AECP, H-NOTIFY, H-COUNTERS, H-MAAP and H-SRP. They identify mailbox RX/event/deadline starts and TX_HEAD/state commitments, record the final fan-out recipient, and add wire observations where required. Backlog, event-ring delay, CPU stalls, NVM work and full TX rings consume the original budget; newly available space cannot restart the clock. Checks include malformed input, stale tags, zero/max draws, retry, wrap/reset, counter coherency/rate limits, all shapes, both adapters and mixed placements. Late service fails even after recovery. Cross-channel response ordering agrees with [issue #653](https://github.com/kebag-logic/milan-fpga/issues/653). These are integration acceptance obligations, not claims that all instrumentation exists.

**[R508] PASS Tests - docs/reference/FR_NFR.md:391; docs/ARCHITECTURE_HW_SW_SPLIT.md:191, :229; receipts/focused-results.json; receipts/scope-version.log - Focused gates pass and future evidence is stated accurately.**

Eleven independent focused checks ran concurrently, at most eight workers, each with a log and exit receipt. All returned zero: document health/privacy, style, cited paths, solution facts, feature status, generated traceability, wire accountability with controls, contents, fragment anchors, added-line punctuation and generated mailbox consistency. Traceability regenerated in memory without drift and passed its controls. Wire accountability reports 77 checks and zero findings. The punctuation gate judges all 562 added lines and passes 339 controls. These gates do not establish a standards citation's truth; F1 remains despite their passes.

The plan requires deliberately late service and reordered output to fail, retains mutation arms, and requires target composition and bench evidence before the flip. All five named VERSION assertions exist, are byte-identical to the base and still expect `0x00020060`; the CSR parameter remains `32'h0002_0060`. The retired hostplane suite is absent. The plan carries its `VERSION >> 16` assertion into a live suite and checks both architecture identities. No runtime test changes are hidden in this PR.

**Docs applied, UNCLEAN through F1.** `receipts/approval-parity.log` proves all eight changed FR/NFR rows, REQUIREMENTS section 1 and the complete new budget/hooks sections match the public approval text. Only line wrapping, table escaping and link markup are normalized, with no paraphrasing. The PR snapshot hashes identically to the published PR-BODY artifact. F1 is therefore also in the text proposed for owner approval.

The [published handoff](https://github.com/kebag-logic/milan-fpga/blob/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1/author/HANDOFF.md) hashes to its manifest. Its four-search ledger reproduces exactly: 617 base hits and 643 candidate hits, including every locator. `receipts/sweep-reproduction.log` records the census. Independently examined surviving fabric-only phrases, SCOUT references, updated summaries, shipping register/egress documents, F0/F1 contracts and scope notes. Remaining guide labels describe scoped shipping flow; snapshot phrases describe reset domains; persistence comparisons describe retained designs. Historical evidence, generated inventories and supported fabric implementation descriptions do not prohibit selectable placement. No additional ownership contradiction was found. Historical material was inspected only for this requested sweep.

## Prior findings and reviewer-owned ledger

After the independent diff pass, all three public PR discussion surfaces were checked. At observation, there were two review-start comments, no submitted reviews and no inline review comments; no finding preceded this round's public start. No prior findings therefore require resolution or retention. See `receipts/prior-findings-inventory.json`. No other reviewer's report contributed to this verdict.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | REQUIREMENTS.md:23; docs/reference/FR_NFR.md:318, :329; four standards; public scope decisions; F1 | R508-1 applied; F1 open | a27808375427859dc357f6bfd0a88842062b20ed |
| RTL | CLEAN | docs/ARCHITECTURE_HW_SW_SPLIT.md:31, :68, :111; docs/design/MAILBOX_SPLIT.md:102; docs/reference/MAILBOX_CONTRACT.md:256; sw/firmware/ctrl_nvm/README.md:130 | R508-1 | a27808375427859dc357f6bfd0a88842062b20ed |
| Robustness | CLEAN | docs/reference/FR_NFR.md:336, :391; docs/ARCHITECTURE_HW_SW_SPLIT.md:53, :123; sw/firmware/ctrl_nvm/README.md:130; issue #653 | R508-1 | a27808375427859dc357f6bfd0a88842062b20ed |
| Tests | CLEAN | docs/reference/FR_NFR.md:391; docs/ARCHITECTURE_HW_SW_SPLIT.md:191, :229; receipts/focused-results.json; receipts/scope-version.log; public handoff gate table | R508-1 | a27808375427859dc357f6bfd0a88842062b20ed |
| Docs | UNCLEAN | All 21 documentation changes; receipts/approval-parity.log; receipts/sweep-reproduction.log; public approval table; F1 and non-blocking R1 | R508-1 applied; F1 open | a27808375427859dc357f6bfd0a88842062b20ed |

Clean results apply to this documentation change only. They do not approve future implementation or override F1.

## Limits and pending manager duties

- Reviewer execution was limited to focused checks and read-only audits. Full parent, processor, synthesis and builder banks were not repeated. No simulator, vendor implementation run, hardware, container runner, source edit, commit, push, merge or public write was performed.
- The published source handoff reports 91 zero exit receipts, with vendor analysis SKIPPED and builder calibration NOT RUN. Its command table and digests were examined; separate complete raw bank logs are not contained in that public two-file packet. The assignment also reports successful manager source/native validation. Neither statement is reviewer execution or final current-dev candidate acceptance.
- `receipts/hosted-contexts.json` is one exact-head observation, not final acceptance. Some jobs succeeded, others were still running, and the physical job was skipped. Skipped contexts and field skips supply no hardware proof. Hosted/local replica acceptance remains the manager's responsibility.
- The source base matched the assigned live dev tip, but this review did not construct or gate the final merge result. Validate against live dev at merge time and publish source/base/tree identities.
- Fix F1, synchronize approval text and obtain re-review of affected lenses at the corrected head. Obtain owner approval of the exact requirements and 10 ms proposal. Record R1 in the residue checklist. Complete independent external review and ensure no round remains in flight.
- Before merge, accept required source/candidate and hosted evidence and obtain explicit maintainer authorization. After authorized merge, run required containment/integrity checks, preserve their proof limits, and close/move the issue only when the full completion bar is met. F2-F5 target-time, full-stream/counter, audio-soak and VERSION-3 default-flip work remain later implementation obligations.

`receipts/integrity-before.txt` and `receipts/integrity-after.txt` prove root head/tree, raw tracked blob bytes, executable modes, index entries and index flags. They also verify all tracked bytes and indexes of the three required submodules at their gitlinks. The optional external gitlink remains unchanged and uninitialized. No untracked source file remains. No source bytes required restoration.

## Reproduction and publication

Portable scripts are in `scripts/`. Disposable environments and licensed extracts remain exclusively in `scratch/`, excluded from publication. Use a packet-local environment with the hash-locked `tools/markdown/requirements.txt` and PyYAML. Scripts accept checkout/packet paths without embedding machine paths.

```sh
python3 scripts/verify_tree.py <checkout>
python3 scripts/inspect_scope.py <checkout>
python3 scripts/run_focused.py <checkout> <packet>
python3 scripts/check_approval.py <checkout> <packet>/receipts/pr-body.md
python3 scripts/check_sweep.py <checkout> <downloaded-public-HANDOFF.md>
python3 scripts/inspect_maap_citation.py <checkout> "$STANDARDS_DIR" <packet>
```

The sweep input is the exact public handoff linked above. Standard identities are in `receipts/standards-identity.txt`. `MANIFEST.sha256` lists publishable scripts, receipts and this final report with packet-relative paths. Unlisted exploratory inputs and `scratch/` are not publication artifacts.

R508-1 FINISHED
