[R584] NEGATIVE - exact head 386b8e69e6f2fd0233e7a432e75c9d877c583a7b

# R584-2: internal cleared-context review of PR #705 (issue #697, lane 697c), round 2 and round 2b

- Exact head: `386b8e69e6f2fd0233e7a432e75c9d877c583a7b`, tree `adbf9c46415f9eed0d90da652020ab9ec78bb54f`. It is a merge commit. Its parents are round 2's head `38240ac4` and dev `aef7ac66605c4404900ce04cbaaeff88e41bb880` (F5, #700).
- Delta reviewed: `60e7b57c..386b8e69`. That is round 2 (`e11733db`, `a205dab9`, `38240ac4`), answering R584-1-F1/S1/S2 and R585-1-F1/F2, plus round 2b, the merge of dev `aef7ac66`.
- Source base `8b61b70902f3ebf118e56967277e2686731081bd`. Live dev at assignment: `554e61d299ef7ddb5aca6fb9ce0e6a6cd076d8cb`. That current-dev candidate is not reviewed here; the manager builds it at the merge turn.
- Read in this order:
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - issue #697 (acceptance 1 to 5, owner decisions 6074086970, 6074093506 and 6074191062, lane assignment 6091228902, pin ruling 6092176555, round 2 assignment 6092628778, round 2b assignment 6093389868, and the author's REVIEW READY comments 6093383132 and 6094033396);
  - the diff and its history;
  - the public evidence at `ec6854f6` `review-evidence/697c-r1`;
  - the exact-head hosted runs.
- I wrote my verdict and ledger draft (`receipts/draft_verdict_before_prior_findings.md`) before reading R584-1 and R585-1. Section 4 resolves or retains each of their findings.
- **Verdict: NEGATIVE on two MINOR findings.** Both are residues of the round-2 asks, of the same class as the findings they answer:
  - F1: a build configuration the boundary never judges;
  - F2: a stack-building target that skips the pin check.

  Every acceptance measurement I re-ran holds:
  - 35 of 35 linked RV32 images are byte-identical to dev `aef7ac66`;
  - the coverage rows on the hosted runners are identical to dev, file for file;
  - the hosted verdict lines are identical to dev by name, plus one new control;
  - F5's sources, tests, coverage rows and 74 AECP plants are unchanged;
  - R585-1's three escaped probes and R584-1's two pin probes are now refused by name.

## 1. What I ran (this exact head unless stated; receipts under `receipts/`, scripts under `scripts/`)

