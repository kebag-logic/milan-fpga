[R557] NEGATIVE - exact head 60c911b92825a720044e78bed540752c7dd0368e

Two MINOR gate defects remain. Production behavior and both required targets passed the checks described below. Neither finding alleges a failure of the current 311 mutation grades.

Reviewed tree: `356130401dbcb3a47184742b9f4973508f2b72eb`. Full PR base: `ae982af85ec97286bd35b39403926d8f0eaec81d`. Round-6 delta: `625b001173fda5f6401af1dceaef8d8ab86f5ae9..60c911b92825a720044e78bed540752c7dd0368e`, one commit. [Public review start](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6077901753).

Reconstruction followed contribution instructions and README/docs, frozen issue acceptance and public decisions, requirements and port authorities, full diff and history, then public execution evidence. No repository AGENTS.md exists; the supplied session instruction was applied. The [independent verdict and ledger](receipts/independent-verdict.md) were recorded before opening earlier reviewer findings in full. Those findings were then reconciled below. No other current-round report was used.

The governing [assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074245112) limits this lane to the standalone stack. The [comment decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074811248), [dual-target decision](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074877336), and [round-6 class-closure requirements](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6076983832) govern this delta. Consumer integration, submodule admission and firmware-image identity remain later work. Branch `dev-linux` was outside the review.

