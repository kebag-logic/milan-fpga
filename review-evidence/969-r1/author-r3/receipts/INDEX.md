# Receipts index

Generated from the files present (index.py); size in bytes, sha256 prefix, first line.

## budget

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `disposition-c113018d-on-5dba2089-1x1.txt` | 1812 | `72d11171534bd87b` | # run.py's disposition (kept_grade.Disposition at c113018d) on the same run's logs and grades, against that ru |
| `disposition-c113018d-on-5dba2089-8x8-1if.txt` | 2336 | `09be5f39c0f110bd` | # run.py's disposition (kept_grade.Disposition at c113018d) on the same run's logs and grades, against that ru |
| `harness-selftest-run.py_--self-test-c113018d.log.gz` | 42325 | `6022c09effe0d564` |  |
| `hot-section-census.txt` | 3146 | `e475c0d532471c59` | # the hot section (_ctrl_hot_start .. _ctrl_hot_end), base dd163e41 against the final firmware (5dba2089; no f |
| `kept_grade-c113018d-on-5dba2089-1x1.txt` | 2469 | `fb2639cb85937e24` | # kept_grade.py at c113018d (standalone) on the 5dba2089 run of srp-kept and srp-bound at 1x1 (run.py --groups |
| `kept_grade-c113018d-on-5dba2089-8x8-1if.txt` | 2678 | `5e858afa84c4738a` | # kept_grade.py at c113018d (standalone) on the 5dba2089 run of srp-kept and srp-bound at 8x8-1if (run.py --gr |