Toolchain: host gcc/g++ 16.2.1 and clang 23.1.1, GoogleTest headers from the system, CPython 3.14, and the pinned RV32 SDK (`riscv32-linux-gcc` 14.3.0). Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`) was identified but not needed, since no bench was rebuilt. This is not the CI-parity container (gcc 13.3). Dev was always built with its own scripts, in its own disposable clone at `aef7ac66`.

| Check | Result | Receipt |
|---|---|---|
| Boundary gate `ctrl_boundary.py --require-rv32 --selftest` | rc 0, PASS. 51 firmware units, host and RV32, 18 build modes, 376 preprocessings, 0 findings. 36 boundary controls and 15 pin controls, 0 misbehaved. The stack's own gate and its self-test ran. | `boundary_selftest_head.log`, `.rc` |
| Modes the gate derives | 32 builder files found, 18 modes. F5's `AECP_TEST_APP`, `AECP_TEST_MAILBOX` and `AECP_TEST_NVM` are picked up with nothing hand-listed. | `modes_at_head.txt` |
| Flags the derivation skips | 10 computed flags (f-strings) in builders: `IMAGE_SINKS`/`IMAGE_SOURCES` (`ctrl_image.py:351`), `AECP_TEST_INTERFACES`, `AECP_WIRE_INTERFACES`, `PP_ENTITY_CAPS`, `SRP_EXPECT_*`, `NVM_TALLY_SHAPE` and `FW_GTEST_LABEL`. Only the image pair feeds a unit the gate judges (see F1). | `computed_flags_scan.txt` |
| Boundary probes on the real path, in disposable copies. Stack plants are committed in the copy's submodule with the gitlink staged, so the pin passes and the boundary itself must name them. | **CAUGHT by name (8 of 8):** R585-1's `CTRL_REENTRY_ASSERT`-region include, the adapter reaching `acmp_fake.hpp` by its search-path name, and the `#ifndef NDEBUG` include; R584-1-S2's stack-test `mbx_hal.h` include; and four new probes: a stack test header including `mbx_contract.h`, an RV32-only (`__riscv`) stack include, an RV32-only firmware reach, and an `AECP_TEST_NVM`-only reach. **Escaped (2 gap probes):** an include under `IMAGE_SINKS > 1u` (F1), and a mode written as two tokens (S1). | `boundary_probes.log`, `.json`, `boundary_probe_logs/` |
| Shape probe | The same `IMAGE_SINKS > 1u` plant (stack `examples/adp_port.h`, then `#error PROBE-REACHED`): the gate passes it (rc 0). `ctrl_image.py` hits `PROBE-REACHED` at both its shapes, after the include resolved. The builders' values are 2/2 (1x1 tdm8) and 9/9 (8x8). The gate uses 1/1. | `shape_probe.log`, `shape_probe_outputs/`, `image_shape_values.txt` |
| Pin probes, in a disposable clone. 11 entry points: the `--stack-pin` CLI, `make stack-pin`, `make obj_fw/libctrlfw.a`, the MAAP differential in both modes, `aecp_arms`, `aecp_mutants`, `aecp_wire`, `ctrl_image`, the firmware gate and the boundary gate. | Pristine: accepted. A modified `src/maap.c`, an `assume-unchanged` edit (`git status` empty), a `skip-worktree` edit of `include/wire.h` (`git status` empty), and an untracked `include/extra.h` are each refused by all 11 entry points, naming the file (44 of 44). An edited `scripts/check_boundary.py` is refused by the CLI and the boundary gate. **Gap:** a poisoned `include/wire.h` is compiled by `make run-if2` with no pin refusal (F2). | `pin_probes.log`, `pin_probe_outputs/` |
| RV32 images, dev `aef7ac66` against the head | **35 of 35 ELF sha256 identical.** Each tree used its own `ctrl_image.py` (5 shapes) and `ctrl_srp_image.py` (5 shapes x 1/2 interfaces x without SRP / SRP / AECP), the same pinned compiler, and the same stand-in runtime archives. Distinct compositions give distinct hashes. | `image_compare.txt`, `image_runs/`, `runtime_archives.sha256`, `scripts/runtime/rt.c` |
| Coverage, from the hosted logs | 30 rows on each side, 0 differ: dev's firmware-unit job 114089603191 at `aef7ac66` against this head's job 114137888898. The core rows differ only in path. `srp_mbx.c` is 514/514 on both, so dev's ratchet row 515 is stale and the head's row equals dev's measurement. The 8 AECP rows are unchanged in the ratchet. | `hosted_dev_vs_head_compare.txt` |
| Campaign verdicts, from the hosted logs | 892 verdict lines at dev, 893 at the head. The only difference is one new coverage control, `[ok] the stack's sources and headers are measured, its tests and examples are not`. `mutants: 471 of 471 caught` on both. | `hosted_verdict_lines_*`, `.diff` |
| F5 unchanged | Between dev and the head, no file changes under `aecp/`, `test_aecp*.cpp`, `aecp_wire*.{cpp,hpp}`, `app/`, `test/ctrl_aecp_image.c` or `ctrl_nvm/`, except `aecp/README.md` (three lines on the stack's wire layer). The AECP `DEFECTS` table is 74 plants with 87 checks, and its sha256 of `repr` is identical on both trees (`92d08f9a...`). `ctrl_mutants.MUTANTS` is 471 on both. The stack's `tests/acmp_fake.hpp` is token-identical to dev's `sw/firmware/ctrl/test/acmp_fake.hpp` (1139 tokens, comments aside). | this report; `git diff aef7ac66 386b8e69 --` the paths named |
| Merge resolution (`git show --remerge-diff`) | `sw/firmware/ctrl/README.md` keeps the post-move `acmp/` row and F5's `aecp/` row. `ctrl_srp_image.py` keeps `source_tree` with the stack and F5's `aecp_inputs`/`verify_abi`/`--with-aecp`. Every other merge change is the stack wiring of F5's three tools, the boundary units and modes, and docs. No HDL changes (`git diff aef7ac66 386b8e69 -- hdl syn tb/common` is empty). | this report |
| Hosted checks at the exact head | The PR is now mergeable; hosted runs exist for `386b8e69`. `rtl-fast` run 38026314581 succeeded: firmware-unit, verilator-lint, yosys-elaboration and bdd-conformance all executed. docs-check, docs-check-no-git, elaborate and wire-accountability succeeded. `rtl-full` run 38026314601 completed with success: full-ci-gate, Yosys shards 0 to 3 and Verilator shards 0 to 4 executed and succeeded; Physical gPTP was skipped (nightly and manual only). firmware-unit fetched `third_party/tsn-c-stack` at `1a9f651c`, printed the pin before the firmware gate, and ran the boundary step with 0 findings and 0 misbehaved. All five Verilator shards fetched `third_party/tsn-c-stack` at `1a9f651c`. Shard 2 runs the `mbx` suite and reports `PASS mbx`. | `hosted_firmware-unit_114137888898.log`, `hosted_verilator_shard_job_*.log` |
| Review clone restored | HEAD and tree exact, status empty, index equal to the HEAD tree, and no assume-unchanged or skip-worktree flags. 1259 tracked blobs re-hashed with modes, 0 mismatches. Every gitlink is at its pin; the initialised tsn-c-stack and lwSRP are clean. All probes ran in disposable clones under `scratch/`. | `clone_restore_check.txt` |

## 2. Findings

### R584-2-F1 - MINOR - Conformance, Robustness, Tests, Docs - the image fixtures are judged only at a shape no builder compiles, so an include under a shape value escapes the boundary

`[R584] MINOR Conformance/Robustness/Tests/Docs — sw/firmware/ctrl/test/ctrl_boundary.py:112,162-173,421-427; sw/firmware/ctrl/README.md:90; docs/testing/CI_WORKFLOWS.md:58 — "every configuration the firmware builds" excludes the shape values its builders compile`

- **Authority and evidence.**
  - Round 2 item 1 (6092628778) answers R585-1-F1: "judge the boundary in every configuration the firmware builds".
  - The gate's docstring (`ctrl_boundary.py:36`), `sw/firmware/ctrl/README.md:90` and `docs/testing/CI_WORKFLOWS.md:58` all state that it does. The gate prints "in every configuration of 18 build modes".
  - The derivation drops every flag a builder computes (`ctrl_boundary.py:162-173`, f-strings). Instead it hand-lists `-DIMAGE_SINKS=1u -DIMAGE_SOURCES=1u` in `FIRMWARE_DEFINES` (`:112`).
  - The only builder of `test/rv32_image/image_main.c`, `ctrl_image.py:351`, compiles it with `IMAGE_SINKS`/`IMAGE_SOURCES` equal to 2/2 (shipping 1x1 tdm8) and 9/9 (8x8) (`receipts/image_shape_values.txt`). The gate therefore judges this unit only in a configuration that is never built, and in none that is.
  - The generated entity headers (`generated()`, `:421-427`) are likewise written from the single `SRP_ENTITY` config, while the SRP and AECP image fixtures compile five shapes.
- **Probe** (`receipts/shape_probe.log`, `boundary_probes.log`). I planted this in `image_main.c`:

  ```c
  #if IMAGE_SINKS > 1u
  #include "../../../../../third_party/tsn-c-stack/examples/adp_port.h"
  #endif
  ```

  The gate passes it (rc 0, `ctrl_boundary: PASS`). `ctrl_image.py --shape endstation_ax7101_1x1_tdm8` and `--shape endstation_ax7101_8x8` both compile the branch. A following `#error` fires only after the stack-example include has resolved. The unconditional form of the same reach is a refused control (`image source reaches a stack test's header`). This is the R585-1-F1 class again: an include behind a configuration the gate does not try.
- **Impact.** A firmware or image unit can reach a stack-private header (`examples/`, `tests/`, `src/`) under a shape-dependent condition. Every shipped image would carry it, and the boundary gate would pass. Three documents claim the opposite.
- **Required outcome.** One of these:
  - The units are judged under the shape values their builders actually compile. Derive them from the builders and the configs, not from a hand-listed 1/1: at least the `ctrl_image.py` shapes for the image fixtures, and the per-shape generated headers for the SRP and AECP fixtures. Add a planted control under a shape value, refused by name.
  - Or a recorded decision bounds the property to the derived `-D`/`-U` modes, with the docstring, `sw/firmware/ctrl/README.md:90`, `docs/testing/CI_WORKFLOWS.md:58` and the gate's summary line saying exactly that.
- **Verification.** Re-run `scripts/shape_probe.sh` and `scripts/boundary_probes.py`. The shape row must read CAUGHT by name, or the corrected text must match what the probe shows. `ctrl_boundary.py --require-rv32 --selftest` must PASS with the new control.

### R584-2-F2 - MINOR - Conformance, Robustness, Tests, Docs - the mailbox bench's `run-if2` builds against the stack without the pin check

`[R584] MINOR Conformance/Robustness/Tests/Docs — tb/verilator/mbx/Makefile:45,112-118; tb/verilator/mbx/README.md:16-18; sw/firmware/ctrl/README.md:103 — one target of the mailbox bench compiles the stack's headers unpinned`

- **Authority and evidence.**
  - Round 2 item 2 (6092628778) asks that "every gate that builds the stack refuses an off-pin or modified stack". It names the `mbx` suite (`tb/verilator/mbx/Makefile`).
  - `Makefile:45` says the pin check "runs before every firmware build". `sw/firmware/ctrl/README.md:103` lists "the mailbox bench" among the gates that run it.
  - Only `obj_fw/libctrlfw.a` has the order-only `| stack-pin` (`:79`).
  - `run-if2` (`:112-118`) compiles the firmware's host model `sw/firmware/ctrl/host/mbx_model.c` with `$(FW_INC)`, which holds `-I$(STACK_DIR)/include`. That model includes `mbx_wire.h`, which includes the stack's `wire.h` (inline code). It does this with no `stack-pin` prerequisite.
- **Probe** (`receipts/pin_probes.log`, `pin_probe_outputs/S6.out`, disposable clone). I appended `#error PIN-PROBE` to the submodule's `include/wire.h`. Then `make -C tb/verilator/mbx VERILATOR=true run-if2` compiled `host/mbx_model.c` against it: the build stops on the poisoned header (`wire.h:46: error: #error PIN-PROBE`), not on a pin refusal. In the same clone, every other entry point refuses the same class of edit by name (44 of 44).
- **Scope.** The hosted path is protected. `scripts/run_all_suites.sh:394` runs `make` (target `all`), where `run-cosim`, and so `stack-pin`, precedes `run-if2`. The gap is the documented stand-alone target (README item 4).
- **Impact.** A local `make run-if2` result can come from an unpinned or edited stack, while three statements promise a refusal. This is the part of R584-1-F1 / R585-1-F2 that remains.
- **Required outcome.** `run-if2`'s firmware compile depends on `stack-pin` as `obj_fw/libctrlfw.a` does, and a pin control covers it (as the `bench("obj_fw/libctrlfw.a")` arm does at `ctrl_boundary.py:754`). Otherwise, the three statements name exactly the targets that check the pin.
- **Verification.** Re-run `scripts/pin_probes.sh`. Row S6 must show `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/wire.h` with rc 2, or the corrected text must match.

### R584-2-S1 - SUGGESTION - Robustness - a mode written as two tokens is not derived

`mode_flags` (`ctrl_boundary.py:162-173`) reads only single-token constants (`"-DNAME"`). GCC also accepts `-D NAME`. A builder that writes `["-D", "CTRL_TWO_TOKEN_MODE"]` is not explored, and a plant under that mode passes (`boundary_probes.log`, gap row). No builder at this head uses that form (`computed_flags_scan.txt`), so this is optional. Either read a bare `-D`/`-U` followed by a constant, or refuse a builder that writes a bare `-D`/`-U`.

### R584-2-R1 - RESIDUE - Docs (PR body only) - relative links in the PR body do not resolve

The PR body's "Authoritative references" links `../sw/firmware/ctrl/aecp/README.md`, `../sw/firmware/ctrl/README.md`, `../sw/firmware/gtest/README.md`, `../docs/reference/SUBMODULES.md` and `../docs/testing/CI_WORKFLOWS.md`. In a pull-request description, these resolve against the PR URL, not the repository tree. Exact fix: replace each with its blob URL at the head, for example `https://github.com/kebag-logic/milan-fpga/blob/386b8e69e6f2fd0233e7a432e75c9d877c583a7b/sw/firmware/ctrl/aecp/README.md`. The template's own `../CONTRIBUTING.md` links can follow the same form. This is wording only: it changes no measurement, claim or code.

## 3. Clean-lens evidence

```text
[R584] PASS RTL — git diff 60e7b57c..386b8e69 and aef7ac66..386b8e69 -- hdl syn tb/common (both empty); receipts/image_compare.txt (35/35 ELF identical to dev aef7ac66); tb/verilator/mbx/Makefile:46-80 (source and include lists unchanged but for the stack-pin order-only prerequisite); hosted rtl-fast 38026314581 (verilator-lint, yosys-elaboration, elaborate success) — no RTL or interface change; the firmware the RTL hosts links byte-identically at every shape and composition; the bench's RTL lists are unchanged
```

The checks below support the other lenses. They do not clear those lenses while F1 or F2 is open.

- **Conformance.**
  - Acceptance 1 (pin `1a9f651c` per 6092176555; copies removed; lwSRP `9197193e` unchanged) still holds.
  - Acceptance 3 (35 of 35 images identical to dev) holds.
  - Acceptance 4 (coverage rows identical to dev on the hosted runners; verdicts identical by name) holds.
  - Round 2 items 2 to 5 and round 2b items 1 to 3 are met, except for F1 and F2.
  - F5's AECP stays in milan-fpga (`aecp/` unchanged), and the boundary now judges it (the AECP controls and my `AECP_TEST_NVM` probe).
- **Robustness.**
  - The pin check never reads the index: assume-unchanged, skip-worktree, untracked and script edits are all refused.
  - A missing submodule makes `stack_pin` refuse with exit 2.
  - RV32-only and debug-only plants are refused on both sides.
- **Tests.**
  - The 36 boundary and 15 pin controls behave at the head.
  - Each of my 8 refusal probes is refused by the finding it names.
  - The verdict lines equal dev's.
  - No AECP plant changed.
- **Docs.**
  - `sw/firmware/ctrl/README.md:56-130`, `sw/firmware/gtest/README.md` (R585-1-R5 applied, links pinned to `1a9f651c` with the `#ownership-and-dispatch` anchor present at `docs/PORTING.md:29`), `sw/firmware/ctrl/aecp/README.md:128-130`, `sw/firmware/ctrl/maap/README.md:171-172`, `tb/verilator/mbx/README.md:16-18` and `docs/testing/CI_WORKFLOWS.md:55-63,193-197`.
  - The counts in the README (33 refused plus 3 passing controls; 15 pin controls) match `PLANTS` and the arms.
  - The hosted docs-check and docs-check-no-git succeeded at this head.

## 4. Prior public findings on PR #705, resolved or retained at this head

| Finding | Status at `386b8e69` | Evidence |
|---|---|---|
| R584-1-F1 (MINOR): the MAAP differential and the `mbx` suite do not refuse an off-pin or modified stack | **Resolved in part, retained in part as R584-2-F2.** Both differential modes and `obj_fw/libctrlfw.a` refuse. `run-if2` does not. | `pin_probes.log` |
| R584-1-S1: the pin trusts `git status`; scripts and CMake are not covered | Resolved. | `pin_probes.log` S2, S3 and S5 |
| R584-1-S2: the stack's tests are outside the boundary | Resolved. | `boundary_probes.log` rows 4 and 5 |
| R585-1-F1 (MINOR): the boundary is judged in one configuration | **Resolved for the `-D`/`-U` modes** (the three escaped probes are now CAUGHT by name). **Retained in class as R584-2-F1** for builder-computed shape values. | `boundary_probes.log`, `shape_probe.log` |
| R585-1-F2 (MINOR) = R584-1-F1 | As for R584-1-F1. | |
| R585-1-S1: the pin does not cover the stack script | Resolved. | `pin_probes.log` S5 |
| R585-1-R1 to R4 (PR body) | Applied (PR body lines 129, 157, 166 and 173). | |
| R585-1-R5 (`sw/firmware/gtest/README.md` `adp.c` rows) | Applied (`38240ac4`). | `git show 38240ac4` |

## 5. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Issue #697 acceptance 1 to 5 with owner decisions and the pin ruling; round 2 items 1 to 5 and round 2b items 1 to 3; `image_compare.txt` (35/35); `hosted_dev_vs_head_compare.txt`; `hosted_verdict_lines_dev_vs_head.diff`; the F5 path diff; the AECP `DEFECTS` hash; `acmp_fake.hpp` token identity; the remerge diff; the hosted firmware-unit and shard logs | R584-2 | `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` |
| RTL | CLEAN | Empty `hdl`/`syn`/`tb/common` diffs against `60e7b57c` and `aef7ac66`; `tb/verilator/mbx/Makefile:46-80`; `image_compare.txt`; hosted verilator-lint, yosys-elaboration and elaborate at the exact head | R584-2 | `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` |
| Robustness | UNCLEAN (F1, F2) | `ctrl_build.py:186-281` (`STACK_PROVEN`, `blob_id`, `worktree_files`, `stack_pin`, CLI); `ctrl_boundary.py` (modes, explore, preprocess with stand-ins, both sides, tests side); `pin_probes.log` (5 spoils x 11 entry points, plus the gap); `boundary_probes.log` (10 probes); `shape_probe.log` | R584-2 | `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` |
| Tests | UNCLEAN (F1, F2) | `boundary_selftest_head.log` (36 + 15 controls); `ctrl_boundary.py:529-775` (`PLANTS`, `pin_controls`); the hosted campaign verdicts dev against the head; the AECP plant table on both trees; my probe receipts | R584-2 | `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` |
| Docs | UNCLEAN (F1, F2) | `sw/firmware/ctrl/README.md:56-130`; `sw/firmware/gtest/README.md` (the coverage section and rows); `sw/firmware/ctrl/aecp/README.md:125-131`; `sw/firmware/ctrl/maap/README.md:168-173`; `tb/verilator/mbx/README.md:13-20`; `docs/testing/CI_WORKFLOWS.md:55-63,193-197`; the module docstrings of `ctrl_boundary.py`, `ctrl_build.py` and `maap_differential.py`; the PR body (R1 residue only) | R584-2 | `386b8e69e6f2fd0233e7a432e75c9d877c583a7b` |

## 6. Real limits

- I used the host toolchain, not the CI-parity container: gcc 16.2.1 against CI's 13.3, and CPython 3.14 against 3.12. Coverage and the campaign verdicts come from the exact-head and dev hosted firmware-unit logs, not from local runs. I did not run the firmware gate, `fw_coverage.py`, the MAAP differential, the `mbx` bench, the AECP campaign, the wire comparison or the saved-state campaign locally.
- The SRP and AECP image comparison links both sides against the same stand-in runtime that I wrote (`scripts/runtime/rt.c`), not the Picolibc/compiler-rt archives. The identity therefore proves that dev and the head link the same firmware objects in the same order. It does not reproduce the published absolute hashes of those 30 images. The 5 `ctrl_image.py` images use no library, so they are the real images.
- Verilator shard 2/5 runs `mbx`. Its job log shows the submodule fetch at the pin and `PASS mbx`, but not the suite's own log. The `mbx` pin line (`tsn-c-stack at ...`) is therefore not seen in hosted evidence here; it would be in the suite-log artifact.
- No act, no Docker, no `act_ci.py` or its self-test, no PP, gPTP, Yosys or builder bank, and no hardware. Physical calibration NOT RUN. Skipped field contexts (Physical gPTP) are not hardware proof.
- No manager source bank is claimed or inferred at this head. Source-head execution evidence here is my own runs above, the author's published receipts and the exact-head hosted runs.

## 7. Pending manager duties

- Hosted and act acceptance at the exact head: accept the completed runs (`rtl-fast` 38026314581 and `rtl-full` 38026314601, both success) and the `verilator-suites`/`yosys-portability` contexts. Confirm from the `mbx` suite-log artifact that the pin printed before its firmware build. Run act through the audited-install bootstrap for the new `TRUSTED_SUBMODULES` entry.
- The current-dev merge candidate against live dev (`554e61d2...` at assignment): builder and native banks, at the merge turn.
- After F1 and F2 are fixed, re-review at the new head. F1 and F2 un-cover Conformance, Robustness, Tests and Docs. RTL is banked at `386b8e69` only for as long as no RTL-scope artifact changes.
- Carry R584-2-R1 to the residue checklist. S1 is optional.
- The author's open note on dev's `ctrl_image_runtime.py` default stack protector (`__stack_chk_guard` with `--with-aecp`) belongs in its own Issue, as they propose. My stand-in runtime avoided it by construction.

R584-2 FINISHED
