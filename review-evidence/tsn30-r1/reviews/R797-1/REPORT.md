[R797] NEGATIVE - exact head 0cfa8423cbdde8ed6b679a022afa6401f6d62899

# R797-1 independent review: kebag-logic/tsn-c-stack PR #30

- Exact head `0cfa8423cbdde8ed6b679a022afa6401f6d62899`, tree `a8c20d606b2aee4423484bcd41e050f9cda761ae` (both verified in the detached review clone).
- Source base `d7e6a2a19a57a8277cd26042557a8c99f2ee5496` (main, the merge of #29). Tracking issue: none (main CI red).
- Reviewed delta: `git diff d7e6a2a1..0cfa842`. One file, `scripts/check_privacy.py`, +6/-1, mode 100644 in both trees.
- Public review start: PR #30 comment 6720358089. No earlier public review findings exist on this PR. At reading time the only comment was the review-start notice, and the PR had no reviews and no inline comments. Nothing needed resolving.

## Verdict summary

The code change is correct and as narrow as the PR states:
- The gate exempts the full 40-hex id of `d7e6a2a1` from the one-line message rule only.
- The identity check and the content scan still reach that commit. Fault probes confirm both.
- The two new controls test what they name, and the existing two-line controls still fail for any other id.
- The privacy gate passes at this head and fails on main only on `d7e6a2a1`. The comment and licence gates pass.
- Nothing else changed.

The verdict is NEGATIVE for one reason: the repository's own documents still describe the old exception set. They now contradict the gate and its self-test (F1, MINOR).

That defect describes a privacy rule and a documented test claim, so under the owner rule it cannot be RESIDUE.

## Reconstruction

- `CONTRIBUTING.md:14`: "Use one-line commit subjects. Use no body, trailers or attribution footer." `CONTRIBUTING.md:19` links the privacy gate.
- `docs/IMPORT.md:128-138` ("Squash metadata"): the gate exempts only the owner squash `ae982af8` from the identity and one-line checks. Every new commit must use one of the two identity pairs and a one-line subject.
- `docs/VERIFICATION.md:41-42`: gate table rows for `check_privacy.py` and `check_privacy.py --selftest`.
- `CHANGELOG.md:8`: precedent entry for an earlier privacy-gate acceptance change ("Accept GitHub squash merges in the privacy gate ...").
- `scripts/validate.py:69-70`: the hosted driver runs `privacy-selftest` and then `privacy`. `.github/workflows/quality.yml` checks out with `fetch-depth: 0` at `pull_request.head.sha || sha`.
- The repository has no requirement ID for the privacy gate. `docs/REQUIREMENTS.md` and `docs/CODING_STANDARD.md` have no privacy or commit-message entry. No HDL source is tracked (0 `.v/.sv/.vhd` files).
- The PR body states the scope and validation. It also says "No source, test or docs change."
- Author receipts: milan-fpga `8a5ed4ee` `review-evidence/tsn30-r1/` (`MANIFEST.json`, `author/gates.log`, `author/change.diff`).
  - Both files match their manifest `published_sha256`.
  - `author/change.diff` is byte-identical to my `git diff d7e6a2a1..0cfa842`.
  - `author/gates.log` matches my independent results line for line: selftest 13 controls; head 17 commits, 264 historical blobs, 98 current files, pass; main fails on `d7e6a2a1`; comments 34 files pass.

## Executed evidence (this review)

Script: `scripts/run_gates_and_probes.sh <review-clone> <packet> <clang-18>`. Every run used a fresh local clone under `scratch/`. Log: `receipts/gates-and-probes.log` (host paths redacted to `$PACKET`, `$CLONE`, `$TOOLS`). The pinned lexer reported `Ubuntu clang version 18.1.3`.

| Run | Tree | Result |
|---|---|---|
| `check_privacy.py --selftest` | head | `13 commit controls pass`, rc 0 |
| `check_privacy.py` | head | `17 commits, 264 historical blobs, 98 current files; pass`, rc 0 |
| `check_privacy.py --selftest` | main `d7e6a2a1` | `11 commit controls pass`, rc 0 |
| `check_privacy.py` | main `d7e6a2a1` | only `d7e6a2a1...: commit message must be one line`, rc 1 |
| `check_license.py --selftest` / plain | head | pass / pass, rc 0 |
| `check_comments.py` / `--selftest` | head | `34 code files and all mutation fragments pass`; all controls refused or passed as named, rc 0 |
| `git diff --raw d7e6a2a1 0cfa842` | - | `:100644 100644 b2385cf 211d9f4 M scripts/check_privacy.py` only |

Mutation and fault probes. Each probe edits `scripts/check_privacy.py` in its own clone:

| Probe | Change | Selftest | Gate at head | Reading |
|---|---|---|---|---|
| M1 | drop the exemption | `fail two-line-merge` | fails on `d7e6a2a1` | the control and the gate both need the exemption |
| M2 | exemption also skips identity | `fail two-line-merge-foreign` | pass | the foreign control pins the identity rule for the exempt id |
| M3 | one-line rule off for every commit | `fail web-flow-two-lines, holder-two-lines` | pass | the existing controls still bound other ids |
| M4 | match on the 8-char prefix | 13 pass | pass | survives; no near-miss control (S1) |
| M5 | two-line controls use the zero id | `fail two-line-merge` | pass | the positive control depends on the exact id |
| M6 | skip the content scan for the exempt id | 13 pass | pass | survives; the content scan is not pinned by a control (S2) |
| P1 | add a pattern for the exempt commit's body text | 13 pass | `d7e6a2a1...: restricted content`, rc 1 | the content scan reaches the exempt commit |
| P2 | change the web-flow committer email | 13 pass | `d7e6a2a1...: unexpected identity` (+7 other web-flow commits), rc 1 | the identity check reaches the exempt commit |

Direct boundary calls on the head `commit_errors`:
- The exempt id with the web-flow pair or the holder pair passes with two lines.
- The exempt id with the reversed pair fails on identity.
- These ids all fail on the one-line rule: abbreviated `d7e6a2a1`, upper-case, last digit changed, trailing newline, zero id, and the merge's first parent `70936b77`.
- The owner squash is unchanged.
- The repository object format is sha1. The match is an exact string-set lookup, so it fails closed under any other id form.

Hosted evidence at the exact head was read through the read-only API (`receipts/head-check-runs.json`, `receipts/hosted-gate-summary.txt`):
- Runs 42471280863 (push) and 42471294304 (pull_request) checked out `0cfa842`.
- `quality` executed every gate, `privacy-selftest` and `privacy` included, with rc 0. `bare-metal` succeeded.
- Main's run 42467930308 at `d7e6a2a1` ran `quality` to `privacy: rc 1` and stopped there. Every earlier gate had rc 0.
- Those runs executed; no context was skipped. Hosted and act acceptance remain the manager's.

Clone integrity after probes (`receipts/clone-integrity.txt`): the review clone was never edited.
- HEAD and tree are exact, and porcelain status is empty, ignored files included.
- Index entries (mode, blob, path) equal the HEAD tree.
- Every worktree blob hash matches HEAD.
- `check_privacy.py` is blob `211d9f4`, mode 644.
- The repository has no gitlinks and no `.gitmodules`, so no submodule gitlink is required.

## Findings

### F1 - MINOR - Docs, Conformance

- **Where:**
  - `docs/VERIFICATION.md:42`
  - `docs/IMPORT.md:133` and `docs/IMPORT.md:136-138`
  - `CHANGELOG.md:3-8` (no entry)
  - against `scripts/check_privacy.py:16-17,34,53-54`
- **Authority and evidence:**
  - `VERIFICATION.md:42` documents the self-test: "the exact owner squash passes ... and so does a multi-line message [fail]". At this head the control `two-line-merge` (`check_privacy.py:53`) requires a multi-line message to pass for `d7e6a2a1`. The row does not mention that exemption or its two controls.
  - `IMPORT.md:133` says the gate "exempts only that exact commit" (`ae982af8`). `IMPORT.md:136` says "Every new commit must use one of these two identity pairs and a one-line subject". The gate now accepts `d7e6a2a1`, a post-import commit with a two-paragraph message.
  - The PR body says "No ... docs change". The precedent at `CHANGELOG.md:8` records privacy-gate acceptance changes, but no entry was added.
- **Impact:**
  - The written privacy rule and the documented test claim no longer match the gate. A reader of the governing documents would believe the owner squash is the only exception.
  - The new exception has no trace outside the source comment and this PR.
  - This touches a privacy rule and a test claim, so it is not RESIDUE.
- **Required outcome:**
  - In `docs/VERIFICATION.md:42`, record that the exact merge of #29 passes with a two-paragraph message under its identity pair, and that the same message fails under a foreign identity.
  - In `docs/IMPORT.md` "Squash metadata", record `d7e6a2a19a57a8277cd26042557a8c99f2ee5496` as the one commit exempt from the one-line rule only. Say that its identity and content are still checked, and that main's history is not rewritten.
  - Add an Unreleased `CHANGELOG.md` entry, for example: "Exempt the merge of #29 from the one-line message rule by its exact commit; its identity and content are still checked."
- **Verification:** re-read the three locations against `check_privacy.py`. `check_privacy.py` and `--selftest`, `check_port_contracts.py --selftest` and `traceability.py --selftest` still pass.

### S1 - SUGGESTION - Tests, Robustness

- **Where:** `scripts/check_privacy.py:53-59`. Probe M4.
- **Issue:** a prefix-match broadening of the exemption survives both the self-test and the gate. Every non-exempt control uses the zero id.
- **Suggestion:** add a near-miss control: the exempt id with one hex digit changed, the web-flow pair and two lines, expected to fail.
- **Verification:** M4 fails the self-test.

### S2 - SUGGESTION - Tests

- **Where:** `scripts/check_privacy.py:65-67,77`. Probe M6.
- **Issue:** the PR's claim that the content scan still runs on the exempt commit is true by code (P1) but not pinned by a control. A change that skips `scan` for the exempt id passes everything. This is a pre-existing structure: `scan` has no self-test control for any commit, and this delta does not touch that path.
- **Suggestion:** add a scan control on the exempt commit's metadata.
- **Verification:** M6 fails the self-test.

### S3 - SUGGESTION - Robustness, Docs

- **Where:** `scripts/check_privacy.py:78-79`.
- **Issue:** the gate logs a line when the owner-squash exception is reachable, but nothing when the new exemption is applied.
- **Suggestion:** add an equivalent line, for example "privacy: exact #29 merge one-line exception; identity and content checks remain enabled", so gate logs show the exception in use.

### S4 - SUGGESTION - Docs (comment judgement)

- **Where:** `scripts/check_privacy.py:16`.
- **Judgement:** the comment complies with the owner comment rule.
  - It states the behaviour ("exempt from the one-line rule only") and the cause ("recorded with a second message paragraph").
  - It cites #29 and contains no bench lane label, lane name, review round, reviewer ID or issue-comment ID, so it adds no RESIDUE.
  - It is accurate, because identity and content are still checked.
  - No tracking issue and no requirement ID exist to cite.
- **What it omits:** why an exemption is used instead of a fix: main's published history is not rewritten.
- **Suggested wording:** "Merge of #29 (d7e6a2a1) was recorded with a second message paragraph and main is not rewritten; it is exempt from the one-line rule only, and its identity and content are still checked."

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `CONTRIBUTING.md:14,19`; `docs/IMPORT.md:128-138`; `docs/VERIFICATION.md:41-42`; `CHANGELOG.md`; PR body; `d7e6a2a1` and `0cfa842` commit objects (identity pairs, messages) | R797-1 | 0cfa8423cbdde8ed6b679a022afa6401f6d62899 |
| RTL | CLEAN (not applicable) | 0 tracked HDL files; the delta is one Python gate script; no hardware or timing claim | R797-1 | 0cfa8423cbdde8ed6b679a022afa6401f6d62899 |
| Robustness | CLEAN (S1, S3 open as suggestions) | `check_privacy.py:15-36,70-94`; boundary calls (abbreviated, case, near-miss, newline, parent id, reversed pair); P1/P2 fault probes; sha1 object format; fail-closed exact lookup | R797-1 | 0cfa8423cbdde8ed6b679a022afa6401f6d62899 |
| Tests | CLEAN (S1, S2 open as suggestions) | `check_privacy.py:39-63`; head selftest 13 pass; main selftest 11 pass; M1-M6 mutations; head/main gate runs; licence and comment gates and their self-tests; hosted runs 42471280863, 42471294304, 42467930308 | R797-1 | 0cfa8423cbdde8ed6b679a022afa6401f6d62899 |
| Docs | UNCLEAN (F1) | `docs/VERIFICATION.md:42`; `docs/IMPORT.md:133,136-138`; `CHANGELOG.md:8`; source comment `check_privacy.py:16` (rule-compliant, S4); author receipts and manifest hashes | R797-1 | 0cfa8423cbdde8ed6b679a022afa6401f6d62899 |

## Real limits

- My gate runs used the local Python 3.14 and git 2.56, not the hosted Ubuntu 24.04 image. The hosted runs at this head are cited as read, not reproduced.
- I did not run the full validation driver, the builds, the mutation campaign or the RV32 bank. The delta cannot reach C sources. Hosted runs at this head report those gates at rc 0.
- The pinned simulator was not needed: the delta contains no HDL.
- No manager source bank ran at this head, and none is claimed or inferred. The author's receipts are source-head evidence only.
- Physical calibration NOT RUN. No hardware claim is made.
- The merge candidate against live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c` was not built or examined.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link the receipts on the PR. With this delta, `privacy` must pass on the candidate, whose history includes `d7e6a2a1`.
- Own hosted and act acceptance.
- Carry F1 back to the author for a docs update at a new head, then a re-review of that head.
- No RESIDUE item is raised by this round.

R797-1 FINISHED
