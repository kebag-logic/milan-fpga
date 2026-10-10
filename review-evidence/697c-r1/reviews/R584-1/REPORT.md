[R584] NEGATIVE - exact head 60e7b57c962dce06ae8862b0992c98f20d1afe76

# R584-1: internal cleared-context review of PR #705 (issue #697, lane 697c)

- Exact head: `60e7b57c962dce06ae8862b0992c98f20d1afe76`, tree `16fc1d5d753a8733d6dbbd12f8aa31058da9a10d`.
- Source base: dev `8b61b70902f3ebf118e56967277e2686731081bd`. The current-dev merge candidate (live dev `aef7ac66605c4404900ce04cbaaeff88e41bb880`) is not reviewed here; the manager builds it at the merge turn.
- Authorities read, in order: AGENTS.md, CONTRIBUTING.md (2.2, 3), docs/README.md, issue #697 body (acceptance 1 to 5), owner decisions 6074086970, 6074093506, 6074191062, lane assignment 6091228902, pin ruling 6092176555, then the diff `8b61b709..60e7b57c` (six commits), then the public author evidence at `ec6854f6` `review-evidence/697c-r1` (HANDOFF.md, PR-BODY.md, pin-proof.txt).
- Prior public review findings on PR #705: none. The PR holds only the two review-start notices (6092180526, 6092181006). Nothing to resolve or retain.
- Verdict: NEGATIVE on one MINOR (F1). Every acceptance measurement I re-ran holds: token-identical cores at the pin, 25 of 25 images byte-identical, 471 of 471 plants caught by name on both trees, identical coverage, both boundary directions with planted controls.

## What I ran (all local, this exact head unless stated; receipts in `receipts/`)

Toolchain: host gcc/g++ 16.2.1 with GoogleTest/GoogleMock 1.14.0 as system headers; the pinned RV32 SDK installed by `scripts/ci_rv32_sdk.py` from the digest-checked archive (`d42680e9...b78f`, GCC 14.3.0); Verilator 5.050 (`--version`: `Verilator 5.050 2026-07-01 rev v5.050`). This is not the CI-parity container (gcc 13.3). Dev was rebuilt with dev's own scripts in a disposable worktree at `8b61b709`, never with head's harness.

