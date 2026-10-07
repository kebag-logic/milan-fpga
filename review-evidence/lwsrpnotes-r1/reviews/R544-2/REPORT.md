[R544] POSITIVE - exact head f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152

# R544-2 internal independent review: kebag-logic/lwSRP PR #15 (issue #16)

- Reviewer role: internal independent reviewer, cleared context, own detached clone.
- Exact head `f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152`, tree `e7c4cf6a8fb382e5260f5fc9674c21c286289841`. The PR head and remote `refs/pull/15/head` were both confirmed at this head (`receipts/public-inventory.txt`).
- Source base `a4cbe41de1c80d43f26e0d348cbdb45075273a4f`. The delta under review is one documentation commit, `f680e3c8`, on `ced667d8`.
- Verdict: POSITIVE. The three prior MINOR count findings are resolved at this head, and every changed figure matches an exact-head measurement. No MINOR, MAJOR or BLOCKER is open. One RESIDUE (PR-body wording) and four SUGGESTIONS are recorded.

## Reconstruction order

1. Read `CONTRIBUTING.md`; the repository has no `AGENTS.md`. Then read `README.md`, `doc/tester.md`, `doc/manager.md`, `doc/developer.md` and `doc/tools/README.md`.
2. Issue #16 has four frozen acceptance items: a note 4 test for the VP and VO cells in both PointToPointMAC values; a note 5 test for AA/rIn! in both values; a reversal that fails each test in both profiles; and no change to `src/`. The issue has no comments, so there are no further scope decisions. Read the PR body and the R544-2 review-start notice.
3. Authority: IEEE 802.1Q-2018, clause 10.7.7, Table 10-3, read from a local copy (digest and paraphrased oracle in `receipts/standard-check.txt`). Interfaces: `mrp_port_configure` (`src/include/shish_lan/mrp.h:307`) and the Applicant guard and table (`src/core/mrp_mad.c:506-512`, `:206-212`).
4. Read `git diff a4cbe41d..f680e3c8`, the delta `ced667d8..f680e3c8`, the history, and the merge resolution (`receipts/diff-and-scope.txt`, `receipts/history-merge.txt`).
5. Read the public evidence at milan-fpga `03b25f53`, `review-evidence/lwsrpnotes-r1`. Both published files match their manifest digests. They report results for `ced667d8`, so they predate this head. The issue and PR contain no separate manager evidence comments.
6. Recorded the independent verdict and ledger (`receipts/independent-verdict-before-prior-findings.md`). Only after that were the R544-1 and R545-1 findings read.

## Delta at this head

`f680e3c8` changes only these three lines:

| Line | Before | After |
| --- | --- | --- |
| `doc/manager.md:56` | 86 tests, 19885 assertions | 87 tests, 19901 assertions |
| `doc/manager.md:57` | 86 tests, 19873 assertions | 87 tests, 19889 assertions |
| `doc/tester.md:193` | 93 reversals | 94 reversals |

Nothing else changed: `git diff --stat ced667d8 f680e3c8` lists only these two files, with 3 insertions and 3 deletions. The commit has one subject line, no body or trailer, no whitespace errors and no non-ASCII text.

Across the whole PR, the `src/` diff from `a4cbe41d` is empty, and the `src` tree ID is identical at base and head. The `ced667d8` merge resolved the conflicts in the README count and the REQUIRED_FAILURES list by keeping both sides. It also aligned `doc/tester.md:29,70`; `receipts/history-merge.txt` has the exact resolution diff.

## Executed evidence (exact head unless marked)

