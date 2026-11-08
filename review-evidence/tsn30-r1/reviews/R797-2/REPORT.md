[R797] POSITIVE - exact head 62d24a37c4b81a78edda2721dd8611d753b2bc8e

# R797-2 independent review: kebag-logic/tsn-c-stack PR #30

- **Head:** exact head `62d24a37c4b81a78edda2721dd8611d753b2bc8e`, tree `39369307e99aab4c06f6b47e4bbd1d0f25c413d0`. I verified both in the detached review clone.
- **Base:** source base `d7e6a2a19a57a8277cd26042557a8c99f2ee5496` (main, the merge of #29). Tracking issue: none (main CI red).
- **Previously reviewed head:** `0cfa8423` (R797-1, NEGATIVE on F1).
- **Delta since that head:** `git diff 0cfa842..62d24a37`. One commit, four files, every mode 100644 in both trees:

  | File | Change |
  |---|---|
  | `CHANGELOG.md` | +1 |
  | `docs/IMPORT.md` | +4/-1 |
  | `docs/VERIFICATION.md` | +1/-1 |
  | `scripts/check_privacy.py` | +5/-1 |

  Full PR delta `d7e6a2a1..62d24a37`: the same four files, +16/-3.
- **Commit `62d24a37`:**
  - It uses the holder identity as both author and committer.
  - Its message is one line with no body or trailer, as `CONTRIBUTING.md:14` requires.
- **Review start:** PR #30 comment 6720468644.

## Verdict summary

Round 1 found one defect, F1: the docs did not record the new exemption. This head fixes it.
- `docs/VERIFICATION.md:42`, `docs/IMPORT.md:133-137` and `CHANGELOG.md:5` now describe the exemption of `d7e6a2a1` as the gate implements it:
  - by the exact commit id;
  - from the one-line rule only;
  - with its identity and content still checked;
  - with main's history not rewritten.

The three suggestions that were taken work as stated:
- **S1:** the new near-miss control now catches the prefix-match mutation that survived round 1.
- **S3:** the log line prints when the exempt merge is in history and stays silent when it is not.
- **S4:** the code comment now says why an exemption stands. It follows the comment rule.

The PR body says S2 is not taken and why. I keep S2 open as a suggestion.

The gates pass at this head, both in my runs and in the hosted runs. The author's round-2 receipts match their manifest and my own diff.

No MINOR, MAJOR or BLOCKER finding is open. Three suggestions remain (S2, S5, S6). There is no RESIDUE.

## Reconstruction (delta-scoped)

**Authorities.** The repository has no `AGENTS.md`. The authorities, which this delta leaves unchanged, are:
- `CONTRIBUTING.md:14`: one-line commit subjects, no body.
- `CONTRIBUTING.md:19`: link to the privacy gate.
- `docs/IMPORT.md` "Squash metadata" (`:128-139`) and `docs/VERIFICATION.md:41-42`: the governing text that F1 named.
- No requirement ID covers the privacy gate. No HDL is tracked.
- The round-1 reconstruction stands for everything else (`scripts/validate.py:69-70` runs `privacy-selftest` and then `privacy`).

**Public scope.**
- The PR body says what broke, the change, how to validate, and a "Round 2" section mapping F1, S1, S3 and S4 to the changes.
- It says S2 is not taken because `scan` has no self-test control for any commit.
- It says no C source or test changes.

**Prior public findings on this PR.** I read them only after my own pass over the diff. The only report is my own R797-1 (comment 6720436497: F1 MINOR; S1-S4 suggestions). The PR has no reviews and no inline comments. A second reviewer's start notice (6720511160) carries no findings. Every round-1 item is resolved or kept below.

**Author receipts** (milan-fpga `acdaccf524b8107625c1f8c71bb1e7712edb2948`, `review-evidence/tsn30-r1/`, branch `tsn30-review-evidence`, read through the read-only API):
- `author-r2/round2.diff`
  - sha256 `823164a6...87d11a` matches its manifest `published_sha256`.
  - It is byte-identical to my `git diff 0cfa842..62d24a37`.
- `author-r2/gates.log`
  - sha256 `ffc73e49...afa83fa` matches its manifest `published_sha256` (path-redacted).
  - Every line agrees with my runs:
    - self-test: 14 controls;
    - gate: both exception log lines, then 18 commits, 268 historical blobs, 98 current files, pass;
    - comments: 34 files pass;
    - port contracts: self-test passes.
- The evidence commit is not GPG-signed: GitHub reports `unsigned`. Integrity rests on the manifest hashes, which I checked, and on the diff being byte-identical to mine.
- The author log does not name the head it ran on. Its counts (18 commits, 268 blobs) are unique to this head among the trees I ran: the parent gives 14 and 255.

## Executed evidence (this review)

The script is `scripts/run_gates_and_probes.sh <review-clone> <packet> <clang-18>`. Every run used a fresh local clone under `scratch/`. The log is `receipts/gates-and-probes.log`, with host paths redacted to `$PACKET`, `$CLONE` and `$TOOLS`. Tools: Python 3.14.8, git 2.56.0, pinned clang 18.1.3, pinned GoogleTest 1.14.0.

| Run | Tree | Result |
|---|---|---|
| `check_privacy.py --selftest` | head | `14 commit controls pass`, rc 0 |
| `check_privacy.py` | head | owner-squash line; `exact #29 merge one-line exception; identity and content checks remain enabled`; `18 commits, 268 historical blobs, 98 current files; pass`, rc 0 |
| `check_privacy.py --selftest` | prior head `0cfa842` | `13 commit controls pass`, rc 0 (the near-miss control is new) |
| head `check_privacy.py` in the history of the merge's first parent `70936b77` | parent | owner-squash line only, no #29 line; `14 commits, 255 historical blobs ... pass`, rc 0 |
| `check_privacy.py` / `--selftest` | main `d7e6a2a1` | only `d7e6a2a1...: commit message must be one line`, rc 1 / 11 controls pass |
| `check_license.py --selftest` / plain | head | pass / pass, rc 0 |
| `check_comments.py` / `--selftest` | head | `34 code files and all mutation fragments pass`, rc 0 |
| `check_port_contracts.py --selftest` | head | name-removal and 20 meaning-removal controls refused; contracts present, rc 0 |
| `traceability.py --selftest` | head | 45 requirements, 151 test declarations; 8 binaries, 425 instances; every control caught, rc 0 |

The first traceability attempt ran under `python3 -I`, which cannot import the sibling module (rc 1). The next attempt had no GoogleTest prefix, so `cmake` failed (rc 1). Both were harness errors, not results. The row above is the rerun with the pinned GoogleTest prefix that `docs/VERIFICATION.md:96` documents. All three attempts are in the log.

**Mutation and fault probes.** Each probe edits `scripts/check_privacy.py` at the head in its own clone.

| Probe | Change | Self-test | Gate | Reading |
|---|---|---|---|---|
| M1 | drop the exemption | `fail two-line-merge` | fails on `d7e6a2a1` | unchanged from round 1 |
| M2 | the exemption also skips the identity check | `fail two-line-merge-foreign` | pass | unchanged |
| M3 | one-line rule off for every commit | `fail web-flow-two-lines, holder-two-lines, two-line-merge-near-miss` | pass | the new control also bounds it |
| M4 | match on the 8-character prefix | `fail two-line-merge-near-miss` | pass | **killed: S1 resolved** (survived in round 1) |
| M5 | two-line controls use the zero id | `fail two-line-merge` | pass | unchanged |
| M6 | skip the content scan for the exempt id | 14 pass | pass | survives; S2 not taken, as the PR body states |
| M7 | the near-miss control uses the exact id | `fail two-line-merge-near-miss` | pass | the near-miss control really changes the id |
| M8 | match ignores the last digit (`[:39]`) | `fail two-line-merge-near-miss` | pass | killed |
| M9 | match on the last 8 characters only | 14 pass | pass | survives (S5) |
| M10 | drop the new log line | 14 pass | pass, no #29 line | the log line is informational and not pinned (acceptable) |
| P1 | add a pattern for the exempt commit's body text | 14 pass | `d7e6a2a1...: restricted content`, rc 1 | the content scan reaches the exempt commit |
| P2 | change the web-flow committer email | 14 pass | `d7e6a2a1...: unexpected identity` (and 7 other web-flow commits), rc 1 | the identity check reaches the exempt commit |

**Direct boundary calls on the head `commit_errors`** (unchanged from round 1):
- The exempt id passes with two lines under the web-flow pair and under the holder pair. Under the reversed pair it fails on identity.
- These ids all fail the one-line rule:
  - the abbreviated id;
  - the upper-case id;
  - the id with its last digit changed;
  - the id with a trailing newline;
  - the zero id;
  - the first parent `70936b77`.
- The exempt id with an empty message passes. This has no impact: the sha1 id binds the immutable message of `d7e6a2a1`, so no other message can carry that id.

**Hosted evidence at the exact head** (`receipts/head-check-runs.json`, `receipts/hosted-gate-summary.txt`):
- The runs are 42472273572 (push) and 42472276375 (pull_request).
- Both `quality` jobs (128705621127 and 128705629655) logged `git checkout --progress --force 62d24a37...`.
- Both executed every gate with rc 0, from `entity-golden` through `privacy-selftest`, `privacy`, the GCC and clang-sanitizer builds and tests, coverage, static analysis, `mutation`, `mutation-controls` and `graphs`.
- `bare-metal` succeeded in both runs.
- No context was skipped. Hosted and act acceptance remain the manager's.

**Clone integrity** after the probes (`receipts/clone-integrity.txt`, `scripts/clone_integrity.sh`). I never edited the review clone.
- HEAD and tree are exact.
- Porcelain status is empty, ignored files included.
- The index (mode, blob, path) equals the HEAD tree.
- Every worktree blob hash matches HEAD.
- The four changed files are the blobs `6790ee6`, `8775f77`, `d6f46b4` and `28976bd`, all mode 100644.
- The repository has no gitlinks and no `.gitmodules`, so no submodule gitlink is required.

## Round-1 findings at this head

### F1 - MINOR - Docs, Conformance - RESOLVED

I re-read each location against `scripts/check_privacy.py`. Line 17 is `TWO_LINE_MERGES`. Line 32 is the identity check, still applied to every commit except the owner squash. Line 34 is the exact-id set lookup for the one-line rule. Line 79 is the scan, still applied to every commit.

- **`docs/VERIFICATION.md:42`.** It says the exact merge of #29 passes with a two-paragraph message under its GitHub pair. It also says the same message fails under a foreign identity and under an id one digit away. These match the controls at `check_privacy.py:53-55` and `:61`. The near-miss changes the last digit.
- **`docs/IMPORT.md:133-137`.**
  - `:133`: "exempts only that exact commit" became "exempts that exact commit", so the owner-squash sentence no longer claims it is the only exception.
  - `:135-137` cites the full id `d7e6a2a1...96` and states the one-line rule only.
  - It says identity and content are still checked, and that main's published history is not rewritten.
- **`CHANGELOG.md:5`** (Unreleased): "Exempt the merge of #29 from the one-line message rule by its exact commit; its identity and content are still checked." It follows the precedent format.
- **Verification step:**
  - `check_privacy.py` and `--selftest` pass.
  - `check_port_contracts.py --selftest` and `traceability.py --selftest` pass.
  - `check_comments.py` and its self-test pass.
  - Hosted runs at this head pass.

### S1 - SUGGESTION - Tests, Robustness - TAKEN, RESOLVED

The control `two-line-merge-near-miss` (`check_privacy.py:55,61`) kills M4 (prefix match) and M8 (last digit ignored). M7 shows that the control depends on the id change. A single near-miss leaves one class open; see S5.

### S2 - SUGGESTION - Tests - NOT TAKEN, RETAINED

`check_privacy.py:67-69,79`. M6 still survives: a change that skips `scan` for the exempt id passes the self-test and the gate. The PR body declines S2 because `scan` has no self-test control for any commit today. That is a fair scope boundary: the structure predates this PR, and P1 shows that the scan does reach the exempt commit at this head. The suggestion stays open, does not block, and could go in a separate change.

### S3 - SUGGESTION - Robustness, Docs - TAKEN, RESOLVED

`check_privacy.py:82-83` prints `privacy: exact #29 merge one-line exception; identity and content checks remain enabled` only when the exempt id is in `rev-list HEAD`. It printed at the head and in every head-based probe clone, and not in the first-parent history `70936b77`. M10 shows it is not pinned. That is acceptable for an informational line, and it matches the owner-squash line.

### S4 - SUGGESTION - Docs (comment judgement) - TAKEN, RESOLVED

`check_privacy.py:16`: "Merge of #29 (d7e6a2a1) was recorded with a second message paragraph; it is exempt from the one-line rule only, since main's published history is not rewritten."
- It states the behaviour and the reason, and cites #29. `d7e6a2a1` is a commit id, not an issue-comment ID.
- It contains no bench lane label, lane name, review round, reviewer ID or issue-comment ID, so it is **not RESIDUE** under the comment rule.
- No requirement ID exists to cite.
- `check_comments.py` passes.

## New items at this head

### S5 - SUGGESTION - Tests, Robustness

- **Where:** `scripts/check_privacy.py:55,60-61`. Probe M9.
- **Issue 1:** the one near-miss control changes only the last digit. A broadened match that still includes the last characters survives the self-test and the gate. M9 is an example: it matches on the last 8 characters only.
- **Issue 2:** the controls pick the exempt id with `next(iter(TWO_LINE_MERGES))`. While the set has one member this is exact. If a second id is added, the choice depends on string-hash order, and only one member would be tested.
- **Suggestion:**
  - Add a second near-miss that changes the first digit.
  - Run the `two-line-merge*` controls for every member of `TWO_LINE_MERGES`.
- **Verification:** M9 fails the self-test, and each member of the set is named in the self-test output.

### S6 - SUGGESTION - Docs

- **Where:** `docs/VERIFICATION.md:42`, last clause: "and so does a multi-line message on any other commit."
- **Issue:**
  - In context, "other" refers to the two exceptions the row has just named, so the claim is correct. This is why it is not a finding.
  - But the sentence before it covers only the merge of #29. A reader could take "other" to mean "other than that merge", and the owner-squash control (`check_privacy.py:44`) does pass a multi-line message.
- **Suggested wording:** "and so does a multi-line message on any commit other than these two."

No RESIDUE item is raised. The added doc lines, the changelog entry and the code comment contain no lane label, round, reviewer ID or comment ID.

The PR body still describes the round-1 change as "Two new self-test controls" in its Change section. Its Round 2 section adds the near-miss control and states the total of 14. Read together, the body is accurate, so this is not raised as a finding.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CONTRIBUTING.md:14,19`; `docs/IMPORT.md:128-139`; `docs/VERIFICATION.md:41-42`; `CHANGELOG.md:3-5`; PR body (Round 2 section, S2 statement); `62d24a37` commit object (holder pair, one-line message); `d7e6a2a1` commit object; F1 resolved | R797-2 (delta); R797-1 (unchanged authorities) | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| RTL | CLEAN (not applicable) | 0 tracked HDL files; the delta is one Python gate script and three Markdown files; no hardware or timing claim | R797-2 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Robustness | CLEAN (S5 suggestion open) | `check_privacy.py:16-17,30-36,72-98`; P1/P2 fault probes; first-parent history run (log line absent); boundary calls (abbreviated, case, near-miss, newline, parent, reversed pair, empty message); exact-set lookup fails closed | R797-2 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Tests | CLEAN (S2 retained, S5 open, both suggestions) | `check_privacy.py:39-65`; head self-test 14 pass, prior head 13, main 11; M1-M10 mutations (M4 and M8 now killed, M6 and M9 survive); privacy, licence, comments (and self-test), port-contracts and traceability self-tests; hosted runs 42472273572 and 42472276375 (all gates rc 0); author `author-r2/gates.log` matched | R797-2 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |
| Docs | CLEAN (S6 suggestion open) | `docs/VERIFICATION.md:42`; `docs/IMPORT.md:133-137`; `CHANGELOG.md:5`; source comment `check_privacy.py:16` (rule-compliant); log text `:83`; PR body; author manifest hashes and `round2.diff` byte identity | R797-2 | 62d24a37c4b81a78edda2721dd8611d753b2bc8e |

## Real limits

- My gate runs used local Python 3.14.8 and git 2.56.0, not the hosted Ubuntu 24.04 image. I cite the hosted runs at this head as read from their logs; I did not reproduce them.
- I did not run the full validation driver, the GCC and sanitizer builds, the mutation campaign or the RV32 bank. The delta cannot reach C sources or their tests. The traceability self-test built the test binaries and reconciled their registration. Hosted runs at this head report every gate at rc 0.
- The pinned simulator was not needed: the delta contains no HDL.
- The author evidence commit is unsigned. Its integrity rests on the manifest sha256 values and the byte-identical diff, both of which I checked.
- No manager source bank ran at this head, and none is claimed or inferred. The author's receipts are source-head evidence only.
- Physical calibration NOT RUN. No hardware claim is made.
- I did not build or examine the merge candidate against live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`.

## Pending manager duties

- At the merge turn, build and validate the current-dev merge candidate (builder and native banks), and link the receipts on the PR. `privacy` must pass on the candidate, whose history includes `d7e6a2a1`. The `#29 merge` log line should appear there.
- Own hosted and act acceptance.
- Obtain the second independent review that merge requires.
- No RESIDUE item to carry. S2, S5 and S6 are optional suggestions for the author.

R797-2 FINISHED
