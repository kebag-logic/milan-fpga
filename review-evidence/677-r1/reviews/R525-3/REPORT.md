[R525] POSITIVE - exact head 34475e774dfe1c92c81fa51293668e64dc95fa85

R525-3, external cleared-context delta review of issue #677 / PR #684 (round 3, merge only; assignment #677 6029754278). Head `34475e774dfe1c92c81fa51293668e64dc95fa85`, tree `46cc939a85be1aa400f15fbd7c72ea983ac88271`. The delta since the POSITIVE R524-2/R525-2 head `6c94e9f5` is the `--no-ff` merge of dev `910f338d` (`232970db`, bringing #667, #673 and #679) and one resolution commit, `34475e77`. All five lenses were applied at this head. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One SUGGESTION is recorded. This is a source-review verdict, not merge authorization.

## Reconstruction

Read in order: AGENTS.md and CONTRIBUTING.md; docs/README; issue #677 body (frozen acceptance 1-3), #678 body and manager ruling, #679 body (closed); the #677 lane comments (assignment, TAKEN, round-1 REVIEW READY, correction 6024757146, round-3 assignment 6029754278, round-3 REVIEW READY 6030485056); the PR #684 body. Then the diffs and history below, then the executable checks below. The author packet `review-evidence/677-r1/author-r3/` (evidence branch commit `215abe01`) was spot-checked after the independent runs. Prior review findings were read only after my draft verdict and ledger were recorded (`receipts/draft-verdict-before-prior-findings.txt`, 04:12:11Z). No other round-3 reviewer report was read.

## Merge fidelity

| Check | Result | Receipt |
|---|---|---|
| `git diff 910f338d 232970db` against round 1 (`git diff 6714181d 6c94e9f5`), index lines and hunk offsets normalized | Identical except the `rv32` paragraph of the `test_ctrl_firmware.py` docstring. 26 files on both sides. | `receipts/round1-vs-merge.normdiff`, `round1.diff`, `merge-vs-dev.diff` |
| The converse: `git diff 6c94e9f5 232970db` against dev's side `git diff 6714181d 910f338d` | Identical except the same docstring hunk. Every #667, #673 and #679 change is present. | `receipts/devside-vs-merge.normdiff`, `dev-side.diff`, `merge-vs-pr.diff` |
| Combined diff of the merge (`git show --cc 232970db`) | One conflicted hunk only. It is docstring text, and the resolution keeps #679's wording and adds "(string, format or assertion)". | `git show --cc 232970db` |
| Files touched by both sides | `ctrl/README.md`, `ctrl_nvm/README.md`, `ctrl/test/ctrl_arms.py`, `ctrl/test/test_ctrl_firmware.py`, `gtest/README.md`. #679's `arm_rv32` rewrite (exact `HELPERS`, `--extern-only`, ABI/frame checks) and this PR's `reentry` arms coexist in `ctrl_arms.py`. The default gate lists `arm_rv32` and both re-entry arms (`test_ctrl_firmware.py:120-123`); the coverage gate lists both re-entry arms (`:89-91`). | `receipts/pr-vs-dev-head.diff` |
| Firmware C/H sources, mutant catalogs and tally/coverage self-tests, `6c94e9f5`..head | No `.c`, `.h` or `.cpp` firmware source changed except the new `rv32_include` headers. `ctrl_mutants.py`, `nvm_mutants.py`, `tally_selftest.py`, `fw_coverage_selftest.py`, `fw_coverage.py`, `fw_gtest.py`, `nvm_bench.py` and `coverage.ratchet` are byte-identical. | `git diff --name-only 6c94e9f5 34475e77` |
| PR footprint against live dev `910f338d` | 30 files, all under `sw/firmware/`. No RTL, testbench, configuration, workflow or gitlink change. | `receipts/pr-vs-dev-head.diff` |

## Semantic conflict and its resolution

