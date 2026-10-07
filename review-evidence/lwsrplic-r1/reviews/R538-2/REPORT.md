[R538] POSITIVE - exact head 4eba61b7b1c49fc9b7260a487240ca86f9d38168

# R538-2 independent review: kebag-logic/lwSRP PR #9 (closes #8), Apache-2.0 licensing after the history rewrite

- Exact head `4eba61b7b1c49fc9b7260a487240ca86f9d38168`, tree `bf90243127da3e4d22eaeef1402542f1095ee263`. Both were verified in the isolated detached clone, which was clean before and after every check (`receipts/clone_integrity.txt`).
- PR commits: `bc6687a` (licence, on `92647aa`), `e59b21f` (merge of `main` `1401654`), and `4eba61b` (documentation anchor shift). Each has a one-line message by the owner's company account (`receipts/head_history.txt`, `receipts/pr_commit_message_lines.txt`).
- Inputs, in order:
  - `CONTRIBUTING.md`. The repository has no `AGENTS.md`.
  - `README.md` and `doc/`.
  - Issue #8 body (acceptance 1-4). Issue #8 has no comments.
  - Issue #1 body and comments (owner's release rules, including rule 7: no tool or model names).
  - PR #9 body and comments.
  - `git diff 1401654..4eba61b7`, the full history of all six branches on a fresh clone, and a fresh mirror including GitHub pull refs.
  - The public evidence packet `review-evidence/lwsrplic-r1` at milan-fpga `9d6a0632`.
- I did not read private author material, lane scratch areas, management storage or other checkouts. In particular, I did not use the existing unit-framework builds under the lane scratch areas. The unit framework was built from its upstream release `1.7.0` (commit `feeb85ed`) in this packet's scratch area.

## Process disclosure

- While enumerating PR #9's public comments to find manager evidence, I printed every comment body before my own pass.
- That output included the R538-1 report and the first 6000 characters of the R539-1 report.
- The focus list for this round already named their findings (R538-1-F1, R539-1-01 and R539-1-02).
- My checks were scripted from issue #8's acceptance and this round's focus list. Every result below comes from my own executed receipts.
- The resolution table in "Prior public findings" uses that evidence.

## Verdict summary

- **History rewrite (focus item 1).** All six branches on a fresh clone contain no tool or model name and no trace of the removed root guidance file. The scan covered 35 commits, 184 trees and 209 blobs, with 0 hits.
- **Trees and authorship (focus item 2).** All 33 rewritten commits keep their author, committer, both dates, message and mapped parents. Each tree either equals its pre-rewrite tree (9 commits) or differs only by:
  - deleting the removed root file;
  - dropping exactly one matching line from `doc/architecture.md` (24 commits).

  The head tree equals the reviewed `1a1d6cbe` tree. The merge tree equals the `375dbe13` tree.
- **Anchors (focus item 3).** All 69 documentation line anchors select the same source text at the head as at the documentation's base.
  - 68 anchors moved by one line; the unchanged one targets an unchanged file.
  - The three named anchors are correct: Leave interval at `mrp.h` line 119, LA at `mrp_mad.c` lines 162-163, and the stream address at `msrp.c` lines 353-354.
  - The link checker passes on all 290 local links.
- **Licence checks (focus item 4).**
  - `LICENSE` is byte-identical to the canonical Apache-2.0 text.
  - `NOTICE` names kebag-logic.
  - All 43 other tracked files carry exactly one Apache-2.0 SPDX line in their own comment syntax.
  - There is no third-party code.
  - Build, `ctest` (9 tests, 1690 assertions) and `behave` (3 scenarios, 10 steps) pass.
- Compiled objects are byte-identical between base and head, so the header change does not affect behaviour.

There is no open MINOR, MAJOR or BLOCKER. Three wording items are RESIDUE, and two items are SUGGESTION.
The pre-rewrite objects are still reachable through GitHub pull refs, and issue #1's body names the removed file. Both are manager duties, listed below; they are not findings.

## Findings

### R538-2-R1 - RESIDUE - Docs - PR #9 body ("What changes" and "Validation" sections)

