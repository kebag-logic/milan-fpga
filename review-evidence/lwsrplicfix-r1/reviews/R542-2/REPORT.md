[R542] NEGATIVE - exact head f800a2bb920c543934d6286a47fe20dde3efa2c5

# R542-2 independent re-review: kebag-logic/lwSRP PR #14 (Closes #13)

- Exact head: `f800a2bb920c543934d6286a47fe20dde3efa2c5`, tree `f950b4f333aeb8b2cb267c7c2040645ff6f8050c`. Both were verified in the reviewer clone before and after all runs.
- Source base: `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, which is the PR base (`main`).
- Public review start: [PR #14 comment 6037211599](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037211599).
- Rules and guides: [CONTRIBUTING.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md), [README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/README.md), [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md), [doc/tools/README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md) and [doc/manager.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/manager.md). The repository has no AGENTS.md.
- Frozen acceptance: [issue #13](https://github.com/kebag-logic/lwSRP/issues/13) items 1-3. The issue has no comments, so there is no later scope decision.
- Interface authority: the [canonical Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0.txt). It returned HTTP 200 with 11358 bytes and sha256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
- Public evidence read: [review-evidence/lwsrplicfix-r1 @ f15a271b](https://github.com/kebag-logic/milan-fpga/tree/f15a271b1211a566ff3b163b5a8195280e8bac9e/review-evidence/lwsrplicfix-r1) and the manager validation archive [844b7333 author/validation/](https://github.com/kebag-logic/milan-fpga/tree/844b733300ed292745bb5e8996232cd05bbdcdb5/review-evidence/lwsrplicfix-r1/author/validation). Every archived file matches its manifest sha256 (`receipts/manager-evidence-check.txt`).

## Verdict basis

The licence change is correct and complete for issue #13.
Every check I ran at the head passes.
The PR body figures match my runs and the manager logs.
R542-1/F1 and R542-1/F2 are resolved.
The verdict is NEGATIVE because of one new open MINOR, R542-2/F4.
The PR record still omits two results that the contribution rule requires: the graph render and the scenario dry run.
F4 needs only a PR-body and evidence update, so a re-review can stay at this exact head.

## Executed evidence (all at the exact head)

| # | Check | Result | Receipt |
| --- | --- | --- | --- |
| E1 | Diff and history `a4cbe41..f800a2b` | One commit; one file. `LICENSE` stays 100644; its blob goes from `d1e1ed2` to `d645695`, with two deletions. The commit message is a single subject line with no body or trailers ([CONTRIBUTING.md:62](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L62)). | `receipts/diff-raw.txt`, `receipts/diff.patch`, `receipts/commit-metadata.txt` |
| E2 | `cmp LICENSE <canonical>` | rc 0. The head blob `d645695673349e3947e8e5ae42332d0ac3164cd7` equals the hash of the canonical file. No `.gitattributes` exists, so checkout cannot rewrite the bytes. The base file differs at byte 1. | `receipts/apache-LICENSE-2.0.txt`, `receipts/apache-fetch-headers.txt`, `receipts/licence-probes.txt` |
| E3 | GitHub licence API (read-only GET) | `ref=f800a2b…`: `Apache-2.0` (`apache-2.0`, blob `d645695`). `ref=a4cbe41…`, the default branch and the repository: `NOASSERTION`, which reproduces the issue. The repository is public. | `receipts/github-license-api.txt` |
| E4 | SPDX sweep of the first five lines of every tracked file, base vs head | 60 files. At head, only `LICENSE` has no SPDX line. The only difference between the sweeps is the `LICENSE` row. | `receipts/spdx-sweep-a4cbe41.tsv`, `receipts/spdx-sweep-f800a2b.tsv` |
| E5 | Search for `LICENSE` and SPDX dependencies in docs, tools, build and tests | Nothing requires an SPDX line inside `LICENSE`. [doc/tools/README.md:31](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L31) requires only that the link resolves. | this report; `receipts/licence-probes.txt` |
| E6 | Disposable probes on an exported copy (`licence_probes.sh`) | `cmp` accepts the head file. It rejects five variants: base, SPDX line added, no final newline, CRLF, and a filled appendix. A link-check control gives 354/20/0, rc 0. With `LICENSE` removed, the local link check gives rc 1 with 4 failures, so the required link is enforced. | `receipts/licence-probes.txt` |
| E7 | `check_sentences.py` | rc 0; 975 sentences/fragments; 0 over limit; 0 prose exceptions. The output matches the manager's `sentences.log` byte for byte. | `receipts/head/check-sentences.*` |
| E8 | `check_references.py` and `--self-test` | rc 0 both. 0 unlinked references; the self-test runs 79 cases with 0 failures. Both outputs are byte-identical to the manager logs. | `receipts/head/check-references*.*` |
| E9 | `check_links.py`, anonymous (the post-publication form) | rc 0; 354 local links, 20 external URLs, 0 failures. The output is byte-identical to the archived `author/links.log`. | `receipts/head/check-links-anon.*` |
| E10 | `render_mermaid.py` | rc 0; 27 graphs; 0 failures. | `receipts/head/render-mermaid.*` |
| E11 | Default profile (`LWSRP_MILAN=OFF`) | configure, build, ctest, direct `unit_tests`, `behave` and `behave --dry-run` each return rc 0. ctest passes 1 of 1 tests. The runner has 86 tests and 19885 passes. behave passes 1 feature, 3 scenarios and 10 steps; the dry run leaves 3 scenarios and 10 steps untested. | `receipts/head/profile-off.*` |
| E12 | Milan profile (`LWSRP_MILAN=ON`) | The same six steps each return rc 0. ctest passes 1 of 1; the runner has 86 tests and 19873 passes; behave passes 3 scenarios and 10 steps. | `receipts/head/profile-on.*` |
| E13 | `check_embedded.py`; `check_freestanding.py` in default and Milan modes | rc 0 for all three. Both profile links and dispatch probes pass. Each freestanding run covers 7 sources with 0 failures. | `receipts/head/check-embedded.*`, `receipts/head/check-freestanding*.*` |
| E14 | `check_reversals.py` in both profiles | rc 0 both; 93 reversals and 0 failures in each. | `receipts/head/check-reversals-*.*` |
| E15 | Hosted status at the exact head | 0 check runs, 0 statuses and 0 workflow runs; the tree has no `.github`. No hosted job executed and none was skipped. | `receipts/hosted-status.txt` |
| E16 | PR body against the manager archive and my runs | The live body is byte-identical to the archived `author/validation/PR-BODY.md`; export adds only a trailing newline. Every figure matches E2, E4 and E7-E11. Both repository links are pinned to `f800a2bb…`. | `receipts/pr-body-observed.md`, `receipts/pr-body-compare.txt`, `receipts/manager-evidence-check.txt` |
| E17 | Clone integrity before and after | HEAD, tree and index tree match the exact head; there are no status entries, including ignored files. All 60 tracked blobs and modes match, and there are 0 gitlinks. | `receipts/clone-integrity-before.txt`, `receipts/clone-integrity-final.txt` |

E7-E14 ran concurrently through `run_checks.sh` and `wait_checks.sh`, with builds and work directories under unpublished scratch.
The unit framework is not installed on the host, so its public 1.7.0 tag was built under scratch.
Tool versions are in `receipts/environment.txt`.
Published logs replace local paths with `<packet>` and `<clone>`; see `receipts/path-redaction.txt`.

## Findings

### R542-1/F1 - MINOR - RESOLVED
- Lenses: Conformance, Tests, Docs.
- Artifact: PR #14 body, `## Validation at f800a2b` table.
- Authority: [CONTRIBUTING.md:59-60](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L59-L60).
- Required outcome (R542-1): record exit codes and counts for the sentence and reference checks, the self-test, the build, ctest, the unit runner and behave.
- Verification: the body now has rows for all of them. They read 975/0, 0 unlinked, 79/0, configure and build rc 0, ctest 1/1 with 19,885 unit passes, and 3 scenarios with 10 steps. These values match E7, E8 and E11 and the manager logs (E16). The unit runner's result is part of the ctest row, and the ctest log shows that runner's output. The outcome R542-1 required is met.

