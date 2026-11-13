[R712] POSITIVE - exact head 084cf7a8455e9fa8e24a0e5bcf57c9557816c819

R712-10: external independent delta review of PR #810, issue #665, author round 31.

All five lenses are CLEAN for this delta. R712-9-F1, R712-9-F2, R711-9 RES-2 and the stale-body residue are resolved. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised. Previously recorded optional suggestions remain explicitly carried below. This is a review verdict, not merge authorization or acceptance of pending merge gates.

Scope and reconstruction

The reviewed tree is `1ca7a215f77761a09bbb7363d70b5926e899628a`. The delta starts at `325514224bcc356a6b43843f1003c2323f09de25`, tree `a3ca67b9b69d9de4ef9da684e56082c4a05d3bae`. That tree equals round 30's source head `5bea2597`. Three ordinary commits change two files: `f150b8cb`, `47e44d73`, `084cf7a8`. No executable behavior, cost, bound, ledger number, gate, HDL or gitlink changes.

I reconstructed from AGENTS.md and CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, then the linked requirements and interfaces. I inspected the full-source delta inventory against `e5f88a8e8b7cf21b873bcf02836844cf64998533`, its relevant memory-document hunks and history, and every line of the round-31 delta. The assigned later-round rule carries untouched implementation verdicts; it does not require re-reviewing all 163 files in the historical source delta.

The round-31 assignment is the maintainer-delegated brief supplied for this review, cross-checked against [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6850895861) and the prior findings' required outcomes. The public decisions preserve the service bounds, the limited cold-cost exception, the ledger caps, and the separate flip obligations. This documentation correction changes none of those decisions. Relevant authorities include REQUIREMENTS.md:49, FR_NFR.md:331, SPLIT_CONTROL_MEMORY.md sections 2, 3, 5 and 13, and MAILBOX_SPLIT.md:271.