| Check | Result | Receipt |
| --- | --- | --- |
| Profile OFF: configure, build, ctest, unit runner, behave, dry run | All rc 0. `Running "main" (87 tests)`; `Completed "main": 19901 passes`. Behave: 3 scenarios and 10 steps passed; dry run 3 untested. | `receipts/suites/profile-OFF.log` |
| Profile ON (`LWSRP_MILAN=ON`), same commands | All rc 0. 87 tests; 19889 passes. Behave: 3 scenarios and 10 steps passed. | `receipts/suites/profile-ON.log` |
| Runtime test count, independent of the runner header (reporter wrap on an exported copy) | OFF: 87 tests, 19901 passes. ON: 87 tests, 19889 passes. | `receipts/counts/count-{OFF,ON}.log` |
| Count controls at base `a4cbe41d` and pre-delta `ced667d8` | Base: 86 tests, with 19885 (OFF) and 19873 (ON) passes. `ced667d8`: 87 tests, with 19901 and 19889. The +16 per profile equals 8 assertions × 2 link modes in the new test. | `receipts/counts/count-{base,ced}-*.log` |
| `tests/check_reversals.py`, OFF | `Reversals: 94; failures: 0`; 94 KILLED, 0 SURVIVED; restored build and check rc 0 | `receipts/suites/reversals-OFF.log` |
| `tests/check_reversals.py --milan ON` | `Reversals: 94; failures: 0`; 94 KILLED, 0 SURVIVED; restored build and check rc 0 | `receipts/suites/reversals-ON.log` |
| `CASES` inventory | 93 at base and 94 at head, all labels unique. All 61 REQUIRED_FAILURES keys name an existing case. The guide figure is 94 at head. | `receipts/reversal-case-inventory.txt` |
| Note reversals' named failures, both profiles | `point-to-point-condition` fails both note tests. `pending-point-to-point-condition` fails `pending_applicant_joinin_obeys_note_four`. `shared-in-condition` fails `applicant_receive_conditions_follow_link_mode`. Every build is rc 0 and every ctest is rc 8. | `receipts/reversals/{OFF,ON}/` |
| Reviewer probes, 6 × 2 profiles | The control passes. Four guard faults are killed by the named note tests in both profiles: drop VO, ignore link mode for note 4, ignore link mode for note 5, and invert note 4. The carried S1 fault survives in both profiles. | `receipts/probes/results.json` |
| ASan and UBSan, both profiles | rc 0, no report; 19901 and 19889 passes | `receipts/sanitizer/` |
| Embedded check; freestanding OFF and ON | rc 0. Both profile links and dispatch probes pass; 7 sources, 0 failures. | `receipts/suites/{embedded,freestanding-*}.log` |
| Isolated codec command from `doc/tester.md:89-99` | rc 0; 9 tests, 1690 passes, matching `doc/tester.md:101` | `receipts/codec-isolated-run.log` |
| Documentation checks | All rc 0: 975 sentences, 0 over the limit; 0 unlinked references; 79 self-test cases; authenticated and anonymous link checks each found 354 local and 20 external links with 0 failures; 27 graphs rendered | `receipts/doc-checks/` |
| Count statements in tracked Markdown | Every unit figure reads 87/19901 (OFF) or 87/19889 (ON), and the reversal figure reads 94. No stale `86 tests`, `19885`, `19873` or `93 reversals` remains. | `receipts/doc-count-statements.txt` |
| Hosted contexts at the exact head | 0 check runs, 0 statuses, 0 workflow runs, and no workflow directory. The aggregate "pending" only reflects zero contexts. Nothing executed and nothing was skipped. | `receipts/hosted-exact-head.txt` |
| Clone integrity after all probes | HEAD, tree and index tree are exact. All 60 tracked blobs match bytes and modes (59 × 100644, 1 × 100755). The repository has 0 gitlinks and no `.gitmodules`. Status is clean, including ignored files. | `receipts/clone-integrity.txt` |

## Findings

### R544-2-R1: RESIDUE (lens: Docs): PR body scope wording

- Artifact: PR #15 body, fourth bullet, "Tests only, no source change." The same text appears in the published `author/PR-BODY.md` (sha256 `0ce5ed80…`).
- Evidence: the PR also changes recorded totals in `README.md:45`, `doc/manager.md:56-57` and `doc/tester.md:29,70,193` (`receipts/diff-and-scope.txt`). "No source change" is accurate: the `src/` diff is empty.
- Impact: wording only. No measurement, figure, test, code or conformance claim changes.
- Exact fix: "Tests and their recorded totals in `README.md`, `doc/manager.md` and `doc/tester.md`; no `src/` change."
- Verification: re-read the PR body against `git diff --stat a4cbe41d..<head>`.

### Suggestions (non-blocking)

- R544-2-S1 (Tests, Conformance; carries R544-1-S1). Making note 4 apply to every Applicant state (guard set to `true`) still passes all 87 tests in both profiles (`receipts/probes/results.json`, `note4-all-states`). Table 10-3 makes AA rJoinIn! → QA unconditional (`receipts/standard-check.txt`), so this over-application goes undetected. It is outside issue #16's frozen acceptance, which covers only VO and VP. A follow-up point-to-point control asserting AA rJoinIn! → QA, plus a reversal, would close it.
- R544-2-S2 (Docs; carries R544-1-S2). The VO and AA/rIn! cells are covered by the pre-existing `applicant_receive_conditions_follow_link_mode`. Only the VP cell has a new test. The PR body or issue-closing note could map each cell to its test. Acceptance item 1 is still met by the two named tests together.
- R544-2-S3 (Tests). No reversal isolates the VO cell. `point-to-point-condition` disables the whole note 4 guard, and `pending-point-to-point-condition` drops only VP. A reviewer probe that drops only VO is killed by `applicant_receive_conditions_follow_link_mode` in both profiles. A matching named reversal would therefore be cheap to add.
- R544-2-S4 (Tests, Docs). The recorded unit and reversal totals are hand-maintained in six statements (`README.md:45`, `doc/manager.md:56-57`, `doc/tester.md:29,70,193`), and no documentation check compares them with the runner output or `len(CASES)`. That gap allowed the stale counts found at `ced667d8`. A small check comparing the stated totals with the runner summary and the `CASES` list would prevent a recurrence.

