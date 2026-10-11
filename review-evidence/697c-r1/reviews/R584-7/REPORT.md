[R584] NEGATIVE - exact head 4cab445aa2475903b6cf8b87566d2c8a1e15e391

Round R584-7. Internal cleared-context review of issue #697 / PR #705 (lane 697c). Exact published head
`4cab445aa2475903b6cf8b87566d2c8a1e15e391`, tree `52c4164caae5e10e56f80313b5e556827da30d94`. Source base
`8b61b70902f3ebf118e56967277e2686731081bd`. The lane's own delta is `aef7ac66..4cab445a`, because `aef7ac66`
(dev with #700, F5 AECP) was merged in as `386b8e69`. Everything else in `8b61b709..4cab445a` is #700's, which
was reviewed on its own PR.

The verdict, findings and ledger were written before any earlier review report was read. The section on
earlier findings was added after; it changed no verdict.

## Verdict

NEGATIVE. Two MINOR findings are open.

- Acceptance 1 to 5 are met on the evidence below: the pin, the removed copies, the boundary gate and its
  planted controls, the byte-identical images, the updated references, coverage and kills, and the README.
- F1 (MINOR): the lane's shared stack pin check accepts another revision's stack under a `refs/replace` entry.
  It does not set `GIT_NO_REPLACE_OBJECTS=1`, which CONTRIBUTING requires of this class of pin proof (#236).
- F2 (MINOR): the firmware README's count of the boundary self-test's controls disagrees with the gate.

## Scope as reconstructed

- **Acceptance 1 to 5 of #697**, read through the owner's repository decision (comment 6074093506: option (b),
  the stack in its own repository as a pinned submodule) and the name decision (6074191062:
  `third_party/tsn-c-stack`).
- **Lane assignment 6091228902:** pin the newest tsn-c-stack commit whose cores match milan-fpga's copies;
  `git rm` the copies; RV32 images byte-identical at every shape; the lwSRP pin unchanged; a boundary gate in
  both directions with a planted control; every reference updated; coverage 100 % with the same denominator;
  every campaign keeps its kills; hosted jobs that need the stack check it out and nothing skips silently; a
  README note.
- **Pin ruling 6092176555:** the property is token-identical cores plus byte-identical images, not
  byte-identical files.
- **Manager's budget ruling of 2026-10-11** (`firmware-unit`'s headroom is #716's).

## Findings

### F1 - MINOR - Robustness, Tests, Docs - the stack pin check follows `refs/replace`, so it accepts another revision's stack

- **Where:** `sw/firmware/ctrl/test/ctrl_build.py:211-239` (`stack_pin`); its git calls at `:220` and `:224`
  go through `run` (`:103`), which sets no `GIT_NO_REPLACE_OBJECTS`. The claims it falsifies:
  - `sw/firmware/ctrl/README.md:165-166`: "Every file ... must hash to the gitlink's tree ... so an edit hidden
    from `git status` is refused too";
  - `sw/firmware/ctrl/test/ctrl_boundary.py:77-80`, the same claim;
  - `ctrl_build.py:212-215`: "every gate builds the pinned stack or none".
  - The controls that miss it are `sw/firmware/ctrl/test/ctrl_pin.py:248` (`pin_controls`, 20 controls).
- **Authority:**
  - CONTRIBUTING.md:476-483 (#236) states the rule for a pin proved byte by byte. Every Git call contributing to
    the decision sets `GIT_NO_REPLACE_OBJECTS=1`, because "a mutable `refs/replace/<pin>` must not make
    `git ls-tree <pin>` read a different commit while `HEAD` still prints the pinned id". The real-Git self-test
    installs that substitution and requires a refusal.
  - The same directory already follows the rule (`sw/firmware/ctrl/test/ctrl_reuse.py:55`).
  - The lane added `stack_pin` to prove the stack's bytes, in answer to R584-1-S1.
- **Evidence:** `receipts/probe_pin_replace_ref.txt` (script `scripts/pin_replace_probe.sh`). The probe uses a
  disposable clone of the stack with HEAD at the pin `1a9f651c`, and the files under `src/ include/ tests/
  examples/ scripts/` taken from the existing import commit `ae982af`, whose `src/` bytes differ from the pin.
  No commit was created.
  1. The clean clone at the pin is accepted.
  2. With the substituted files and no replace ref, the check refuses.
  3. After `git replace 1a9f651c ae982af`, it prints `ACCEPTED: tsn-c-stack at 1a9f651c...`. Meanwhile
     `git status` lists 64 changed paths, and `src/adp.c` on disk is not the pin's blob.
  4. The same check under `GIT_NO_REPLACE_OBJECTS=1` refuses.
  So in this state a plain `git status` check would refuse, but the hash proof accepts.
- **Impact:**
  - Every gate that runs the shared check builds a stack that is not the gitlink's while attesting `tsn-c-stack
    at <pin>`. Those gates are the host test and its coverage, the boundary gate, the MAAP differential, the
    mailbox bench's `stack-pin` prerequisite, both image fixtures and the AECP tools.
  - Hosted checkouts carry no replace refs, so CI is not affected today. The defect is in a lane-added proof
    whose documented purpose is to refuse exactly such hidden local substitutions.
- **Required outcome:**
  - Every Git call that decides the stack pin reads the real objects. That covers at least `rev-parse HEAD`,
    `rev-parse --show-object-format` and `ls-tree <pin>` in `stack_pin`.
  - A standing pin control installs `refs/replace/<pin>` with a differing tree on disk and requires a refusal by
    name.
  - The README and docstring claims hold as written.
- **Verification:** rerun `scripts/pin_replace_probe.sh <checkout> <stack repo> <work>`; step 3 must print
  `REFUSED`. `ctrl_boundary.py --selftest` must list the new pin control `[ok]`, with the 21 pin controls
  behaving.

### F2 - MINOR - Docs - the README's control count disagrees with the gate's own count

- **Where:** `sw/firmware/ctrl/README.md:151`: "It then plants 95 defects, each refused by name, and eight
  passing controls, where the firmware builders' capture is."
- **Evidence:**
  - `receipts/plant_counts.txt`: `ctrl_plants.PLANTS` at this head holds 104 firmware-run plants, 96 refused by
    name and 8 passing, plus 5 Verilator plants.
  - The gate prints `105 boundary ... controls` for the firmware run, which is the base plus 96 plus 8:
    `receipts/hosted_boundary_summaries_at_head.txt` and the PR body. The README's figures give
    1 + 95 + 8 = 104.
  - `receipts/boundary_selftest_full_head.log` counts 110 controls with the Verilator five.
  - The README was already one short at round 7 (93 against 94), and round 8 added two to each.
- **Impact:** an authoritative page misstates the size of the self-test that releases the boundary. It is a
  figure, not pure wording, so it is not RESIDUE.
- **Required outcome:** the README states the count the gate runs: 96 refused by name and eight passing, or
  wording that cannot drift from `ctrl_plants.py`.
- **Verification:** `python3 -c` over `ctrl_plants.PLANTS` (`receipts/plant_counts.txt`) agrees with the
  README sentence, and the gate's printed count equals 1 plus the two numbers.

### RES1 - RESIDUE - PR body only - stale "not pushed" statements

- **Where:** PR #705 body, Status: "`697-consume` -> `dev`, not pushed". Known limitations, last bullet:
  "Round 8: `firmware-boundary`'s 30-minute timeout is chosen for a new job (38 % locally); its hosted figures
  need a push."
- **Fact:** the head is published. Hosted rtl-fast run 38124499476 at `4cab445a` executed `firmware-boundary`,
  `firmware-verilator` and `firmware-unit` (`receipts/hosted_jobs_at_head.txt`), and the manager published the
  hosted figures (#697 ruling of 2026-10-11 08:57).
- **Exact fix:**
  - In Status, replace "— `697-consume` -> `dev`, not pushed;" with "— `697-consume` -> `dev`, published;".
  - Replace the Known-limitations bullet with: "Round 8: `firmware-boundary`'s 30-minute timeout is chosen for a
    new job (38 % locally); its hosted figures at `4cab445a` are in the manager's ruling on #697."

### S1 - SUGGESTION - Docs - cite exact-head hosted figures on the CI page

- `docs/testing/CI_WORKFLOWS.md` gives `firmware-boundary`'s figures from a replica at `0a9c5fa8`, and
  `firmware-verilator`'s from hosted `5b4f6fbe`, before the dependency pass.
- Both are accurate for the heads they name. The hosted figures at this head (13 min 34 s and 10 min 31 s, the
  manager's ruling) could replace them when the page next changes. This is optional.

## Evidence

All receipts are under `receipts/`, and the scripts under `scripts/`. Host toolchain: GCC 16.2.1, GoogleTest
1.18.0 and CPython 3.14. RV32 used the pinned Bootlin SDK (GCC 14.3.0), installed from its verified archive
into scratch with `scripts/ci_rv32_sdk.py` (archive sha256 `d42680e9...` checked). Verilator was the scoped
pinned 5.050 wrapper; `--version` printed `Verilator 5.050 2026-07-01 rev v5.050`. This is not the CI
container: these are source-head runs on a newer host toolchain.

In the receipts, host paths are replaced by `$PACKET` (this packet), `$CLONE` (the review clone at the head)
and `$PINNED_VERILATOR`. `probe_fw_realpath_gate_try1_unresolvable_path.log` is a first probe attempt whose
`../../../../` path did not resolve in the builders' copies. The gate refused it, exit 2, on the build failure.
The plant was then re-anchored through the stack's `include/` (`probe_fw_realpath.diff`).

| What | Result | Receipt |
|---|---|---|
| Pin: the removed cores against tsn-c-stack `1a9f651c`, comments stripped, token by token | 7 of 7 files identical. The only later stack commit touching `src/`/`include/` (`5187037`) differs, and nothing lies between them. | `token_compare_pin.txt` |
| lwSRP gitlink | `9197193e` at base and head | `clone_restore_check.txt` |
| Firmware sources changed in the lane | Only the deleted cores and a comment in `mbx/mbx_wire.h` (0 non-comment lines) | `firmware_sources_changed.txt` |
| RV32 images, each tree's own builders, the same runtime archives | 35 of 35 ELF hashes identical, `aef7ac66` against head: `ctrl_image.py` at 5 shapes; `ctrl_srp_image.py` at 5 shapes × 1/2 interfaces × SRP/no SRP/AECP | `images_base_vs_head.txt` |
| Image sensitivity control | A one-token change in base `adp.c` changes the ELF hash | `image_sensitivity_control.txt` |
| `ctrl_image.py --base aef7ac66` from head | `+0` in every section at both default shapes | `ctrl_image_base_delta_head.log` |
| Control campaign plants, base against head by name | 471 = 471, no name added or lost. All 471 mutated programs are token-identical (43 re-anchored). Kills are identical but for the two disclosed A29 message texts, whose checks are unchanged. AECP's 74 are identical. | `mutant_equivalence_base_vs_head.txt` |
| Core test names, base against head | All 108 base names present at head, plus 11 of the stack's own | `test_names_base_vs_head.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test`, 3 slices | rc 0 each. 59 arms `[ok]`; `mutants: 157 of 157` × 3 = 471 of 471; AECP 74, SRP 169 + 68 and both lwSRP pin arms `[ok]`; 0 escaped | `fw_selftest_head_summary.txt`, `fw_selftest_head_slice*.log` |
| `fw_coverage.py --check`, base and head, same compiler | Both PASS with 30 files. Raw line and branch counts are identical file for file, the core paths mapped. | `coverage_base_vs_head.txt`, `coverage_check_*.log` |
| `ctrl_boundary.py --require-rv32 --selftest`, every builder with Verilator | PASS: 0 findings; 110 boundary and 20 pin controls, 0 misbehaved; bench, MAAP differential and AECP wire `--every` exit 0 | `boundary_selftest_full_head.log` |
| Reviewer real-path probe, firmware side | Two edits in a disposable clone, each reaching `examples/adp_port.h` through the stack's `include/` by `../`: `maap/maap_csr.c` (C, every image), and `aecp/aecp_nvm.h` under `__cplusplus` (only the AECP NVM test). The gate FAILs rc 1 with 3 findings naming both. | `probe_fw_realpath.diff`, `probe_fw_realpath_gate.log` |
| Reviewer stack-side plants through the gate's control machinery | Six plants, each refused by name: K1 the mailbox contract (host), K2 the loop under `NDEBUG`, K3 the HAL (RV32 image), K4 the app from a stack test (C++), K5 the store's state port, K6 a mailbox header by a relative path. The pass control K7 passes. | `probe_stack_plants_gate.log`, `scripts/stack_plants_probe.py` |
| Pin check under `refs/replace` | ACCEPTED (F1) | `probe_pin_replace_ref.txt` |
| `--build-only` with `--self-test` or `--check` | Refused, rc 2 each | `build_only_refusals.txt` |
| tsn-c-stack's own CMake suite at the pin (GoogleTest 1.14.0) | 7 of 7 tests passed | `stack_own_suite_ctest.txt` |
| Docs and CI-model gates | `docs_check`, `check_submodule_docs` (and selftest), diagram `--check`/`--selftest`, `DOC_MAP --check`, doc style, solution docs, em-dash (pinned renderer), `ci_events --check` (1902 items) and `--selftest` (2610 arms), `ci_scope --selftest`, coverage selftest 29/29, `--stack-pin`: all rc 0 | `docs_and_ci_model_gates_head.txt` |
| Hosted, exact head, read-only inspection | rtl-fast run 38124499476: `firmware-boundary` (step PASS; 105 + 20 controls; Verilator builders named LEFT OUT), `firmware-verilator` (PASS) and `firmware-unit`, all success. docs run 38124499478 success. rtl-full run 38124499487 success (Physical gPTP skipped by design). | `hosted_jobs_at_head.txt`, `hosted_boundary_summaries_at_head.txt` |
| Clone restored | HEAD and tree exact; index equals the HEAD tree; 0 flagged entries; 0 byte or mode differences; no untracked or ignored files; all gitlinks at their pins and clean; no replace refs | `clone_restore_check.txt` |

## Earlier public findings on this PR, at this head

These are rounds R584-1 to R584-6 and R585-1 to R585-6, read after the verdict above. This round's parallel
external report was not read. Here, "standing control" means a line `[ok] boundary control ...` or
`[ok] tsn-c-stack pin control ...` in `receipts/boundary_selftest_full_head.log` (L).

| Finding | State at `4cab445a` | Evidence |
|---|---|---|
| R584-1-F1, R585-1-F2 (MAAP differential and bench built an unpinned stack) | Resolved | L: pin controls "the MAAP differential, a core source edited" and "...self-test, a core source edited" (exit 2); the bench targets refuse on a poisoned `wire.h`; Makefile order-only `stack-pin` |
| R584-1-S1 (the pin trusted `git status`) | Resolved as stated (hash proof; the assume-unchanged control in L). A new class is open as **F1** above (`refs/replace`). | L; `probe_pin_replace_ref.txt` |
| R584-1-S2 (the stack's tests outside the boundary) | Resolved | L: "a stack test includes the mailbox HAL"; reviewer plant K4 |
| R585-1-F1 (one build configuration judged) | Resolved by construction: the recorded compiles are judged | L: mode controls; reviewer K2 under `NDEBUG`; real-path probe under `__cplusplus` |
| R585-1-S1 (the pin did not cover the stack script) | Resolved | L: "a stack script edited" refused |
| R584-2-F1, R585-2-F1 (image at a fixed shape; headers only as C) | Resolved | L: "the image reaches a stack file under a shape's stream count", "...SRP shape header force-included", "...two-interface contract", "a firmware header reaches a stack test's fake in C++ only"; real-path `aecp_nvm.h` probe |
| R584-2-F2, R585-2-F2 (`run-if2` unpinned) | Resolved | `tb/verilator/mbx/Makefile` `run-if2: if2-gen \| stack-pin`; L: "make run-if2, the stack's wire.h poisoned: exit 2" |
| R584-2-S1, R585-2-S1 (a mode written as two tokens) | Resolved | L: "a mode a builder writes as two arguments" |
| R584-2-R1 (relative links in the PR body) | Resolved | 0 relative links in the PR body |
| R585-2-S2 (an explicit `--stack` still builds the submodule's tests) | Retained as SUGGESTION (the PR body states it is not addressed; the default invocation pins) | PR body, Known limitations |
| R584-3-F1 (a builder-named C++ source not followed) | Resolved | L: "a header only the MAAP differential's C++ source reaches ..." |
| R584-3-S1 (three forms) | Multi-word literal resolved by construction. The other two (a force-included header named as a constant; a pin recipe ignoring its exit status) are retained as SUGGESTION, as the PR body states. | PR body; L |
| R585-3-F1 MAJOR (`firmware-unit` timed out at 45 min) | Resolved: the boundary moved to `firmware-boundary`. Hosted at this head: `firmware-unit` success in 34 min 41 s, `firmware-boundary` in 13 min 34 s. | `hosted_jobs_at_head.txt`; manager ruling 2026-10-11 |
| R585-3-S1, R585-3-S2, R584-4-F1, R584-4-F2, R585-4-F1 (spellings not derived; computed or written sources) | Resolved by construction | L: "patsubst", "a Makefile computes a mode's name", computed-name and written-source controls |
| R584-5-F1 (driver spellings), R585-5-F1 (response file) | Resolved | L: `-Wp,`, `-Xpreprocessor`, `--define-macro=`, `-imacros`, precompiled-header and response-file controls |
| R584-5-F2 (Verilator-only configurations judged by no required job) | Resolved | `firmware-verilator` in the rtl-fast aggregate (`rtl-fast.yml`); hosted success at this head; L: V1 to V3 |
| R584-6-F1, R585-6-F1 (store sources not judged) | Resolved | L: N1; reviewer real-path probe (`maap_csr.c`) |
| R585-6-F2 (fixed include path; a builder-only shadow of a C header) | Resolved | L: Q7 |
| R585-5-S1 (a Python builder under `-I`/`-E` loads no audit hook) | Retained as a stated limit (README:138) | `sw/firmware/ctrl/README.md:138` |
| R585-5-S2 (recorder header cap) | Superseded: the round-7 recorder keeps no per-compile header texts | `ctrl_shim.py`, `ctrl_capture.py` (no cap) |
| R584-4-S2, R585-4-S1 (`firmware-unit` headroom) | Retained as SUGGESTION, ruled #716's scope by the manager | manager ruling 2026-10-11 |
| R584-4-S1, R585-4-S2, R585-5-S3, R585-6-S1 (cite hosted figures on the CI page) | Partly applied (hosted `5b4f6fbe` for `firmware-verilator`); the rest is carried as **S1** above | `docs/testing/CI_WORKFLOWS.md` |
| R584-3..6 and R585-3..6 RESIDUE items (stale or duplicated PR-body status lines) | Applied in their rounds; the stale lines at this head are **RES1** above | PR body |

## Lens ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 acceptance 1-5 with comments 6074093506, 6074191062, 6091228902 and 6092176555. `token_compare_pin.txt`; `images_base_vs_head.txt` (35/35) with the sensitivity control; `ctrl_image_base_delta_head.log`; `mutant_equivalence_base_vs_head.txt`; `coverage_base_vs_head.txt`; `test_names_base_vs_head.txt`; `firmware_sources_changed.txt`; boundary run and probes (acceptance 2); `sw/firmware/ctrl/README.md:56-199` (acceptance 5); workflow fetch lines (`rtl-fast.yml` firmware jobs, `rtl.yml` verilator-shards). The cores are token-identical, so no IEEE 1722/1722.1/Milan behaviour changes. | R584-7 | `4cab445aa2475903b6cf8b87566d2c8a1e15e391` |
| RTL | CLEAN | `rtl_paths_changed.txt` (no `hdl/`, `syn/`, contract or processor-gitlink change); `tb/verilator/mbx/Makefile` (order-only `stack-pin` prerequisite of `obj_fw/libctrlfw.a`, `run-cosim` and `run-if2`; stack sources and include path); `make -C tb/verilator/mbx`, `maap_differential.py --self-test` and `aecp_wire.py --every` exit 0 under pinned Verilator 5.050 in `boundary_selftest_full_head.log`; `mbx/mbx_contract.h` unchanged; hosted `firmware-verilator` success | R584-7 | `4cab445aa2475903b6cf8b87566d2c8a1e15e391` |
| Robustness | UNCLEAN (F1) | `ctrl_build.py:177-262` (pin, gitlink, legacy map), `probe_pin_replace_ref.txt`; `ctrl_boundary.py` classification (`:150-257`) against the probes; `ctrl_expand.py:253-270` (plain-environment baseline, so `CPATH` cannot widen the C implementation); `build_only_refusals.txt`; the refusal paths in the boundary log | R584-7 | `4cab445aa2475903b6cf8b87566d2c8a1e15e391` |
| Tests | UNCLEAN (F1) | `ctrl_pin.py:248` (`pin_controls`, no replace-ref control); `ctrl_plants.py` (`plant_counts.txt`); reviewer probes K1-K7 and the real-path probe; campaign summary; mutant equivalence; coverage comparison; `ctrl_mutants.unnamed_tests` (stack tests may be named by the stack's own table, and all 108 base tests are still named by milan's) | R584-7 | `4cab445aa2475903b6cf8b87566d2c8a1e15e391` |
| Docs | UNCLEAN (F1, F2) | `sw/firmware/ctrl/README.md` (stack section `:56-199`; count `:151`; pin claim `:165-166`); `sw/firmware/gtest/README.md`; `docs/testing/CI_WORKFLOWS.md`; `docs/reference/SUBMODULES.md`; `docs/design/MAILBOX_SPLIT.md`; `CONTRIBUTING.md`; `QUICKSTART.md`; `README.md`; `THIRD_PARTY.md`; `sw/firmware/ctrl/{aecp,maap}/README.md`; `tb/verilator/mbx/README.md`; PR body (RES1, S1); `docs_and_ci_model_gates_head.txt` | R584-7 | `4cab445aa2475903b6cf8b87566d2c8a1e15e391` |

## Real limits

- **Toolchain:** the runs used the host's GCC 16.2.1, GoogleTest 1.18.0 and Python 3.14, not the CI container's
  GCC 13.3, GoogleTest 1.14 and Python 3.12. The coverage comparison is base against head under one compiler.
  It is not the CI measurement.
- **SRP runtime archives:** built from the public Picolibc (`ad4203ce`), compiler-rt (`25a8bb51`) and LiteX
  (`b2759f69`) sources, the same for base and head. So the SRP-image hashes prove base equals head, but they do
  not reproduce the author's absolute hashes. The `ctrl_image.py` hashes match the author's.
- **Reviewer stack-side plants:** these go through the gate's own control machinery (planted copies compiled by
  the real builder functions). A real gitlink bump was not staged, to avoid creating commits.
- **Not run:** act, the host `act_ci` and its selftest, the full parent, PP, gPTP and Yosys banks, and any
  hardware. Physical calibration was NOT RUN; field skips are not hardware proof.
- **Hosted:** inspected read-only. All three runs at this head concluded success. The Yosys shards finished in
  under 40 s, which the manager should confirm is their expected exact-head behaviour.

## Pending manager duties

- Validate the current-dev merge candidate (source base `8b61b709`, live dev `ac2c5e77`) with the builder and
  native banks, and publish the receipts. No manager source bank ran at this head, and none is claimed here.
- Accept the hosted runs at this head (rtl-fast, docs and rtl-full, all success when inspected), and the act
  bootstrap for the new trusted submodule.
- Carry RES1 to the residue checklist.

R584-7 FINISHED
