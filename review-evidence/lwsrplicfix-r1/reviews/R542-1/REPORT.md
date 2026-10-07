[R542] NEGATIVE - exact head f800a2bb920c543934d6286a47fe20dde3efa2c5

# R542-1 independent review: kebag-logic/lwSRP PR #14 (Closes #13)

- Exact head: `f800a2bb920c543934d6286a47fe20dde3efa2c5`, tree `f950b4f333aeb8b2cb267c7c2040645ff6f8050c` (verified in the reviewer clone).
- Source base: `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, which is `refs/heads/main`, the PR base.
- Scope reconstructed from [CONTRIBUTING.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md), [README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/README.md), [doc/tools/README.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md), [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md) and [doc/manager.md](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/manager.md); there is no AGENTS.md in this repository.
- Requirement authorities: [issue #13](https://github.com/kebag-logic/lwSRP/issues/13) acceptance 1-3 (the issue has no comments, so no later scope decision), and the earlier [licence issue #8](https://github.com/kebag-logic/lwSRP/issues/8) acceptance 2 (SPDX on every tracked source, header, build, test and documentation file).
- Interface authority: the canonical text at https://www.apache.org/licenses/LICENSE-2.0.txt, fetched 2026-10-07T11:29Z (HTTP 200, `last-modified: Sun, 28 Dec 2025 17:09:26 GMT`, sha256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`).
- Public evidence read: [review-evidence/lwsrplicfix-r1 @ f15a271b](https://github.com/kebag-logic/milan-fpga/tree/f15a271b1211a566ff3b163b5a8195280e8bac9e/review-evidence/lwsrplicfix-r1). It holds `MANIFEST.json`, `author/PR-BODY.md` (sha256 `3d2c35ed…80f9`, matching the live PR body) and `author/links.log` (sha256 `b9bfa147…eb67`). The issue has no manager evidence comments. The PR has only the two review-start comments. No public receipt of the manager's source/static/builder/native banks was found at this head; see Limits.

## Verdict basis

The change is correct and complete for issue #13 acceptance 1 and 3, and acceptance 2 is shown at the head ref.
Every executed check passes. Results are listed below.
The verdict is NEGATIVE only because of F1, an open MINOR: the PR does not record the exit codes required by the contribution rules.
F1 needs a PR-body update and no source change, so a re-review can stay at this exact head.

## Executed evidence (all at exact head)

| # | Check | Result | Receipt |
| --- | --- | --- | --- |
| E1 | `git diff --stat/--raw a4cbe41..f800a2b` | One file: `LICENSE` 100644→100644, blob `d1e1ed2`→`d645695`, 2 deletions, 0 additions | `receipts/diff-stat.txt`, `receipts/diff-raw.txt`, `receipts/diff.patch` |
| E2 | `git ls-tree -r` base vs head, excluding LICENSE | identical (rc 0): every other path, mode and blob is unchanged; 60 tracked files (59×100644, 1×100755 `build.sh`), 0 gitlinks | `receipts/grep-spdx-license.txt`, `receipts/clone-integrity.txt` |
| E3 | `cmp LICENSE <canonical>` (worktree and `git show HEAD:LICENSE`) | rc 0 both; sha256 equal (`cfc7749b…3d30`); ASCII, LF, no CR, ends with one newline | `receipts/apache-LICENSE-2.0.txt`, `receipts/apache-fetch-headers.txt`, `receipts/license-structure.txt` |
| E4 | Base `LICENSE` == `"SPDX-License-Identifier: Apache-2.0\n\n"` + head `LICENSE` | `cmp` rc 0: the commit removes exactly the two lines and nothing else | `receipts/license-structure.txt` |
| E5 | SPDX sweep of every tracked blob at base and head (`spdx_sweep.sh`) | Head: 58 files carry `Apache-2.0` on line 1 and `build.sh` on line 2 (after the shebang). Only `LICENSE` has none. The only base-to-head difference is the `LICENSE` row. | `receipts/spdx-sweep-a4cbe41.tsv`, `receipts/spdx-sweep-f800a2b.tsv` |
| E6 | GitHub licence API (read-only GET) per ref | `ref=f800a2b…` and `ref=licence-canonical`: `Apache-2.0` (`apache-2.0`, sha `d645695`). `ref=main` and the repository: `NOASSERTION`, which reproduces the issue. Repository visibility is `public`. | `receipts/github-license-api.txt` |
| E7 | Search for SPDX/LICENSE requirements in checks, build and docs | No check, build rule, test or document requires an SPDX line in `LICENSE`. [CONTRIBUTING.md:41](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L41) covers Markdown pages only. [doc/tools/README.md:31](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L31) requires the licence link to resolve, not its content. `check_references.py` treats `SPDX` and `LICENSE` only as reference words. | `receipts/grep-spdx-license.txt` |
| E8 | Probes on exported copies (`licence_probes.sh`) | control: links 354/20/0, sentences 975/0, references 0, rc 0 each. `oldlic` (head plus base LICENSE, which equals the base tree): identical counts, rc 0, so no check reads or requires the SPDX line. `nolic`: `check_links.py --local-only` rc 1 with 4 `missing target` failures (CONTRIBUTING.md:4, README.md:63, doc/manager.md:89, doc/tools/README.md:31), so the required link is enforced. | `receipts/licence-probes.txt` |
| E9 | `check_sentences.py` | rc 0; 975 sentences/fragments; 0 over limit; 0 prose exceptions | `receipts/head/check-sentences.*` |
| E10 | `check_references.py`, `--self-test` | rc 0; 0 unlinked references. Self-test: 79 cases, 0 failures | `receipts/head/check-references*.*` |
| E11 | `check_links.py` (anonymous, the post-publication form) and `--github-auth` | rc 0 both; 354 local links, 20 external URLs, 0 failures. This matches the PR body and `author/links.log`. | `receipts/head/check-links-*.*` |
| E12 | `render_mermaid.py` | rc 0; 27 graphs; 0 failures | `receipts/head/render-mermaid.*` |
| E13 | Default profile (`LWSRP_MILAN=OFF`): configure, build, `ctest`, `unit_tests`, `behave`, `behave --dry-run` | rc 0. ctest 1/1 passed. 86 tests, 19885 passes. behave: 1 feature, 3 scenarios, 10 steps passed. These match README.md and doc/tester.md. | `receipts/head/profile-off.*` |
| E14 | Milan profile (`LWSRP_MILAN=ON`): same sequence | rc 0. ctest 1/1 passed. 86 tests, 19873 passes. behave: 3 scenarios, 10 steps passed. These match doc/tester.md. | `receipts/head/profile-on.*` |
| E15 | `tests/check_embedded.py`, `tests/check_freestanding.py` (default and `-DLWSRP_MILAN=1`) | rc 0 all; both profiles link and dispatch; 7 freestanding sources, 0 failures each | `receipts/head/check-embedded.*`, `receipts/head/check-freestanding*.*` |
| E16 | Hosted status at exact head | 0 check runs, 0 commit statuses. The repository tracks no workflow files, so no hosted job executed and none was skipped. | `receipts/hosted-status.txt` |
| E17 | Clone integrity after all runs | HEAD, tree and index tree match the exact head. Worktree and index are clean. No untracked or ignored files. All 60 blob hashes and modes match. 0 gitlinks. Re-checked after the probes and the prior-findings read. | `receipts/clone-integrity.txt`, `receipts/clone-integrity-final.txt` |

The E9-E15 jobs ran concurrently through `run_checks.sh` and `wait_checks.sh`. Builds and work directories were outside the checkout. Tool versions are in `receipts/environment.txt`. The unit framework is not installed on the host, so a disposable copy of its 1.6.3 tag was built under scratch. Published logs replace the local packet and clone paths with `<packet>` and `<clone>`.

## Findings

### F1 - MINOR - PR record omits required exit codes
- Lenses: Tests, Docs, Conformance.
- Location: PR #14 body, `## Validation` table (identical to `author/PR-BODY.md`, sha256 `3d2c35ed…80f9`).
- Authority: [CONTRIBUTING.md:59-60](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L59-L60) says to run the [test commands](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tester.md#run-the-suites) and the [documentation checks](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md), and to "Record exit codes and failures in the pull request". [Issue #8](https://github.com/kebag-logic/lwSRP/issues/8) acceptance 4 also asks that build, `ctest` and `behave` still pass after licence changes.
- Evidence: the PR body records only `cmp` and `check_links.py`. It gives no exit code for `check_sentences.py`, `check_references.py`, `--self-test`, the build, `ctest`, `unit_tests` or `behave`. No other public record at this head supplies them: the evidence tree holds only `links.log`, and the PR has no manager evidence comment.
- Impact: the contribution rule's evidence record is incomplete. This is not wording-only: fixing it adds executed results (exit codes and counts) to the PR record. The underlying checks pass (E9-E15), so code and licence correctness are not affected.
- Required outcome: the PR body, or a linked public evidence record at this exact head, records exit codes and failure counts. It must cover `check_sentences.py`, `check_references.py` (and `--self-test`), the build, `ctest`, the unit runner and `behave`.
- Verification: re-read the PR body or linked record at `f800a2bb920c543934d6286a47fe20dde3efa2c5`. Values must be consistent with E9-E14: all rc 0; 975/0 sentences; 0 unlinked; 79/0 self-test; ctest 1/1; 86 tests and 19885 passes (OFF); 3 scenarios and 10 steps.

### F2 - RESIDUE - PR body links use the moving branch name
- Lenses: Docs.
- Location: PR #14 body, the `LICENSE` link and the `doc/tools/check_links.py` link, both `…/blob/licence-canonical/…`.
- Evidence: the links resolve today. They will break if the branch is deleted after merge, and they are not pinned to the reviewed head.
- Exact fix: replace `blob/licence-canonical/` with `blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/` in both links. This is wording only and changes no figure, verdict or claim.

### F3 - SUGGESTION - stale private-repository wording (pre-existing, outside this diff)
- Lenses: Docs.
- Location: [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L17) and [doc/tools/README.md:34-40](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/doc/tools/README.md#L34-L40).
- Evidence: the repository is public (E6). The page still lists `--github-auth` as the command and describes the private case first. Anonymous `check_links.py` passes (E11).
- Suggestion: in a separate issue, make the anonymous command the default. This PR need not change it.

No other defect was found. The commit subject is one line with no body or trailers, which conforms to [CONTRIBUTING.md:62](https://github.com/kebag-logic/lwSRP/blob/f800a2bb920c543934d6286a47fe20dde3efa2c5/CONTRIBUTING.md#L62). The PR body's factual claims (byte-identical, `cmp` 0, every other file keeps SPDX, 354/20/0 links) are all reproduced (E3, E5, E11).

## Lens notes

- Conformance: #13 acceptance 1 is met (E3, E4). Acceptance 2 is met at the head ref (E6); the repository-level value changes only once `main` holds this blob, which is a manager duty after merge. Acceptance 3 is met (E5). #8 acceptance 2 lists source, header, build, test and documentation files, not the licence text, and #13 is the later scoped decision, so there is no conflict. The contribution evidence rule is unmet (F1).
- RTL: not applicable. The repository is a C library with no RTL, and the diff touches only `LICENSE` (E1, E2).
- Robustness: no code, build input or data changed (E2). The probes show that no check depends on `LICENSE` content, and that its absence is still caught (E8). The file has no CR or BOM and ends with a newline (E3).
- Tests: both profiles' build, ctest, unit runner and behave pass with the documented counts (E13, E14). Embedded and freestanding checks pass (E15). The PR record omits these results (F1).
- Docs: no document claims `LICENSE` carries SPDX (E7). All doc checks pass (E9-E12). Wording residue F2; suggestion F3.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F1) | issue #13 acceptance 1-3; issue #8 acceptance; CONTRIBUTING.md; canonical Apache-2.0 text; GitHub licence API per ref; PR body; E1-E8 | R542-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| RTL | CLEAN (not applicable: no RTL in repository, LICENSE-only diff) | diff stat/raw; full tracked tree listing | R542-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Robustness | CLEAN | LICENSE bytes and structure; base vs head tree; oldlic/nolic probes; clone integrity | R542-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Tests | UNCLEAN (F1) | OFF and ON build/ctest/unit_tests/behave/dry-run; check_embedded; check_freestanding ×2; hosted status; PR validation table | R542-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |
| Docs | UNCLEAN (F1); F2 residue, F3 suggestion | README.md, CONTRIBUTING.md, doc/*.md, doc/tools/README.md; check_sentences, check_references (+self-test), check_links (anonymous and authenticated), render_mermaid; PR body | R542-1 | f800a2bb920c543934d6286a47fe20dde3efa2c5 |

## Prior public review findings

These were read after this verdict and ledger were written, at 2026-10-07T11:34:45Z (`receipts/prior-public-review.txt`).
PR #14 has 0 submitted reviews and 0 review comments.
Its only issue comments are the two review-start notices (R542-1 and R543-1), which contain no findings.
Issue #13 has no comments.
No prior public finding exists, so none needs to be resolved or retained.

## Real limits

- `tests/check_reversals.py` (the reversal or mutation campaigns, both profiles) was not run. The diff changes no code or test input, so these regressions are unchanged from base.
- The unit framework came from a disposable build (cgreen 1.6.3 tag), not the manager's pinned prefix. The counts match the documented ones exactly.
- The canonical text was fetched once, through a CDN cache. Its sha256 matches the widely published value for that file.
- Repository-level GitHub detection (acceptance 2 at repository scope) can only be observed after `main` changes. Here it is shown for the head ref through the same detection API.
- The brief states that the manager's full source static/builder and native banks passed at this head. No public receipt of those banks was found in the cited evidence tree or on the issue or PR, so this review does not rely on them.
- No hosted CI exists for this repository (E16). No act or hosted acceptance was attempted, which is the manager's duty.
- Physical calibration was NOT RUN. No hardware was used, and field skips are not hardware proof. Neither is relevant to a licence-text change.
- The final current-dev candidate (source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`, live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`) was not built. This review validates the source at the exact head only.

## Pending manager duties

1. Resolve F1 by recording the required exit codes on the PR, or in linked public evidence, at this head. Then request re-review at the same head.
2. Carry F2 to the residue checklist with the exact fix above.
3. Optionally open a follow-up issue for F3.
4. After merge, confirm that `GET repos/kebag-logic/lwSRP/license` and the repository `license.spdx_id` report `Apache-2.0` on `main`, and close #13 against that observation.
5. Build and validate the final current-dev candidate at the merge turn. Update any parent gitlink that pins lwSRP. Own hosted/act acceptance.
6. Merge still needs two independent positive reviews.

R542-1 FINISHED
