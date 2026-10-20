[R670] NEGATIVE - exact head 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5

R670-2 external independent delta review, issue #637 / PR #768.

The functional corrections satisfy this round's reviewed scope. One MINOR remains in the public validation account: it reports a successful full mutation-campaign exit where the receipt records rc 2. The separate successful listener rerun completes the case coverage, but does not change that earlier command's exit. Three wording-residue items are also recorded. No RTL fix or additional full campaign is requested for the MINOR.

Head tree: `fc876150e72e530d5c4122f04c3ec89700523b2a`. Source base: `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`. Previously reviewed head: `63a187e1579474bca562d85304b9a91466877c33`. The delta merges dev `e26f1816` through `8a7e6beb`, followed by eight commits. Processor pin remains `2cbed0a987c1e68402658d69459ab7e5aa571adc`.

Reconstruction and independence

I read AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue's frozen acceptance and public decisions, the exact round-2 assignment, the linked requirements and interfaces, the complete source-base diff and round-2 delta/history, then the public executable evidence. The [assignment](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269988820) accepts one-pass restore with complete rollback and held faces; it requires the cross-port ownership correction.

`independent-initial.md` records my independent verdict and five-lens ledger before opening either prior public review. Subsequent receipt reconciliation identified the account discrepancy below; this final report supersedes that interim verdict. No private author material, management checkout, current other-reviewer report, or other implementation checkout was read. No source edit, commit, push, GitHub write, hardware operation or full bank was performed.

Finding R670-2-F1: MINOR; Tests, Docs

Artifact: PR #768 body, “Validation account (round 2)” row combining the full synthesis run and mutation campaign; issue #637 [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/637#issuecomment-6294768287), “Validation (all rc 0...)”. Exact snapshots are `public-pr-body.md` and `public-review-ready.md`.

Title: The public account converts a failed full campaign plus successful partial rerun into a full-command rc 0.

Authority/evidence: Round-2 assignment item 4 requires an accurate validation account. CONTRIBUTING section 3 and AGENTS sections 5-6 require reproducible execution evidence. At the published evidence commit `180fc3a8e01eb0022b77b504b4709c3e8a3194a4`:

- `published-receipts/campaign/campaign-af5eefc6.log.excerpt` ends `65 checks: 63 PASS, 2 FAIL`, followed by make's error and `CAMPAIGN rc=2`.
- Its failures are the clean listener leg and its mutation, because the listener's generated inputs were absent. The other four clean legs and 59 mutations passed.
- `published-receipts/campaign/campaign-row36-af5eefc6.log` records the required render build followed by `python3 dynmap_mutants.py --jobs 2 36`: `2 checks: 2 PASS, 0 FAIL`, `ROW36 rc=0`.
- The public HANDOFF lines 85-96 correctly describe this combination (`handoff-campaign-excerpt.txt`). Thus all 60 controls are caught and all five clean legs pass across the two executions. The full campaign invocation at `af5eefc6` nevertheless did not return zero.
- The PR table instead says the full synthesis run and mutation campaign at `af5eefc6` returned “rc 0”; the issue puts that same invocation under “all rc 0”. Its cancellation/supersession list does not reconcile this campaign failure.

Impact: A cold reader is told that a named whole-command gate succeeded when its recorded exit is failure. This is an execution-verdict claim, so the owner's RESIDUE exception does not apply. It is not evidence of a surviving functional mutant, and does not invalidate the passing individual cases.

Required outcome: Correct the PR and issue validation account to separate the full campaign (`rc 2`, 63/65 checks passed) from the listener rerun (`rc 0`, 2/2 passed), then state the resulting aggregate coverage: 60/60 mutations caught and five clean legs passed across those executions. Keep the synthesis rc 0 separate. Link both receipts, as the public handoff already does. Alternatively, a genuinely successful full rerun may be reported with its own receipt. No additional execution is needed merely to correct this account.

Verification: Compare the revised public text with both retained raw receipts. The failed first invocation must not be relabeled as successful. This retains the evidence-accounting part of prior R670-F4 in narrowed form; the three source gate defects themselves are fixed.

Wording residue

These items are Docs-only RESIDUE under the owner's wording/comment rules. They change no behavior, measurement, verdict, test oracle, generated artifact or conformance claim and leave no additional lens unclean. Pre-existing instances outside the delta remain with #746.

