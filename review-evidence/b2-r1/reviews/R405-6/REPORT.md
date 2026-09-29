[R405] POSITIVE - exact head 61752396bbebf271fa3da6d872de54e7ae3e7049

# R405-6: composition review of PR #622 (issue #606, with #608 and #75)

- Round R405-6, composition reviewer, cleared context. Review start: PR comment 5889658213.
- Exact head `61752396bbebf271fa3da6d872de54e7ae3e7049`, tree `b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59`. Its parents are live dev `79c36963660c10e4c1c11a744fb5bff41a552b8b` and the PR head `d62b1e1a3a37283ebad039880163873698a011db`.
- `d62b1e1a` is the manager's merge "Merge dev into b2-bench-0929". Its parents are the reviewed source head `5c57927413e0dae279f06a75d2a58e3fec8a2bb0` and dev `79c36963`.
- Scope: composition acceptance only. The source head `5c579274` has two POSITIVE source reviews:
  - [R404-5](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5889607062);
  - [R405-5](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5889625764).

**Verdict: the composed tree adds no defect beyond the reviewed sources.**

- The one textual conflict, in the findings index, is resolved line-exactly. Dev's #451 row is intact, and this PR's three rows are byte-identical to the reviewed head.
- Outside that file, the merge brings in dev's content and nothing else. The candidate differs from dev only in this PR's three Markdown pages.
- No statement in the PR's pages is contradicted or made stale by what #616, #619, #618 and #620 landed.
- Every documentation gate that reads the composed files returns rc 0 on the candidate.
- One optional SUGGESTION is recorded. No MINOR or higher finding is open.

## Authorities, in the order read

1. `AGENTS.md` (sections 3 and 5 to 8) and `CONTRIBUTING.md` step 7, "Validate the candidate merge result". Also the documentation-gate sections (`docs_check.py`, `gen_toc.py`, `check_em_dash.py --base <rev>`, the pinned renderer in `tools/markdown/requirements.txt`).
2. `.github/workflows/docs.yml`, for the gates the hosted docs job runs.
3. Issue #606 body and the public assignment comments (5885087413 bench lane B2, and the round-2 to round-4 assignments). These frame "one findings page per issue" and "no other doc edits".
4. The candidate and source history: `git log`, `git diff 13eda870..5c579274` (the PR), `git diff 13eda870..79c36963` (dev since the lane base), `git diff 5c579274..d62b1e1a` (the merge), and `git diff 79c36963..61752396` (the composition).
5. The dev pages this PR's text leans on: `docs/findings/599_394_E1_LINK_CYCLES.md` and `docs/findings/387_SOFTWARE_GM_STEP.md` (#620, B1), `docs/findings/451_TDM8_FIRST_LIGHT.md` and its index row (#616), and the `docs/testing/TESTING.md` rows (#618, #617). Also the unchanged `75_RECONNECT_RESTART_MEASUREMENT.md` and `docs/reference/SUBMODULES.md`.
6. Public evidence: branch `b2-review-evidence` (tip `76c017d4`, layout only) and the manager's F4 disposition 5886425159. Hosted check runs on `d62b1e1a`.
7. Prior public review findings, read only after the independent pass and the checks below were complete.

## Checks

### C1. Overlap between this PR and its predecessors in the candidate

The candidate is live dev plus this PR. No other queued PR is between them: the first parent of `61752396` is `79c36963`, and `git ls-remote` read dev at `79c36963` at 11:50:24Z (`receipts/ls_remote.txt`). The predecessors are dev's four merges since the lane base `13eda870`: #616, #619, #618 and #620.

- The PR changes 3 paths (`receipts/pr_files.txt`), and dev changes 62 (`receipts/dev_files.txt`).
- Their intersection is exactly one path, `docs/findings/README.md` (`receipts/overlap.txt`).
- Shared registries were checked for semantic interaction:
  - Gitlinks: dev did not move the processor pin (`c951a9ff` at both `13eda870` and `79c36963`), and the candidate's four gitlinks equal dev's.
  - Workflow and record pins: `ci_events.py --check`.
  - Test-evidence inventory: `measure_test_evidence.py --check`.
  - Tables of contents and anchors: `gen_toc.py --check` and `--verify-anchors`.
  - Cited paths: `check_doc_paths.py`.
  - Findings index: C2.
