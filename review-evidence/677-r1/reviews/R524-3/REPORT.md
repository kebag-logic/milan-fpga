[R524] NEGATIVE - exact head 34475e774dfe1c92c81fa51293668e64dc95fa85

R524-3: internal independent delta review of issue #677 / PR #684 (with the #678 scope), round 3 (merge only), at tree `46cc939a85be1aa400f15fbd7c72ea983ac88271`. The round applied all five lenses at this head. The merge and its resolution are correct. Specifically:

- `git diff 910f338d 232970db` matches the round-1 diff hunk for hunk, apart from the conflicted docstring.
- The `assert.h` resolution conforms to C11 7.2.
- The runtime allowance adds exactly one name.
- Both witnesses fail as claimed.
- Every gate and campaign passes.

One MINOR Docs finding remains open, so the verdict is NEGATIVE. The PR's `nvm_klj2.c` bound check adds 4 bytes of RV32 text to every shipped shape. The store README's measured size table still shows the pre-fix figures (#679's dev measurement). Fixing it changes figures, so under the owner rule it is not RESIDUE. Conformance, RTL, Robustness and Tests are CLEAN at this head. Docs is UNCLEAN.

## Reconstruction

Sources read, in this order:

1. AGENTS.md
2. Issue #677: body (frozen acceptance 1-3) and comments
   - assignment 6021510152
   - REVIEW READY 6024328677
   - correction 6024757146
   - round-3 assignment 6029754278
   - round-3 REVIEW READY 6030485056
3. Issue #678: body and ruling
4. Review start 6030497872
5. Interface authorities
   - `sw/firmware/ctrl/adp/adp.h:130-145` (the no-callback rule)
   - `sw/firmware/gtest/README.md` "RV32 object builds"
   - `scripts/ci_rv32_sdk.py` (SDK pin)
6. The history and diffs `6714181d..34475e77`
7. Public author packet `review-evidence/677-r1/author-r3/` at archive `215abe0160df5e054b89e917fe79fe22c287d723`, consulted only to corroborate after my own measurements

The four prior review comments on PR #684 (6024636464, 6024750681, 6024881372, 6024898348) were read only after this pass and its findings were complete.

The delta since the round-2 head `6c94e9f5` has two commits:

- `232970db` is a `--no-ff` merge of dev `910f338d`, which brings #673/#681 and #679/#683.
- `34475e77` changes five files:
  - `sw/firmware/gtest/rv32_include/assert.h` (new)
  - `sw/firmware/ctrl/test/ctrl_build.py`
  - `sw/firmware/gtest/fw_rv32_selftest.py`
  - `sw/firmware/gtest/fw_rv32.py`
  - `sw/firmware/gtest/README.md`

Against live dev `910f338d`, the PR changes 30 paths, all under `sw/firmware/`. No `hdl/`, `tb/`, `syn/`, `.github/` or `scripts/` path differs (`receipts/merge-vs-dev.diff`).

## Findings

**R524-3-F1 | MINOR | Docs | `sw/firmware/ctrl_nvm/README.md:351-355` ("Static sizes" table, `text` column) | Measured RV32 text figures do not match the code at this head**

- **Authority/evidence.** The section heading says these are "RV32I object sizes, compiled with the pinned SDK at `-Os`" (`:337`). The store gate prints those measurements (`test_ctrl_nvm.py:150`).
  - At this head, `receipts/gate-nvm.log` measures text = 12,116 / 12,132 / 12,124 / 12,124 / 12,136 for `endstation_arty_current`, `_ax7101_1x1_tdm8`, `_arty_4x4`, `_arty_8ch`, `_ax7101_8x8`.
  - The table says 12,112 / 12,128 / 12,120 / 12,120 / 12,132.
- **Causation** (`receipts/nvm-size-table-vs-measured.txt`; same pinned SDK, same gate, each commit in its own scratch copy):
  - At base `6714181d` and at dev `910f338d`, each table matches its own measurement exactly.
  - At `6c94e9f5` and at this head, every shape measures +4 bytes. That is the 3-line erased-payload `loaded` check at `nvm_klj2.c:298-300`, which this PR adds.
  - The defect has been present since round 1. Round 2 did not report it. The merge replaced the stale base figures with #679's equally pre-fix dev figures, so the table is still stale at this head.
  - The public author log `author-r3/logs/nvm-controls.log` (archive `215abe01`) shows the same five measured values.
- **Impact.** The store's authoritative module document misstates a measured figure for all five shipped shapes. It also loses the record that the #677 fix has a cost. This changes figures, so it is not wording-only and not RESIDUE.
- **Required outcome.** The text column of `sw/firmware/ctrl_nvm/README.md:351-355` matches the gate's measurement at the merge head: 12,116 / 12,132 / 12,124 / 12,124 / 12,136, in table order. The other columns (bss etc.) are unchanged and match.
- **Verification.** Run `MILAN_RV32_CC=<pinned SDK> python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` at the corrected head. Compare each `rv32 at ... text=` line with the table row whose bss matches. A reviewer re-covers Docs at that head.

**R524-3-S1 | SUGGESTION | Tests | `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:150` | Nothing ties the README size table to the measurement.** The gate prints the sizes but compares them with nothing, which is why F1 survived two positive rounds. An optional check, or a note in the table that names the gate line, would stop the next drift. Optional; it does not affect coverage.

### Prior public findings at this head

Both prior findings remain RESOLVED at this head. Neither was re-opened by the merge:

- **R524-1-F1 / R525-1-F1 (MINOR, Conformance, Docs): RESOLVED.** The current PR #684 body authority bullet cites "Milan v1.2 section 5.6.3 (Advertise state machine) and IEEE 1722.1-2021 section 6.2 (ADPDU)". This agrees with `sw/firmware/ctrl/adp/adp.h:9-10`.
- **R524-1-F2 / R525-1-F2 (MINOR, Tests, Docs): RESOLVED.** Correction comment 6024757146 stands. At this head, `sw/firmware/gtest/README.md:219` says "All fourteen rows" and the table under "Coverage exclusions" (`:223`) has 14 data rows, five of them `adp.c`. That is unchanged by the merge.

## Delta verification (what was checked)

1. **Textual conflict.**
   - `receipts/hunk-compare.txt` compares the round-1 diff (`6714181d..6c94e9f5`, `receipts/round1.diff`) with `910f338d..232970db` (`receipts/merge-vs-dev.diff`). It strips index lines and hunk offsets. The two are identical except for the `rv32` paragraph of the `test_ctrl_firmware.py` docstring.
   - `receipts/hunk-compare-devside.txt` makes the converse comparison: dev's `6714181d..910f338d` against `6c94e9f5..232970db`. They are identical except for the same docstring.
   - Neither side lost a check, arm, mutant or planted defect. The merged docstring (`test_ctrl_firmware.py:34-38`) keeps #679's text and names assertion interfaces.
2. **Semantic conflict.** At the merge commit `232970db`, the ctrl `rv32` arm fails with `adp.c:17:10: fatal error: assert.h: No such file or directory` (W1). At this head it passes, and `__assert_fail` is undefined alongside the previously allowed names (W2).
3. **Header conformance (C11 7.2)** (`receipts/c11-assert-probe.log`):
   - `assert` is redefined at every inclusion: `#undef` sits outside the guard, and the `NDEBUG` form is exactly `((void)0)`.
   - An active assertion evaluates its operand once. Re-inclusion under `NDEBUG` evaluates it zero times, and `#undef NDEBUG` plus re-inclusion re-enables it.
   - A failing assertion passes the argument text, `__FILE__`, `__LINE__` and `__func__` to a `_Noreturn` handler.
   - `static_assert` expands to `_Static_assert`.
   - The unit compiles `-std=c11 -pedantic -Wall -Wextra -Werror` on host gcc and on the pinned RV32 compiler.
   - A `-DNDEBUG` RV32 object has no undefined symbol.
   - `rv32_include` is placed on the include path only by `fw_rv32.includes` (`fw_rv32.py:42`), so no host build sees this header.
4. **The allowance is exactly one name.**
   - `ctrl_build.py:46` is `{"memset","memcpy","vsnprintf","__assert_fail"}` (W2b), and `fw_rv32.HELPERS` is unchanged and exact (`fw_rv32.py:24-26`).
   - Each of these is still refused: `malloc` (W5), `__unexpected_service` (W6), the newlib handler name `__assert_func` (W7), and the prefix sibling `__assert_fail2` (W8).
   - The store's `LIBC_OK` (`nvm_rv32.py:28`) is unchanged and has no assertion name. The store includes no `assert.h`.
5. **Witnesses.**
   - Removing the header makes the arm fail (W3).
   - Removing the name makes it fail with `symbols outside the C library and libgcc: __assert_fail` (W4).
   - An `NDEBUG` build passes without the name and lists no handler (W9).
   - `fw_rv32_selftest.py` fails without the header (W10).
   - The hostile sysroot poisons `assert.h` (`fw_rv32_selftest.py:30`), and the probe source includes it and uses `assert` (`:37`, `:42`). The self-test passes 17 checks at this head.
6. **#677/#678 evidence still holds.**
   - `nvm_klj2.c` and `adp.c`/`adp.h` are byte-identical to `6c94e9f5`.
   - The ASan erased-prefix binary runs in the default store gate (`gate-nvm.log`: "NVM erased prefixes under AddressSanitizer: checks: 1 failures: 0").
   - The three erased-payload defects are caught by `codec_erased_loaded_prefix`. The restored `end` bound crashes on signal 6, the sanitizer abort (`gate-nvmself-part1.log`).
   - The re-entry arms pass 122 + 122. `reentry-guard-removed`, `reentry-uncounted` and `reentry-not-ignored` are caught.
   - Coverage is 100 % lines and branches on 14 files, with the ratchet file unchanged in the delta.

## Executed evidence at 34475e77

All runs used the pinned SDK, installed from the local archive by the head's `scripts/ci_rv32_sdk.py` with digest `d42680e9…b78f` (receipt verified, GCC 14.3.0; `receipts/sdk-install.log`), selected via `MILAN_RV32_CC`. Host tools were GCC 16.2.1 and GoogleTest/GoogleMock 1.18.0.

| Command (from the clone root unless noted) | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 11` | all 9 arms PASS (rv32 undefined includes `__assert_fail`; reentry 122/122 each); campaign stopped by the 585 s wave limit after 75/79, all caught | `gate-ctrl-arms-and-partial-campaign.log` (rc 124) |
| `scripts/ctrl_campaign_slice.py i 4` ×4, repository `ctrl_mutants.campaign` on disjoint slices | 20+20+20+19 = 79/79 caught, each graded once (including `pool-falls-back-to-heap` via `rv32`) | `gate-ctrlmut{0..3}.log` |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | 5 shapes, 435 tests, all RV32 builds PASS | `gate-nvm.log` |
| `test_ctrl_nvm.py --require-rv32 --self-test --config configs/endstation_ax7101_1x1_tdm8.yaml --jobs 14` | 84 graded and caught before the 585 s limit | `gate-nvmself-part1.log` (rc 124) |
| `scripts/nvm_campaign_rest.py`, repository `self_test` on the 25 not yet graded | 25/25 caught; unnamed tests against all 109: none. Total 109/109 | `gate-nvmself-part2.log` |
| `fw_rv32_selftest.py --require-rv32` | 17 checks PASS | `gate-rv32self.log` |
| `fw_coverage.py --check --jobs 4` / `--selftest` | 14/14 files 100 % / 28 of 28 | `gate-coverage.log`, `gate-covself.log` |
| `tally_selftest.py --mutants` | 18/18 | `gate-tally.log` |
| `scripts/witness_probes.py` (W1-W10, scratch copies only) | 0 failures | `witness-probes.log` |
| `scripts/c11_assert_probe.sh` | rc 0 | `c11-assert-probe.log` |
| store gate at `6714181d`, `910f338d`, `6c94e9f5` (scratch copies) | all rc 0; size causation for F1 | `gate-nvm-at-*.log`, `nvm-size-table-vs-measured.txt` |
| `docs_check.py`; `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py --base 910f338d` and `--base 6714181d` (pinned Markdown venv, requirements digest `40cdefe0…2817`); `git diff --check` vs `910f338d` and `6c94e9f5` | all rc 0 (the first attempt without the pinned renderer refused with rc 2 and is kept) | `docs-gates-mdvenv.log`, `docs-gates.log` |

`scripts/run_gates.sh` was the first, detached launcher. Only its three short gates (rv32 self-test, coverage self-test, tally) completed. The long gates it started were stopped when the launching call returned, and were re-run with `scripts/run_wave.sh` as listed above.

Hosted contexts at the exact head, read-only:

- Executed and successful: `firmware-unit`, `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3, Verilator shards 0 and 3, `bdd-conformance`, `wire-accountability`, `changes`, `full-ci-gate`.
- Still in progress when read: Verilator shards 1, 2 and 4.
- Skipped: `Physical gPTP`. This is not hardware evidence.

The manager owns hosted/act acceptance.

## Lens results

[R524] PASS Conformance - `sw/firmware/gtest/rv32_include/assert.h:5-17`, `receipts/c11-assert-probe.log`, `sw/firmware/ctrl_nvm/nvm_klj2.c:296-300`, `sw/firmware/ctrl/adp/adp.c:27-35`, `sw/firmware/ctrl/adp/adp.h:130-145`, `receipts/hunk-compare.txt` - checked:
- the header against C11 7.2 (per-inclusion NDEBUG, single evaluation, diagnostic arguments, `static_assert`)
- #677 acceptance 1-3 and #678 acceptance 1-3, with byte-identical code since round 2 and all gates re-run here
- the round-3 assignment items 1-3: both sides kept, re-grades stated

[R524] PASS RTL - `receipts/merge-vs-dev.diff`, `receipts/hunk-compare-devside.txt`, `sw/firmware/ctrl/test/ctrl_build.py:42-46`, `sw/firmware/gtest/fw_rv32.py:24-42` - checked:
- No HDL/testbench/synthesis/workflow path differs from live dev.
- The merged RTL from dev (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv`) equals dev's bytes.
- The firmware build contract is unchanged except the named interface: the RV32 flags stay NDEBUG-free, with the ILP32 soft-float RV32I ABI and static-frame checks.
- `__assert_fail` takes the line number as `unsigned int`, the same width as the glibc prototype.

[R524] PASS Robustness - `receipts/witness-probes.log` (W3-W10), `receipts/gate-nvm.log:43`, `receipts/gate-nvmself-part1.log` (erased_payload_*), `receipts/gate-ctrl-arms-and-partial-campaign.log` (reentry arms and the 3 re-entry defects) - checked:
- missing-header and missing-name failure paths
- that heap, unknown double-underscore, foreign-handler and prefix-sibling dependencies are still refused
- that NDEBUG builds need no handler
- the exact-loaded-prefix ASan bounds
- re-entry assert/count/ignore at the merged head

[R524] PASS Tests - `receipts/gate-ctrlmut{0..3}.log` (79/79), `receipts/gate-nvmself-part{1,2}.log` (109/109, no unnamed test), `receipts/gate-rv32self.log` (17), `receipts/gate-coverage.log`, `receipts/gate-covself.log` (28/28), `receipts/gate-tally.log` (18/18), `receipts/witness-probes.log` - checked:
- every campaign and gate at this head
- that each new or regraded check fails for its defect: W3, W4 and W10 fail without the header or name, and W5-W8 still refuse
- that the ratchet and the exclusion table are unchanged

R524-3-S1 is optional.

[R524] UNCLEAN Docs - `sw/firmware/ctrl_nvm/README.md:351-355`, `receipts/nvm-size-table-vs-measured.txt`; also checked and correct: `sw/firmware/gtest/README.md:341-358`, `sw/firmware/ctrl/README.md:57-60`, `sw/firmware/ctrl/test/test_ctrl_firmware.py:34-38`, `sw/firmware/gtest/fw_rv32.py:1-7`, `ctrl_build.py:44-45`, the PR body authority bullet, `receipts/docs-gates-mdvenv.log` - R524-3-F1 is open.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `rv32_include/assert.h`, C11 7.2 probe, `nvm_klj2.c:296-300`, `adp.c:27-35`, `adp.h:130-145`, hunk comparisons, PR authority bullet | R524-3 (R524-2 covered the then-unchanged code at `6c94e9f5`) | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| RTL | CLEAN | PR vs live-dev diff (`sw/firmware/` only), merged dev RTL bytes, `ctrl_build.py:42-46`, `fw_rv32.py:24-42` | R524-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Robustness | CLEAN | witnesses W1-W10, ASan prefix test, erased-payload defects, re-entry arms and defects | R524-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Tests | CLEAN | ctrl 79/79, NVM 109/109, RV32 self-test 17, coverage 14 files plus self-test 28/28, tally 18/18 | R524-3 | 34475e774dfe1c92c81fa51293668e64dc95fa85 |
| Docs | UNCLEAN (R524-3-F1 open) | `ctrl_nvm/README.md:351-355` and the files listed above | R524-3 (round 2's clean Docs at `6c94e9f5` no longer applies: the README changed in this delta and the figure was already stale there) | 34475e774dfe1c92c81fa51293668e64dc95fa85 |

## Real limits

- **Not run here: the lwSRP arm and pin defects.** The private checkout is absent. The delta does not touch the lwSRP arm.
- **Not run here: the builder bank, `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `act`, Docker, and physical calibration or hardware.** All were outside this assignment. Field skips are not hardware proof.
- **Not re-measured: the README's "largest static frame is 128 bytes per shape" (`ctrl_nvm/README.md:340`).** The gate does not print it.
- **Both long campaigns ran in parts.** The ctrl campaign was graded as four disjoint slices through the repository's own `campaign()`, after one full-gate run that reached 75/79. The NVM campaign was graded in two parts through the repository's `self_test()`. This was because of the per-call time limit. Together the parts cover each defect exactly once.
- **The RV32 evidence covers objects, not a linked target image.** A debug target build would need a runtime `__assert_fail(expr, file, line, func)`. That is disclosed in the round-3 REVIEW READY and is not a finding.
- **The clone was restored after probing.** This review's early `--help` runs created 20 ignored `__pycache__` files at 05:49:17. They were removed. The clone is at HEAD `34475e77`, `git write-tree` = `46cc939a85be1aa400f15fbd7c72ea983ac88271`, there are no untracked or ignored files, the index equals HEAD, and the gitlinks are unchanged (`receipts/clone-integrity.log`). All probes ran in scratch copies.

## Pending manager duties

- Carry R524-3-F1 to the executor. After it is fixed, a reviewer re-covers Docs at the new head. The other four lenses stay banked here unless the fix touches their scope.
- Accept hosted results at the final head. Verilator shards 1, 2 and 4 were still running when read. Run the act replica.
- Build and validate the final current-dev candidate at the merge turn (source base `6714181d…`, live dev `910f338d…`).
- Record the still-owed long local gates (`run_all_suites.sh`, `syn/yosys/run.sh`).
- Note that physical calibration was NOT RUN.

R524-3 FINISHED
