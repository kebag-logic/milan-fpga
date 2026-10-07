[R542] POSITIVE - exact head f800a2bb920c543934d6286a47fe20dde3efa2c5

# R542-3 independent re-review: kebag-logic/lwSRP PR #14 (Closes #13)

- Exact head: `f800a2bb920c543934d6286a47fe20dde3efa2c5`, tree `f950b4f333aeb8b2cb267c7c2040645ff6f8050c`. Both were verified in the reviewer clone before and after all runs, together with the index tree.
- Source base: `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. It is the PR base and the current `main`.
- Public review start: [PR #14 comment 6037581941](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037581941).
- Rules and guides: [CONTRIBUTING.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md), [README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/README.md), [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md), [doc/tools/README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md) and [doc/manager.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/manager.md). The repository has no AGENTS.md.
- Frozen acceptance: [issue #13](https://github.com/kebag-logic/lwSRP/issues/13), items 1-3. The issue has no comments, so no later scope decision exists.
- Interface authority: the [canonical Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt). It returned HTTP 200 with 11358 bytes and sha256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
- Public evidence read:
  - The cited tree [f15a271b review-evidence/lwsrplicfix-r1](https://github.com/kebag-logic/milan-fpga/tree/f15a271b1211a566ff3b163b5a8195280e8bac9e/review-evidence/lwsrplicfix-r1). It holds only `author/PR-BODY.md` and `author/links.log`.
  - The manager validation archives [844b7333 author/validation/](https://github.com/kebag-logic/milan-fpga/tree/844b733300ed292745bb5e8996232cd05bbdcdb5/review-evidence/lwsrplicfix-r1/author/validation) and [7f80fa70 author/validation2/](https://github.com/kebag-logic/milan-fpga/tree/7f80fa7098e747eca97455dc349b3ca87ca2e8e3/review-evidence/lwsrplicfix-r1/author/validation2), on the evidence branch `lwsrplicfix-review-evidence`.
  - Every fetched author file matches its manifest sha256 (`receipts/manager-evidence-check.txt`).
  - Apart from the review-start notices, the manager posted no evidence comments on the issue or the PR (`receipts/prior-public-review.txt`).

## Verdict basis

The licence change is correct and complete for issue #13.
Every documented check I ran at the exact head passes.
The PR body now records the graph render and the scenario dry run. Both results match my own runs and the archived logs, so R542-2/F4 is resolved.
The ctest row now reads "1/1 tests", so R542-2/F5 is resolved.
R542-1/F3 remains an optional SUGGESTION and is carried forward.
No open MINOR, MAJOR or BLOCKER remains, and no RESIDUE is open.

## Executed evidence (all at the exact head)

| # | Check | Result | Receipt |
| --- | --- | --- | --- |
| E1 | Diff and history `a4cbe41..f800a2b` | One commit, one path. `LICENSE` stays mode 100644; its blob goes from `d1e1ed2` to `d645695` with two deletions and no additions. The commit message is a single subject line with no body or trailers ([CONTRIBUTING.md:62](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L62)). | `receipts/diff-raw.txt`, `receipts/diff.patch`, `receipts/history.txt`, `receipts/pr-and-commit-metadata.txt` |
| E2 | `cmp LICENSE <canonical>` | rc 0. The head blob `d645695673349e3947e8e5ae42332d0ac3164cd7` equals the hash of the canonical file. The base file minus its first two lines also equals it, so no other byte changed. No `.gitattributes` exists, so checkout cannot rewrite the bytes. | `receipts/apache-LICENSE-2.0.txt`, `receipts/licence-probes.txt` |
| E3 | GitHub licence API (read-only GET) | The head ref reports `Apache-2.0` for blob `d645695`. The base ref, `main` and the repository report `NOASSERTION`, which reproduces the issue. The repository is public. | `receipts/github-license-api.txt` |
| E4 | SPDX sweep of the first 400 bytes of every tracked file | Base: 60 of 60 files carry the identifier. Head: 59 of 60 do; only `LICENSE` lacks it, and only `LICENSE` changed. | `receipts/licence-probes.txt` |
| E5 | Disposable probes on copies | `cmp` rejects four near-miss variants: SPDX line re-added, CRLF, final newline dropped, and leading blank line dropped. With `LICENSE` removed from an exported copy, `check_links.py --local-only` fails with rc 1 and 4 missing targets. The required licence link is therefore still enforced. | `receipts/licence-probes.txt`, `scripts/licence_probes.sh` |
| E6 | `check_sentences.py` | rc 0; 975 sentences or fragments; 0 over the limit; 0 prose exceptions. The output is byte-identical to the manager `sentences.log`. | `receipts/head/check-sentences.*` |
| E7 | `check_references.py` and `--self-test` | rc 0 for both. There are 0 unlinked references, and the self-test runs 79 cases with 0 failures. Both outputs are byte-identical to the manager logs. | `receipts/head/check-references*.*` |
| E8 | `check_links.py`, anonymous form | rc 0; 354 local links, 20 external URLs, 0 failures. The output is byte-identical to the archived `author/links.log`. | `receipts/head/check-links-anon.*` |
| E9 | `render_mermaid.py --output <scratch>` | rc 0; 27 graphs, 27 render commands, 0 failures. After path normalisation the log is identical to the manager `validation2/render.log`. | `receipts/head/render-mermaid.*`, `receipts/manager-evidence-check.txt` |
| E10 | Default profile (`LWSRP_MILAN=OFF`) | Configure, build, ctest, direct `unit_tests`, `behave` and `behave --dry-run` each return rc 0. ctest reports "100% tests passed out of 1". The runner has 86 tests and 19885 passes. behave passes 1 feature, 3 scenarios and 10 steps. The dry run reports 1 feature, 3 scenarios and 10 steps untested, with no undefined steps. Apart from the timing line it is identical to the manager `validation2/behave-dry.log`. | `receipts/head/profile-OFF.*`, `receipts/manager-evidence-check.txt` |
| E11 | Milan profile (`LWSRP_MILAN=ON`) | The same six steps each return rc 0. ctest passes 1 of 1, and the runner has 86 tests and 19873 passes. behave passes 3 scenarios and 10 steps. | `receipts/head/profile-ON.*` |
| E12 | Isolated codec command from [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#run-the-existing-codec-tests) | Compile rc 0; run rc 0; 1690 passes. | `receipts/head/codec-isolated.*` |
| E13 | `check_embedded.py`, plus `check_freestanding.py` in default and Milan modes | rc 0 for all three. Both profile links and dispatch probes pass. Each freestanding run covers 7 sources with 0 failures. | `receipts/head/check-embedded.*`, `receipts/head/check-freestanding*.*` |
| E14 | `check_reversals.py` in both profiles | rc 0 for both; 93 reversals and 0 failures in each. The restored check passes in each. | `receipts/head/check-reversals-*.*` |
| E15 | Hosted status at the exact head | 0 check runs, 0 statuses and 0 workflow runs; the tree has no workflow files. No hosted job executed and none was skipped. | `receipts/hosted-status.txt` |
| E16 | Live PR body against the archive and my runs | Without the final newline that the API export adds, the live body is byte-identical to the archived `validation2/PR-BODY.md` (sha256 `440d5f83…9a9a`). Each of its ten Validation rows matches E2, E4 and E6-E10. Both repository links are pinned to `f800a2bb…`. | `receipts/pr-body-observed.md`, `receipts/pr-body-compare.txt` |
| E17 | Clone integrity before and after | HEAD, the HEAD tree and the index tree equal the exact head. Tracked bytes and modes are clean, and there are 0 untracked and 0 ignored entries. There are 0 gitlinks, so no submodule pin applies. | `receipts/clone-integrity-before.txt`, `receipts/clone-integrity-final.txt`, `scripts/verify_clone.sh` |

E6-E14 ran concurrently through `scripts/run_checks.sh`, as 13 jobs in one foreground wait group, in 79 s of wall time.
Builds and work directories stayed under unpublished scratch.
The host has no unit framework installed, so the public cgreen 1.6.3 tag was built under scratch.
All counts match the documented values.
Tool versions are in `receipts/environment.txt`; path redaction is described in `receipts/path-redaction.txt`.

## Findings

My independent verdict was recorded in `receipts/independent-pass.md` before I read any prior review. It found no defect at MINOR or above.
I then read the R542-1 ([6037064383](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037064383)), R543-1 ([6037208048](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037208048)) and R542-2 ([6037569246](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037569246)) reports. Every prior finding is dispositioned below.

### R542-1/F1 - MINOR - RESOLVED (confirmed at this head)
- Lenses: Conformance, Tests, Docs.
- Artifact: PR #14 body, `## Validation at f800a2b` table.
- Authority: [CONTRIBUTING.md:59-60](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L59-L60).
- Verification: the sentence, reference, self-test, configure and build, ctest-with-runner and behave rows are still present, and their values match E6, E7 and E10 (see E16).

