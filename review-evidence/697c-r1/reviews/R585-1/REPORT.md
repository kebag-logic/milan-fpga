[R585] NEGATIVE - exact head 60e7b57c962dce06ae8862b0992c98f20d1afe76

# R585-1: external review of PR #705 (issue #697, lane 697c)

Reviewer: [R585], cleared-context external reviewer. Round R585-1.
Head under review: `60e7b57c962dce06ae8862b0992c98f20d1afe76`, tree `16fc1d5d753a8733d6dbbd12f8aa31058da9a10d`.
Source base: dev `8b61b70902f3ebf118e56967277e2686731081bd`. Stack pin: tsn-c-stack `1a9f651cdf7846b8e10ac246a6ef6916960fbb92`.

Verdict: NEGATIVE, on two MINOR findings in the stack boundary and pin gates (F1, F2).
Every property the pin ruling asks for holds at this head, and each one was reproduced here:
- the cores are token-identical at the pin;
- 25 of 25 RV32 images are byte-identical;
- 471 of 471 control plants and 239 SRP and pin defects are caught, at base and head, with identical verdicts by name;
- coverage is identical file for file;
- the docs gates are green without submodules.

## 1. What was read, in order

1. `AGENTS.md`, `CONTRIBUTING.md` (local bar, submodule rules), `docs/README.md`.
2. Issue #697 body and every comment: owner decisions 6074086970, 6074093506 and 6074191062;
   lane assignment 6091228902; TAKEN 6091267846; REVIEW READY 6092168627; pin ruling 6092176555.
3. Interface authorities: `sw/firmware/ctrl/README.md`, `sw/firmware/gtest/README.md`,
   `docs/reference/SUBMODULES.md` and `docs/testing/CI_WORKFLOWS.md`. In tsn-c-stack at the pin:
   `README.md`, `docs/PORTING.md` and `scripts/check_boundary.py`.
4. `git diff 8b61b709..60e7b57c` (56 files) and the six commits.
5. Public evidence at `ec6854f6…/review-evidence/697c-r1` (HANDOFF, PR-BODY, pin-proof, pin-text-diff)
   and the PR body. When this round began, the PR had no review findings, only two review-start notices.

## 2. Findings

### F1 - MINOR - Conformance, Robustness, Tests

`[R585] MINOR Conformance/Robustness/Tests — sw/firmware/ctrl/test/ctrl_boundary.py:76,199-210 — the boundary is judged in one build configuration, but the firmware builds the stack in three`

- **Requirement and evidence.** Acceptance 2 and the lane scope (6091228902, item 3) require a gate
  that refuses any include from the stack into mailbox, platform, register-map or image code. The
  scope also adds the milan-fpga-side direction.
  - `ctrl_boundary.py` preprocesses the stack's side only under `C_FLAGS` and `RV32_FLAGS`, and both
    define `-DNDEBUG`.
  - The firmware side uses only `FIRMWARE_DEFINES` (`-DNDEBUG`, one shape).
  - The arms also build the stack and the adapters under `-DCTRL_REENTRY_ASSERT`
    (`ctrl_arms.py:47,52,81`) and under `-UNDEBUG` (`ctrl_arms.py:145,172`).
  - The pinned stack has code regions under both macros (`src/acmp.c:33`, `include/acmp.h:454`,
    `src/maap.c:6,17`).
- **Probe** (`scripts/boundary_probes.py`, receipt `receipts/boundary_probes.txt`), on copies only:
  - The stack already has a `#ifdef CTRL_REENTRY_ASSERT` region in `src/acmp.c`. Planting
    `#include "mbx_hal.h"` inside it passes both `ctrl_boundary.judge()` and the stack's own
    `check_boundary.py`: **ESCAPED**. The acmp arm compiles exactly that configuration, with `mbx/`
    on its include path.
  - The firmware adapter `acmp/acmp_mbx.c` reaching the stack's `tests/acmp_fake.hpp` under
    `#ifdef CTRL_REENTRY_ASSERT` passes `ctrl_boundary`: **ESCAPED**.
  - The same kind of include under `#ifndef NDEBUG` is also missed by `ctrl_boundary`. The stack's
    own gate catches it, because it builds Debug.
  - Control: the same include written unconditionally is refused by both gates.