- **Witness at the merge commit.** At `232970db`, the ctrl `rv32` arm fails because `adp.c:17` cannot find `assert.h` under `-nostdinc` (`receipts/merge-commit-rv32.log`). The same arm passes at dev `910f338d` (`receipts/devtip-rv32.log`). #679 had removed the `__`-prefix allowance (`stray = ... and not s.startswith("__")`) in favour of `fw_rv32.HELPERS`.
- **Header conformance, C11 7.2.** `sw/firmware/gtest/rv32_include/assert.h` behaves as follows:
  - `#undef assert` and the `NDEBUG` test sit outside the include guard, so `assert` follows `NDEBUG` at each inclusion (7.2p1).
  - The `NDEBUG` form is exactly `((void)0)`.
  - The active form is a void expression that evaluates its argument once and passes `#expr`, `__FILE__`, `__LINE__` and `__func__` to the handler (7.2.1.1).
  - `static_assert` expands to `_Static_assert` (7.2p3).
  - The `_Noreturn` handler declaration matches the glibc `__assert_fail(const char *, const char *, unsigned int, const char *)` signature.

  An executable probe compiled `probe.c` against `rv32_include` only (`-nostdinc`, `-std=c11 -pedantic -Wall -Wextra -Werror`). It checks each of these on the host, including toggling across three inclusions and a non-evaluated argument under `NDEBUG`. RV32 objects show `__assert_fail` undefined in a debug build and no undefined symbol under `-DNDEBUG` (`scripts/assert_c11/`, `receipts/assert-c11.log`, rc 0).
- **The allowance is exactly one name.** `ctrl_build.py:46` is #679's set plus `__assert_fail`. Run against the real ctrl arm with the pinned SDK (`scripts/assert_witness.py`, `receipts/assert-witness.log`, rc 0):
  - W0: the head passes with `__assert_fail` open.
  - W1: it fails without `rv32_include/assert.h`.
  - W2: it fails naming `__assert_fail` without the allowed name.
  - W3: an `NDEBUG` build passes with no assertion handler referenced, even with the name removed.
  - W4: `malloc`, `__unexpected_service`, `__assert_func`, `__assert`, `__assert_failx` and `abort` are each rejected as "symbols outside the C library".
- **Self-test.** `fw_rv32_selftest.py:30` poisons `assert.h` in the hostile sysroot and the probe includes and uses it (`:37`, `:42`). The count stays 1 + 9 + 7 = 17, as at `910f338d`. With `rv32_include/assert.h` removed, the self-test's positive control fails on `assert.h` (`scripts/selftest_header_witness.py`, `receipts/selftest-header-witness.log`, rc 0).

## Gates run at this head (pinned SDK, receipt verified)

The pinned SDK is `riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9...b78f`. It was installed into scratch through `scripts/ci_rv32_sdk.py --archive` and verified (`receipts/sdk-install.log`). It was selected with `MILAN_RV32_CC`. Host toolchain: GCC/gcov 16.2.1, GoogleTest/GoogleMock 1.18.0.

| Command | rc | Result | Receipt |
|---|---|---|---|
| `fw_rv32_selftest.py --require-rv32` | 0 | 17 checks PASS | `receipts/rv32-selftest.log` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 6` | 0 | 423 host checks (14+30+26+21+2+41+5x9+122+122); RV32I build PASS with `undefined: __assert_fail, __lshrdi3, __mulsi3, __udivsi3, __umodsi3, memcpy, memset, vsnprintf`; mutants 79 of 79 caught, including `reentry-guard-removed`, `reentry-uncounted`, `reentry-not-ignored` and `pool-falls-back-to-heap` (rv32) | `receipts/ctrl-selftest.log` |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 6` (one full invocation) | 0 | 5 shapes, 435 tests, five RV32 builds, all 109 planted defects reddened; `erased_payload_end_bound`, `_guard_early` and `_guard_late` are caught by `codec_erased_loaded_prefix` | `receipts/nvm-selftest.log` |
| `tally_selftest.py --mutants` | 0 | 18 of 18 listener defects caught | `receipts/tally.log` |
| `fw_coverage.py --check --jobs 4` (no lwSRP arm) | 0 | 14 files, 100% lines and branches; PASS | `receipts/coverage-check.log` |
| `scripts/asan_end_bound.py` | 0 | The head's prefix suite passes under AddressSanitizer. The restored `end` bound gives `heap-buffer-overflow`, `READ of size 1`, in `nvm_all_erased` | `receipts/asan-end-bound.log` |
| `docs_check.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base 910f338d`, `git diff --check 910f338d HEAD`, `git diff --check 232970db HEAD` | all 0 | pass | `receipts/docs-gates.log` |