**R557-5-F1 — MINOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifact: [scripts/check_comments.py:47](https://github.com/kebag-logic/tsn-c-stack/blob/60c911b92825a720044e78bed540752c7dd0368e/scripts/check_comments.py#L47), especially lines 53–56. The assembly scanner checks hashes in the original source and deletes their tails before further inspection. It never checks comments created by preprocessing.

This short compiling control passes:

```asm
#define REVIEW_HASH #
nop REVIEW_HASH review probe prose
```

The definition's second hash has an empty tail, which passes the allowlist. At use, preprocessing produces `nop # review probe prose`; the assembler discards the prose. The original source's use line contains no hash for the gate to inspect.

Evidence: [independent controls](receipts/independent-probes.json), [full-tree reproduction](receipts/assembly-full-tree-probe.json), and [portable script](scripts/preservation_and_probe.py). Appended to `examples/rv32/start.S` in a disposable exact-head copy, it gives full comment-gate rc 0, conditional-matrix rc 0, and RV32 Debug/Release link-and-smoke rc 0. The ordinary direct prose control is refused. An allowlisted tracing control passes. No production source was changed.

Authority: the owner permits only SPDX, requirement and standard-tracing comments; round 6 requires the assembly hiding class closed by construction, including hashes in preprocessor definitions. Related enforcement claims are in [CODING_STANDARD.md:31](https://github.com/kebag-logic/tsn-c-stack/blob/60c911b92825a720044e78bed540752c7dd0368e/docs/CODING_STANDARD.md#L31) and the comment row of VERIFICATION.

Impact: forbidden prose can survive the mandatory gate in a compiled assembly source. This is executable enforcement behavior, not wording-only residue. The earlier quote-character examples are fixed, but the assembly class remains open.

Required outcome: ensure preprocessing cannot introduce unchecked assembler comments. Either inspect the relevant preprocessed assembly configurations as well as source comments, or close the permitted preprocessing subset against this construction. Keep legitimate SPDX/tracing and required startup builds working.

Verification: the two-line control must compile but make the full comment gate fail; the direct and macro-produced tracing controls must retain their intended result. Add a compiling regression control, replay the unchanged earlier probes, and retain passing Linux/RV32 jobs.

**R557-5-F2 — MINOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifact: [scripts/needle_audit.py:13](https://github.com/kebag-logic/tsn-c-stack/blob/60c911b92825a720044e78bed540752c7dd0368e/scripts/needle_audit.py#L13) and line 37. The default-template list covers selected assertion families but omits the numeric-nearness template.

The compiled control `EXPECT_NEAR(1.0, 2.0, 0.1) << "The difference between";` emits a default diagnostic beginning with that phrase. A table needle `The difference between` nevertheless passes `validate_needles`: it has more than eight characters, appears in one streamed literal, and is absent from the finite template list. Evidence: [source, compilation, actual failure text and audit result](receipts/independent-probes.json); [portable probe](scripts/independent_probes.py).

Authority: round 6 item 4 separately requires the audit to refuse a needle that is a substring of a default GoogleTest template. [VERIFICATION.md:27](https://github.com/kebag-logic/tsn-c-stack/blob/60c911b92825a720044e78bed540752c7dd0368e/docs/VERIFICATION.md#L27) states that default-message fragments are refused.

Impact: the positive audit still accepts a generic default-template fragment from a supported assertion form. The runtime correction works: the companion failing assertion streams a different message, and `matches()` correctly returns false for the phrase appearing only in its default output. This finding does not claim a false runtime catch or invalidate the current campaign.

Required outcome: enforce the default-template exclusion across the assertion forms the inventory and instrumentation accept. Add a compiled numeric-nearness control, and document any deliberately unsupported forms instead of accepting them under a universal claim.

Verification: the demonstrated needle must fail the audit; a specific owned message must pass; the companion default-only match must remain false. Existing short-fragment controls and all 311 named mutation grades must continue to pass.

**Executed evidence**

| Area | Exact-head examination and result |
|---|---|
| C/C++ lexer and assembly controls | Clang 18.1.3 verified from disposable packages; source uses C11 for C/headers and C++20 for C++/headers. All 32 compiling built-in controls reach the expected result. Real tree and mutation fragments pass. [Receipt](receipts/local-linux/comments.log). F1 is an additional compiling control. |
| Conditional regions | All 22 files and 38 non-guard sides compile. Includes the nested-unreachable refusal and assembly symbol controls. Guard placement, macro allowlist, redefinition restrictions and CI invocation inspected. [Matrix](receipts/conditional-results.json), [control log](receipts/local-linux/conditionals.log). |
| Linux | All 21 local gates return zero (diagram rendering was inspected in the hosted artifacts). GCC coverage and Clang address/undefined-behavior sanitizer builds each run 369 instances in seven binaries, with no skips. Leak detection and halt-on-error enabled. [Gates](receipts/local-linux/gates.json), [independent counts](receipts/independent-result-audit.json), [GCC instances](receipts/gcc-instances.log), [sanitizer instances](receipts/clang-sanitizers-instances.log). |
| Coverage | Adjusted 1164/1164 lines and 583/583 branches. Raw ADP is 203/205 lines and 93/100 branches; other measured files are complete. The same inherited exclusions remove two statements and seven arcs. Exact-exclusion controls pass. [Receipt](receipts/local-linux/coverage.log). |
| Mutation | Fresh and optimized-Python reused campaigns each report 311 CAUGHT, zero ESCAPED/ERROR. Reused per-binary XML independently confirms all 329 required killers inside streamed-message delimiters. [Fresh summary](receipts/mutation-results.json), [reused summary](receipts/mutation-reused-results.json), [independent audit](receipts/independent-result-audit.json), [per-binary XML](receipts/mutation-xml/). Report freshness, missing/partial/skipped reports, unknown tests and default-only diagnostic controls pass. [Control log](receipts/local-linux/mutation-controls.log). |
| RV32 | Debug and Release build all three cores with RV32I/ILP32/freestanding flags, restricted headers and whole-archive linkage. Both final ELF files have zero unresolved symbols and pass ADP/ACMP/MAAP smoke checks. Startup, BSS/stack layout, memory subset and completion path inspected. [Results](receipts/local-rv32/results.json), [log](receipts/rv32.log). |
| Preservation | All seven production files are byte-identical across round 6. Their non-comment token streams equal the full PR base. All 311 plant substitutions and killer names are unchanged across round 6; 25 needles changed. Test changes are five message literals. [Production proof](receipts/production-preservation.json), [table audit](receipts/independent-result-audit.json). The earlier public object-comparison proof was reconciled; no new independent 22-object comparison is claimed. |
| Other gates and documents | Boundary controls compile and refuse forbidden dependencies/imports with both compilers; static analysis, licence, privacy, registration, traceability and port-contract controls pass. Restored interface contracts and diagnostic tables inspected against deleted header material. 408 relative links and 251 line links pass, including generated test anchors. [Links](receipts/document-links.json), [gate receipts](receipts/local-linux/). |

The [exact-head PR run](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37909284956) has successful quality and bare-metal jobs. All 14 recorded steps succeeded; none was skipped. Downloaded artifacts contain 22 zero-return Linux gates, 311 caught plants, two passing RV32 configurations and three rendered diagrams. [Job metadata](receipts/pr-run-jobs.json), [artifact audit](receipts/independent-result-audit.json), [selected hosted receipts](receipts/hosted/). The duplicate push run has successful quality and cancelled bare-metal; it is not a second RV32 pass. [Final checks](receipts/pr-checks-final.json). This is evidence inspection, not manager hosted acceptance.

The compact mutation summary merges failures by test name and overwrites two debug messages with release messages for `reentry-guard-removed`. Therefore the fresh and hosted summaries alone independently expose 327/329 messages. The reused per-binary XML preserves both arms and confirms 329/329. This receipt limitation is distinguished from the driver's successful grades.

The specified [round-1 evidence tree](https://github.com/kebag-logic/milan-fpga/tree/2ae0b85299a979413a5ba4b7fe3e3de175967a19/review-evidence/697-r1) contains original-import author receipts, not exact-head manager execution. The [round-6 author statement](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6077884025), current hosted artifacts and reviewer executions are distinct evidence sources. No manager source bank ran at this head; none is claimed or inferred.

**Earlier public findings at this head**

Original severities remain unchanged. Dispositions use the [round-2](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075317932), [round-3](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6075697881), [prior internal](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076927671) and [prior external](https://github.com/kebag-logic/tsn-c-stack/pull/16#issuecomment-6076974636) findings, read after the independent verdict. R557-3 produced no verdict.

| Prior finding | Severity | Disposition and exact-head evidence |
|---|---|---|
| R556-2-F1; R557-2-F1 | MINOR each | RESOLVED. PORTING contains SRP start/NULL stop, admission withdrawal and call timing, source-state flags, Talker Failed meaning, storage, preconditions and counters. Name and 14 meaning-removal controls pass. |
| R556-2-F2; R557-2-F2 | MINOR each | Original direct assembly, SPDX-tail and splice forms RESOLVED. Current controls and unchanged prior probes refuse them. Assembly completeness remains open under F1 above. |
| R556-2-F3 | MINOR | RESOLVED. `maap-stall-unqueued` uses its own frame-count message. The named plant is caught and default-value needles are refused. |
| R556-3-F1; R557-4-F1 | MINOR each | RETAINED in part as R557-5-F1. Every original form is refused, including the quote-character control. The preprocessing-created assembly comment remains unchecked. |
| R556-4-F1 | MINOR | RESOLVED for its C/C++ literal and conditional forms. Compiler tokens and conditional refusal replace the earlier tokenizer rules; unchanged probe reports zero gaps. |
| R556-3-F2; R556-4-F2 | MINOR each | Runtime/default-only grading and original short fragments RESOLVED. The strengthened audit's default-template exclusion remains incomplete as R557-5-F2. |
| R557-1-F1 | MAJOR | RESOLVED. Fresh complete reports and registration checks are enforced; stale/partial/early-exit controls pass and reused campaign succeeds. |
| R556-1-F1 | MINOR | RESOLVED for its 14 weak killers. Specific literals remain; current 329 required killers pass the per-binary audit. |
| R556-1-F2; R557-1-F2 | MINOR each | RESOLVED. Compiler dependency and object-symbol boundary with compiling refusal/pass controls remains green. |
| R556-1-F3; R557-1-F3 | MINOR each | RESOLVED. Separate per-standard links, generated traceability, executable registration reconciliation and missing/unknown controls pass. |
| R557-1-F4 | MINOR | RESOLVED under owner decision. ADP-01, PORTING and DEV-08 preserve and disclose inherited input limits; hosted/RV32 controls pass. Correction remains issue 3. |

Unchanged replay results: R556-3 `comment_probes.py` reports `gaps: 0`; R556-4 `comment_bypass_probe.py` reports `gaps: 0 of 11`; `needle_default_fragments.py` tries 955 fragments per killer and reports zero accepted fragments. R557-4 `full_comment_bypass.py` reports `bypass: false`, with clean gate rc 0 and prose gate rc 1; the script itself returns 1 because it was written to demonstrate the old bypass. One exploratory C23-suffix row in R556-4's script does not compile under local Clang C11 with warnings-as-errors; all six originally assigned rows compile and are refused. [Replay receipts](receipts/prior-replay/), [unchanged-script provenance](receipts/prior-probe-provenance.json).

Adopted/deferred items were also reconciled: R556-2-S2/S3/S4 and R556-3-S1/S2/S3 remain implemented; R556-2-S5 and R556-4-S1's conditional/pragma examples are refused. R556-2-S1's header blank runs remain manager-deferred. R556-2-RS1/RS2 and R556-3-RS1 remain corrected; R556-2-RS3 concerned historical PR wording superseded by the current round-6 body. R556-1-S1/S2/S3 remain implemented; S4's published clause confirmation remains, with independent full-standard corroboration limited. R556-1-R1/R2/R4 remain resolved.

**R556-1-R3 — RESIDUE — Docs — RETAINED**

Artifact: [closed PR #1 body](receipts/closed-pr1-body.md), sentence “Hosted execution awaits publication of this branch.” It remains stale. Authority: the earlier public residue and round-2 disposition. Impact is historical prose only; existing execution measurements and acceptance do not change.

Exact fix: replace that sentence with “Hosted runs [37885778682](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778682) (pull_request) and [37885778700](https://github.com/kebag-logic/tsn-c-stack/actions/runs/37885778700) (push) pass all 16 gates at `b9b9c20`.” Verification: reread the body and confirm the stale sentence is absent. The manager carries this residue; it does not affect verdict or lens cleanliness.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Frozen issue decisions; requirements/deviations; preserved core tokens; port contracts; compiler boundary; round-6 obligations F1/F2 | R557-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| RTL | CLEAN | No HDL or gitlinks in tree/delta; portable-core boundary; RV32 startup/link/runtime; final ELF and smoke results; no hardware assertion | R557-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Robustness | UNCLEAN | Token extraction, conditional reachability, re-entry/backpressure/wrap/input suites, sanitizers, report controls, F1/F2 probes | R557-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Tests | UNCLEAN | 369 instances per compiler; 311 plants/329 per-binary killers; coverage; compiled controls; unchanged replay; hosted executed jobs; missing refusals F1/F2 | R557-5 | 60c911b92825a720044e78bed540752c7dd0368e |
| Docs | UNCLEAN | README/personas; CONTRIBUTING; PORTING/ARCHITECTURE; requirements/traceability; verification/coding claims; import/coverage/analysis registers; PR scope; F1/F2 | R557-5 | 60c911b92825a720044e78bed540752c7dd0368e |

**Limits and pending manager duties**

No full parent, PP, gPTP, synthesis or builder bank was run. No hardware or physical timing was tested. Physical calibration NOT RUN; field skips provide no hardware proof. RTL CLEAN means this standalone delta changes no RTL and preserves the examined software boundary; it is not FPGA acceptance. Standard editions and local interface authorities were reconstructed, but full licensed standards were not independently re-audited.

The manager owns final current-dev candidate validation at the merge turn, including builder/native receipts and their publication on the PR, hosted/act acceptance, two independent positive reviews, publication and the later consumer-integration bar. Source validation at base `ae982af85ec97286bd35b39403926d8f0eaec81d` is distinct from the final candidate involving live dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`.

All review operations used foreground supervisors with bounded concurrent child commands and explicit logs/return codes. Disposable compilers, builds and probe copies stayed under packet `scratch/`. No source fix, commit, push, GitHub write, author contact, shared install or other-checkout edit occurred. [Final integrity](receipts/checkout-final.json) verifies all 70 tracked blob bytes/modes, index, exact head/tree and clean status. Base, prior head and current head contain zero gitlinks; no required submodule pin was altered.

[Replay instructions](REPLAY.md) identify portable scripts. Publish REPORT.md and only files listed in MANIFEST.sha256. Scratch is excluded. Published execution receipts retain results with host locations replaced by neutral placeholders; the redaction receipt records original and published hashes.

R557-5 FINISHED