| ID | Artifact | Authority/evidence and impact | Exact required outcome | Verification |
|---|---|---|---|---|
| R670-2-R1 | `hdl/milan/milan_datapath.sv:4921`; `tb/verilator/milan_dp/sim_nxn.cpp:5528` | New comments cite PR comment `6269988820`. The owner requires behavior/reason and issue/requirement IDs, not issue-comment IDs. This is comment provenance residue only. | In RTL, replace `#637 ruling, PR #768 comment 6269988820` with `#637; D3 18.4`. In the C++ banner, replace `the #637 ruling, PR #768 comment 6269988820` with `#637`. Preserve the behavioral explanation and Milan/D3 references. | Inspect added comment lines; no executable token or expected result changes. |
| R670-2-R2 | `tb/verilator/milan_dp/dynmap_mutants.py:29`, `:35`, `:148`, `:163`, `:310`, `:339`, `:380` | New docstring/comments contain review rounds and reviewer identities. The same source-comment rule applies. Existing older provenance elsewhere is outside this delta. | At line 29 replace `The #637 round-2 controls follow (reviews R669-1 and R670-1)` with `Additional #637 controls follow`; at line 35 replace `round-1 ordering` with `per-port ordering`; in the four section comments remove `round 2`; at line 163 replace `round 1's order` with `per-port order`. Keep runtime mutation names, anchors and check labels unchanged. | Added-line inspection confirms only documentation/comment edits and preserved test behavior. |
| R670-2-R3 | PR #768 body, Linked Issue / roles | Both role entries still say round 2 is “to be assigned”, despite the public review-start notices. This is stale administrative wording, not a changed review verdict. | Replace each “round 2 to be assigned” with “round 2 assigned”, linking its public review-start notice (6294832626 for the internal role, 6294842809 for the external role). Do not imply an unissued positive verdict. | Compare the two role entries with the public assignment notices. |

Results by lens and acceptance

Conformance: CLEAN. `milan_datapath.sv:5484` records validation only for a framed, identified, CRC-clean record. Lines 5769-5773 compose busy, done, fail and blank into the real CSR connections at lines 2837-2841. Saved and empty maps are nonblank; a map failure raises fail and suppresses blank; busy spans the map interval and done waits. D3 section 3 rule 7, section 5.2 and section 18.4 now state the accepted map-only, one-pass transaction and its fault/deadline validation obligation. The processor's normative `07_memory_maps.md` section 5.1 retains ownership in the parent. No processor register-map, top-level port or parameter change exists.

RTL: CLEAN. `amr_fsm` at `milan_datapath.sv:5363`, `:5484`, `:5591` implements three sweeps: remove every dynamic reset set, read/apply saved sets, then put back marked ports. Static ports are skipped. A refused saved ADD marks its port; a refused take-down or put-back enters AS_RB. `amr_pb_r` and the stage/cursor registers reset explicitly; the cursor can represent the end of the record population. The existing rollback reaches stores and owner bits at line 4858 and restarts the crossbar sweep at line 4664. The face multiplexer, CSR/edit/GET/format holds, entity enable and pending qualification remain connected to that restore ownership. Same-clock operation introduces no CDC. The unchanged device arbiter remains stable during a command and drains abandoned reads. Source equality carries the route measurement at `887b6bf2` to this head for `hdl/`, `syn/` and `constraints/`: LUT +260, FF +258, within DR4's 1,250/600 map ceiling; WNS +0.065 ns, WHS +0.036 ns, complete routing. These are published author measurements, not new reviewer runs or full 8x8 placement proof.

Robustness: CLEAN. `sim_nxn.cpp:5050` onward retains first/later record device errors, CRC corruption, rollback, held commands, taint, contention, late-read drainage and retry exhaustion. Lines 5351-5494 add or preserve public status checks for both deadline paths, CRC-clean holes, bad layout/id, invalid ranges, conflicting keys, refused ADD/put-back and real pass-0 DEFAULTS. The directional cases keep the other direction's valid record as a positive control. `maprec8` at lines 5682-5730 grades transfers in both port orders, a cyclic swap, cross-port conflicts and refused put-back; `maprec4` at lines 5735-5770 grades first/last inputs, an emptied intermediate port and a narrower restored format. The valid transfers are saved by the actual writer before reset, not simply injected into post-restore state.