- **Defect:** the body still says "The licence commit was made on `19f5796`". After the rewrite, that commit is `92647aa`, and `19f5796` is reachable only through pre-rewrite pull refs. The body also does not mention the third commit `4eba61b`, and its validation heading says "at the merge commit".
- **Evidence:** `receipts/commit_map.txt` (`19f5796b6365` maps to `92647aaf38e4`), `receipts/head_history.txt`.
- **Why RESIDUE:** wording only. Every figure in the validation table reproduces at the head:
  - build rc 0;
  - `ctest` rc 0, 1690 passes;
  - `behave` 3 scenarios, 10 steps;
  - 290 local links;
  - 7 anonymous external failures: 6 own private URLs and the ISO 403.

  The SHA is in a code span, so GitHub does not turn it into a link.
- **Exact fix:**
  - Replace the bullet "The licence commit was made on `19f5796`. The second commit merges `main`, which brings in the test-harness fix ([#3](https://github.com/kebag-logic/lwSRP/pull/3)) and the documentation ([#5](https://github.com/kebag-logic/lwSRP/pull/5))." with:

    "The licence commit `bc6687a` was made on `92647aa`. The second commit, `e59b21f`, merges `main`, which brings in the test-harness fix ([#3](https://github.com/kebag-logic/lwSRP/pull/3)) and the documentation ([#5](https://github.com/kebag-logic/lwSRP/pull/5)). The third commit, `4eba61b`, moves 68 documentation source-line anchors down one line, past the added licence headers."
  - Rename "## Validation at the merge commit" to "## Validation at the head commit `4eba61b`".
- **Verification:** read the edited body. No re-run is needed, because the figures were reproduced at the head (`receipts/head/`, `receipts/doc/`).

### R538-2-R2 - RESIDUE - Docs - `doc/tools/README.md:31` (retains R538-1-R1)

- **Defect:** "The required [licence](../../LICENSE) and [notice](../../NOTICE) links fail until the separate licence change is present." is stale at this head, because both files are present and their links resolve (`receipts/doc/links_auth.log`).
- **Why RESIDUE:** wording only. The checker behaviour it describes is real: probe P4 removes `NOTICE`, and the notice links fail (`receipts/probes/p4_links.log`).
- **Exact fix:** "The [licence](../../LICENSE) and [notice](../../NOTICE) links are required and must resolve."
- **Verification:** `python3 doc/tools/check_sentences.py`, `python3 doc/tools/check_references.py` and `python3 doc/tools/check_links.py` all return 0 on local links.

### R538-2-R3 - RESIDUE - Docs - `doc/manager.md:85-87` (retains R538-1-R2)

- **Defect:** "requires the separate licence work and documentation before publication. Licence files are supplied by that separate change. Verify their presence in the combined release tree." describes the time before this PR.
- **Why RESIDUE:** wording only.
- **Exact fix:** replace lines 85-87 with two lines:
  - "The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) required the licence and documentation before publication."
  - "The [licence issue](https://github.com/kebag-logic/lwSRP/issues/8) added both files."
- **Verification:** the same three documentation checks return 0.

### R538-2-S1 - SUGGESTION - Docs, Tests - `doc/tools/check_links.py` (line-range checks)

- **Observation:** the link checker validates only that an anchor's line range is in bounds. Probe P1 moves the Leave-interval anchor back to the Join line (`#L118`). `check_links.py` still reports no local failure, while `scripts/anchor_check.py` reports BAD (`receipts/probes/probes.txt`, `receipts/probes/p1_anchor.log`).
- **Impact:** a later header or code insertion can silently move anchors again. This PR's anchors are correct, so nothing is open.
- **Suggested outcome:** in a later change, check anchor content, for example by comparing the selected text with a base revision as `scripts/anchor_check.py` does.

### R538-2-S2 - SUGGESTION - Tests - public evidence `review-evidence/lwsrplic-r1/author/*.log` (retains R538-1-S1)

- **Observation:** the published logs record no commit, and they predate the rewrite. No file in the packet names `4eba61b7`, `1a1d6cbe`, `375dbe13` or `e59b21f` (`receipts/public_evidence_r1_check.txt`; all seven hashes match the packet manifest).
- **Impact:** none on this verdict. My own runs at the exact head reproduce every figure.
- **Suggested outcome:** future evidence logs should start with the exact commit and tree. The manager's exact-head bank receipts should be published (see manager duties).

## Prior public findings at this head