### R542-1/F2 - RESIDUE - RESOLVED
- Lenses: Docs.
- Artifact: the `LICENSE` and `doc/tools/check_links.py` links in the PR #14 body.
- Verification: both links now use `blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/`, which was the required fix (E16).

### R542-1/F3 - SUGGESTION - RETAINED (carried forward)
- Lenses: Docs.
- Artifact: [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L17) and [doc/tools/README.md:34-40](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L34-L40). This text predates the change and lies outside the diff.
- Evidence: the repository is public (E3). The command list still shows `--github-auth`, and the prose describes the private case first. The anonymous form passes (E9).
- Suggestion: in a separate issue, make the anonymous command the default example. This PR need not change it.

### R542-2/F4 - MINOR - OPEN: PR record omits the graph render and scenario dry-run results
- Lenses: Conformance, Tests, Docs.
- Artifact: PR #14 body validation table (sha256 `619a025e…2c83`, identical to the archived `author/validation/PR-BODY.md`), and the manager archive [844b7333 author/validation/](https://github.com/kebag-logic/milan-fpga/tree/844b733300ed292745bb5e8996232cd05bbdcdb5/review-evidence/lwsrplicfix-r1/author/validation).
- Authority: [CONTRIBUTING.md:59-60](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L59-L60) says to run the [test commands](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#run-the-suites) and [documentation checks](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md), and to record their exit codes in the pull request.
  - [doc/tools/README.md:13-19](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L13-L19) lists five documentation checks, including `render_mermaid.py`.
  - [doc/tester.md:205](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#L205) says "Include every graph render result".
  - [doc/tester.md:203-204](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#L203-L204) asks for missing dependencies to be reported separately.
  - [doc/tester.md:17-24](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#L17-L24) lists `behave --dry-run` among the six suite commands.
- Evidence:
  - The body records four of the five documentation checks; the graph renderer is absent.
  - It records five of the six suite commands, counting the direct unit runner as covered by the ctest row. `behave --dry-run` is absent.
  - The manager archive has no render log and no dry-run log (`receipts/manager-evidence-check.txt`), so no public record at this head supplies them.
- Scope note: R542-1/F1 listed the checks it required more narrowly than the rule it cited. R542-1 ran both commands itself (its E12 and E13) but did not list them in F1's required outcome. This round applies the same rule in full; it does not add a new requirement. R543-1 closed its ledger on F1's narrower list; I disagree only on these two items.
- Impact: the contribution rule's evidence record is still incomplete. This is not wording-only, because fixing it adds executed results to the PR record. Licence and code correctness are unaffected: both commands pass at this head (E10, E11).
- Required outcome: at this exact head, the PR body or a linked public evidence record must give the exit code and result for two commands:
  - `python3 doc/tools/render_mermaid.py --output <dir>`: expected rc 0, 27 graphs, 0 failures. If the renderer's dependencies are unavailable, report that explicitly instead.
  - `behave --dry-run`: expected rc 0, with 1 feature, 3 scenarios and 10 steps untested.
  - Each needs an archived log.
- Verification: re-read the PR body or linked record at `f800a2bb920c543934d6286a47fe20dde3efa2c5`. Its values must match E10 and E11.

### R542-2/F5 - RESIDUE - OPEN (wording only)
- Lenses: Docs.
- Artifact: PR #14 body, `ctest --output-on-failure` row: "rc 0; 1/1 targets; …".
- Evidence: ctest counts tests, not targets. Both the manager log and E11 report "100% tests passed out of 1" for test `#1: unit`.
- Exact fix: replace "1/1 targets" with "1/1 tests". No figure, claim or verdict changes.

No other defect was found.
The body's other claims are reproduced: two lines dropped, `cmp` returns 0, every other file keeps its SPDX header, and 354/20/0 links (E1, E2, E4, E9).

## Lens notes

- Conformance: issue #13 acceptance 1 is met (E2, E6). Acceptance 2 is met at the head ref (E3); the repository-level value changes only after merge. Acceptance 3 is met (E4). The contribution evidence rule is not fully met (F4).
- RTL: there is no HDL in this repository, and the diff touches only `LICENSE`. The C library still builds and links in both profiles, including the embedded and freestanding checks (E11-E13).
- Robustness: byte identity is checked at blob level, and no attribute file can rewrite it (E2). Negative controls reject near-miss variants, and the link checker still catches a missing licence (E6). No code, build input or data changed (E1, E4).
- Tests: both profiles, both reversal campaigns, and the embedded and freestanding checks pass at the head (E11-E14). The PR record lacks the dry-run result (F4).
- Docs: no document depends on the removed line (E5). All documentation checks pass (E7-E10). The PR record lacks the graph render result (F4). F5 is residue and F3 a suggestion.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F4) | Issue #13 acceptance 1-3; canonical Apache text; licence API per ref; SPDX sweeps; CONTRIBUTING.md; PR body; manager archive; R542-1/F1 closure | R542-2 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| RTL | CLEAN (no HDL; LICENSE-only diff) | Diff and history; full tracked tree; both profile builds; embedded and freestanding checks | R542-2 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Robustness | CLEAN | LICENSE blob and bytes; attribute files; five negative `cmp` controls; missing-licence link probe; clone integrity before and after | R542-2 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Tests | UNCLEAN (F4) | Both profiles: configure, build, ctest, direct runner, behave and dry run; reversals in both profiles; embedded and freestanding checks; hosted status; manager ctest and behave logs; PR table | R542-2 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Docs | UNCLEAN (F4); F5 residue; F3 suggestion | README.md, CONTRIBUTING.md, doc/*.md, doc/tools/README.md; sentence, reference, self-test, anonymous link and graph checks; PR body; R542-1/F2 closure | R542-2 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |

## Prior public review findings

My verdict and ledger were written to `receipts/independent-pass.md` before I read any prior review report.
I then read the R542-1 report ([PR comment 6037064383](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037064383), archived blob `af15835f`) and the R543-1 report ([PR comment 6037208048](https://github.com/kebag-logic/lwSRP/pull/14#issuecomment-6037208048)).
- R542-1/F1 (MINOR): resolved. R542-1/F2 (RESIDUE): resolved. R542-1/F3 (SUGGESTION): retained and carried forward.
- R543-1 raised no findings of its own beyond the R542-1 dispositions.
- PR #14 has no submitted reviews and no inline comments, and issue #13 has no comments (`receipts/prior-public-review.txt`).

## Real limits

- The unit framework came from a disposable build of its public 1.7.0 tag, not the manager's prefix. All counts match the documented values.
- The canonical text was fetched once, through a CDN. Its sha256 matches the value recorded by both earlier rounds.
- Repository-level licence detection can be observed only after `main` changes. Here it is shown for the head ref through the same API.
- The manager logs carry no explicit return-code lines. The "rc 0" entries in the body are confirmed by my own runs, not by the logs.
- The archived `links.log` is from the earlier packet (`f15a271b`) and has no head marker. It is byte-identical to my anonymous run at this head.
- The brief says the manager's full static, builder and native banks passed at this head. The cited archives hold only the listed validation logs, so this review does not rely on those banks.
- No hosted CI exists for this repository (E15). Hosted and act acceptance were not attempted; they are manager duties.
- The final current-dev candidate (source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`) was not built. This review covers the source at the exact head only.
- Physical calibration was NOT RUN, and no hardware was used. Field skips are not hardware proof, and none is relevant to a licence-text change.

## Pending manager duties

1. Resolve F4: add the graph render and scenario dry-run results at this head, with archived logs. Then request re-review at the same head.
2. Carry F5 to the residue checklist with the exact fix above.
3. Optionally open a follow-up issue for F3.
4. After merge, confirm that the default-branch licence API and the repository `license.spdx_id` report `Apache-2.0`, and close #13 against that observation.
5. Build and validate the final current-dev candidate at the merge turn, update any parent gitlink that pins lwSRP, and own hosted and act acceptance.
6. Merge still needs two independent positive reviews and the full completion bar.

R542-2 FINISHED