- **Today's tree is clean.** The pinned tree passes every configuration
  (`receipts/boundary_configs.txt`): 0 findings with `-DCTRL_REENTRY_ASSERT`, with `-UNDEBUG`, and
  with both. So this is a gap in the gate, not a present violation.
- **Impact.** Either of two changes could make the stack depend on the mailbox HAL or on a firmware
  test header:
  - a later pin;
  - an honest edit inside the existing reentry-hook region.

  The milan-side gate cannot see either. The docs say the gate judges the stack under "the
  firmware's own flags" (`ctrl_boundary.py:8`, `sw/firmware/ctrl/README.md:78`). That covers less
  than what the arms actually build.
- **Required outcome.** Both sides are judged under every configuration the firmware builds them
  with: at least `C_FLAGS`, `-DCTRL_REENTRY_ASSERT` and `-UNDEBUG`, on host and on RV32 where it is
  built. Alternatively, enumerate the configurations from the arms, so that a new one cannot be
  missed. Add one planted control per configuration-only include, each refused by name.
- **Verification.** Re-run `scripts/boundary_probes.py`: rows 2 and 4 must read CAUGHT by
  `ctrl_boundary`. `ctrl_boundary.py --require-rv32 --selftest` must PASS with the new controls.

### F2 - MINOR - Robustness, Docs, Tests

`[R585] MINOR Robustness/Docs/Tests — sw/firmware/ctrl/README.md:84; sw/firmware/ctrl/test/ctrl_boundary.py:312; tb/verilator/mbx/Makefile:46-54; sw/firmware/ctrl/test/maap_differential.py:20-24 — "every gate that builds the stack" refuses an off-pin or edited stack, but two do not`

- **Requirement and evidence.**
  - The README says: "Every gate that builds the stack first refuses a submodule off its gitlink.
    It refuses one with edited sources, headers or tests too."
  - `ctrl_boundary.py:312` calls the pin check one "which every gate runs first".
  - `stack_pin` is called by the firmware gate, by coverage (through the firmware gate), by the
    boundary gate and by both image fixtures.
  - It is not called by the `mbx` Verilator suite, which the hosted Verilator shards run. It is not
    called by `maap_differential.py` either.
- **Probe** (`receipts/pin_gap_probe.txt`, in a disposable clone), with
  `third_party/tsn-c-stack/src/maap.c` edited:
  - `make -C tb/verilator/mbx run-cosim` builds the edited source and prints `RESULT: PASS`, rc 0.
  - `maap_differential.py` runs and passes, rc 0.
  - Control: `test_ctrl_firmware.py` refuses with
    `tsn-c-stack differs from the pinned 1a9f651c: src/maap.c`, rc 2.
  - The clone was restored afterwards, with 0 changes.
- **Impact.** A local bench or differential result can come from unpinned cores, while the docs
  promise a refusal. Hosted shards check out the gitlink clean, so hosted evidence is not affected.
- **Required outcome.** One of these two:
  - both build paths refuse an off-pin or edited stack before building, for example by running the
    same pin check in the bench's `obj_fw` rule and in `differential()`, each with a planted control;
  - the README sentence and the docstring name exactly the gates that check the pin.
- **Verification.** Repeat the probe. Either the bench and the differential refuse, or the corrected
  text names only gates that the probe shows refusing.

### S1 - SUGGESTION - Robustness

`[R585] SUGGESTION Robustness — sw/firmware/ctrl/test/ctrl_build.py:194-195 — the pin check does not cover the stack script that the boundary gate runs`

`stack_pin` checks only `src/`, `include/` and `tests/`. Yet `ctrl_boundary.py` runs the submodule's
`scripts/check_boundary.py`. When that script is edited, `stack_pin` still accepts the checkout
(`receipts/pin_scripts_probe.txt`). Consider adding `scripts/check_boundary.py`, or the whole
submodule worktree, to the clean check. This is optional: hosted checkouts are clean.

### Residue (wording only; changes no measurement, verdict, test or code)