I wrote an independent verdict and five-lens ledger before opening the prior reports. I then read the findings, suggestions and limits in [R712-9](https://github.com/kebag-logic/milan-fpga/pull/810#issuecomment-6850656712) and [R711-9](https://github.com/kebag-logic/milan-fpga/pull/810#issuecomment-6850590935). Their reconciliations below do not substitute for the independent delta checks.

Resolved findings

| ID | Original severity; all assigned lenses | Artifact at this head | Authority, impact and required outcome | Verification and disposition |
|---|---|---|---|---|
| R712-9-F1 | MINOR; Docs | `docs/design/SPLIT_CONTROL_MEMORY.md:442,455,456` | The sync had dropped `6eacd76d`'s two corrections: the four-PR composition and both regions' smallest margins. This falsely identified the limiting memory margin. Restore both statements without losing their historical context. | CLOSED. `base-memory.diff` retains #874, #880 with #823, #889 and #888. The paragraph explicitly concerns the pin-move merge, not today's ledger. Independently checking every image/shape row yields minimum ROM slack 288 B and SRAM slack 16 B. `verify_delta.log` records the calculation. |
| R712-9-F2 | MINOR; Docs | `docs/design/SPLIT_CONTROL_MEMORY.md:2323,2331`; round-30 `X-GA8-regrade.log:10`, `X-GA1-regrade.log:10` | Round-29 row margins were attributed to the current image, overstating margin. Use round-30 values with group/instance, explicitly identify unavailable derivations, and point the later bullet only at current figures. | CLOSED. The current aged-window margins are 8.162 and 9.992 ms. Both groups and instances match the receipts. “At most” correctly bounds the unknown all-row minimum. The text expressly says neither arm A's all-row minimum nor either answering-every-port minimum was re-derived in round 30. All four round-29 figures are labelled historical. |
| R711-9 RES-2 | RESIDUE; Docs | `sw/litex/ctrl_memory.py:257,265` | The newly added reason text named a lane. Required fix: name the hybrid XIP work and #665 decision D3 instead, with no ledger behavior change. | CLOSED. Both requested strings changed. Normalizing just those two values makes the entire Python AST identical to round 30. Symbols, tiles and all other syntax are unchanged. No “owed to S14” remains. Published exact-head `test_ctrl_memory.py` ends with 0 failures and PASS. Existing neighbouring lane/ruling wording remains the previously identified #746 material. |
| R712-9 RES-1 = R711-9 RES-1, carried from R712-8 RES-1 | RESIDUE; Docs | Live PR #810 body, captured in `pr-body.md:18,49,81,351,369` | The old body presented round 28. Required outcome: publish the current scope and evidence rather than the obsolete summary. | CLOSED. The live body identifies `084cf7a8`, describes rounds 30 and 31, includes all three fixes, and distinguishes round-30 broad execution from round-31 focused gates. |

The memory calculation uses the unchanged `GRANULE_BYTES = 2048` at `ctrl_memory.py:51`: 112,640 - 112,352 = 288; 56 × 2,048 - 114,672 = 16. One additional SRAM granule adds half a RAMB36, taking the historical platform plan from 59.0 to 59.5.

The timing receipts identify `backlog-adp@program-aged2-7.service.aecp.last.if1` at 11.838 ms and `backlog-adp@verify-aged2-5.service.aecp.last.if0` at 10.008 ms. Subtracting each from its 20 ms bound gives the documented margins. `ctrl_service_budget/run.py:732` selects the minimum only among aged windows, which justifies the explicit limit on the claim.

Earlier findings and optional work

R712-8 F1 / R711-8 F1 (platform ledger) and R712-8 F2 / R711-8 F2 (SRP control) remain CLOSED as independently covered in round 30. Their symbols, caps, controls and measurements' consumers are unchanged by the AST and file-delta checks. Earlier closed findings retain the round-30 reconciliation; no prior closure is reopened by this delta. Moving an open defect to another issue is not treated as resolution.

The following suggestions remain optional and open; none is silently claimed fixed. Their original severity is SUGGESTION, and the original lens assignments are preserved.

| IDs; all attributable lenses | Artifact / evidence | Impact; required outcome if taken; verification |
|---|---|---|
| R712-9 S1 = R711-9 S1; RTL, Robustness | `hdl/milan/mailbox/KL_mbx_dma.sv:185,296,391`; `MAILBOX_SPLIT.md:273` | A misprogrammed ring base could select a register with different latency. Retain the suggestion to reject that base or document/enforce the ring-only precondition; verify with an out-of-ring request. CPU-path and ring-path code are untouched. |
| R711-9 S2; Tests | `tb/verilator/mbx/dma_main.cpp:86` | The latency model can drift from the real mailbox. Retain the optional composed mailbox/mover test with a CPU read behind and alongside a transfer; require the old routing to fail. No test changed. |
| R712-9 S2; Tests | `tb/verilator/ctrl_split_boot/boot_soc.py:73`, `plat_ledger.py:61` | Duplicate override maps can diverge. Retain deriving one from the other or checking equality; verify a deliberately divergent map fails. |
| R712-9 S3; Docs | Published `X-*-compare.txt` receipts | Identical images/samples coexist with differing build-input digests. Retain explaining the differing inputs from evidence; verify that explanation against those artifacts. No cause is inferred here. |
| R712-9 S4; Docs | `tb/verilator/ctrl_split_boot/README.md:125` | Manual sync gates can be omitted. Retain adding the existing gates to the lane recipe; verify the recipe invokes them. |
| R711-9 S3; Conformance, Docs | Section 13; ruling `6842347916`; earlier polls-base STATED receipts | Retain explicitly distinguishing firmware-stated costs from restated grader-table costs in the trigger-2 explanation; verify wording against the ruling and receipts. The prior reviewer accepted the interpretation; this delta does not change it. |
| R711-9 S4, carried from R711-8 S6 / R711-7 S6; Tests | `sw/firmware/ctrl/test/test_aecp.cpp` | Retain an optional test that resumes a notification walk across interfaces after refusal/loss; verify it catches skipped or repeated recipients. |
| R711-8 S7 = R712-8 S6; Docs | Published receipt indexes and `MANIFEST.json` | Retain clarifying post-redaction hash authority or regenerating indexes. Verification here uses `published_sha256` in the archive manifest, not pre-redaction index hashes. |

The PR body's other previously carried suggestions, including R711-7 S2 (persistent mover error redelivery), R711-7 S3-S5 and R712-7 S3 (tier itemisation), retain their prior optional dispositions. Round 31 changes no relevant artifact. The flip's accepted outstanding obligations (#890, #894, #872) remain obligations under the public scope decisions, not findings resolved by this report.

Verification

- `verify_delta.py` PASS: exact head/tree, round-30 source/sync tree equality, exactly two changed files, complete Python AST equality except two reason values, all eight historical image/shape rows' slack, published receipt hashes, and corrected timing claims.
- All 47 selected published files match `MANIFEST.json` at archive `3cb4df23ab4d50650e4945b31063250af797edcb`: the complete round-31 packet and the six round-30 regrades, image/sample comparisons and clean-tree receipts. Raw selected gate and timing receipts are retained under `published/`.
- Local `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 32551422`, `check_em_dash.py --selftest`, `check_py_idiom.py`, and `git diff --check 32551422 HEAD`: each rc 0. Documentation scrub: 0 findings; em-dash check: 0 findings over five added lines, 339/339 arms. The foreground runner waits for all independent checks and keeps separate logs/rc files.
- The author's exact-head `test_ctrl_memory.py` receipt has rc 0, “0 failure(s)” and “RESULT: PASS”, with no SKIP marker. Spot-read ledger controls include wrong symbols, missing symbols, wrong point, cap widening and override misuse. I did not rerun that dependency-heavy test; the local interpreter lacks its required HDL Python dependency. Its published run is explicitly distinguished from my local checks.
- `verify_checkout.py` PASS: every tracked raw blob, mode and stage-zero index entry equals the exact head, including direct per-file verification inside all five required initialized submodules. Root: 1,612 entries; protocol processor 750; gPTP processor 109; lwSRP 65; TSN stack 100; axis 214. The checkout is clean. No source bytes needed restoration.

Reviewer-owned lens ledger

These are delta verdicts at the exact head. Untouched implementation coverage is carried from R712-9 at `325514224bcc356a6b43843f1003c2323f09de25`, with the independence and scope checks above. Every lens was applied; none is credited merely because its name appears.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue decisions and REVIEW READY; REQUIREMENTS.md:49; FR_NFR.md:331; SPLIT_CONTROL_MEMORY.md:442,456,2323; memory/timing arithmetic in verify_delta.log. No bounds or accepted exceptions changed. | R712-10 delta; untouched implementation carried from R712-9 | 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 |
| RTL | CLEAN | delta.diff; ctrl_memory.py:251,271; MAILBOX_SPLIT.md:271; AST equality in verify_delta.log. No clock/reset, CDC, host-port, width or scheduling dependency changed. | R712-10 delta; untouched implementation carried from R712-9 | 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 |
| Robustness | CLEAN | ctrl_memory.py:271,284; published/test_ctrl_memory.log ledger refusal controls; exact invariant ledger symbols/caps and complete AST comparison. Boundary and failure behavior unchanged. | R712-10 delta; untouched implementation carried from R712-9 | 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 |
| Tests | CLEAN | run_checks.py and local logs/rc files; published/test_ctrl_memory.log and rc; round-30 AGED receipts; run.py:732; published hashes. Tests and gates unchanged, and the numerical check uses the correct receipt population. | R712-10 delta; untouched implementation carried from R712-9 | 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 |
| Docs | CLEAN | base-memory.diff; delta.diff; SPLIT_CONTROL_MEMORY.md:442,455,456,2323,2331; ctrl_memory.py:257,265; live pr-body.md. Both MINOR findings rechecked at cause and closed; all requested wording outcomes met. | R712-10 | 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 |

Real limits and pending manager duties

The archive commit contains no cryptographic signature, and no detached signature was found in the packet listing. Verification establishes published-hash integrity, not signer authentication. The earlier reference to a signed packet is not claimed satisfied by a hash alone.

No harness leg, full parent/processor/gPTP bank, synthesis bank, builder bank, hardware campaign, or workflow replica ran in this review. Source execution evidence is the author's published receipts; there is no manager source-bank run at this exact head, and none is inferred. Hosted executed-versus-skipped acceptance remains with the manager; this report makes no fresh hosted-success claim.

The 183,244-cycle 8x8/2if heaviest-pass figure and its 16,756-cycle margin remain unchanged round-30 claims. The published GN8 verdict exposes the maximum pass carrying a store step (88,448), which is a different population and cannot independently prove that all-work-pass maximum. The author discloses this in the live body. The 1x1 GN1 store-step maximum is 166,127; its subtraction from 200,000 is 33,873. No new all-row or all-pass minimum is invented here. Physical calibration is NOT RUN; field skips supply no hardware proof.

The 2.7% cold-cost exception still expires at the 8x8/2if flip. Tier rows and the accepted load/ROM debts remain subject to their public decisions and follow-up gates. This docs-only verdict does not certify the flip, field qualification, or silicon timing.

The manager must publish this report and the manifest-listed receipts, finish exact-head hosted/act acceptance, and validate the current-dev merge candidate with the required builder/native banks at the merge turn. Source base is `e5f88a8e8b7cf21b873bcf02836844cf64998533`; the supplied live development tip is `b7d692952305e4e0e132abb8f99c339eeb17a873`. The live PR metadata still names `dev-soft-core`; this review does not retarget it or confuse its recorded base with the eventual validation base. Merge authorization, the complete independent-review bar, no outstanding round, containment after landing, and public issue/project disposition remain manager/maintainer duties.

Reproduction: from this clone, run `python3 -B <packet>/verify_delta.py`, `DOCS_PYTHON=<pinned-markdown-python> python3 -B <packet>/run_checks.py`, and `python3 -B <packet>/verify_checkout.py`. The archive commit must be present. Only REPORT.md and MANIFEST.sha256-listed files are publication material; scratch is excluded.

R712-10 FINISHED