### R542-1/F2 - RESIDUE - RESOLVED (confirmed at this head)
- Lenses: Docs.
- Artifact: the `LICENSE` and `doc/tools/check_links.py` links in the PR #14 body.
- Verification: both links use `blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/` (E16).

### R542-1/F3 - SUGGESTION - RETAINED (carried forward)
- Lenses: Docs.
- Artifact: [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L17) and [doc/tools/README.md:34-40](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L34-L40). The text predates this change, lies outside the diff, and is unchanged at this head.
- Evidence: the repository is public (E3), but the command list still shows `--github-auth` and the prose describes the private case first. The anonymous form passes (E8).
- Impact: none on this PR. Readers must apply the later instruction to omit authentication after publication.
- Suggested outcome: in a separate issue, make the anonymous command the default example. This PR need not change it.
- Verification: re-read those lines after any follow-up change, and rerun the anonymous link check.
- A suggestion leaves no lens unclean.

### R542-2/F4 - MINOR - RESOLVED: graph render and scenario dry-run results are now recorded
- Lenses: Conformance, Tests, Docs.
- Artifact: PR #14 body rows 19-20 ([live body](https://github.com/kebag-logic/lwSRP/pull/14), archived as [validation2/PR-BODY.md](https://github.com/kebag-logic/milan-fpga/blob/7f80fa7098e747eca97455dc349b3ca87ca2e8e3/review-evidence/lwsrplicfix-r1/author/validation2/PR-BODY.md)). The logs are [validation2/render.log](https://github.com/kebag-logic/milan-fpga/blob/7f80fa7098e747eca97455dc349b3ca87ca2e8e3/review-evidence/lwsrplicfix-r1/author/validation2/render.log) and [validation2/behave-dry.log](https://github.com/kebag-logic/milan-fpga/blob/7f80fa7098e747eca97455dc349b3ca87ca2e8e3/review-evidence/lwsrplicfix-r1/author/validation2/behave-dry.log).
- Authority: [CONTRIBUTING.md:59-60](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L59-L60) requires the pull request to record exit codes for the [test commands](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#run-the-suites) and [documentation checks](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md).
- R542-2's required outcome had three parts:
  - The PR body must give the exit code and result for `render_mermaid.py`: rc 0, 27 graphs, 0 failures.
  - It must do the same for `behave --dry-run`: rc 0, with 1 feature, 3 scenarios and 10 steps untested.
  - Each result needs an archived log.
- Verification:
  - The live body now reads "rc 0; 27 graphs, 0 failures" and "rc 0; 1 feature, 3 scenarios, 10 steps matched (untested in dry-run)".
  - Both logs are archived, and their sha256 values match the evidence manifest.
  - After path normalisation, the render log is identical to my E9 run.
  - Apart from the timing line, the dry-run log is identical to my E10 dry run.
  - The phrase "matched (untested in dry-run)" is accurate. The dry run reports 10 untested steps and none undefined, and [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#run-the-suites) defines the dry run as a step-matching check only.
  - The archived logs carry no explicit return-code line. The rc 0 values rest on the renderer's documented summary semantics and on my reproduction (E9, E10).
- Every part of the required outcome is met, and no new requirement arises.

### R542-2/F5 - RESIDUE - RESOLVED
- Lenses: Docs.
- Artifact: PR #14 body, `ctest --output-on-failure` row.
- Verification: the row now reads "rc 0; 1/1 tests; the unit runner completes 19,885 passes". This matches E10 ("100% tests passed out of 1"; 19885 passes). The exact fix was applied, and no residue remains for the checklist.

### New findings in this round
None.
I considered one possible wording point. Except for the link checker, the Validation table names its tools without links.
I did not raise it, because the link rule in [CONTRIBUTING.md:34-44](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L34-L44) governs repository documentation, not PR bodies.

## Lens notes

- Conformance: issue #13 acceptance 1 is met (E2, E5). Acceptance 2 is met at the head ref (E3); the repository-level value changes only after merge to `main`. Acceptance 3 is met (E4). The contribution evidence rule is now fully met for the documented test commands and documentation checks (E16, F4).
- RTL: the repository has no HDL, and the diff touches only `LICENSE`. The C library still builds and links in both profiles, as do the isolated codec, embedded and freestanding checks (E10-E13). The pinned simulator was not needed and was not used.
- Robustness: byte identity holds at blob level, and no attribute file can rewrite it (E2). Negative controls reject near-miss variants, and the link checker still catches a missing licence (E5). No code, build input or data changed (E1, E4). The clone was left intact (E17).
- Tests: both profiles pass, including executed and dry-run scenarios. Both reversal campaigns and the embedded, freestanding and codec checks also pass at the head (E10-E14). The PR record now carries every result named in the suite list.
- Docs: no document or check needs an SPDX line inside `LICENSE`. [doc/tools/README.md:31](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L31) requires only that the link resolve (E5). All five documentation checks pass (E6-E9). The PR body is accurate and pinned (E16). F3 remains a non-blocking suggestion.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #13 acceptance 1-3; canonical Apache text and blob hash; licence API for base, `main` and head; SPDX sweeps at base and head; CONTRIBUTING.md evidence rule; live PR body and archived validation and validation2 records; F1 and F4 closure | R542-3 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| RTL | CLEAN (no HDL; LICENSE-only diff) | Diff and history; full tracked tree; both profile builds; isolated codec, embedded and freestanding checks | R542-3 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Robustness | CLEAN | LICENSE bytes and blob; absence of attribute files; four negative `cmp` controls; missing-licence link probe; clone integrity before and after, including the index tree and gitlinks | R542-3 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Tests | CLEAN | Both profiles: configure, build, ctest, direct runner, behave and dry run; reversals in both profiles; embedded, freestanding and isolated codec checks; hosted status; manager ctest, behave and dry-run logs; PR table; F4 and F5 closure | R542-3 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Docs | CLEAN (F3 suggestion carried forward) | README.md, CONTRIBUTING.md, doc/*.md and doc/tools/README.md; sentence, reference, self-test, anonymous link and graph checks; manager render log; PR body wording and links; F2, F4 and F5 closure | R542-3 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |

## Real limits

- The unit framework came from a disposable build of the public cgreen 1.6.3 tag, not the manager's prefix. All counts match the documented and archived values.
- The canonical text was fetched once. Its sha256 matches the value recorded by the earlier rounds.
- Repository-level licence detection changes only after `main` changes. It is shown here for the head ref through the same API.
- The manager logs carry no explicit return-code lines. The "rc 0" entries in the body are confirmed by my own runs.
- The cited evidence tree `f15a271b` does not contain the `validation/` or `validation2/` logs. They live at commits `844b7333` and `7f80fa70` on the evidence branch `lwsrplicfix-review-evidence`, not on the evidence repository's default branch. Their hashes match the manifest.
- The brief says the manager's full static, builder and native banks passed at this head. The cited archives hold only the validation logs listed above, so this review does not rely on those banks.
- This repository has no hosted CI (E15). Hosted and act acceptance were not attempted; they are manager duties.
- I did not build the final current-dev candidate (source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, live dev `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`). This review covers the source at the exact head only.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof, and none is relevant to a licence-text change.

## Pending manager duties

1. Publish this report and the receipts listed in `MANIFEST.sha256`.
2. Optionally open a follow-up issue for R542-1/F3.
3. Keep the `lwsrplicfix-review-evidence` commits `844b7333` and `7f80fa70` reachable, or archive them where the published evidence pointer resolves.
4. Build and validate the final current-dev candidate at the merge turn. Update any parent gitlink that pins lwSRP, and own hosted and act acceptance.
5. After merge, confirm that the default-branch licence API and the repository `license.spdx_id` report `Apache-2.0`. Close #13 against that observation.
6. Merge still needs two independent positive reviews and the full completion bar.

R542-3 FINISHED
