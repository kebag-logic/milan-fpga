# HANDOFF r3: [A817] #969 / PR #971, answering R885-2 and R886-2 (both NEGATIVE, MINORs only, at `e816c74d`)

Status: **REVIEW READY** (07:15 CET 2026-11-23) at `c113018d`. Every gate of the round is recorded below; nothing of
this lane is running. REVIEW READY posted: #969 issuecomment-7093069092 (text: REVIEW-READY.md).
Checkout verified clean at `e816c74d` after the 00:39 host crash (no uncommitted change, no untracked file).

Lane: `/data-2/milan/lanes/fix-969`, branch `pf-969-1` (pushed by the manager as `969-srp-kept-talkers`), from
`e816c74d`. Local commits only; nothing pushed. No firmware, RTL, mailbox-contract or CPU budget bound changed: the
round touches only the CPU budget grader `kept_grade.py`, `kept_window.py`'s docstring, the harness README and one
line of `SPLIT_CONTROL_MEMORY.md`. Nothing was re-measured: the grader regrades round 2's runs of both groups.

## Findings and their fixes

| Finding | Cause | Fix | Evidence |
|---|---|---|---|
| R885-2-F1 / R886-2-F1 MINOR: incomplete, missing or stale share results accepted as a clean grade; a missing bound mate skipped; an idle entry crashed the reader | THE SHARE was read from `<group>.json` beside the log, defaulting a missing field to "no overrun"; a failed log was not refused; `held` skipped a kept probe whose mate was absent; `over_share` read `start_sys` from idle entries | `held` reads THE SHARE from the logs it grades (`grade.pass_share`, `over_share` splitting work passes from idle runs), refuses an unfinished log (`grade.refuse_run`), requires every probe kept_window makes at the point's interface count and no other, each with its record, and finds a kept probe with no same-interface bound record. An idle run over THE SHARE is a finding in either group (an idle pass makes no registration, so none is owed). The standalone entry point never reads a result file; a log that does not parse is a finding | R886-2's probe unchanged and R885-2's adapted: every required case fails by name, the controls hold (receipts/grader/REVIEWER-PROBES-c113018d.txt) |
| R885-2-F2 MINOR: the hot-function count contradicts its receipt | round 2 wrote "152 after reset_interface", but its census (152 at another offset or size) included reset_interface itself | census by position, base `dd163e41` against the final firmware, at both points: 152 changed = `reset_interface` resized at its own offset + 151 after it, each 16 B later; 109 before it unmoved. The CPU budget images: 155 = 1 + 154 | receipts/budget/hot-section-census.txt (base platform images rebuilt from the base clone; the head's sha256 equals round 2's image) |
| R885-2-F3 MINOR: the described LeaveAll frame is not the one carrying the kept values | the text said the build sending the LeaveAll carries the kept attributes | the LeaveAll carries none (txLA! takes each observed attribute to LO with an optional [s], IEEE 802.1Q-2018 Table 10-3); the next MRPDU's tx! sends In from LO (s, 10.7.6.5), and that build encodes the kept values (2 at 1x1, 9 at 8x8); mrpdu_grade's LeaveAll row grades the LeaveAll's owner and deadline | round 2's decoded receipt leaveall-build-with-the-kept.txt; Table 10-3 read from the standard |
| R885-2-F4 MINOR: the self-test does not plant every held-condition breach | 5 checks; no build pass, no pair requirement, no standalone guard | `--selftest` 19 checks through `held`, `Disposition` and the standalone `main`; a plant script removes each of 20 guards in memory and every one is caught | receipts/grader/kept_grade-selftest-c113018d.txt, kept_grade-plants-c113018d.txt |
| R885-2-R1 / R886-2-R1 RESIDUE | a review-round label in a source comment | `kept_grade.py:58` "(#969, ruling of 2026-11-22, option 1)" | the diff |
| R885-2-R1 / R886-2-R2 RESIDUE | `kept_grade.disposed` does not exist | `kept_window.py:33` `kept_grade.Disposition` | the diff |

## Changes (file:line at `c113018d`, reason)

| Where | Reason |
|---|---|
| `tb/verilator/ctrl_service_budget/kept_grade.py:3-35` | the module docstring states the six conditions as graded (logs, records, kept <= bound, the share from the logs, builds, pair) |
| `kept_grade.py:58` | the residue wording |
| `kept_grade.py:66-70` `probes` | each group's probe names at the interface count, from `kept_window.groups` itself |
| `kept_grade.py:85-99` `dearest`, `over_share` | only the probes the point makes; THE SHARE from the log, work passes by their start and idle runs by their index (F1's idle crash) |
| `kept_grade.py:102-162` `held` | an unfinished log refused (`:111`); a missing probe (`:115`) or a foreign one (`:116`) found; a kept probe with no same-interface bound record found, never a skipped comparison; srp-kept's work pass over THE SHARE found (`:147`), srp-bound's owed, any idle run over it found (`:151`) |
| `kept_grade.py:165-170` `point_shape`, `:172-202` `Disposition` | run.py's disposition grades the same logs through `held` (no result file's share) |
| `kept_grade.py:205-224` `grade_dir`, `:395-418` `main` | the standalone grade: a missing or unparsable log is a finding; no result file is read |
| `kept_grade.py:227-392` `Synthetic`, `selftest_held`, `standalone`, `selftest_files`, `selftest` | 19 checks (F4), each function within the idiom gate's 100 lines |
| `kept_window.py:17-22, 33` | F3's LeaveAll and next-MRPDU description; the helper's name |
| `tb/verilator/ctrl_service_budget/README.md:769-791` | F3; the conditions as graded, THE SHARE from the logs, the self-test's coverage (F1, F4 docs) |
| `docs/design/SPLIT_CONTROL_MEMORY.md:693` | F2's counted population at both one-interface points |

