[R942] POSITIVE - exact head 079c4fa1514be460949ddc28ae3277ea1873cb48

External independent review, R942-2, issue #1009 / PR #1017. All five lenses were applied. No BLOCKER, MAJOR or MINOR remains in this source delta and its required evidence. One RESIDUE item is recorded below. This verdict does not complete physical acceptance, authorize merge, or validate the future merge candidate.

Tree: `be2122cbd487361b4ed8a99ff283565c1bec3eb2`. Source base: `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`. Round delta: `85569e241625d8e4176aae7d77c524783dff30cd..079c4fa1514be460949ddc28ae3277ea1873cb48`.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README, the issue and public scope decisions, requirements/interfaces, source diff/history, then public execution evidence. The independent verdict and five-lens ledger were written before prior review findings were read. No concurrent round-2 review was consulted. No formal reviews or inline threads were present at inspection; the prior findings are in the two round-1 conversation comments.

Authority: [#1009 ruling 3](https://github.com/kebag-logic/milan-fpga/issues/1009#issuecomment-7176978406), REQUIREMENTS.md, DR2a at `docs/design/SAVED_STATE_MATERIALIZATION.md:2394`, the flash/state interfaces and `sw/firmware/ctrl/loop/ctrl_loop.h:121`. Ruling 3 controls this whole-commit step. The binding class gets 100 ms; other classes retain 1,000 ms. KLJ3 minor 0, two-slot atomicity, blank checking and verification remain. Strict save-before-response is the stated departure owned by #1012, not a newly introduced claim of conformance.

Evidence anchors: [round-1 author packet](https://github.com/kebag-logic/milan-fpga/tree/a7eb193aa6d85f970500c8ca64ea45189a8ba7a3/review-evidence/p1win-r1/author), [round-2 author packet](https://github.com/kebag-logic/milan-fpga/tree/e2d4a1d3ca42c07812cb2112446eb6b8c73120ef/review-evidence/p1win-r2/author), [prior external findings](https://github.com/kebag-logic/milan-fpga/pull/1017#issuecomment-7182393758), and [prior internal findings and narrowing](https://github.com/kebag-logic/milan-fpga/pull/1017#issuecomment-7184600298). Below, `r2/` means that pinned round-2 author directory; `r1/` means the pinned round-1 author directory.

**Delta and five-lens examination**

[R942] PASS Conformance - `sw/firmware/ctrl_nvm/nvm_store.h:22`, DR2a `SAVED_STATE_MATERIALIZATION.md:2394`, `r2/full-run/*-identity.txt`, `*-results.json` - the revised explanation names the existing step pace explicitly; it changes neither window nor bound. The full execution records now identify the exact head, tree, submodule pins, command, successful exit and clean status before/after. The results retain the required idle, in-flight, burst and other-class distinctions.

[R942] PASS RTL - `sw/firmware/ctrl_nvm/nvm_store.h:29`, `sw/firmware/ctrl/loop/ctrl_loop.h:149,422`, `r2/receipts/lut-attribution.txt`, `r1/receipts/win/images.txt` - the round delta is three comment lines replaced by three comment lines. Removing comments leaves identical bytes. The explicit `CTRL_LOOP_STEP_AGE + 1` is three centiseconds. No executable source, HDL, clock, reset, CDC, interface, layout or gitlink changes. The resource evidence now separates synthesized counts from placed counts and identifies the partial ROM banks mapped to logic.

[R942] PASS Robustness - `sw/firmware/ctrl_nvm/test/test_nvm_window.cpp:69,156,190,233,249`, `tb/verilator/ctrl_service_budget/bind_save.py:140,277`, `save_grade.py:75` - unchanged coverage of class boundaries, non-restarting windows, capture joins, in-flight ordering, retry backoff, burst convergence and swept cuts carries forward from the clean prior round. The comment does not alter its dependencies. Focused binding/verify controls independently confirm rejection of duplicate-byte, pre-program and cross-write read coverage. Board summaries are checked only to the limits stated below.

[R942] PASS Tests - `r2/full-run/*-results.json`, `*-table.md`, `r2/receipts/gate-*.txt`, `audit-packet.txt`, `probe-grade.txt` - both 113-group records and their published hashes were checked. Counts and complete tables regenerate from the published group results. The seven 8x8 held-egress rows satisfy the unchanged ledger. Independently executed: 33 binding/verify controls pass, all 26 associated planted defects are caught, and the load calculation passes. Published gate receipts consistently name this clean head; no full execution bank was rerun by this reviewer.

[R942] PASS Docs - `sw/firmware/ctrl_nvm/nvm_store.h:22`, the store README, DR2a, `r2/PR-BODY.md`, `r2/receipts/lut-attribution.txt` - the antecedent defect is corrected exactly. Timing claims distinguish simulated busy times, idle versus in-flight changes, measured board brackets, and pending work. The PR reports the single registration-share overrun instead of calling all passes clean. One redundant LUT headline needs the wording correction below; its detailed measurements already state the actual values. No prohibited label or review identity was introduced in the source-comment delta.

**Results checked at their evidence source**

| Evidence | Checked result and qualification |
|---|---|
| Full service runs | 113 unique groups per point; 968 measured probe instances at 1x1/1if, 974 at 8x8/1if; no refusals or save misses. Identity receipts record full commands with 16 jobs and exit 0 from the clean exact head. Both complete tables reproduce from the group results. |
| Ordinary service rows | Excluding the deliberate 60 ms held-egress group, maximum ACMP is 4.84739 / 8.29073 ms, notification 3.17894 / 3.26262 ms, SRP 9.23753 / 11.48331 ms (1x1 / 8x8). All these rows meet their 20 ms budgets and therefore the assigned ACMP/notice bounds. |
| Known exceptions | Seven held-egress misses at each point; all seven 8x8 rows remain below their unchanged ledger figures. No 1x1 work-pass overrun; one 8x8 `srp-bound` pass at 2.12037 ms. `kept_grade.py:3` and `run.py:941` retain the pre-existing #977 disposition. This is not a newly clean 2 ms measurement and no allowance was raised here. |
| Idle / in-flight / burst | Maxima 304.535 / 550.481 ms on idle stores; 394.959 / 891.169 ms at capture-end among ten in-flight arrivals; burst convergence 306.463 / 646.392 ms, four / two saves and erases. Bounds remain 800 ms idle and 450 / 950 ms in flight. |
| Other-class saves and load | Save-burst 1,097.438 / 1,353.998 ms; save-flight 147.073 / 650.995 ms, below 5 s in these simulations, whose other-class groups have no device busy delay. Independently calculated load 0.512 / 0.744, below 0.70 / 0.76. The load script directly gates 1x1; the latter comparison uses its reported 8x8 value. Longest pass carrying the store step 1.15805 ms; longest store step 0.79312 ms. |
| Clean gate receipts | Store: 656 executions across five shapes and 170 planted defects; coverage: 513/513 store lines, 317/326 branches before the nine documented exclusions; budget self-test: 321 mutants caught; restore grader: 79 checks; firmware, platform-memory and documentation gates: successful receipts. These are author executions, not independent reruns here. |
| Synthesis and placement | 8x8: 48,021 -> 48,044 synthesized LUTs (+23), then 45,814 -> 45,973 placed (+159). 1x1: 34,476 -> 34,495 synthesized (+19), then 32,656 -> 32,647 placed (-9). Generated logic inputs are reported equal apart from firmware ROM contents and nonfunctional text; the partial ROM bank maps to logic. Hierarchical changes include parent and leaf rows and must not be summed as independent cells. This supports ROM-content-dependent synthesis plus physical optimization, not statistically proven placement noise or zero synthesized growth. |
| Routed qualification | The same preselected placement recipe was used for each endpoint. Implementation slow WNS / least WHS: +0.045 / +0.036 ns at 8x8/1if; +0.126 / +0.036 ns at 1x1/1if. Tiles stay 98.5 / 80.5. The base 1x1 hold value +0.013 ns misses the stated floor; the implementation passes. No route or memory-ledger rerun is claimed. |
| Board summaries | 108 command readings plus 36 cut-hold readings at 8x8, and 24 plus eight at 1x1: 144 and 32 total. All reported upper readings are below 800 ms. All 44 graded bind cuts assert idle at bind, durability before outlet-off, and at least 1.271 s before the last DUT frame, exceeding 250 ms. The summaries also count three additional outlet actions without bind-hold readings; those are not the 44 graded cuts. Their original acquisitions and grader are not in this packet, so this checks published summaries, not an independent regrade of physical traces. |

The service-harness ELF identities in the clean-run receipts are `f4bbbb4d0107ec8e54d9bcec04add8d11c16bfdfd4137e32d4bb34bcc6a9448e` (1x1) and `57c023afc9e6a7b0c4f022f75aa8e27ae2149945b3f88447d5addd90b789336d` (8x8/1if). Each results file's executable digest matches its identity receipt. These are not the physical-image ELFs: the routed-image receipt records `bf81ad95d6df374b6e746df92f83bbc6e5e5049e3d3a1b9918721d985939bca1` and `6c82d9626ebf898252b5843bfeed48c362f6df2e4786007c57cd4782e4bbed21`, respectively, built at `8a4ad2c4`. Later source changes are documentation, the coverage ratchet and this comment. Binaries are not included in the public packet, so their digests are attested by receipts, not independently rehashed here. The two board summaries alone do not identify the deployed ELF; that linkage remains part of physical acceptance.

**Disposition of every named prior finding**

| Prior ID | Disposition at this head |
|---|---|
| R942-1-F2, narrowed by R941-1; Conformance, Tests, Docs | RESOLVED. The clean exact-head full-run identities, results, tables and exit statuses now satisfy the retained requirement. Hashes, counts, rows, ledger limits and reconstructed tables pass inspection. Split-target and interchange closures established in R941-1 are retained: the comment delta touches none of their executable inputs. No manager source bank is used to close this finding. |
| R942-1-F1; Conformance, RTL, Tests, Docs | RESOLVED at the resource-evidence cause. The new post-synthesis/placement attribution supplies the missing intermediate counts. The earlier inference that all firmware ROM was block RAM is not repeated: the receipt explicitly identifies partial banks in logic. Ruling 3 imposes timing, ledger and block-RAM limits, not a hard LUT-difference cap. The measured +159 remains recorded. |
| R941-1-RES1; Docs | RESOLVED. `nvm_store.h:29-31` names the step pace explicitly, exactly as requested; behavior and bounds are unchanged. |
| R941-1-S1; RTL, Docs | Attribution suggestion SATISFIED by `r2/receipts/lut-attribution.txt`. Only 8x8/1if and 1x1/1if were routed. Whether the superseded ruling's two-interface route is additionally required remains the manager's explicit scope question; no such result is claimed. |
| R941-1-S2; Tests, Docs | Clean-receipt suggestion substantially SATISFIED: the store, coverage, budget self-test, restore self-test, firmware, memory, platform, load and documentation receipts name this clean head. Fresh split-target campaigns remain the prior clean-head evidence. The six size-fixture arms are not newly rerun in r2; their unchanged-source prior disposition remains. |
| R931-1-F1/F2/F7/F8 and R932-1-F2, as disposed on PR #1017 | Prior closures RETAINED. No executable dependency changed. The split-target window/whole-container checks, separately ruled in-flight bound, complete-save ownership and byte-coverage checks remain. The focused verification controls pass again. |
| R931-1-F6 evidence obligation | RESOLVED through the full-run closure above. No claim is made that existing #977 debt was fixed. |

The separate frame-format findings on #1014 are outside this whole-commit step; none is declared closed here.

**R942-2-RES1 - RESIDUE - Docs - `r2/PR-BODY.md:90`, PR “Memory and fit” headline**

Authority/evidence: the headline says “The LUT difference is placement, not design growth.” The same paragraph already gives +23/+19 synthesized LUTs and explains the partial ROM banks in logic. The detailed figures and attribution are explicit; the headline is misleading shorthand.

Impact: wording obscures the synthesis contribution. No measurement, figure, test, artifact, verdict or protocol claim needs changing.

Required outcome / exact fix: replace that bold sentence with **“The LUT difference comes from changed firmware ROM contents and the resulting physical optimization.”** Keep the numerical evidence unchanged.

Verification: compare the edited sentence with `r2/receipts/lut-attribution.txt`; confirm all counts and qualifications remain. Carry on the manager's residue checklist. This item does not make a lens unclean. No additional suggestion is filed.

**Reviewer-owned ledger**

Scope is the reviewed source delta and its evidence closure. Physical and merge acceptance remain separate below. Untouched prior clean coverage is carried only after checking its dependencies.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1009 ruling 3; DR2a:2394; nvm_store.h:22; r2 full-run identities/results and gate receipts | R942-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| RTL | CLEAN | nvm_store.h:29; ctrl_loop.h:149,422; comment-only delta; r2 LUT attribution; r1 routed receipts | R942-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Robustness | CLEAN | test_nvm_window.cpp:69,156,190,233,249; bind_save.py:140,277; save_grade.py:75; probe-grade.txt; prior clean dependency check | R942-2, carrying unaffected R942-1 coverage | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Tests | CLEAN | r2 results/tables; clean gate receipts; audit-packet.txt; probe-grade.txt; load-check.txt | R942-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |
| Docs | CLEAN; RES1 carried | nvm_store.h:22; store README; DR2a; r2 PR body, identities, LUT and board summaries | R942-2 | 079c4fa1514be460949ddc28ae3277ea1873cb48 |

**Independent receipts, limits and pending manager duties**

`audit_packet.py` verifies all 1,987 tracked superproject blobs, modes and index against the exact head, the four required initialized submodules plus the SRP submodule, the comment-only delta, both author manifests and committed packet bytes, the full-run identities and tables, selected budgets, and the per-cut summary arithmetic. `audit-packet.txt` is its successful raw receipt. `probe_grade.py` / `probe-grade.txt` record the independent 33 checks and 26 caught defects. `load-check.txt` is the independent static-load receipt. Reproduction commands and evidence limits are in `RECEIPTS.txt`. Disposable files stay in `scratch/` and are excluded from publication.

The packet's hashes and immutable archive commit were verified. The available archive commit is unsigned and no detached signature was published; cryptographic signer authentication was therefore not performed. This is integrity checking, not a claim of signature verification.

No full parent, processor, synthesis, builder or service-execution bank was run here. No hardware was touched. Physical calibration is NOT RUN; field skips are not hardware proof. No source edits, commits, pushes, shared installs, container runs or GitHub writes occurred. No simulator execution was needed for the comment-only delta. Final bytes/modes/index and required gitlinks remain exact, and the published branch still names the reviewed head.

The manager still owes:

- Physical acceptance or an explicit public resolution decision: the existing 31.7-37.1 ms brackets do not meet <=10 ms; the corrected paired reader is described as prepared, not executed. The inconclusive 8x8 input-0 case remains context pending its corrected rerun. Do not count it as passed. Retain deployed-image identity, board in-flight <=1,000 ms evidence, the boot-read comparison and the complete physical receipts.
- The S1 scope question about an additional 8x8/two-interface route, if applicable; no extra route is implied by this review.
- The current-dev candidate built from source base `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350` and live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` (or the then-current tip), with the required builder/native banks and published candidate receipts. There is no manager source bank at this head, claimed or inferred.
- Hosted and local workflow acceptance, distinguishing executed jobs from skipped contexts; the independent-review completion bar; explicit maintainer merge authorization; post-merge containment and issue/project closure. Hosted status was not used as execution evidence here.
- R942-2-RES1 on the residue checklist.

R942-2 FINISHED
