[R882] POSITIVE - exact head 287ca1ee96e69f71a5036061d2bf33c564965755

R882-1: external independent review of issues #950/#954 and PR #961.
Tree: `e293283d32580fb8bcfb8fb4dc48d413cda71f68`.
Range: `15168e14..287ca1ee96e69f71a5036061d2bf33c564965755`, nine commits, 19 files.

All five lenses were applied. No BLOCKER, MAJOR, MINOR or RESIDUE finding remains from this review. This verdict covers the source head, not a future merge candidate or permission to merge.

## Scope and authority

Reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md, [issue #950](https://github.com/kebag-logic/milan-fpga/issues/950) and its public takeover/review-ready comments, [issue #954](https://github.com/kebag-logic/milan-fpga/issues/954), REQUIREMENTS.md, the AECP applied/changed contract, platform ports, and the diff/history. Public execution evidence was inspected after the independent source pass. No private author material or other reviewer's report informed the verdict.

The frozen scope repeats SET_STREAM_FORMAT's own running check after acknowledgement: binding for STREAM_INPUT, streaming for STREAM_OUTPUT. Refusal leaves the change undone, returns STREAM_IS_RUNNING or ENTITY_MISBEHAVING if unobservable, and emits no command notice. Inputs 1-7 retain #947's serialization. Other waiting commands retain their existing behavior. #954 supplies GET_TX_STATE's REGISTERING_FAILED from the registrar state at every output at both one-interface shapes.

Checked the normative text of IEEE 1722.1-2021 7.4.9.1/2 and the ACMP flag definition, and Milan v1.2 5.4.2.7/Table 5.47. Milan explicitly distinguishes bound inputs from streaming outputs. IEEE requires the current format in the response, including the old value on failure. Table 5.47 conditions REGISTERING_FAILED on Listener Asking Failed registration, without a Talker-declaring prerequisite.

The [2026-11-15 owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745) permits a measured ROM ledger increase as named debt while retaining device fit and timing gates. The [2026-11-18 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6972255348) distinguishes held and reported 8x8/1if rows. The [2026-11-20 decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7044585511) retains owner bounds while restating measured costs.

## Findings and lens results

No findings requiring a source change.

[R882] PASS Conformance - `sw/firmware/ctrl/aecp/aecp_commands.c:126`, `:140`; `aecp.c:952`; `sw/firmware/ctrl/plat/ctrl_plat.c:99`; `third_party/tsn-c-stack/src/acmp.c:1064` - Replay reuses the original brief check and propagates its status. Failure avoids swap, suppresses the command notice, restores the held requester's response and reports the values in force. The source port selects its own interface/index and maps present/non-ready registration to asking_failed. The unchanged ACMP responder assigns only REGISTERING_FAILED; other flags and response fields retain their construction. S13/S14/T1 pass at both shapes and fail against the base implementation.

[R882] PASS RTL - `sw/firmware/ctrl/aecp/aecp.c:472`, `:952`, `:999`; `aecp_commands.c:88`, `:340`; `sw/firmware/ctrl/plat/ctrl_plat.c:201`; `sw/firmware/ctrl/srp/srp_mbx.c:985`; `sw/litex/ctrl_memory.py:329` - No RTL, clocks, resets, CDC, mailbox layouts or submodule pins changed. Verified the saved-change invariant: incoming mutations encounter refusing while waiting; getters and registry operations do not call aecp_note; expiry follows the waiting return; retry processing also waits. Only SET_STREAM_FORMAT records AECP_CHANGE_FORMAT. The saved kind/type/index therefore still identify that waiting command. The platform wrapper retains input 1-7 serialization and republishes retained values on refusal. ACMP validates the source and configured interface before the callback. Registrar fields are the indexed state already used by GET_STREAM_INFO. Memory policy remains point-specific.

[R882] PASS Robustness - `sw/firmware/ctrl/test/test_aecp.cpp:1687`; `test_plat_sinks.cpp:1205`, `:1241`, `:1280`; `aecp_mutants.py:727`; `sw/litex/ctrl_memory_ledger.py:86` - Covered bound/streaming distinctions, failed observation, no replay/no notice on refusal, requester/sequence retention, timeout and late/partial acknowledgement, subsequent accepted commands, and existing context serialization. The shipping application at two interfaces passed 178 tests; the two platform suites passed 15 tests each. T1 covers absent, Asking Failed, Ready, Ready Failed, transitions back to Asking Failed, other-output isolation and departure. The allocator accepts 58.5 and refuses 59.0 RAMB36, including through the product allocator; a widened-entry control is caught.

[R882] PASS Tests - `sw/firmware/ctrl/test/aecp_again_mutants.py:15`, `aecp_mutants.py:727`, `sink_mutants.py:188`, and `receipts/{head,base,aecp-plants,control-plants}/` - Independently reproduced base failures and head passes. All seven new AECP mutations and five re-anchored waiting-command mutations fail their named diagnostics in completed runs. All six control mutations are caught across eleven arm executions. The four rows re-anchored on aecp_again's final body are among those seven, not four additional plants. Re-anchored tests still exercise the original timeout/failure faults. No assertion was weakened. Test-first commit `9ed4fc95` precedes both functional fixes.

[R882] PASS Docs - `sw/firmware/ctrl/aecp/aecp.h:203`, `aecp/README.md:77`, `sw/firmware/ctrl/plat/README.md:86`, `docs/design/SPLIT_CONTROL_MEMORY.md:693`, `:3226`, `tb/verilator/ctrl_split_boot/README.md:133` - The applied contract describes the completion check, status, undone state and notice rule. The platform documents registrar ownership and tests. Section 13 records the full CPU re-measure and separates accepted misses from passing bounds. Memory tables/tests consistently use 58.5, refuse 59.0 and record 2.5 RAMB36 / 10,240 B of debt. Reviewed added source comments under the owner's rule; no new reviewer identity, review round, issue-comment ID or bench-lane label was introduced there. Existing historical wording was not counted as newly introduced residue.

## Reviewer-owned coverage ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 7.4.9; Milan 5.4.2.7/Table 5.47; aecp_commands.c:126/140; aecp.c:952; ctrl_plat.c:99; S13/S14/T1 receipts | R882-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| RTL | CLEAN | aecp_rx/poll/retry; sink_applied/changed; registrar copies; ACMP source dispatch; range/gitlink audit; memory ledger | R882-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Robustness | CLEAN | 178-test shipping application; both 15-test platform suites; refusal/timeout mutations; allocator boundary/control | R882-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Tests | CLEAN | Test-first history; base/head receipts; 12 AECP and 6 control plants; published source gate receipts | R882-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |
| Docs | CLEAN | aecp.h; AECP/platform READMEs; split-memory sections 3/5/13; split-boot README; public scope/evidence | R882-1 | 287ca1ee96e69f71a5036061d2bf33c564965755 |

## Execution and budget evidence

Portable scripts take checkout and packet paths as arguments. All disposable source/builds stayed under `scratch/`. The foreground supervisor ran independent campaigns concurrently, with no more than 16 compiler jobs. No source fixes, commits, pushes, remote writes, hardware operations or prohibited full banks were performed.

| Check | Result and receipt |
|---|---|
| Both full platform sink/stream suites | PASS, 15 tests each; `receipts/head/*platform.log` |
| Shipping application, two interfaces | PASS, 178 tests; `receipts/head/endstation_ax7101_1x1_tdm8-core.log` |
| 8x8 new core test, two interfaces | PASS; `receipts/head/8x8-focused.log` |
| Base production files with current tests | Expected failures at both shapes; `receipts/base/` |
| Seven new AECP + five re-anchored plants | 12/12 caught; `receipts/aecp-plants/results.json` |
| Six control plants | 6/6 caught; `receipts/control-plants/results.json` |
| Memory ledger and widened-entry control | PASS; `receipts/ledger.log` |
| Both flip graders, load and shape-cost graders | PASS; `receipts/flip-1x1.log`, `flip-8x8.log`, `load.log`, `shape-costs.log` |
| Published receipt digest verification | 64 files match published manifest; `receipts/public-evidence-digests.log` |
| Raw tree/index/mode/gitlink audit | PASS; `receipts/integrity.log` |

The [author's published receipts](https://github.com/kebag-logic/milan-fpga/tree/e223b05bea1c1cd8a37fbaca737b5ea28c38b29a/review-evidence/950-r1/author-r1/receipts) supply full CPU measurements, four exact-head firmware shards, coverage, boundary, twin, release-image and linked-platform-size evidence. These are author source-head receipts, not a manager source bank. Digest verification does not independently reproduce execution.

Inspected the CPU table, statement surveys, record-class results, image hashes, group/miss census, final flip grades and platform ledger receipts. Runtime firmware is unchanged from `c7cfba76` to this head; later edits concern tests, docs, ledger policy and budget statements. Selected published final-image comparisons also match the measured images. At 100 MHz, 23,858 cycles with 5% allowance rounds up to 255 us in 5-us units. Both statement columns use 255. The 1x1/1if grader holds queued notice 127.43/130 ms, ACMP 29.15/30 ms, txL 47.98/49 ms and load 0.512/0.70. At 8x8/1if it holds load 0.744/0.75 and transmit 76.81/77 ms; other solved rows remain reported under the owner decision.

Published measurements cover 64 parts per point, 241/240 groups, zero refusals and 0/69 statements exceeded at each point. They retain seven held-egress misses per applicable arm and four largest-command passes over the share at 8x8/1if. These are explicit pre-existing limits, not newly passing rows. The linked platform's 139,304 B ROM need exceeds old capacity by 40 B, supporting the next-half-tile entry. Routed fit and timing are separate duties.

## Limits and execution exceptions

- The first narrowed AECP campaign was refused by its whole-table census before any plant ran. The wrapper was corrected to run the unchanged census/diagnostic-reader controls on the full table before selecting twelve rows. The corrected campaign passed; the first-attempt receipt is retained.
- An extra unfiltered 8x8/two-interface application run crashed in unchanged `Nvm.WholeMapFramingAndEmptySetAreDistinct`. That same case crashes with base production files. `aecp_arms.all_arms` selects the full application at the shipping shape and only named subsets at 8x8; this extra combination is outside that matrix. It is neither passing evidence nor attributed to this delta. The focused 8x8 regression passes separately. The initial supervisor's nonzero status is retained and explained by this extra run and the census refusal.
- Full CPU simulation, full firmware banks, coverage and two-placement simulation were not rerun here; their public receipts were inspected. The published docs-step run includes three SDK-provenance refusals and explicit setup/hosted-recording skips; it is not an unqualified full workflow pass.
- The specified simulator executable reported identity 5.050. No RTL simulation was performed in these focused firmware checks.
- Physical calibration NOT RUN; field skips are not hardware proof. No hardware acceptance is claimed.

## Prior public findings and pending manager duties

The independent verdict and ledger above were written before the final public-findings census. The subsequent read of PR conversation comments, submitted reviews and inline threads found only the two manager review-start comments, zero submitted reviews and zero review threads. No prior public FINDINGS were present to resolve or retain. `public-scope.json` preserves that census.

The manager owns hosted/act acceptance, full current-dev candidate validation with builder/native banks and receipts, device fit/timing acceptance, merge immediately after PR #960 and any rebase, post-merge bench proof, independent-review completion, containment and issue/project closure. No manager source bank ran at this head and none is inferred. A changed merge candidate must be assessed against this ledger's artifacts. The analogous SET_CONFIGURATION/SET_STREAM_INFO replay gap remains the publicly excluded follow-up scope; this review does not claim to fix it.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch, extracted standards and build trees are excluded. Published receipt path redactions preserve original local logs under scratch and do not change outcomes.

R882-1 FINISHED
