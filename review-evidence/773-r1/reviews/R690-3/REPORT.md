[R690] POSITIVE - exact head e658682ed451ba46885225e5b3fc16841f61a5ca

External independent merge review, R690-3, issue #773 / PR #779.
Tree: `5023d9f2e8c37399701a6afc62f39e3054dd0f15`.
Source base: `a032c6d6e3775f145349d5a495c1e1ad12294936`.
Previous reviewed head: `1b47a3dcff0cb65cb5cebe1f86327429a76f775d`.

All five lenses are CLEAN. The prior MINOR measurement finding and reviewer-placeholder RESIDUE are resolved. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. Three previously optional suggestions remain below; none prevents clean coverage.

This is the verdict at the exact published head, not a verdict on a future merge result. The single commit since R690-2 changes only `docs/design/MEDIA_CLOCK_FOLLOWING.md`. Every other tree entry, including executable code, tests, configuration, interfaces and submodule pins, is identical. R690-2 coverage of those artifacts carries forward under the owner’s delta-review rule. The changed prose was independently re-covered under all applicable lenses.

The review reconstructed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public decisions, requirements and interface authorities, the base-to-head diff and history, then executable receipts. The controlling scope is [ruling (b)](https://github.com/kebag-logic/milan-fpga/issues/773#issuecomment-6380110812), with the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/pull/779#issuecomment-6383506324) and [manager correction](https://github.com/kebag-logic/milan-fpga/pull/779#issuecomment-6384888081). Authorities include IEEE 1722-2016 4.3.3 Equation (1), 4.3.5, 10.7 Equation (14), and Milan v1.2 4.4.2.1 / 5.3.7.6. Direct standards examination from R690-2 carries for unchanged interpretations; this round rechecked the local requirements, architecture and MAC interface boundary. The independent verdict and ledger were written before reading other reviewers’ prior report bodies (`independent-verdict.txt`). Prior public findings were reconciled afterward. No private author material was used.

**Focused results**

- `MEDIA_CLOCK_FOLLOWING.md:1887-1890` agrees with the published capture log: the largest 2 ms `[HOLD]` maximum is **2,059,807 ns in 9 of 23 runs**; the other **14 report 2,059,787 ns**. The difference is one 20 ns cycle. The live PR body states the same distribution. The manager’s correction explicitly supersedes the inaccurate historical REVIEW READY sentence.
- The unchanged R690-2 `check_bounds.py` passes at this head, including its sentence check. It independently recomputes both shapes’ arrival bounds, queue margins, supported ranges and MAC figures, and bounds all 31 observations at both offsets. A disposable copy of the prior two pages returns **rc 1 at precisely the old universal sentence**, after passing the numeric checks. `check_delta.py` additionally requires the new affirmative sentences to match the log and verifies the PR roles and immutable delta.
- The start-up maximum remains below 2.126 ms. After the five later events, the render margin is **492,145 ns (1x1)** and **486,968 ns (8x8)**. The 166,667 ns lead is below the strict 231,860 ns Equation (1) ceiling; the page’s 231.8 us ceiling is conservative.
- `MEDIA_CLOCK_FOLLOWING.md:1858-1860` now explicitly says the 8x8 CRF PDU can leave 2,714 ns after **its timestamp less the applied offset**, and that this is after the hand-over, **Equation (1)’s TT**, so it consumes transit budget. The arithmetic remains unchanged: the stated store-and-forward ordering adds 18,040 ns against 15,326 ns spare. The interface at `docs/integration/INTEGRATION_GUIDE.md:74` and MAC integration at `sw/litex/milan_soc.py:1748-1807` preserve the distinction between ownership transfer and later egress. Backpressure that prevents transfer is not exempted by this wording.
- The PR body explicitly names internal reviewer `[R689]` and external reviewer `[R690]`. Its Status table remains the author’s explicitly head-labelled execution record at 1b47a3dc and earlier heads; the manager’s separate correction identifies the current documentation commit. No source-bank execution at e658682e is inferred from that table.
- All six requested documentation commands pass with the hash-pinned renderer. No source comment changed in this delta, so it introduces no comment-provenance residue.

**Evidence and execution**

| Check | Result | Receipt |
|---|---|---|
| Exact delta and PR snapshot | One documentation commit, only the named page changed; current head, measurement sentences and roles verified; PR head/body stable at final read | `delta.diff`, `delta-check.log`, `pr.json`, `provenance.json` |
| Independent numeric and sentence checks | rc 0; 31 observations bounded; 23-run distribution reproduced | `check_bounds.py`, `bounds.log`, `bounds.rc` |
| Prior bad-sentence control | Expected rc 1; numerical checks pass first, universal sentence fails | `prior-sentence-control.log`, `prior-sentence-control.rc`, `check_delta.py` |
| Documentation wording/privacy and style | 0 findings; 23 current documents pass style | `docs-check.log`, `doc-style.log` |
| Em-dash gate against a032c6d6 | 0 findings over 202 added lines; 339/339 controls | `em-dash.log` |
| Documentation paths | 1,062 cited paths resolve; two allowlisted; ten line anchors valid | `doc-paths.log` |
| TOC anchors and drift | 537 cross-page fragment links reproduced; 149 annotated TOCs pass | `toc-anchors.log`, `toc-check.log` |
| Published execution receipts | Hashes verified; four shard commands, return codes, head/tree and suite membership reconciled | `publication-hashes.json`, `evidence-audit.log`, `verify_evidence.py` |
| Final source integrity | 1,442 parent blobs, raw bytes, executable modes and index match HEAD; all five required initialized submodules likewise match their gitlinks | `tree-final.log`, `tree-final.rc`, `audit_tree.py` |

The source execution evidence is the [published author packet](https://github.com/kebag-logic/milan-fpga/tree/1faf10a1331f93451a6aa4e43956a51de6ab4da3/review-evidence/773-r1). The four shards at **1b47a3dc / f608aefd** cover 15, 16, 17 and 16 suites, each rc 0. Their union equals the current 64-suite inventory exactly, with **2,190,887 checks and zero reported in-suite failures**. Spot-checked excerpts report capture_coherence junction 20,832/0, datapath 847/0 and controls 42/42; AAF startup controls 8/8; milan_dp legs zero failures. Behavior receipts report 406 scenarios / 1,977 steps passed; lint reports 89 <= 89. These are earlier author executions carried by unchanged artifacts, not new runs at the reviewed head.

The earlier documentation aggregate has 41 successes, two explicit skips, and an initial base-resolution failure superseded by the successful direct-base em-dash receipt. Skips are not executed passes. Earlier synthesis, route and campaign receipts retain their original named heads. No manager source bank exists or is claimed at e658682e.

The evidence commit is **unsigned**: local signature status N and the repository API both say unsigned. No detached signature was supplied. This review verifies published SHA-256 bytes, including declared publication redactions, and receipt consistency; it does not claim cryptographic signer authentication. Sixty-six selected receipt hashes were checked, and the unchanged bound/evidence scripts were checked against their public manifest at `25317d59bec88014249f28df80e6b45218827f49`. Only the expected-head constant was changed in the portable tree auditor.

The pinned renderer was installed in a disposable local environment from `tools/markdown/requirements.txt` with required hashes. Three initial gates refused because the local runner resolved the environment’s interpreter symlink to the system interpreter. The runner was corrected; all six documentation commands then passed using the pinned environment. The initial rc-2 receipts are retained as environment failures, not source findings. Package identities and final commands/return codes are in `renderer-identity.json` and `checks.json`.

**Prior-finding reconciliation**

| Prior ID; severity; all attributable lenses | Disposition at this head | Cause-specific evidence |
|---|---|---|
| R689-1-F1; MINOR; Docs | Resolved, carried from R690-2 | Design page:1871-1900 and :2045-2053; matrix:191; both start-up and grid-live bounds, margins and eight-period supported range recomputed in `bounds.log` |
| R690-1-F1; MINOR; Conformance, Docs | Resolved under both original lenses | Same bounds; every measured maximum fits; default queue margin remains positive |
| R690-1-F2; MINOR; Conformance, Tests, Docs | Resolved, carried from R690-2 | Complete 1b47a3dc four-shard execution, head/tree/commands/rc bound; unchanged code and tests at e658682e; PR claims retain their actual execution heads |
| R689-1-R1; RESIDUE; Docs | Resolved | `hdl/ieee1722/crf/KL_media_domain_event.sv:28-33` contains the requested terms; comment-stripped equality independently rechecked; file unchanged this round |
| R689-1-S2; SUGGESTION; Docs | Taken and resolved | Design page:1846-1865 states MAC-level quantities and exclusions; rational arithmetic passes |
| R689-2-F1 and R690-2-F1; MINOR; Docs | Resolved at the cause in R690-3 | Design:1887-1890, live PR and manager correction now match 9/23 and 14/23; old sentence fails the disposable control |
| R689-2-S1; SUGGESTION; Conformance, Docs | Taken and resolved | Design:1858-1860 names timestamp-minus-applied-offset and the post-TT transit boundary |
| R689-2-RES1 and R690-2-R1; RESIDUE; Docs | Resolved | Current PR role lines name both assigned reviewers; `delta-check.log` |
| R689-1-S1; SUGGESTION; RTL, Robustness | Retained as optional | Detail below |
| R689-2-S2; SUGGESTION; Tests | Retained as optional | Detail below |
| R689-1-S3 / R689-2-S3; SUGGESTION; Tests | Retained as optional | Detail below |

The final public snapshot has no submitted PR reviews or inline comments requiring another disposition. Prior report findings were read after the independent verdict; the other current-round report was not used as evidence for this verdict.

**Retained optional findings**

| ID / severity / all lenses | Artifact and authority/evidence | Impact | Optional required outcome | Verification |
|---|---|---|---|---|
| R689-1-S1 / SUGGESTION / RTL, Robustness | `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:243-265`, `hdl/ieee1722/crf/KL_crf_tx.sv:302-317`, `hdl/milan/milan_datapath.sv:1482-1506`; ruling (b) relies on documented spare at the evaluated product clock | Unusual configurations lack an executable guard for the spare’s arbitration allowance; no defect established for the accepted shapes | Optionally guard sufficient spare at the product clock or state the configuration condition beside the guard | Accepted product shapes pass; a shape with inadequate spare is rejected or explicitly excluded |
| R689-2-S2 / SUGGESTION / Tests | `author-r2/receipts/round2/sweep/shard-0/clone_identity.txt:3`, `scripts/run_all_suites.sh:86-90`; receipt reports two tracked changes, while the driver documents result-file regeneration | Count alone cannot prove which paths changed or pre-run cleanliness; remains a provenance limit | Record pre-run status and post-run changed paths/diff | Confirm only the expected generated result files changed |
| R689-1-S3 / R689-2-S3 / SUGGESTION / Tests | `tb/verilator/capture_coherence/sim_dp.cpp:548-643` and published `[WIRE]` minima; contention cover remains derived | No measured worst-age contended scenario anchors that derivation | Optionally add a maximum-frame/other-output contention scenario | Its measured hand-over remains in the window and a targeted defect fails the check |

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling (b); `docs/design/MEDIA_CLOCK_FOLLOWING.md:1858-1900`; `docs/integration/INTEGRATION_GUIDE.md:74`; `sw/litex/milan_soc.py:1748-1807`; `bounds.log`; boundary and default-fit claims hold | R690-3 delta re-cover; R690-2 unchanged coverage carried | e658682ed451ba46885225e5b3fc16841f61a5ca |
| RTL | CLEAN | `delta.diff`; `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:238-266,779-785`; `hdl/ieee1722/crf/KL_crf_tx.sv:299-318,540-546`; `hdl/milan/milan_datapath.sv:1459-1531,7438-7446`; no executable/interface change | R690-3 identity check; R690-2 coverage carried | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Robustness | CLEAN | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1861-1900`; `tb/verilator/capture_coherence/sim_dp.cpp:548-643`; start-up/fallback, both offsets, drift qualification, queue margin and bounded MAC transit; unchanged mutation controls | R690-3 delta re-cover; R690-2 behavior coverage carried | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Tests | CLEAN | `check_bounds.py`, `bounds.log`, `prior-sentence-control.log`, `delta-check.log`; author four-shard receipts and unchanged test blobs; new statement is falsifiable against raw observations | R690-3 focused checks; R690-2 suite coverage carried | e658682ed451ba46885225e5b3fc16841f61a5ca |
| Docs | CLEAN | `docs/design/MEDIA_CLOCK_FOLLOWING.md:1858-1860,1887-1890`; `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191`; live PR roles/measurement and manager correction; six successful documentation gates | R690-3 | e658682ed451ba46885225e5b3fc16841f61a5ca |

**Limits and pending manager duties**

Physical calibration is **NOT RUN**. Field skips and simulation passes are not hardware proof. True-clock 8x8 TDM32 remains derived-only, as the ruling permits; the 8x8 entity test uses different clocks. The MAC analysis does not cover multiple maximum frames ahead, the MAC’s crossing/pipeline, or 100 Mb/s. Post-TT delay consumes the stream’s transit budget; arbitrary transfer-blocking backpressure is not proved safe. Bench predictions remain unmeasured.

No full parent/processor/synthesis/builder bank, hardware action, shared install, source fix, commit, push, GitHub write or merge was performed. No exact-head hosted execution was audited or inferred from emitted/skipped contexts. The manager owns hosted/local-replica acceptance, the independent-review completion bar, and final current-dev merge-candidate validation, including builder and native banks and publication of their receipts. Source evidence is distinct from that candidate. The stated source base and live dev are a032c6d6e3775f145349d5a495c1e1ad12294936; recheck live dev at the merge turn. This report grants no merge authorization. Authorized merge, post-merge containment, and issue/project disposition remain manager duties; the PR uses “Relates to #773”.

Portable reproduction: run `verify_evidence.py REPO PACKET`, then `check_bounds.py REPO PACKET/public/author-r2/receipts/round2/sweep/excerpts/capture_coherence.txt`, `check_delta.py REPO PACKET PACKET/pr.json`, and `audit_tree.py REPO`. `run_checks.py REPO PACKET PINNED_PYTHON` records the gates. Disposable environments and controls remain under `scratch/`; they are not publishable. Only REPORT.md and files listed in MANIFEST.sha256 are publishable. The final raw-byte/mode/index/gitlink audit passed; no source bytes required restoration.

R690-3 FINISHED