Tests: Functional checks PASS; lens UNCLEAN only for F1's execution-account claim. The tests read PP_STAT through AXI, query GET_AUDIO_MAP, compare ownership/store values and inspect both routing RAMs. The multi-port RAM oracle compares pre-cycle routing to post-cycle routing, with independently expected GET/ownership sets. `dynmap_mutants.py:444` requires nonzero exit, a completed harness failure and every named failing assertion; compilation errors/crashes do not count as kills. The assignment's six arms each have committed stimuli and named killing controls: put-back rows 45/46/55/60, holes 47, layout/id 48/49, ranges 50, conflicts 51/52/57, pass-0 DEFAULTS 53. Status disconnects are rows 38-44/56; row 54 restores the defective per-port ordering and fails 12/219 checks. Makefile ordinary-case inventory and `test_sim_pool.py` add both multi-port legs without removing an existing leg. The boot helper's TX backpressure preserves the held response while the longer public done poll runs; it does not weaken that response oracle.

Docs: Technical contracts PASS; lens UNCLEAN only for F1. `REGISTER_MAP.md:2401` now names the parent map writer in PP_STAT[4], its three attempts 500 ms apart and reset-sticky alarm. Busy/done/fail/blank descriptions match the wiring. D3 18.4 distinguishes map rollback from already-completed processor state, specifies held faces, records deadline obligations and discloses the measured holds. The literal offset binding at `milan_datapath.sv:9152` explains whole-record commands starting at byte zero. The full source-base delta changes no budget/ratchet file; the three previously failing gates now pass. No physical cold-cycle claim was inferred from retained-window resets.

Prior findings, explicitly reconciled at this head

