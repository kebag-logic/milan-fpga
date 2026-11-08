[R798] POSITIVE - exact head 62d24a37c4b81a78edda2721dd8611d753b2bc8e

# R798-1 external independent review: kebag-logic/tsn-c-stack PR #30

- Exact head `62d24a37c4b81a78edda2721dd8611d753b2bc8e`, tree `39369307e99aab4c06f6b47e4bbd1d0f25c413d0`, verified in a detached clean clone (`receipts/00-identity.txt`, `receipts/04-integrity.txt`).
- Base: main `d7e6a2a19a57a8277cd26042557a8c99f2ee5496` (merge of #29). Two PR commits: `0cfa8423` and `62d24a37`.
- Scope: issue #none (main CI red). Rewriting main is out of scope. The change exempts exactly one commit from the one-line message rule of `scripts/check_privacy.py`, in the same way the gate already exempts the owner squash `ae982af8`. It records the exemption in `docs/VERIFICATION.md`, `docs/IMPORT.md` and `CHANGELOG.md`.

## Verdict summary

POSITIVE. All five lenses are clean. There is no open BLOCKER, MAJOR or MINOR finding.
- One RESIDUE (PR body wording) goes to the residue checklist.
- Two SUGGESTIONs are recorded. Both are outside the reviewed delta's behaviour.
- All five R797-1 findings are re-checked at this head: four are resolved, and S2 is retained as my S1, a SUGGESTION.

## Reconstruction

- `CONTRIBUTING.md:14-17`: one-line commit subjects, no body, neutral labels, no host or product names. `AGENTS.md` does not exist in this repository.
- `docs/VERIFICATION.md:41-42` lists the privacy gates. `docs/IMPORT.md:128-141` ("Squash metadata") documents the identity and one-line rule and its exceptions. `docs/CODING_STANDARD.md:3` and `scripts/check_comments.py` set the comment contract, which covers only C, C++, assembly and linker sources.
- PR body (public): the scope and acceptance as stated in the review brief. Round 2 lists R797-1 F1 and S1, S3 and S4 as taken, and S2 as not taken.
- Requirements: no `REQ` ID, requirement record or traceability row is affected. `docs/REQUIREMENTS.md`, `docs/TRACEABILITY.md` and `requirements.json` are untouched.
- Delta: `git diff d7e6a2a1..62d24a37` changes 4 files (+16/-3): `scripts/check_privacy.py`, `docs/VERIFICATION.md`, `docs/IMPORT.md`, `CHANGELOG.md`. Nothing else changed. The added lines contain no non-ASCII byte.
- History: `d7e6a2a1` has parents `70936b77` and `c687810b`. Its author is `hackerman-kl <161579364+Mister-M-alt@users.noreply.github.com>` and its committer is `GitHub <noreply@github.com>`, which is exactly the gate's `WEB_FLOW` pair. Its message is the subject "Merge pull request #29: ..." plus one body paragraph. Its tree `20c87867` equals the tree of its second parent, so the merge brings in no content of its own. Both PR commits use the holder pair and a one-line message.
- Public evidence: milan-fpga `acdaccf5` `review-evidence/tsn30-r1/author` and `author-r2`.
  - `author/change.diff` and `author-r2/round2.diff` are byte-equal to `git diff d7e6a2a1..0cfa8423` and `git diff 0cfa8423..62d24a37`.
  - Their published sha256 values match `MANIFEST.json`.
  - The figures in `author-r2/gates.log` (14 controls; 18 commits, 268 blobs, 98 files) equal my own run (`receipts/06-author-evidence.txt`).

## Executed evidence (this review)

The probe script is `scripts/run_probes.sh <clone> <packet>`. It ran in the foreground. Every edit was made in disposable copies under `scratch/`; the clone was only read.

| Check | Result | Receipt |
|---|---|---|
| `check_privacy.py --selftest` at head | `14 commit controls pass`, rc 0 | `01-gates.txt` |
| `check_privacy.py` at head | owner-squash line, `exact #29 merge one-line exception; identity and content checks remain enabled`, `18 commits, 268 historical blobs, 98 current files; pass`, rc 0 | `01-gates.txt` |
| main `d7e6a2a1` with its own gate | `d7e6a2a1...: commit message must be one line`, rc 1 (its selftest: 11 pass) | `01-gates.txt` |
| main `d7e6a2a1` history with the head gate | pass, 16 commits, rc 0 | `01-gates.txt` |
| head history with the main gate | the only error is the `d7e6a2a1` one-line error, rc 1 | `01-gates.txt` |
| `check_license.py` and `--selftest` at head | pass, rc 0 | `01-gates.txt` |
| Reachable multi-line commits | only `ae982af8` and `d7e6a2a1` (18 reachable) | queried during review; see Robustness |

Mutation probes on `check_privacy.py` (`receipts/02-mutations.txt`):

| ID | Mutant | Selftest | Gate | Outcome |
|---|---|---|---|---|
| M1 | drop the exemption from the one-line rule | fail `two-line-merge` | - | killed |
| M2 | also exempt the merge from the identity check | fail `two-line-merge-foreign` | - | killed |
| M3 | match the 8-char prefix | fail `two-line-merge-near-miss` | - | killed |
| M4 | match the 39-char prefix | fail `two-line-merge-near-miss` | - | killed |
| M5 | match the merge subject instead of the id | fail `two-line-merge-near-miss` | - | killed |
| M6 | exempt every web-flow commit from the one-line rule | fail `web-flow-two-lines`, `two-line-merge-near-miss` | - | killed |
| M7 | remove the near-miss id derivation (test of the test) | fail `two-line-merge-near-miss` | - | killed: the control is load-bearing |
| M8 | skip the content scan for the exempt id in `main()` | 14 pass | pass | survives (S1) |
| M9 | drop the identity error for the exempt id in `main()` | 14 pass | pass | survives (S1) |

Synthetic end-to-end probes (`receipts/03-synthetic.txt`) use a fresh two-commit history. The second commit has a two-paragraph message, and its id is patched into a working-tree copy of the head gate:
- S1-clean, web-flow pair: pass, rc 0.
- S2, restricted path in the body: `restricted content`, rc 1, with no one-line error.
- S3, foreign identity: `unexpected identity`, rc 1.

This shows that inside `main()` the exemption removes the one-line error only.

Hosted runs at the exact head (`receipts/05-hosted.txt`, read-only queries):
- Run 42472276375 (pull_request) and run 42472273572 (push): `quality` and `bare-metal` executed and succeeded. Each checkout is `git checkout --force 62d24a37...`, and every validate step reports rc 0, including `privacy-selftest` and `privacy`.
- Main run 42467930308 at `d7e6a2a1`: `quality` failed with `privacy: rc 1` as its only failing step.

## Lenses

- **Conformance - CLEAN.**
  - The change conforms to `CONTRIBUTING.md:14-17`: both PR commits use the holder pair and a one-line message.
  - The exemption mirrors the existing owner-squash pattern by full id.
  - No protocol behaviour, requirement or traceability claim changes.
  - Comment rule: the new comment `scripts/check_privacy.py:16` states the behaviour (exempt from the one-line rule only) and the reason (recorded with a second paragraph; main is not rewritten), and cites #29. It contains no bench lane label, lane name, review round, reviewer ID or issue-comment ID, so it adds no RESIDUE. The `[A10]` tag appears only in PR text, where lane names are allowed.
- **RTL - CLEAN.**
  - The delta touches no RTL, C, header, test or build file (diffstat in `00-identity.txt`), so there is nothing to simulate. The pinned Verilator was not needed.
  - The hosted `bare-metal` job at the exact head succeeded and is unaffected by the change.
- **Robustness - CLEAN.**
  - The exemption is a set lookup on the full 40-hex id (`check_privacy.py:17,34`). Prefix, subject-match and broad web-flow broadenings are all killed (M3-M6).
  - The identity check (`:32`) and the content scan (`main()`, `:79`) still apply to `d7e6a2a1`. This is shown by code reading, by M2, and by the synthetic probes S2 and S3. `d7e6a2a1` passes the identity check on its own merits, because its pair is exactly `WEB_FLOW`.
  - The only reachable multi-line commits are `ae982af8` and `d7e6a2a1`. Every other commit at this head still meets the one-line rule.
  - The log line at `:82-83` fires only when the id is reachable.
- **Tests - CLEAN.**
  - There are three new controls (`:53-55`): the two-line merge passes under its exact id; the same message fails under a foreign identity; the same message fails under an id one digit away (`...4960`).
  - The 11 earlier controls still use the zero id or the owner squash id and still give the same results. `web-flow-two-lines` and `holder-two-lines` keep failing for any other commit.
  - All of M1-M7 are killed.
  - The `main()` loop has no selftest control (S1). This structure existed before the change and the delta does not weaken it.
- **Docs - CLEAN.**
  - `docs/VERIFICATION.md:42` matches the 14 controls exactly.
  - `docs/IMPORT.md:133-137` drops the now-false "only", and records the full id link, "the one-line rule only", identity and content still checked, and main not rewritten.
  - `CHANGELOG.md:5` matches the gate.
  - The log text matches the behaviour.
  - S2 notes an older sentence that the delta did not change.

## Findings

### R1 - RESIDUE - Docs (PR body wording)

- **Where:** PR #30 body, last paragraph: "No C source or test changes."
- **Evidence:** the head adds three self-test controls in `scripts/check_privacy.py:53-55,60-61`. The body itself lists them, so the claim is only imprecise: nothing under `tests/` changed.
- **Impact:** wording only. It changes no measurement, test, code or privacy rule.
- **Exact fix:** "No C source or `tests/` changes; the gate self-test gains three controls."
- **Verification:** re-read the PR body.

### S1 - SUGGESTION - Tests, Robustness

- **Where:** `scripts/check_privacy.py:72-83` (the per-commit loop in `main()`). Mutants M8 and M9.
- **Issue:** the selftest exercises only `commit_errors`. If the content scan or the identity error were skipped for the exempt id inside `main()`, every gate would still pass at this head. This is the same structure that already exists for the owner squash, and the delta does not touch that path. It carries over R797-1 S2, which the author declined as a separate change.
- **Suggestion:** in a follow-up, route the per-commit checks through one function that the selftest calls with the exempt id and a planted restricted string.
- **Verification:** M8 and M9 then fail the selftest.

### S2 - SUGGESTION - Docs

- **Where:** `docs/IMPORT.md:138`, "Later pull requests are squash-merged on GitHub.", which this delta did not change.
- **Issue:** the new sentence at `:135` documents `d7e6a2a1`, a two-parent merge commit, directly before this claim. The identity rule that follows (`:139-140`) is still accurate, because the merge uses the hosted pair.
- **Suggestion:** "Later pull requests are merged on GitHub with a one-line message. Their commits carry the account's noreply author and GitHub as committer."
- **Verification:** re-read the section against `git log --merges`.

## Prior public findings at this head (read after my own pass and verdict; `receipts/07-own-pass-verdict.txt`)

| Finding | Status at 62d24a37 | Evidence |
|---|---|---|
| R797-1 F1 (MINOR, docs did not match the gate) | RESOLVED | `docs/VERIFICATION.md:42`, `docs/IMPORT.md:133-137` and `CHANGELOG.md:5` now record the exact commit, "one-line rule only", identity and content still checked, and main not rewritten. The PR body no longer says there is no docs change. |
| R797-1 S1 (near-miss control) | RESOLVED | control `two-line-merge-near-miss` added; M3 and M4 are killed |
| R797-1 S2 (scan control) | RETAINED as SUGGESTION (my S1) | M8 survives; the author declined it as a separate change |
| R797-1 S3 (log line) | RESOLVED | `check_privacy.py:82-83`; the line appears in the head gate output |
| R797-1 S4 (comment gives the reason) | RESOLVED | `check_privacy.py:16` now says main's published history is not rewritten; still within the comment rule |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CONTRIBUTING.md:14-17`; `scripts/check_privacy.py:15-36`; commit objects `d7e6a2a1`, `0cfa8423`, `62d24a37` (identity, parents, messages); comment `:16` against the owner comment rule; PR body | R798-1 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| RTL | CLEAN | diffstat (4 files, no RTL, C or test source); hosted `bare-metal` job at the exact head | R798-1 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Robustness | CLEAN (S1 open as a suggestion) | `check_privacy.py:17,26-36,72-83`; M2-M6; synthetic S1-S3; reachable multi-line commit list; merge tree equals second-parent tree | R798-1 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Tests | CLEAN (S1 open as a suggestion) | `check_privacy.py:39-65`; head selftest 14 pass; main selftest 11 pass; M1-M9; head and main gate cross-runs; licence gate and selftest; hosted runs 42472276375, 42472273572, 42467930308 | R798-1 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Docs | CLEAN (R1 residue; S2 open as a suggestion) | `docs/VERIFICATION.md:41-42`; `docs/IMPORT.md:128-141`; `CHANGELOG.md:3-6`; gate log text; author receipts and manifest hashes | R798-1 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |

## Real limits

- No manager source bank runs at this head, and I claim none. Source-head execution evidence is the author's published gate receipts, my own focused gate runs, and the hosted runs.
- I did not run the full `validate.py` bank locally (out of scope). The hosted runs at the exact head executed it, with every step at rc 0.
- I did not run `check_comments.py` locally: the comment lexer is not on this host's search path. The delta changes no file in the gate's suffix set (`.c .h .cpp .hpp .S .ld`), and the hosted `comments` step at the exact head reports rc 0.
- The exemption relies on the repository's SHA-1 object ids, the same as the owner-squash exception.
- Physical calibration was NOT RUN and does not apply. There is no hardware proof.
- The final current-dev candidate (source base `d7e6a2a1`, live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`) was not examined. That object is not present in this clone.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn and link its receipts on the PR. Own hosted and act acceptance.
- Record #30 on main with a one-line message under the holder or hosted pair. GitHub's default message for a merge commit, or for a squash of this two-commit PR, adds a body that this gate would reject on main again.
- Carry R1 to the residue checklist.
- Merge still needs two independent positive reviews and the full completion bar.

R798-1 FINISHED
