[R844] POSITIVE - exact head 98c0b62be911f5cff7a03ebfee7f837c23847d14

External independent delta review R844-2, issue #894 / PR #914. All five lenses are CLEAN. R844-1-F1 is resolved at its cause. No BLOCKER, MAJOR or MINOR remains in this delta; two wording residues are listed below.

Head tree: `42431e547e28fcdaa50feec57700fef4887d92e0`. Review scope: the four commits `716a8ae7979a31315a6e085959dc4dcc8b7ee022..98c0b62be911f5cff7a03ebfee7f837c23847d14`, within the PR's source-base range `7398ec0aeea468d92ff642a03a06e291a0cd58d1..98c0b62be911f5cff7a03ebfee7f837c23847d14`. Unchanged implementation keeps its preceding review coverage unless this delta changes its dependencies. This does not review #902's later work.

I reconstructed the workflow, documentation map, issue body and public scope decisions, requirements and relevant interfaces, then examined the delta and public executable evidence. An independent verdict and five-lens ledger were written before reading the prior review comments. Only then were [R844-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885381555) and [R843-1](https://github.com/kebag-logic/milan-fpga/pull/914#issuecomment-6885564795) reconciled. No other current-round report, private author material or management checkout was read.

The binding authorities are [the shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), [held-egress ruling (a)](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), [egress bounds](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126), [retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227), REQUIREMENTS.md, FR_NFR.md 3.4.1 and SPLIT_CONTROL_MEMORY.md section 13. No bound or ceiling is relaxed: AECP 20 ms, ACMP/ADP/MAAP 30, SRP 90, first/last queued notice 20/130, txL 49, paced R4L 238, commit-side joins 181–239, 8x8/1if load 0.75 and slice cap 1,600 us. The seven held-egress rows remain recorded misses, not passing service-budget rows.

**Prior findings, resolved or retained**

| Prior ID | Original severity and lenses | Disposition at this head |
|---|---|---|
| R844-1-F1 | MAJOR; Conformance, Robustness, Tests | RESOLVED. `egress_ledger.py:140` checks every measured ledger instance numerically, without a name-only waiver. `author-r4/scripts/gate_r4.py:180` delegates to it. Every row one cycle over and every large overrun fails by name; original fault fixtures now fail; six archived legs regrade successfully. |
| R844-1-R1 | RESIDUE; Docs | RESOLVED. Original comment audit emits zero lines. Changed comments retain behavior, issue IDs and ruling subjects. |
| R843-1-R1 | RESIDUE; Docs, RTL, Tests | RESOLVED. Broader scan of added non-Markdown lines is also empty, including check descriptions. Token/AST comparison confirms the intended wording scope. |
| R843-1-S1 | SUGGESTION; RTL, Robustness | ADDRESSED within the stated guard limit. Explicit charging units get the named missing-table diagnostic; two-interface core arms get their own mailbox contract and the interface assertion. An undeclared future charging unit still gets an ordinary undeclared-name error; that disclosed limit is retained, not claimed solved. |

R844-1's unmeasured-input note was not a separate finding. Its original fixture now fails explicitly too. No earlier blocking finding is deferred to another issue.

**Conformance and robustness evidence**

`tb/verilator/ctrl_service_budget/egress_ledger.py:43,55,76,89,140` implements the seven unchanged section-13 figures, integer comparison at 10 ns resolution, rejection of never released/answered and unmeasured instances, missing ledger rows and other budget misses. A matching name in another group does not qualify. Its self-test also binds the names and figures to section 13.

Independent runs in this review:

- `egress_ledger.py --selftest`: 30 controls in process and as separate processes, eight mutants caught, zero failures (`receipts/ledger-selftest.log`).
- Published `gate_controls.py` against the exact-head grader: 20 controls pass. All 14 per-row one-cycle/large-increase plants fail by name; unchanged ledger and published measurement controls pass (`receipts/gate-controls.log`).
- The original R844-1 fixture contents, with only invocation and expected status adapted: control exits 0; 100.0 ms `backlog.owed.if0` and `required.cpu.row` unmeasured each exit 1 with the expected name (`receipts/prior-probes.log`).
- Both the tracked grader and packet acceptance gate regrade the six archived logs successfully (`receipts/regrade.log`, `receipts/gate-regrade.log`).

The log-based regrade is valid evidence for this correction. `run.py:515` turns every unmeasured probe into a refusal and every missed or never-completed probe into a miss; `run.py:776` prints every miss, and its summary counts them. The six published logs contain exactly one summary and successful END each: 22/24/24/25/16/1 groups, 112 total, zero refusals, seven BUDGET lines matching seven summary misses, and no STATED lines. All seven misses occur in C-A0.

The grader adds 0.0005 ms to each figure printed to 1 us. Thus the recorded upper bounds are:

| Row | Conservative upper bound, ms | Ledger, ms |
|---|---:|---:|
| backlog.owed.if0 | 63.0835 | 63.24 |
| backlog.owed_behind0.if0 | 63.3055 | 63.47 |
| backlog.owed_behind1.if0 | 63.5265 | 63.69 |
| backlog.owed_behind2.if0 | 63.7475 | 63.91 |
| backlog.owed_behind3.if0 | 63.9695 | 64.20 |
| backlog-owed.service.acmp.last.if0 | 62.0255 | 62.18 |
| backlog-owed.service.aecp.last.if0 | 61.6805 | 61.83 |

The least remaining margin is 0.1495 ms. Reading these logs does not recover the deleted per-group grades or remeasure CPU rows, queued notices, rounds or joins. Those results carry through the identity evidence and unchanged grading logic. The prior measurement receipt still reports the CPU rows within their stated bounds, 2,455,411 retry rounds within statement, joins 186.687–190.705 ms and last queued notice 26.195 ms. The 8x8/1if every-source model rows remain reported debt under #872, not substituted for measured acceptance.

**RTL, architecture and test evidence**

The delta contains no HDL or submodule-pin change. The product code change is the include order and guarded compile diagnostic at `sw/firmware/ctrl/aecp/aecp.c:3` and `aecp.h:67`; it introduces no runtime call. Five independent compile probes confirm correct-order and noncharging inclusion compile, both declared missing/late-table cases fail in THE SHAPES' words, and undeclared charging has the documented ordinary diagnostic (`receipts/guard-probe.log`).

`aecp_arms.py:116` generates the two-interface core contract through `srp_arms.prepared`; `test_aecp.cpp:42` asserts `MBX_N_IF == AECP_TEST_INTERFACES`. Mailbox arms retain their generated contracts. The debug arm uses a separate test source configuring one interface and is not falsely described as a two-interface core check. The public `item3-guard-and-assert-checks.txt` records both new build mutants rejected, the planted wrong-contract arm rejected by the assertion, 83/83 core tests at each interface count, 4/4 selected 8x8/1if tests, and the debug check passing. These host suites and the expanded campaign were rerun by the author; this reviewer independently probed the compile guard, not the entire host campaign.

I reran the published token/AST comparison for the wording commit. C/H/C++ tokens are unchanged; Python syntax trees are unchanged after stripping docstrings except five printed check descriptions, whose differences were inspected (`receipts/identity.log`). Later functional edits were reviewed separately. `rows_grade.py` changes only its shape-keying docstring.

The public image receipts contain identical ELF and loadable-byte hash pairs for all eight fixture/platform images at the old-head rebuild, after wording changes, after guard changes and at the final head. These pairs also match round 3's receipt (`receipts/evidence-audit.log`). The 8x8/1if platform remains 56.0 RAMB36. This is verification of published image receipts, not a claim that this reviewer rebuilt the images.

Sweep carry is supported by unchanged HDL and dependencies, the token-identical loop header, the `mbx/Makefile:67` firmware list, and `milan_dp/Makefile:704` suite cases. The separately affected twin and counter paths have fresh author receipts. The new ledger reads output; it does not alter the measured image or earlier harness grading. The earlier sweep and measurement therefore carry for this bounded delta.

**Public evidence and documentation**

Evidence source: [archive 843c40b1](https://github.com/kebag-logic/milan-fpga/tree/843c40b1e9249d89862a9174da7e2b4c32c300d1/review-evidence/894b-r1), principally author-r4, with author-r3 comparison receipts. All 94 extracted author files match the manifest's published SHA-256 values. All 45 round-four index entries match either the original digest or an explicitly declared path redaction. The pinned archive commit has no embedded signature header; this establishes Git-object/digest integrity, not a verified cryptographic signer.

The exact-head author receipts, rather than any manager source bank, supply the broad execution evidence:

- Workflow-step inventory: 139 local executions at rc 0, 226 NOT RUN entries with reasons, no unexpected result. These are locally executed workflow steps, not hosted jobs or hosted status conclusions.
- The first LiteX aggregate timed out in `test_soc_timing_cuts` at 900 seconds, rc 92/UNKNOWN. Its published rerun shows all eight simulations passing, zero timeouts; the earlier timeout is not counted as a pass.
- Firmware campaigns: 716/277/345 caught, zero escaped; both new compile-refusal rows are named. Boundary, wire and counter receipts are present.
- Lane gates: 59 entries, 55 rc 0; exactly four expected rc 1 results: `rows_tiers --terms`, default `flip --check`, `flip --point 1x1/1if --design as-built`, and `flip --point 8x8/2if`.
- The sweep and CPU measurement are explicitly carried, not rerun this round. `docs_inventory --check` is explicitly NOT RUN because it is absent from this source head; it must run after synchronization brings it from dev. Physical calibration and field skips provide no hardware proof.

Section 13 preserves every ledger value while expanding the two service-row names and relabelling the ledger column accurately. FR_NFR and the harness README describe the executable rule and conservative log precision. The AECP README states the conditional guard's actual reach. Public REVIEW READY, the PR finding table, scope decisions and receipts are sufficient for this delta's reconstruction.

**Open wording residues**

R844-2-R1 — RESIDUE — Docs, RTL — `sw/firmware/ctrl/aecp/aecp.h:63`, and PR #914's “The guard” paragraph.

Authority/evidence: the new comment says every unit includes `aecp.h` before the table, although `aecp.c:7` deliberately includes the table first. Impact: a contradictory introductory sentence only; the guard, neighboring explanation, tests and runtime behavior are correct. Exact required fix: replace “Every unit includes this header before the table, and most charge nothing” with “Most units include this header before the table and charge nothing”; make the corresponding PR sentence agree. Verification: inspect the wording-only diff and retain the same guard and image results. No measurement, bound, verdict, generated artifact, normative claim or privacy rule changes.

R844-2-R2 — RESIDUE — Docs — `author-r4/receipts/source/carry-by-identity.txt:36`.

Authority/evidence: the narrative names `counters-f5-3bb204c8.txt`, while the published final-head receipt and INDEX name `receipts/firmware/counters-f5-98c0b62b.txt`. Impact: a stale receipt filename; the final-head counter evidence exists and was examined. Exact required fix: update that filename/reference to the published final-head receipt. Verification: the link/name resolves to the already published receipt; no result or execution claim needs changing.

Neither residue leaves a lens unclean. No additional suggestion is open.

**Reviewer-owned completion ledger**

Paths below are repository-relative unless labelled author-r4 or receipts. Every row covers the delta and the named prior findings at the exact head; unaffected earlier coverage carries as described above.

| Lens | CLEAN/UNCLEAN | Examined artifacts and result | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #894 held-egress ruling (a); docs/reference/FR_NFR.md:393; docs/design/SPLIT_CONTROL_MEMORY.md:2526; tb/verilator/ctrl_service_budget/egress_ledger.py:140; receipts/regrade.log; numerical acceptance restored | R844-2 | 98c0b62be911f5cff7a03ebfee7f837c23847d14 |
| RTL | CLEAN | sw/firmware/ctrl/aecp/aecp.c:3; aecp.h:67; sw/firmware/ctrl/test/aecp_arms.py:116; test_aecp.cpp:42; image hash receipts; unchanged HDL/gitlinks; guard and interface contracts checked | R844-2 | 98c0b62be911f5cff7a03ebfee7f837c23847d14 |
| Robustness | CLEAN | egress_ledger.py:76,89,140; receipts/ledger-selftest.log, gate-controls.log, prior-probes.log, guard-probe.log; boundary, absent, never-completed, wrong-group and include-order failures checked | R844-2 | 98c0b62be911f5cff7a03ebfee7f837c23847d14 |
| Tests | CLEAN | egress_ledger.py:265,334; sw/firmware/ctrl/test/aecp_retry_mutants.py:200; run.py:515,776; author-r4 firmware/gate receipts; controls kill the acceptance defect and fresh tests cover changed host code | R844-2 | 98c0b62be911f5cff7a03ebfee7f837c23847d14 |
| Docs | CLEAN | section 13 ledger/ruling map; FR_NFR 3.4.1; AECP and harness READMEs; PR #914 body; author-r4 INDEX, manifest and NOT RUN inventory; both comment scans; R1/R2 are wording residue | R844-2 | 98c0b62be911f5cff7a03ebfee7f837c23847d14 |

**Limits and pending manager duties**

This is source-head approval, not merge authorization or final candidate validation. No manager source bank at this head is claimed or inferred. Broad source execution is the author's published evidence; independent execution here was limited to the ledger/gate controls, original fault fixtures, log regrades, source comparison/scans, compile probes and integrity checks. No fresh CPU simulation, image build, full parent/processor bank, synthesis bank, builder bank, hosted run, container workflow or hardware run was performed.

The known pre-existing `Mailbox.ARoundFillsWhatItsPassHasLeft` 8x8/1if failure remains separately tracked. Existing 1x1 SRP-cost concerns, two-interface debt, the unmeasured k=3 retry interpolation, and the every-source rows owed to #872 are not newly certified by this delta.

The manager must publish this packet, carry R1/R2 to the residue checklist, finish the other independent review, synchronize onto #902's final head after it merges, establish the new byte-identity base, remeasure 8x8/1if using this ledger, and run the required full pass. Validate the resulting current-dev merge candidate with builder/native banks and required hosted/local acceptance at the merge turn; publish those receipts separately. The source base is `7398ec0aeea468d92ff642a03a06e291a0cd58d1`; supplied live dev is `6b66f66d89cf25d2717687bcc2c3bf617685a99a`. Neither is interchangeable with this source head. Renew affected lens coverage after changes, wait for all review rounds, and complete containment and issue/project closure after an authorized merge.

No source edits, commits, pushes, GitHub writes or author contact occurred. `receipts/integrity.log` proves all 1,627 superproject entries against raw tracked bytes, types/modes and index, with no hidden/sparse flags; it also proves all five required initialized submodules against their gitlinks and tracked contents. The external gitlink is unchanged and uninitialized. Working-tree status is clean.

`REPRO.md` records portable commands and receipt provenance. Only REPORT.md and files listed in MANIFEST.sha256 are publishable; scratch is excluded.

R844-2 FINISHED
