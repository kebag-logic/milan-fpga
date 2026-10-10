[R585] NEGATIVE - exact head 386b8e69e6f2fd0233e7a432e75c9d877c583a7b

# R585-2: external review of PR #705 (issue #697), delta 60e7b57c..386b8e69

- Head `386b8e69e6f2fd0233e7a432e75c9d877c583a7b`, tree `adbf9c46415f9eed0d90da652020ab9ec78bb54f`. This is a merge commit; its parents are `38240ac4` (round 2) and dev `aef7ac66` (F5).
- Source base `8b61b709`. I did not review live dev `554e61d2`; the manager's merge-turn candidate covers it.
- Reconstructed from: AGENTS.md and CONTRIBUTING.md; the #697 body and the owner and manager comments; the pin ruling 6092176555; the round-2 assignment 6092628778; the round-2b assignment 6093389868; the executor's REVIEW READY comments 6093383132 and 6094033396; the diff and history; the published round-1 evidence `review-evidence/697c-r1` at `ec6854f6`; and the hosted checks at this exact head.
- I read prior public findings (R584-1 and R585-1) only after my own pass over the diff, and after writing a draft verdict and ledger.

**Verdict: NEGATIVE.** There are two MINOR findings, both gaps of the same kind the round-2 assignment closed "by construction".
- The boundary gate does not judge the firmware headers in C++, although every arm compiles them that way. It also does not judge the image under the shape values the image builder compiles.
- The bench's documented `run-if2` target compiles the stack's `wire.h` with no pin check.

Every other round-2 and round-2b requirement I could test holds at this head:
- R585-1's three escaped probes and R584-1's two probes are each refused by name.
- Every stack builder refuses an edited stack and an edit hidden by `assume-unchanged`.
- F5 is intact.
- 35 of 35 images are byte-identical to dev.
- Coverage raw rows are identical to dev.
- The 843 campaign verdicts are identical to dev's by name.
- Hosted checks are green.

## 1. Findings

### R585-2-F1 - MINOR - Conformance, Robustness, Tests, Docs - the boundary does not judge firmware headers as the C++ the arms compile, nor the image at the shape values its builder compiles

`[R585] MINOR Conformance/Robustness/Tests/Docs — sw/firmware/ctrl/test/ctrl_boundary.py:453,112,162-171 — firmware units are judged only as C and only at the one-sink default shape`

**Authority**
- Round-2 assignment 6092628778, item 1: "judge the boundary in every configuration the firmware builds".
- Round-2b assignment 6093389868, item 1: the derivation covers what F5 added.
- Lane scope 6091228902, item 3: the milan-fpga-side direction.
- The #697 goal: the firmware "consumes the stack through its public headers only".

**The claims**
- `ctrl_boundary.py:36`: "Both sides are judged in every configuration the firmware's builders compile them in."
- `sw/firmware/ctrl/README.md:90`: "Every unit is judged in every configuration the firmware builds."
- `docs/testing/CI_WORKFLOWS.md:58`.
- `.github/workflows/rtl-fast.yml:287`.
- The PR body's Status line and Boundary row.

**Evidence**
- `firmware_side` preprocesses every firmware unit, headers included, with `-x c` only (`ctrl_boundary.py:453`). But the arms compile those headers as C++.
  - `test_adp.cpp` includes `adp_mbx.h`, and `test_acmp_mbx.cpp` includes `acmp_mbx.h`. Both are compiled with the arms' test include path, which adds the stack's `tests/` (`ctrl_build.py:138`).
  - Six firmware headers have `#ifdef __cplusplus` regions (`receipts/tested_macros.txt`): `acmp_mbx.h`, `acmp_nvm.h`, `adp_mbx.h`, `aecp.h`, `aecp_image.h` and `aecp_mbx.h`.
- The firmware defaults fix `IMAGE_SINKS=1u` and `IMAGE_SOURCES=1u` (`ctrl_boundary.py:112`). `mode_flags` drops every f-string flag as "a value, not a mode" (`ctrl_boundary.py:162-171`).
  - `ctrl_image.py` compiles `rv32_image/image_main.c` at both shipped shapes (`ctrl_image.py:93,351`). `endstation_ax7101_8x8` is built with 9 sinks (`receipts/runs/img-head.log`: "9 STREAM_INPUTs").
