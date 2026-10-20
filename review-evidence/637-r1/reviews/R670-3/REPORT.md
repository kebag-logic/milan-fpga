[R670] POSITIVE - exact head 1e914414557874648ac5041aff88b96908e0e053

R670-3 external independent delta review of issue #637 / PR #768.

All five lenses are CLEAN for this source head. R669-2-F1, R669-2-F2 and R670-2-F1 are resolved. No open BLOCKER, MAJOR or MINOR remains in the reviewed scope. Wording residue and optional suggestions are collected below; they do not clear physical acceptance or authorize merge.

Tree: `033e6bc1fb66904e7faf7b57929d6c7a28d89732`. Previously reviewed head: `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`. Source base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. Three new commits change seven test/documentation files. There is no change under `hdl/`, `syn/` or `constraints/`, no processor interface change, and no gitlink change.

Independence and scope

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue's frozen acceptance and public decisions, linked requirements/interfaces, source-base diff and history with the round-3 delta examined in detail, then the public receipts. The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295599722) defines the three corrections. The [one-pass ruling](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269988820) remains applicable: map-only transaction, all-map rollback on failure, and held faces until completion.

`independent-initial.md` records the independent verdict and five-lens ledger before prior public findings were opened. The four prior public finding comments were then reconciled. No current other-reviewer report, private author material or management checkout was read. There were no source fixes, commits, pushes, GitHub writes, sub-agents, hardware operations or full-bank executions.

The issue requires parent map persistence/restoration, rollback, documented ownership, retained-record power-cycle tests and preserved or remeasured census/capture. Its board cold-cycle addition remains owed. This report accepts the desk delta only; it does not mark issue #637 complete.

Assigned findings resolved at their causes

