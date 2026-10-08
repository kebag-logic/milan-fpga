[R533] POSITIVE - exact head fe1cd0679f5028c749af7242c903a82ca2b3d692

R533-14 external independent delta review of issue #665 / PR #690. Tree `1452e3d48865f09739432b92608401371257dfb1`. All five source-review lenses are CLEAN. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. Prior source findings retain their resolved dispositions; R532-12-S1 remains optional. This verdict does not authorize merge or complete the umbrella issue.

The independently reviewed delta is `154722e14781c7373f3229420b6e007f9bcf9835..fe1cd0679f5028c749af7242c903a82ca2b3d692`: one commit, exactly two files. The complete source-base diff against `99e4eb6c14462aafa84bb1ac597fd241abc1a240` and history supplied context. Round-13 coverage is retained for unchanged artifacts; the firmware and prior campaigns were not independently rerun this round.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, linked requirements and interfaces, diff/history, then executable evidence. Controlling public inputs are the [F4 contract](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), [round-14 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6055458854), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6055933097), and [review start](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6055957838). Requirements retain the selected ownership, shipping-default and physical-evidence limits in `REQUIREMENTS.md:24`, `docs/reference/FR_NFR.md:317` and `docs/design/MAILBOX_SPLIT.md:268`.

The independent verdict and five-lens ledger were written before opening prior review findings or reports; `receipts/independent-verdict-order.txt` records that boundary. Only public material and this isolated checkout were read. No other lane, private author material, management scratchpad, candidate host runner, container replay or remote write was used.

**Manifest and trust assessment**

`scripts/act_ci.py:229` adds exactly `("third_party/lwSRP", "third_party/lwSRP", "https://github.com/kebag-logic/lwSRP.git")`, matching `.gitmodules:13`. `REQUIRED_SUBMODULES` at :235 derives four materialized paths and continues to exclude `external`. The exact tree and index contain five gitlinks, including lwSRP `9197193e47a6bb1c45a56d90a18c1784123aba44`.

Every other production syntax-tree node equals the parent. `git_environment` (:1069), `git_prefix` (:1086), committed-blob validation (:1671), materialization (:1736), and orchestration (:5256) are unchanged. Manifest validation still precedes checkout and dependency fetch; workflow sandbox checks still precede dependency materialization. Git disables transports by default and enables HTTPS alone, with hooks, helpers, prompts and ambient configuration withheld. The SSH-only `external` tuple must match but is never selected for fetch. The addition authorizes one fixed public dependency already required by F4; it introduces no generalized network, credential, path, callback or host-execution authority.

The manager's proposed live-dev runner plus exactly this tuple is the minimal sound adaptation. The trusted source at `17f62ef64a66562384e8a93b1d6be6f86e51f95c` has the old manifest and otherwise the same production syntax tree. An inert, unexecuted construction of the proposed adaptation preserves every other node. Trusted-base file SHA-256: `79579e6b618f1d05fae202018e18f066a23cd8d667202fdbe03b561ecad638f8`; manifest-only adapted bytes: `35d2cd4436a9beab31e59be1e67d7eadef28b8e448401ee7717c0af4836e67d4`.

Use the documented audited-install mechanism for those adapted bytes: record the base commit, exact patch and installed digest, install outside the candidate without writable mode bits, and invoke with the explicit repository/worktree and digest arguments. Editing a trusted-dev worktree in place would violate its clean-byte check. This review approves the narrowly described adaptation; it does not attest that an installation or replay has happened. Candidate runner bytes remain confined to the disposable job for their self-test.

**Refusal and test assessment**

The fixture at `scripts/act_ci.py:10590` is a literal inventory independent of `TRUSTED_SUBMODULES`. Omitting lwSRP from both candidate trust and its previously derived fixture can no longer hide the omission. The materialization assertion at :10624 names all four public paths explicitly. `SelftestTally.refused` at :5341 records failure when the expected refusal disappears.

| Case in `selftest_lwsrp_manifest`, :10685 | Specific reason for refusal | Discriminating evidence |
| --- | --- | --- |
| Drop lwSRP config | Missing path and URL keys; gitlinks unchanged | Published equality-removal plant fails the named drop assertion |
| Duplicate lwSRP config | Repeated keys before dictionary equality | Duplicate-key guard removal fails the named duplicate assertion |
| Add another lwSRP config | Unexpected name/path keys; gitlinks unchanged | Equality-removal plant fails the named addition assertion |
| Redirect lwSRP URL | Changed trusted URL value | Equality-removal plant fails the named redirect assertion |
| Drop lwSRP gitlink | Missing allowlisted tree path | Gitlink-guard removal fails the named omission assertion |
| Add lwSRP gitlink | Unexpected tree path | Gitlink-guard removal fails the named addition assertion |

