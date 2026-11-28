# tsnfix-a867: main gate fixes for kebag-logic/tsn-c-stack

- Clone: `$LANES/tsn-fix`, fresh from GitHub. Branch `main-gate-fixes` from main `5a07d9b7d87298f04b15aa28f0304ec88b0aef81`.
- Head: `a8551cdd3cf715c52cca164a57d6d7f022e62c00`. Tree clean. **Nothing pushed, nothing posted.**
- Scratch, outside the clone: `$LANES/tsn-fix-work`. It holds the builds, worktrees for `ea4af6f`, `a795471`, `c3bff8f` and `5a07d9b`, and the validate work directory.
- Source: the a864 report, `margin-a864/REPORT.md` lines 150-162.

## Commits (holder identity, one-line subjects, no body or trailers)

| Commit | Subject | Files |
|---|---|---|
| `a905c32` | Exempt the merge of #41 from the one-line message rule by its exact commit, and check each exempt merge in the privacy self-test | `scripts/check_privacy.py`, `docs/VERIFICATION.md`, `docs/IMPORT.md`, `CHANGELOG.md` |
| `a8551cd` | Record the measured coverage: adp.c 215/215 lines and 95/95 branches, as #40 removed two zero-seed guards and added one | `tests/coverage.ratchet`, `CHANGELOG.md` |

Nothing under `src/` or `include/` changed.

## 1. Privacy gate

- Before, at main: `5a07d9b7…: commit message must be one line`, rc 1. Receipt: `receipts/privacy/main-5a07d9b.txt`.
- Fix: `TWO_LINE_MERGES` gains the full SHA, with a comment citing PR #41. This follows the same pattern as `d7e6a2a1` for #29. The log line now names both exceptions. The docs and change log are updated as #29's were (`62d24a3`).
- Self-test change. The old code took `next(iter(TWO_LINE_MERGES))`. With two entries, set order is hash-seeded, so each run would check one of the two at random. The exemption controls are now built per exempt merge, in sorted order: pass, foreign identity refused, one-digit near miss refused. The controls for non-exempt commits are unchanged: `web-flow-two-lines` and `holder-two-lines` still require a two-line message on a non-exception commit to be refused. 17 controls, up from 14.
- Plants, from `receipts/tools/privacy_plants.py.txt`: 5 of 5 refused (`receipts/privacy/plants.txt`). The one aimed at the rule you named is a non-exception commit added to the set; `web-flow-two-lines` and `holder-two-lines` refuse it.
- After, on the branch: `privacy: 67 commits, 522 historical blobs, 100 current files; pass` (`receipts/privacy/branch.txt`).

## 2. Coverage ratchet

- Re-measured with the repository's own `scripts/coverage.py`, on a GCC `-DTSN_COVERAGE=ON` build plus ctest, as validate.py's gcc arm does it. The ratchet was regenerated with `scripts/coverage.py --write`, the generator its header names. No row was edited by hand.
- **The coverage gate was not failing on main.** `compare()` checks covered/total fractions, and 215/215 vs 205/205 is 1 = 1. It passes at main with rc 0 (`receipts/coverage/measure-5a07d9b-main.txt`). The defect is a stale record of an "exact" ratchet, not a red gate. The report calls it a base defect, not a failure, so this matches it, but reviewers should know.
- **Wider than the brief.** `--write` also moved `src/acmp.c` from 813/813 and 424/424 to 877/877 and 468/468, only upward. #33 and #34 took it to 847/436 (measured at `a795471`), and #41 to 877/468 (measured at main). I kept it: the file is generated, and hand-editing only the adp row would leave the acmp row stale too. If the reviewer wants an adp-only change, drop that row's hunk.
- **Why `adp.c` branches went from 97 to 95.** Measured at the commits either side of PR 40's merge, `a795471` (205/207 lines, 97/104 arcs raw) and `c3bff8f` (215/217, 95/102). Per-line arc dumps are in `receipts/coverage/arcs-*.txt`:
  - −2: `if (a->rng == 0u)` in `adp_init` (old line 180), both arcs covered (1 and 40316 hits).
  - −2: `if (a->rng == 0u)` in `adp_set_enable` (old line 234), both covered (1 and 132615).
  - +2: `a->rng = x != 0u ? x : 1u;` in the new `leave_down` (line 108), both covered (174255 and 1).

  Net −2 raw arcs. The exclusion rows in `docs/COVERAGE.md` (7 arcs, 2 lines) are unchanged and still match, so the post-exclusion total is 97 − 2 = 95, with nothing uncovered. Lines went up 10, net. `adp.c`'s arc layout at main is identical to `c3bff8f` (`arcs-5a07d9b.txt`). The stated reason is in the change-log entry and in the commit subject.
- `ea4af6f`, the merge just after the last ratchet write `8a1cb08`, measures exactly the old ratchet (205/97, 813/424). That confirms the method reproduces the recorded values.

## Gates

`scripts/validate.py --work … --jobs 16 --graphs`, CI's command, on head `a8551cd`. Toolchain: Clang 18.1.3, clang-tidy 18.1.3, GoogleTest 1.14.0 (pinned in `$VALIDATION_TOOLS`) and mmdc 11.16.0. Result: **28 of 28 gates rc 0**, including privacy, privacy-selftest, coverage and coverage-controls. Mutation: 522 caught, 0 escaped. Receipts: `receipts/validate/`.

## Notes for the reviewer

- `PR-BODY.md` has no tool-attribution footer. CONTRIBUTING keeps assistant product names out of public documents, and the brief bars tool and model names.
- The privacy gate scans untracked, non-ignored files in the clone, so the builds were kept outside the clone.
- Open question for the owner: should the ratchet be exact, refusing any mismatch rather than only drops? The acmp row has been stale since #33, and the adp row since #40, without anything failing.
