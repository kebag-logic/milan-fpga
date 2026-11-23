[R899] POSITIVE - exact head a18f0996f4b1b654a232dfe56fa64ee7ecaf697e

R899-2 technical delta review of issue #963 / PR #984. Tree: `a897a1e08c1cd4b63c37b0e5625b819d4649d568`. All five lenses were applied. The named prior source/evidence findings are resolved; no new source finding remains. This technical verdict does not authorize merge or assert completion of the verification bar. The sequencing limitation below prevents representing this report as satisfying the requested strict cleared-context procedure without a replacement review.

Scope and evidence

The source comparison is `dd163e41438acb86e0c4d4e76df90f3f91ace1c0..a18f0996f4b1b654a232dfe56fa64ee7ecaf697e`; the re-review delta is one commit after `4cca956932073b3f704f12f81c53f2934cfa215c`. `delta.patch` and `delta-paths.txt` show only `sw/firmware/ctrl/test/test_aecp.cpp` and `sw/firmware/ctrl/test/aecp_map_mutants.py` changing this round. No production firmware, RTL, interface, workflow, `tb/` file or gitlink changes. The full range has five files, including the earlier production cut and `docs/design/SPLIT_CONTROL_MEMORY.md:2628`; that design entry is unchanged in round 2. Prior technical verdicts for untouched production artifacts stand.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, issue #963's acceptance and public scope, REQUIREMENTS.md, FR_NFR.md 3.4.1, `ctrl_loop.h` THE SHARE, the AECP interface README, then source history and diff. Prior public findings were fetched after the independent diff pass. Current PR and issue readiness snapshots are retained in `public-context.json`.

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/7bd1b85460690e53a860c53d92c44816667e8be2/review-evidence/963-r1) supplied both rounds' receipts. `audit.py` verified all 1,052 author-file published SHA-256 values. No files under its `reviews/` directory were extracted or opened. The evidence commit has no signature header; the selected packet supplies no detached signature. This is hash verification, not signature verification.

Prior finding dispositions

| Finding | Severity and lenses | Disposition at this head |
|---|---|---|
| R898-1 F1 and R899-1-F1 | MINOR; Tests, Docs | RESOLVED. PR Status and issue comment 7100166169 separate 1,756 prior campaign plants, 88 normal suite arms and two dependency-pin controls. The new comment explicitly supersedes the old tally. |
| R899-1-F2 | MINOR; Tests, Docs | RESOLVED. The verification-bar checkbox is unchecked; Status names each execution head and the unrun native sweep. Final-head shard 0 is explicitly only its 18 AECP arms, not the whole gate. |
| R898-1 R1 | RESIDUE; Docs | RESOLVED. The PR now says: "Each observation calls the port as before: a brief observation of the mapping's STREAM_OUTPUT." The once-per-stream disclosure remains. |
| R898-1 S1 | SUGGESTION; Tests, Robustness | RESOLVED. The existing-stream, out-of-format-channel case and `map-read-before-legal` row expose the ordering error. Independent probes confirm new rejection and old escape. |

F1 required accurate units. Live dispatch independently gives 826 control plants, 389 prior AECP plants, and SRP campaigns of 359 + 167 + 15 = 541 plants: **1,756**. Adding 88 suite arms and two pin controls explains the old 1,846. The 1,758 in R898-1 included those two pin controls; the corrected PR follows that finding's permitted alternative of stating each shard's own unit.

Round-1 oversized logs are published excerpts. Their embedded original hashes match the new counting receipt; shard 1 prints `mutants: 826 of 826 caught`, and all three excerpts end in PASS. The live dispatcher independently confirms category populations. This review does not claim to recover omitted lines from hashes.

At the current head, the 20 complete AECP partition logs contain precisely the live table's **390 names**, each once and in its prescribed partition, all caught, every rc 0. The independent inventory self-test reports 1,848 invocations, shards `[88, 827, 391, 542]`; these include campaign controls and are not plant counts. The 18 normal AECP arms pass in their final-head receipt. The complete `--shard 2/4` wrapper was not executed at this head; its entire campaign table ran through the same campaign entry point in 20 partitions. The PR states this distinction correctly.

Artifact-specific lens results

[R899] PASS Conformance - issue #963 acceptance; `test_aecp.cpp:2857-2991`; `aecp_maps.c:488-537`; `ctrl/loop/ctrl_loop.h:64`; published `author/receipts/share/strict-regrade-final.md` - the test represents legality-before-observation for an existing Stream Output, consistent with the unchanged validation contract and cited IEEE 1722.1-2021 7.4.45/.46 and Milan 5.4.2.27/.28. No normative interpretation changes. The prior production conformance verdict is carried forward, not claimed as a new standards investigation.

Unchanged strict receipts show base 2/108 passes over 200,000 cycles in each 8x8/1if arm, versus head 0/106. Maximum head passes remain 149,307 and 153,071 cycles. The formal campaign's rc 0 reporting mode is distinct from strict base acceptance: strict regrading returns 1 for each base run. The cause remains 63 repeated observations during REMOVE/ADD of 63 mappings beside the 550-byte notice to 15 recipients. The cut, limits and graded rows are unchanged. Published product images remain 139,208 ROM bytes and 58.0 RAMB36 at 8x8/1if, and 45.0 tiles at 1x1. These are carried source measurements, not new synthesis or hardware measurements.

[R899] PASS RTL - `delta-paths.txt`; `full-range-paths.txt`; `aecp_maps.c:255-288,478-537`; `aecp_commands.c:116-122`; `sw/firmware/ctrl/aecp/README.md:185-221` - no production dependency of the prior architecture verdict changes. The legality guard still precedes bitmap observation; state remains local to the edit; the brief reader interface is unchanged. No new clock, reset, CDC, indexing or resource claim is introduced. The mutation reverses guards only inside disposable runs.