- Probes (`scripts/boundary_probes.py`). Each runs the gate's own `planted()` and `judge()` in the universe it derives, on host and RV32, against disposable copies (`receipts/boundary/*.log`):
  - n1: `acmp/acmp_mbx.h`, `#ifdef __cplusplus` region, `#include "acmp_fake.hpp"`: **ESCAPED** (no finding).
  - n2: `adp/adp_mbx.h`, `#ifdef __cplusplus` region, `#include "../../tsn-c-stack/src/adp.c"`: **ESCAPED**.
  - n3: `test/rv32_image/image_main.c`, `#if IMAGE_SINKS > 1u` around `#include "../../../tsn-c-stack/src/acmp.c"`: **ESCAPED**.
  - Controls in the same harness are all CAUGHT by name: R585-1's three classes (r1-*), a stack-test include, an AECP-mode region (n5) and a stack public header's C++ region (n6, through the tests side).
- Real path (`scripts/cplusplus_realpath.py`, `receipts/cplusplus_realpath.log`):
  - I planted `#include "acmp_fake.hpp"` in a copy of `adp/adp_mbx.h`'s C++ region.
  - The firmware's own `test_adp.cpp`, preprocessed exactly with the arms' test flags and include path, reaches `third_party/tsn-c-stack/tests/acmp_fake.hpp` through `adp_mbx.h`.
  - The same header preprocessed as C, the only language the gate uses, reaches nothing outside `include/`.
- Today's tree is clean: no existing `__cplusplus` region in those headers holds an `#include` (`receipts/tested_macros.txt`). This is a gap in the gate and its claims, not a present violation.

**Impact**
- A firmware adapter header can come to depend on the stack's test fakes or private sources in the C++ build that every arm compiles, or the image can at a non-default shape.
- The boundary gate would still print PASS "in every configuration of 18 build modes".
- The docs and the PR body state that every configuration is judged.

**Required outcome.** One of these two, with one planted control per form, each refused by name:
- The firmware side also judges each firmware header in C++, with the arms' test flags and include path. It also judges the image units at the shape values the image builders compile (both shipped shapes, or values derived from the builders).
- Or every claim (ctrl_boundary.py:36, README.md:90, CI_WORKFLOWS.md:58, rtl-fast.yml:287, the PR body) names exactly what is judged. It must state that C++ inclusion of firmware headers and non-default shape values are not judged.

**Verification**
- Rerun `scripts/boundary_probes.py <checkout> <work> n1-fw-header-cplusplus-fake` (and n2, n3). Each reads CAUGHT with a finding naming the header and the reached file, or the corrected text names the unjudged forms.
- `ctrl_boundary.py --require-rv32 --selftest` passes with the new controls.

### R585-2-F2 - MINOR - Conformance, Robustness, Tests, Docs - the mailbox bench's `run-if2` builds the stack's wire layer with no pin check

`[R585] MINOR Conformance/Robustness/Tests/Docs — tb/verilator/mbx/Makefile:112-118 — run-if2 compiles against $(STACK_DIR)/include with no stack-pin prerequisite`

**Authority**
- Round-2 assignment 6092628778, item 2: "every gate that builds the stack refuses an off-pin or modified stack. That covers … the `mbx` suite (`tb/verilator/mbx/Makefile`)".

**The claims**
- `tb/verilator/mbx/Makefile:44-46`: the shared pin check "runs before every firmware build, so a stack off its gitlink or differing from it is refused and never built".
- `sw/firmware/ctrl/README.md:99,103`: "Every gate that builds the stack first runs the same pin check", listing the mailbox bench.
- The PR body's Pin check row.

**Evidence**
- Only `obj_fw/libctrlfw.a` carries `| stack-pin` (`Makefile:79`). `run-if2` (`Makefile:112-118`) compiles `host/mbx_model.c` with `$(FW_INC)`, which holds `-I$(STACK_DIR)/include`. `mbx_model.c` includes `mbx_wire.h`, and `mbx_wire.h:22` includes the stack's `wire.h`.
- `tb/verilator/mbx/README.md:273` documents `make -C tb/verilator/mbx run-if2` as a standalone run.
- Probe (`scripts/pin_probes.sh`, `receipts/pin_probes.txt`, `receipts/pin/WIRE-mbx_run_if2.log`):
  - I appended `#error PLANTED_WIRE_EDIT` to the submodule's `include/wire.h`.
  - `make -C tb/verilator/mbx run-if2` compiled `host/mbx_model.c` against it: the error fires from `third_party/tsn-c-stack/include/wire.h:46`. No pin line and no refusal appear.
  - Control: `run-cosim` on the same edit is refused (`differs from the pinned 1a9f651c: include/wire.h`).