- **R1 (PR body, Known limitations).** The body says "The MAAP differential and the mailbox bench are
  local gates, not in CI." But the bench is the `mbx` suite, which the hosted Verilator shards run
  (`make all`, including `mutants-quick`). That is why this PR fetches the stack there
  (`CONTRIBUTING.md:386-391`, `docs/testing/CI_WORKFLOWS.md:190-192`).
  Fix: "The MAAP differential is a local gate, not in CI. The mailbox bench runs in CI as the `mbx`
  Verilator suite."
- **R2 (PR body, Definition of Done).** The body says "(all met locally; the pin reading awaits
  confirmation, see Known limitations)". The pin was confirmed in 6092176555.
  Fix: "(all met locally; pin confirmed in #697 comment 6092176555)".
- **R3 (PR body, How to validate).** The body says "The detailed tables … are in the evidence
  comment." No evidence comment exists on the PR; the tables are in the published HANDOFF.
  Fix: replace "the evidence comment" with a link to `review-evidence/697c-r1/author/HANDOFF.md`
  at `ec6854f6`.
- **R4 (PR body, How to validate).** `python3 scripts/act_ci.py --selftest` is listed as a reviewer
  command. `AGENTS.md` section 5 allows the candidate copy's self-test only inside the disposable CI
  job boundary.
  Fix: "`python3 scripts/act_ci.py --selftest` (inside a disposable container or the CI job only,
  never on the host)".
- **R5 (`sw/firmware/gtest/README.md:245-246` and rows `312-316`).** The five `adp.c` exclusion rows
  say "The no-callback rule in `adp.h` prevents a port from interrupting these transitions". The
  pinned `include/adp.h` no longer states that rule: the stack's comment reduction moved it to
  `docs/PORTING.md#ownership-and-dispatch`. `fw_coverage.py` only checks that the reason is
  non-empty (`fw_coverage.py:329`).
  Fix: in rows 312-316, write "The no-callback rule of the stack's porting guide (Ownership and
  dispatch) prevents …". At line 245, write "The five `adp.c` rows cite the no-callback rule of the
  stack's porting guide, for the ports of `adp.h`".

## 3. Clean lens and evidence lines

```text
[R585] PASS RTL — git diff --stat 8b61b709..60e7b57c -- hdl (empty); receipts/mbx_bench_tallies.txt; receipts/image_hashes.txt; sw/firmware/ctrl/test/ctrl_build.py:57-62 — no HDL change; the mbx co-simulation (RTL plus firmware built from tsn-c-stack/src) gives identical tallies at base and head (382, 427, 32, 384, 429 and 369 checks, 0 failures; quick mutants 5 of 5); the link order and include path are proven unchanged in effect by 25 of 25 byte-identical ELFs
```

The checks below support the other lenses. They do not clear those lenses while F1 or F2 is open.

