[R666] NEGATIVE - exact head 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e

Issue #188 + #189 / PR #195, round R666-2. Assigned tree: `34af6de87215cc90a774757debc8af90073aaa87`.

The assigned functional repairs pass this delta review. Both coalesced registration directions follow the final registered type, and all five requested owed-Leave settle cases have effective regressions and killed controls. No production-code defect was found. One MINOR remains in the PR's published mutation accounting; it makes this verdict NEGATIVE under the supplied rule. One new comment RESIDUE and the previously unassigned SUGGESTION are also recorded so they can be handled together.

Reconstruction and scope

Read the supplied instruction file and checked the repository/ancestor instruction locations: no repository AGENTS.md or CONTRIBUTING.md was present. Read `docs/README.md`, the frozen issue bodies and original assignment, then the [round-2 assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6264243047) in full. Authorities examined were REQ-ACMP-011/016/018/022, REQ-NET-003, REQ-SRP-005, F05.3/F05.14, the 02 event/status contract and 10 §6.4/§6.5. These trace to Milan v1.2 Tables 5.30/5.39, §5.5.3.5.44, §4.2.7.2.2, and IEEE 802.1Q-2018 §10.7.7/Table 10-3 and §35.2.6. No new interpretation of a standard is asserted; the frozen public requirements and repository's cited tables are the normative reconstruction used here. Original standards PDFs were not supplied or independently inspected.

Reviewed `b48312e1..7f56fc4d` and its history, concentrating on the six author commits from `cb8bab04` to `cca12e3c` and the merge of `24c7f853`. Untouched baseline code retains its earlier lens assessment except where this delta changes a dependency. The imported #185/#186 implementation was checked for composition, not re-qualified as a new issue. Its engine/notification files and campaign driver remain byte-identical to the main parent; the listener files and ACMP/SRP drivers remain byte-identical to the author parent.