- Every other builder refuses, by name and with exit 2, both a plain edit and an `assume-unchanged` edit with an empty submodule `git status` (24 arms): `test_ctrl_firmware.py`, `fw_coverage.py --check`, `maap_differential.py` in both modes, `make run-cosim`, `aecp_arms.py`, `aecp_mutants.py`, `aecp_wire.py`, `ctrl_image.py`, `ctrl_srp_image.py --with-aecp`, `ctrl_boundary.py` and `ctrl_build.py --stack-pin`. An untracked `src/extra.c` is refused too.

**Impact**
- The documented two-interface run can build and run the host model on an unpinned wire layer with no refusal.
- The hosted path is not affected. The serial default `make` reaches `stack-pin` through `run-cosim` before `run-if2`, so it refuses.

**Required outcome**
- `run-if2`, and any other bench target that compiles against `$(STACK_DIR)`, runs the shared pin check first, with a planted control on `run-if2`.
- Or the claims name the exception.

**Verification.** Rerun `scripts/pin_probes.sh`. The `WIRE-mbx_run_if2` arm exits non-zero with `differs from the pinned 1a9f651c: include/wire.h` before any compile.

### R585-2-S1 - SUGGESTION - Robustness - a mode written as two arguments is not derived

`ctrl_boundary.py:162-171` matches only single literals such as `"-DNAME"`.
- A builder writing `("-D", "CTRL_SPLIT_MODE")`, which is valid for gcc, is not a mode. Probe n4 is ESCAPED, and its control n4c, written as one literal, is CAUGHT.
- No builder uses that form today: all 18 derived modes are single literals (`receipts/modes_universe.txt`).

Consider pairing an adjacent bare `-D` or `-U` constant with the next constant, or refusing a bare one in a builder.

### R585-2-S2 - SUGGESTION - Robustness - an explicit `--stack` pins that clone while the build still uses the submodule's tests

`aecp_arms.py:144` pins `args.stack`, but `aecp_arms.py:83` compiles the AECP tests with `-I{STACK_TESTS}`, which is always the submodule's `tests/` (`ctrl_build.py:56`). With `--stack` pointing at another clean clone, an edited `third_party/tsn-c-stack/tests/acmp_fake.hpp` would be built without a check. The default invocation is unaffected. This comes from reading the code; I did not run a probe for it.

Consider also pinning the submodule when `--stack` differs from it, or taking the tests from the stack given.

### Residue (PR body wording only; changes no measurement, verdict, test or code)

- **R585-2-RS1 (Status).** "Hosted runs and act have not run yet." Hosted runs completed green at `386b8e69` (`receipts/check_runs_386b8e69_final.tsv`).
  Fix: "Hosted checks at `386b8e69` are green (firmware-unit, the five Verilator and four Yosys shards, verilator-suites, yosys-portability); act has not run yet."
- **R585-2-RS2 (Known limitations).** "both ship on the hosted Ubuntu image, not yet observed on this PR."
  Fix: "both ship on the hosted Ubuntu image; the boundary step passed in `firmware-unit` at `386b8e69`."
- **R585-2-RS3 (How to validate).** "round 2's and round 2b's are in the lane packet's HANDOFF." That packet is not public; only `697c-r1` is under `review-evidence/` at `ec6854f6`.
  Fix: link the published round-2 and round-2b evidence once it is published. Until then, cite the REVIEW READY comments [6093383132](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093383132) and [6094033396](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6094033396).

## 2. Prior public findings at this head

