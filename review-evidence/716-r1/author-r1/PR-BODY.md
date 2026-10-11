[A601]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Local implementation and touched gates pass; ready for independent review.
Hosted acceptance item 2 remains pending the manager's ten consecutive runs.
`716-fw-unit-split` -> `dev`.
Head: `f41e4f2dd56eaccebb30d6c1ec255624b0ae7a48`.

## Linked Issue / roles

Relates to #716

Executor: `[A601]`
Internal cleared-context reviewer: `[R620]`
External reviewer: `[R621]`

## Description

The existing firmware job reached 2450 of 2700 seconds across 17 sampled hosted jobs.
Four required jobs now separate normal suites and the complete control, AECP, and SRP
mutation campaigns. The normal job retains saved-state tests, RV32 controls, tally checks,
and the complete coverage ratchet. Every timeout remains 45 minutes.

The driver proves exhaustive, disjoint assignment against its live default inventory.
All 844 original invocations remain in the same order across the shards: 59, 472, 75, 238.
Missing and duplicate dispatch mutants fail; an injected future suite is discovered
without a hand-maintained ownership list. The generated command census retains every
original command and condition, permitting only the new shard arguments and repeated setup.
The CI contract pins every worker, aggregate result, SDK check, and documented budget.

Coverage remains unsplit. Separate baseline and candidate measurements match in all 30
files, including raw and post-exclusion line/branch fractions and covered locations.
Suite populations, exclusions, thresholds, and the digest-keyed SDK cache are unchanged.
Build outputs remain fresh and are never persisted in that cache.

## Authoritative references

- Issue #716 and assignment comment 6107547907.
- `REQUIREMENTS.md`, REQ-VER-04.
- `CONTRIBUTING.md` and `docs/testing/CI_WORKFLOWS.md`.
- `.github/workflows/rtl-fast.yml` and `scripts/ci_events.py`.

## How to get into the same state

```sh
git switch 716-fw-unit-split
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
```

Base: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`.
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
python3 scripts/check_em_dash.py --base ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5
git diff --check ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5 HEAD
```

All listed validation commands exited zero. Expected results at this head:

- CI contract: 1944 items and 2672 self-test arms pass; census reports `preserved: true`.
- Dispatch: 844 invocations occur exactly once; both ownership mutants are caught.
- Control: all 471 mutants caught; AECP, both SRP campaigns, and pin refusals pass.
- Saved-state: five shapes, 435 tests pass; coverage: 30 files, 28 self-test cases pass.
- Documentation and Python gates: no findings or increased budgets.

The unchanged complete firmware workload and all four candidate workloads ran separately
with four-CPU affinity, four workers, fresh builds, and no concurrent test/build activity
from this lane. Historical suite figures are timestamped reporting windows because buffered
logs do not expose precise individual binary build/run durations.

Base hosted run 38095263410, job 114339840343, supplies
2247 seconds of matching compute steps. The local baseline is
2606.655866 seconds, giving hosted/local ratio 0.862024032.
The conservative table uses the slowest matching historical compute total,
2312 seconds at job 114282060753, ratio
0.886960197. Every estimate adds 60 seconds
for setup/completion, covering the observed maximum and a 60-second minimum allowance.
Formula: `ceil(local seconds * ratio + setup allowance)`.

| Job | Four-CPU local seconds | Conservative hosted prediction | Timeout used |
|---|---:|---:|---:|
| `firmware-unit` | 642.830 | 631 s | 23.37% |
| `firmware-control-mutants` | 922.927 | 879 s | 32.56% |
| `firmware-aecp-mutants` | 219.862 | 256 s | 9.48% |
| `firmware-srp-mutants` | 617.701 | 608 s | 22.52% |

Every prediction is below 1620 seconds, 60% of its unchanged 45-minute timeout.
The handoff records all 17 historical job IDs, full step times, reporting windows,
command inventories, per-file coverage comparison, and log sizes/digests.
Historical samples and local predictions do not establish acceptance item 2.

Acceptance item 2's ten consecutive hosted-run table is reserved for the manager:

| Run | Head | firmware-unit | firmware-control-mutants | firmware-aecp-mutants | firmware-srp-mutants | Each within 1890 s |
|---|---|---|---|---|---|---|
| Pending manager | | | | | | |

## Known limitations / out of scope

- Publication and the ten hosted acceptance runs belong to the manager.
- Compiler/package differences and SDK-cache conditions limit the timing prediction;
  hosted measurements determine acceptance.
- Buffered historical logs do not support exact per-binary duration claims.
- The full local RTL sweeps, protected hosted contexts, independent reviews,
  candidate-merge validation, and post-merge containment remain required before completion.
- No firmware behavior or hardware validation changes are included.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