## docs

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs-workflow-c113018d.txt` | 10077 | `680f7d780fabd0fc` | # the docs workflow's 103 commands (the flip lane's table, the em-dash base dd163e41), quick.sh on a clean clo |
| `docs-workflow-d1f35329-FAILED-py-idiom.txt` | 10017 | `e6b934a1fed8b8e7` | # the same at d1f35329 (before the self-test split): 63-check_py_idiom refused kept_grade.selftest's length (1 |

## grader

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `REVIEWER-PROBES-c113018d.txt` | 1483 | `5265eeac867be88a` | # reviewers' probes run at c113018d: R886-2's probe_kept_grade.py unchanged; R885-2's probe_kept_grade.py and  |
| `kept_grade-plants-c113018d.txt` | 2750 | `bba946161b54f5bc` | # scripts/plant_kept_grade.py at c113018d: each held condition removed in memory, kept_grade's own --selftest  |
| `kept_grade-selftest-c113018d.txt` | 1683 | `672c8d8fca4a2608` | # kept_grade.py --selftest at c113018d |

## grader/r885-probe

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `SUMMARY.txt` | 14659 | `455c9833f5476ba4` | PASS repository selftest: records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed |
| `selftest-coverage-probes.txt` | 172 | `328bf152e7710809` | no-build-over-cost-finding: CAUGHT; 18/19 self-tests pass |
| `stdout.txt` | 14659 | `455c9833f5476ba4` | PASS repository selftest: records at the unit by the rule (27,142 cycles, 285 us), kept <= bound: nothing owed |

## grader/r885-probe/complete-clean

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `rc.txt` | 2 | `9a271f2a916b0b6e` | 0 |
| `srp-bound.json` | 215 | `f5d5eaa4cc975110` | { |
| `srp-bound.log` | 148 | `e97bc8b566b326c3` | MARK 1000000 srp.bound_advertise.if0 |
| `srp-kept.json` | 214 | `054fd04c73392b94` | { |
| `srp-kept.log` | 318 | `aa0bdf3f4ccecf57` | MARK 1000000 srp.kept_advertise.if0 |
| `stderr.txt` | 0 | `e3b0c44298fc1c14` |  |
| `stdout.txt` | 1522 | `d11450cad5d96d80` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |

## grader/r885-probe/complete-over-share

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `rc.txt` | 2 | `4355a46b19d348dc` | 1 |
| `srp-bound.json` | 215 | `f5d5eaa4cc975110` | { |
| `srp-bound.log` | 148 | `e97bc8b566b326c3` | MARK 1000000 srp.bound_advertise.if0 |
| `srp-kept.json` | 300 | `8978c8a789779a08` | { |
| `srp-kept.log` | 319 | `7199f80e04a7a5a2` | MARK 1000000 srp.kept_advertise.if0 |
| `stderr.txt` | 0 | `e3b0c44298fc1c14` |  |
| `stdout.txt` | 1610 | `0acd6695543aa494` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |

## grader/r885-probe/empty-json

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `rc.txt` | 2 | `4355a46b19d348dc` | 1 |
| `srp-bound.json` | 215 | `f5d5eaa4cc975110` | { |
| `srp-bound.log` | 148 | `e97bc8b566b326c3` | MARK 1000000 srp.bound_advertise.if0 |
| `srp-kept.json` | 3 | `ca3d163bab055381` | {} |
| `srp-kept.log` | 319 | `7199f80e04a7a5a2` | MARK 1000000 srp.kept_advertise.if0 |
| `stderr.txt` | 0 | `e3b0c44298fc1c14` |  |
| `stdout.txt` | 1610 | `0acd6695543aa494` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |

## grader/r885-probe/missing-json

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `rc.txt` | 2 | `4355a46b19d348dc` | 1 |
| `srp-bound.json` | 215 | `f5d5eaa4cc975110` | { |
| `srp-bound.log` | 148 | `e97bc8b566b326c3` | MARK 1000000 srp.bound_advertise.if0 |
| `srp-kept.log` | 319 | `7199f80e04a7a5a2` | MARK 1000000 srp.kept_advertise.if0 |
| `stderr.txt` | 0 | `e3b0c44298fc1c14` |  |
| `stdout.txt` | 1610 | `0acd6695543aa494` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |

## grader/r885-probe/missing-share

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `rc.txt` | 2 | `4355a46b19d348dc` | 1 |
| `srp-bound.json` | 215 | `f5d5eaa4cc975110` | { |
| `srp-bound.log` | 148 | `e97bc8b566b326c3` | MARK 1000000 srp.bound_advertise.if0 |
| `srp-kept.json` | 42 | `6b92eab323b47aa5` | { |
| `srp-kept.log` | 319 | `7199f80e04a7a5a2` | MARK 1000000 srp.kept_advertise.if0 |
| `stderr.txt` | 0 | `e3b0c44298fc1c14` |  |
| `stdout.txt` | 1610 | `0acd6695543aa494` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |

## grader/r886-probe

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `grader-absent-result.log` | 1597 | `9c5689e1e495177b` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-absent-result.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-empty-result.log` | 1597 | `9c5689e1e495177b` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-empty-result.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-missing-mate.log` | 1751 | `be5f506d2092d44a` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-missing-mate.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-missing-share.log` | 1597 | `9c5689e1e495177b` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-missing-share.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-probe-results.json` | 1597 | `9006f14b71df70a1` | [ |
| `grader-stale-result-regrade.json` | 148 | `41c6896ebbae99b3` | { |
| `grader-stale-result.log` | 1689 | `0a863b0a6979b044` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-stale-result.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-valid-over.log` | 1597 | `9c5689e1e495177b` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-valid-over.rc` | 2 | `4355a46b19d348dc` | 1 |
| `grader-valid-within.log` | 1508 | `9c36b4db4476734d` | POINT endstation_ax7101_1x1_tdm8, 1 interface(s): shape (1, 2, 2) |
| `grader-valid-within.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `stdout.txt` | 1405 | `580b7f694a139acd` | {"name": "valid-within", "rc": 0, "kind": "valid", "kept_pass_cycles": 1000, "verdict": "kept_grade: PASS (0 f |

## scripts

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `disposition_regrade.py` | 1503 | `290543e228b24b91` | #!/usr/bin/env python3 |
| `hot_census.py` | 2005 | `a20aabac24fea742` | #!/usr/bin/env python3 |
| `plant_kept_grade.py` | 3664 | `da87a3b249003a22` | #!/usr/bin/env python3 |
| `r885_probe_kept_grade.py` | 5306 | `55b3bcf52e1d6e1d` | #!/usr/bin/env python3 |
| `r885_probe_selftest_coverage.py` | 1413 | `ccd947a0cfdb4822` | #!/usr/bin/env python3 |
| `r886_probe_kept_grade.py` | 3553 | `844ffc02f205494e` | #!/usr/bin/env python3 |

