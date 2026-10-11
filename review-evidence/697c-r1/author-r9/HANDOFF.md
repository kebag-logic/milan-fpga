# HANDOFF — lane 697c, [A583]

Issue: [kebag-logic/milan-fpga#697](https://github.com/kebag-logic/milan-fpga/issues/697), assignment comments 6091228902 (round 1), 6092628778 (round 2), 6093389868 (round 2b), 6094873968 (round 3), 6096148471 (round 4), 6097800045 (round 5), 6102039501 (round 6), 6104711137 (round 7) and 6105928035 (round 8).
Branch: `697-consume` from dev `8b61b70902f3ebf118e56967277e2686731081bd`, pushed as PR #705; PR #705 shows round 7's head `8436dfc0`.
Head: `4cab445aa2475903b6cf8b87566d2c8a1e15e391` (round 8: six commits on `8436dfc0`, not pushed).
Status: round 8 REVIEW READY at `4cab445aa`, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`) (see [Round 8](#round-8)); round 7 REVIEW READY at `8436dfc0b`, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (see [Round 7](#round-7)); round 6 REVIEW READY at `5b4f6fbeb`, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`) (see [Round 6](HANDOFF-rounds-2-6.md#round-6)); round 5 REVIEW READY at `92b5be188`, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (see [Round 5](HANDOFF-rounds-2-6.md#round-5)); round 4's REVIEW READY was comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937); round 3's was comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057), round 2b's 6094033396, round 2's 6093383132. Round 1: TAKEN 6091267846, REVIEW READY 6092168627; the pin was confirmed in 6092176555.
PR body: `PR-BODY.md` in this directory (round 2 to 8 sections added, round 5's residue applied; no PR edit made).

Every plant's verdict at the head equals dev's, plant by plant: at round 1, 471 control plants and 237 SRP defects, all caught at both; at round 2b, against dev `aef7ac66`, the same and F5's 74 AECP plants.

## Commits

| Commit | Subject |
|---|---|
| `fea74c5c8` | Add tsn-c-stack as a pinned submodule and trust it in the act manifest |
| `d2bd55c14` | Build the ADP, ACMP and MAAP cores from tsn-c-stack and remove milan-fpga's copies |
| `1aaada1ef` | Hold the TSN stack boundary from both sides and refuse an off-pin or modified stack |
| `eeb00e3ee` | Take the stack's words for the two A29 killers its tests now assert first |
| `6509efb78` | Name the stack pin check and its four controls on the control firmware page |
| `60e7b57c9` | Initialise tsn-c-stack wherever the docs run every Verilator suite |

One-line subjects, no body, no trailers, configured identity.

## Environment used for evidence

- CI-parity container (Ubuntu 24.04.5, CPython 3.12.3, gcc/g++/gcov 13.3.0, GoogleTest and GoogleMock 1.14.0): the firmware gate, its campaigns, coverage, the NVM gate and the harness self-tests. The act self-test also ran in a disposable container (no network, read-only tree, stubbed host tools).
- Host (CPython 3.14, gcc 16.2.1, clang 23.1.1, CMake 4.4.4): the image builds, the boundary gate, the docs and repository gates.
- RV32: the pinned SDK of `scripts/ci_rv32_sdk.py`, `riscv32-ilp32d--glibc--stable-2025.08-1` (archive sha256 `d42680e9…b78f`, GCC 14.3.0, Buildroot 2021.11-18033-g83947c7bb6, libgcc.a sha256 `d8ebca8c…af58`), selected with `MILAN_RV32_CC`.
- Verilator: the pinned 5.050 (rev v5.050), at most two builds at once.
- SRP image runtime: built once by `ctrl_image_runtime.py` from external Picolibc, compiler-rt and LiteX sources; `libc.a` sha256 `6c93b7f6ce811ea28835dbd3bd161abbeb55f42c7fbcf0186ce43604f65d7e51`, `libcompiler_rt.a` sha256 `dff1861be2cf0a23145dfd102f158052c4b852f52e37e9d7d2da66233a8d653c`; the same archives for before and after.
- Baseline: a detached worktree at `8b61b709` with its own submodules, built and run with the same tools.

## tsn-c-stack pin

Pin: `1a9f651cdf7846b8e10ac246a6ef6916960fbb92` ("Port the applicable milan-fpga requirements with origin and clause tracing").

How it was found, by diffing every commit of tsn-c-stack `main` against milan-fpga's copies at `8b61b709`:

| tsn-c-stack commit | Core sources against milan-fpga's copies |
|---|---|
| `ae982af` (import) | SPDX line only (MIT) |
| `18d7378` (comment reduction), `74445d2`, `1a9f651` | comments and SPDX only; every non-comment token identical, on the same line |
| `5187037` (#19, ADP discard change) and `98dc9e3` (main) | `src/adp.c` code differs (1736 vs 1762 tokens) |

`1a9f651` is therefore the newest commit whose cores are the same code, token for token and line for line. Evidence files in this directory:

- `pin-proof.txt`: the token comparison (clang's raw lexer, comments and whitespace dropped, `(kind, spelling, line)` compared) for all seven files at the pin, and the ADP difference at `5187037` and `98dc9e3`.
- `pin-text-diff.txt` (89,497 bytes): the full textual diff of the seven files, which is comment and SPDX lines only.

No tsn-c-stack commit holds files that are byte-identical to milan-fpga's copies: every one carries the MIT SPDX line (owner decision 6074086970), and from `18d7378` the comments are reduced (owner decision 6074811248). The assignment's "byte-identical core sources" is read as "identical code"; see the open questions.

The linked result is byte-identical: all 25 images (below). The `rv32` arm's object sizes and open symbols are unchanged.

## Changes (file:line at head)

Step 1, submodule and trust:

- `.gitmodules:16` adds `third_party/tsn-c-stack` (HTTPS URL); the gitlink is `1a9f651c`.
- `scripts/act_ci.py:235` adds the stack to `TRUSTED_SUBMODULES`; `:10607` six-entry fixture and five-pin materialization; `:10734` `selftest_stack_manifest` (drop, redirect, drop gitlink, extra gitlink, each refused); the lwSRP gitlink arm now drops lwSRP by name.
- `scripts/check_submodule_docs.py:31` the "C cores" edge role.
- `docs/diagrams/submodule_boundaries.gen.py:43,104` the stack's role and card; SVG, drawio, PNG and `PNG_MANIFEST.json` regenerated by the generator.
- `docs/reference/SUBMODULES.md:27` pin row, initialise command, licence lines and ownership row; `THIRD_PARTY.md:21` MIT row; `docs/testing/CI_WORKFLOWS.md` six gitlinks and five fetched pins.

Step 2, build from the stack and remove the copies:

- Removed with `git rm`: `sw/firmware/ctrl/{adp/adp.c, adp/adp.h, acmp/acmp.c, acmp/acmp.h, maap/maap.c, maap/maap.h, wire/wire.h}` and the core-test copies `sw/firmware/ctrl/test/{test_acmp.cpp, acmp_fake.hpp, test_adp_reentry.cpp, test_maap_debug.cpp}`. The core cases of the mixed files left: `test/test_adp.cpp:7` keeps B1 to F7 (A0 to A24 are the stack's `tests/test_adp.cpp`), `test/test_maap.cpp:4` keeps the three `MaapCsr` tests (the Annex B cases are the stack's `tests/test_maap.cpp`).
- `sw/firmware/ctrl/test/ctrl_build.py:43` `STACK`, `STACK_PREFIX`, `STACK_PARTS`, `STACK_INCLUDE`, `STACK_TESTS`; `:57` `PORTABLE` names the cores `tsn-c-stack/src/*.c` in the same link order; `:88` `Tree.stack`; `:105` includes the stack's `include/`; `:126` `test_source` and the stack's tests directory for test compiles; `:141` `label`; `:164` `source`; `:206` `LEGACY` and `:211` `legacy_stack` for trees from before #697.
- `sw/firmware/ctrl/test/ctrl_arms.py:32` `ADP_TESTS`; `:43` `ACMP_TESTS` and its label; `:80` `acmpif2` keeps the tree's stack; `:127` `MAAP_BINARIES`; `:140` `MAAP_DEBUG_LABEL`; `:166` `REENTRY_LABELS`; `:303` the entity arm's core.
- `sw/firmware/gtest/fw_gtest.py:165` `label_object` and the new `sw/firmware/gtest/fw_gtest_label.cpp` (a binary none of whose test files names its tally; labels kept identical).
- Mutation tables: `sw/firmware/ctrl/test/ctrl_mutant.py:13` the five stack paths; every core plant names them (`ADP_C`, `ACMP_C`, `ACMP_H`, `MAAP_C`, `MAAP_H`); 43 plants whose anchor was a comment the stack removed take the stack's own re-anchored text (its `tests/mutations.json`, same plant name) — `ctrl_mutants.py`, `acmp_mutants.py`, `acmp_review_mutants.py`, `maap_mutants.py`. `ctrl_mutants.py:478` `STACK_TABLE`, `:490` `unnamed_tests` reads the stack's test file and also accepts the stack's own table for the stack's tests, `:504` `plant` copies the stack's `src/` and `include/` and plants there, `:601` the campaign's tree.
- `sw/firmware/ctrl/test/maap_differential.py:20,72` the core and its header from the stack; plants into a stack copy.
- `sw/firmware/ctrl/test/srp_arms.py:37,69,78` stack include, sources and tests directory.
- `sw/firmware/ctrl/test/ctrl_image.py:156,169` includes and compile through the stack; `:411` `base_tree` reads a base's own cores (before #697) or its gitlink's stack from the submodule's objects.
- `sw/firmware/ctrl/test/ctrl_srp_image.py:9,37` `--stack-source`, `source_tree` with the same legacy rule.
- `sw/firmware/gtest/fw_coverage.py:86` measures the stack's `src/` and `include/`; `fw_coverage_selftest.py:109` `stack_scope` case; `coverage.ratchet` regenerated by `--write`; `README.md:176,312` and the five exclusion rows on `third_party/tsn-c-stack/src/adp.c`.
- `tb/verilator/mbx/Makefile:46` the bench builds the cores from the stack.
- CI: `.github/workflows/rtl-fast.yml:255` firmware-unit fetches `third_party/tsn-c-stack`; `.github/workflows/rtl.yml:161` the Verilator shards fetch it (the `mbx` co-simulation links the cores); `scripts/ci_events.py:2125,2352` pins; `scripts/ci_scope.py:329` gitlink fixture; `docs/testing/CI_WORKFLOWS.md:56` and the Verilator-worker paragraph.
- Docs: `sw/firmware/ctrl/README.md:54` "The TSN stack submodule" (provides, must not depend on, tests, licence), layout, ACMP table, arms table, planted defects, run, `--base`; `sw/firmware/ctrl/maap/README.md:19`; `docs/design/MAILBOX_SPLIT.md:110` and the ADP and ACMP core links; `sw/firmware/ctrl/mbx/mbx_wire.h:8` comment (same line count). Links into the stack are pinned URLs, because the docs gates run before any submodule is fetched.

Step 3, boundary and pin:

- New `sw/firmware/ctrl/test/ctrl_boundary.py`: the stack's side (every `src/*.c` and `include/*.h` preprocessed with the firmware's own host and RV32 flags; each dependency a stack public header or a C library header), the firmware's side (34 firmware and image units preprocessed with the stack's other directories searched last; a dependency inside the stack outside `include/` refused; no file under `sw/firmware` named as a stack source or header), and the stack's own `scripts/check_boundary.py`.
- `ctrl_build.py:174` `stack_gitlink`, `:183` `stack_pin`: the submodule at its gitlink with `src/`, `include/` and `tests/` unmodified; called first by `test_ctrl_firmware.py:124` (both modes), `ctrl_boundary.py`, `ctrl_image.py:445` and `ctrl_srp_image.py` (default stack).
- `.github/workflows/rtl-fast.yml:291` the firmware-unit step `ctrl_boundary.py --require-rv32 --selftest`; `scripts/ci_events.py` pins the step, the job's ten steps and its compiler refusal arm; `docs/testing/CI_WORKFLOWS.md`; `sw/firmware/ctrl/README.md:77`.

Step 4: `sw/firmware/ctrl/test/acmp_review_mutants.py:228,245` take the stack's words for two killers (see Mutation campaigns).

Step 5: `sw/firmware/ctrl/README.md:84` names the pin check and its four controls.

Step 6: `README.md:191` (Tier 1, every testbench), `QUICKSTART.md:161` (before the run-everything loop) and `CONTRIBUTING.md:386` (the local bar's submodules: four, the fourth for the `mbx` co-simulation) initialise `third_party/tsn-c-stack`.

Steps 5 and 6 are text only. The firmware gate, its campaigns, coverage and images ran at `eeb00e3ee`, whose code, tests and tables are this head's; the docs gates ran again at the head.

## RV32 image hashes, before and after

Both fixtures at every shipped shape: `ctrl_image.py` at the five shapes, and `ctrl_srp_image.py` at the five shapes, one and two interfaces, with and without SRP. 25 of 25 ELF files are byte-identical. The before images were rebuilt once into a second directory to show the hashes are deterministic. The after images were built at the step-2 commit and again at the head.

| Image (fixture/shape) | sha256 before (dev 8b61b709) | sha256 after (head) | |
|---|---|---|---|
| ctrl_image.py endstation_arty_4x4 | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | `5232e40ecbc0d0ed97c31d645b51b3b7c6a2b0c4c407be2f6c1663175bf8d071` | identical |
| ctrl_image.py endstation_arty_8ch | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | `6073714e3fe7dfb49b7c384b71777cb39d16fd1a642ebfbc300132e33d0bbaae` | identical |
| ctrl_image.py endstation_arty_current | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | `604f16d207c01178b30519ea5e9f93a1fb40ff51106b80e1df95b60831291260` | identical |
| ctrl_image.py endstation_ax7101_1x1_tdm8 | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | `c47a379013c3d2f518f11a09c46f42baf6c327038c97d5393c60ce4a7a863a6f` | identical |
| ctrl_image.py endstation_ax7101_8x8 | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | `da74a7ead4a80cdabe3a8659ac6dc2bd90f950f06ec892301f9743b9c70ec5f6` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-nosrp | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | `2daabe0c1b4367b6979d4d1938e38b13553051a10d2a891b64c9468a5b3bf182` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if1-srp | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | `2f735a17dd84b43d802b7bbfd48d3c4f08a4b26e222dae5b864ce944674b1a4d` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-nosrp | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | `67cb0e1cc7f46a2c6d347983cd4305b3f97359555a7777738f02ae1da7699319` | identical |
| ctrl_srp_image.py endstation_arty_4x4-if2-srp | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | `621c0703c34f27a981841df62c6ed24b1bf42500b4c7c86948dab225655e0814` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-nosrp | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | `18b67362d222ee4cff516e6e552c322bac94b7e851fd8a147881ab2ba9e651d3` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if1-srp | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | `935f86f68f4fcaaaddf20dc56e9088ef4a992210a522caca5a5aa581273ee05d` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-nosrp | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | `a5f36deb6c139f3783afd4c301e1a5f17d9d87345cbf4069cfd834ce2818e38a` | identical |
| ctrl_srp_image.py endstation_arty_8ch-if2-srp | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | `991374a26c691848c44f1d800fed328f2cdd1ae713989b0e98226792317c64fb` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-nosrp | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | `39f5ed170bd43de4e0d8fc4132bad14a90f9a041a91582f36a73c41cd1d132de` | identical |
| ctrl_srp_image.py endstation_arty_current-if1-srp | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | `d0a54aa47af63e0f7e43da32ddd5f17d32a38532360037a3e3d86d7952570e78` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-nosrp | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | `1cb077c3c02ebe6b948cb20b28a0985730608e50d3edb5c384e71bb0010f1908` | identical |
| ctrl_srp_image.py endstation_arty_current-if2-srp | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | `8a8b61f8f88ad0d636b565d7b5262df9a64d7867bfbb30f6184de7a4987ee938` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-nosrp | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | `3ed7fdc5d3fa36afc8fb63f45795b56d7caa0844f7b91d583fc853a29130995f` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if1-srp | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | `ed04049b21806328b75701d6737c6b0c4ff4f88ae85438d7730a3285f0ac973e` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-nosrp | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | `26039329ad2ed34cd83acfa8c39d0e2c0447bc6d2ccd97c22fa80ae9274578c5` | identical |
| ctrl_srp_image.py endstation_ax7101_1x1_tdm8-if2-srp | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | `c1142f8d5a18564dbaa791247820939d39ecdf5704eb32216e1ee89833e197ea` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-nosrp | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | `b5f79fd932cb17d6090158827f626710fa6a27a6d45eddb4281f67c7577f6989` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if1-srp | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | `4688e4c84ecc487a805126acefbdd5d4a9d7f8adf35cee0fd9775cad27521c21` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-nosrp | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | `1503a953ad94e7863f516f11122b92e6151df59988f6deeccfbe054f77b5685a` | identical |
| ctrl_srp_image.py endstation_ax7101_8x8-if2-srp | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | `5cd36014ec1857c35c133138cddc55d519f70ada9b477910e461e791b47a13b6` | identical |

Further evidence: `ctrl_image.py --base 8b61b709` (legacy path) and `--base 1aaada1ef` (gitlink path) give base figures equal to head (`+0` in every section) and base ELFs equal to the hashes above at the shipping and largest shapes; `ctrl_image.py --base e21c1ca0` gives the same figures from the new and the old harness; `ctrl_srp_image.py --without-srp --ctrl-source` a dev export (legacy path) at 8x8, one and two interfaces, equals the before hashes.

## Gates and planted controls

| Gate | Where | Result | Planted controls |
|---|---|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | container | PASS: 51 arms ok; `mutants: 471 of 471 caught`; SRP 169 and 68 caught, 0 escaped; lwSRP pin 2 of 2; prints `tsn-c-stack at 1a9f651c…` | the control, SRP and lwSRP-pin campaigns below |
| `fw_coverage.py --selftest` and `--check --jobs 4` | container | PASS, 22 files | 29 of 29 (one new: the stack's `src/` and `include/` measured, its tests, examples and scripts not) |
| `ctrl_boundary.py --require-rv32 --selftest` | host | PASS, 0 findings | 15 boundary controls (13 refused by name: the mailbox HAL, the register-map contract, the composition, the store's port, a macro include of the loop, a public header including the platform, an unresolvable header, an OS header, the firmware reaching a stack example, a stack source by relative path, a stack test from the image, a copied `wire.h`, a copied `adp.c`; 2 passing), 4 pin controls (clean clone accepted; edited source, edited test, other revision refused), the stack's own 12 |
| `ctrl_boundary.py --require-rv32` without a compiler | host | exit 2, refused | — |
| `maap_differential.py --self-test` | host, Verilator 5.050 | 16/16 base, 16/16 head, same plants | 16 |
| `make run-wb run-axil run-cosim run-if2` in `tb/verilator/mbx` | host | same tallies base and head (382, 427, 32, 384, 429, 369, all 0 failures) | `mutants.py --quick --jobs 2`: 5 of 5 |
| `tally_selftest.py`, `fw_rv32_selftest.py --require-rv32`, `ctrl_image_selftest.py --require-rv32` | container | rc 0 | their own |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | container | OK, 5 shapes, 435 tests | — |
| `act_ci.py --selftest` | disposable container | PASS, 446 arms (base 442 + 4 new) | 4 new tsn-c-stack manifest refusals |
| `ci_events.py --check`, `--selftest` | host | OK, 1757 items; PASS, 2387 arms | its own |
| docs gates in a fresh clone with no submodule initialised (as the hosted docs job runs them): links, cited paths, anchors, contents, submodule docs and diagram, style, CI contract | host | all rc 0 | — |
| the firmware gate and the boundary gate in that clone | host | exit 2, "initialise the tsn-c-stack submodule" (refused, never skipped) | — |
| docs job (37 commands: links, em-dash, style, contents, cited paths, submodule docs and diagram, PNGs, idioms, ratchets, archive, CI scope) | host | all rc 0 | their own |

Plant equivalence (scratch tool): for all 471 control plants, the base table on the base tree and the head table on the head tree give the same non-comment tokens on the same lines (311 of them in the stack's files); the kills differ only in the two needles of step 4.

## Coverage

Same denominator. Raw totals are identical file for file between dev and the head, measured in the same container; the four core files only change path.

| File (before -> after) | Raw lines before / after | Raw branches before / after | Ratchet before | Ratchet after |
|---|---|---|---|---|
| `sw/firmware/ctrl/acmp/acmp.c -> third_party/tsn-c-stack/src/acmp.c` | 742/742 / 742/742 | 348/348 / 348/348 | 742/742 348/348 | 742/742 348/348 |
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 73/73 / 73/73 | 26/26 / 26/26 | 73/73 26/26 | 73/73 26/26 |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 / 38/38 | 10/10 / 10/10 | 38/38 10/10 | 38/38 10/10 |
| `sw/firmware/ctrl/adp/adp.c -> third_party/tsn-c-stack/src/adp.c` | 204/206 / 204/206 | 95/102 / 95/102 | 204/204 95/95 | 204/204 95/95 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 / 83/83 | 38/40 / 38/40 | 83/83 38/38 | 83/83 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 / 42/43 | 40/44 / 40/44 | 42/42 40/40 | 42/42 40/40 |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 / 82/82 | 62/62 / 62/62 | 82/82 62/62 | 82/82 62/62 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 / 101/101 | 62/62 / 62/62 | 101/101 62/62 | 101/101 62/62 |
| `sw/firmware/ctrl/maap/maap.c -> third_party/tsn-c-stack/src/maap.c` | 209/209 / 209/209 | 140/140 / 140/140 | 209/209 140/140 | 209/209 140/140 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 / 39/39 | 18/18 / 18/18 | 39/39 18/18 | 39/39 18/18 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 / 98/98 | 60/60 / 60/60 | 98/98 60/60 | 98/98 60/60 |
| `sw/firmware/ctrl/mbx/mbx.c` | 189/189 / 189/189 | 74/74 / 74/74 | 189/189 74/74 | 189/189 74/74 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 / 15/15 | 12/12 / 12/12 | 15/15 12/12 | 15/15 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 / 10/10 | 0/0 / 0/0 | 10/10 0/0 | 10/10 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 / 19/19 | 6/6 / 6/6 | 19/19 6/6 | 19/19 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 / 99/99 | 60/60 / 60/60 | 99/99 60/60 | 99/99 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 / 22/22 | 6/6 / 6/6 | 22/22 6/6 | 22/22 6/6 |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 514/514 / 514/514 | 478/478 / 478/478 | 515/515 478/478 | 514/514 478/478 |
| `sw/firmware/ctrl/wire/wire.h -> third_party/tsn-c-stack/include/wire.h` | 10/10 / 10/10 | 2/2 / 2/2 | 10/10 2/2 | 10/10 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 / 198/199 | 106/110 / 106/110 | 198/198 106/106 | 198/198 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 / 434/434 | 259/266 / 259/266 | 434/434 259/259 | 434/434 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 / 100/100 | 63/64 / 63/64 | 100/100 63/63 | 100/100 63/63 |

The `srp_mbx.c` ratchet row moves from a stale 515/515 to 514/514. Dev itself measures 514/514 (this container, and the hosted firmware-unit run of `8b61b709`); `--write` records the measurement.

## Mutation campaigns

| Campaign | dev `8b61b709` | head |
|---|---|---|
| control (`ctrl_mutants.py` with ACMP, ACMP review and MAAP tables) | 471 of 471 | 471 of 471 |
| SRP, two interfaces | 169 caught, 0 escaped | 169 caught, 0 escaped |
| SRP, one-interface subset | 68 caught, 0 escaped | 68 caught, 0 escaped |
| lwSRP pin arms | 2 of 2 | 2 of 2 |
| tests named by no defect | 0 | 0 |
| MAAP differential | 16 of 16 | 16 of 16 |
| mailbox bench quick | — | 5 of 5 |

Two killers changed words, not kills. The stack's `AcmpCore.A29TheAdmitPortFollowsEachSinksBoundTalker` and `AcmpCore.A29RestoredBindingsAreAdmittedWhenTheTransportOpens` now assert the admission count first ("A29 re-binding emits one admission", "A29 opening after reset emits one withdrawal"). With `acmp-admit-ignores-another-talker` and `acmp-reset-forgets-the-admitted` planted, that assertion stops the test first. A head run before step 4 caught 469 of 471: both escapes failed the named test on the new words. The stack's own table uses the same words.

The stack's tests add cases of their own in milan-fpga's arms: `adp` runs 34 tests (26 before), `acmp` 91 (85). The six new ACMP tests are named by the stack's own table (`tests/mutations.json`, which its CI plants); `unnamed_tests` accepts that table for the stack's tests only.

## Open risks and questions

1. **Pin criterion.** No tsn-c-stack commit is byte-identical to milan-fpga's copies (MIT SPDX line, comment reduction). This lane pins the newest commit whose cores are identical code on identical lines (`1a9f651`, the assignment's expected candidate), proven by tokens, objects and images. Please confirm the reading.
2. **act and hosted CI not run.** No push or PR was allowed. The PR changes `scripts/act_ci.py`'s manifest, so act needs the audited-install bootstrap: an independent reviewer installs this exact `act_ci.py` outside the candidate worktree before the first act run.
3. **Hosted runners need CMake and Clang** for the stack's own gate in the new firmware-unit step. The ubuntu-latest image carries both; not yet observed on a hosted run.
4. **Pinned URLs.** Docs link files inside the stack by URLs at `1a9f651c`; a later pin bump (tsn-c-stack main brings the ADP change of #19 and the YAML generator of #703) must move them with the gitlink.
5. `maap_differential.py` and the mailbox bench are local gates (not in CI); both ran at base and head.

## Rounds 2 to 6

Moved verbatim to [`HANDOFF-rounds-2-6.md`](HANDOFF-rounds-2-6.md) in round 8 (its sections: [Round 2](HANDOFF-rounds-2-6.md#round-2), [Round 2b](HANDOFF-rounds-2-6.md#round-2b), [Round 3](HANDOFF-rounds-2-6.md#round-3), [Round 4](HANDOFF-rounds-2-6.md#round-4), [Round 5](HANDOFF-rounds-2-6.md#round-5), [Round 6](HANDOFF-rounds-2-6.md#round-6)), so this file stays under 200 KB.

## Round 7

Assignment: #697 comment [6104711137](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6104711137), answering [R584-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104503651) and [R585-6](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6104708471), both NEGATIVE on MINORs only (R584-6-F1 = R585-6-F1: the `ctrl_nvm` store sources escaped the firmware side, which took its units from directory listings, probe N1; R585-6-F2: the stack side resolved headers on a fixed search path, so a builder-only directory could shadow a C library header, probe Q7). Ruling: the compile's own dependency list decides, the gate's own resolution goes; standing controls N1 and Q7, Q9 and the clean controls pass; README, CI page and docstring claim exactly that, the CI page cites the hosted figures (R585-6-S1); residue R584-6-RS1 and R585-6-RS1.
Base of the round: `5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `8436dfc0bd5e0f3c592dd1faa0a4ced1841a2651`.
Status: REVIEW READY, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (its text: `round7/review-ready-round7.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `c34ca24a3` | Make the capture's empty baseline stand-in once, read-only, whichever expansion helper comes first, so two at once no longer fail on it | found when the first N1 replay refused with `PermissionError: ... expand/in/base.c` (two helpers creating the read-only stand-in at once; round 6's code, `logs/` not kept, the rerun is `probes/probe.N1.log`); `Path.touch(exist_ok=False)` now, an existing one accepted; every later run had 0 expansion errors |
| `1bcf60e12` | Judge each side of the TSN stack boundary in exactly the compiles a capture recorded, by the compiler's own dependency output for each and where every file it read lives | the hosted command against a CI-parity capture made with this recorder: PASS, 103 boundary and 20 pin controls, 0 misbehaved, 80 s (`logs/hgate1.log`); the Verilator-only command PASS, 6 and 20, 0 misbehaved (`logs/vgate3.log`); all 102 firmware-run controls through a scratch harness on the host (`logs/harness-all-2.log`); pyflakes, `check_py_idiom.py` every ratchet held |
| `dfe36f668` | Say in the firmware README, the CI page and the workflow's comments that each compile's own dependency list decides the TSN stack boundary, with the hosted figures at 5b4f6fbe | `docs_check.py` (0 findings, 202 pages), `check_doc_style.py`, `check_em_dash.py --base 5b4f6fbe` (0 over 74 added lines), `check_doc_paths.py`, `check_hygiene.py --check`, `ci_events.py --check`, `measure_fail_fast.py --check`, `check_submodule_docs.py`, `gen_toc.py --check`, `check_baremetal_only.py --check`, all rc 0; then the docs job's 54 commands and `act_ci.py --selftest` at this commit |
| `8436dfc0b` | Say what three of the boundary controls' shared constants hold now that the controls compile a planted copy | comments only (`ctrl_plants.py`); pyflakes, `check_py_idiom.py`; both boundary commands, the docs job's 54 commands and `act_ci.py --selftest` rerun at this head (below) |

One-line subjects, no body, no trailers, configured identity. `git diff --stat 5b4f6fbe HEAD`: 10 files, 1424 insertions, 1974 deletions: `ctrl_shim.py`, `ctrl_capture.py`, `ctrl_expand.py`, `ctrl_configs.py`, `ctrl_boundary.py`, `ctrl_runs.py`, `ctrl_plants.py`, `sw/firmware/ctrl/README.md`, `docs/testing/CI_WORKFLOWS.md`, `.github/workflows/rtl-fast.yml` (comments only). No firmware source or header, no image builder, no mutation table, no coverage row, no Makefile, no build flag. `ctrl_configs.BUILDERS` now runs the MAAP differential with `--keep {work}/maap-differential` (its own option) so a control can replay its compile.

### Item 1: the compile's own dependency list decides

| What | Where (at the head) |
|---|---|
| The dependency pass: for each source the expansion says an invocation compiles (C, C++, preprocessed assembler), the recorder runs the real compiler once more, in the invocation's directory and environment (`LC_ALL=C`, so the verdict is read in English), with the invocation's own arguments, its output and dependency options dropped as the expansion drops them, every other input left out (one source per pass), and `-M -MF <file> -MT dependencies -H -fpch-preprocess` added (`-Qunused-arguments` for a driver the expansion found to be Clang). `-M` lists every file the compile reads (the source, what the command line reads first, what the source includes, system headers); `-H` prints the tree of what the source's own `#include` lines read (GCC and Clang print neither a file the command line reads first nor what it reads). `-fpch-preprocess` makes the pass read a precompiled header the compile reads first, as the compile does (without it GCC reads the header's text: Verilator's model objects, which read `V…__pch.h.fast` whose text file does not exist, failed the pass in the first Verilator replica). Every name is resolved while the files are there; the list (the source aside) and the tree (as indexes into it) are kept by SHA-256 | `ctrl_shim.py` docstring THE DEPENDENCY PASS; RECORDER `dependencies`, `prerequisites`; `main` (the record's sources are `[path, language, list digest, why none]`) |
| A pass gives no list, and the record says why: the compiler failed (but on `#error`/`#warning` alone, after which GCC still lists every file it read), wrote no rule (a builder's `-Wp,-MD,file` overrides `-MF`), named first a file that is not the source, named a file that does not exist, printed a tree entry the rule does not hold, or the source is standard input. `ctrl_configs.held` refuses each by name | `ctrl_shim.py` `dependencies`; `ctrl_configs.py` `unlisted`, `held` |
| The reader: each source's `Deps` (files, tree), `edges` (every includer and file of the tree); a compile that reads a precompiled header first also reads what the compile that made it read (its header and its list). A capture made by an earlier recorder (no lists) is refused: "a recorder that lists no dependencies made it: capture again" | `ctrl_capture.py` `Deps`, `Source`, `deps`, `invocation` |
| Where a file lives (`Places`), by its resolved path: the stack's (public under `include/`); the C implementation's (the compiler's baseline: what it reads and searches with no argument; and `sw/firmware/gtest/rv32_include`, the RV32 builds' freestanding C library under `-nostdinc`); the firmware's (under `sw/firmware`, but the harness, `nvm_hosttest`, and every `host/` and `test/` directory; and every file of the checkout an RV32 compile, one whose built-ins define `__riscv`, compiles or reads); the checkout's (the rest of a root); outside | `ctrl_boundary.py` `Places`, `implementation`, `targets` |
| The rules (`findings_of`): a compile of a firmware source reads no stack file outside `include/`; a compile of a stack source reads, through its own `#include` lines, only stack and C implementation files (a stack test also the host's libraries outside the checkout); what its command line reads is no file of the checkout outside the stack; in every compile, no firmware file includes a stack file outside `include/`, and no stack file includes anything but stack and C implementation files | `ctrl_boundary.py` `findings_of`, `admitted`, `judged` |
| What a compile reads first (the expansion's report): a stack file outside `include/` refuses; a file of the checkout outside the stack read first into a compile of a stack source refuses; an installed tool's file is now classified by where it lives too | `ctrl_configs.py` `expanded`, `kind_of` |
| Gone: the gate's own preprocessing (search path, tail, standing-in for generated headers), the exploration over modes, shapes, contracts, the forced header and stream counts, the C++ text follow, the unit lists (`firmware_units`, `firmware_dirs`), the memo; the recorder's C++ text keeping and its 1024-header closure | `git diff 5b4f6fbe -- sw/firmware/ctrl/test` |

Line references at `8436dfc0`: the dependency pass `ctrl_shim.py:47` (docstring), `:543` `prerequisites`, `:587` `dependencies`, `:622` its added options, `:900-922` the compile waited for and its exit status recorded; `ctrl_expand.py:324` "driver clang"; `ctrl_capture.py:310` `Deps`, `:318` `edges`, `:331` `Source`, `:459` `deps`, `:469-505` `invocation` (`:489` the old-format refusal, `:488` a precompiled header's reads); `ctrl_configs.py:214` `held`, `:243` `unlisted`, `:255` `failed`, `:325-347` `expanded`; `ctrl_boundary.py:6` THE COMPILES DECIDE, `:45` WHERE A FILE LIVES, `:146` `Places`, `:199` `implementation`, `:205` `targets`, `:225` `findings_of`, `:255` `admitted`, `:262` `judged`, `:294` `shadows`, `:305` `judge`, `:322` `mirror`, `:349` `control`, `:363` `controls`; `ctrl_runs.py:145-163` `captures` (`:159` a capture made in another checkout refused), `:191` `planted_env`, `:202` `planted_run`, `:223` `replayed`, `:243` `control_capture`; `ctrl_plants.py:189` `PLANTS`, `:566` `BASE`.

Interpretations of the assignment, each public here and in the PR body, each needed for the clean tree to pass or a resolved finding to stay resolved:
1. What a stack-side compile reads through its command line (`-include`, `-imacros`) is the builder's: the SRP builds force-include their generated shape header and the two-interface builds their generated mailbox contract into every unit, the stack's sources among them (1041 + 30 and 12 such compiles in round 6's capture). Those files live outside the checkout; what such a read pulls in must be no file of the checkout outside the stack, and a stack file outside `include/` read first, or a file of the checkout outside the stack read first into a stack compile, refuses. Read literally ("a stack-side compile that reads anything outside the stack itself, its public headers and the C implementation's own headers") the clean tree fails.
2. "The C implementation's own headers" are the compiler's baseline (what it reads and searches with no argument) and the RV32 builds' freestanding C library (`sw/firmware/gtest/rv32_include`, passed by `fw_rv32.includes` with `-nostdinc`, the only `string.h` and `assert.h` there). The RV32 compiles of the stack's sources read those two (`proto_deps.py` on round 6's capture).
3. The firmware side is every compile of a firmware source: under `sw/firmware`, but the test equipment, and every file an RV32 compile reads. Test equipment is held only by the `#include` lines of the firmware and stack files it reads: this repository's tests use the stack's `tests/acmp_fake.hpp` (R584-6-S1).
4. The include tree (`-H`) beyond `-M`: no firmware file includes a stack file outside `include/` and no stack file includes anything but stack and C implementation files, in any compile. It keeps round 3's C++-only finding (R585-2 n1) and the stack-public-header controls resolved; it only refuses more.
5. A stack test (its `tests/`) may read the host's libraries outside the checkout (GoogleTest wherever it is installed, as R584-6 and R585-6 install it by `CPLUS_INCLUDE_PATH`).
6. A compile that failed compiled nothing: where its dependency pass failed with it, it is named, not refused. The RV32 self-test compiles planted header defects that must fail (`no include path in which to search for stdint.h`, 1 in the capture). A source a passing compile compiled whose pass failed or is incomplete refuses (standard input, a builder's own `-Wp,-MD`).
7. A POSIX header of the host's C library (`<unistd.h>`) is the C implementation's on the host; the RV32 build has none, so the image builders fail there and the gate's own image runs refuse by name.
8. A mode reaches only the compiles a builder gives it: rounds 3 to 6 explored every combination; round 7 judges exactly the recorded compiles, as the population rule says.

### Item 2: standing controls

Every control compiles a planted copy of the firmware's tree and the stack (`ctrl_boundary.mirror`: `sw/firmware/ctrl`, `sw/firmware/ctrl_nvm` and the stack's `src/`, `include/`, `tests/`, `examples/`, laid out as in the checkout) through a capture of its own, and the gate judges what that capture recorded, the run's capture beside it for what a capture must hold. Three ways to compile the copy:
- a builder's own compile function, imported from the gate's directory: the image builder's `ctrl_image.compile_all` (its `IMAGE` pointed at the copy's `rv32_image`, the shape's headers from `ctrl_image.shape_build`), the arms' `ctrl_build.compile_c`, the arms' C++ `fw_gtest.compile_tests` with `ctrl_build.includes` and the checkout's stack `tests/`;
- a spelling of the planted builder's own (a Makefile or a Python script, the arms' include path for the copy in `PLANT_INCLUDES`);
- a replay (`ctrl_runs.replayed`): every compile of the run's capture whose source has the plant's name and whose inputs are still there, run again through the control's capture with its own arguments, the checkout's `sw/firmware/ctrl`, `sw/firmware/ctrl_nvm` and stack in them replaced by the copy's, and its output its own. The image builders' compiles (the gate's own runs) and the Verilator builders' (the wire comparison's `--output` and, new, the differential's `--keep` under the run's directory) are replayable; the firmware steps' are not (their temporary files are gone).

The base compiles the unplanted copy the ways the controls do (the arms' C compile of every portable source and `plat/mbx_plat_mmio.c`, the AECP core, the arms' C++ compile of the five stack tests the arms build and of every header of `acmp`, `adp`, `maap`, `mbx`, `port`, `loop`, `app`, and the image builder's compile at both of its shapes) and must pass.

New and restated controls (old name -> new):

| Old control (round 6) | Round 7 | Why |
|---|---|---|
| stack source includes a header nobody supplies | pass: ... the compile fails, and compiled nothing | a compile that fails compiles nothing; its failed pass is named, not refused (the RV32 self-test's planted header defects fail so on purpose) |
| stack source includes an OS header | pass: a stack source includes an OS header of the host's C implementation | `<unistd.h>` is the host C implementation's header (the assignment's allowed set); the RV32 build has none, so the image builders fail and the gate's own image runs refuse by name |
| image source reaches a stack test's header | image source reaches a stack file outside its public headers | a C compile of a C++ fixture fails to preprocess; the reach is to `examples/rv32/include/string.h`, compiled by the image builder |
| firmware adapter reaches a stack test's fake under the re-entry assertion | a firmware adapter reaches a stack source under the re-entry assertion | as above (C) |
| firmware adapter reaches the stack's test fake by its checkout path under the re-entry assertion | (folded into) a firmware header reaches a stack test's fake in C++ only | the arms' C++ compile reaches the checkout's own stack `tests/` (`ctrl_build.STACK_TESTS`), so the checkout's stack is classified as the copy's is |
| the SRP image's composition reaches a stack source | ..., as the SRP image builder compiles it | a replay of `ctrl_srp_image.py`'s compiles of `test/ctrl_image.c` |
| the AECP image's SRP composition reaches a stack source | ..., as the SRP image builder compiles it | a replay |
| the image reaches a stack example's header under a shape's stream count | the image reaches a stack file under a shape's stream count | the image builder at the 8x8 shape (`IMAGE_SINKS=9u`) |
| an adapter reaches a stack source on the two-interface contract | ..., as the SRP image builder compiles it | a replay of the two-interface SRP images' compiles (their variant contract) |
| a mode a builder compiles with is explored without being named here; a mode an AECP arm writes ...; a mode a new builder nobody lists ... | a mode a builder compiles the stack with | no mode is explored across units any more: a mode reaches the compiles given it |
| a mode a builder writes as two arguments is explored; a mode a new Makefile writes as two words is explored | a mode a builder writes as two arguments; a mode a new Makefile writes as two words | the builder compiles the stack source with the mode |
| a header only the MAAP differential's C++ source reaches includes a stack test's fake in C++ only | ... includes a stack file in C++ only (a replay, `needs="verilator"`) | the differential's own compile (needs its Verilated header), replayed where its capture is |
| a builder writes a C++ source whose include a macro computes | a firmware header reaches a stack file through a computed include in C++ only | text no longer follows includes; the compiler resolves a computed one |
| a builder copies a C++ source whose include a macro computes out of its own directories | a builder copies a C++ source out of its own directories and compiles it from elsewhere | as above |
| a builder compiles a C++ source that is no file | pass: ... the compile fails, and compiled nothing | as the first row |
| a builder compiles a stream count no shipped shape gives | (retired) | it checked the exploration's model of the image's stream counts, which is gone |
| pass: a builder compiles a mode no unit tests | pass: a builder compiles the firmware with a mode no file tests | renamed |
| pass: a builder compiles an installed tool's C++ source whose include a macro computes | pass: a builder's own C++ source whose include a macro computes reads a firmware header | the recorder no longer tells installed sources apart |
| (new) | N1, Q7; a firmware directory shadows a header the C library's own headers include, for the stack; a store source reaches a stack file outside its public headers in the image build; -include of a header the builder writes defines a mode; a builder passes a dependency option the pass cannot override; a builder reads a firmware header first into a compile of a stack source | |

Every other control keeps its name and defect; its builder now compiles the planted file (the old spelling controls compiled an empty `planted.c` and relied on the exploration).

Counts: the firmware run holds the base and 102 plants (94 refused by name, 8 passing): 103 boundary controls; the Verilator run the base and 5 refused: 6; 20 pin controls each, unchanged. Every control and the finding that refused it at the head: `logs/hgate-final.log`, `logs/vgate-final.log`.

### Item 3: docs

`sw/firmware/ctrl/README.md` (the stack section's boundary paragraphs: what decides, where a file lives, both sides' rules, the command-line reads, test equipment, failed compiles, the capture, the controls, with N1 and Q7 named), `docs/testing/CI_WORKFLOWS.md` (both jobs' boundary paragraphs; the hosted figures at `5b4f6fbe`: `firmware-unit`'s step 93 s, job 114344992704, 1861 s of 2700; `firmware-verilator`'s step 438 s, job 114344992708, the job 473 s), the gate's docstring (`ctrl_boundary.py:1-91`) and the module docstrings of `ctrl_shim.py`, `ctrl_capture.py`, `ctrl_configs.py`, `ctrl_runs.py`, `ctrl_plants.py`; `.github/workflows/rtl-fast.yml`'s comments on the two boundary steps.

### Item 4: residue

PR-BODY.md, the exact texts of both reviews: R584-6-RS1 (Status: "Round 6's hosted figures come after its push." replaced by the four figures; the second `92b5be18` sentence deleted; Known limitations: "; the hosted step took 113 s at `92b5be18` (job 114282060753)" deleted) and R585-6-RS1 (the same two deletions). Where they overlap they make the same edit, applied once.

### Captures, images, kills, coverage

- The capture of the hosted job's firmware steps at the round's recorder (`fullcap.sh` in the CI-parity container, Ubuntu 24.04.5, CPython 3.12.3, GCC 13.3, GoogleTest 1.14.0, four CPUs, a clean clone, the gate modules of `1bcf60e12`'s tree): 23,213 invocations (round 6: 23,213), 22,031 compiled sources, 22,030 with a dependency list and 1 without (a failed compile, the RV32 self-test's planted defect), 2 compiles with a non-zero exit, 2,004 distinct lists, 551 expansions (round 6: 551), 0 expansion errors, 89 MB (round 6: 78 MB). Step times (`logs/fullcap2-summary.txt`; the log is 324,441 bytes, sha256 `58e71b4a4645cdcd5025e30d4ad69d62b5e659f0afb97337431ccedfe2f0eae6`, not copied): `fw_rv32_selftest` 9 s (round 6: 8), `test_ctrl_firmware` 2123 s (1863), `test_ctrl_nvm` 98 s (82), coverage self-test 1 s (1), coverage check 266 s (249): 2497 s against 2203 s, 13% more, the dependency passes (other jobs ran on the host's other CPUs meanwhile).
- Kills: the firmware gate's 845 verdict lines (843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`) through that capture are byte-identical to rounds 4, 5 and 6 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `logs/fw-verdicts-cap2.txt`); the store gate `OK across 5 shape(s), 435 tests`; coverage self-test 29 of 29.
- Coverage: `fw_coverage.py --check` PASS (30 files), its 32-line table byte-identical to round 6's (`logs/cov-cap2.txt`); `coverage.ratchet` unchanged.
- Images: `images6.sh` (round 6's script) at the round's tree with the pinned SDK and round 1's runtime archives: 35 of 35 ELF files, the manifest byte-identical to round 6's and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `logs/images-head.sha256`). Every hash of the round-3 table holds; no image builder or firmware file changed this round.

### Gates at the round-7 head

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --capture <capture> --without verilator` (the hosted `firmware-unit` step) | CI-parity container, GNU make 4.3 under `MAKEFLAGS=w`, the capture's own clone at `8436dfc0`, four CPUs | PASS: `22528 compiled sources of 23795 recorded invocations (3337 the firmware's, 1688 the stack's, 17503 test equipment's and builders' own) ...; 0 finding(s), 103 boundary and 20 pin controls, 0 misbehaved`, 73 s (`logs/hgate-final.log`); at `dfe36f66` 71 s, and 74 s under `MAKEFLAGS=w` (`logs/hgate-head.log`, `logs/hgate-head-makeflags.log`) |
| the same step, round 6's code against round 6's capture, then this round's against its own, one after the other on the same four CPUs | CI-parity container | 132 s and 80 s (`logs/hgate-r6-same.log`, `logs/hgate1.log`): the step preprocesses nothing itself |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | CI-parity image with cmake 3.28 and clang 18, the pinned Verilator 5.050 and RV32 SDK mounted, a clean clone at `8436dfc0`, four CPUs | PASS: `816 compiled sources of 916 recorded invocations (386 the firmware's, 94 the stack's, 336 test equipment's and builders' own) ...; 0 finding(s), 6 boundary and 20 pin controls, 0 misbehaved`, V1 to V3 and the MAAP differential's replay caught by name, 472 s: bench 53 s, differential 149 s, wire comparison at both references 206 s (`logs/vgate-final.log`); at `dfe36f66` PASS in 454 s, bench 54 s, differential 140 s, wire comparison 195 s (`logs/vgate-head.log`); at `1bcf60e12`'s tree 486 s (`logs/vgate3.log`) |
| the docs job's 54 commands (`docsjob.sh`, CPython 3.12.3 with the locked renderer) | clean clone at `8436dfc0` with the docs job's submodules | 54 of 54 rc 0 (`logs/docsjob-final.txt`): `ci_events.py --check` OK (1848 items), `--selftest` PASS (2530 arms); `check_py_idiom.py` every ratchet held; `check_em_dash.py --base 5b4f6fbe` 0 findings over 74 added lines; `docs_check.py` 0 findings; `measure_fail_fast.py --selftest` 106 of 106 |
| `act_ci.py --selftest --worktree <head>` (the copy installed 0555 outside the tree, sha256 `797f123b…d22d1`, identical to the tree's) | host, CPython 3.12.3 with PyYAML | PASS, 446 arms (`logs/act-selftest-final.log`) |
| pyflakes over the gate modules; `check_py_idiom.py` | host | rc 0 (`logs/idiom5.log`) |
| every firmware-run control through a scratch harness (`scripts/ctrl_harness.py`: the gate's own image runs as the base, a stand-in for every other builder) | host, GCC 16 | 102 run, 0 misbehaved, 64 s (`logs/harness-all-2.log`) |

### Reviewers' probes at the head

| Probe | At `5b4f6fbe` (the reviews) | At the round's tree |
|---|---|---|
| R584-6 N1 (`probe_nvm.sh`: `nvm_store.c` after line 1 reaches the stack's `examples/adp_port.h`; `--only verilator`, no capture) | PASS, rc 0 | FAIL, rc 1: `firmware: sw/firmware/ctrl_nvm/nvm_store.c reads tsn-c-stack/examples/adp_port.h, not one of the stack's public headers [sw/firmware/ctrl/test/ctrl_image.py]` and its include edge (`probes/probe.N1.log`) |
| R584-6 N1C (N1 and the same reach in `maap/maap_csr.c`) | `maap_csr.c` only | FAIL, rc 1: both files, `maap_csr.c` through the mailbox bench's compile (`probes/probe.N1C.log`) |
| R585-6 Q7 (`ctrl_nvm/plat/stdbool.h` shadows the C library header; against a capture of the firmware steps, `--without verilator`) | PASS, rc 0 | FAIL, rc 1, 6 findings: `stack: tsn-c-stack/src/acmp.c reads sw/firmware/ctrl_nvm/plat/stdbool.h (included by tsn-c-stack/include/acmp.h), which is neither the stack's nor the C implementation's [sw/firmware/ctrl/test/ctrl_image.py]`, and `adp.c`, `maap.c` alike (`probes/probe_Q7.log`) |
| R585-6 Q8 (the same in `ctrl_nvm/`) | FAIL, 19 findings | FAIL, 6 findings, the same files (`probes/probe_Q8.log`) |
| R585-6 Q9 (nothing planted) | PASS | PASS, rc 0 (`probes/probe_Q9.log`) |

The probes ran with the reviewers' plants and gate commands; `probe7_nvm.sh` restores only the two planted files (the reviewer's restores all of `sw/firmware`, which would have undone the uncommitted gate files in the scratch clone), and `probe7_q.sh` judges a capture made in the same clone (round 7 refuses a capture made in another checkout). Q7 and Q8 are refused through the gate's own image compiles, which run with the plant in place even when the capture given predates it. A capture made by round 6's recorder is refused by name: `a recorder that lists no dependencies made it: capture again`.

### Open risks and questions (round 7)

1. The eight interpretations above (Item 1) are mine, made so the clean tree passes and no resolved finding reopens; each is a decision the manager may want to confirm or reverse. The weightiest: command-line reads into stack compiles judged as the builder's (1), test equipment held only through the firmware and stack files it reads (3), failed compiles named rather than refused (6), and modes no longer explored across units (8).
2. `firmware-unit`'s headroom: the dependency passes add about 13% to its firmware steps in the container (2497 s against 2203 s); the step itself is faster (80 s against 132 s on the same CPUs). Scaled from the hosted run at `5b4f6fbe` (1861 s of 2700) that is near 2050 s; at `92b5be18`'s slower hosted run (2450 s) it would be near 2750 s, past the 45 minutes. The hosted figures at this head need a push; the headroom issue is the manager's (carried).
3. A capture judged must have been made in the checkout judged; reviewers who capture in one clone and judge in another are now refused by name, where round 6 judged against the other clone's paths.
4. Replays run only where the recorded compile's inputs still exist: the gate's own image runs and the Verilator builders (kept under the run's directory); the firmware steps' compiles (their temporary files gone) are not replayable, so the controls that need the arms' configurations compile through the arms' own functions instead.
5. The recorder now waits for the compile (to record its exit status) and writes the record after it; a compile killed by an uncatchable signal leaves no record (the builder then fails, which refuses a given capture).
6. R584-6-S1 (say that this repository's tests use the stack's test fakes): the README says so now. R584-6-S2 (the pin check's executable bit), R584-3-S1's remainder and R585-2-S2: optional, not addressed.

## Round 8

Assignment: #697 comment [6105928035](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105928035), from the manager's hosted check at `8436dfc0` (not a review): hosted `firmware-unit` was cancelled at its 45-minute timeout (job 114392589133) inside "Run the control-plane firmware suites and RV32 builds" (39 min 43 s, every compile under the capture also running its dependency pass); the coverage ratchet and the boundary step never ran; `firmware-verilator` passed in 11 min 22 s (job 114392589175). Required: (1) the boundary capture leaves `firmware-unit` for a new required job that runs every builder the boundary judges under the capture, builds only, its builder list read from the gate's own known set so a dropped builder still refuses by name, the `rtl-fast` aggregate requiring it and `scripts/ci_events.py` pinning it; `firmware-unit` runs its suites, store suites and coverage ratchet without the capture; (2) each of `firmware-unit`, the new job and `firmware-verilator` at or under 60 % of its timeout at the head, local timings reported, or the shortfall said with the measurement; (3) nothing else of the round-7 design changes.
Base of the round: `8436dfc0bd5e0f3c592dd1faa0a4ced1841a2651` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `4cab445aa2475903b6cf8b87566d2c8a1e15e391`.
Status: REVIEW READY, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`).

Housekeeping: this file had reached 210,737 bytes; rounds 2 to 6 moved verbatim to `HANDOFF-rounds-2-6.md`, so it stays under 200 KB.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `f878188c6` | Give the firmware, store and coverage gates a build-only mode that builds every binary their suites build and runs none | each mode on the host (`test_ctrl_firmware.py --require-rv32 --build-only`: 54 binaries `built, not run`, `test_ctrl_firmware: BUILT`, 319 s; the store's: `BUILT across 5 shape(s)`, 82 s; the coverage gate's: both gates `BUILT`, 228 s); `firmware-unit`'s steps in the CI-parity container with these files (`logs/ujob-1/`, every step rc 0, the firmware gate's 845 verdict lines byte-identical to round 7's); `--build-only` with `--self-test` (both suite gates) or `--check` refused, rc 2; pyflakes (only dev's own unused `os` import in `test_ctrl_firmware.py`, present at `8b61b709`), `check_py_idiom.py` |
| `ffa613d62` | Hold the TSN stack boundary in a firmware-boundary job that runs the gate's known builders by their builds, and run firmware-unit's suites without the capture | `firmware-boundary`'s command in the CI-parity container (`logs/bjob-2.log`: PASS, 103 boundary and 20 pin controls, 0 misbehaved, 651 s); `firmware-verilator`'s (`logs/vjob-1.log`: PASS, 6 and 20, 477 s); `ci_events.py --check` (1902 items) and `--selftest` (2610 arms); `check_py_idiom.py` |
| `09af0d047` | Say in the firmware, harness and CI pages that firmware-boundary holds the TSN stack boundary over the builders' builds and firmware-unit runs the suites alone | `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 8436dfc0`, `check_doc_paths.py`, `gen_toc.py --check`, `check_hygiene.py --check`, `check_submodule_docs.py`, `measure_fail_fast.py --check`, `check_baremetal_only.py --check`, `ci_scope.py --selftest`, `ci_events.py --check` and `--selftest`, all rc 0; then, at this commit in fresh clones: both boundary replicas, `firmware-unit`'s steps, the docs job, the act self-test, the images, and the dropped-builder probe, which failed (below) |
| `0b4c140a5` | Hold each known builder by a run of its own and every program that names the firmware's tree by a listing, so a builder dropped from the known set refuses by name where another still runs it | offline against the saved build-only capture (`capb`): nothing new refused; the known set without the store gate refuses it by name; the control gate's own run dropped refuses it by name though the coverage gate's run still compiles it; then `firmware-boundary`'s replica (`logs/bjob-fix.log`: PASS, 105 boundary and 20 pin controls, 0 misbehaved), `firmware-verilator`'s (`logs/vjob-fix.log`: PASS, 6 and 20), the probe again (`logs/probe-fix.log`: rc 2, refused by name); pyflakes, `check_py_idiom.py` |
| `0a9c5fa82` | Say on the firmware and CI pages that a known builder is held by its own run and a dropped one refuses by name, with the two controls that plant each | `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 09af0d04`, `check_doc_paths.py`, `gen_toc.py --check`, `check_hygiene.py --check`, `ci_events.py --check`, `measure_fail_fast.py --check`, all rc 0; then both boundary replicas at this commit in fresh clones (below) |
| `4cab445aa` | Give firmware-boundary's figures on the CI page at the head that holds each known builder by its own run | `docs_check.py`, `check_doc_style.py`, `check_em_dash.py --base 0a9c5fa8`, `ci_events.py --check`, `gen_toc.py --check`, all rc 0; then the docs job and the act self-test at this head (below). It changes the CI page alone, which neither boundary command reads |

One-line subjects, no body, no trailers, configured identity. `git diff --stat 8436dfc0 HEAD`: 15 files, 6 commits. No firmware source or header, no image builder, no mutation table, no coverage row, no Makefile, no build flag; the linked images are byte-identical (below).

### Item 1: the boundary job

| What | Where (at the head, `4cab445a`) |
|---|---|
| A build-only mode in the harness: `fw_gtest.Execution` (one per process, `EXECUTION`); a gate's `--build-only` clears `run` before it builds; every binary is then built and linked as before and `run_binary` runs none, answering `built, not run (--build-only)` with no failure | `sw/firmware/gtest/fw_gtest.py:19` (docstring), `:55` `NOT_RUN`, `:63` `Execution`, `:72` `EXECUTION`, `:219` |
| The three suite gates take `--build-only`, refuse it with `--self-test` (no test runs, so no defect is planted), and end `BUILT`, never `PASS` or `OK`: the control gate (every arm's binaries and its RV32 build; with `--coverage`, the coverage builds), the store's gate (every shape's binaries and its RV32 arm; its log now prints the `built, not run` lines), the coverage gate (both gates' coverage builds by their `--build-only`; nothing run or measured; `measure` split into `coverage_runs` and the reading) | `test_ctrl_firmware.py:91`, `:158` `verdict`, `:183`, `:190-191`; `test_ctrl_nvm.py:36`, `:128` `evidence`, `:257-262`, `:288`; `fw_coverage.py:48`, `:436`, `:458` |
| The known set runs the builds: `ctrl_configs.BUILDERS` now gives `test_ctrl_firmware.py --require-rv32 --build-only --jobs 4`, `test_ctrl_nvm.py --require-rv32 --build-only --jobs 4` and `fw_coverage.py --build-only --jobs 4` (was `--self-test`; no flag; `--selftest` and `--check`); `fw_rv32_selftest.py --require-rv32` runs as it was (it compiles its planted header, ABI and runtime cases and runs no binary) | `sw/firmware/ctrl/test/ctrl_configs.py:9` THE BUILDERS, `:99-132` |
| The builders found by text that compile only in a suite, which a build-only run does not run: `SUITES`, each with what it compiles there (the control, AECP and SRP campaigns: planted copies, and the checkout's tests against them; the coverage reader's planted cases: programs it writes outside the checkout). Without it the first run refused all four by name, as the cross-check must (`logs/bjob-1.log`) | `ctrl_configs.py:167` `SUITES` |
| A dropped builder refuses by name (commit `0b4c140a5`). The probe at `09af0d04` (`test_ctrl_nvm.py` removed from `BUILDERS` in a scratch clone, the `firmware-boundary` command) passed, rc 0 (`logs/probe-drop.log`): the coverage gate runs the store gate (and the control gate) as a program of its own, so the dropped builder still compiled in the capture, which both checks took as held. Two rules close it, both in `held`: a known builder must hold an invocation from a run of its own (the record already kept its command's builder file, CTRL_CAPTURE_RUN; the reader now keeps it apart, `Invocation.run`, `Capture.ran`); and a builder found by text that is a program (a Makefile, or a Python module with a `__main__` block) must be known or listed, compiling inside another builder's run being enough only for a module that is no program. Two programs are listed with the builder they run under (`PART_OF`): `aecp_arms.py` (a developer's runner of the AECP arms the control gate builds) and `ctrl_build.py` (whose program is the pin check the bench's Makefile runs). The probe at the fix: rc 2, `REFUSED: sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py names the firmware's tree and is a program, and is neither a known builder (ctrl_configs.BUILDERS) nor listed ...` (`logs/probe-fix.log`) | `ctrl_capture.py:359` `run`, `:388` `ran`, `:487`; `ctrl_configs.py:9` THE BUILDERS, `:137` `PART_OF`, `:230` `program`, `:259` `held` (`:270` own run, `:277` program) |
| Two standing controls plant each (firmware run: 105 boundary controls, was 103): a known builder whose own run compiles nothing, which another builder still runs (`alter="drop run ..."`, the control gate), and a builder dropped from the known set, which another builder still runs (`alter="forget ..."`, the store gate), each refused by name | `ctrl_plants.py:41` (the alterations), `:490-495`; `ctrl_runs.py:257` (drop run); `ctrl_boundary.py:316-317` (forget) |
| The job: `firmware-boundary`, `needs: changes`, the same `if`, 30 minutes; checkout, the five submodules, GoogleTest and GoogleMock, the RV32 SDK's cache and install, then `ctrl_boundary.py --require-rv32 --selftest --without verilator` with no capture: the gate reads its builders from `BUILDERS` (`ctrl_runs.standalone`) and runs each by its builds under its own capture, then the stack's gate and the image builders (as before), then judges | `.github/workflows/rtl-fast.yml:296-342` |
| `firmware-unit` back to dev's steps (no `ctrl_capture.py` prefix, no boundary step), with the stack fetched; 45 minutes unchanged | `rtl-fast.yml:247-294`; `git diff 8b61b709 HEAD -- .github/workflows/rtl-fast.yml` shows only the fetch line in that job |
| The aggregate requires it: `needs` and the verdict pair `firmware-boundary:$FIRMWARE_BOUNDARY_RESULT` | `rtl-fast.yml:417`, `:428`, `:439` |
| `ci_events.py` pins it: `FIRMWARE_BOUNDARY_JOB`, its six-step list, `FIRMWARE_BOUNDARY_RESULT` in the aggregate's env; `firmware-unit`'s list back to dev's nine steps; the RV32 arms per job (`RV32_REQUIRED_STEPS`: `firmware-unit`'s two suite steps, `firmware-boundary`'s gate step) and `firmware-boundary`'s cache, installation and step-count arms; the unused `CAPTURE` constant removed | `scripts/ci_events.py:594`, `:1262`, `:2401`, `:7814`, `:7830-7831`, `:7852`; the self-test now runs 2610 arms (round 7: 2530), 93 of its lines naming `firmware-boundary` |
| Wording: the gate's messages, docstrings and the firmware README say "the firmware builders" where they said "the firmware steps" | `ctrl_boundary.py:63` THE CAPTURE, `:376`, `:396`, `:399`; `ctrl_plants.py:42`; `ctrl_runs.py:18` |

A dropped builder refuses by name: the probe and its controls above.

### Item 2: budget

Local figures are the CI-parity container (Ubuntu 24.04.5, CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28) on four CPUs of a shared host, a fresh clone at the head; the job setup (checkout, submodules, apt, SDK cache) is not replicated, and took 25 to 35 s hosted.

| Job | Timeout | Local, at `09af0d04` | Share | Hosted |
|---|---|---|---|---|
| `firmware-unit` | 45 min (2700 s) | steps 1986 s (`logs/ujob-1.outer`, its own four CPUs; 2074 s at `09af0d04`, `logs/ujob-head.outer`, where my docs gates shared its CPUs for about three minutes); the control gate 1686 s of it | 74 % (77 %) | at `8436dfc0` cancelled at 45 min (job 114392589133); dev's own, no capture: `8b61b709` 1963 s (job 114029646010, 73 %), and the 64 successful runs on other branches among `rtl-fast`'s last 80: eight early ones 278 to 386 s, the other 56 1302 to 2468 s, the twenty most recent 1484 to 2462 s (`logs/hosted-unit-other.txt`) |
| `firmware-boundary` | 30 min (1800 s) | step 682 s at `0a9c5fa8` (`logs/bjob-final.log`); 638 s at `09af0d04` (`logs/bjob-head.log`) | 38 % (35 %) | not yet run (needs a push) |
| `firmware-verilator` | 40 min (2400 s) | step 494 s at `0a9c5fa8` (`logs/vjob-final.log`); 454 s at `09af0d04` | 21 % (19 %) | at `8436dfc0` 682 s (job 114392589175), 28 % |

`firmware-boundary`'s step at `09af0d04`: the builders 567 s (the control gate's `--build-only` 272 s, the coverage gate's 211 s, the store's 76 s, the RV32 self-test 8 s), then the image builders, the stack's gate, the 103 boundary controls and the 20 pin controls in about 70 s. At `0a9c5fa8`: the builders 614 s (the control gate 299 s, coverage 226 s, the store 80 s, the RV32 self-test 9 s) and the rest 68 s, the Verilator replica, the docs job and the act self-test running on the other four CPUs meanwhile. The capture holds 3053 invocations (round 7's of the suites: 23,795), 2822 compiled sources (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own).

`firmware-unit` does not meet 60 % of 45 minutes, and this round cannot make it: with no capture at all, its suites are dev's own (this lane adds the stack's eight ADP and six ACMP tests to arms that already ran), and the job runs 1484 to 2462 s hosted on other branches' twenty most recent runs (55 to 91 %), 1963 s at this lane's base. The control gate's mutation campaigns are most of it (1686 s of 1986 s here). Meeting 60 % needs a longer timeout (the slowest of those runs, 2462 s, would need 69 minutes) or the campaigns sharded across jobs (`test_ctrl_firmware.py --mutation-shard`); the first is a timeout change, which the CI page records as a ruling (#673), and the second changes what the job runs; neither is this round's to take. Published as an open question.

### Item 3: nothing else changes

- The judgement is unchanged: `ctrl_boundary.py`'s `Places`, `findings_of`, `judged`, `judge` and every control are round 7's; the diff to the gate's modules is the known set's commands, `SUITES`, and wording (`git diff 8436dfc0 HEAD -- sw/firmware/ctrl/test`).
- Every standing control still refuses by name: 105 boundary controls (the base, 96 refused by name, 8 passing; the two new ones above) and 20 pin controls, 0 misbehaved, in `firmware-boundary`; 6 and 20, 0 misbehaved, in `firmware-verilator`, which names the firmware run's 104 plants as left out (`logs/bjob-final.log`, `logs/vjob-final.log`). The Verilator run's figures are round 7's exactly: 816 compiled sources of 916 invocations (386, 94, 336).
- The population. The capture now holds the builds, not the suites, so the planted-defect campaigns' compiles leave it (the manager's "builds only, not the suites"). Measured on round 7's capture of the suites (`round7/cap2`) against a capture of the four build commands at this tree (`capb`), both read by the gate's own reader and classification (`scripts/popcmp.py`, `scripts/phases.py`, `scripts/popdiff.py`):
  - by phase, the compiles of the arms' builds (798 firmware, 154 stack, 135 checkout, 31 outside), the store's (44, 80), the coverage builds (386, 80, 93, 7 and 29, 80) and the RV32 self-test's (12 stack, 70 outside) are the same counts in both; what leaves is the campaigns' (control, AECP, SRP at one and two interfaces: 14,019 outside the checkout, 1,715 of the firmware's, 931 of the stack's, 199 of the checkout's) and their tests' preprocessing;
  - every judged fact of the builds' capture is in the suites' (266 of 266 facts of what a firmware or stack source read, 659 of 659 include edges from a file of the checkout); the suites' capture holds 5 facts and 20 edges more, each a stack test or a test file of the checkout reading or including a file outside the checkout (the campaign's planted copy), which every rule admits (`logs/popdiff-cap2-capb.txt`). No fact a rule can refuse is lost.
- Firmware gates (`firmware-unit`'s steps, no capture) at `09af0d04`, in a fresh clone; no module those commands load changed after it (`git diff 09af0d04 0a9c5fa8` touches the gate's modules and two pages, which none of them imports): the firmware gate's 845 verdict lines byte-identical to rounds 4 to 7 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, 59 arms `[ok]`, `mutants: 471 of 471 caught`, every AECP and SRP defect and both lwSRP pin arms `[ok]`, `test_ctrl_firmware: PASS`); the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `fw_coverage.py --check` PASS (30 files), its table row for row round 7's (`logs/cov-ujob1.txt`). The gate's log is 317,882 bytes (sha256 `a8ce22e685cc0ed3e78ee068ec2ca7364d169e6b9cbf075eb799d1151c4017c1`, the run with `f878188c`'s harness files; at `09af0d04` 317,882 bytes, sha256 `228b1470c9eaea89dbb36ea145726e3119b15337b7796d16fbcec604b7fa6066`), not copied.
- Images: 35 of 35 ELF files relinked at the head (`images6.sh`, the pinned SDK, round 1's runtime archives), the manifest byte-identical to rounds 6 and 7 and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `round8/images-head.sha256`); every hash of the round-1 table above holds.

### Gates at the round-8 head

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | CI-parity container, fresh clone at `0a9c5fa8` (the head but its CI page), four CPUs | PASS: `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) ...; 0 finding(s), 105 boundary and 20 pin controls, 0 misbehaved`, the two new controls refused by name, 682 s (`logs/bjob-final.log`) |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | the same image with the pinned Verilator 5.050 and RV32 SDK mounted, fresh clone at `0a9c5fa8` | PASS: `816 compiled sources of 916 recorded invocations (386 the firmware's, 94 the stack's, 336 test equipment's and builders' own) ...; 0 finding(s), 6 boundary and 20 pin controls, 0 misbehaved`, the firmware run's 104 plants named as left out, 494 s: bench 55 s, differential 148 s, wire comparison at both references 215 s (`logs/vjob-final.log`) |
| `firmware-unit`'s steps (`unitjob.sh`: tally self-test, RV32 self-test, the control gate with `--self-test`, the store's gate, the coverage self-test and check) | CI-parity container, fresh clone at `09af0d04` (no module these commands load changed after it) | every step rc 0, 2074 s (`logs/ujob-head.outer`); the same with `f878188c`'s harness files in 1986 s (`logs/ujob-1.outer`); results above |
| the docs job's 54 commands (`docsjob.sh`, CPython 3.12.3 with the locked renderer) | fresh clone at `4cab445a` with the docs job's three submodules | 54 of 54 rc 0 (`logs/docsjob-head2.txt`): `ci_events.py --check` OK (1902 items), `--selftest` PASS (2610 arms); `check_py_idiom.py` every ratchet held; `check_em_dash.py --base 8436dfc0` 0 findings over 62 added lines; `docs_check.py` 0 findings across 202 pages; `measure_fail_fast.py --selftest` 106 of 106 |
| `act_ci.py --selftest --worktree <head clone>` (the copy installed 0555 outside the tree, sha256 `797f123b…d22d1`, identical to the tree's, which this round does not change) | host, CPython 3.12.3 with PyYAML, `--worktree` a clone at `4cab445a` | PASS, 446 arms, line for line round 7's (`logs/act-selftest-head2.log`) |
| `--build-only` with `--self-test` (control and store gates) and with `--check` (coverage gate) | host | rc 2, each refused by name |
| images (`images6.sh`) | host, pinned SDK, clone at `09af0d04` (no image builder or firmware file changed after it) | 35 of 35 identical to round 7 |
| dropped-builder probe: `test_ctrl_nvm.py` removed from `BUILDERS`, `ctrl_boundary.py --require-rv32 --without verilator` | CI-parity container, scratch clones | at `09af0d04`: rc 0, PASS (the gap; `logs/probe-drop.log`); at the fix: rc 2, refused by name (`logs/probe-fix.log`) |

### Open risks and questions (round 8)

1. `firmware-unit` over 60 % (Item 2): its suites alone are dev's, 1484 to 2462 s hosted on other branches' twenty most recent runs; a longer timeout or sharded campaigns would meet 60 %, and both are decisions this round does not take.
2. The population (Item 3): the campaigns' compiles of planted copies no longer reach the boundary. Measured, they add no fact a rule can refuse; a defect a planted copy alone could show would be a defect of the plant, not of the tree. `SUITES` names the four modules that compile only there; a module listed there that later compiles in a build is judged as any other, since a builder that compiled in the capture needs no listing.
3. `firmware-boundary`'s 30-minute timeout is this round's choice for a new job: 638 s locally is 35 %; hosted `firmware-unit` runs on other branches have taken up to 24 % longer than this replica of its steps (2462 s against 1986 s). Hosted figures need a push.
4. The program rule is read from the text (`__main__`, or a Makefile): a builder program written without a `__main__` block (run by `runpy`, or a shell script) would be held as a module, by having compiled in the capture. None exists; the two programs that run under another builder are listed in `PART_OF`.
5. Round 7's eight interpretations stand unchanged (see Round 7).

## Round 9

Assignment: #697 comment [6107732413](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107732413), answering R584-7 ([6107725598](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6107725598)) and R585-7 ([6107554012](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6107554012)), both NEGATIVE at `4cab445a` with the same two MINOR findings: (1) the stack pin check follows replacement objects; (2) the README's 95 should be 96. RES1 is the manager's at merge (#495); S1 is optional.
Base of the round: `4cab445aa2475903b6cf8b87566d2c8a1e15e391` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `feed95bbb6429e5af0ee3f0a24c531777279e9de`.
Status: REVIEW READY, comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179) (its text: `round9/review-ready-round9.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `2d24214d0` | Prove the stack pin from the real objects alone through one Git helper, over the whole tree with its types and modes, and hold the proof's Git commands to that helper by a census | the pin controls in-process (`logs/pin-controls-nomake.log`, 24 of 24 `[ok]` without the Makefile builders' bench arms); six in-process mutants of the proof (`logs/pin-mutants.log`, below); the census over seven planted forms (`logs/census-forms.log`); both reviewers' probes on the working tree (`logs/probe-r584-worktree.txt`, `logs/probe-r585-worktree.txt`: every replacement case REFUSED); `ctrl_build.py --stack-pin` exit 0; pyflakes; `check_py_idiom.py` (every ratchet held after `pin_controls` was split into `Clone`: long function 9 <= 9, os.path use 1 <= 1), `check_hygiene.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `measure_test_evidence.py --check`, `docs_check.py`, `check_em_dash.py --base 4cab445a` (14 added lines, 0 findings), `check_doc_paths.py`, `gen_toc.py --check`, all rc 0 |
| `107aab303` | Give the firmware README the boundary self-test's own figures, 96 defects among them, and refuse a figure there that is not the self-test's count of its controls | the figure check and its four controls in-process (`logs/figures-unit.log`: none at the head; at `4cab445a` it names the 95); pyflakes, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --check`, `check_em_dash.py --base 4cab445a` (18 added lines, 0 findings), all rc 0; then both boundary replicas at this commit (PASS, below) and the docs job, whose `ci_scope.py --selftest` failed (next row) |
| `feed95bbb` | Edit the stack's LICENSE in the pin control for a file no gate builds, so no literal there names a documentation page ci_scope reads | `ci_scope.py --selftest` failed at `107aab30` with `FAIL gate-read page README.md (named at sw/firmware/ctrl/test/ctrl_pin.py:479) is relevant` (`logs/docsjob-head/scripts_ci_scope.py_--selftest.log`): its scan reads a bare `README.md` literal as the top-level page. The control now edits the stack's `LICENSE`. `ci_scope.py --selftest` PASS, the pin controls 24 of 24, the census and the figures clean, pyflakes, `check_py_idiom.py`, `docs_check.py`, `check_doc_paths.py`, all rc 0; then every replica at this head (below) |

One-line subjects, no body, no trailers, configured identity. `git diff --stat 4cab445a HEAD`: 4 files (`sw/firmware/ctrl/README.md` +24/-, `ctrl_boundary.py`, `ctrl_build.py`, `ctrl_pin.py`), 397 insertions, 112 deletions. No firmware source or header, image builder, mutation table, coverage row, Makefile, workflow, build flag or tsn-c-stack pin changes; the linked images are byte-identical (below).

### Item 1: the pin proof reads the real objects

| What | Where (at the head) |
|---|---|
| One Git helper. `ctrl_build.git(directory, *args, stdin=None)` runs `git -C <directory> ...` with `ctrl_build.git_env()`: the caller's environment with `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null/no-grafts` (`NO_GRAFTS`, a path under a file, which no directory can be, so it can never exist). It captures output as UTF-8 with `surrogateescape`, so any path round-trips. Every Git call of the pin proof goes through it: `stack_gitlink` (`ls-files --stage`), `stack_pin` (`rev-parse --show-toplevel`, `rev-parse HEAD`, `rev-parse --show-object-format`, `ls-tree`), and in `ctrl_pin.py` `mirror`'s `ls-files` and every control's setup (`Clone.fresh`, `Clone.answer`). `ctrl_build.run` is kept for its other callers (`aecp_arms.py`, `ctrl_srp_image.py`), which run no Git | `sw/firmware/ctrl/test/ctrl_build.py:180` `NO_GRAFTS`, `:183` `git_env`, `:189` `git`, `:196` `stack_gitlink`; `ctrl_pin.py:255` (`mirror`), `:325` `Clone.fresh`, `:333` `Clone.answer` |
| Verified on this host's Git 2.56.0 before relying on it: `GIT_NO_REPLACE_OBJECTS=1` neutralises a replace ref but not `info/grafts` (`rev-parse HEAD^` still printed the grafted parent with it alone); `GIT_GRAFT_FILE` pointing at a missing path does, with no warning (ENOTDIR is not reported) | scratch experiment, `round9/exp` (not kept) |
| Disk bytes are hashed without Git: `blob_id` hashes `blob <len>\0<bytes>` of the file itself (a symbolic link's target), with the repository's object format, never through an index, attribute or filter | `ctrl_build.py:205` |
| The whole tree. `stack_pin` reads the pinned commit's whole tree (`ls-tree -r -t -z --full-tree <pin>`, trees included) and `on_disk` reads every entry of the checkout but its own top-level `.git`: a directory as `040000 tree`, a symbolic link as `120000 blob <target's id>`, a regular file as `100755` when its owner may execute it else `100644`, with its blob id, anything else as no type a tree holds. The two maps must be equal: the same path set, the same type and mode at every path, the same blob for every file and link; every differing path is named. `STACK_PROVEN` (round 2's seven parts) and `worktree_files` are gone. This settles R584-6-S2 (executable mode) | `ctrl_build.py:212` `on_disk`, `:235` `stack_pin`, `:249` the `ls-tree` |
| The census. `ctrl_pin.census(texts, env)` parses each module of the pin proof (`PROOF`: `ctrl_build.py`, `ctrl_pin.py`) and names every string constant (bytes too, f-string parts included) outside the helper's body and the docstrings in which the Git program's name stands as a word (`GIT_WORD`: not inside `gitlink`, `.git` or a URL's `.git`); a missing helper in `ctrl_build.py`; and a helper environment that does not set `GIT_NO_REPLACE_OBJECTS=1` or whose `GIT_GRAFT_FILE` is unset or exists. The census builds its own pattern and anchors from the helper's name (`HELPER = git.__name__`), so no string of `ctrl_pin.py` names the program; the gate's messages spell it `Git`. `proof_census()` runs it over the checkout with the helper's own environment; `ctrl_boundary.py` adds its findings on every run, not only `--selftest`. Stated limit: a program name assembled at run time is not seen | `ctrl_pin.py:11` THE CENSUS, `:67` `PROOF`, `:70` `HELPER`, `:72` `GIT_WORD`, `:111` `census`, `:143` `proof_census`; `ctrl_boundary.py:514` |
| Standing controls (pin controls 20 to 30). Each spoils a fresh clone and calls the pin check directly, so each is refused before any build: a file no gate builds edited (the stack's `LICENSE`; the whole tree), a symbolic link standing in for `src/adp.c` to a copy of its own bytes (type), `scripts/check_boundary.py` made executable (mode); and, with `src/adp.c` edited on disk, a replacement tree (the pinned `src/` tree replaced by one holding the edit, written with `hash-object -w`, `mktree`, `replace`), a replacement commit for the pin (a copy of the pinned commit whose root tree holds the edit, written with `hash-object -t commit -w`; HEAD still prints the pin), a graft file (`info/grafts` making the pin a root), and a clean filter applied through attributes (`info/attributes` gives `src/adp.c` a `head -c <size>` filter in the clone's config; the control first checks that `git hash-object src/adp.c` through the filter prints the pinned blob, else its setup refuses). Each must be refused naming `src/adp.c` (or the changed file). The clean clone still passes. The three census controls: `ctrl_build.py` with the pin check reading HEAD by `run(["git", ...])` (the round-8 form) must be named at its line; the helper environment without `GIT_NO_REPLACE_OBJECTS`, and without `GIT_GRAFT_FILE`, must each be named. `ctrl_pin.Clone` holds the setup (so `pin_controls` stays under the 100-line ratchet) | `ctrl_pin.py:29` THE CONTROLS, `:314` `Clone`, `:344-411`, `:419` `counted`, `:426` `outside`, `:436` `without`, `:441` `pin_controls`, the arms at `:479-499` |
| The README and the docstrings say the whole-tree, real-object proof and the census, and name the controls | `sw/firmware/ctrl/README.md:163-188`; `ctrl_boundary.py:77` THE PIN; `ctrl_build.py:235` `stack_pin` docstring; `ctrl_pin.py:3-49` |

The graft. A graft rewrites only a commit's parents, and nothing the proof reads depends on a parent (`rev-parse HEAD`, the pinned commit's tree). So the graft control cannot fail by the helper dropping `GIT_GRAFT_FILE` alone; it shows that a graft carries no altered stack past the proof, and the helper's graft setting is held by the census's environment check, which the third census control plants. The mutants below show both.

Mutants of the proof (`round9/scripts/pin_mutants.py`, patched in-process, `logs/pin-mutants.log`), each run against the 24 pin controls that need no Makefile builder, with the gate's census on the mutant:

| Mutant | Controls that fail (ESCAPED) | Census |
|---|---|---|
| helper without `GIT_NO_REPLACE_OBJECTS` | the replacement tree and the replacement commit (accepted), and the third census control (its finding is the first variable's) | names it |
| helper without `GIT_GRAFT_FILE` | none (above) | names it |
| disk hashed through Git's filters (`git hash-object <path>`) | the clean filter (accepted) | clean |
| modes not compared | the script made executable (accepted) | clean |
| symbolic links followed (type not compared) | the symbolic link (accepted) | clean |
| only round 8's seven parts compared (both sides) | the file no gate builds (accepted) | clean |

The census over planted forms (`round9/scripts/census_forms.py`, `logs/census-forms.log`), a line added to `ctrl_pin.mirror`: a command list (`run(["git", ...])`), a shell line, `shutil.which("git")`, `/usr/bin/git`, a Python program run with `-c`, an f-string: each named at its line; `"g" + "it"`: not seen (the stated limit). The checkout as it is: no finding.

The reviewers' probes (fetched from `697c-review-evidence`, read before running; each makes a disposable clone in a scratch directory):

| Probe | `4cab445a` (base) | `feed95bb` (head) |
|---|---|---|
| R584-7 `scripts/pin_replace_probe.sh <checkout> <stack repo> <work>` step 3 (`refs/replace/<pin>` -> `ae982af`, its files on disk) | `ACCEPTED: tsn-c-stack at 1a9f651c...` | `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: CMakeLists.txt, cmake, ...` (steps 2 and 4 refuse as before; step 1 accepts) |
| R585-7 `pin_probe.py <checkout> <scratch>` (the `include/` tree replaced, `ADP_ADVERTISE_MS 9000u` on disk, the compiler reading 9000u) | `replacement control: ESCAPED; pin check accepted 1a9f651c...` | `replacement control: REFUSED tsn-c-stack differs from the pinned 1a9f651c: include/adp.h`; the restored clone accepted |

Logs: `logs/probe-r584-base-p.txt`, `logs/probe-r584-final-d.txt`, `logs/probe-r585-base-p.txt`, `logs/probe-r585-final-d.txt`.

Every entry point (`round9/scripts/entrypoints.py`, `logs/entrypoints.log`): in a full clone at the head whose submodule holds `ADP_ADVERTISE_MS 9000u` in `include/adp.h` disguised by each of a replacement tree, a replacement commit for the pin, a graft file and a clean filter (`sed` turning it back into the pinned blob), and a fifth state with `scripts/check_boundary.py` made executable, each of 17 entry points must exit non-zero naming the changed file: `ctrl_build.py --stack-pin`, `test_ctrl_firmware.py --build-only` and `--self-test`, `fw_coverage.py --check`, `ctrl_image.py`, `ctrl_srp_image.py`, `ctrl_boundary.py --without verilator`, `maap_differential.py` and its `--self-test`, `aecp_arms.py --app`, `aecp_mutants.py --shard 0 1000`, `aecp_wire.py`, and `make -C tb/verilator/mbx` for `stack-pin`, the firmware library, `run-cosim`, `run-if2` and the default target. 85 of 85 refused, each `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: include/adp.h` (or `scripts/check_boundary.py`), exit 2, at `107aab30` and again at `feed95bb`.

### Item 2: the README's figures, checked against the self-test's population

| What | Where (at the head) |
|---|---|
| The figure corrected: 96 defects refused by name and 8 passing controls in the firmware builders' run (the base besides: 105); 5 in the Verilator builders' run; 30 pin controls (was "Twenty"). Written as numerals so the check reads them | `sw/firmware/ctrl/README.md:151`, `:158`, `:179` |
| No figure check existed in the repository: the "structure check" R585-7 cites (`structure_check.py`) is the reviewer's own script on the evidence branch. The check is added to the boundary self-test, which owns the population: `population(pins)` counts `ctrl_plants.PLANTS` (firmware run: needle and no needle; the Verilator run) and the pin controls the run made; `figures(text, counts)` reads the four sentences (`FIGURES`) and names each figure that is not the count, or that the page gives other than once; a finding fails the gate. `figure_controls` plants the page with each figure one more and requires a finding naming that figure (4 controls). It runs under `--selftest`, in both hosted runs (the counts are the same in each). The page is named as `fw_coverage.README` names its own, joined from stem and suffix, for `ci_scope.py`'s scan | `ctrl_boundary.py:154` `README`, `:156` `FIGURES`, `:409` `population`, `:417` `figures`, `:428` `figure_controls`, `:93` (docstring), `:514`, `:525` (the summary line: `<n> boundary, <n> pin and 4 figure controls`) |
| Against the README at `4cab445a` the check names the 95 (`gives the defects in the firmware builders' run as 95, where the self-test has 96`) and the three figures written as words (`as nothing`) | `logs/figures-unit.log` |

### Gates at the round-9 head

Local figures: the CI-parity container (Ubuntu 24.04.5, CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each, fresh clones; the docs job, the probes and the images on the host with CPython 3.12.3 (PyYAML, the locked renderer) and the pinned SDK.

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | container, fresh clone at `feed95bb` | PASS, 677 s (38 % of 30 minutes): `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) ..., every Makefile builder's pin prerequisites and the pin proof's census; 0 finding(s), 105 boundary, 30 pin and 4 figure controls, 0 misbehaved` (`logs/bjob-final.log`); at `107aab30` the same, 691 s (`logs/bjob-head.log`) |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | container with the pinned Verilator 5.050 and the RV32 SDK, fresh clone at `feed95bb` | PASS, 492 s (21 % of 40 minutes): `816 compiled sources of 916 recorded invocations (386, 94, 336) ...; 0 finding(s), 6 boundary, 30 pin and 4 figure controls, 0 misbehaved`, the firmware run's 104 plants named as left out (`logs/vjob-final.log`); at `107aab30` 480 s (`logs/vjob-head.log`) |
| `firmware-unit`'s steps (`unitjob.sh`: tally self-test, RV32 self-test, the control gate with `--self-test`, the store's gate, the coverage self-test and check) | container, fresh clone at `107aab30`; `feed95bb` changes only `ctrl_pin.py` and the firmware README, which no command of this job loads or reads | every step rc 0, 2051 s (76 % of 45 minutes; `logs/ujob-head.outer`): the firmware gate's 845 verdict lines byte-identical to rounds 4 to 8 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `logs/fw-verdicts-head.txt`: `tsn-c-stack at 1a9f651c...`, 843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`); the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `fw_coverage.py --check` PASS (30 files), its table row for row round 8's (`logs/cov-head.txt`). The gate's log is 317,882 bytes, sha256 `d1c6f1a106be57421dedeeea7da87bda0dd6aa9f2c6b7af4571c20134e04e362`, not copied |
| the docs job's 54 commands (`docsjob.sh`) | fresh clone at `feed95bb` with the docs job's three submodules | 54 of 54 rc 0 (`logs/docsjob-final.txt`): `ci_events.py --check` OK (1902 items), `--selftest` PASS (2610 arms); `ci_scope.py --selftest` PASS; `check_py_idiom.py` every ratchet held; `check_em_dash.py --base 4cab445a` 0 findings over 18 added lines; `docs_check.py` 0 findings across 202 pages; `measure_fail_fast.py --selftest` 106 of 106. At `107aab30`: 53 of 54, `ci_scope.py --selftest` failed (the README literal, fixed by `feed95bb`) |
| images (`images6.sh`) | host, pinned SDK, round 1's runtime archives, fresh clone at `feed95bb` | 35 of 35 ELF files relinked; the manifest byte-identical to rounds 6, 7 and 8 and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `round9/images-head.sha256`); every hash of the round-1 table holds |
| the reviewers' probes | clones at `4cab445a` and `feed95bb` | base: ACCEPTED / ESCAPED; head: REFUSED / REFUSED (Item 1) |
| every entry point under each disguise (`entrypoints.py`) | full clones at `107aab30` and `feed95bb` | 85 of 85 refused by name (Item 1) |
| pin-proof mutants, census forms | host, in-process | as tabled in Item 1 |
| `act_ci.py --selftest` | not run: this round changes no workflow, `act_ci.py` or `ci_events.py`; round 8's run at `4cab445a` stands for those files |

Memory: the service stayed near 1 GB; each container under 0.5 GB when sampled.

### Open risks and questions (round 9)

1. The census reads text. A program name assembled at run time, or a Git command started by a function of another module the proof calls, would not be seen; the proof's modules call no other module that runs Git (`fw_gtest.run`, the only other process helper `ctrl_build` reaches, runs none for the proof). Stated in the README and `ctrl_pin.py`.
2. The graft control cannot fail by the helper dropping `GIT_GRAFT_FILE` alone, because nothing the proof reads depends on a commit's parents; the census's environment check holds that setting, planted by its third control. A reviewer may prefer the proof to refuse a repository that holds a graft file or replacement refs outright; that would be a further rule, not taken here (the assignment asks that Git read the real objects).
3. The whole tree: the pin check now compares every entry of the submodule's checkout but its `.git`, so anything left inside it (a CMake build directory made there, an editor's backup) refuses every gate by name until removed. The README's command for the stack's own suite builds outside it.
4. No figure check existed in the repository; the "existing structure check" of the assignment is read as R585-7's own `structure_check.py`, and the check is added to the boundary self-test, which owns the population. It reads four sentences of the firmware README; a figure written elsewhere on the page is not checked.
5. S1 (exact-head hosted figures on the CI page) is not applied: this round changes what `firmware-boundary` runs, so `4cab445a`'s hosted figures (13 min 34 s; `firmware-verilator` 10 min 31 s) are not this head's. RES1 is the manager's at merge; the PR body's two stale lines are corrected in `PR-BODY.md` with the reviewers' exact wording.
6. `firmware-unit` stays over 60 % of its 45 minutes (2051 s here, 76 %), its suites alone; ruled #716's scope.
7. The lwSRP pin check (`ctrl_arms.lwsrp_pin`) is unchanged; it is lwSRP's, not the stack pin proof.