| Check | Result | Receipt |
|---|---|---|
| Pin: cores token-identical to dev's copies (clang raw lexer, comments dropped) | `1a9f651c`: all 7 files IDENTICAL, same lines. `5187037` (#19): `src/adp.c` DIFFERENT (1736 vs 1762 tokens). `ae982af` is also identical. First-parent history of tsn-c-stack `main`: `5187037` is the first commit after `1a9f651c` that touches `src/` or `include/`. `1a9f651c` is on `origin/main`. | `token_identity.txt`, `tsn_c_stack_branches.txt` |
| RV32 images, every shape, before and after | 25 of 25 ELF sha256 identical: `ctrl_image.py` at 5 shapes, `ctrl_srp_image.py` at 5 shapes x 1/2 interfaces x with/without SRP. Every pair also equals the published table. | `images_run1.txt`, `images_compare.txt` |
| Image sensitivity control | A stack copy with `MAAP_PROBE_RETRANSMITS` 3u to 2u changes the 1x1 if1 nosrp image (`3ed7fdc5...` to `a2b122e5...`). | `image_sensitivity_control.txt` |
| Firmware gate `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`, slices 1/2 and 2/2, dev and head | All four PASS. `mutants: 236 of 236` and `235 of 235` on both trees. 1051 `[ok]` lines and 0 ESCAPED on each side, lwSRP pin controls ok. Once the per-plant count of failing checks is normalised, the two sides' verdict lines are identical (the counts differ because the stack adds tests). | `gate_fw-*.txt`, `fw_gate_verdicts_dev_vs_head.txt` |
| Plant equivalence (each plant applied to its own side's source) | 471 names on both sides: 160 identical plants, 311 re-pathed (43 re-anchored), all token-identical mutated programs, 0 different. Two killers changed words (`acmp-admit-ignores-another-talker`, `acmp-reset-forgets-the-admitted`). Their new needles are the first, fatal `ASSERT_EQ` messages at the stack's `tests/test_acmp.cpp:1826` and `:1873`; the old words remain on the following assertion. | `mutant_equivalence.txt` |
| No test case lost in the split | 108 dev test names (5 files), 0 missing at head across milan-fpga `test/` and the stack's `tests/`; 11 new from the stack. | `test_names.txt` |
| Coverage `fw_coverage.py --check --jobs 4`, dev and head; `--selftest` head | Both PASS (22 files). Raw lines/branches identical file for file, with core paths normalised (`acmp.c` 742/742 348/348, `adp.c` 204/206 95/102, `maap.c` 209/209 140/140, `wire.h` 10/10 2/2). Self-test 29 of 29. Dev's hosted firmware-unit job (run 37992340103, job 114029646010) measures `srp_mbx.c` 514/514, so the ratchet's 515 to 514 is a stale-entry correction. This host measures 515 on both trees. | `coverage_dev_vs_head.txt` |
| Boundary gate `ctrl_boundary.py --require-rv32 --selftest` | PASS, 0 findings, 34 firmware units, host and RV32; 15 boundary controls (13 refused by name, 2 passing) and 4 pin controls ok; the stack's own gate ran. | `ctrl_boundary_selftest_head.txt` |
| Boundary, my own real-path controls (plant committed locally inside a disposable worktree's submodule, never pushed; gitlink staged so the pin check passes and the real path runs) | `src/acmp.c` including `ctrl_pool.h`: FAIL, host + RV32 + the stack's own gate. `src/maap.c` including `../../../sw/firmware/ctrl/mbx/mbx.h`: FAIL, 5 findings. `tests/test_maap_debug.cpp` including `mbx_hal.h`: PASS (see S2). | `probe_boundary_realpath.txt` |
| Without the submodule | The boundary gate REFUSED (exit 2). The `mbx` suite fails loudly (`No rule to make target .../tsn-c-stack/src/adp.c`, rc 2). No silent skip. | `probe_boundary_without_stack.txt`, `probe_mbx_without_stack.txt` |
| `mbx` Verilator suite, dev and head | Identical: 382, 427, 32 (cosim), 384, 429, 369 checks, 0 failures; quick plants 5 of 5. | `mbx_suite_*.txt` |
| `maap_differential.py --self-test`, dev and head | 16 of 16 on both, the same plants. Run with the host's GoogleTest; the 1.14.0 static libraries hit a link-order error inside the Verilator build on this host only. | `maap_differential_selftest_*.txt` |
| Docs-job replay without `tsn-c-stack` (42 docs.yml commands, processor submodules as the job fetches them) | 42 of 42 rc 0 at head and the same at dev. Before the job's submodule fetch, the pre-fetch commands also pass with no submodules. | `docs_replay_*.txt` |
| `ci_events.py --selftest` | PASS (1757 items, 2387 arms), including `RV32 firmware-unit ctrl_boundary.py allows a stood-down compiler` caught. | `ci_events_selftest_head.txt` |
| lwSRP pin | Gitlink `9197193e...` before and after. | `tsn_c_stack_branches.txt` |
| tsn-c-stack never pushed to | No tsn-c-stack ref moved after the lane started (newest ref 2026-10-09 22:37 +0200; the lane was taken 2026-10-10 01:53 +0200). | `tsn_c_stack_branches.txt` |
| Review clone restored | HEAD and tree as above. 1227 tracked blobs and modes re-hashed with 0 mismatches. Index equals the HEAD tree, no assume-unchanged or skip-worktree flags. Every gitlink at stage 0 with its pin; initialised submodules clean; disposable worktrees removed. | `clone_restore_check.txt` |

I read the act manifest change statically only; running act or its self-test was out of bounds for me. `TRUSTED_SUBMODULES` gains the exact `.gitmodules` stanza (`scripts/act_ci.py:234-238`). `validate_submodule_manifest` (`act_ci.py:1676`) compares the parsed blob for exact equality, then the gitlink set. Each new arm (drop, redirect, drop gitlink, extra gitlink, `act_ci.py:10734`) therefore reaches a refusal. The lwSRP drop arm now drops lwSRP by name instead of the last entry.

Hosted CI: firmware-unit (`rtl-fast.yml:255`) and the Verilator shards (`rtl.yml:161`) fetch the submodule, and `ci_events.py` pins both. The only other jobs that build firmware are the docs/elaborate builder gates and the NVM host tests, and none of them builds the ctrl cores (no reference from `sw/builder` or `sw/litex`). The hosted RV32 compiler exists only where the SDK is installed, and `--require-rv32` refuses rather than skips in firmware-unit.

## Findings

### R584-1-F1 - MINOR - Docs, Robustness, Tests - two gates that build the stack do not refuse an off-pin or modified stack, but three statements say every gate does

- Where:
  - `sw/firmware/ctrl/README.md:84-85` ("Every gate that builds the stack first refuses a submodule off its gitlink. It refuses one with edited sources, headers or tests too.");
  - `sw/firmware/ctrl/test/ctrl_boundary.py:27-29`;
  - `sw/firmware/ctrl/test/ctrl_build.py:184-186` ("every gate builds the pinned cores and tests or none");
  - the PR body's Boundary row ("Every gate first refuses a stack that is off its gitlink or modified").
- Evidence: `sw/firmware/ctrl/test/maap_differential.py:20-25` builds the submodule's `src/maap.c` and `include/`, and its `--self-test` copies them, with no `stack_pin()` call. `tb/verilator/mbx/Makefile:43-55` compiles `$(STACK_DIR)/src/{adp,maap,acmp}.c` with no pin or cleanliness check. I edited `src/maap.c` in a disposable worktree's submodule (`git status`: ` M src/maap.c`):
  - `maap_differential.py` printed `RESULT: PASS`, rc 0 (`probe_maap_differential_modified_stack.txt`);
  - `make -C tb/verilator/mbx` passed every bench and `mbx mutants: 5 of 5 caught`, rc 0 (`probe_mbx_suite_modified_stack.txt`).

  The other builders do refuse: `test_ctrl_firmware.py` (including `--coverage`), `ctrl_image.py`, `ctrl_srp_image.py` with the default stack, and `ctrl_boundary.py`.
- Impact: a local MAAP differential or `mbx` co-simulation run can be produced from cores that are not the pinned ones, with no refusal. The firmware page promises refusal. `docs/reference/SUBMODULES.md` says dirty submodules invalidate local evidence. Hosted runs are unaffected because they check out the gitlink fresh. The defect is a false verification claim plus a missing refusal, not wording alone.
- Required outcome: one of two.
  - The MAAP differential (both modes) and the `mbx` suite refuse a stack that is off its gitlink or modified, each with a planted control.
  - Or the three statements and the PR body name exactly the gates that refuse, and state that the differential and the `mbx` suite do not.
- Verification: repeat the two probes. Either both refuse by name with a nonzero exit, or the corrected text matches the observed behaviour of every builder listed above.

### R584-1-S1 - SUGGESTION - Robustness - the stack pin check trusts `git status`

`ctrl_build.stack_pin` (`ctrl_build.py:183-199`) accepts a hidden edit. I appended to `src/adp.c` and set `git update-index --assume-unchanged`; `stack_pin()` returned the pin (`probe_stack_pin_assume_unchanged.txt`). It also does not cover `scripts/` or the CMake files, which `ctrl_boundary.py` executes from the submodule. The lwSRP pin (`ctrl_arms.lwsrp_pin`) has the same pattern, and it needs deliberate index manipulation, so this is optional. The per-blob hash proof that CONTRIBUTING 3 describes for `xvlog_gate.py` would close both gaps.

### R584-1-S2 - SUGGESTION - Robustness, Tests - the stack's tests are outside both boundary checks

`ctrl_boundary.py` judges only `src/*.c` and `include/*.h`, and the stack's own gate builds with `-DTSN_TESTS=OFF`. The ctrl arms compile the stack's `tests/` with the firmware's include path (`ctrl_build.compile_tests`). A real-path plant of `#include "mbx_hal.h"` in the stack's `tests/test_maap_debug.cpp` passed (`probe_boundary_realpath.txt`). The stack's standalone CI would fail such a test, because the header does not exist there, so this stays optional. Either compile the stack's tests without the firmware's directories, or add `tests/` to the stack-side scan under the test include path.

## Reviewer-owned completion ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #697 acceptance 1 to 5 as modified by owner decisions 6074093506/6074191062, assignment 6091228902 and pin ruling 6092176555, checked one by one: pin at `1a9f651c` (token identity, first change `5187037`); copies removed (diffstat); images byte-identical (`images_compare.txt`); lwSRP unchanged; every path updated (stale-path search over HEAD; docs replay); coverage 100 % with identical counts; kills identical by name; README "The TSN stack submodule" (`sw/firmware/ctrl/README.md:54-108`) with contents, must-not-depend list, test commands and MIT inside CERN-OHL-W; `THIRD_PARTY.md:21`; `.gitmodules`; `act_ci.py:234-238`. No firmware behaviour change (verdicts, images). | R584-1 | `60e7b57c962dce06ae8862b0992c98f20d1afe76` |
| RTL | CLEAN | No HDL file changes (diffstat). The `tb/verilator/mbx/Makefile:40-55` source and include lists, with the `mbx` suite identical to dev (`mbx_suite_*.txt`). Link order `ctrl_build.PORTABLE` (`ctrl_build.py:56-59`) unchanged apart from the stack prefix. RV32 objects linked into byte-identical ELFs with the image audit passing. MAAP differential against the parent `KL_maap.sv` 16 of 16. | R584-1 | `60e7b57c962dce06ae8862b0992c98f20d1afe76` |
| Robustness | UNCLEAN | F1 (off-pin or modified stack accepted by two gates). Also examined: missing-submodule refusals (boundary exit 2, `mbx` loud failure), `stack_pin` controls, the `stack_gitlink` stage-0 check, real-path boundary plants, the `--require-rv32` refusal arm, the `legacy_stack`/`base_tree` paths of the image readers. S1 and S2 are optional. | R584-1 | `60e7b57c962dce06ae8862b0992c98f20d1afe76` |
| Tests | UNCLEAN | F1 (the claimed pin refusal of every stack-building gate is not true of the differential and the `mbx` suite). Also examined and clean: firmware gate and all campaigns on dev and head with identical verdicts; plant equivalence 471/471; the two re-worded needles; no lost test names; `fw_coverage_selftest.py` `stack_scope` case (29/29); `ctrl_boundary.py` 15+4 controls plus my 3 real-path controls; `selftest_stack_manifest` read statically; `ci_events` 2387 arms; image sensitivity control. | R584-1 | `60e7b57c962dce06ae8862b0992c98f20d1afe76` |
| Docs | UNCLEAN | F1 (`sw/firmware/ctrl/README.md:84-85`, `ctrl_boundary.py:27-29`, `ctrl_build.py:184-186`, PR body). Also examined: `sw/firmware/ctrl/README.md`, `sw/firmware/gtest/README.md`, `sw/firmware/ctrl/maap/README.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/reference/SUBMODULES.md`, `docs/testing/CI_WORKFLOWS.md`, `README.md:191`, `QUICKSTART.md:157-162`, `CONTRIBUTING.md:383-391`, `THIRD_PARTY.md`, and the regenerated `submodule_boundaries` diagram (rendered PNG inspected). Links into the stack use pinned URLs, and the docs gates pass without the submodule. | R584-1 | `60e7b57c962dce06ae8862b0992c98f20d1afe76` |

## Real limits

- Host toolchain, not the CI-parity container: gcc 16.2.1 (CI gcc 13.3), CPython 3.14 (CI 3.12). Coverage of `srp_mbx.c` reads 515 here and 514 on the hosted runner, which is toolchain-dependent. Dev and head were compared under the same toolchain.
- The MAAP differential used the host's GoogleTest (1.18), because of a 1.14.0 static-library link-order error inside the Verilator build on this host.
- The docs replay covered 42 docs.yml commands. These were not run: the HDL reference build, the wavedrom checks, `make -C gptp-processor docs`, the builder and NVM firmware gates, the gPTP submodule doc gate, `act_ci.py --selftest`, the `docs-check-no-git` job, `test_ctrl_nvm.py`, `tally_selftest.py`, `ctrl_image_selftest.py` and `fw_rv32_selftest.py`.
- I ran no act, no Docker, no hosted job, no Yosys, PP, gPTP or builder bank. Physical calibration was NOT RUN. Nothing here is hardware evidence.
- The SRP-image runtime archives were rebuilt locally from Picolibc, compiler-rt and LiteX sources. Their hashes differ from the author's because archive metadata is not deterministic, yet the linked ELFs match the published hashes.
- No manager source bank is claimed or inferred at this head. Source-head execution evidence here is my own local runs above plus the author's published receipts.

## Pending manager duties

- Exact-head hosted evidence: at review time no check run exists for `60e7b57c`. The manager owns hosted acceptance (`rtl-fast` including the new firmware-unit step, the Verilator shards with the submodule, docs, elaborate) and the act run through the audited-install bootstrap for the new manifest entry.
- The current-dev merge candidate against live dev `aef7ac66...` (builder and native banks) at the merge turn.
- After F1 is fixed: re-review at the new head. F1 touches the Docs, Robustness and Tests lenses, and the fix may also change scope under the other lenses.
- Carry S1 and S2 as optional.

R584-1 FINISHED