The two standing trust plants at :10706 replace only the expected config dictionary, respectively permitting omission and addition. They leave the gitlink list equal to the trusted list. The validator therefore returns and the nested refusal assertion records one failure, which the outer check requires. The independent probes reproduce that data relationship. A failure from another guard cannot mask these plants.

The eight published source-mutation cases include the missing inventory entry, missing materialization path, duplicate-key guard, config equality and gitlink guard. Equality removal is deliberately used for three distinct named assertions; gitlink-guard removal for two. These are eight check/plant pairs, not eight distinct implementation mutations. Every raw mutation log contains its intended `FAIL` assertion, and the baseline has zero failures. These executions belong to the author, inside the published disposable-job recipe, and were inspected as evidence rather than run here.

The independent probe script never imports or executes `act_ci.py`. It parses its syntax tree, compares unchanged production nodes, and submits inert manifests to Git's config parser under an empty configuration environment. Its oracle accepts the exact manifest and refuses all six assigned cases plus wrong path, SSH URL, escaping path and custom update command. This is focused static/data evidence, not an execution of the candidate validator or a substitute for the manager's live replay.

**Evidence and independent executions**

| Check | Result and receipt |
| --- | --- |
| Independent manifest/trust probes | PASS; `receipts/manifest-probes.log`, `.rc`; `scripts/audit_manifest.py` |
| CI contract | PASS, 1741 contract items; `receipts/ci-contract-check.log`, `.rc` |
| CI contract controls | PASS, 2362 arms; `receipts/ci-contract-controls.log`, `.rc` |
| Documentation/privacy | Zero findings across 200 Markdown and 1191 text files; 23/23 scrub controls, 4/4 routing arms; `receipts/docs-check.log`, `.rc` |
| Documentation style | PASS, 22 current documents; `receipts/doc-style.log`, `.rc` |
| Published exact-head receipt audit | All 87 successful command records match the publisher's original/public hash mapping, including 11 path-redacted logs; `receipts/public-evidence-audit.log`, `.rc` |
| Published runner and mutation evidence | 442 passing runner checks; baseline and eight named defect catches; raw receipts in `receipts/published-source/` |
| Source restoration | 1215 superproject blobs, modes and complete index equal HEAD; all five gitlinks exact; three initialized dependencies verified; `receipts/checkout-verification.log`, `.rc` |