| Finding | Status at 386b8e69 | Evidence |
|---|---|---|
| R584-1-F1 = R585-1-F2: the MAAP differential and the `mbx` suite built an unpinned stack | **Resolved for both named builders.** The differential (both modes) and the bench's firmware library refuse an edited and a hidden edit, by name, with exit 2. The bench's remaining `run-if2` path is new finding R585-2-F2. | `receipts/pin_probes.txt` (EDIT/HIDE maap_differential, maap_differential_selftest, mbx_run_cosim); `receipts/runs/boundary-selftest.log:47-50` |
| R584-1-S1: the pin trusted `git status` | **Resolved.** `stack_pin` hashes every file of `STACK_PROVEN` as a blob against the gitlink's tree and never reads the index (`ctrl_build.py:188-240`). The `assume-unchanged` edit (empty `git status`), an untracked file, an edited script and an edited CMake file are refused. | `receipts/pin_probes.txt` (HIDE-*, UNTRACKED-*); `receipts/runs/boundary-selftest.log:42-45` |
| R584-1-S2: the stack's tests were outside the boundary | **Resolved.** A `#include "mbx_hal.h"` plant in `tests/test_acmp.cpp` is refused by name. | `receipts/boundary/r1-stack-test-include.log` |
| R585-1-F1: boundary judged in one configuration | **Resolved for its probes.** The `CTRL_REENTRY_ASSERT` region of `src/acmp.c`, the adapter reaching `tests/acmp_fake.hpp` under `CTRL_REENTRY_ASSERT`, and `#ifndef NDEBUG` are each CAUGHT with their configuration label. The modes are derived from the builders. The C++ and shape-value configurations remain unjudged: new finding R585-2-F1. | `receipts/boundary/r1-*.log`; `receipts/modes_universe.txt` |
| R585-1-S1: the pin did not cover the stack's script | **Resolved.** `scripts/` and the CMake files are in `STACK_PROVEN`, and the script-edit control is refused. | `receipts/runs/boundary-selftest.log:42` |
| R585-1-R1 to R4 (PR body) | **Applied.** | `receipts/pr705_body.md` lines 166, 173, 157, 129 |
| R585-1-R5 (`adp.c` exclusion rows) | **Applied.** Line 245 and the five rows cite the stack's porting guide at the pin. | `git diff 60e7b57c 386b8e69 -- sw/firmware/gtest/README.md` |

## 3. Round-2 and round-2b checks

**Boundary.**
- My own run of `ctrl_boundary.py --require-rv32 --selftest` at the head passes: 51 firmware units, 18 build modes, 376 preprocessings, 0 findings, 36 boundary and 15 pin controls, 0 misbehaved. The stack's own gate and its controls pass (`receipts/runs/boundary-selftest.log`).
- The derived modes include F5's `AECP_TEST_APP`, `AECP_TEST_MAILBOX` and `AECP_TEST_NVM`, with nothing hand-listed (`receipts/modes_universe.txt`, 32 builders found).
- The documented counts match the code: 33 refusing plus 3 passing plants, and 51 units.

**Pin.**
- One shared check, `ctrl_build.stack_pin`, runs first in every builder I ran (`receipts/pin_probes.txt`, 27 arms). The one exception is `run-if2` (F2).

**F5 retained.** Of the 38 files dev changed since `8b61b709`, nine differ at the head (`receipts/f5_files_changed_at_head.txt`):
- Docs and README rows.
- Path and pin edits in `aecp_arms.py`, `aecp_mutants.py` and `aecp_wire.py`.
- `ctrl_srp_image.py` and `test_ctrl_firmware.py`.
- The ratchet's path moves.

No F5 C source, header or C++ test differs. F5 touched none of the moved cores or core tests.
- The 74 AECP plants hash identically at dev and the head (`scripts/tables.py`).
- The control table has the same 471 plants, by name, arm and test, with only paths moved into the stack (`receipts/ctrl_table_*.txt`); the two needle changes were disclosed in round 1.
- The stack's `tests/acmp_fake.hpp` is token-identical to dev's copy.
- AECP stays under `sw/firmware/ctrl/aecp/` (milan-fpga).

**Images.** 35 of 35 linked RV32 ELFs are byte-identical to dev `aef7ac66`.
- `ctrl_image.py` at five shapes: identical three ways, between the head, the head's harness on dev (`--base aef7ac66`, `+0` everywhere) and dev's own harness (`receipts/ctrl_image_elf_hashes.txt`).
- `ctrl_srp_image.py` at five shapes × one and two interfaces × without SRP, with SRP and with AECP: 30 of 30, linked at both revisions with the same stand-in runtime archives (`receipts/srp_image_elf_hashes.txt`, `receipts/standin_runtime_hashes.txt`).