Hosted, exact head (snapshot in `receipts/hosted-check-runs.tsv`):
- `firmware-unit` executed on the PR merge ref with dev `910f338d` and succeeded. Its log shows 17 RV32 self-test checks, the ctrl RV32 arm with `__assert_fail` undefined, and 435 store tests (`receipts/hosted-firmware-unit-extract.txt`).
- `rtl-fast`, `elaborate`, `verilator-lint`, `yosys-elaboration`, all four Yosys shards, and Verilator shards 0 and 3 succeeded.
- Verilator shards 1, 2 and 4 were still in progress at the snapshot.
- `Physical gPTP` is skipped. That is a skipped context, not executed evidence.
- The manager owns hosted and local-replica acceptance.

## Findings

**R525-3-S1 | SUGGESTION | Conformance, RTL | `sw/firmware/gtest/rv32_include/assert.h:17`, `sw/firmware/ctrl/test/ctrl_build.py:46`**
- Authority/evidence: the declared handler follows glibc's `__assert_fail(expr, file, line, func)`. The repository's documented bare-metal C library is LiteX's (`docs/integration/BAREMETAL_FIRMWARE.md:522`; picolibc per `sw/builder/test_builder.py:5501`). Upstream picolibc, and newlib, declare `__assert_func(file, line, func, expr)` instead (picolibc `libc/include/assert.h`).
- Impact: none today. These are object-only checks, nothing links this firmware, and the executor disclosed the limit in the PR body ("If the eventual target runtime names its handler differently, the declaration and the allowed name change together").
- Suggested outcome: when a target link of `sw/firmware/ctrl` is introduced, align the declared handler and the allowed name with that runtime, or supply the named handler there.
- Verification: a linked debug image of the ctrl firmware resolves its assertion handler.

**Observation (not a finding):** the intermediate merge commit `232970db` alone fails the ctrl `rv32` arm. The PR is reviewed and merged as its head, and the next commit resolves it, but bisection over this lane should skip `232970db`.

### Prior public findings at this head

- **R524-1-F1 / R525-1-F1 (MINOR, Conformance, Docs): RESOLVED, retained.** The PR body still cites Milan v1.2 section 5.6.3 and IEEE 1722.1-2021 section 6.2. `adp.h:9` is unchanged.
- **R524-1-F2 / R525-1-F2 (MINOR, Tests, Docs): RESOLVED, retained.** Correction 6024757146 stands. The README exclusion table at `sw/firmware/gtest/README.md:284` still has 14 data rows; every table in the file is byte-identical to `6c94e9f5`. The "All fourteen rows" text at line 219 is unchanged.
- No other prior finding was published on this PR.

## Lens results

[R525] PASS Conformance - `sw/firmware/gtest/rv32_include/assert.h:5-17`, `receipts/assert-c11.log`, `sw/firmware/ctrl_nvm/nvm_klj2.c:298`, `receipts/asan-end-bound.log`, `receipts/round1-vs-merge.normdiff` - The header meets C11 7.2 (per-inclusion `NDEBUG`, exact `((void)0)`, single evaluation, the four diagnostic values, `static_assert`). #677 acceptance 1-3 still hold at the merged head: the loaded bound precedes the read, the ASan prefix test fails the old bound, the ratchet holds and the store mutants are caught. #678 acceptance 1-3 are unchanged: the header rule, the guard, both standing probes and the three guard mutants are caught. #679's acceptance (freestanding ctrl and ctrl_nvm RV32 arms) still passes with the pinned SDK, locally and in hosted `firmware-unit`. The round-3 assignment (both sides kept, re-grades stated) is met.