## New checks (planted defect, failing words)

`receipts/scripts/plant_kept_grade.py` removes each guard in memory and runs kept_grade's own self-test on it.
All 20 are caught; the unplanted self-test is 19/19.

| Plant | Caught by (failing check's words) |
|---|---|
| log-refusal-removed | an unfinished srp-kept log measures nothing |
| never-marked-unfound | a probe the point makes that is never marked is a finding |
| foreign-probe-unfound | a kept probe with no bound record of its own interface is a finding |
| no-record-unfound | a probe with no record is a finding |
| unit-never-owed | records past the unit with kept <= bound are owed to #977 |
| mate-missing-skipped | a kept probe with no bound record of its own interface is a finding, never a skipped comparison |
| kept-over-bound-unfound | a kept record one cycle dearer than the bound one breaks kept <= bound |
| share-not-read-from-log | a work pass of srp-kept over THE SHARE is a finding (and 4 more) |
| kept-share-unfound | a work pass of srp-kept over THE SHARE is a finding |
| bound-share-not-owed | srp-bound's is owed to #977 |
| idle-run-unfound | an idle run over THE SHARE in either group is a finding |
| idle-read-as-work (F1's crash restored) | the same, by the exception caught as a finding |
| build-over-cost-unfound | a build of one MRPDU one cycle over its stated cost is a finding in either group |
| pair-not-required | one group graded alone is a finding |
| disposition-ignores-findings | both groups graded together with a condition broken in a log: the finding stays |
| owed-despite-findings | one group graded alone is a finding: nothing is owed |
| share-owed-despite-findings | both groups graded together with a condition broken in a log |
| record-taken-by-the-next-mark | records at the unit by the rule (and 12 more) |
| absent-log-unfound | standalone: a group with no log fails by name |
| unparsed-log-unfound | standalone: a log that does not parse fails by name |

The first plant run at the pre-split head had one escape, `disposition-ignores-findings`; the
`Disposition`-with-a-broken-log check was added for it before the commit.

## Gate table

| Gate | Head | Result | Receipt |
|---|---|---|---|
| `kept_grade.py --selftest` | `c113018d` | PASS, 19 checks | receipts/grader/kept_grade-selftest-c113018d.txt |
| kept_grade plants (20 guards) | `c113018d` | 20 caught, 0 escaped | receipts/grader/kept_grade-plants-c113018d.txt |
| R886-2's probe_kept_grade.py (unchanged) | `c113018d` | valid-within rc 0; valid-over, absent, empty, missing-share, missing-mate, stale rc 1, each by name | receipts/grader/r886-probe/ |
| R885-2's probe_kept_grade.py, probe_selftest_coverage.py (adapted to the new signatures; diffs in scripts/) | `c113018d` | every case PASS: clean rc 0; over-share, missing-json, empty-json, missing-share rc 1; build-one over, single group, OWED lines, idle-only row; 3 of 3 plants caught | receipts/grader/r885-probe/, REVIEWER-PROBES-c113018d.txt |
| kept_grade standalone regrade of round 2's runs (5dba2089 images; firmware unchanged since f02d44cd) | `c113018d` | PASS at 1x1/1if (4 OWED) and 8x8/1if (5 OWED, srp-bound's 224,540-cycle share pass); figures as round 2 | receipts/budget/kept_grade-c113018d-on-5dba2089-*.txt |
| run.py's Disposition on the same runs | `c113018d` | 5 and 7 STATED lines, 0 and 1 SHARE lines, all owed, 0 findings | receipts/budget/disposition-c113018d-on-5dba2089-*.txt |
| Hot-section census | base `dd163e41` vs final firmware | 152 = 1 resized + 151 shifted (platform); 155 = 1 + 154 (CPU budget image) | receipts/budget/hot-section-census.txt |
| check_py_idiom | `d1f35329` | FAIL: long function 10 > 9 (selftest); fixed in `c113018d` | receipts/docs/docs-workflow-d1f35329-FAILED-py-idiom.txt |
| Docs workflow, 103 commands, clean clone | `c113018d` | 99 PASS; the 4 CI-environment rows refuse as on the base | receipts/docs/docs-workflow-c113018d.txt |
| `run.py --self-test`, clean clone | `c113018d` | 0 failures; 295 mutants caught, as round 2's | receipts/budget/harness-selftest-run.py_--self-test-c113018d.log.gz |
| Firmware gate, coverage, ledger, twin, routes | round 2's heads | not re-run: no input they read changed (the round touches only the CPU budget grader and docs) | round2/receipts/ |

## Commits (one-line subjects, no body, no trailers)

| # | Commit | What |
|---|---|---|
| 33 | `71b6b15c` | kept_grade: THE SHARE from the logs, unfinished logs refused, every probe and its mate required, idle runs, the self-test |
| 34 | `102ce631` | harness README and kept_window: the MRPDU after the LeaveAll; the conditions as graded |
| 35 | `d1f35329` | SPLIT_CONTROL_MEMORY: 152 = reset_interface resized + 151 moved |
| 36 | `c113018d` | kept_grade's self-test split for the idiom gate's length |

REVIEW READY c113018d3cd4e70a7d3b66940a3a88fb93f0421a