The [immutable author packet](https://github.com/kebag-logic/milan-fpga/tree/2276e34a9a7a615cdf65b4e6c026129680ede1f9/review-evidence/665f4-r1/author-r14) is source execution evidence. Its scope receipt names this exact head and runner SHA-256 `35890beace97bf9e2b26bb24a8016b585767e24566ffbf9a62a0ada0beccfd66`, matching the reviewed file. Its complete control log has 51 named arms and 1252 checks, with zero failures. Its compiler log records 2146 invocations and zero omitted arms. The builder log explicitly says all gates pass except one NOT RUN calibration arm. No manager source bank at this head is claimed or inferred.

Two receipt-auditor development assumptions were corrected, with failed-attempt logs retained: the control log reports counts through 51 named arm headings and 57 component tallies, rather than a literal summary sentence or one tally per arm. The initial checkout probe also assumed every dependency was initialized; it now explicitly verifies and reports an empty uninitialized dependency. These were reviewer-script assumptions, not candidate failures. No source was changed to make a check pass.

[R533] PASS Conformance - .gitmodules:13; scripts/act_ci.py:207,235,1662,1736 - Exact assigned tuple, exact five-entry inventory and four public dependency materialization paths match issue 665 comment 6055458854. External remains excluded from fetch.

[R533] PASS RTL - receipts/round14.diff; scripts/act_ci.py:1069,1086,1671,1778,5256 - One commit changes only the manifest, its tests and CI prose. Every other production AST node equals the parent. No RTL, firmware, workflow, interface or gitlink changed; host trust and sandbox sequencing remain intact.

[R533] PASS Robustness - scripts/act_ci.py:10677; receipts/manifest-probes.log - Six candidate refusal cases reach independent config or gitlink discrepancies. Duplicate keys refuse before equality. Both standing trust plants retain the original gitlinks, making the removed config refusal observable. Independent inert probes also refuse wrong path, SSH URL, escape path and update command.

[R533] PASS Tests - scripts/act_ci.py:10584,10677; public author-r14/round14-receipts/runner-final.log and manifest-*.log; receipts/ci-contract-check.log; receipts/ci-contract-controls.log - Independent literal fixture breaks shared-inventory assumptions; materialization checks four explicit paths. Published eight mutation cases fail their named assertions. Independently executed CI contract: 1741 items, 2362 controls.

[R533] PASS Docs - docs/testing/CI_WORKFLOWS.md:1542; docs/reference/SUBMODULES.md:212; receipts/docs-check.log; receipts/doc-style.log - Enumeration states five gitlinks, four public materialized dependencies, HTTPS only and external never fetched. Source execution evidence remains author evidence; manager replay and final current-dev candidate remain separate obligations.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | .gitmodules:13; scripts/act_ci.py:207,235,1662,1736; assignment 6055458854 | R533-14 delta | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| RTL | CLEAN | round14.diff; scripts/act_ci.py:1069,1086,1671,1778,5256 | R533-14 delta | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Robustness | CLEAN | scripts/act_ci.py:10677; manifest-probes.log | R533-14 delta | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Tests | CLEAN | scripts/act_ci.py:10584,10677; public author mutation logs; CI contract receipts | R533-14 delta | fe1cd0679f5028c749af7242c903a82ca2b3d692 |
| Docs | CLEAN | CI_WORKFLOWS.md:1542; SUBMODULES.md:212; docs-check and style receipts | R533-14 delta | fe1cd0679f5028c749af7242c903a82ca2b3d692 |

**Prior public finding disposition**

After the independent pass, the public finding sections and [R533-13](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6052580165) / [R532-13](https://github.com/kebag-logic/milan-fpga/pull/690#issuecomment-6052690604) closures were reconciled. Both prior verdicts are POSITIVE at `154722e14781c7373f3229420b6e007f9bcf9835`. The exact two-file delta preserves every source/test/pin remedy below. Retained resolution carries the prior reviewers' severity and lens assignments; it is not a claim of fresh historical test execution. Original public review links are indexed in `receipts/prior-review-sources.json`.

| Finding IDs | Disposition at this head; preserved evidence/artifact |
| --- | --- |
| R532-12-F1 | RESOLVED retained: the three Failed-kind single-PDU cases at `sw/firmware/ctrl/test/srp_feedback.hpp:87,104,122` and named plants in `srp_mutants.py:802` are byte-identical to round 13. |
| R533-12-R1 | RESOLVED retained: `docs/design/MAILBOX_SPLIT.md:295` still cites the exact lwSRP pin. |
| R532-11-F1 | RESOLVED retained: `srp_mbx.c:159` reads copied state without a library call; `snapshot` at :572 remains outside callbacks. |
| R532-11-F2 | RESOLVED retained: supersession, settled reset and pre-withdrawal-kind cases at `srp_feedback.hpp:239` and their `p11-` plants are unchanged. |
| R533-10-F1; R532-10-F1 | RESOLVED retained: kind-only update at `acmp.c:1132`, `acmp.h:420` and `ctrl_app_srp.c:84`. |
| R533-10-F2 | RESOLVED retained: withdrawal capture at `srp_mbx.c:562` and ordered composition delivery at `ctrl_app_srp.c:78`. |
| R532-10-F2/F3 | RESOLVED retained: replacement/refusal tests and actual feedback-access measurements in `srp_feedback.hpp:298`. |
| R532-9-F1/F2/F3 | RESOLVED retained: deferred registration feedback, permanent-refusal parking and measured bound terms in `ctrl_app_srp.c:39`, `srp_binding.hpp` and `srp_app.cpp`. |
| R533-8-F1 | RESOLVED retained: owned asynchronous binding delivery, retry and supersession in `ctrl_app_srp.c:36` and `srp_binding.hpp`. |
| R532-8-F1 | Source/test defect RESOLVED retained: owned extra-byte fixture at `test_acmp.cpp:208`. Hosted firmware-unit/rtl-fast acceptance remains a manager duty; it is not cleared by this source review. |
| R532-8-F2/F3/F4 | RESOLVED retained: real access measurements in `srp_app.cpp`, correct three-module attribution at `maap/README.md:134`, and scoped plant claims at `ctrl/README.md:143`. |
| R533-1-F1; R532-1-F1 | RESOLVED retained: MSRP immediate IN leave and original LV/#608 deadline in unchanged lwSRP pin, with round-13 adapter/differential evidence. |
| R533-1-F2; R532-2-F1 | RESOLVED retained: level reconciliation, restart and receive fencing at `srp_mbx.c:674`. |
| R533-1-F3; R533-2-F1; R532-2-F3/F4; R532-3-F1/F2 | RESOLVED retained: shared identity, replacement inheritance, final-user VLAN withdrawal and Domain ownership at `srp_mbx.c:324,587`; unchanged shared-binding tests. |
| R532-1-F2 parts 1/2 | RESOLVED retained: unchanged admission-boundary and Ready/ReadyFailed adapter tests. |
| R532-1-F2 part 3; R533-2-F2 | RESOLVED retained: unchanged public dependency pin contains note-4/5 cases and reversals. No upstream suite rerun is claimed. |
| R532-2-F2 | RESOLVED retained: dependency licence, inventory, HTTPS fetch instructions and diagram unchanged; local documentation gate passes. |
| R533-5-F1; R532-5-F1; R532-6-F1 | RESOLVED retained: complete-record recovery and original-arrival timeout at `srp_mbx.c:409,742`; unchanged `srp_rx_retry.cpp` and prior evidence. |
| R533-1-F4; R532-6-F2 | RESOLVED retained: published linked composition/base-delta evidence and image fixtures unchanged. No fresh link or routed measurement claimed. |
| R533-6-F1 | RESOLVED retained: live PR mailbox export recipe retains tracked paths and NVM include paths. No mailbox bank rerun claimed. |
| R532-1-R1/R2; R532-2-R1/R2; R532-3-R1; R532-5-R1/R2; R532-6-R1; R532-7-R1; R532-8-R1/R2; R533-6-R1; R533-7-R1; R533-8-R1 | Wording resolutions retained: tick units, public pin/publication status, retry completion/expiry, composition and checkout wording remain corrected under the round-13 baseline. No new residue. |
| Earlier optional suggestions | Prior addressed/optional dispositions retained without a new obligation. R532-11-S1 remains addressed by CPU-work calibration text at `MAILBOX_SPLIT.md:735`. R532-12-S1 is explicitly retained below. |

R532-12-S1 | SUGGESTION | RTL, Tests | `sw/firmware/ctrl/srp/srp_mbx.c:30,159,572` | Retain optional internal-visit reentry assertion.

Authority/evidence: the unchanged pinned callback contract is cited at :163; current callbacks read copied state and make no library entry. The external-entry guard remains debug-asserted and release-counted. The older public probe showed a future restoration of a callback-time `snapshot()` would evade that guard. Impact: a future source regression could escape enforcement; no such call exists at this head. Optional outcome: hold a debug flag across receive/timer/transmit library calls and assert it is clear before registrar visitation. Verification: restore the forbidden visit in a disposable test copy and require the named assertion. It remains optional and leaves both lenses CLEAN.

**Coverage interpretation, limits and pending manager duties**

The ledger above is reviewer-owned at `fe1cd0679f5028c749af7242c903a82ca2b3d692`. It applies all five lenses to the changed artifacts and carries the round-13 coverage of unchanged artifacts at `154722e14781c7373f3229420b6e007f9bcf9835`. It does not certify a later merge candidate.

- The manager owns hosted acceptance and trusted local replay, including the remaining hosted obligation associated with R532-8-F1. At the exact-head snapshot in `receipts/hosted-snapshot.json`, executed successes were changes, full-ci-gate, lint, all four synthesis shards, behavior conformance, wire accountability and docs-check-no-git. All five simulation shards, firmware-unit, synthesis elaboration, elaborate and docs-check were still running. The physical job was skipped; required aggregates were not all available. Neither unfinished nor skipped work is counted as execution proof.
- No manager source bank ran at this exact head. The old manager compiler-absent comment concerns `c1049de1`; the round-14 assignment's prior candidate-bank success belongs to the earlier head. Neither proves this head or the future candidate.
- At merge turn the manager must resolve the current `dev`, construct the merge candidate, run builder and native banks plus the required candidate gates, and publish their receipts. Source base is `99e4eb6c14462aafa84bb1ac597fd241abc1a240`; assigned live dev is `17f62ef64a66562384e8a93b1d6be6f86e51f95c`. Recheck it at that turn. This source review and the proposed runner adaptation do not replace candidate validation.
- Full parent, processor, gPTP, synthesis and builder banks, firmware campaigns, linked images, live boundary probes, container replay and hardware were not run by this reviewer. No HDL executable was needed or invoked. Licensed standards were not freshly reread in full; this delta changes no protocol interpretation or interface.
- Physical calibration is NOT RUN. Field skips, host checks and linked-image figures supply no hardware, target timing, boot or audio-soak proof. Existing target calibration and integration obligations remain open.
- The isolated clone's lwSRP directory remains uninitialized and empty. Its tree/index pin is exact. The three initialized dependencies have exact tracked bytes/modes/indexes: processor 562 blobs, gPTP 104 and axis 214. No local lwSRP/firmware execution is claimed. The complete superproject is unchanged, including all 1215 tracked blobs and file modes; final status, including ignored paths, is empty.
- The manager must obtain the other independent current-head verdict, close all in-flight review rounds, satisfy the full merge bar, obtain explicit maintainer merge authorization and perform post-merge containment. This review makes no GitHub writes and closes no issue.

Portable reproduction instructions are in `REPRODUCE.md`. Publish only `REPORT.md` and files listed in `MANIFEST.sha256`; `scratch/` is excluded. All foreground commands have completed.

R533-14 FINISHED