[R525] PASS RTL - `receipts/pr-vs-dev-head.diff`, `receipts/devside-vs-merge.normdiff`, `sw/firmware/ctrl/test/ctrl_build.py:42-46`, `sw/firmware/ctrl/adp/adp.c:17,29` - The PR footprint against live dev is 30 files under `sw/firmware/`, with no RTL, clock/reset/CDC, configuration, workflow or gitlink change. The RTL that `232970db` brings (`KL_aaf_packetizer.sv`, #667) is byte-identical to dev's. Firmware architecture is unchanged since R525-1/R525-2. Both build modes keep their contract: the guard asserts in the NDEBUG-free RV32 build (`__assert_fail` open) and an `NDEBUG` build references no handler (W3).

[R525] PASS Robustness - `receipts/assert-witness.log` W1-W4, `receipts/asan-end-bound.log`, `receipts/ctrl-selftest.log` (re-entry 122+122), `receipts/nvm-selftest.log` - The negative paths of the resolution are all exercised: a missing header, a missing name, a broadened allowance (five foreign names, including `__assert_func`, `__assert` and a near-prefix), and a release build. The #677 boundary fails closed under ASan at the merged head. The #678 debug and release re-entry matrices and the inline-expiry probes pass in both modes, and the guard defects are caught.

[R525] PASS Tests - `receipts/rv32-selftest.log`, `receipts/selftest-header-witness.log`, `receipts/ctrl-selftest.log`, `receipts/nvm-selftest.log`, `receipts/tally.log`, `receipts/coverage-check.log`, `sw/firmware/gtest/fw_rv32_selftest.py:30-42` - #679's 17 checks are kept. The `assert.h` addition to the self-test can fail: it fails when the header is absent. The standing ctrl arm itself fails without the header or the name (W1, W2), and the `__unexpected_service` plant guards against a re-broadened prefix. All checks and planted defects from both sides are present and graded: 423 + RV32, 79/79, 435 + 5 RV32, 109/109, 18/18, and 14 files at 100%.

[R525] PASS Docs - `sw/firmware/gtest/README.md:339-360`, `sw/firmware/gtest/fw_rv32.py:4-6`, `sw/firmware/ctrl/test/ctrl_build.py:44-45`, `sw/firmware/ctrl/test/test_ctrl_firmware.py:35-39`, `sw/firmware/ctrl/README.md:60`, PR #684 body "Round 3", `receipts/docs-gates.log` - The text describes the three declared headers, the named `__assert_fail` interface, and the merged `rv32` docstring accurately. The PR body's merge, re-grade and witness claims were each reproduced independently. Docs gates pass. Both prior Docs findings remain resolved.

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `rv32_include/assert.h`; C11 probe; `nvm_klj2.c:298` + ASan witness; #677/#678/#679 acceptance against gate receipts; merge fidelity diffs | R525-3 (firmware C behaviour also covered by R525-1/R525-2 at `6c94e9f5`, unchanged since) | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| RTL | CLEAN | PR-vs-dev diff (firmware only); dev-side fidelity; `ctrl_build.py:42-46`; `adp.c:17,29`; NDEBUG witness | R525-3 (architecture of unchanged firmware: R525-1/R525-2 at `6c94e9f5`) | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Robustness | CLEAN | W1-W4 witnesses; ASan end-bound witness; re-entry arms; NVM campaign | R525-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Tests | CLEAN | rv32 self-test + header witness; ctrl self-test 79/79; NVM self-test 109/109; tally 18/18; coverage check | R525-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Docs | CLEAN | gtest README, `fw_rv32.py`, `ctrl_build.py` comment, merged docstring, ctrl README row, PR body Round 3, docs gates | R525-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |

Open: none at BLOCKER, MAJOR, MINOR or RESIDUE. SUGGESTION R525-3-S1 does not affect coverage.

## Real limits

- Not run by this reviewer: the builder bank, `fw_coverage.py --selftest`, the lwSRP arm and pin defects, the mailbox co-simulation, `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `act`, and any Vivado or hardware step. The NVM campaign ran as one full `--self-test --jobs 6` invocation, not in batches.
- The RV32 evidence is freestanding objects and their symbol inventory. It is not a linked image or a target assertion handler (see S1).
- The C11 probe ran the header's semantics on the host compiler. On RV32 it is compile-only plus symbol checks.
- Physical calibration was NOT RUN. Skipped hosted contexts are not hardware proof.
- Hosted Verilator shards 1, 2 and 4 were in progress at my snapshot.
- Checkout integrity after the probes: HEAD and tree match exactly, there are 0 status lines, the index equals the HEAD tree in modes, blobs and paths, and the submodule gitlinks match with clean submodules (`receipts/restore-check.txt`). All probes ran on copies or in-process patches under scratch.

## Pending manager duties

- Build and validate the candidate merge against live dev at the merge turn.
- Run the owed long local gates: `scripts/run_all_suites.sh` and `syn/yosys/run.sh`.
- Run the trusted-dev `act_ci.py --pr 684` replica and accept the exact-head hosted contexts, including the Verilator shards still running at my snapshot.
- Confirm the second independent positive verdict.
- Obtain explicit maintainer authorization before any merge, then check post-merge containment and close #677 and #678.

R525-3 FINISHED