**Coverage.** `fw_coverage.py --check` passes at both dev and the head (30 files). All 30 raw rows are identical, with dev's core paths mapped to the stack's: 4775 of 4779 lines and 3264 of 3289 branches raw at both (`receipts/coverage_raw_compare.txt`). The denominator is the same as dev's.
- `srp_mbx.c` measures 515 lines at both under this host's compiler and 514 under the hosted gcc 13.3 (`firmware-unit` log). The ratchet change from 515 to 514 is the hosted toolchain's count, as the PR body states, not a change in denominator.

**Kills.** `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` passes at both.
- 843 verdict lines, 774 names, identical by name, all `[ok]` (`receipts/verdicts_compare.txt`).
- `mutants: 471 of 471 caught` at both.
- MAAP differential at the head: the pin line first, then 16/16 caught (`receipts/maapdiff_summary.txt`).
- `make -C tb/verilator/mbx` at the head: the pin line before the firmware build, then 382, 427, 32, 384, 429 and 369 checks with 0 failures, and `mbx mutants: 5 of 5 caught` (`receipts/runs/mbx.log`).
- The gate plants (36 boundary and 15 pin) all behave.

**Hosted at the exact head** (`receipts/check_runs_386b8e69_final.tsv`):
- Every check succeeded, except "Physical gPTP (nightly and manual)", which was skipped, not executed.
- `firmware-unit` (job 114137888898): it fetched `third_party/tsn-c-stack` at `1a9f651c`, printed `mutants: 471 of 471 caught`, ran the boundary step (`ctrl_boundary: PASS`, 36 and 15 controls), and printed `firmware coverage: PASS (30 files)`.
- All five Verilator shards' logs show `Submodule path 'third_party/tsn-c-stack': checked out '1a9f651c…'`. Shard 2/5 owns `mbx`.
- I did not open the per-suite tally artifacts.

## 4. Lens evidence

```text
[R585] MINOR Conformance — R585-2-F1, R585-2-F2 (above)
[R585] PASS RTL — git diff --stat aef7ac66..386b8e69 and 60e7b57c..38240ac4 -- hdl syn constraints '*.sv' '*.v' '*.svh' (both empty); receipts/runs/mbx.log; receipts/ctrl_image_elf_hashes.txt; receipts/srp_image_elf_hashes.txt — no HDL change in the delta; firmware C sources differ from dev only by the removed cores and the two-line mbx_wire.h comment (round 1); RTL plus firmware co-simulation passes at the head with the round-1 tallies; link order and include path are unchanged in effect, shown by 35 of 35 byte-identical ELFs
[R585] MINOR Robustness — R585-2-F1, R585-2-F2 (above)
[R585] MINOR Tests — R585-2-F1, R585-2-F2 (above)
[R585] MINOR Docs — R585-2-F1 (ctrl_boundary.py:36, sw/firmware/ctrl/README.md:90, docs/testing/CI_WORKFLOWS.md:58, rtl-fast.yml:287), R585-2-F2 (Makefile:44-46, sw/firmware/ctrl/README.md:99,103); residue RS1 to RS3 does not affect coverage
```