| Finding | Disposition | Evidence and verification |
|---|---|---|
| R669-2-F1, MINOR, Tests | RESOLVED | `tb/verilator/milan_dp/sim_nxn.cpp:5496` adds four lone-record windows; `:5523` invokes CRC, layout, id and magic cases; `:5557` raises the page guard from 51 to 59. Each window grades both ports' reset lists, both RAMs and public PP_STAT done 1/busy 0/fail 0/blank 1. `dynmap_mutants.py:414` onward removes the three validated-record predicate terms independently, without altering the adjacent restore-refusal predicate. Published rows 61/62/63 fail their named blank checks, respectively 1/2/1 failures of 649. The independent byte probe confirms exactly one failed frame field per case. |
| R669-2-F2, MINOR, Docs | RESOLVED | `docs/reference/REGISTER_MAP.md:2378` and the PP_STAT row at `:2403`, plus `docs/design/SAVED_STATE_MATERIALIZATION.md:1499`, now state that map restore adds no cause: D3 cause is zero and binding cause is preserved. This matches `milan_datapath.sv:5347` (D3 cause/rollback start gate), `:2845` and `:9316` (binding cause passes through), and `hdl/common/csr/milan_csr.sv:670`. A simultaneous binding failure no longer contradicts the description. |
| R670-2-F1, MINOR, Tests and Docs | RESOLVED | PR body round-2 validation rows, public HANDOFF round-2 Gates table and [issue correction](https://github.com/kebag-logic/milan-fpga/issues/637#issuecomment-6298458163) separately report full campaign rc 2, 63/65; listener rerun rc 0, 2/2; aggregate 60 caught controls and five clean legs across the two executions. Both receipts are linked; synthesis rc 0 is separate. The original issue comment is explicitly corrected rather than silently reinterpreted. Round 3 is independently supported by one successful full campaign, rc 0, 68/68. |

Artifact-specific lens results

[R670] PASS Conformance - D3 section 3 rule 7, sections 8.3/8.7/18.4; FASTCONNECT 6.1; processor `docs/architecture/07_memory_maps.md` section 5.1; `sim_nxn.cpp:5496`; REGISTER_MAP PP_STAT - invalid framing retains defaults and permits blank only when nothing validated and no restore failed. The new tests isolate that contract without modifying it. Parent ownership, accepted one-pass transaction and the earlier empty/non-default persistence coverage carry forward. The physical cold cycle is excluded from this PASS.

[R670] PASS RTL - `git diff 8000520c..1e914414 -- hdl syn constraints` is empty; `milan_datapath.sv:5347`, `:5487`, `:5769`; CSR cause wiring - the three-stage restore, rollback, status composition, deadlines, same-clock ownership and device arbitration are unchanged. The validated predicate requires magic/length, layout/id and CRC. The cause-field correction describes existing wiring. Prior R670-2 RTL coverage carries forward; no new synthesis or timing result is inferred from test changes.

[R670] PASS Robustness - `sim_nxn.cpp:5503`, `:5523`, `maprec_grade_both` at `:4932`, `maprec_grade_stat` at `:4880`; `lone-record-receipt-excerpt.txt` - each newly corrupted window leaves both ports and RAMs at reset, reaches a terminal, and reports done/not busy/not failed/blank. CRC corruption changes a payload byte under its old CRC; header corruption is resealed, preserving CRC validity. Prior error, deadline, rollback, ordering, legal-maximum and multi-port coverage carries forward; its tests and RTL were not weakened.

[R670] PASS Tests - `dynmap_mutants.py:414`, `:457`, `:496`; `sim_nxn.cpp:5496-5557`; verified campaign receipts - each new mutation has a unique source anchor and a named blank assertion. The driver requires a harness failure and every named failing check; build errors or crashes are not catches. Row 62 requires both layout and id checks. The clean dynmap leg grows from 589 to 649 checks; the eight new GET pages explain 51 to 59. All 63 README failure tallies match the full campaign receipt. The magic/length conjunction is exercised through magic; separate length-only mutation coverage is not claimed or required by this assignment.

[R670] PASS Docs - REGISTER_MAP paragraph/row, D3 8.7, TESTING.md:277, milan_dp README campaign table, Makefile:569, PR/issue/HANDOFF accounts - the corrected causes match the implementation, campaign counts match the executable list and receipts, and failed/retried/aggregate executions are distinguished. Added source comments in this delta contain no new reviewer identity, review-round label or issue-comment ID. Existing assigned residue is retained below.

Earlier findings and suggestions explicitly reconciled

The [R670-2 findings](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295076402) and [R669-2 findings](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6295588258) provide the prior dispositions. Their unchanged implementation coverage is carried forward under the round-3 scope rule; changed tests/docs were re-examined above.

| Prior items | Disposition at this head; artifact evidence |
|---|---|
| R670-F1; R669-F1/S2 | RESOLVED, carried forward. `pp_stat_*_w` at `milan_datapath.sv:5769-5773`; public status assertions; controls 38-44/56 remain caught. The distinct term-coverage gap R669-2-F1 is resolved above. |
| R670-F2; R669-F5 | RESOLVED, carried forward. Three-stage `amr_fsm`; maprec8 transfers in both port orders and cyclic swap; old-order control 54 remains caught, 12/219. No limitation-only waiver. |
| R670-F3; R669-F2 | RESOLVED, carried forward. Real restore-path put-back, holes, layout/id, ranges, conflicting keys and pass-0 abort checks; controls 45-53/55/57/60 remain caught. |
| R670-F4; R669-F3/F4 | RESOLVED. Prior literal-port, C++ structure and test-evidence defects remain fixed. Round-3 docs receipts give 95 zero exits without a ratchet change. The narrowed execution-account defect R670-2-F1 is resolved above. |
| R670-F5; R669-F6 | RESOLVED, carried forward. REGISTER_MAP PP_STAT[4] names the parent map writer, three attempts 500 ms apart and reset-sticky alarm. |
| R670-F6 | RESOLVED, carried forward. Public ruling and D3 3/18.4 explicitly accept the map-only one-pass transaction and its validation obligations. |
| R670-R1/R2/R3; R669-R1/R2/R3 | RESOLVED, carried forward. Layout comment says check 15 at `milan_datapath.sv:4938`; assigned lane labels are removed from `KL_pp_shadow.sv:966` and the shared-face test. |
| R669-S1 | ADDRESSED. D3 18.4 documents counting an ungranted request wait as an attempt and the capture-hold rationale. |
| R669-S3 | RETAINED SUGGESTION, Tests. `scripts/check_nvm_record_space.py` check 15 guards the layout literal, not all parent payload-length formulas. Optional outcome: guard formula/census agreement across shapes; verify with a formula mutation. No mandatory correction assigned. |
| R669-2-S1 | RETAINED SUGGESTION, Tests. `milan_datapath.sv:5380` sweep wait. Optional outcome: hold the sweep across terminal and grade RAMs, or prove redundancy with the server wait; verify a removed-wait control. |
| R669-2-S2 | RETAINED SUGGESTION, Tests and Docs. `milan_datapath.sv:5602` refused stage-0 take-down. Optional outcome: perturb the store to exercise rollback or document defensive reachability; verify the public fail/default result under that perturbation. |
| R669-2-S3 | RETAINED SUGGESTION, Tests and Docs. `tb/verilator/milan_dp/Makefile:575` does not prepare the listener build. Optional outcome: make the campaign target prepare it; verify a fresh-clone campaign. This round explicitly performs the prerequisite build and has a successful complete receipt. |

Wording residue, all Docs-only

These retain their original IDs where already filed. The assignment explicitly leaves them for the merge checklist. No item below changes a measured result, test oracle, conformance claim or review verdict. Source-comment changes must preserve executable tokens and stable test identifiers.

| ID / severity | Artifact | Authority/evidence and impact | Exact required outcome | Verification |
|---|---|---|---|---|
| R670-2-R1 / R669-2-RES-1/RES-2, RESIDUE | `milan_datapath.sv:4921-4926`; `sim_nxn.cpp:5564-5565` | Owner comment rule; issue-comment ID remains in source prose. Administrative provenance residue. | Replace the RTL ruling/comment citation with `#637; D3 18.4`; C++ banner with `D3 18.4; Milan v1.2 5.3.10.1; #637`. | Comment-only diff; behavior and reason retained. |
| R670-2-R2 / R669-2-RES-3, RESIDUE | `dynmap_mutants.py:29`, `:35`, `:154`, `:168`, `:316`, `:345`, `:386` | Owner comment rule; reviewer identities and round names remain. | Use `Additional #637 controls follow`; `per-port ordering`; remove `round 2` from section comments; use `per-port order` at line 168. Keep runtime identifiers/anchors stable; the prior observation also names the descriptive row-54 string at line 387. | Comment/docstring inspection with no oracle or generated-result change. |
| R669-2-RES-4, RESIDUE | `dynmap_mutants.py:29-40` | Prior prose census omits some of the already enumerated controls. Executable inventory and current measured table are correct. | Describe eight composition rows, fourteen value/recovery rows and one ordering row, or list all 23. | Count rows 38-60; no mutation change. |
| R669-2-RES-5, RESIDUE | `milan_datapath.sv:5491` | Stage 0 already emptied the port; comment says refused before port touched. | Replace with `refused before its saved set touches the port`. | Comment-only edit against the existing stage sequence. |
| R670-2-R3 | PR roles at `public-pr-body.md:25-26` | RESOLVED: round-2 assignments and negative verdicts are now recorded. New stale round-3 wording is separately listed below. | None for the old item. | Compared with both round-2 notices. |
| R670-3-R1, RESIDUE | PR roles, `public-pr-body.md:25-26` | Both roles say round 3 is to be assigned, while public start notices 6298509526/6298519097 exist. Administrative wording only. | Say `round 3 assigned` and link the respective start notice; publication may then link each actual verdict. | Compare with public notices; do not invent the other review's verdict. |
| R670-3-R2, RESIDUE | Public `author-r3/HANDOFF.md:80`, Head cell | `tb, hdl equal to the head` is loose shorthand. Lines 8-9 and 69 already precisely disclose the README and Makefile-comment differences. Tested inputs are equivalent; no measurement is disputed. | Replace the parenthesis with `executable inputs equal to the head; README and Makefile comment differ`. | Compare `600565b4..1e914414`, which changes only those two documentation locations. |

Execution evidence and limits

The pinned public evidence is [4d31fa3d.../review-evidence/637-r1](https://github.com/kebag-logic/milan-fpga/tree/4d31fa3d8b9bd09b15b2f4b78ed7b8f2c2d04a47/review-evidence/637-r1). Thirty selected artifacts were fetched with Git-blob verification, including the manifest; the other 29 also match its `published_sha256` entries. No claim is made to have downloaded or verified every file in the entire evidence tree. Source and evidence commits are reported unsigned; no detached signature was supplied. This verifies published-byte integrity, not signer authentication.

| Evidence | Result and practical limit |
|---|---|
| Exact-head author legs | dynmap 649/0, maprec8 219/0, maprec4 137/0; all rc 0. Four new cases explicitly report PP_STAT `5b000484`. |
| Full round-3 author campaign | At `600565b434f09ee581508d5a5f3a02a3594afd55`, after the render prerequisite: 63 controls caught, five clean legs, 68/68, rc 0. Only README and a Makefile comment differ from the reviewed head. |
| Round-3 author docs/builder | 95 docs commands rc 0; both builder legs rc 0 at exact head. Builder calibration gate 11 remains NOT RUN. Initial origin-mismatch builder refusals are disclosed and superseded by complete reruns, not counted as successes. |
| Round-2 author campaign | Full rc 2, 63/65; listener rerun rc 0, 2/2. Aggregate case coverage is 60/60 plus five clean legs across executions. Synthesis is separate. |
| Reviewer probe | `check_record_terms.py`: four actual codec windows, independent CRC calculation, exactly CRC/layout/id/magic respectively fails. Initial probe incorrectly assumed eight output slots; codec refused it. Corrected to this shape's seventeen output clusters, then all four passed. Both raw receipts are retained. This is a record-generation probe, not new RTL simulation. |
| Reviewer receipt checks | `verify_evidence.py`: manifest, 63 row identities/named checks, all README failure tallies, five clean legs, leg counts and exit tables agree. No full campaign was rerun. |
| Checkout integrity | `audit_tree.py`: 1,422 parent blobs and every tracked blob in all five required populated submodules match exact bytes, modes and index; no hidden index flags. HEAD/index tree matches the assigned tree. Optional `external` stays uninitialized at its recorded gitlink. No source restoration was needed. |
| Hosted exact-head evidence | API snapshot: zero check runs; combined status pending. No executed or skipped successful hosted context is claimed. Manager owns hosted/act acceptance. |

No manager source bank ran at this head and none is inferred. Source evidence above is the author's published evidence. Prior route/ooc, synthesis, frontend and full-sweep evidence carries only within its previously reviewed unchanged scope; no new full run is claimed here. No simulator build was executed by this reviewer, so no local compiler identity is offered as execution evidence.

Physical calibration and the board cold cycle are NOT RUN. Field skips, retained-window resets and simulations are not hardware proof. The 1x1 hold remains 598-672 clocks on a zero-latency window model; board DDR latency is unmeasured. The documented non-shipping 8x8 hold is about 13,700 clocks against a 4,096-clock gather watchdog, with placement/timeout obligations still open.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | D3 3/8.3/8.7/18.4, FASTCONNECT 6.1, processor 07 section 5.1; lone-record cases; unchanged status and restore logic | R670-3 delta, carrying R670-2 unchanged scope | 1e914414557874648ac5041aff88b96908e0e053 |
| RTL | CLEAN | Empty hdl/syn/constraints delta; AS_BOOT/AS_RJDG and pp_stat composition; CSR cause wiring; exact gitlinks | R670-3 dependency check, carrying R670-2 RTL | 1e914414557874648ac5041aff88b96908e0e053 |
| Robustness | CLEAN | sim_nxn.cpp:5496-5557; reset-list/RAM/status receipts; independent four-window probe; unchanged multi-port/error/deadline tests | R670-3 delta, carrying R670-2 unchanged scope | 1e914414557874648ac5041aff88b96908e0e053 |
| Tests | CLEAN | dynmap_mutants rows 61-63 and verdict parser; page guard; 63-row receipt/table audit; corrected execution account | R670-3 | 1e914414557874648ac5041aff88b96908e0e053 |
| Docs | CLEAN | REGISTER_MAP:2378/2403; D3:1499; TESTING:277; README/Makefile counts; public PR/HANDOFF/issue corrections | R670-3 | 1e914414557874648ac5041aff88b96908e0e053 |

The carried round is R670-2 at `8000520cc12ec5d107a2a67f8ba3d6134b87d2b5`; its clean Conformance/RTL/Robustness scope is unchanged except for the test/doc additions applied here. Tests and Docs are cleared by this round, not by the earlier negative verdict.

Pending manager duties

- Obtain the other independent verdict and confirm no review is in flight. Carry the residue and optional suggestions above without treating them as blocking defects.
- Complete hosted/act acceptance on the final source head. This review supplies no successful required hosted context.
- Construct and validate the current-dev merge candidate with the required builder/native banks and publish receipts. The supplied live dev is `78ca9bdf104819265588726bce4322696c38b8c2`; use its current successor if it advances. This source review proves no such candidate execution.
- Retain board cold-cycle, physical calibration, measured DDR hold and outstanding 8x8 obligations. Keep issue #637 open for unfinished physical acceptance; the PR correctly uses “Relates to”.
- Obtain explicit maintainer merge authorization, then perform required containment and final issue/project accounting. This report is not merge authorization.

Reproduction: run `python3 check_record_terms.py <exact-head-clone>`, `python3 verify_evidence.py <exact-head-clone>` and `python3 audit_tree.py <exact-head-clone>` from this packet. The first places disposable generation output under `scratch/`; that directory is excluded from publication. `fetch_evidence.py` retrieves only the selected pinned public evidence. `MANIFEST.sha256` enumerates publishable receipts and scripts, with paths relative to the packet.

R670-3 FINISHED