| Check | Evidence | Result |
|---|---|---|
| Token identity at the pin | `scripts/token_identity.py`, `receipts/token_identity.txt` | The seven files are token-identical at `ae982af`, `18d7378`, `74445d2` and `1a9f651c`. `51870377` is the first commit that differs (`src/adp.c`, 1736 vs 1762 tokens), and `98dc9e3` (main) differs too. Comments were stripped by the preprocessor, independently of the author's lexer. |
| Pin is on stack main; stack untouched | `receipts/stack_branches.txt` | `1a9f651c` is on `main`. tsn-c-stack `pushed_at` is 2026-10-09T20:37:54Z, before the lane assignment at 23:49:21Z. |
| lwSRP pin unchanged | `git ls-tree` at `8b61b709` and `60e7b57c`, `third_party/lwSRP` | `9197193e…` at both |
| RV32 images | `scripts/images.sh`, `scripts/compare_images.sh`, `receipts/image_hashes.txt` | 25 of 25 identical, with 25 distinct hashes. Each tree was built with its own scripts, the same pinned SDK and the same runtime archives. The five `ctrl_image.py` hashes also equal the author's published ones. |
| Control campaign | `receipts/fw_gate_summary.txt`, `receipts/raw/fw_*.log` | `mutants: 471 of 471 caught` at base and head; `test_ctrl_firmware: PASS`, rc 0 |
| SRP and lwSRP-pin campaigns | `receipts/fw_gate_summary.txt` | 239 verdicts (169 + 68 + 2), identical by name at base and head, 0 not ok |
| Plant equivalence | `scripts/plant_dump.py`, `scripts/plant_compare.py`, `receipts/plant_equivalence.txt` | 471 plants at both trees, 311 of them moved into the stack. Every planted program is token-identical to dev's. Only the two declared A29 needles change their words; arm and test stay the same. |
| No test lost | `scripts/test_names.py`, `receipts/test_names.txt` | Every base case of the five moved test files exists at head, in milan-fpga or in the stack; 12 cases were added. Arm tallies differ only in `adp` (26→34) and `acmp` (85→91), per `receipts/fw_arm_tallies_diff.txt`. |
| Coverage | `receipts/fw_coverage_check.txt`, `receipts/coverage_raw_compare.txt`, `receipts/fw_coverage_selftest_head.txt` | PASS at both trees: 22 files at 100 %, raw counts identical file for file (four paths moved); self-test 29 of 29. The ratchet's `srp_mbx.c` change from 515 to 514 matches the hosted dev measurement (`receipts/hosted_base_srp_mbx_coverage.txt`). This host's compiler reads 515 at both trees. |
| MAAP differential | `receipts/maap_differential.txt` | 16/16 at base and head, same plant names |
| Boundary gate as shipped | `receipts/raw/boundary_head.log` | PASS: the 15 boundary and 4 pin controls behave, and so do the stack's 12 |
| Behaviour without submodules | `receipts/docs_gates_nosubmodule.txt`, `receipts/nosubmodule_refusals.txt` | In a clone with no submodule, 19 docs-job commands return rc 0. The firmware, boundary and image gates refuse (rc 2). The differential and the bench stop on a compile or make error; neither passes silently. |
| Docs-job repository gates | `receipts/docs_job_repository_gates.txt` | 17 more commands return rc 0 with only the docs job's three submodules: idiom, naming, hygiene, TOC, archive and source-list gates |
| Hosted jobs that need the stack | `rtl-fast.yml:255,292`, `rtl.yml:161`, `ci_events.py:2125,2352,2380` | `firmware-unit` and every Verilator shard fetch it, and no other job builds firmware C. `ci_scope.py` reads gitlinks from `.gitmodules`, and a case for the stack is added at `:329`. |
| act manifest | `scripts/act_ci.py:234-238,10605-10760` (static reading only) | The stack is the sixth trusted entry, and `REQUIRED_SUBMODULES` gains it. Four refusal arms (drop, redirect, drop gitlink, extra gitlink) mirror lwSRP's. Not executed, because running it is forbidden here. |
| README and licence | `sw/firmware/ctrl/README.md:54-108`, `THIRD_PARTY.md:21`, `docs/reference/SUBMODULES.md:27,238-244`, `receipts/stack_readme_ctest.txt` | The README says what the stack provides, what it must not depend on, how to run its tests, and its licence: MIT inside CERN-OHL-W, with lwSRP as Apache-2.0. Its CMake/CTest commands pass (7 of 7). No milan-fpga file changed licence. |

## 4. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue #697 acceptance and rulings; `receipts/token_identity.txt`, `image_hashes.txt`, `fw_gate_summary.txt`, `coverage_raw_compare.txt`, `boundary_probes.txt` | R585-1 | 60e7b57c962dce06ae8862b0992c98f20d1afe76 |
| RTL | CLEAN | `hdl/` diff (none); `receipts/mbx_bench_tallies.txt`; `image_hashes.txt`; `ctrl_build.py:57-62` link order and include path | R585-1 | 60e7b57c962dce06ae8862b0992c98f20d1afe76 |
| Robustness | UNCLEAN (F1, F2) | `ctrl_boundary.py`, `ctrl_build.py:174-197`, `tb/verilator/mbx/Makefile`, `maap_differential.py`; `receipts/boundary_probes.txt`, `pin_gap_probe.txt`, `nosubmodule_refusals.txt` | R585-1 | 60e7b57c962dce06ae8862b0992c98f20d1afe76 |
| Tests | UNCLEAN (F1, F2) | `ctrl_boundary.py:233-341` controls; mutation tables; `receipts/plant_equivalence.txt`, `test_names.txt`, `fw_arm_tallies_diff.txt`, `maap_differential.txt`, `fw_coverage_selftest_head.txt` | R585-1 | 60e7b57c962dce06ae8862b0992c98f20d1afe76 |
| Docs | UNCLEAN (F2) | `sw/firmware/ctrl/README.md`, `sw/firmware/gtest/README.md`, `CONTRIBUTING.md`, `QUICKSTART.md`, `README.md`, `docs/reference/SUBMODULES.md`, `docs/testing/CI_WORKFLOWS.md`, `docs/design/MAILBOX_SPLIT.md`, PR body; `receipts/docs_gates_nosubmodule.txt`, `docs_job_repository_gates.txt` | R585-1 | 60e7b57c962dce06ae8862b0992c98f20d1afe76 |