- The PR adds no gate, workflow, script, test or RTL, so no inventory or pin reads anything this PR changed apart from the index and the two new pages.

### C2. The findings-index conflict (manager item 1)

`check_readme_merge.py` (rc 0, `receipts/check_readme_merge.txt`) compares `docs/findings/README.md` at `13eda870`, `79c36963`, `5c579274`, `d62b1e1a` and `61752396` line by line:

- Dev added 1 line (the `451_TDM8_FIRST_LIGHT.md` row) and removed none. The PR added 3 lines and removed 1 (the old #75 row).
- All 4 added lines are present in the merge. The removed #75 row is not resurrected. The merge has 0 lines of its own.
- The merged file equals the ordered expectation: dev's 451 row directly above the rewritten #75 row, followed by `606_FIRST_BIND_MEASUREMENT.md`, then `608_75_WITHDRAWAL_AND_RESTART.md`, then dev's untouched `COMMERCIAL_TIMING_395.md` and `397_SERVICE_BUDGET.md` rows.
- The candidate's file is identical to the merge's.
- `git diff 79c36963 61752396 -- docs/findings/README.md` (`receipts/readme_dev_to_candidate.diff`) shows only this PR's 3 added rows and 1 removed row. That is the same hunk as the source diff (`receipts/readme_pr_source.diff`), shifted by dev's one line.
- The 397 service-budget row is byte-identical at `13eda870`, `79c36963` and the candidate.

### C3. The merge brings in only dev's content (manager items 2 and 4)

`check_merge_scope.py` (rc 0, `receipts/check_merge_scope.txt`):

- Outside the index, `git diff --raw 5c579274 d62b1e1a` covers 61 paths. Their path, mode and blob set equals dev's own `13eda870..79c36963` set exactly (`receipts/merge_vs_source_raw.txt`).
- The two new pages have the same blobs at the reviewed source head and at the candidate: `19dadb8b` for #606 and `c69870c5` for #608/#75.
- `d62b1e1a^{tree}` = `61752396^{tree}` = `b4a1f5ed6a5b00ecde3dcba7781f45fb72480b59`, and the parents are as stated above.
- The candidate differs from dev in exactly three paths: the two pages and the index (`receipts/candidate_vs_dev_raw.txt`, +914 / -1).
- Gitlinks are equal between dev and the candidate.

### C4. Semantic composition with #616, #619, #618 and #620 (manager item 3)

`check_cross_page.py` (rc 0, `receipts/check_cross_page.txt`) reads the candidate's pages.

- **Image identity (13eda870).** These values in the #606 page's identity and hash tables match B1's `599_394_E1_LINK_CYCLES.md:33-44`:
  - VERSION `0x00020060`;
  - ROM `acad92b9`, QSPI `d84bce7b` (`eppo` `bf44ccc9`, `asl` `809fcffa`), AEM `93742dd2`;
  - bitstream `690d87e4…`, payload `6597f7a6…`, AEM `9b077636…`, CSR `7723d0b8…`;
  - the full dev commit.

  The UART grader's SHA-256, `bc41ab03…`, is the same at `13eda870` and at the candidate (dev did not touch it).
- **Saved-state layer.** B2's start and end rows equal B1's final-restore rows in both landed B1 pages (`599…:291-296`, `387…:270-275`):
  - slots 229 / 230, image 230;
  - commits 2 / 0;
  - `PP_STAT` `0x5b000c44`;
  - `PP_NVM_STAT` `0xc34000e4`.

  So `606…:285-289` and `608…:430` ("inherited from lane B1", "reads the same") stay true. The cause they attribute to B1 is "SET_CLOCK_SOURCE writes, whose sticky level only a DUT reset clears". The landed pages state the same at `599…:303-321` and `387…:283-285`.
- **Counters.**
  - B1 ends DUT CRF Stream Output 1 (Output 1 to peer input 8, `599…:69`) at 11 / 10 (`599…:242`), then unbinds at 06:22:05Z (`599…:304`). That gives B2's start census of 11 / 11 (`608…:390`).
  - LINK_UP / LINK_DOWN 12 / 11 (`599…:239`) and GPTP_GM_CHANGED 22 + (9 × 3 + 1) = 50 (`599…:240`, `387…:240`) match `608…:401`.
- **Bench state.**
  - "Outlets read as B1 left them" matches `599…:274`: OUT1 and OUT3 OFF, the other five ON.
  - The peer "in configuration 1 at 48 kHz, as PR #620 found" matches `599…:61`.
  - "More than 1,800 s" since B1's restore holds: the unbind was at 06:22:05Z, and B2's first action sample is 06:53:46Z (`606…:259`).
- **#75 and the B1 link-cycle findings.** `599…:228` says link-cycle restarts exceed one second but "the trigger differs, so this is no #75 verdict", and `394_387_E1_SWITCH_CYCLES.md:15` "does not close #75". The PR grades the reconnect trigger only. There is no contradiction.
- **#617 DIN coherence and the #451 row.** The PR's pages make no statement about TDM, DIN, #451 or #617. #618 changed shipping RTL (`milan_datapath.sv`, `KL_chan_map_capture.sv`, the CRF grid aligner and NCO) after `13eda870`. Both pages and all three index rows scope their measurements to the `13eda870` image (606:4, :40; 608:4, :63; index rows "on dev `13eda870`"), so they claim nothing about the post-#618 tree.
- **9e9954e9 references.** These comparison figures come from the #75 page, which dev did not change:
  - median 0.019175 s and maximum 0.117736 s;
  - Listener Ready 6.888605 s;
  - first PDU 6.889398 s;
  - LeaveAll 6.080 s;
  - 3 of 100 non-stop holds.
- **Cited authorities untouched or anchor-stable.**
  - `117_GPTP_SILICON_EVIDENCE.md`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md`, `SAVED_STATE_FASTCONNECT.md`, `SUBMODULES.md` and `75_RECONNECT_RESTART_MEASUREMENT.md` are unchanged by dev.
  - `TESTING.md` changed only in two table rows (capture_coherence and media_nco). Section 6b, which both pages cite for retention, is unchanged.
  - `SUBMODULES.md:73`, "Issues #606 and #608 adopt processor pin `c951a9ff`", still agrees with the pages.

### C5. Gates on the candidate

Every gate was run in the foreground from this clone at `61752396` (`receipts/gates.txt`). The environment was a scratch venv with `--require-hashes` from `tools/markdown/requirements.txt` (cmarkgfm 2025.10.22, html5lib 1.1, Python 3.14.7), plus pyyaml 6.0.3, which the hosted job also installs unpinned. All rc 0:

| Gate | Result |
|---|---|
| `docs_check.py` | 0 findings, 179 md + 949 scrubbed files |
| `gen_toc.py --check` | 121 pages OK |
| `gen_toc.py --verify-anchors` | 270 cross-page fragment links reproduced |
| `gen_toc.py --selftest` | 1501/1501 arms |
| `check_em_dash.py --base 79c36963` (the candidate's dev parent) | 0 findings over 914 added lines in 3 pages |
| `check_em_dash.py --base 13eda870` (lane base) | 0 findings over 2548 added lines in 35 pages |
| `check_em_dash.py --selftest` | 339 arms |
| `check_doc_style.py`, `--selftest` | OK |
| `check_doc_paths.py` | 860 cited paths resolve |
| `check_gptp_docs.py`, `check_solution_docs.py`, `check_submodule_docs.py` | OK (4 exact gitlinks) |
| `check_feature_status.py --self-test` | 0 findings |
| `check_baremetal_only.py --check`, `--selftest` | 0 findings over 947 files; 700 arms |
| `ci_scope.py --selftest` | PASS |
| `ci_events.py --check`, `--selftest` | 1655 contract items; 2206 arms |
| `measure_test_evidence.py --check` | ratchet PASS |
| `git diff --check 79c36963 61752396` | clean |

The first `check_baremetal_only.py --check` returned rc 2 because pyyaml was not yet installed ("pyyaml is unavailable"). That was an environment refusal, not a finding. After installing pyyaml it returned rc 0. Both runs are in the receipt.

### C6. The gates can see the composed files

`probes.sh` (`receipts/probes.txt`) plants three defects in a disposable clone at the candidate (`scratch/`, unpublished), one at a time, and restores the bytes after each:

| Planted defect | Caught by |
|---|---|
| Broken index link, `606_FIRST_BIND_MEASUREMEN.md` | `docs_check.py` rc 1 |
| Broken cross-page anchor, `608` page to `606…#saved-state-layers` | `gen_toc.py --verify-anchors` rc 1 (269 of 270 reproduced) |
| Unresolved conflict markers around the 451 row | `git diff --check` rc 2, "leftover conflict marker" |

- Each of the three composition failure classes is detected by a gate that passes on the candidate.
- `check_doc_paths.py` does not check Markdown link targets, so it is not the gate for the first arm.
- The probe clone ended with 0 dirty paths and tree `b4a1f5ed`.

### C7. Hosted state (manager-owned; recorded, not relied on)

The check runs on `d62b1e1a` were read at 11:56:08Z (`receipts/hosted_checks_d62b1e1a.tsv`):

- **Success:** `rtl-fast`, `elaborate`, `full-ci-gate`, `bdd-conformance`, `changes`, `docs-check-no-git` and `wire-accountability`.
- **In progress:** `docs-check`.
- **Skipped, not executed:** `verilator-suites`, `verilator-lint`, `yosys-portability`, `yosys-elaboration`, the shard matrices and physical gPTP. This matches a Markdown-only change.

The candidate `61752396` itself is not on GitHub; the API answers 422 for it. Its tree equals the tree a hosted pull-request merge of `d62b1e1a` into dev `79c36963` produces.

### C8. Clone integrity after the review

At the end of the review this clone matched the exact head (`receipts/clone_integrity.txt`):

- HEAD is `61752396` and the tree is `b4a1f5ed`. The index `write-tree` is `b4a1f5ed`.
- `status --porcelain` is empty, `diff-index --cached` is empty and `git diff --quiet HEAD` returns rc 0.
- The required submodules are checked out at their gitlinks: `gptp-processor` `5dce647a`, `protocol-processor` `c951a9ff` and `third_party/verilog-axis` `48ff7a7e`. `external` is not initialised, as found.
- No edits were made in this clone. All probes ran in the scratch clone.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### S1 SUGGESTION (Docs): the B1 cross-references can now point in-tree

- **Where:** `docs/findings/606_FIRST_BIND_MEASUREMENT.md:287-289` and `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md:430`.
- **Evidence:** both lines cite [PR #620](https://github.com/kebag-logic/milan-fpga/pull/620) for B1's final saved-state reading, and 606:289 says "That page attributes the pending bit to SET_CLOCK_SOURCE writes". With #620 landed, the same reading and cause are in-tree at `599_394_E1_LINK_CYCLES.md#saved-state-layer` (`:287-321`) and `387_SOFTWARE_GM_STEP.md#restore`.
- **Impact:** none on correctness. The PR link resolves, and its statements match the landed pages (C4). An in-tree anchor would be checked by `gen_toc.py --verify-anchors` and would name the page that "That page" means.
- **Outcome (optional):** a later docs change may add the in-tree anchor beside the PR link.
- **Verification:** `gen_toc.py --verify-anchors` and `docs_check.py` rc 0.

## Prior public findings at this head

These were read after the checks above.

- The two pages are byte-identical to `5c579274`, where R404-5 and R405-5 recorded every finding resolved.
- The PR's index rows are byte-identical to the rows reviewed there.
- The live PR body, read at the review, carries the F7 wording R404-5 and R405-5 accepted ("210 state-changing ACMP commands (105 `CONNECT_RX`, 105 `DISCONNECT_RX`), all to the peer's input"), and it has no closing keyword (`receipts/pr622_body.md`).

| Finding | State at `61752396` |
|---|---|
| R404-1 and R405-1 F1 MINOR (Conformance, Docs): #608 reading shown as undecided | Resolved. The #608 page is blob `c69870c5`, as reviewed. |
| R404-1 and R405-1 F2 MINOR (Conformance, Docs): restore omits the saved-state layer | Resolved. The tables are unchanged, and they agree with the landed B1 pages (C4). |
| R404-1 and R405-1 F3 MINOR (Conformance, Docs): cycle-22 attribution | Resolved. The page is unchanged. |
| R404-1 and R405-1 F4 MINOR (Conformance, Docs): controller identity in the archive | Resolved by the redacted evidence branch (disposition 5886425159). The composition adds no archive content. |
| R404-2 and R405-2 F5 MINOR: stream-input poll count | Resolved. `606…:267-269` is unchanged. |
| R404-3 and R405-3 F6 MINOR: command-census premise | Resolved. `606…:277-279` is unchanged. |
| R404-4 and R405-4 F7 MINOR: PR-body census clause | Resolved. The clause in the live body is as accepted. |

No prior finding is retained.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | The composition touches this scope only through dev content the pages cite. Checked: C4 identity, saved-state, counter, binding, bench-state and #75-scope cross-checks against `599_394_E1_LINK_CYCLES.md`, `387_SOFTWARE_GM_STEP.md`, `394_387_E1_SWITCH_CYCLES.md:15`, `SUBMODULES.md:73` and `75_RECONNECT_RESTART_MEASUREMENT.md`; issue #606 assignment scope; `receipts/check_cross_page.txt`. The PR's measurement claims themselves were covered by R404-5 and R405-5 at `5c579274`, and the blobs are identical. | R405-6 (composition); source: R404-5, R405-5 | `61752396` (source `5c579274`) |
| RTL | CLEAN | The composition does not touch this scope. The candidate differs from dev only in 3 Markdown paths, with gitlinks equal (`receipts/check_merge_scope.txt`, `candidate_vs_dev_raw.txt`). The #618 RTL after `13eda870` is dev's own reviewed content, and the pages scope all claims to the `13eda870` image (C4). Source coverage: R404-5, R405-5. | R405-6 (applied: scope check); source: R404-5, R405-5 | `61752396` |
| Robustness | CLEAN | Merge-resolution integrity: row order, no resurrected or lost line, no conflict residue, candidate tree = merge tree (`check_readme_merge.py`, `check_merge_scope.py`, `git diff --check`). The three planted composition defects are each caught (`receipts/probes.txt`). | R405-6 | `61752396` |
| Tests | CLEAN | The PR adds no test. Checked: `measure_test_evidence.py --check` and `ci_events.py --check`/`--selftest` on the candidate; gate sensitivity shown by C6 probes; the gate self-tests (`gen_toc` 1501 arms, `check_em_dash` 339, `check_baremetal_only` 700) pass. | R405-6 | `61752396` |
| Docs | CLEAN (S1 optional) | `docs/findings/README.md` resolution (C2); all C5 docs gates rc 0 on the candidate; 270 cross-page anchors, 860 cited paths; no stale or contradicted statement (C4). | R405-6 | `61752396` |

## Limits

- This is a composition review. The measurement content was not re-derived from raw captures; R404-5 and R405-5 cover it at `5c579274`, and the blobs are identical.
- No hardware and no bench were used. Physical calibration was NOT RUN. Hosted skipped contexts are not hardware or simulation proof.
- The full parent, processor, gPTP, Yosys and builder banks, Docker and act were not run, as this round's rules require. No such bank reads the three Markdown paths the composition adds.
- The manager's static, builder and native bank results at this head were not found as a public comment when read. This verdict does not rely on them.
- Hosted `docs-check` on `d62b1e1a` was still in progress at 11:56:08Z.
- pyyaml in the scratch venv is unpinned, as in the hosted job.

## Pending manager duties

- Confirm live dev is still `79c36963` at the merge turn. If it has moved, rebuild the current-dev candidate and re-run the composition gates.
- Accept hosted `docs-check` on the exact PR head, and the act replica, which the manager owns.
- Obtain explicit maintainer authorization to merge. After the merge, run `check_merge_containment.py` as CONTRIBUTING step 7 requires.
- The PR says "Relates to" #606, #608 and #75, so no issue closes on merge. #608 item 3 stays qualified until the processor PR #133 pin adoption and a re-run.

R405-6 FINISHED