| Prior finding | Status at `4eba61b7` | Evidence |
| --- | --- | --- |
| R538-1-F1 (MAJOR): tool name in reachable history | RESOLVED for every branch. | Fresh clone of all six branches: 0 hits, with no hits on any branch alone (`receipts/history_scan_branches.txt`, `receipts/history_scan_per_ref.txt`). Neither cited blob, `21654351` or `396d6fe8`, is in the fresh clone (`receipts/prior_blob_presence.txt`). Remaining GitHub pull-ref reachability is a manager duty. |
| R539-1-01 (MAJOR): historical disclosure | RESOLVED for the branch history, on the same evidence. | As above. Pull refs `refs/pull/3/head`, `refs/pull/5/head` and `refs/pull/12/merge` still reach the pre-rewrite objects (9, 9 and 29 hits). This round's assignment hands that to the manager. |
| R539-1-02 (MINOR): shifted source anchors | RESOLVED. | 69 anchors: 68 moved and 1 unchanged, all selecting identical text, with 0 bad (`receipts/anchor_check.txt`). The three named targets were read directly. The link checker passes on all 290 local links. |
| R538-1-R1 (RESIDUE): `doc/tools/README.md:31` | RETAINED as R538-2-R2. | Line unchanged at the head. |
| R538-1-R2 (RESIDUE): `doc/manager.md:85-87` | RETAINED as R538-2-R3. | Lines unchanged at the head. |
| R538-1-S1 (SUGGESTION): logs lack commit identity | RETAINED as R538-2-S2. | Packet unchanged at `9d6a0632`. |

PR #9 has no review objects and no review comments (0 and 0).

## Evidence by lens

### Conformance (issue #8 acceptance and release hygiene)

1. **`LICENSE` and `NOTICE`.**
   - `LICENSE` matches the canonical text byte for byte: sha256 `cfc7749b…3d30`, 11358 bytes, blob `d6456956` (`receipts/license_notice.txt`).
   - `NOTICE` reads "lwSRP / Copyright 2026 kebag-logic / Licensed under the Apache License, Version 2.0."
   - The merge carries the same `LICENSE` and `NOTICE` blobs as the licence commit (`receipts/merge_delta.txt`).
2. **SPDX headers.** All 43 non-licence files carry exactly one `SPDX-License-Identifier: Apache-2.0` line (`receipts/spdx_first_lines.tsv`).
   - It is on line 1 in each file's own syntax: `#`, `/* */` or `<!-- -->`.
   - In `build.sh` it is on line 2, after the shebang.
   - 16 files already had it at the base. The merge adds it to the other 27 and changes nothing else (`receipts/merge_delta.txt`).
3. **No third-party code or other licence.**
   - No copyright, licence, derivation or attribution text exists outside `LICENSE`, `NOTICE` and the SPDX lines.
   - The register queue (`src/core/switch_ctrl.c:23`, `src/include/shish_lan/switch_ctrl.h:93`) cites a published lock-free queue algorithm by name.
   - Its code is an original C11-atomics implementation, with its own names, structure and a simplified single-consumer dequeue. It is not a copy of a reference listing.
   - **Commit authorship.** Every reachable commit is by the owner: the personal account (1, the root commit) or the company account (34, including 2 merges committed by the hosting service) (`receipts/identities_all_branches.txt`).
4. **Build and documentation links.**
   - Build, `ctest` and `behave` pass (see Tests).
   - The LICENSE and NOTICE links resolve: 290 of 290 local links pass (`receipts/doc/links_auth.log`).