## Prior public review findings at this head

| Prior finding | Disposition | Evidence at f680e3c8 |
| --- | --- | --- |
| R544-1-F1 MINOR: `doc/manager.md:56-57` stale 86/19885/19873 | RESOLVED | Lines read 87/19901 and 87/19889; runtime counts are 87 tests with 19901 (OFF) and 19889 (ON) passes |
| R544-1-F2 MINOR: `doc/tester.md:193` stale 93 reversals | RESOLVED | Line reads 94; `len(CASES)` = 94; both drivers report `Reversals: 94; failures: 0` |
| R545-1-F1 MINOR (shared): the same three figures | RESOLVED | All three corrections are present; doc checks pass; no stale figure remains (`receipts/doc-count-statements.txt`) |
| R544-1-S1 SUGGESTION | RETAINED as R544-2-S1 | Reproduced at this head in both profiles |
| R544-1-S2 SUGGESTION | RETAINED as R544-2-S2 | Test bodies unchanged since `ced667d8` |

The independent pass found the same POSITIVE result before these findings were read (`receipts/independent-verdict-before-prior-findings.md`).

## Acceptance (issue #16) at this head

| Item | Status | Evidence |
| --- | --- | --- |
| 1. VP and VO cells, both values (note 4) | Met | `tests/unit/integration_test.c:327-335` (VO) and `:350-366` (VP) |
| 2. AA/rIn!, both values (note 5) | Met | `tests/unit/integration_test.c:336-346` |
| 3. A reversal fails each test, in both profiles | Met | `tests/check_reversals.py:74-80,185-188`; `receipts/reversals/{OFF,ON}/` |
| 4. No change in `src/` | Met | `receipts/diff-and-scope.txt` |

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Table 10-3 rJoinIn!/rIn! rows and notes 4–5 compared with `src/core/mrp_mad.c:206-212,506-512`; the three encoded cells and their PDU bytes; empty `src/` diff; 5 guard probes × 2 profiles | R544-2 | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| RTL | CLEAN | Not applicable: host C library; tracked tree contains no HDL; `src/` unchanged; pinned simulator not needed | R544-2 | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Robustness | CLEAN | ASan and UBSan in both profiles; per-iteration create and destroy in the new test; merge resolution; reversal driver restore and baseline contract; clone byte integrity after probes | R544-2 | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Tests | CLEAN | ctest, unit runner and behave in both profiles; runtime test counts at head, `ced667d8` and base; 94 reversals × 2 profiles with named failures; 12 probe runs; embedded, freestanding and isolated codec runs | R544-2 | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |
| Docs | CLEAN (RESIDUE R1 recorded) | `f680e3c8` delta; every count statement in `README.md`, `doc/manager.md` and `doc/tester.md`; `CONTRIBUTING.md` commit and documentation rules; PR body; published evidence; all `doc/tools` checks | R544-2 | f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152 |

## Real limits

- The reviewer built the unit framework from the public cgreen 1.6.3 tag in packet scratch, not with the manager's prefix. Counts match the manager's measurements exactly (`receipts/tool-versions.txt`).
- The reversal driver uses Release builds and the profile runs use Debug; both were exercised. The driver has no jobs option, so the two profiles ran concurrently.
- The probes plant single faults in the note 4/5 guard only. They are not exhaustive mutation testing of the Applicant table.
- The full parent, PP, gPTP, Yosys and builder banks, containers, act and host CI were not run. The manager's source static/builder and native bank passes are manager evidence, not reviewer execution.
- Physical calibration was NOT RUN. This is a host-only library review: field skips and host passes are not hardware proof.
- The final current-dev candidate (source base `a4cbe41d`, live dev `e21c1ca0`) was not built here. This review certifies the source head only.
- Local absolute paths in receipts are replaced with `$PACKET`, `$CHECKOUT`, `$DATA` and `$HOME`.

## Pending manager duties

- Carry R544-2-R1 to the residue checklist (exact fix above).
- Decide whether S1, S3 and S4 become follow-up issues.
- The published evidence (`F4-ROUND5-EXCERPT.md`) names `ced667d8`. Its figures still hold at `f680e3c8` per this review, but the manager should publish exact-head evidence or state that equivalence.
- Build and accept the final current-dev candidate at the merge turn. The manager also owns hosted and act acceptance; this repository currently runs no hosted contexts.
- Obtain the second independent positive review and meet the full completion bar before any merge.

R544-2 FINISHED
