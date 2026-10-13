[A601]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Round 2](#round-2)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Local firmware and touched gates pass at `941e15593ef3dbf561bd8ed75aaf680f5d146a41`.
`716-fw-unit-split` -> `dev`; the merge head remains unpushed.
Item 2 passed at f41e4f2d; the manager rechecks hosted runs at this new head.

## Linked Issue / roles

Closes #716

Acceptance item 2: ten consecutive hosted runs at `941e1559`, all success; the slowest firmware job took 916 s, 33.9 % of its 45-minute timeout (manager comment 6117443205).

Executor: `[A601]`
Internal cleared-context reviewer: `[R620]`
External reviewer: `[R621]`

## Description

The original firmware job reached 2450 of 2700 seconds.
Four required firmware jobs now separate normal suites and complete control,
AECP and SRP mutation campaigns. Normal suites retain saved-state, RV32 and
tally controls plus the unsplit coverage ratchet. Every timeout stays 45 minutes.
The aggregate requires every result. Only the pinned SDK is cached.

The merged population has 916 invocations, partitioned 60/507/77/272.
The actual dev default, merged default and concatenated shards agree exactly.
Missing and duplicate work fails the ownership check; future suites are discovered.
The generated command census preserves every command and its conditions.
The CI contract pins the layout, aggregate, caches and per-job budgets.

Coverage remains unsplit. Separate fresh dev-driver and merge-head measurements
match file by file across all 30 files, including raw and retained fractions
and covered line/branch locations. The lane leaves thresholds and exclusions intact.

## Authoritative references

- Issue #716 and assignment comments 6107547907 and 6113977586.
- `REQUIREMENTS.md`, REQ-VER-04.
- `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`.
- `.github/workflows/rtl-fast.yml` and `scripts/ci_events.py`.

## How to get into the same state

```sh
git switch 716-fw-unit-split
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
```

Original base: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
Merged dev: `09c7231eca343607c97c0d66abebb2553688712c`. Expected head: `941e15593ef3dbf561bd8ed75aaf680f5d146a41`.
Use CPython 3.12.3 and the dependencies in `sw/firmware/gtest/README.md`.
The local measurements used GCC 16.2.1 and GoogleTest/GoogleMock 1.18.0;
the sampled hosted jobs report GCC 13.3.0 and GoogleTest/GoogleMock 1.14.0.
Install the pinned Markdown dependencies for documentation checks.
Set `SCRATCH` to writable disk storage outside the checkout.

```sh
python3 -m pip install pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
export TMPDIR="$SCRATCH"
export PYTHONPYCACHEPREFIX="$SCRATCH/pycache"
python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/rv32-sdk"
export MILAN_RV32_CC="$SCRATCH/rv32-sdk/bin/riscv32-linux-gcc"
```

## How to validate

```sh
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_events.py --firmware-census
python3 scripts/ci_scope.py --selftest
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 sw/firmware/gtest/tally_selftest.py
python3 scripts/ci_rv32_sdk_selftest.py
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

All commands exited zero at the merge head. Expected results:

- CI event contract: 2016 items, 2828 self-test arms; census preserved.
- Shard controls: 916 exclusive invocations, missing/duplicate mutants caught,
  future suite discovered, nine invalid combinations refused.
- Control campaign: 506/506 mutants caught; AECP and both SRP campaigns pass.
- F-INT comparator: five controls and eighteen planted defects pass.
- Saved-state: five shapes and 435 tests; coverage: 30 files and 28 planted cases.
- Documentation and Python checks: no findings or increased budgets.

## Round 2

Merged dev `09c7231eca343607c97c0d66abebb2553688712c` into `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48` as
`941e15593ef3dbf561bd8ed75aaf680f5d146a41` using a merge commit, without rebasing or amending.
Submodules were updated at their merged pins.

The aggregate retains dev's required publication-census job and all four firmware
jobs. The normal shard includes the new SRP comparator; the SRP shard retains
all new publication mutants at both interface counts. The policy records ownership.
The separate publication-census job and its step contract are unchanged from dev.

All four firmware command sequences ran separately with CPython 3.12.3,
four-CPU affinity, four workers, fresh builds and no competing lane workload.
The original hosted/local ratio was `2247 / 2606.655866 = 0.862024032`
(run 38095263410, job 114339840343).
The conservative recalibration includes all 40 historical split-job measurements.
Its maximum is `674 / 642.830291 = 1.048488239`, at run 38162821680,
attempt 2, job 114542554327. Setup/completion allowance is 60 seconds,
above the observed 33-second split-job and 37-second original-job maxima.
Formula: `ceil(local seconds * 1.0484882393632189 + 60)`.

| Job | Four-CPU local seconds | Original-ratio prediction | Calibrated prediction | Timeout used |
|---|---:|---:|---:|---:|
| `firmware-unit` | 652.567 | 623 s | 745 s | 27.59% |
| `firmware-control-mutants` | 991.799 | 915 s | 1100 s | 40.74% |
| `firmware-aecp-mutants` | 222.970 | 253 s | 294 s | 10.89% |
| `firmware-srp-mutants` | 695.161 | 660 s | 789 s | 29.22% |

The slowest prediction is 1100 seconds, 40.74% of the unchanged timeout,
below the 1620-second pre-review ceiling. No assigned STOP condition was triggered.
The handoff contains per-command receipts, census and shard controls,
coverage comparison, historical step/suite timings, calibration and log digests.

The manager's ten-run table is retained below, measured at f41e4f2d.
It does not establish hosted acceptance at the new merge head.

Measured at `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`.

| Run | Head | firmware-unit | firmware-control-mutants | firmware-aecp-mutants | firmware-srp-mutants | Each within 1890 s |
|---|---|---|---|---|---|---|
| 38162821680 attempt 1 | `f41e4f2d` | 684 s | 682 s | 239 s | 567 s | yes |
| 38162821680 attempt 2 | `f41e4f2d` | 703 s | 841 s | 243 s | 415 s | yes |
| 38162821680 attempt 3 | `f41e4f2d` | 676 s | 823 s | 174 s | 577 s | yes |
| 38162821680 attempt 4 | `f41e4f2d` | 667 s | 831 s | 250 s | 595 s | yes |
| 38162821680 attempt 5 | `f41e4f2d` | 660 s | 840 s | 242 s | 482 s | yes |
| 38162821680 attempt 6 | `f41e4f2d` | 538 s | 815 s | 207 s | 610 s | yes |
| 38162821680 attempt 7 | `f41e4f2d` | 534 s | 838 s | 169 s | 604 s | yes |
| 38162821680 attempt 8 | `f41e4f2d` | 667 s | 826 s | 260 s | 625 s | yes |
| 38162821680 attempt 9 | `f41e4f2d` | 449 s | 648 s | 203 s | 505 s | yes |
| 38162821680 attempt 10 | `f41e4f2d` | 693 s | 830 s | 244 s | 604 s | yes |

## Known limitations / out of scope

- The manager must collect new-head hosted acceptance and obtain re-review.
- R620-1 and R621-1 were positive at f41e4f2d only.
- R620-1 RES1 and RES2 go to #495 at merge, as manager duty.
- Compiler/package differences and cache conditions limit predictions.
- Historical buffered logs provide reporting windows, not precise binary timings.
- The full verification, merge authorization and containment lifecycle remains pending.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied at the new head
- [x] New or changed behavior has self-checking tests
- [ ] Required full local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the new head
- [ ] External review is positive at the new head
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


