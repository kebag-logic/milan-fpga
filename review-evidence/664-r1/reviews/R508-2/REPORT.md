[R508] POSITIVE - exact head 8fb296e3e02985aee27ef04cb08278836b734a14

R508-2, internal independent review of issue #664 / PR #674. All five lenses are CLEAN. The prior findings are resolved; no new finding or open residue remains. This verdict covers the documentation candidate, not merge authorization or runtime acceptance.

Tree: `ce846f8ab472d3c9bf605598224ae2521966d928`.
Source base and observed live dev: `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Previous reviewed head: `a27808375427859dc357f6bfd0a88842062b20ed`.

The complete source diff changes 21 Markdown files. The four round-2 commits change only `docs/reference/FR_NFR.md` and `docs/design/MAILBOX_SPLIT.md`. RTL, firmware source, executable tests, VERSION, build scripts, generated mailbox artifacts and gitlinks are unchanged. See `history.txt`, `changed-paths.txt`, `round2-diff.patch` and `integrity-final.log`.

Reconstruction followed repository instructions, documentation authorities, the [frozen issue and owner decisions](https://github.com/kebag-logic/milan-fpga/issues/664), linked interfaces and primary clauses, the source diff/history, and public executable evidence. `INDEPENDENT.md` records the independent verdict and ledger written before reading prior public review findings. No private author material or other checkout was read. Prior clean conclusions stand where unaffected; each lens was also applied to this exact head.

## Prior findings, explicitly resolved

**R508-1-F1 = R509-1-F1: MINOR; Conformance, Docs; RESOLVED.**

- Artifact: `docs/reference/FR_NFR.md:367` and `:368`; the public PR's approval timing and round-2 old/new tables in `pr-body.md`.
- Authority/evidence: Directly checked IEEE 1722-2016 B.3.2/Table B.7, B.3.3/Table B.8, B.3.5.5 and B.3.6.6. The corrected rows use B.3.2/Table B.7 for state-dependent conflict handling, loss and restart, B.3.3/Table B.8 only for constants, and the proper event/action clauses. Numeric intervals and three retransmissions are unchanged. Standard identities are in `standards-identities.txt`.
- Prior impact: The proposal incorrectly directed implementers to constants for mandatory transitions.
- Required outcome: Correct both authorities and synchronize owner-approval text.
- Verification: Clause reading confirms the correction. `check_review.py` verifies exact visible wording for the complete timing/hook sections and all round-2 table entries. `integrity-final.log` and the documentation checks pass.

**R509-1-F2: MINOR; Conformance, Robustness, Tests, Docs; RESOLVED.**

- Artifact: `docs/reference/FR_NFR.md:360`, `:403`, `:411`, `:422`, `:576`; `docs/design/MAILBOX_SPLIT.md:341`; matching approval text.
- Authority/evidence: IEEE 1722.1-2021 6.2.2.5 defines received validity in two-second units, with legal AVAILABLE values 1 through 31. Milan v1.2 5.6.4.1 requires every matching bound sink; Table 5.54 and 5.6.4.5.1-.4 define the transitions. The new rows agree with direct reading of those clauses.
- Prior impact: Advertiser/ACMP hooks could pass without measuring received discovery and delayed aging through connection actions.
- Required outcome: Explicit receive/expiry starts, discovery/connection commitments and subsequent TX completion; one shared allowance; separate normative waits; named adverse transitions.
- Verification: H-DISC starts at AVAILABLE/DEPARTING RX_HEAD publication or the original TMR_NO_ADP deadline. Completion includes each matching sink's discovery/timer and connection commitments and the last resulting TX_HEAD/wire observation. State commitment never restarts the allowance. The check table covers initial discovery, rising index, restart with departed-before-discovered ordering, interface mismatch, GM/domain mismatch, departing, expiry, ignored departure and stale expiry. Validity 1, 10 and 31 is required; unchanged-state input handling still has observable completion. MAILBOX_SPLIT states the same boundary and identifies future F3 implementation. Late listener processing must fail independently of advertiser checks. Approval parity and checkout/archive checks pass.

**R508-1-R1 = R509-1-R1: RESIDUE; Docs; RESOLVED.**

- Artifact: `pr-body.md:246`, reproduction instructions and limitations.
- Evidence and prior impact: The unpublished-branch preparation wording was stale prose only.
- Exact outcome: The body names PR #674 as the review object, supplies `git checkout --detach 8fb296e3e02985aee27ef04cb08278836b734a14`, and labels the executor's no-remote-write account as historical local validation.
- Verification: The live PR head and body still match the reviewed snapshot (`public-state.json`). No unpublished-branch claim remains. The manager can close this residue entry.

Original findings: [R508-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010426351), [R509-1](https://github.com/kebag-logic/milan-fpga/pull/674#issuecomment-6010388957). The inspected inventory contains no submitted reviews or inline review comments; prior findings are in these discussion comments.

## Evidence by lens

**[R508] PASS Conformance - REQUIREMENTS.md:21; docs/reference/FR_NFR.md:321 and :328; docs/ARCHITECTURE_HW_SW_SPLIT.md:30 - Frozen scope and corrected clauses agree.**

All five control functions, including AECP notifications/counter serving, have one selected owner. Mark II defaults to the core; all-fabric remains supported and shipping until F2-F5 acceptance. Media, gPTP, framing, timestamps and filtering retain fabric ownership. VERSION stays major 2. The proposed 10 ms remains project policy requiring owner approval, with independent normative deadlines, ordering and spacing. The listener row's minimum received validity gives a 200 ms ten-percent ceiling; resulting ACMP work retains the tighter 20 ms ceiling from its 200 ms transaction interval. Both contain the 10 ms proposal. MAAP and listener transition claims agree with the examined primary standards. Unchanged timing conclusions from R508-1 stand.

**[R508] PASS RTL - docs/ARCHITECTURE_HW_SW_SPLIT.md:30 and :67; docs/reference/MAILBOX_CONTRACT.md:22; docs/design/MAILBOX_SPLIT.md:109 and :341; sw/firmware/ctrl_nvm/README.md:130 - Interface and ownership boundaries remain coherent.**

Checked exclusive ownership, coherent fabric snapshots, applied state before successful responses, response-before-notification, atomic ring publication, global TX sequence order, 32-bit accesses, one interrupt, no DMA and the bus/HAL/YAML seam. F1 retains binding-before-D3 apply, rollback/CLOSED behavior and UNREAD write-back inhibition. H-DISC uses the existing record/event boundaries without claiming the missing listener accept term exists. No clock/reset/CDC/width implementation changed; future integration remains unapproved by this review.

**[R508] PASS Robustness - docs/reference/FR_NFR.md:335, :403 and :411; docs/design/MAILBOX_SPLIT.md:345 - Adverse listener paths consume the original budget.**

Original deadline timing includes delayed event publication. Backlog, TX stalls, NVM work and all matching sinks share one allowance; only normative waits contribute W. State-only and ignored inputs require completion observations. Guards match their states: a rising available_index refreshes validity after the interface check, while GM/domain rechecking belongs to the restart branch. Departure/expiry and stale-event cases are explicit. Reset, wrap, CPU stalls, maximum supported shapes, both adapters and mixed placements remain required. Eventual recovery cannot excuse late service.

**[R508] PASS Tests - docs/reference/FR_NFR.md:391 and :428; docs/ARCHITECTURE_HW_SW_SPLIT.md:195 and :229; focused-results.json; archive-results.json - Test obligations and evidence limits are explicit.**

H-DISC can reject the formerly omitted late receive/aging work, including state-only completion and subsequent TX. Planted late-service and reordered-output defects remain required. FT, coverage, public-function/state/error tests and retained mutations match the public #665 directives. F0 access counts and F1 model time are not target-loop proof. All five named VERSION assertions still expect `0x00020060`, unchanged from the base; the later plan carries the retired major-only assertion into a live suite. This documents-only lane does not claim implemented runtime instrumentation.

Eleven focused checks ran concurrently, at most four workers, all rc 0: approval/integrity, document health, style, contents, generated matrix, added-line punctuation, feature status, paths, solution facts, generated mailbox consistency and diff whitespace. Two additional metadata-free archive checks ran concurrently, both rc 0. The archive documentation gate explicitly skips Git inventory parity; the checkout gate supplies that check. Logs and individual exit files are retained. No heavy bank or runtime build was repeated.

**[R508] PASS Docs - all 21 Markdown changes; pr-body.md; integrity-final.log; docs.log; matrix.log; archive-docs_check.log - The public proposal matches the candidate.**

Approval verification covers REQUIREMENTS section 1 old/new text, all eight changed FR/NFR rows, both complete timing/hook sections and all eleven round-2 old/new entries. Wording matches exactly after decoding table escaping and replacing links with their visible labels. The listener reference resolves in a checkout and a metadata-free archive without imported documentation files. The generated matrix remains unchanged: 77 modules, zero untested. Document health reports zero findings across 195 Markdown files and 1,081 scrubbed text files. Punctuation checks 594 added lines and passes 339 controls. A focused current-document ownership search found no restored categorical prohibition on moved control work; fabric implementation descriptions remain scoped to the shipping placement.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REQUIREMENTS.md:21; FR_NFR.md:328-426; IEEE 1722 B.3.2-.6; IEEE 1722.1 6.2.2.5; Milan 5.6.4; public scope decisions | R508-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| RTL | CLEAN | Split architecture sections 1-5; MAILBOX_CONTRACT registers; MAILBOX_SPLIT ring/discovery boundaries; F1 boot contract; changed-paths.txt | R508-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Robustness | CLEAN | FR_NFR.md:335-426 and :428-441; MAILBOX_SPLIT.md:341-356; Milan Table 5.54 transitions | R508-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Tests | CLEAN | FR_NFR.md:391-441; split architecture sections 6-7; focused-results.json; archive-results.json; unchanged VERSION assertions | R508-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |
| Docs | CLEAN | All 21 changed documents; pr-body.md; integrity-final.log; docs.log; matrix.log; archive-docs_check.log | R508-2 | 8fb296e3e02985aee27ef04cb08278836b734a14 |

## Real limits and pending manager duties

The fixed [public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/b8faae80174f23ea928a49d0611a21884711c475/review-evidence/664-r1) contains R1's handoff and prepared body, with commands and digests rather than complete raw bank logs. Its downloaded handoff matches the manifest. Current-head evidence appears in [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6010818951) and the current PR body: 93 zero exit receipts with explicit skips. The assignment separately reports passing manager source static/builder and native banks. These are not claimed as reviewer executions.

Physical calibration was NOT RUN. Vendor/field skips and skipped physical contexts supply no hardware proof. Hosted completion was not queried or accepted by this review; hosted/local-replica acceptance remains the manager's duty. Source validation remains distinct from the final candidate constructed from live dev at the merge turn, even though the observed dev SHA still equals the source base.

Before merge, obtain owner approval of the exact requirements and 10 ms proposal, both independent positive reviews, no review in flight, required source/current-dev candidate and hosted/local evidence, and explicit maintainer merge authorization. After authorized merge, complete containment/integrity checks and issue/project closure under their stated proof limits. F2-F5 target timing, all-stream/counter tests, audio soak and the VERSION-3 default flip remain later obligations.

`integrity-final.log` verifies 1,105 parent blobs and all 876 required-submodule blobs: exact bytes, executable/symlink modes, complete stage-zero indexes and pins. Required pins are `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (verilog-axis), `ead8036035affd53ef4b29979190f2f4f67084c0` (protocol processor), and `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (gPTP processor). The unused external gitlink is unchanged. No tracked source bytes were edited, so restoration was unnecessary. No commits, pushes, GitHub writes, merges, author contact, delegated review, container execution, privileged operation or hardware access occurred.

## Reproduction and publication

Portable scripts are at the packet root. Install the repository's hash-locked `tools/markdown/requirements.txt` into `scratch/markdown-deps`; PyYAML is also required. Run `python3 run_focused.py <checkout>`, `python3 check_archive_review.py <checkout>`, and `python3 check_review.py <checkout> pr-body.md`. Drivers join all work in the foreground and retain logs and exit codes. Disposable archives, dependencies and licensed extracts remain under `scratch/`, excluded from publication.

Only REPORT.md and files enumerated in MANIFEST.sha256 are publication artifacts. The manifest uses packet-relative paths and SHA-256 digests.

R508-2 FINISHED
