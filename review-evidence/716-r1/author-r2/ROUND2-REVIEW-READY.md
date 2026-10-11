[A601] REVIEW READY

Commit: `941e15593ef3dbf561bd8ed75aaf680f5d146a41`
Branch: `716-fw-unit-split`; committed, clean and unpushed.

Round 2 assignment 6113977586 is complete locally. Merged dev
`09c7231eca343607c97c0d66abebb2553688712c` into
`f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48` with one merge commit,
without rebase or amendment. Submodules were updated at their merged pins.

Changed: resolved all four shared-file conflicts, preserving the required
publication-census job and all four firmware jobs. The normal shard includes
F-INT's SRP comparator; the SRP shard retains all five ROUND5 publication
mutants in both interface campaigns. The CI contract and policy retain the
aggregate results, command census, SDK-only caches and four 45-minute budgets.

Preservation evidence:

- The actual dev default, merged default and concatenated shards contain the
  same ordered 916 invocations; shard sizes are 60/507/77/272.
- Command census: 19 original script lines, 55 after repeated setup; identical
  command and condition sets after removing only terminal shard arguments.
  Independent step metadata comparison also passes.
- Missing/duplicate dispatch mutants fail; a future suite is discovered;
  nine invalid/narrowing combinations refuse. Independent omission and
  duplication of the new comparator invocation also fail the comparison.
- Coverage stays unsplit. Fresh dev-driver and merge-head measurements match
  across all 30 files: raw/retained fractions and covered line/branch locations.
  Ratchet thresholds and exclusions are unchanged by this lane.

All four job sequences ran serially at this head under CPython 3.12.3,
four-CPU affinity and four workers, with fresh builds and no competing lane
workload. Every measured command returned zero.

| Job | Local seconds | Conservative hosted prediction | Timeout used |
|---|---:|---:|---:|
| firmware-unit | 652.567 | 745 s | 27.59% |
| firmware-control-mutants | 991.799 | 1100 s | 40.74% |
| firmware-aecp-mutants | 222.970 | 294 s | 10.89% |
| firmware-srp-mutants | 695.161 | 789 s | 29.22% |

Original calibration: `2247 / 2606.655866 = 0.862024032`, run 38095263410,
job 114339840343. The conservative recalibration includes all 40 historical
split jobs at f41e4f2d. The largest compute ratio is
`674 / 642.830291 = 1.048488239`, run 38162821680 attempt 2,
job 114542554327. Formula: `ceil(local seconds * 1.0484882393632189 + 60)`.
The 60-second allowance exceeds observed overhead maxima of 33 seconds for
those split jobs and 37 seconds for the original samples.
The slowest prediction, 1100 seconds, is below the 1620-second / 60% ceiling.
No assigned STOP condition was triggered.

Validation, all exit 0 at the merge head:

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_events.py --firmware-census
python3 scripts/ci_scope.py --selftest
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/rv32-sdk"
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_doc_style.py --selftest
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --selftest
python3 scripts/check_py_idiom.py
python3 scripts/check_py_idiom.py --selftest
python3 scripts/check_em_dash.py --selftest
python3 scripts/check_em_dash.py --base 09c7231eca343607c97c0d66abebb2553688712c
git diff --check 09c7231eca343607c97c0d66abebb2553688712c HEAD
```

Results: CI contract 2016 items and 2828 arms; control 506/506 mutants caught;
AECP and SRP campaigns plus pin controls pass; comparator five controls and
18 planted defects pass; saved-state five shapes and 435 tests; coverage
30 files and 28 self-test cases; documentation and Python gates pass.
The independent census and coverage comparison also return zero.

Acceptance: the merged layout and local preservation/prediction requirements
are met. Item 2 needs the manager's hosted check at the new head.
The ten-run table is retained unchanged in both handoff documents and clearly
marked as measured at f41e4f2d. The prepared PR body uses `Relates to #716`.
R620-1 and R621-1 remain positive at f41e4f2d only; re-review and the remaining
verification/merge lifecycle are pending. RES1 and RES2 go to #495 at merge
as manager duty, per the assignment.

`HANDOFF.md`, `PR-BODY.md`, round 2 inventories, calibration, per-file coverage
comparison, gate receipts and log size/SHA-256 manifests are in the assigned
output directory. Every output file is below 200 KB; all builds and dependencies
remain in scratch. No push, PR mutation, hosted execution or hardware action
was performed. No TAKEN was repeated. Stopping here.