Also examined, and clean apart from the findings above:
- **Conformance:** the pin against ruling 6092176555; acceptance 3 (images) and 4 (coverage and kills); round-2b items 1 and 2.
- **Robustness:** the edit, hidden-edit, untracked-file, script and CMake pin arms; the refusal when the submodule is missing (`stack_pin`'s top-level check).
- **Tests:** every new control behaves in my run; the campaign verdicts are identical to dev's; the probes' controls are caught.
- **Docs:** `sw/firmware/ctrl/README.md:60-109`, `sw/firmware/ctrl/aecp/README.md:125-130`, `sw/firmware/ctrl/maap/README.md`, `tb/verilator/mbx/README.md`, `docs/testing/CI_WORKFLOWS.md:50-66,190-197`, `docs/README.md` and the PR body.

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R585-2-F1, R585-2-F2) | #697 acceptance 1-5, assignments 6092628778 and 6093389868, ruling 6092176555; image hashes, coverage rows, verdict comparison, F5 file and table comparisons | R585-2 | 386b8e69e6f2fd0233e7a432e75c9d877c583a7b |
| RTL | CLEAN | empty HDL diffs over the delta; mbx co-simulation at the head; 35 identical ELFs | R585-2 | 386b8e69e6f2fd0233e7a432e75c9d877c583a7b |
| Robustness | UNCLEAN (R585-2-F1, R585-2-F2) | `ctrl_boundary.py`, `ctrl_build.py:188-240`, the bench Makefile, the AECP tools' `--stack`; 11 boundary probes, 27 pin arms | R585-2 | 386b8e69e6f2fd0233e7a432e75c9d877c583a7b |
| Tests | UNCLEAN (R585-2-F1, R585-2-F2) | boundary self-test (36+15), firmware gate self-test at dev and head (843 verdicts), MAAP differential 16/16, bench 5/5, coverage at dev and head | R585-2 | 386b8e69e6f2fd0233e7a432e75c9d877c583a7b |
| Docs | UNCLEAN (R585-2-F1, R585-2-F2) | READMEs, CI_WORKFLOWS, workflow comment, gate docstrings, PR body (RS1-RS3 are residue) | R585-2 | 386b8e69e6f2fd0233e7a432e75c9d877c583a7b |

## 6. Real limits

- **Toolchain.** The firmware, coverage and boundary runs used this host's gcc 16.2.1 with GoogleTest and GoogleMock 1.14.0, and the pinned RV32 SDK. The SDK archive's sha256 matches `scripts/ci_rv32_sdk.py`. This is not the CI-parity gcc 13.3 container. Every dev-against-head comparison used one toolchain for both.
- **Stack gate's compiler.** The stack's own boundary gate ran with this host's cmake and clang, not a pinned Clang 18.
- **Runtime archives.** The 30 SRP and AECP images were linked with reviewer stand-in runtime archives: byte-loop memory and string primitives, plus the repository's own `rv32_image/image_arith.c`. They were not the picolibc and compiler-rt archives of `ctrl_image_runtime.py`. Identity at dev and at the head proves the firmware's contribution identical, not the absolute bytes of the archived images.
- **MAAP differential.** It failed to link against the static GoogleTest 1.14.0 (`receipts/runs/maapdiff-static-gtest-link.log`). The `-lgmock -lgtest` libraries come before the objects; this ordering is unchanged in this delta and is not a finding. I ran it with the host's shared GoogleTest 1.18 instead.
- **Not run by me.** The AECP wire comparison, the saved-state store campaign and the tally listener campaign; `ci_events.py`, the docs gates, act and `act_ci.py --selftest` (forbidden); full parent, PP, gPTP and Yosys banks (out of scope).
- **No hardware or calibration.** Physical calibration was NOT RUN. Skipped hosted contexts are not hardware proof.
- **Clone state.** The `tsn-c-stack` and `lwSRP` submodules were initialised in this clone for the review, at their gitlinks. All probes ran on disposable copies or on the submodule worktree, restored after each arm. At the end, HEAD, tree and index match. All 1265 tracked files match their blobs and modes. No untracked or ignored file remains, and every required gitlink is at its pin and clean. `external` is uninitialised, as at the start; its receipt line shows the superproject's HEAD for that reason (`receipts/restore_verification.txt`).

## 7. Pending manager duties

- The current-dev merge candidate (live dev `554e61d2`): builder and native banks, and their receipts on the PR.
- act through the audited-install bootstrap. The PR changes `act_ci.py`'s trusted manifest.
- Publishing the round-2 and round-2b author evidence (see RS3), and applying RS1 to RS3 to the PR body.
- Hosted acceptance. This includes the `mbx` suite tally inside the Verilator shard 2/5 artifacts, which I did not open.
- After F1 and F2 are fixed: re-review of the boundary and pin under all five lenses at the new head.

## 8. Receipts

The receipts are listed in `MANIFEST.sha256`. Host-specific paths in them are replaced by `<checkout>`, `<packet>`, `<home>`, `<pinned-rv32-sdk>`, `<googletest-1.14.0>` and `<verilator-5.050>` (`scripts/sanitize.py`).

R585-2 FINISHED