Residue R1 to R5 leaves every lens as it is, and S1 is optional.

## 5. Limits and pending manager duties

- **Toolchain.** This host ran gcc 16.2.1 and CPython 3.14, not the CI-parity container (gcc 13.3,
  CPython 3.12).
  - GoogleTest and GoogleMock 1.14.0 came from a static install treated as system headers.
  - The MAAP differential linked the host's shared GoogleTest 1.18.0 at both trees. The static
    archives do not link in its argument order, at base and head alike.
  - Every comparison is base against head on this one host. Absolute coverage line counts can
    therefore differ from CI by toolchain: `srp_mbx.c` reads 515 here and 514 hosted.
- **SRP image runtime.** It was built from current public Picolibc, compiler-rt and LiteX sources,
  not from the author's archives. So the 20 SRP-image hashes differ from the author's table; they are
  equal between base and head here, which is the property under test. The five `ctrl_image.py`
  hashes equal the author's.
- **Not run here, by instruction:** `act_ci.py` and its self-test, Docker/act, hosted jobs, the full
  parent/PP/gPTP/Yosys/builder banks, and `test_ctrl_nvm.py`.
- **Hosted and act acceptance belong to the manager.** No hosted run exists at the exact head; the
  PR reports no checks. The manager's duties include:
  - the audited-install bootstrap for the changed trusted manifest;
  - confirming that the hosted `firmware-unit` job has CMake and Clang for the stack's own gate.
- **Manager banks.** No manager source bank ran at this head, and none is claimed. The current-dev
  merge candidate (live dev `aef7ac66605c4404900ce04cbaaeff88e41bb880`), with its builder and native
  banks, is the manager's at the merge turn.
- **Hardware.** Physical calibration NOT RUN; no hardware evidence is claimed.
- **Clone restored and verified** (`receipts/clone_restore_verification.txt`):
  - status is empty, and the index equals the head tree (mode and blob);
  - every tracked blob rehashes equal, and the gitlinks are unchanged;
  - `third_party/tsn-c-stack` and `third_party/lwSRP` are checked out clean at their gitlinks.
    They were uninitialised in the fresh clone and were initialised for this review.

## 6. Prior public review findings

The prior public findings were read only after sections 2 to 5 were written. When this round
started, the PR held only the two review-start notices. One review has been published since:
[R584-1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092573026), NEGATIVE at
this same head. Each of its findings is resolved or retained at `60e7b57c` as follows.

- **R584-1-F1 (MINOR; Docs, Robustness, Tests): RETAINED.** It is the same defect as F2 above, and
  my probe reproduces it independently (`receipts/pin_gap_probe.txt`). Nothing at this head changes
  it. Its Tests attribution is accepted: F2 is held under Robustness, Docs and Tests, since no control
  exercises the claimed refusal. That changes no lens state, because Tests is already UNCLEAN under F1.
- **R584-1-S1 (SUGGESTION; Robustness): RETAINED, optional.** It overlaps S1 above. My probe shows
  the `scripts/` part of it (`receipts/pin_scripts_probe.txt`). I did not repeat the
  `assume-unchanged` part.
- **R584-1-S2 (SUGGESTION; Robustness, Tests): RETAINED, optional.** The arms compile the stack's
  `tests/` with the firmware's include path (`ctrl_build.py:131-139`), and `ctrl_boundary.py` scans
  only `src/` and `include/`. I did not plant that probe myself.

F1 above (configuration-dependent includes) and R5 do not appear in R584-1. They are new in this round.

R585-1 FINISHED