[R899] PASS Robustness - `test_aecp.cpp:2870-2991`; `aecp_map_mutants.py:119-123`; `control.log`, `order-plant.log`, `old-test-order-plant.log`, `tally-probe.log` - the new illegal mapping uses stream 0 or 1 and a channel equal to its format's channel count, the first invalid channel. Both fixture streams use the same format. The oracle checks legality before recording a read, and the new floor counts output refusals at existing streams not yet observed by the edit.

The first 4,000 seeded edits retain prior random draws: extra stream selection occurs only in the second population's conditional branch. Another 4,000 edits permit the new mapping; not every edit contains it. Raising only disposable tally-reporting floors reproduces **86** qualifying refusals. The source floor remains 20. Status, unchanged map, notice behavior and read counts are checked. Existing repeated-stream, running, unanswered and next-edit-reset cases remain intact.

[R899] PASS Tests - `probe.py`, `probe-results.json`, `audit-results.json`; published `author-r2/receipts/tests/focused-head/` and `firmware/aecp-campaign/p0..p19/` - independent normal execution passes both mapping tests. `map-read-before-legal` fails the required read-count diagnostic at edit 4065; the same production plant against the exact previous test blob passes. The driver exits 0 after expected child statuses 0, 1, 0, 1. The last expected failure is the tally-reporting probe, not a regression.

Published focused receipts show the new row and the 16 other rows graded by the definition caught on their named diagnostics. Complete campaign receipts and normal AECP arms were audited, not rerun wholesale. Coverage receipts show 40 files PASS, `aecp_maps.c` 352/352 lines and 423/424 branches. The cut monolithic coverage command has rc 124 and is not counted as a pass; two coverage-mode gate executions followed by measurement supply the result.

The unchanged-evidence spot check validates 481 unique exact base/head group records, all five target combinations, and loads 0.4891093771929825 and 0.6008172807017544. This audits published measurements; no full service-budget campaign was rerun. Held record-class results are unchanged. The reported-only 1x1 declaring-outputs paced class above its statement remains a baseline limit, not newly passing evidence.

[R899] PASS Docs - PR #984 Status, Description, limitations and checklist; issue #963 comment 7100166169; `docs/design/SPLIT_CONTROL_MEMORY.md:2628`; added comments at `test_aecp.cpp:2866-2868,2935-2937` and `aecp_map_mutants.py:119` - corrected units and execution identities agree with receipts. The 43 completed docs steps are individually rc 0. `gate_24` was cut twice, rc 124; two builder legs were not run at this head. All three are disclosed. New comments describe behavior/reason with surrounding issue/clause references and contain no bench lane, review round, reviewer identity or issue-comment identity. No new source-comment RESIDUE is recorded.

Reviewer-owned technical coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue acceptance; test_aecp.cpp:2857-2991; aecp_maps.c:488-537; strict share receipts; unchanged production authorities | R899-2, carrying untouched R899-1 production result | a18f0996f4b1b654a232dfe56fa64ee7ecaf697e |
| RTL | CLEAN | delta-paths.txt; aecp_maps.c:255-288,478-537; aecp_commands.c:116-122; AECP port contract | R899-2, carrying untouched R899-1 production result | a18f0996f4b1b654a232dfe56fa64ee7ecaf697e |
| Robustness | CLEAN | test_aecp.cpp:2870-2991; aecp_map_mutants.py:119-123; four focused probe logs | R899-2 | a18f0996f4b1b654a232dfe56fa64ee7ecaf697e |
| Tests | CLEAN | probe-results.json; audit-results.json; campaign, normal-arm and coverage receipts; corrected PR claims | R899-2 | a18f0996f4b1b654a232dfe56fa64ee7ecaf697e |
| Docs | CLEAN | current PR/issue snapshots; source comments; SPLIT_CONTROL_MEMORY.md:2628; docs step receipts | R899-2 | a18f0996f4b1b654a232dfe56fa64ee7ecaf697e |

Real limits and pending manager duties

The prior-comment fetch returned full public round-1 review bodies, including surrounding results and ledgers, after my independent diff pass but before this verdict and ledger were written. Reconciling prior findings was required, but reading the surrounding reports then did not meet the user's stricter sequencing instruction. Later probes cannot undo that limitation. The technical results are supported by the listed checks, but a replacement cleared-context review is needed before this report can satisfy that procedural condition. No private author material or other checkout was read.

No manager source bank ran at this exact head, and none is inferred. Source execution evidence is the author's public receipts plus the explicitly identified focused reviewer probes. The native sweep is **NOT RUN and OWED to the merge candidate**. Shard 0 was not rerun as a complete gate at the final source head. No hosted job success or skipped-context execution is claimed; hosted and local workflow acceptance remain the manager's responsibility.

The manager must validate the actual current-dev candidate, publish its identities and builder/native/Yosys receipts, reconcile the train's statement composition, obtain qualifying reviews, and complete authorized merge and post-merge containment. Source base `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` and supplied live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` are distinct. Future candidate execution must not be relabeled source execution. Physical calibration was NOT RUN; field skips and desk results are not hardware proof.

`integrity.json` verifies 1,935 superproject tracked blobs and modes, its exact stage-zero index, and all five required submodules' pinned heads, tracked bytes, modes and indexes. The optional `external` gitlink remains intact and uninitialized. No source fix, commit, push, GitHub write, hardware action or shared installation occurred. `REPRODUCE.md` records a corrected probe-setup error and incidental recursive-fetch failure. Disposable files stay under `scratch/`. Only REPORT.md and MANIFEST.sha256-listed receipts are intended for publication.

R899-2 FINISHED