5. **History hygiene (owner's option (b)).**
   - Branch history is clean (see the prior-findings table).
   - Commit map: 33 rewritten commits, plus 2 root-side commits whose hashes did not change (`d50ca4f`, `1c41344`), with 0 problems (`receipts/commit_map.txt`).
   - `4eba61b7` has the same tree as `1a1d6cbe`.
   - The `375dbe13`→`1a1d6cbe` diff is byte-identical to the `e59b21f`→`4eba61b7` diff.
   - `1a1d6cbe` = `375dbe13` + anchor fix (`receipts/robustness.txt`).
6. **Clause and evidence links.** The 68 moved anchors keep their clause comparisons pointed at the same code (see Docs).

### RTL

- Not applicable. All 45 tracked files and every commit in the PR are C, Python, CMake, Kconfig, YAML, shell and Markdown.
- There is no HDL, no RTL interface and no generated hardware artifact.
- The pinned HDL simulator was not needed and was not run.

### Robustness

- **Behaviour-neutral headers.** The ten library and binding sources were compiled with `-O2 -g0` and path-neutral file names at the base and the head. The two sets of objects are byte-identical (`receipts/head/objs.sha256`, `receipts/base/objs.sha256`).
- **Executable mode.** `build.sh` keeps mode `100755`, its shebang is still line 1, and `bash -n` passes.
- **Parsers.**
  - `zephyr/module.yml` parses.
  - Every Python file parses.
  - `Kconfig.zephyr` is unchanged.
  - The feature file's comment header is accepted by `behave`.
- **Diff hygiene.** `git diff --check 1401654..4eba61b7` is clean (`receipts/robustness.txt`).
- **Probes.** Fault probes ran on disposable clones (`receipts/probes/probes.txt`):
  - P2: a missing SPDX line is detected.
  - P3: a one-byte `LICENSE` change is detected, and the mutation was confirmed applied.
  - P4: a missing `NOTICE` fails the link check.
  - P5: the history scanner finds a term in both a nested blob and a commit message (positive control).

### Tests

- Head and base were each exported with `git archive` and built and run separately (`receipts/head/rc.txt`, `receipts/base/rc.txt`).
- Both pass every step: configure, build with `cmake --build --parallel 16`, `ctest`, the direct unit run, `behave` and `behave --dry-run`.
- At the head:
  - the build log has no warnings under `-Wall -Wextra -Wpedantic`;
  - `ctest`: 1 of 1 passed;
  - the direct run of `mrp_pdu_suite` gives 9 tests and 1690 passes;
  - `behave` passes 1 feature, 3 scenarios and 10 steps.
- The PR body and `README.md` figures match these results.
- **Hosted evidence.** The exact head has 0 check runs and 0 commit statuses (`receipts/hosted_check_runs.json`, `receipts/hosted_status.json`). There are no executed hosted jobs, and no skipped context is claimed as coverage.

### Docs

- **Anchor equivalence.** `scripts/anchor_check.py` pairs each anchor at the head with its base counterpart (`receipts/anchor_check.txt`).
- **Directly read targets.**
  - `mrp.h:119` is `MRP_LEAVE_TIME_CS 60u`.
  - `mrp_mad.c:162-163` is the LA comment and its `TX_MSG_LEAVE → LO` row.
  - `msrp.c:353-354` is the group-address comment and its initializer.
  - `mrp_pdu.c:155-156` is the LeaveAll callback.
  - `mrp_mad.c:836-842` is `rx_on_leaveall`.
  - `switch_steps.py:27-37` is the two state assertions.
  - `msrp.h:79-90` is the declaration and withdrawal prototypes.
- **Documentation checks** (`receipts/doc/rc.txt`):
  - Sentences: 760, 0 over 25 words, rc 0.
  - Unlinked references: 0, rc 0.
  - Reference self-test: 79 cases, 0 failures, rc 0.
  - Graphs: 22 rendered, 0 failures, rc 0.
  - Links with repository authentication: 290 local, 18 external, 1 failure (the ISO site's HTTP 403 to automated clients), rc 1.
  - Anonymous links: 7 failures, the 6 own private-repository URLs plus ISO, rc 1. This matches the PR body.
- **Licence text.** The `README.md` licence section matches the owner-agreed text exactly. `CONTRIBUTING.md` states contribution under Apache-2.0.
- **Rewritten line.** The `doc/architecture.md` line removed by the rewrite was a fenced directory-tree entry. Its removal leaves every historical version well formed, and the head page is unaffected.
- Open items are wording only: R538-2-R1 to R3.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #8 acceptance 1-4; canonical licence comparison; `NOTICE`; 43 SPDX headers; merge delta; third-party scan including the queue's algorithm citation; authorship of all 35 commits; history scan of six branches; 33-commit rewrite map; clause-evidence anchors. Prior F1, R539-1-01 and R539-1-02 resolved. | R538-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| RTL | CLEAN (not applicable) | All 45 tracked files and all three PR commits; no HDL, RTL interface or hardware artifact. | R538-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Robustness | CLEAN | Byte-identical objects at base and head; executable mode and shebang; YAML, Python, shell and Kconfig parsing; `diff --check`; probes P2-P5; clone integrity after all runs. | R538-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Tests | CLEAN | Exported head and base trees: configure, build, `ctest`, direct unit run (9 tests, 1690 assertions), `behave` (3 scenarios, 10 steps), dry run; hosted check census (none). Suggestion S2 open, non-blocking. | R538-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |
| Docs | CLEAN | 69-anchor equivalence; named targets read; sentence, reference, self-test, graph and link checks (authenticated and anonymous); PR body; README licence text; probe P1. RESIDUE R1-R3 and suggestion S1 open, non-blocking. | R538-2 | 4eba61b7b1c49fc9b7260a487240ca86f9d38168 |

## Real limits

- The repository is still private. Six of its own URLs fail anonymous checks and pass with authentication. Anonymous public access can only be confirmed after publication.
- The ISO page answers HTTP 403 to automated clients, so it was not verified automatically.
- The exact head has no hosted CI, and there are no hosted results to inspect. Hosted and container acceptance belong to the manager.
- The unit framework is the upstream `1.7.0` release built here. The author's version is not recorded, but the assertion counts are identical.
- The history scan uses a private list of 26 case-insensitive patterns, so the published receipts carry no names.
  - Hits are reported redacted as `[TERM<n>]`.
  - On the six branches the only matches were two GitHub-generated committer addresses. Those are generic, so their pattern was dropped and the final branch scan reports 0.
  - The issue and PR text scan's 5 hits in the R538-1 comment are generic words ("assistant-guidance", "regenerated with"), not product names.
- The graph renderer checks syntax only. This PR changes no graph.
- Physical calibration was NOT RUN. Hardware was not used, and field skips are not hardware proof.
- The manager's static/builder and native bank receipts at this head are not in the cited public packet (S2). This verdict relies on my own runs.
- The final current-dev candidate (source base `1401654530ce7d9275de9b901e67df47e5bbc536`, live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`) was not reviewed here.

## Pending manager duties

1. **Pull refs.** Before the repository goes public, make sure no GitHub ref reaches the pre-rewrite objects (`receipts/history_scan_per_ref.txt`):
   - `refs/pull/3/head` (`e4f9995b`, closed PR #3): 9 hits.
   - `refs/pull/5/head` (`cd659eb5`, closed PR #5): 9 hits.
   - `refs/pull/12/merge` (`c474054f`): 29 hits. This is the hosting service's test merge for **open** PR #12, still built on the pre-rewrite `main` `02700d9e`. It is not a closed-PR ref, and it should refresh once PR #12's mergeability is recomputed.

   Verify on a fresh `--mirror` clone with `TERMS_FILE=<private list> scripts/history_scan.py <mirror>`; expect `hits=0`. `refs/pull/9/merge` (`e5604ff4`, parents `1401654` and `4eba61b7`, tree `bf902431`) is already clean.
2. **Issue #1 body.** Line 21 of the body names the removed root file, which is a tool name (`receipts/github_text_scan.txt`). Issue text becomes public with the repository. Edit it before publication, then re-run `scripts/github_text_scan.py`.
3. **Residue checklist.** Carry RESIDUE R538-2-R1 (PR body), R2 (`doc/tools/README.md:31`) and R3 (`doc/manager.md:85-87`) to the residue checklist with the exact fixes above.
4. **Exact-head receipts.** Publish the exact-head bank receipts, and build the final current-dev candidate at the merge turn.
5. **After publication.** Re-run `python3 doc/tools/check_links.py` without authentication. The six own-URL failures should clear.
6. **Merge gate.** Merge still requires two independent positive reviews and the full completion bar.

## Reproduction

The scripts are in `scripts/`; raw receipts are in `receipts/`, listed in `MANIFEST.sha256`.

- `scripts/history_scan.py` and `scripts/github_text_scan.py` take a private term file through `TERMS_FILE`.
- `scripts/commit_map.py <mirror> <branch-clone>` maps the rewritten commits.
- `scripts/anchor_check.py <repo> 1401654530ce7d9275de9b901e67df47e5bbc536 4eba61b7b1c49fc9b7260a487240ca86f9d38168` checks the anchors.
- `CGREEN_PREFIX=<prefix> scripts/validate.sh <repo> <rev> <workdir> <logdir>` builds and tests one exported tree.
- `scripts/probes.sh` runs the fault probes.

Host paths in logs are redacted to `$SCRATCH`, `$CLONE` and `$HOME`.

R538-2 FINISHED
