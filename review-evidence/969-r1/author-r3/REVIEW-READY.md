[A817] REVIEW READY
Commit: c113018d3cd4e70a7d3b66940a3a88fb93f0421a (branch `pf-969-1`, pushed as `969-srp-kept-talkers`, PR #971; round 3, answering R885-2 and R886-2 at `e816c74d`)

Changed (the CPU budget grader and three documents only; no firmware, RTL, mailbox-contract or CPU budget bound change; nothing re-measured):
- **R885-2-F1 / R886-2-F1 (MINOR): a grade with incomplete or missing evidence is a finding, never clean.**
  - `kept_grade.held` reads THE SHARE from the logs it grades (`grade.pass_share`). `over_share` separates work passes from idle runs, so the reader no longer raises on an idle entry.
  - `run.py`'s `Disposition` and the standalone entry point both grade through it, and neither reads a `<group>.json`. A stale, empty or absent result file neither clears THE SHARE nor hides a pass over it.
  - A log that did not finish (an incomplete simulation, a trap or a bus error, `grade.refuse_run`) is a finding, and so is one that does not parse.
  - Every probe `kept_window` makes at the point's interface count must be marked, and no other. A kept probe with no bound record of its own interface is a finding; the comparison is never skipped.
  - An idle run over THE SHARE is a finding in either group. An idle pass makes no registration, so none is owed.
- **R885-2-F4 (MINOR): the self-test covers every held condition.**
  - `--selftest` now has 19 checks, run through `held`, `Disposition` and the standalone `main`: unfinished log, unmarked probe, foreign probe, missing record, missing mate, kept over bound, srp-kept work pass over THE SHARE (beside a stale and an empty result file), idle run, build-one over its cost in either group, a group graded alone, a pair with a broken log, an absent log, an unparsable log, plus the unit's owed lines.
  - The README's description now matches what the checks execute.
- **R885-2-F2 (MINOR): one counted population.** Base `dd163e41` against the final firmware, by position in the hot section, at 1x1/1if and 8x8/1if: 152 of the hot list's 261 functions change in offset or size. That is `reset_interface`, which grows 16 B at its own offset, and the 151 after it, each 16 B later at its own size; the 109 before it do not move. The CPU budget images show 155 = 1 + 154. `SPLIT_CONTROL_MEMORY.md` and the PR body now state this, and the new census receipt replaces round 2's count.
- **R885-2-F3 (MINOR): the frame measured.** The LeaveAll itself carries no kept value. Its txLA! takes each observed attribute to LO with only an optional [s] (IEEE 802.1Q-2018 Table 10-3). The next MRPDU's tx! sends In from LO (s, 10.7.6.5), and that build encodes the kept values: 2 at 1x1/1if, 9 at 8x8/1if. `mrpdu_grade`'s LeaveAll row grades the LeaveAll's owner and deadline. `kept_window.py`, the harness README and the PR body say so.
- **Residue (both reviews):** `kept_grade.py:58` now reads "(#969, ruling of 2026-11-22, option 1)", and `kept_window.py:33` reads `kept_grade.Disposition`.

Validation (at `c113018d` unless named):
- `kept_grade.py --selftest`: PASS, 19 checks.
- Planted guards: each of 20 grader guards is removed in memory and the self-test run on the result. All 20 are caught and none escape; each has its failing check's words in the receipt.
- R886-2's grader probe, unchanged: valid-within exits 0. valid-over, absent-result, empty-result, missing-share, missing-mate and stale-result each exit 1, each with its finding named.
- R885-2's grader probe and self-test-coverage probe, adapted only to the changed signatures (the diffs are published): every case passes. complete-clean exits 0; over-share, missing-json, empty-json and missing-share exit 1; build-one over its cost, a single group, the OWED lines and the idle-only row all pass; 3 of 3 plants are caught.
- Regrade of round 2's measured runs of both groups (images at `5dba2089`; no firmware source has changed since `f02d44cd`):
  - `kept_grade.py` passes at 1x1/1if and 8x8/1if with the same figures as round 2. kept <= bound: 34,497 / 32,224 / 36,859 against 38,956, and 137,352 / 68,692 / 142,909 against 153,208.
  - THE SHARE: no srp-kept work pass or idle run is over it, out of 1,910 and 1,911 work passes. srp-bound's 224,540-cycle pass at 8x8/1if is OWED #977.
  - Builds are within their stated costs.
  - `run.py`'s `Disposition` on the same logs: 5 and 7 STATED lines and 0 and 1 SHARE lines, all owed, 0 findings.
- `check_py_idiom`: PASS at `c113018d`. At `d1f35329` it refused the self-test's length; `c113018d` splits the function.
- Docs workflow, 103 commands, run on a clean clone: 99 PASS. The 4 rows that need the CI environment refuse, as on the base.
- `run.py --self-test` on a clean clone: 0 failures, with 295 mutants caught as in round 2 (06:23 to 07:09).
- Not re-run, because no input they read changed: the firmware gate (4 shards), coverage, ledger, twin and routes. Their round-2 receipts stand.

Acceptance criteria: unchanged from round 2. The host model meets them (`Early.S13`, `Early.S14`, `SrpEarlyTalker`; 16 early plants at 1x1 with one and two interfaces and at 8x8/1if). The bench re-run after merge is the manager's.

Open risks/questions:
- The standalone grade proves that the logs it reads finished and meet every condition. It does not prove which head built them; `run.py` records that in the build's `build.json`.
- Unchanged from round 2: the share condition is held on `srp-kept`. srp-bound's own pass over THE SHARE at 8x8/1if is owed to #977.
- The bench re-run after merge is the physical check; there was no bench access here.