Read after the independent initial pass: [R670-1](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6269970193) and [R669-1](https://github.com/kebag-logic/milan-fpga/pull/768#issuecomment-6268811441).

| Prior items | Disposition and evidence |
|---|---|
| R670-F1; R669-F1/S2 | RESOLVED. Real CSR composition and public assertions; disconnect controls 38-44/56 are caught. |
| R670-F2; R669-F5 | RESOLVED. Three-stage ownership release; maprec8 transfers in both orders and cyclic swap; old-order control 54 is caught. No limitation-only waiver used. |
| R670-F3; R669-F2 | RESOLVED. All six restore arms now have committed real-path checks and killing controls; directional and boundary coverage described above. |
| R670-F4; R669-F3/F4 | Source gate defects RESOLVED: port rationale, C++ structure and assertion wording; unchanged ratchets; focused checks pass and full public docs receipts are zero. Evidence-accounting requirement remains open only as R670-2-F1. |
| R670-F5; R669-F6 | RESOLVED. PP_STAT[4] row names all three producers and alarm semantics. |
| R670-F6 | RESOLVED by the public one-pass ruling and D3 sections 3/5.2/18.4 amendment, including map-only scope and validation obligations. |
| R670-R1/R2/R3; R669-R1/R2/R3 | RESOLVED. Check 15 reference corrected; the two assigned lane labels removed. New residues above are distinct instances. |
| R669-S1 | ADDRESSED in D3 18.4: ungranted request wait counts as an attempt, with the 50 ms capture-hold rationale. |
| R669-S3 | OPTIONAL, explicitly unassigned. A census-to-formula guard remains an optional improvement; new 4x4/8x8 behavioral coverage does not claim to implement it. No blocking finding retained. |

Execution evidence and integrity

All evidence below is source evidence. No manager source bank at this exact head is claimed or inferred.

| Evidence | Result and limits |
|---|---|
| Published evidence tree `180fc3a8.../review-evidence/637-r1` | 362 downloaded public files match the published SHA-256 manifest. The initial 360 receipts plus manifest also match their Git blob IDs. 23 selected raw receipts are retained with source URLs and SHA-256 values in `receipt-provenance.json`. |
| Evidence authentication | GitHub reports this commit unsigned; no detached signature is present in the supplied evidence subtree. Hash integrity verified; signer authentication could not be verified. This is a provenance limit, not a claim that a signature passed. |
| Exact-head docs-workflow receipts | `gates-head/docs-ci/rc.tsv`: 95 commands, all rc 0. Both builder legs and both boundary legs have zero receipts; boundary census is 165 controls. Builder gate 11 is explicitly NOT RUN, not a pass for its underlying physical/build prerequisite. |
| Four exact-head suite shards | 63 suites passed; 2,187,192 checks, zero failures. Four declared field/freshness skips contribute no execution. The reported dynmap/maprec8/maprec4 tallies are 589/0, 219/0, 137/0. |
| Mutation campaign at `af5eefc6` | Main invocation rc 2, 63/65 checks passed; listener rerun rc 0, 2/2. Combined evidence covers 60 killed controls and five passing clean legs. `hdl/` and `tb/` are identical to this head; only the firmware README count changes afterward. |
| Synthesis/route/front-end evidence | Published source-equivalent receipts; no reviewer rerun. The front-end check is analysis, not elaboration. Standalone 8x8 diagnostics do not prove full 8x8 placement. |
| Reviewer focused checks | Seven commands all rc 0: port contracts and self-test (82/82), C++ idiom and self-test (75/75), test-evidence ratchet, capture contract and record-space census (five configurations). `focused_gates.py` runs the independent checks concurrently and retains a log/rc per command. |
| Checkout integrity | `audit_tree.py` verifies 1,422 parent blobs plus all required populated submodule blobs, file kinds/modes and exact index entries. Exact head/tree and all five required gitlinks match. Optional `external` remains uninitialized. No probe modified source bytes. |

The scoped simulator reports version 5.050, but no simulation build or new mutation campaign was run in this review. Existing public receipts and source inspection sufficed for the functional delta; the focused executions falsified the previously failing source-gate claims. Public receipts of a hosting-runner self-test were read as evidence only; that self-test and host orchestration were not executed here.

Reproduction: `python3 focused_gates.py <exact-head-clone> <receipt-directory>`; `python3 audit_tree.py <exact-head-clone>`; `python3 verify_receipts.py` (optionally `--online` to compare retained receipts against their pinned public URLs). Disposable/downloaded material is under `scratch/` and excluded from publication. `MANIFEST.sha256` lists the publishable packet.

Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue/assignment; D3 3, 5.2, 18.4; processor 07 section 5.1; milan_datapath.sv:5484,5769; status/transfer controls | R670-2 | 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5 |
| RTL | CLEAN | milan_datapath.sv:4644,4858,5217,5363,5591,5611; KL_pp_shadow.sv:1018; route/ooc receipts and source identity | R670-2 | 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5 |
| Robustness | CLEAN | sim_nxn.cpp:5050,5351,5389,5468,5682,5735; dynmap_mutants.py:310; error/deadline/refusal/ordering receipts | R670-2 | 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5 |
| Tests | UNCLEAN: R670-2-F1 | sim_nxn.cpp MAPREC; dynmap_mutants.py:444; Makefile:598; test_sim_pool.py; campaign/sweep receipts and public exit claims | R670-2 (applied, not clean) | 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5 |
| Docs | UNCLEAN: R670-2-F1 | D3 amendment; REGISTER_MAP.md:2401; docs-workflow receipts; public PR/issue/HANDOFF validation accounts | R670-2 (applied, not clean) | 8000520cc12ec5d107a2a67f8ba3d6134b87d2b5 |

Real limits and pending manager duties

- Correct F1's public account and obtain reviewer acceptance of that correction; carry R1/R2/R3 to the residue checklist. No defect is cleared by moving it to another issue.
- Physical calibration and the on-board cold cycle are NOT RUN. Field skips, simulation resets and retained-window memory are not hardware proof. The cold cycle is not a finding in this review and remains owed under #637.
- The healthy 1x1 hold of 598-672 clocks uses a zero-latency window model. Actual DDR latency remains unmeasured. The non-shipping 8x8 hold is about 13,700 clocks versus the processor's 4,096-clock gather watchdog; the documented command-timeout and placement obligations remain open.
- Hosted/act acceptance remains with the manager. This review did not inspect current hosted jobs and claims no successful executed hosted aggregate; skipped/cancelled contexts never become execution evidence here.
- At merge time, construct and validate the candidate against live dev `78ca9bdf104819265588726bce4322696c38b8c2` or its then-current successor, with the required builder/native banks and published receipts. No current-dev candidate execution is claimed by this source review.
- Independent review completion, maintainer merge authorization, post-merge containment, physical qualification and final issue/board completion remain separate duties. No merge authorization is supplied.

R670-2 FINISHED
