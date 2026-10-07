[A556]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 3](#round-3)** — The `--no-ff` merge of dev `910f338d` (#679) and the re-graded RV32 checks.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN on the assigned gates. `677-fw-fixes` -> `dev`.

- Base: dev `910f338dbd050f4efd2d96991ddcf928a583d55f`, merged in with `--no-ff` (round 3).
- Head: `34475e774dfe1c92c81fa51293668e64dc95fa85`.
- Commits: the fix `6c94e9f5` (on `6714181d`), the merge `232970db`, and the RV32 resolution `34475e77`.

Results at the head (round 3; every RV32 build on the pinned SDK):
- Control firmware: 423 host checks and the RV32I build pass; 79/79 mutants caught.
- RV32 self-test (#679): 17 checks pass.
- Tally listener: 18/18 defects caught.
- NVM store: 435 tests over 5 shapes and five RV32 builds pass; 109/109 mutants caught.
- Coverage: the ratchet holds at 100% lines and branches on all 14 files, with no new exclusion.
- Docs and tooling bank: all 47 commands pass.
- Builder bank (round 1, at `6c94e9f5`): all 100 functions pass, with the census run in disjoint slices. It is not on the round-3 list.

The long local gates `scripts/run_all_suites.sh` and `syn/yosys/run.sh` are
still owed (see Known limitations).

## Linked Issue / roles

Closes #677
Closes #678
Relates to #665 and #675.

Executor: `[A556]`
Internal cleared-context reviewer: `[R524]`
External reviewer: `[R525]`

## Description

A bounds-checking fix and a re-entrancy robustness fix in the bare-metal
control firmware. Both are host-tested under the FT coverage ratchet.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | **Out-of-bounds read (#677).** An erased record's payload was bounded only by the container end, which comes from the container's own length field. A caller holding just a loaded prefix could therefore be read past its buffer. The codec now refuses a payload beyond `loaded` (`NVM_VD_REC`) before reading it. The `end` check still runs first, so an overrun container still gets `NVM_VD_LEN`. |
| `sw/firmware/ctrl/adp/adp.h`, `adp.c` | **Re-entrant callbacks (#678).** The no-callback rule is now public: every port returns before the event loop delivers another core input, including a zero-delay timer expiry. A shared guard brackets all six port calls, and every public ADP entry checks it before touching its arguments, including `adp_init` and `adp_build`. Debug and test builds assert. Release builds ignore the call and count it (`adp_reentry_count`, lifetime, modulo 2^32). A refused `adp_poll` returns false. The guard spans every instance on the one event loop. |
| Nine other port headers (`adp_mbx.h`, `mbx.h`, `mbx_hal.h`, `ctrl_debug.h`, `ctrl_pool.h`, `shlan_port.h`, `nvm_flash.h`, `nvm_state.h`, `nvm_flash_litespi.h`) | State the same port rule; `shlan_port.h` carries it to F2-F5. |
| `sw/firmware/ctrl/test/test_adp_reentry.cpp` | The two inline-expiry probes become standing tests, plus 6 ports x 10 entries x same/other instance (120 cases). All 122 tests run in a debug arm and in a release arm. |
| `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp` | An AddressSanitizer test owns exact-sized buffers of 40, 47 and 48 bytes and checks both sides of the final payload boundary. It runs in the default firmware-unit command. |
| `ctrl_mutants.py`, `nvm_mutants.py` | Planted defects: `reentry-guard-removed`, `reentry-uncounted`, `reentry-not-ignored`; `erased_payload_end_bound` (the old bound, reported as a heap-buffer-overflow), `erased_payload_guard_early`, `erased_payload_guard_late`. Every previous mutant is retained. |
| `fw_gtest.py`, `nvm_bench.py`, `ctrl_arms.py`, `test_ctrl_firmware.py`, `fw_coverage.py` | Host-only ASan build option, the new arms in the default and coverage gates, and the `--jobs` limit honored. |
| `sw/firmware/gtest/coverage.ratchet`, `gtest/README.md` | The ratchet was regenerated through `fw_coverage.py --write`. The five ADP exclusion proofs now cite the header rule; there are no new or widened exclusions. |
| `sw/firmware/ctrl/README.md`, `ctrl_nvm/README.md` | Document the new arms, the sanitizer test and the campaign size. |

There is no RTL, configuration, builder or workflow change. Neither the
shipping bare-metal image nor the default all-fabric build compiles
`sw/firmware/ctrl` or `sw/firmware/ctrl_nvm`.

## Round 3

R524-2 and R525-2 were POSITIVE at `6c94e9f5`. #679 then merged into dev
(`910f338d`, PR #683), and dev was merged into this branch with `--no-ff`
(`232970db`). There was no rebase and no amend.

**Textual conflict.** There was one, in the `rv32` paragraph of the
`test_ctrl_firmware.py` docstring. The resolution keeps #679's wording and
adds the assertion interface. Everything else merged automatically.
`git diff 910f338d 232970db` equals the round-1 diff hunk for hunk, apart from
that docstring hunk. Both gates still run the debug and release re-entry arms
next to #679's `rv32` checks. The mutant catalogs are byte-identical to
round 1, and #679's 17 RV32 self-test checks are all kept.

**Semantic conflict, resolved in `34475e77`.** #679 builds RV32 objects with
`-nostdinc` against its own `rv32_include` declarations. `adp.c` includes
`<assert.h>` for the #678 debug guard, so at the merge commit the ctrl `rv32`
arm failed with `assert.h: No such file`. #679 also replaced the `__`-prefix
allowance with exact helper names, and `__assert_fail` had been admitted only
by that prefix. The fix follows #679's pattern for consumed C-library
interfaces:

| File | Change |
|---|---|
| `sw/firmware/gtest/rv32_include/assert.h` (new) | The C11 `assert` macro (it follows `NDEBUG` at each inclusion), `static_assert`, and a declaration of `__assert_fail`. It is a declaration only. |
| `sw/firmware/ctrl/test/ctrl_build.py` | `RV32_LIBC` gains exactly `__assert_fail`. |
| `sw/firmware/gtest/fw_rv32_selftest.py` | The hostile hosted sysroot also poisons `assert.h`, and the probe includes and uses it. |
| `sw/firmware/gtest/fw_rv32.py`, `gtest/README.md` | Describe the third declared header and the named interface. |

Two checks are re-graded:
- **The ctrl runtime-dependency check.** The allowed set gains
  `__assert_fail`. #678 requires debug builds to assert, and the arm builds
  without `NDEBUG`, so this is the same symbol round 1 listed, now admitted by
  name instead of by prefix. The shared helper set, the store's allowed set,
  and the ABI, frame and stack-protector checks are unchanged. `malloc` and
  unknown `__` names are still rejected.
- **#679's header-isolation proof.** It now covers `assert.h` as well.

A witness at the head confirms the re-grade:
- the arm fails without the header;
- it fails on `__assert_fail` without the allowed name;
- an `NDEBUG` build references no assertion handler.

A debug target build of `sw/firmware/ctrl` needs its bare-metal runtime to
supply `__assert_fail`; a release build needs none. Nothing shipped compiles
this firmware.

## Authoritative references

- #677 assignment comment 6021510152, #677 acceptance criteria and the #678 manager ruling.
- `REQUIREMENTS.md` and `docs/reference/FR_NFR.md`: experimental firmware scope and retained fabric ownership.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 6.2: KLJ2 container and record validation.
- `sw/firmware/ctrl_nvm/nvm_klj2.h`: the partial-prefix (`loaded`) validation contract.
- `sw/firmware/ctrl/adp/adp.h`: Milan v1.2 section 5.6.3 (Advertise state machine) and IEEE 1722.1-2021 section 6.2 (ADPDU) references, and the no-callback port contract.
- `sw/firmware/gtest/README.md`: FT coverage rules and exclusion proofs.

## How to get into the same state

```sh
git fetch origin 677-fw-fixes
git switch 677-fw-fixes
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
sudo apt-get install -y --no-install-recommends libgtest-dev libgmock-dev
python3 -m pip install pyyaml
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

Validated with:
- GCC/gcov 16.2.1 and GoogleTest/GoogleMock 1.18.0.
- The repository-pinned RV32 SDK (GCC 14.3.0) for every RV32 build in round 3, selected with `MILAN_RV32_CC`, and for the round-1 builder census.
- Verilator 5.050.

The optional lwSRP arm uses a checkout at
`19f5796b63652eb1151906de73cb827d4980a53f`.

## How to validate

```sh
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_em_dash.py --base 910f338dbd050f4efd2d96991ddcf928a583d55f
git diff --check 910f338dbd050f4efd2d96991ddcf928a583d55f HEAD
```

Expected result / pass criteria:
- Every command returns 0.
- The RV32 self-test passes 17 checks, and the ctrl `rv32` arm lists `__assert_fail` among its undefined symbols.
- 18 listener defects, 79 control-firmware mutants and 109 NVM mutants are caught.
- There are 423 control host checks; the re-entry arms run 122 tests in each of debug and release.
- There are 435 NVM tests across 5 shapes, with all RV32 builds passing.
- All 14 measured firmware files stay at 100% lines and branches, with the exclusions unchanged.
- The builder's only skip is the resource calibration, which needs an absent historical placement report.

With the old `end` bound restored, `NvmCodec.codec_erased_loaded_prefix` must
fail with an AddressSanitizer heap-buffer-overflow. With the guard removed,
`AdpReentry.AdvertiseInlineExpiry` must fail in both modes.

The handoff evidence records each of these at the head that ran it.
- Round 3, at `34475e77`: every command except the builder bank, plus the
  47-command docs and tooling bank and the optional lwSRP controls.
- Round 1, at `6c94e9f5`: the builder bank and the mailbox firmware
  co-simulation. Neither is on the round-3 list, and this PR changes no
  builder or RTL file.

Commands that exceed a ten-minute window ran as bounded slices built on the
repository's own functions: the NVM campaign, and the builder census inside
function 13.

## Known limitations / out of scope

- **Not a lock.** The shared ADP guard diagnoses re-entry on a single event loop; it is not a concurrency lock. Its release counter covers the whole lifetime and wraps modulo 2^32.
- **RV32 evidence.** It covers the freestanding object builds and #679's dependency checks. `__assert_fail` is declared in `rv32_include/assert.h` and named in the ctrl allowed set. The evidence is not a linked target image or a target assertion handler. If the eventual target runtime names its handler differently, the declaration and the allowed name change together.
- **Long local gates owed.** `scripts/ci_scope.py` classifies any change under `sw/` as RTL/tooling-relevant. The long local gates `scripts/run_all_suites.sh` and `syn/yosys/run.sh` are therefore owed before this PR is marked validated. They were not part of this lane's assigned gates and have not run. The RTL is unchanged.
- **Builder skip.** The builder's resource calibration arm is NOT RUN: it needs an mf48 placement report that is not on the validation host.
- **Unchanged.** No RTL, default fabric build, shipping image, board or hardware behavior changes.
- **Pending.** Hosted CI, the local hosted-workflow replica, independent review and merge validation.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
