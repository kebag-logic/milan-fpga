[R538] NEGATIVE - exact head 375dbe132c6f1498f2f3e714ce5905d34456c9d5

# R538-1 independent review: kebag-logic/lwSRP PR #9 (closes #8), Apache-2.0 licensing

- Exact head `375dbe132c6f1498f2f3e714ce5905d34456c9d5`, tree `942f26fe59d72990af8ddc5ac6937921b5e401ec` (verified in the isolated detached clone).
- Parents: `fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b` (licence commit on `19f5796`) and `02700d9ead0a29dd5d53c1d85e163ea392b79ab0` (main: PR #3 and PR #5).
- Inputs, in order: CONTRIBUTING.md (the repository has no AGENTS.md), README.md and doc/; issue #8 body (acceptance 1-4); issue #1 (owner's release scope, including "Remove [the root assistant-guidance file] from the public tree" and "no tool or model names"); PR #9 body; the diffs `02700d9e..375dbe13` and `fed1a0d..375dbe13`; full history; the public evidence packet `review-evidence/lwsrplic-r1` at milan-fpga `9d6a0632`.
- At this head, issue #8 and PR #9 had no manager evidence comments and no prior review findings. Their only comments were the two review-start notices, and PR #9 had 0 reviews and 0 review comments. There is no prior finding to resolve or retain.

## Verdict summary

The licence change itself is correct and complete at this head:
- LICENSE is byte-identical to the canonical Apache-2.0 text.
- NOTICE suits section 4(d).
- All 43 non-licence files carry the right SPDX header in their own comment syntax.
- The merge exactly reproduces both sides.
- The build, ctest (1690 assertions), behave (3 scenarios, 10 steps) and the documentation checks pass.

The verdict is NEGATIVE for one reason: the release-gate hygiene criterion covers the whole history, and it fails. Five reachable commits, including this PR's own commit `fed1a0d`, contain a root assistant-guidance file and a documentation line that name a code-assistant product. The public record has no owner decision accepting this history (F1). Two stale wording items are recorded as RESIDUE.

## Findings

### F1 - MAJOR - Conformance, Docs - tool name in published history

- **Artifact:** the history reachable from this head. Blob `21654351bd62a20125f6c9209b55bdf9a8ce7f57` is a root Markdown file named after a code-assistant product; its line 1 names that product and line 3 names it with its URL. Blob `396d6fe887b6fb807a1939e14eb6f144b95c6e9c` is `doc/architecture.md`; its line 36 lists that file as "AI assistant guidelines and coding style".
- **Where:** both blobs are in the trees of `f8db42a`, `19f5796`, `fed1a0d` (this PR's licence commit), `e4f9995` and `d96d9d4`. Commit `8962e2f` (main) removes both. Neither is in the tree at `375dbe13`.
- **Authority:** the review scope requires public-release hygiene "across the whole tree and history", with no tool or model names. Issue #1 rule 7 says "no tool or model names". Issue #1 scoped the removal of this file to "the public tree" only. Neither issue #1 nor #8 records an owner decision about history.
- **Evidence:** `receipts/history_scan.txt` (lines 9, 67, 68, 75; names redacted to `[TOOL]`), produced by `scripts/history_scan.sh`. Commit membership was checked with `git cat-file -e <commit>:<path>` for every commit.
- **Impact:** the repository goes public after this PR merges, and publication cannot be undone. All history becomes public with it, including the tool-named file. Merging also adds one more commit (`fed1a0d`) whose tree carries that file. The tree at this head is clean.
- **Required outcome:** before publication, either:
  - (a) the owner records a public decision that the existing history may keep these two blobs; or
  - (b) the history is rewritten to drop them, then reviewed again at the new exact head. This changes every commit hash from `f8db42a`, including main.

  This PR cannot fix F1 with a tree change alone.
- **Verification:**
  - For (a), cite the decision link.
  - For (b), at the rewritten head, `EXTRA_TERMS=<private term list> scripts/history_scan.sh <clone>` must report no tool-name match, and the tree checks below must still pass.

### R1 - RESIDUE - Docs - `doc/tools/README.md:31`

- **Defect:** the sentence "The required [licence](../../LICENSE) and [notice](../../NOTICE) links fail until the separate licence change is present." is stale at this head, because both files are present and resolve (`receipts/validate_logs/doc_links_local.log`).
- **Why RESIDUE:** wording only. The checker behaviour it describes is real, as probes `no_license_links` and `no_notice_links` show.
- **Exact fix:** replace it with "The [licence](../../LICENSE) and [notice](../../NOTICE) links are required and must resolve."

### R2 - RESIDUE - Docs - `doc/manager.md:85-87`

- **Defect:** "requires the separate licence work … Licence files are supplied by that separate change. Verify their presence in the combined release tree." is written for the time before this PR merged.
- **Why RESIDUE:** wording only.
- **Exact fix:** replace lines 85-87 with two lines:
  - "The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) required the licence and documentation before publication."
  - "The [licence issue](https://github.com/kebag-logic/lwSRP/issues/8) added both files."

### S1 - SUGGESTION - Tests - evidence packet `review-evidence/lwsrplic-r1/author/*.log`

- The ctest, behave and links logs do not record the commit they ran on. PART-A describes the `fed1a0d` checkpoint, where behave failed (rc 1).
- My own runs at the exact head reproduce the PR body's figures, so this changes no result.
- Future packets should record the commit hash (`git rev-parse HEAD`) in each log.

## Lens results and evidence

### Conformance (issue #8 acceptance, Apache-2.0)

- **Acceptance 1 (LICENSE and NOTICE):**
  - LICENSE (blob `d6456956`, 11358 bytes) has the same sha256 (`cfc7749b…3d30`) as the canonical text fetched today (HTTP 200), and `cmp` reports byte identity (`receipts/licence_compare.txt`).
  - NOTICE contains the product name, "Copyright 2026 kebag-logic" and a licence statement. That suits a section 4(d) notice, since no third-party attribution needs to be carried. It matches the README licence section and the issue's copyright holder.
  - LICENSE and NOTICE blobs are identical in `fed1a0d` and the head.
- **Acceptance 2 (SPDX headers):** all 45 tracked files were audited (`receipts/validate_logs/spdx_audit.log`).
  - 22 C/H files have `/* SPDX-License-Identifier: Apache-2.0 */` on line 1.
  - 8 Markdown files have `<!-- … -->` on line 1.
  - 13 hash-comment files have it on line 1, except `build.sh`, where it is on line 2 after the shebang, which is kept.
  - No other SPDX identifier appears anywhere.
- **Acceptance 3 (no third-party code or other licence):**
  - No other licence or copyright marker appears in any historical blob or commit message (`receipts/history_scan.txt`).
  - `src/core/switch_ctrl.c:23` and `src/include/shish_lan/switch_ctrl.h:93` name a published MPSC queue algorithm, but the code is the project's own C11-atomics implementation with project naming and its own sentinel scheme. It contains no copied notice or licence text. An attributed algorithm is not third-party code, so there is no finding.
  - The commit identities are the owner's company identity, the owner's personal identity (root commit) and the hosting service's merge identity. That matches the PR's provenance statement.
- **Acceptance 4:** see Tests.
- **Merge resolution:**
  - Replaying `git merge-tree --write-tree fed1a0d 02700d9` conflicts in exactly two places: README.md (content) and `tests/unit/placeholder.c` (modify/delete).
  - The head tree differs from the replayed tree only there: README.md is main's blob `f6e2d5fb` and the placeholder is deleted, as the PR body says (`receipts/merge_check.txt`).
  - `02700d9..375dbe13` adds only LICENSE, NOTICE and one SPDX line in each of 27 files, and deletes nothing.
  - `fed1a0d`'s README licence text is semantically the same as main's line 58.
- **Unclean** because of F1.

### RTL

Not applicable. lwSRP is a host C library with no HDL. The pinned simulator was not needed and was not used.

### Robustness

- **No header breaks a file:** C compiles with `-Wall -Wextra -Wpedantic` and 0 warnings. Kconfig.zephyr parses (symbols `LWSRP`, `MODULES`). `zephyr/module.yml` parses to exactly `{name, build}`. `behave.ini` parses. Every `.py` parses. Gherkin parses (dry run). `bash -n build.sh` passes.
- **Mutation probes** on disposable copies (`receipts/probes_summary.txt`): all 12 behave as expected.
  - Removing LICENSE or NOTICE makes the link check fail.
  - A wrong comment syntax breaks Kconfig, Gherkin and C.
  - A C-style header in `module.yml` adds a stray key, which the tightened check catches. The first, looser variant did not discriminate (`receipts/probes_summary_run1.txt`); it was corrected and run again.
- **File modes:** unchanged; only `build.sh` is executable.
- **Clean.**

### Tests

The tree was exported with `git archive` at the exact head; the steps are in `scripts/validate_head.sh` and the logs in `receipts/validate_logs/`. cgreen 1.7.0 was built from upstream source in private scratch.

- **Build:** configure rc 0, build rc 0.
- **ctest:** rc 0. `mrp_pdu_suite` has 9 tests and 1690 passes.
- **behave:** rc 0. 1 feature, 3 scenarios and 10 steps passed.

These match issue #8 acceptance 4 and the PR body.

**Clean.**

### Docs

- Sentence check: 760 sentences, 0 over the limit.
- Reference check: 0 unlinked references; its self-test ran 79 cases with 0 failures.
- Link check: `--local-only` resolves 290 local links with 0 failures, including every LICENSE and NOTICE link in README.md, CONTRIBUTING.md, doc/manager.md and doc/tools/README.md. `--github-auth` passes 17 of 18 external URLs; the one failure is iso.org HTTP 403, as the PR body records.
- Tree hygiene: no host paths, private hostnames, devices, credentials, e-mail addresses, or tool or model names (`receipts/history_url_email_scan.txt` and the tree scans).
- R1 and R2 are RESIDUE.
- **Unclean** because of F1 (historical documentation content).

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN (F1) | LICENSE vs canonical text, NOTICE, 45-file SPDX audit, history licence/provenance scan (13 commits, 109 blobs), queue attribution, merge replay | R538-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| RTL | N/A | none applicable: host C library, no HDL | R538-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Robustness | CLEAN | Kconfig/YAML/INI/Python/Gherkin/C/shell parses, shebang order, file modes, 12 mutation probes | R538-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Tests | CLEAN | build, ctest (1690), behave (3 scenarios, 10 steps) on the exported head; author packet comparison | R538-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |
| Docs | UNCLEAN (F1); R1, R2 RESIDUE | sentence, reference and link checks; LICENSE/NOTICE links; tree and history hygiene scans | R538-1 | 375dbe132c6f1498f2f3e714ce5905d34456c9d5 |

## Real limits

- Mermaid rendering (`doc/tools/render_mermaid.py`) was not run, because it needs a browser runtime. It does not bear on the licence change: no graph changed in `02700d9..375dbe13`.
- The canonical licence text was fetched once today from apache.org; equality is against that fetch.
- The hygiene term lists are heuristic. The history scan uses a private list of account, tool and model names that is not published. Matched names are redacted to `[TOOL]` in the receipts.
- The `diff_*.patch` receipts are redacted the same way, so they are no longer byte-exact diffs. They can be regenerated with `git diff <a> <b>`.
- No hosted CI exists for this repository: there are no workflow files, the commit has 0 check runs, and its combined status is `pending` with 0 contexts. There was no hosted evidence to inspect.
- Physical calibration was not run. Nothing here is hardware evidence.
- The Zephyr build path (`ZEPHYR_BASE` branch of CMakeLists.txt) was parsed but not built.

## Pending manager duties

- Obtain and link the owner's decision on F1: accept the history as it is, or rewrite it before publication.
- Carry R1 and R2 to the residue checklist.
- Hosted/act acceptance, and the final current-dev candidate build at merge time (source base `02700d9e`, live dev `09f1841b`).
- The second independent review (R539).

## Restore verification

After all probes, the clone is at `375dbe13` with tree `942f26fe`:
- `git status --porcelain --ignored` is empty.
- The index equals HEAD, and the worktree equals the index.
- All 45 blob hashes and modes match the tree.
- There are no gitlink entries (no submodules are required).

See `receipts/restore_verification.txt`.

R538-1 FINISHED