The independent verdict and five-lens ledger were written to `receipts/independent-verdict.md` before opening either prior findings report. That initial verdict was positive with a comment residue; the final accounting audit below found the MINOR and changes the final verdict. No current-round reviewer report, private author material or management source bank was used. The public [review start](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6284945125) and immutable [evidence publication](https://github.com/kebag-logic/milan-fpga/tree/61e4bb57da96c2c2e4d60987f390a435384ffe9f/review-evidence/pp188-r1) anchor this review.

Findings

**R666-2-001 — MINOR — Docs, Tests (published evidence accounting). The PR overstates the number of killed mutation entries.**

Artifact: current [PR #195 body](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195), Records bullet beginning “`tb/srp_top` mutants: 168 -> 179 arms, all KILLED”. Snapshot: `pr195.json`. Driver: `tb/srp_top/mutants.py:250`, `:299`; accounting receipt: `receipts/campaign-accounting.json`.

Authority/evidence: the assignment requires accurate campaign tallies. The verified public `author-r2/receipts/round2/campaigns/{base,head}/srp_top.log` records distinguish passing positive controls, killed mutation entries, and the assertion-coverage check. Counting the actual outcomes gives:

| Revision | KILLED mutation entries | PASS golden runs | PASS coverage check | Total campaign checks |
|---|---:|---:|---:|---:|
| cb8bab04 | 150 | 17 | 1 (94/94) | 168 |
| cca12e3c | 161 | 17 | 1 (101/101) | 179 |

The exact reviewed head's driver has 161 mutation entries and is byte-identical to `cca12e3c`'s driver. Thus 179 is the correct total check count, but not the killed-arm count. Seventeen successful goldens and one successful coverage check have been described as killed mutation arms.

Impact: the public acceptance summary overstates mutation evidence by 18 entries at each revision. The executable results themselves are sound. This affects a measurement and outcome claim, so it does not meet the supplied purely-wording RESIDUE exception.

Required outcome: replace that bullet with: “`tb/srp_top`: 150 -> 161 mutation entries, all KILLED; 17 golden runs PASS at each revision, plus one passing assertion-coverage check (94/94 -> 101/101), giving 168 -> 179 total campaign checks.” Preserve the immutable raw receipts.

Verification: run `python3 scripts/audit_accounting.py` from this packet and compare the corrected PR body to `receipts/campaign-accounting.json`. No RTL or test-behaviour change is needed.

**R666-2-002 — RESIDUE — Docs, Tests. One new explanatory comment contains a bench label.**

Location: `tb/srp_top/mutants.py:184`: `# WK12's own counts and its precondition, at every shape`.

Authority/evidence: the supplied owner rule of 2026-10-15 forbids bench labels in new source comments. The line is added by the round-2 delta. Impact is comment wording only; it changes no measurement, assertion, generated artifact or clause claim.

Exact fix: `# Grade the repeated-settle walk counts and precondition at every shape.` Keep executable selectors, expected failure strings and receipts unchanged. Verification: inspect the added comment lines; this fix must produce no executable diff. This residue does not make a lens unclean. Existing unrelated labels remain under #746.

**R666-2-S1 — SUGGESTION — Docs. Retain the unassigned R665-1-S1 measurement-date clarification.**

Location: `tb/pp_top/README.md:2120` lead-in and `:2130` (`st_ls_teardown_as_declare`). The table still dates its records to the earlier #639 run while this row now reports the later, correct “1 of 58”. Authority/evidence: [R665-1-S1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/195#issuecomment-6264221765), the explicit round-2 decision not to assign it, and the published campaign record. Impact: readers must infer the row's measurement date. Suggested outcome: date this updated cell or say the issue-specific annotations override the table's historical date. Verification: the date should identify the existing receipt without changing its measured count. Retained as a non-blocking suggestion, not expanded into required work.

Prior findings resolved at this head

| Prior finding | Disposition and cause-level evidence |
|---|---|
| R666-001 and R665-1-F2 | RESOLVED. `hdl/top/protocol_processor_top.sv:3306` selects the live SRP registered type by the presented registration source. `KL_pp_acmp_listener.sv:1030` captures it when accepted; `:1162` performs bookkeeping without a new Table 5.30 arc. The router's first-payload retention is unchanged. AS5d/AS5e in `tb/pp_top/sim_main.cpp:10090` hold TX, fill the ordinary slots, register both types, require exactly one coalesced event, drain exactly six answers, then compare fresh GET_RX_STATE replies and unchanged refreshes byte-for-byte. Exact-head golden passes; restoring first-payload wiring is KILLED in both directions. 05 §6.3 and the PR now describe reconciliation; the residual-exception sentence is absent. |
| R665-1-F1 | RESOLVED. `tb/srp_stream_fsms/sim_main.cpp:1157` covers third-stream settle, return to the parked stream, and LO settled elsewhere; `:1231` covers txLA! and received Listener Mt while parked. RB4–RB8 each have a named killed control. RB9 at `:1282` grades the new record-valid guard. `walk_main.cpp:542` covers repeated settles at all four shapes. The coverage set at `tb/srp_top/mutants.py:303` requires RB1–RB9 and WK1–WK12. Both READMEs record the behaviour, controls and counts. U6/U7 remain explicitly documented as likely equivalent, as assigned. |
| R665-1-F3 | RESOLVED. The same-stream row in 10 §6.4, the listener banner, and the PR table now distinguish LA's Leave from LO's Empty and say New! takes either to VN. |
| R666-002 (round-1 RESIDUE table) | RESOLVED for every listed location. The B4/AS5b/AS5c/AS7, section M/RB1–RB3 and WK11 explanatory prefixes/references were removed; the requested “Every sink but k…” sentence is present. Executable labels remain intact. R666-2-002 above is a separate newly introduced comment. |
| R665-1-S1 | RETAINED as R666-2-S1; expressly unassigned in round 2. |

Execution and evidence

The exact-head focused runs were started together under one foreground supervisor, using isolated temporary trees under this packet's `scratch/`, explicit campaign job limits, and bounded compilation concurrency below 16 jobs. The pinned simulator identifies as revision 5.050. No full bank, hardware run or source fix was performed.

| Exact-head check | Result | Receipt |
|---|---|---|
| Integrated ACMP golden | 58 checks, 0 failures | `receipts/acmp-focused/golden-pp_top--acmp-only.log` |
| Old first-payload wiring control | KILLED; both post-drain checks and both refresh checks fail with the wrong flags | `receipts/acmp-focused/results.json` and mutant log |
| Stream-FSM golden | 1361/1361 PASS | `receipts/srp-focused/control-srp_stream_fsms-suite.log` |
| Walk goldens, source/sink shapes 1/1, 2/2, 3/5, 9/9 | 43/43, 57/57, 87/87, 155/155 PASS | `receipts/srp-focused/control-srp_stream_fsms-walk.log` |
| Parked third-stream identity control | KILLED in suite (RB4/RB5) and walk (WK12) | `receipts/srp-focused.log` |
| Return-to-park, LO-owed, txLA-retire, parked received-value, no-record controls | All KILLED by RB5, RB6, RB7, RB8 and RB9 respectively | `receipts/srp-focused.log` and per-control logs |

Both focused drivers return 0. The SRP driver overwrites the shared-name per-control log when an edit runs in both suite and walk; its outer receipt records both results. The public separate `round2/extra/csid-ram-suite.log` supplies the preserved suite failure detail. No missing suite log is represented as independently preserved here.

The fixed publication's SHA-256 manifest verifies all 491 selected public round-2 receipts (`receipts/public-verification.json`). This checks published bytes, including declared path redactions. It is not signature verification: the publication commit's API verification record says `unsigned`, and no detached signature was supplied. Cryptographic signer authenticity remains NOT VERIFIED; no signed-packet claim is made.

Published author full-gate evidence names `cca12e3c`, before the manager merge. It records seven processor gates returning 0, 1,030,070 suite checks with no failing suite, and fourteen campaign drivers returning 0. ACMP records 65/65 killed entries; SRP records 161 killed entries plus the 18 other passing checks described above. These are author source receipts, not manager execution at `7f56fc4d`.

The author's consumer receipts name parent `e9cbb676`, the `cca12e3c` processor override, and two declared parent patches. All six gitlinks match that public parent with the assigned processor substitution (`receipts/parent-composition.json`). The consumer comparison retains two baseline failures, `lint_rtl` and `submodule_docs`; it is not an all-green consumer bank. Large external consumer logs are represented by the public checksum inventory and comparison summaries, not independently fetched raw execution. Those limitations remain visible in the evidence.

Merge composition and interface

Replaying the merge of `cca12e3c` and `24c7f853` yields exactly tree `34af6de87215cc90a774757debc8af90073aaa87` (`receipts/merge-replay.txt`). The auto-merged top retains both the live-type selection and the imported internal lock-flags wiring. The combined bench retains the coalescing/Leave sections and the imported CONTROL/lock sections. Campaign inventories match their respective parents: ACMP 65, notification 135, dispatch 69; the notification README's 125 + 10 = 135 is consistent. `rd-tail-uncut` remains 17 and `occupancy_reset_set` 32 with their source explanations. SRP suite/walk tallies match the exact-head run. The PR's distinct 179-killed-arms claim is the accounting defect above.

The top's complete module declaration, including parameters and ports, is byte-identical at base, both parents and this head. Register-map owners are unchanged. All 680 tracked blobs and modes match the assigned commit, the index tree matches the assigned tree, and the worktree is clean (`receipts/final-integrity.json`). This standalone processor tree has no submodule gitlinks; the required public consumer gitlinks were checked separately. Disposable builds and mutation copies stayed under `scratch/`; that directory is excluded from publication.

Reviewer-owned final ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | frozen acceptance and assignment; F05.3/F05.14; 02 event/status contract; 10 §6.4/§6.5; live-type selection and LA/LO semantics | R666-2 delta and prior-finding closure; unaffected R666-1 coverage retained | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| RTL | CLEAN | listener event capture/bookkeeping; top source-index mux; record-valid settle guard; parked identity/retirement; exact merge replay and interface comparison | R666-2 delta and dependency checks; unaffected R666-1 coverage retained | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Robustness | CLEAN | blocked-TX coalescing both directions; unchanged refreshes; RB4–RB9; WK12 at both storage implementations; exact-head planted faults | R666-2 delta and prior-finding closure; unaffected R666-1 coverage retained | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Tests | UNCLEAN — R666-2-001, evidence accounting only | new suite assertions, mutation selectors and coverage set; verified public outcomes; focused exact-head executions; PR outcome tally | R666-2; executable checks pass, published accounting remains open | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |
| Docs | UNCLEAN — R666-2-001 | architecture 05/10, listener banner, suite READMEs, merged pp_top campaign sections, PR body and prior residue locations | R666-2; new RESIDUE and retained SUGGESTION do not independently unclean this lens | 7f56fc4d7f5102cac6dacb9c00f372d20d3b379e |

Limits and pending manager duties

Correct R666-2-001 and obtain the required renewed independent acceptance. Carry R666-2-002 to the residue checklist; R666-2-S1 remains optional. At the final hosted snapshot, both docs-gates and both portability jobs had completed successfully; both suite jobs were still running. None of those observed jobs was skipped. Pending work is not a pass, and no hosted/act acceptance is inferred; that acceptance belongs to the manager.

There is no manager source-bank claim at this exact head. The manager still owns the final current-dev merge candidate build, builder/native banks, consumer acceptance and linked receipts at merge turn (source base `b48312e1`; supplied live dev `e26f1816e456dc8027924bc2e5d327a8aa6e46db`). Author source validation, this focused source review and final candidate validation are separate. Physical calibration NOT RUN and field skips are not hardware proof. This review makes no timing-closure, physical or field-validation claim and is not merge authorization.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. The manifest uses paths relative to this packet; `scratch/` is never published.

R666-2 FINISHED
