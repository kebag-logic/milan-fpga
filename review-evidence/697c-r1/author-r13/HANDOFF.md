# HANDOFF — lane 697c, [A583]

Issue: [kebag-logic/milan-fpga#697](https://github.com/kebag-logic/milan-fpga/issues/697), assignment comments 6091228902 (round 1), 6092628778 (round 2), 6093389868 (round 2b), 6094873968 (round 3), 6096148471 (round 4), 6097800045 (round 5), 6102039501 (round 6), 6104711137 (round 7), 6105928035 (round 8), 6107732413 (round 9), 6112358746 (round 10), 6113306444 (round 11), 6114400461 (round 12) and 6116488747 (round 13).
Branch: `697-consume` from dev `8b61b70902f3ebf118e56967277e2686731081bd`, pushed as PR #705; PR #705 shows round 12's head `adb93604`.
Head: `8aaa2da74e3d5ee569fed420debc2b69c6749d44` (round 13: four commits and a merge of dev `c20c85bd` on `adb93604`, not pushed; PR #705 shows `adb93604`).
Status: round 13 REVIEW READY at `8aaa2da74`, comment [6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531) (its text: `round13/review-ready-round13.md`) (pin `405dc683`, dev `c20c85bd` merged, F-INT's plants retargeted, images identical to dev's; see [Round 13](#round-13)); round 12 STOP at `adb936049` (item 1, the dev merge; items 2 and 3 done), comment [6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316) (its text: `round12/stop-round12.md`) (see [Round 12](#round-12)); round 11 REVIEW READY at `aca5e8afc`, comment [6114209149](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114209149) (its text: `round11/review-ready-round11.md`) (see [Round 11](#round-11)); round 10 REVIEW READY at `be607527e`, comment [6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) (its text: `round10/review-ready-round10.md`) (see [Round 10](#round-10)); round 9 REVIEW READY at `feed95bbb`, comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179) (see [Round 9](#round-9)); round 8 REVIEW READY at `4cab445aa`, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`) (see [Round 8](#round-8)); round 7 REVIEW READY at `8436dfc0b`, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (see [Round 7](#round-7)); round 6 REVIEW READY at `5b4f6fbeb`, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`) (see [Round 6](HANDOFF-rounds-2-6.md#round-6)); round 5 REVIEW READY at `92b5be188`, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (see [Round 5](HANDOFF-rounds-2-6.md#round-5)); round 4's REVIEW READY was comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937); round 3's was comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057), round 2b's 6094033396, round 2's 6093383132. Round 1: TAKEN 6091267846, REVIEW READY 6092168627; the pin was confirmed in 6092176555.
PR body: `PR-BODY.md` in this directory (round 2 to 13 sections added, round 5's residue applied; no PR edit made).

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

Round 13 moves the pin to `405dc68310a18f669049ffc10cc23eef7300dcff` (tag `milan-fpga-697-pin-405dc683`), this pin plus F-INT's ACMP publish port, with the same proof against dev `c20c85bd` ([Round 13](#item-1-the-pin)). This section is round 1's.

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

## Round 10

Assignment: #697 comment [6112358746](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6112358746), answering R584-8 ([6112278003](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6112278003)) and R585-8 ([6112241098](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6112241098)), both NEGATIVE at `feed95bb` with one MINOR each, the same defect: the census matched spellings, so Git started under a computed name (R585-8) or in its dashed form (R584-8) passed it. Ruled by construction: in the pin-proof modules only the helper may start a process; an AST census refuses, outside the helper, any reference to a process-launch facility, and dynamic code; five standing controls; both probes must refuse. S1 to S3 are optional and not taken; RES-1 (and R585-8-RS1's recurrence) goes to #495 at merge, and R585-8-RS1's exact wording is applied in `PR-BODY.md`.
Base of the round: `feed95bbb6429e5af0ee3f0a24c531777279e9de` (PR #705's head). New commits only, no rebase or amend; not pushed.
Head: `be607527eaac84cfc8d7456167b070a22228345b`.
Status: REVIEW READY, comment [6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) (its text: `round10/review-ready-round10.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `65115fced` | Let only the helper start a process in the pin proof's modules, refusing by syntax tree every launch facility, dynamic code and reflection outside it, and any name outside the proof's vocabulary where the pin is decided | the clean census (no finding); the 8 census controls in-process; my census forms (`logs/census-forms.log`); R585-8's `census_probe.py` and R584-8's `pin_suite.py` and `proof_mutants.py` (all twelve) on a clone of the working tree; make's database and dry-run reading of every Makefile builder byte-identical to `feed95bb`'s (`logs/make-reading-*.json`, sha256 `4d681718…`); every non-census pin control's verdict line identical to `feed95bb`'s; pyflakes; the docs job's 54 commands on a clone of the working tree, 54 of 54 rc 0 (`check_py_idiom.py` every ratchet held) |
| `be607527e` | Say the pin proof's modules name no process-launch facility but the helper, since their build functions and tool runs start processes through the harness's runner, which what decides the pin cannot reach | wording only (README, three docstrings, two comments), found on rereading: "only the helper starts a process" overclaimed, since `ctrl_build.py`'s build functions and `ctrl_pin.py`'s tool runs start processes through `fw_gtest.run`; pyflakes, `check_py_idiom.py`; then every replica and probe again at this head (below). The replicas started at `65115fce` were stopped and restarted here |

One-line subjects, no body, no trailers, configured identity. `git diff --stat feed95bb HEAD`: 4 files (`sw/firmware/ctrl/README.md`, `ctrl_boundary.py` docstring, `ctrl_build.py`, `ctrl_pin.py`), 328 insertions, 82 deletions. No firmware source or header, image builder, mutation table, coverage row, Makefile, workflow, build flag or tsn-c-stack pin changes; the linked images are byte-identical (below).

### How the round reads "only the helper may start a process"

`ctrl_build.py` is the firmware's shared builder as well as the pin proof: its `compile_c`, `compile_tests`, `label`, `link`, `execute` and `run` start compilers, linkers and test binaries through `fw_gtest` (the harness), and the boundary gate's builder model names it so (`ctrl_configs.BUILDER_NAMES`, `PART_OF`). `ctrl_pin.py` runs `make` and the gates its controls run. Moving all of that out of the two modules would make "only the helper starts a process" literally true, but it reaches into the boundary gate's builder model, its plants and a dozen importers. The round does not take that. It holds two things by construction instead, and states what remains:

1. Module-wide, as the assignment's census specifies: outside the helper, neither module names a process-launch facility (by import, alias, name or attribute), dynamic code, or the reflection that would reach one unnamed. `ctrl_pin.py`'s own tool runs now go through `fw_gtest.run` (as `ctrl_build.run` always has), so `subprocess` is named only inside the helper, which imports it in its own body.
2. Where the pin is decided (`stack_gitlink`, `stack_pin`, the command line's `main`, and every function, class and constant of `ctrl_build.py` they name, followed through each): only a fixed vocabulary of names that start no process. So the decision reaches no process but through the helper, by any route or program name: `ctrl_build.run` is refused there, which is what the reviewers' probes plant.

What remains: a function of another module that starts a process (`fw_gtest.run`, through `ctrl_build.run` and the build functions, and `ctrl_pin.run`) is not a facility the census knows, and outside the decision it is not refused (two planted forms, `logs/census-forms.log`, `NOT SEEN, the stated limit`). Such a process cannot change what the decision reads, which goes through the helper's environment. Stated in the README, `ctrl_pin.py`'s docstring and the PR body.

### The census

| What | Where (at the head) |
|---|---|
| The helper alone names a facility: `ctrl_build.git` imports `subprocess` in its own body and returns its own `GitRun` (exit status, output, errors), so no module-level `subprocess` name exists; `ctrl_build.run` is now `fw_gtest.run` bound by name (the same function it called), kept for its two importers and for the reviewers' mutants | `sw/firmware/ctrl/test/ctrl_build.py:105` `run`, `:189` `GitRun`, `:197` `git`, `:201` the import |
| Module-wide (`launches`): outside the helper's nodes, in both modules, refused: an import of anything with `subprocess`, `pty` or a launch function among its dotted parts (`asyncio.subprocess`, `os.system`, `from subprocess import run as r`), and every later use of a name it bound; any attribute named `system`, `popen`, `startfile`, `fork`, `forkpty`, `exec{l,le,lp,lpe,v,ve,vp,vpe}`, `spawn{…}`, `posix_spawn`, `posix_spawnp`, `create_subprocess_exec`, `create_subprocess_shell`, `subprocess` or `pty`, on any object (so `shutil.os.system` too); the names `eval`, `exec`, `compile`, `__import__`, `importlib`, `builtins`, `__builtins__`, `getattr`, `setattr`, `delattr`, `vars`, `globals`, `locals`; an attribute beginning with an underscore (but `__name__`), a frame's or generator's (`f_`, `gi_`, `cr_`, `ag_`, `tb_`), or `modules`; a wildcard import | `ctrl_pin.py:101` `LAUNCH_NAMES`, `:106` `DYNAMIC`, `:110` `REFLECTIVE`, `:224` `launches` |
| Where the pin is decided (`reach`): from `ROOTS`, every name is resolved through the module's own bindings (`scope`: functions, classes, values, imports, each followed; a name bound some other way is refused), and must be a local, the helper, a builtin of `BUILTINS`, a module of `VOCABULARY` with only its listed names (`os`: `walk`, `readlink`; `hashlib`: `new`, `algorithms_available`; `stat`: four; `pathlib.Path`; `argparse.ArgumentParser`), or an attribute of `ATTRIBUTES` on its own values. A name both local and the module's is judged as the module's. Each finding names the line in the decision and, in brackets, why the name it uses may not be reached | `ctrl_pin.py:98` `ROOTS`, `:112` `VOCABULARY`, `:116` `BUILTINS`, `:120` `ATTRIBUTES`, `:189` `scope`, `:218` `spoken`, `:254` `reach` |
| The rest of `census`: exactly one `ctrl_build.py` given; the helper defined once and its name bound nowhere else (each other binding named at its line); the helper environment's two settings (unchanged) | `ctrl_pin.py:316` `census`, `:347` `proof_census` |
| `ctrl_pin.run` goes through `fw_gtest.run` (output then errors, `LC_ALL=C`). Make's database and dry-run reading of every Makefile builder is byte-identical to `feed95bb`'s, and every non-census pin control prints the same verdict line | `ctrl_pin.py:172`; `logs/make-reading-feed95bb.json`, `logs/make-reading-head.json` |
| The spelling check of round 9 (`GIT_WORD`, string constants naming the Git program) is gone: the route is held instead, so a computed or dashed name, or a Git string never launched, decides nothing | (removed) |
| Docs: the README's stack section states the contract and what remains; `ctrl_pin.py`'s THE CENSUS, `ctrl_boundary.py`'s THE PIN, `ctrl_build.git`'s docstring | `sw/firmware/ctrl/README.md:169-186`, `:191` (35), `:197-199`; `ctrl_pin.py:11-43`; `ctrl_boundary.py:77-85` |

### Standing controls

The three round-9 census controls become eight (`CENSUS_PLANTS`, `ctrl_pin.py:153`; `planted`, `:631`; `counted`, `:623`; `census_arms`, `:653`, used at `:720`); pin controls 30 -> 35, and the README's figure with them (checked by the figure check). Each plant replaces an anchor of a module (or is added at its end), and the census must name the plant's first line and the given words; a missing anchor is reported as a misbehaving control, by name.

| Control | Plant | Finding at the head |
|---|---|---|
| a Git command run by the harness's runner (round 9's, kept) | `stack_pin`: `head = run(["git", "-C", str(stack), "rev-parse", "HEAD"])` | `ctrl_build.py:256 stack_pin names run, which the pin decision may not reach (ctrl_build.py:105 the value of run names fw_gtest.run, outside the pin proof's vocabulary)` |
| a computed name (`git.__name__`) | `stack_pin`, R585-8's exact mutant: `tree = run([git.__name__, "-C", str(stack), "ls-tree", ...])` | `ctrl_build.py:260 stack_pin names run, ...` |
| a dashed program (`git-ls-tree`) | `stack_pin`: `tree = run(["git-ls-tree", "-r", "-t", "-z", "--full-tree", pin], cwd=stack)` | `ctrl_build.py:260 stack_pin names run, ...` |
| an aliased import | `stack_pin`: `from subprocess import run as r` and `tree = r([...])` | `ctrl_build.py:260 imports subprocess.run as r, a process-launch facility` |
| `os.system` | a line added at the end of `ctrl_pin.py` (outside the decision: the module-wide rule) | `ctrl_pin.py:745 names os.system, a process-launch facility` |
| `exec` of a string | `stack_gitlink`: `exec("entry = run([...], cwd=root).stdout.split()")` | `ctrl_build.py:210 stack_gitlink names exec, neither ctrl_build.py's nor in the pin proof's vocabulary` |
| the helper's environment without `GIT_NO_REPLACE_OBJECTS` / without `GIT_GRAFT_FILE` (round 9's, kept) | `without(name)` | the finding naming that setting; now looked for by name, not as the first finding, so another finding no longer hides it |

The clean proof: `census findings: []` and all 35 pin controls `[ok]` (`logs/pin-suite-head.log`, R584-8's `pin_suite.py` unmodified).

My census forms (`round10/scripts/census_forms10.py`, `logs/census-forms.log`), each put at an anchor of a pin-proof module: 28 of 28 named at the planted line: `import subprocess as sp`, `__import__`, `importlib`, `getattr(os, "sys" + "tem")`, `os.popen`, `os.execvp`, `os.posix_spawn`, `os.spawnlp`, `pty.spawn`, `asyncio.create_subprocess_exec`, `from asyncio import create_subprocess_shell as c`, `fw_gtest.run` in `stack_pin`, `shutil.os.system` in `legacy_stack` (outside the decision), `sys.modules[...]`, a generator's `gi_frame.f_globals`, `from os import system`, `eval`, `compile`, a module constant bound to the runner, the helper's name bound again, a new module function or a class's method using `fw_gtest`, a lambda parameter shadowing `run`, the runner as a default argument, `os.environ` changed in `stack_pin`, `from ctrl_pin import run`, `subprocess` in a `ctrl_pin.py` function, a wildcard import. Not seen, as stated: the harness's runner called in `legacy_stack`, and `fw_gtest.run` in `ctrl_pin.mirror`.

### The reviewers' probes

Fetched from `697c-review-evidence` at `3012d4f9`, sha256 equal to their manifests (`proof_mutants.py` `e93fd950…`, `pin_suite.py` `d216e344…`, `census_probe.py` `0cc5e43f…`), run unmodified on disposable clones (CPython 3.12.3 with PyYAML).

| Probe | `feed95bb` (base) | `be607527` (head) |
|---|---|---|
| R585-8 `census_probe.py <checkout> <work>` | `mutant census findings: []`, both replacements accepted by the mutant, `REPRODUCED: the census accepts a bypass that reads replacement objects`, rc 0 | `mutant census findings: ["…ctrl_build.py:260 stack_pin names run, which the pin decision may not reach (…:105 the value of run names fw_gtest.run, …)", "…:260 stack_pin names .__name__, …", …]`; the mutant itself still reads the replacement (it runs Git outside the helper), and the probe stops: `AssertionError: Probe no longer reproduces the census escape`, rc 1 |
| R584-8 `proof_mutants.py … M8 M11` | M8: `census findings: []` (both replacement controls escape); M11: `census findings: []`, rc 0 | M8: `census findings: ["…ctrl_build.py:260 stack_pin names run, …"]`; M11: `census findings: ["…ctrl_build.py:210 stack_gitlink names run, …"]`; each rc 1 |
| R584-8 `proof_mutants.py`, all twelve | — | M1: the replacement controls escape and the census names the environment; M2: the census names it; M3, M4, M5b, M6, M7: their own control escapes; M5: passes every control, as R584-8 reported (caught by type); M8 to M11: the census names the planted line. M5b's `path.stat()` and M6's `.items` are also outside the vocabulary, so the census names them too. Under M8, M10 (`TREE_READ` gone) and M9, M11, a census control whose anchor the mutant replaced reports `the census control's anchor occurs 0 times in ctrl_build.py` |
| R584-7 `pin_replace_probe.sh` step 3, R585-7 `pin_probe.py` (round 9's) | (round 9: ACCEPTED / ESCAPED at `4cab445a`) | `REFUSED` / `replacement control: REFUSED … include/adp.h`, restored clone accepted |

Logs: `logs/probe-r585-8-base.log`, `logs/probe-r585-8-head.log`, `logs/r584-mutants-base/`, `logs/r584-mutants-head/`, `logs/probe-r584-7-head.txt`, `logs/probe-r585-7-head.txt`.

Every entry point (round 9's `entrypoints.py`, `logs/entrypoints.log`): 17 entry points under each of five disguises of `include/adp.h` (or a mode change), 85 of 85 refused by the changed file's name, exit 2, at `be607527` (and at `65115fce`); the clone clean afterwards.

### Gates at the round-10 head

Local figures: the CI-parity container (Ubuntu 24.04.5, CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each (disjoint sets of the service's 64-79, the three jobs at once), fresh clones at `be607527`; the docs job, the probes and the images on the host with CPython 3.12.3 (PyYAML, the locked renderer) and the pinned SDK.

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | container, CPUs 64-67, fresh clone at `be607527` | PASS, 728 s (40 % of 30 minutes; round 9's was 677 s alone, this ran beside two other containers and the host jobs): `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) ..., every Makefile builder's pin prerequisites and the pin proof's census; 0 finding(s), 105 boundary, 35 pin and 4 figure controls, 0 misbehaved` (`logs/bjob-final.log`) |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | container with the pinned Verilator 5.050 and the RV32 SDK, CPUs 72-75, `VERILATOR_JOBS=2`, fresh clone at `be607527` | PASS, 498 s (21 % of 40 minutes): `816 compiled sources of 916 recorded invocations (386, 94, 336) ...; 0 finding(s), 6 boundary, 35 pin and 4 figure controls, 0 misbehaved` (`logs/vjob-final.log`) |
| `firmware-unit`'s steps (`unitjob.sh`: tally self-test, RV32 self-test, the control gate with `--self-test`, the store's gate, the coverage self-test and check) | container, CPUs 68-71, fresh clone at `be607527` | every step rc 0, 2215 s (82 % of 45 minutes, beside the boundary and Verilator replicas; `logs/ujob-final.outer`): the firmware gate's 845 verdict lines byte-identical to rounds 4 to 9 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `logs/fw-verdicts-head.txt`: 843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`, after `tsn-c-stack at 1a9f651c...`); the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `fw_coverage.py --check` PASS (30 files), its table row for row round 9's (`logs/cov-head.txt`). The gate's log is 318,873 bytes, sha256 `c5ab939610bf9066af0ad1e314c5b44e0d17a29ad1668fbf9fe30c2e8a560b48`, not copied |
| the docs job's 54 commands (`docsjob.sh`) | host, fresh clone at `be607527` | 54 of 54 rc 0 (`logs/docsjob-final.txt`): `ci_events.py --check` OK (1902 items), `--selftest` PASS (2610 arms); `ci_scope.py --selftest` PASS; `check_py_idiom.py` every ratchet held; `check_em_dash.py --base feed95bb` 0 findings over 19 added lines in 1 page; `docs_check.py` 0 findings across 202 pages; `measure_fail_fast.py --selftest` 106 of 106 |
| images (`images6.sh`) | host, pinned SDK, round 1's runtime archives, fresh clone at `be607527` (and at `65115fce`) | 35 of 35 ELF files relinked; the manifest byte-identical to rounds 6 to 9 and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `round10/images-head.sha256`); every hash of the round-1 table holds |
| R584-8's `pin_suite.py` (the CLI pin, the census, the 35 pin controls, the figures and their 4 controls, no builds) | host, clones at `feed95bb` and `be607527` | head: `census findings: []`, `pin controls 35, misbehaved 0; figure controls 4, misbehaved 0`, 3 s; `feed95bb`: 30 and 0. Every non-census pin control's verdict line is the same at both (`logs/pin-suite-*.log`) |
| the reviewers' probes, my census forms, every entry point | as above | as tabled above: R585-8 and R584-8 M8/M11 name the planted line; 28 of 28 forms; 85 of 85 entry points |
| `act_ci.py --selftest` | not run: this round changes no workflow, `act_ci.py` or `ci_events.py`; round 8's run at `4cab445a` stands for those files |

Memory: the service stayed under 1.5 GB with the three containers, the docs job and the images running together.

### Open risks and questions (round 10)

1. "Only the helper may start a process" is held as a reference rule module-wide and as a vocabulary where the pin is decided, not by moving `ctrl_build.py`'s build functions and `ctrl_pin.py`'s tool runs out of the two modules (above). A Git process those start through `fw_gtest.run` outside the decision is not refused; it cannot change what the decision reads. If the manager wants the literal reading, the move is a separate change to the boundary gate's builder model.
2. The vocabulary is fixed: a change to the decision that uses a new name (a builtin, a module function, an attribute) fails the census until the name is added to `VOCABULARY`, `BUILTINS` or `ATTRIBUTES` with the census's review. M5b and M6 show it naming such changes.
3. The helper and its environment (`git_env`, `NO_GRAFTS`) are held by the module-wide rule, the environment check and the replacement controls, not by the vocabulary.
4. The census reads the modules as written; code elsewhere that rebinds their names at run time, or a route of Python's own to an object that none of the refused names opens, is not seen.
5. R584-8's F1 asked, alternatively, that the census name a dashed Git string; the round-10 ruling holds the route instead, so a dashed string that is never launched is not a finding, and one launched outside the helper is refused for its route.
6. S1 (verify the object store), S2 (`GIT_NO_REPLACE_OBJECTS` in `ctrl_image.py --base` and `aecp_wire.py`), S3 (count needle-bearing Verilator plants) are optional and not taken. RES-1 and R585-8-RS1 go to #495; RS1's wording is applied in `PR-BODY.md`.
7. `firmware-unit` stays over 60 % of its 45 minutes, its suites alone; ruled #716's scope.

## Round 11

Assignment: #697 comment [6113306444](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113306444), answering R584-9 ([6113294765](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6113294765)) and R585-9 ([6113301631](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6113301631)), both NEGATIVE at `be607527`, one MINOR each:
- the static census did not see rebinding by attribute assignment (R584-9-F1: E2b, E6, E7);
- it did not see dynamic code reached through qualified attributes or written inside the helper (R585-9-F1: 13 escapes in a 66-case matrix).

The ruling moves the guarantee to run time. Before the proof's first Git call it installs a PEP 578 audit hook that refuses every launch but the helper's Git and all dynamic code. The census stays as a fast lint. Each standing control runs the proof with one bypass injected and must end in the named runtime refusal. The three probes must end in it too.
Base of the round: `be607527eaac84cfc8d7456167b070a22228345b`. New commits only, no rebase or amend; not pushed.
Head: `aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783`.
Status: REVIEW READY, comment [6114209149](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114209149) (its text: `round11/review-ready-round11.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `d32ceac87` | Refuse at run time, by an audit hook installed beside the helper, every process or thread start but the helper's Git and all dynamic code while the pin proof runs, and run each bypass control as the proof under that hook | pyflakes; `check_py_idiom.py` (every ratchet held); `docs_check.py`; the clean proof and 24 hook controls on CPython 3.12.3 and 3.14.7; R585-9's matrix (82 of 82) and dynamic probe (refused); R584-9's rebinding probe (E1b, E2b, E6 and E7 refused, the clean copy 0 runner starts); R584-8's `pin_suite.py` (52 pin controls, 0 misbehaved; figures). The three replicas started here were stopped when the self-review below found two gaps |
| `aca5e8afc` | Know the pin proof's code by its files as well as its namespaces, give each rule of the audit hook a control that only it refuses, and state that CPython before 3.14 audits a subprocess start only from Python | found on self-review (below): the hook had recognised `ctrl_pin.py`'s code only through its `sys.audit(PROOF_EVENT)` registration, which a plant rebinding `sys.audit` first skips; and three of the hook's rules had no control that only they refuse. Pyflakes, idiom gate, `docs_check.py`; the hook-rule campaign (17 of 17 caught on both interpreters); 58 pin controls, 0 misbehaved; then every replica and probe again at this head (below) |

One-line subjects, no body, no trailers, configured identity. `git diff --stat be607527 HEAD`: 4 files (`sw/firmware/ctrl/README.md`, `ctrl_boundary.py` docstring, `ctrl_build.py`, `ctrl_pin.py`), 443 insertions, 116 deletions. No firmware source or header, image builder, mutation table, coverage row, Makefile, workflow, build flag or tsn-c-stack pin changes; the linked images are byte-identical (below).

### The hook

| What | Where (at the head) |
|---|---|
| The Git program: `shutil.which("git")` when `ctrl_build.py` is loaded. The helper now starts it by that path (`executable=GIT`, argv unchanged), so the hook can hold the helper to it | `sw/firmware/ctrl/test/ctrl_build.py:201` `GIT`, `:334` |
| What decides the pin: `stack_gitlink`, `stack_pin`, `main` (the lint's `ROOTS` is now this tuple) | `ctrl_build.py:203` `DECISION`; `ctrl_pin.py:150` |
| Every launch event CPython raises on any platform (`subprocess.Popen`, `os.system`, `os.exec`, `os.posix_spawn`, `os.spawn`, `os.fork`, `os.forkpty`, `os.startfile`, `pty.spawn`, `webbrowser.open`, `_posixsubprocess.fork_exec`, `_winapi.CreateProcess`), and the two thread-start events, since a thread could change a start's arguments after the hook read them | `ctrl_build.py:209` `LAUNCH_EVENTS` |
| Dynamic code (`exec`, `compile`) and the reaches into the hook's own state (`gc.get_objects`, `gc.get_referrers`, `gc.get_referents`, `sys.settrace`, `sys.setprofile`) | `ctrl_build.py:215` `DYNAMIC_EVENTS` |
| A function's code or defaults replaced | `ctrl_build.py:218` `RUNS` |
| The installer: a decorator on the helper (`@audited def git`), so the hook is installed when the helper is defined, before any Git call, and holds the helper's own code object. It binds every name it uses as closure variables when installed, builtins included (`type`, `str`, `bytes`, `dict`, `tuple`, `list`, `OSError`, `ValueError`, `sys._getframe`, `sys._current_frames`, `os.write`, `os.stat`, `stat.S_ISDIR`, `os.fsdecode`), so rebinding a name in `ctrl_build`'s namespace (even a builtin's name there) or anywhere else does not change it | `ctrl_build.py:228` `audited`, `:328` `@audited` |
| The proof's code (`ours`): a frame whose code is from `ctrl_build.py` or `ctrl_pin.py` (the paths fixed at install), or whose namespace is `ctrl_build`'s or registered by `sys.audit(PROOF_EVENT)` (which `ctrl_pin.py` raises after its imports, so a copy of it under another name is held too) | `ctrl_build.py:239` `files`, `:247` `ours`; `ctrl_pin.py:141` |
| The proof running (`running`): in any thread (`sys._current_frames`), a frame of a `DECISION` function of `ctrl_build`'s namespace; for launches, also a proof module's top level | `ctrl_build.py:256` |
| A launch while the proof runs is refused unless all of these hold: the subprocess module started it (its frames skipped) for the helper's own code object; the event is `subprocess.Popen`, `os.posix_spawn` or `_posixsubprocess.fork_exec`; the program is `GIT` exactly, as a `str` (or a tuple of bytes all `GIT`); and the environment is a plain `dict` with `GIT_NO_REPLACE_OBJECTS=1` and an absolute `GIT_GRAFT_FILE` whose parent is an existing non-directory | `ctrl_build.py:276` `unlike` |
| `exec`, `compile`, the gc and trace events, and an `import` of `importlib` or `importlib.*` are refused when the issuing frame is the proof's code (the helper's included), or while a `DECISION` function runs, whoever issues them (an import's own code, a library's `eval`) | `ctrl_build.py:306` `hook` |
| At any time, setting `__code__`, `__defaults__` or `__kwdefaults__` on a function of the proof is refused | `ctrl_build.py:306` |
| Each refusal: the proof's innermost line on the stack (its path from the checkout), and what was asked. It is written to the standard error with the prefix `HOOK_REFUSED` before an `AuditRefusal` (a `Refusal`, so every gate exits 2) is raised, so a refusal caught and ignored is still read | `ctrl_build.py:221`, `:224`, `:266` `refuse` |
| `audited` is 98 lines, under the idiom gate's 100 | `check_py_idiom.py` held every ratchet |

What the clean decision raises, traced on both interpreters: 5 `subprocess.Popen` events (and on 3.14 the matching `os.posix_spawn`, since the helper gives an absolute executable), plus `open`, `os.scandir` and `os.walk`. It raises no `exec`, `compile`, `import` or thread event, so refusing them while it runs costs nothing.

### The census, the run under the hook, and the stated limit

- The census (`ctrl_pin.py:489`) is the lint plus `exercised` (`:470`), the proof run under the hook:
  - It runs `PROOF_RUN` (`:204`) in a fresh `python -I -B` interpreter.
  - Each given module's text is compiled under its own path in the checkout: `ctrl_build.py` first, which installs the hook, then `ctrl_pin.py`. Then the command line's pin check runs.
  - The run's environment holds neither of the helper's two settings.
  - The findings are the hook's standard-error lines, or how the run ended if it did not reach the verdict.
- The lint keeps round 10's rules, with two changes:
  - Dynamic code is refused anywhere, the helper included, by name, by import, or as an attribute of any object. So `inspect.builtins.exec` and `pkgutil.importlib` are named, but `re.compile` is not.
  - Reflection is refused everywhere but the installer.
- The lint reads the modules as written, so the docs attribute the guarantee to the hook.
- The limit, stated in the README (`sw/firmware/ctrl/README.md:182-187`), the docstring (THE HOOK, `ctrl_pin.py:11`) and the PR body:
  - The guarantee covers launches through the interpreter's audited interfaces. Native code is the remaining limit: `ctypes` and extension modules.
  - Before CPython 3.14 that includes `_posixsubprocess.fork_exec`, which `subprocess` and `multiprocessing` call. `subprocess` raises its own event from Python just before that call.
  - So on the runner's CPython 3.12.3, code that skips that call starts a process the hook never sees: code that calls `fork_exec` itself, or that rebinds `sys.audit`.
  - CPython 3.14 raises an event in `fork_exec` itself.
  - Also outside the hook: what Git itself starts, and code that runs before the hook is installed (the top of `ctrl_build.py`).
  - Functions of the two modules that start processes while the proof is not running (the build functions, `run`, `ctrl_pin`'s tool runs) are not judged.
- `scripts/limit_probe.py` (round 11) shows the limit. A Git command by the harness's runner where the pin is decided:
  - is refused on 3.12.3 and on 3.14.7 alone;
  - with `ctrl_pin.py` first rebinding `sys.audit`, gives `[]` on 3.12.3;
  - on 3.14.7 is refused as `_posixsubprocess.fork_exec` (`logs/head/limit-probe.log`).

### Self-review after `d32ceac8`

1. **A rebinding that skipped `ctrl_pin.py`'s registration.**
   - At `d32ceac8` the hook knew `ctrl_pin.py`'s code only through its `sys.audit(PROOF_EVENT)` call. A plant that rebinds `sys.audit` before that line leaves the module's top-level launches and dynamic code unjudged.
   - `aca5e8af` also knows the proof's code by its files, which are fixed at install.
   - The new control plants exactly that (`sys.audit` rebound, then `exec`). It escapes with the file rule removed.
2. **Rules no control isolated**, found by deleting each rule of the hook in turn (`scripts/hook_mutants.py`).
   - At `d32ceac8` three rules were not isolated: the helper-code check, an import of `importlib`, and the standard-error record of a refusal. A fourth, dynamic code a library runs while deciding, was isolated by none either.
   - Six controls were added; `pin_controls` gained none apart from these.
   - At the head every one of the 17 rules is caught on both interpreters: removing it makes at least one control escape (`logs/head/hook-mutants-3.12.3.log`, `-3.14.7.log`).
3. **The `sys.audit` route on 3.12.3** (the limit above). Guarding `sys.audit` alone (a module subclass with a read-only property) was tried and works, but it would not close the route. On 3.12, Python code can reach `_posixsubprocess.fork_exec` directly, or through a replaced `subprocess` function, which is the extension-module limit the ruling states. So the round states the limit precisely instead.

### Standing controls (30 under the hook, and the clean proof)

`HOOK_PLANTS` (`ctrl_pin.py:243`), run by `census_arms` (`:830`) through `planted` (`:810`); the clean proof is `unplanted` (`:803`), a pin control of its own (`:894`, outside `census_arms`, since R585-9's matrix treats every `census_arms` arm as a refusal). Pin controls 35 -> 58 (15 direct, 1 clean, 30 hook, 5 tools, 7 bench); the README's figure with them (checked by the figure check). A control is ok when a refusal of the hook holds its words at a line of its plant (the five marked * name no plant line: the refusal is at the helper's line, or at the line of the name the plant gave its code).

| Control | Refusal at the head (3.12.3; 3.14.7 the same) |
|---|---|
| a Git command run by the harness's runner (round 9's) | `ctrl_build.py:388 starts git (subprocess.Popen) while the pin proof runs, not by the helper` |
| a computed name (`git.__name__`, R585-8's mutant) | `ctrl_build.py:392 starts git (subprocess.Popen) ...` |
| a dashed program (`git-ls-tree`, R584-8's) | `ctrl_build.py:392 starts git-ls-tree (subprocess.Popen) ...` |
| the Git program by its path, with the helper's environment, by the harness's runner (isolates the helper-code rule) | `ctrl_build.py:392 starts /usr/bin/git (subprocess.Popen) ...` |
| a refusal caught and ignored (`try`/`except BaseException`; isolates the standard-error record) | `ctrl_build.py:393 starts git (subprocess.Popen) ...` |
| an aliased import (`from subprocess import run as r`) | `ctrl_build.py:393 starts git (subprocess.Popen) ...` |
| `os.system`, a line added to `ctrl_pin.py` | `ctrl_pin.py:920 starts git ls-files (os.system) ...` |
| `exec` of a string | `ctrl_build.py:342 asks for compile in the pin proof: dynamic code, or a reach into the audit hook's own state` |
| the helper's name rebound by attribute assignment in `ctrl_build.py` (E2b's shape) | `ctrl_build.py:344 starts git (subprocess.Popen) ...` |
| the same in `ctrl_pin.py` (E6's shape) | `ctrl_pin.py:925 starts git (subprocess.Popen) ...` |
| `os.walk` rebound to start Git (E7's shape) | `ctrl_build.py:344 starts git (subprocess.Popen) ...` |
| `inspect.builtins.exec`, lines added to `ctrl_pin.py` (R585-9's probe's form) | `ctrl_pin.py:921 asks for compile ...` |
| `inspect.builtins.eval`, in `stack_gitlink` | `ctrl_build.py:343 asks for compile ...` |
| `inspect.builtins.compile`, in `stack_pin` | `ctrl_build.py:393 asks for compile ...` |
| dynamic code a library runs where the pin is decided (`collections.namedtuple`; isolates the deciding rule) | `ctrl_build.py:343 asks for compile ...` |
| `ctrl_pin.py`'s code filed under another name (`code.replace`, then `exec`; isolates the namespace registration) * | `<elsewhere>:922 asks for compile ...` |
| an import of `importlib.metadata`, a line added to `ctrl_pin.py` (isolates the importlib rule) | `ctrl_pin.py:920 asks for an import of importlib.metadata in the pin proof ...` |
| `pkgutil.importlib.import_module("subprocess").run([...])`, in `stack_pin` | `ctrl_build.py:392 asks for exec in the pin proof ...` (the import of `pkgutil` while deciding; were it already loaded, the launch would be refused at the next line) |
| `exec`, `eval`, `compile` inside the helper (three controls) | `ctrl_build.py:333 asks for compile ...` |
| `ctrl_pin.py`'s code kept from the hook by rebinding `sys.audit` first, then `exec` (isolates the file rule) | `ctrl_pin.py:144 asks for compile ...` |
| a thread started, lines added to `ctrl_pin.py` | `ctrl_pin.py:921 starts <bound method Thread._bootstrap ...> (_thread.start_new_thread) ...` |
| the decision's code replaced (`stack_pin.__code__`) | `ctrl_pin.py:920 replaces __code__ of stack_pin, a function of the pin proof` |
| the collector's list of objects (`gc.get_objects`) | `ctrl_pin.py:921 asks for gc.get_objects ...` |
| a trace function (`sys.settrace`) | `ctrl_pin.py:920 asks for sys.settrace ...` |
| the Git program rebound by attribute assignment (`ctrl_build.GIT`) * | `ctrl_build.py:334 has the helper start /usr/bin/true (subprocess.Popen), not the Git program PATH names, /usr/bin/git` |
| the helper's environment without `GIT_NO_REPLACE_OBJECTS` * | `ctrl_build.py:334 has the helper start Git (subprocess.Popen) without GIT_NO_REPLACE_OBJECTS=1, so Git would read a replacement object` |
| the helper's environment without `GIT_GRAFT_FILE` * | `... with GIT_GRAFT_FILE None, a path that can exist, so Git would read a graft file` |
| `git_env` rebound, and `type`, `dict`, `isinstance`, `any` rebound in `ctrl_build`'s namespace * | `... without GIT_NO_REPLACE_OBJECTS=1 ...` |

The hook-rule campaign (`scripts/hook_mutants.py`, `logs/head/hook-mutants-*.log`): each of 17 rules deleted in turn in a disposable clone, the 30 controls and the clean proof run; CAUGHT 17 of 17 on CPython 3.12.3 and on 3.14.7, the clean proof passing in every one. The isolating control of each: H1 the helper-code check, the Git program by its path; H2 the program, the Git program rebound; H3 `GIT_NO_REPLACE_OBJECTS`, its two controls; H4 the graft file, its control; H5 the decision as a scope, 15; H6 a proof module's top level as a scope, `os.system` and the thread; H7 the proof's own dynamic code, 6; H8 dynamic code while deciding, `collections.namedtuple`; H9 an import of importlib, `importlib.metadata`; H10 `__code__`, its control; H11 threads; H12 gc; H13 `sys.settrace`; H14 the proof's files, the `sys.audit` rebinding; H15 the standard-error record, 25; H16 no hook, 30; H17 the registration, the `code.replace` control.

### The reviewers' probes at the head

Fetched from `697c-review-evidence` at `ad626670`, run unmodified on disposable clones at `aca5e8af` (CPython 3.12.3). Their scripts' sha256 match their manifests (only `prior-r585.log`, a log, differs from R585-9's manifest).

| Probe | `be607527` (as the reviews report) | `aca5e8af` |
|---|---|---|
| R585-9 `census_matrix.py` | 66 cases, 13 escaped, rc 1 | `RESULT: 88 cases, 88 passed, 0 escaped`, rc 0 (its 66 forms plus the 30 hook controls; my classification, `scripts/classify_matrix.py`: 59 refused by the hook at run time, 28 by the lint alone, 1 clean). The 28 lint-only cases only name or import a facility, which raises no event, or reach a module already loaded (`import importlib`, `__import__('os')`, `pkgutil.importlib` with no launch), which raises none either. Of R585-9's 13 escapes, 9 are refused by the hook (qualified `eval`/`exec`/`compile` in both modules, and `eval`/`exec`/`compile` in the helper) and 4 by the lint (`pkgutil.importlib` in both modules, `__import__` and `import importlib` in the helper) |
| R585-9 `dynamic_launch_probe.py` | the child ran, `REPRODUCED`, rc 1 | the census names `ctrl_pin.py:922` (the lint twice, and the hook's run); the planted copy, run as a script with the real `ctrl_build`, prints `the pin proof's audit hook refused: .../ctrl_pin_probe.py:922 asks for compile in the pin proof ...` and exits 1, so the probe's `assert result.returncode == 0 and 'OUTSIDE_HELPER_PROCESS_RAN' in result.stdout` fails: `AssertionError`, rc 1; the child never ran |
| R584-9 `make_rebind_mutants.py` + `rebind_runtime_probe.py`, E1b, E2b, E6, E7 | census `[]`, 5 runner starts in `stack_pin()` | each: `census findings: ['<file>:<n> starts git (subprocess.Popen) while the pin proof runs, not by the helper']` at the adapter's line (E1b `ctrl_build.py:347`, E2b `ctrl_build.py:343`, E6 `ctrl_pin.py:929`, E7 `ctrl_build.py:344`), then `stack_pin()` raises `ctrl_build.AuditRefusal` naming the same line, rc 1. The clean copy: `census findings: []`, `runner starts during stack_pin: 0`, rc 0 |
| R584-9 `census_escape_probe.py` | — | the 30 standing controls `[refused]`; E1, E2, E6 named by the hook's run; E3 to E5 (`_posixsubprocess`, `multiprocessing`, a C library's `system`, each only named, none started) `[]`, the stated limit |
| R584-9 `module_wide_forms.py` | 46 as expected | 46 as expected |
| R584-9 `helper_value_only_probe.py` | `IndexError` (S1) | `IndexError` (S1, optional, not taken) |
| R585-8 `census_probe.py` | (round 10: stopped, `Probe no longer reproduces`) | the census names `ctrl_build.py:392`; the probe's mutant module installs its own hook and its run is refused (`review_pin_mutant.AuditRefusal: ...:392 starts git ...`), rc 1 |
| R584-8 `proof_mutants.py`, all twelve, each alone with the bytecode cache cleared | (round 10 table) | M1, M2: `stack_pin()` refused by the hook for the setting; M8, M9, M10, M11: refused at their own lines (`:392`, `:388`, `:392`, `:342`); M3, M4, M5b, M6, M7: their own control escapes, as before; M5: passes every control, as R584-8 reported. Run together, the probe's in-place edits of equal size within one second reuse a stale `.pyc` (its `pin_suite.py` runs `-I` without `-B`), so M9 and M11 then report M8's line; run alone they do not |

Every entry point (round 9's `entrypoints.py`): 17 entry points under five disguises, 85 of 85 refused by the changed file's name, the clone clean afterwards (`logs/head/entrypoints.log`). Make's database and dry-run reading of every Makefile builder byte-identical to `be607527`'s (sha256 `4d681718…`, as rounds 9 and 10). Every non-hook pin control's verdict line identical to `be607527`'s.

### Gates at the round-11 head

Local figures: the CI-parity container (Ubuntu 24.04.5, its CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each (disjoint sets of the service's 64-79, the three jobs at once), fresh clones at `aca5e8af`; the docs job, the probes and the images on the host with CPython 3.12.3 (PyYAML, the locked renderer) and the pinned SDK. The replicas started at `d32ceac8` were stopped (self-review, above) and rerun here.

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | container, CPUs 64-67 | PASS, 671 s (37 % of 30 minutes, beside the two other containers and the host jobs): `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) ..., every Makefile builder's pin prerequisites and the pin proof's census; 0 finding(s), 105 boundary, 58 pin and 4 figure controls, 0 misbehaved`; 58 pin control lines `[ok]`, the 30 hook controls among them (`round11/logs/bjob-final.log`) |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | container with the pinned Verilator 5.050 and the RV32 SDK, CPUs 72-75, `VERILATOR_JOBS=2` | PASS, 481 s (20 % of 40 minutes): `816 compiled sources of 916 recorded invocations (386, 94, 336) ...; 0 finding(s), 6 boundary, 58 pin and 4 figure controls, 0 misbehaved` (`round11/logs/vjob-final.log`) |
| `firmware-unit`'s steps (`unitjob.sh`: tally self-test, RV32 self-test, the control gate with `--self-test`, the store's gate, the coverage self-test and check) | container, CPUs 68-71 | every step rc 0, 1974 s (73 % of 45 minutes, beside the boundary and Verilator replicas; `round11/logs/ujob-final.outer`): the firmware gate's 845 verdict lines byte-identical to rounds 4 to 10 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `round11/logs/fw-verdicts-head.txt`: 843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`, after `tsn-c-stack at 1a9f651c...`), so the gate's process, which installs the hook when it imports `ctrl_build`, builds and runs exactly as before; the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `fw_coverage.py --check` PASS (30 files), its table row for row round 10's (`round11/logs/cov-head.txt`). The gate's log is 318,873 bytes, sha256 `3571f715d200e52d0bf4ff146b1490f7819052c63143d29e951742386fb392f4`, not copied |
| the docs job's 54 commands (`docsjob.sh`) | host, fresh clone at `aca5e8af` | 54 of 54 rc 0: `ci_events.py --check` OK (1902 items), `--selftest` PASS (2610 arms); `ci_scope.py --selftest` PASS; `check_py_idiom.py` every ratchet held (`long function: 9 <= 9`, `long module: 10 <= 10`, `over-long line: 0 <= 0`); `check_em_dash.py --base be607527` 0 findings over 36 added lines in 1 page; `docs_check.py` 0 findings across 202 pages; `check_submodule_docs.py` OK (6 gitlinks); `measure_fail_fast.py --selftest` 106 of 106 |
| images (`images6.sh`) | host, pinned SDK, round 1's runtime archives, fresh clone at `aca5e8af` (and at `d32ceac8`) | 35 of 35 ELF files relinked; the manifest byte-identical to rounds 6 to 10 and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `round11/images-head.sha256`); every hash of the round-1 table holds |
| R584-8's `pin_suite.py` (the CLI pin, the census, every pin control, the figures and their 4 controls) | host, clones at `be607527` and `aca5e8af` | head: `census findings: []`, `pin controls 58, misbehaved 0; figure controls 4, misbehaved 0`; `be607527`: 35 and 0. Every non-hook pin control's verdict line identical at both (`round11/logs/pin-suite-be607527.log`, `round11/logs/head/pin-suite.log`) |
| the hook-rule campaign (`scripts/hook_mutants.py`) | host, CPython 3.12.3 and 3.14.7 | CAUGHT 17 of 17 on each |
| the reviewers' probes, every entry point, make's readings | host | as tabled above: 88 of 88; the dynamic probe and E1b/E2b/E6/E7 refused by the hook; 85 of 85; readings byte-identical |
| `act_ci.py --selftest` | not run: no workflow, `act_ci.py` or `ci_events.py` changes this round; round 8's run at `4cab445a` stands |

Memory: the service stayed under 7 GB with the three containers, the docs job and the images running together.

### Open risks and questions (round 11)

1. The `sys.audit` route on the runner's CPython 3.12.3 (above). The ruling's limit covers it ("native code ... extension modules"). Closing it in the interpreter would need the hosted job's Python at 3.14, a CI change outside this lane.
2. The hook judges the decision `ctrl_build.py` defines. A gate that calls another function bound in `stack_pin`'s name is not the decision. Replacing the decision's code is refused, but rebinding the module attribute is not. Every gate imports `stack_pin` by name when it is loaded.
3. The helper's environment is the caller's plus the two settings. A Git variable the caller's environment sets (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_CONFIG_*`) reaches Git. This is pre-existing (round 9), outside this round's assignment, and not raised by a review; it is noted for the manager to file if wanted.
4. The lint names `import importlib`, `__import__` and `pkgutil.importlib` on their own, but at run time they raise no event once the module is loaded. Anything they reach that starts a process or runs dynamic code in the proof is refused.
5. R584-9-S1 (the lint's `IndexError` when the helper is bound only by assignment) and S2 (more facilities in the lint's list) are optional and not taken. R584-8-RES-1, R585-8-RS1 and R584-7-RES1 / R585-7-RS1 go to #495; R585-9's RES-1 wording is retained for #495 too.
6. `firmware-unit` stays over 60 % of its 45 minutes on its suites alone; that is #716's scope.

## Round 12

Assignment: #697 comment [6114400461](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461), answering R584-10 ([6114394332](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6114394332)), NEGATIVE at `aca5e8af`. It has three items:
1. merge dev `09c7231e`;
2. the scope ruling (the threat model);
3. Git's environment built from an allowlist, with standing controls.

The assignment's STOP condition: "STOP if the dev merge cannot keep both sides' CI guarantees, or if any image changes a byte."
Base of the round: `aca5e8afc58a12ca050cd4c4c5f1c7c02c9ff783`. New commits only, no rebase or amend; not pushed.
Head: `adb936049165dc82e8832e79329984108eb1480f` (three commits on `aca5e8af`, no merge commit).
Status: STOP on item 1 (below); items 2 and 3 done and validated at the head. Posted as #697 comment [6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316) (its text: `round12/stop-round12.md`).

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `6b03a8870` | Start the pin proof's Git with an environment of its own that inherits nothing, have the audit hook refuse any other or one whose keys and values are not plain strings, and set each variable that would redirect Git in a standing control | pyflakes; `check_py_idiom.py` (every ratchet held); `docs_check.py`; the clean proof, the 34 hook plants and the 17 inherited-environment controls on CPython 3.12.3 and 3.14.7 (52 of 52 each); the environment mutants (below) |
| `a3992e545` | State the pin proof's threat model as the state it reads and the environment it inherits, with its own modules reviewed source outside it, the audit hook defence in depth, and the two routes within it left for a decision | pyflakes, idiom gate, `docs_check.py`, `check_em_dash.py --base aca5e8af` (0 findings over 18 added lines) |
| `adb936049` | Let the helper's environment also hold the builders' names a capture's audit hook adds to every start, which Git does not read, so the firmware builders pass the exact-environment rule under the boundary's capture | found by the `firmware-boundary` and `firmware-verilator` replicas at `a3992e54` (below); the pin check under a capture; the 52 controls on both interpreters; then every gate again at this head |

One-line subjects, no body, no trailers, configured identity. `git diff --stat aca5e8af HEAD`: 6 files, 471 insertions, 64 deletions:
- `sw/firmware/ctrl/README.md`;
- `ctrl_boundary.py` (docstring);
- `ctrl_build.py`;
- `ctrl_configs.py` (`GATE` lists the new module);
- `ctrl_pin.py`;
- `ctrl_pin_env.py` (new).

No firmware source or header, image builder, mutation table, coverage row, Makefile, workflow, build flag or tsn-c-stack pin changes; the linked images are byte-identical (below).

### Item 1: the dev merge (STOP)

The merge cannot keep both sides' guarantees, so it was not committed. The trial merge was made in a scratch clone (`git merge --no-commit --no-ff 09c7231e` on `aca5e8af`).

1. **F-INT changed the core this lane moved.** Dev `09c7231e` holds PR #704 (#665 F-INT PR 1, merged 2026-10-11T21:25Z). Its commits `5a50b2045` and `7c583daac` change ACMP's core and its core tests:
   - `sw/firmware/ctrl/acmp/acmp.c` +41 −4: a new `publish` port, called before every frame an entry sends and first in `finish`;
   - `acmp.h` +30: `struct acmp_ports.publish`, the `published_*` fields of `struct acmp_sink`, and the PUBLISHED BEFORE PROMISED contract;
   - `test/acmp_fake.hpp` +27 −2 and `test/test_acmp.cpp` +163 −2.

   The adapter calls the port (`acmp/acmp_mbx.c` `m->ports.publish = port_publish;`), and dev's `ctrl_mutants.py` gains 11 `pub-acmp-*` plants in `acmp/acmp.c` (for example `"\tpublish(a);\n\trearm(a);"`). The other moved files (ADP, MAAP, `wire.h` and their tests) did not change on dev. The core delta is 19,847 bytes, sha256 `3cfc488176127512f324cf9d35f8ba3a768bfea611ed2500aa1ece24b7ee8a74` (scratch `round12/logs/dev-core-delta.diff`, not copied).
2. **No tsn-c-stack commit has it.** `git -C third_party/tsn-c-stack fetch origin`, then `include/acmp.h` of every remote branch but `dev-linux` (main `98dc9e3`, and the review, import, requirements, privacy, ADP-discard and YAML branches) holds no `publish`. `git log --all -S published_stream` is empty, and tsn-c-stack's PRs (1, 16 to 20) and open Issues (4 to 15) hold none.
3. **The trial merge** stops in 13 conflicts:
   - modify/delete on `acmp/acmp.c`, `acmp/acmp.h`, `test/acmp_fake.hpp` and `test/test_acmp.cpp` (deleted here, modified on dev);
   - content conflicts in `.github/workflows/rtl-fast.yml`, `scripts/ci_events.py`, `docs/testing/CI_WORKFLOWS.md`, `docs/reference/SUBMODULES.md`, the submodule diagram (`.drawio`, `.svg`, `.png`, `PNG_MANIFEST.json`) and `tb/verilator/mbx/Makefile`.
4. **Resolving the four deletions as this lane's**, so the stack's core at `1a9f651c` is built: dev's `acmp/acmp_mbx.c` does not compile. Command: `gcc -std=c11 -fsyntax-only -I third_party/tsn-c-stack/include -I<adapters> acmp_mbx.c`, which gives `acmp_mbx.c:98:17: error: 'struct acmp_ports' has no member named 'publish'`, rc 1. With dev's `acmp.h` in front, the same compile is rc 0.
5. **So no resolution keeps both sides:**
   - **Keep dev's `acmp.c`/`acmp.h` in the tree.** This restores the copies the lane removed (acceptance 2). The boundary gate would refuse a firmware file standing for a stack core, and the stack would no longer be the cores' source.
   - **Keep the stack's core and drop the publish port.** That changes the firmware's behaviour and the images against dev `09c7231e`, and drops F-INT's acceptance and its 11 plants. This is the STOP condition, and the lane's own rule (no firmware behaviour change).
   - **Move the pin.** No tsn-c-stack commit carries the port, and this lane may not push to tsn-c-stack.
6. **What would let the merge proceed** (for the manager): F-INT's ACMP core change (both commits' `acmp.c`/`acmp.h` hunks, its `test_acmp.cpp` and `acmp_fake.hpp` cases) lands in tsn-c-stack by its own PR. Then this lane moves the pin to that commit, with the byte-identical-cores diff against dev's `acmp.c`/`acmp.h` at `09c7231e`, retargets the 11 `pub-acmp-*` plants to `tsn-c-stack/src/acmp.c`, and merges dev. PR #724 (#716) touches the same CI files; whichever merges second resolves, as the assignment says.

Not run, since no merge was made: `ci_events.py --check`/`--selftest` and `act_ci.py --selftest` on a merge, and the firmware suites on a merge. `ci_events.py --check` and `--selftest` ran at this head in the docs job (below).

### Item 2: the threat model

The ruling's model is stated in place of "native code is the remaining limit":
- the README (`sw/firmware/ctrl/README.md:184-189`);
- `ctrl_pin.py`'s docstring (THE THREAT MODEL, `ctrl_pin.py:45`);
- the PR body (Round 12, Known limitations).

The model is the state the proof reads: the checkout's files and modes, Git's object store, refs, configuration and attributes, and the environment the proof inherits. The proof's own modules are reviewed source, outside it, and the hook is defence in depth against such code. The texts still say what the hook does not see:
- `ctypes` and extension modules;
- on CPython 3.12.3, `_posixsubprocess.fork_exec`, which `subprocess` calls just after raising its own event from Python;
- what Git starts;
- code above the helper.

They no longer file the `sys.audit` rebinding under a limit of the ruling. Two routes found this round lie within the model and are stated as open, for a decision (below).

### Item 3: Git's environment

| What | Where (at the head) |
|---|---|
| The allowlist: Git's whole environment is `GIT_ENVIRONMENT`, `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE` under `/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, and nothing inherited (no `PATH`, `HOME`, `LANG`; Git falls back to its own exec path and default `PATH`). `git_env()` returns a copy. This follows `scripts/act_ci.py`'s `git_environment` | `sw/firmware/ctrl/test/ctrl_build.py:187`, `:191` |
| The hook's judge of that environment, made when the hook is installed and binding all it uses (`environment_judge`). The environment must be a plain `dict`, or on 3.14's `fork_exec` a list of `bytes` entries, each key once. Every key and value must be a plain `str`, checked before anything is looked up in it, so a `str` subclass's `__eq__`, `__hash__` or `encode` never runs. Then `GIT_NO_REPLACE_OBJECTS=1` and the graft file, with the round-11 words. Then key for key `GIT_ENVIRONMENT` as it was when the hook was installed, naming the key, never an inherited value | `ctrl_build.py:239`, `:253`, `:262`, `:278`; `audited` makes it at `:303` and calls it at `:351` |
| The capture's variable: `CTRL_CAPTURE_FROM`, which a capture's audit hook (`ctrl_capture.HOOK`, installed first) writes into the environment of every process a builder starts. It is let through by name, as a plain `str`; Git does not read it | `ctrl_build.py:232`, `:278` |
| The proof run in a fresh interpreter on a given stack with variables inherited (`proof_run`; `exercised` uses it; `PROOF_RUN` takes the stack) | `ctrl_pin.py:528`, `:542` |
| Four hook plants: the caller's environment given to Git again (`git_env` rebound); `GIT_DIR` added to `GIT_ENVIRONMENT`; a key that compares equal to `GIT_NO_REPLACE_OBJECTS` (`KEYED`); a value that encodes as `0` (`VALUED`). Each is refused at the helper's line | `ctrl_pin.py:257`, `:275`, `:370-379` |
| The 17 inherited-environment controls (`ctrl_pin_env.py`, wired at `ctrl_pin.py:971`) | `sw/firmware/ctrl/test/ctrl_pin_env.py:191` `INHERITED`, `:225`, `:245` |

The inherited-environment controls. Each sets its variables in the environment of the fresh interpreter that runs the proof on a stack clone. Each control's own state lives beside the clone. A variable is held if the verdict is the clone's own and Git starts no program it names (the recorder writes `ran` beside itself).

| Control | What the variable would do if it reached Git | Verdict at the head (3.12.3 and 3.14.7 the same) | At `aca5e8af`'s environment (H22 below) |
|---|---|---|---|
| `GIT_DIR`: a repository whose HEAD and index gitlink are a commit holding the clone's edit of `src/adp.c` | gitlink, HEAD and tree read from it: the edit accepted | `tsn-c-stack differs from the pinned 1a9f651c: src/adp.c` | ESCAPED: `tsn-c-stack at c017579b…` |
| `GIT_INDEX_FILE`: an index whose gitlink is `pin~1`, the clone checked out there | the gitlink read from it | `tsn-c-stack at 74445d28… is not the pinned 1a9f651c…` | ESCAPED: `tsn-c-stack at 74445d28…` |
| `GIT_WORK_TREE`: another directory | the top level read as it | `differs … src/adp.c` | ESCAPED: `… is not its own checkout` |
| `GIT_COMMON_DIR`: an empty repository's | objects and refs read from it | `differs … src/adp.c` | ESCAPED: `cannot read the pinned tree` |
| `GIT_OBJECT_DIRECTORY`: an empty store | objects read from it | `differs … src/adp.c` | ESCAPED: `cannot read the pinned tree` |
| `GIT_ALTERNATE_OBJECT_DIRECTORIES`: a copy of the clone's objects, its own store emptied | objects read from it | `cannot read the pinned tree 1a9f651c …` | ESCAPED: `tsn-c-stack at 1a9f651c…` |
| `GIT_REPLACE_REF_BASE`: `refs/swap/`, under which the pinned `src/` tree is replaced by one holding the edit | the replacement read | `differs … src/adp.c` | held (also held by `GIT_NO_REPLACE_OBJECTS=1`) |
| `GIT_CONFIG_COUNT`/`KEY_0`/`VALUE_0`: `core.fsmonitor` naming the recorder | Git runs it when it reads the index (`ls-files --stage`) | `differs … src/adp.c`, nothing ran | ESCAPED: `Git ran a program …` |
| `GIT_CONFIG_PARAMETERS`: the same | the same | the same | ESCAPED |
| `GIT_CONFIG_GLOBAL`: a file naming it | the same | the same | ESCAPED |
| `GIT_CONFIG_SYSTEM`: a file naming it | the same | the same | ESCAPED |
| `HOME`: a `.gitconfig` naming it | the same | the same | ESCAPED |
| `XDG_CONFIG_HOME`: a `git/config` naming it | the same | the same | ESCAPED |
| `GIT_CONFIG_COUNT`: a clean filter, `head -c <size>`, its attribute in the clone's `info/attributes` (the assignment's control) | the edit hashed through the filter is the pinned blob (checked in setup with `-c`) | `differs … src/adp.c` | held: the proof hashes the files' bytes itself, never through Git |
| `GIT_ATTR_SOURCE`: a tree whose `.gitattributes` gives `src/adp.c` that filter, the filter in the clone's config | the same (checked with `--attr-source`) | `differs … src/adp.c` | held, likewise |
| every variable above at once, the pinned clone unmodified | | `tsn-c-stack at 1a9f651cdf78…` (the clean proof with them all) | ESCAPED: `Git ran a program …` |
| the hook's judge given `fork_exec`'s entries with `GIT_NO_REPLACE_OBJECTS` twice, the first `0` (the one Git's `getenv` reads) | | `… whose entries are not each a key given once` | |

Four hook plants (34 `HOOK_PLANTS`, was 30), at the head:

| Plant | Refusal |
|---|---|
| the caller's environment given to Git again (`git_env = lambda: {**os.environ, **GIT_ENVIRONMENT}`) | `ctrl_build.py:381 has the helper start Git (subprocess.Popen) with HOSTNAME in its environment, which the pin proof's own does not set` (the first inherited key; its value is never printed) |
| `GIT_DIR` added to `GIT_ENVIRONMENT` after the hook was installed | `… with GIT_DIR in its environment, which the pin proof's own does not set` |
| a key, a `str` subclass equal to every key under `GIT_NO_REPLACE_OBJECTS`'s hash, given to Git as `GIT_NO_REPLACE` (R585-10's crafted key, as the assignment describes it) | `… with an environment whose keys and values are not all plain str, so what Git is given is not what was judged` |
| a value, a `str` subclass `"1"` whose `encode` gives `b"0"` (what `os.fsencode` sends on 3.12) | the same |

A direct probe (`round12/probes/inherit_probe.py`, the command-line pin check with one variable inherited; `round12/logs/inherit-probe.log`):

| Probe | `aca5e8af` | head |
|---|---|---|
| inherited `GIT_INDEX_FILE` | exit 0, `tsn-c-stack at 74445d28…`: ESCAPE | exit 2, `… 74445d28… is not the pinned 1a9f651c…` |
| inherited `GIT_DIR` | exit 0, `tsn-c-stack at 2ac3a9c3…` (an edited commit): ESCAPE | exit 2, `differs from the pinned 1a9f651c: src/adp.c` |

So at `aca5e8af` an inherited `GIT_INDEX_FILE` or `GIT_DIR` made every gate accept a stack that is not the gitlink's. Round 11's open note (b) said so without a probe.

### Self-review after `a3992e54`: the capture

The `firmware-boundary` and `firmware-verilator` replicas at `a3992e54` both stopped within ten seconds, on the first captured builder. The step was `test_ctrl_firmware.py --require-rv32` under the gate's capture, and `make -C tb/verilator/mbx`. The refusal: `ctrl_build.py:375 has the helper start Git (subprocess.Popen) with CTRL_CAPTURE_FROM in its environment, which the pin proof's own does not set`.

The capture's audit hook (`ctrl_capture.HOOK`, round 5) is loaded through `sitecustomize`, before the proof's. It writes the builders' names into the `env` mapping of every start, so the helper's Git under a capture has always been given `CTRL_CAPTURE_FROM`.

`adb93604` lets that one name through, as a plain `str`. Git does not read it. Every other extra key is still refused by name. With `ctrl_capture.py --out <dir> -- python3 ctrl_build.py --stack-pin`, and the same for `make -C tb/verilator/mbx stack-pin`, the result is rc 0 at the head. Removing the exemption (H24) fails the captured pin check.

### The hook-rule campaign

`scripts/hook_mutants.py` (round 11's, extended). Each mutant is applied to a disposable clone at the head. The clean proof, the 34 hook plants, the 17 inherited-environment controls and the pin check under a capture are run. Round 11's H1 to H17 keep their meaning. H3 and H4 now edit the judge, so their anchors moved.

| Mutant | 3.12.3 | 3.14.7 |
|---|---|---|
| H0 none | clean proof passes, 0 escaped | same |
| H1 to H17 (round 11's rules) | CAUGHT each, the same escapes as round 11 (H5 19, H15 25, H16 34 now, with the four new plants) | same |
| H18 keys and values not required plain `str` | CAUGHT: `KEYED`, `VALUED` | same |
| H19 the environment not required exactly the proof's own | CAUGHT: the caller's environment again, `GIT_DIR` added | same |
| H20 `fork_exec`'s entries not required each a key once | CAUGHT: the judge control | same |
| H21 the helper inherits the caller's environment (`aca5e8af`'s `git_env`) | CAUGHT: the clean proof refused (`with SHELL in its environment …`) | same |
| H22 H21 with H19 | CAUGHT: 17 escape. They are the two plants, 13 inherited-environment controls and the combined one, plus two hook controls whose anchor the mutant text duplicates. `GIT_REPLACE_REF_BASE`, the clean filter and `GIT_ATTR_SOURCE` hold, as the table says | same |
| H23 the caller's environment under the proof's settings (`{**os.environ, **GIT_ENVIRONMENT}`), with H19 | CAUGHT: 11. The config files' four (`GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `HOME`, `XDG_CONFIG_HOME`) hold, since the settings override them | same |
| H24 the capture's variable not let through | CAUGHT: the pin check under a capture refused | same |

Logs: `round12/logs/hook-mutants-3.12.3.log`, `-3.14.7.log`. A first campaign, on the code committed as `6b03a888` (H0 to H23, before the capture exemption), gave the same verdicts on both interpreters.

### Two routes within the model, found this round and left for a decision

Both are state the proof reads, so the ruling puts them inside the model. Neither is the inherited environment, so neither is in item 3, and neither is fixed here (AGENTS.md section 4: newly discovered work is published, not silently added). Probe: `round12/probes/model_routes_probe.py`, run against the head (`round12/logs/model-routes-probe.log`).

1. **A forged tree object in the stack's object store.**
   - The probe unpacks a clone's packs. It then overwrites the loose object of the pinned `src/` tree (`34150e38…`) with the bytes of a tree holding an edit of `src/adp.c`, and makes that edit on disk.
   - `stack_pin(clone, pin)` returns `1a9f651c…`: ACCEPTED with `src/adp.c` edited.
   - Git 2.43 and 2.56 read subtrees for `ls-tree -r` without checking their hash. Git does check the commit and the root tree it parses.
   - `git fsck` reports `hash mismatch 34150e38…`.
   - A fix inside the decision: rebuild every tree from the listing (mode, name, id, in order) and check its hash, failing closed. That needs new vocabulary in the census, a control, and docs. R584-8-S1 suggested verifying the store.
2. **A program the repository's own configuration names.**
   - With `core.fsmonitor` set in a scratch checkout's `.git/config`, the pin check exits 0. Git ran the program twice, while the decision read the index (`ls-files --stage` in `stack_gitlink`).
   - The texts already said "what Git itself starts is outside the hook". Under the new model it is configuration the proof reads.
   - `-c core.fsmonitor=false` on the helper's command line closes it, as `act_ci.git_prefix` does.

### Gates at the round-12 head

Local figures:
- **Containers:** the CI-parity container (Ubuntu 24.04.5, its CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each, on disjoint sets of the service's 64-75, the three jobs at once, in fresh clones at `adb93604`.
- **Host:** CPUs 76-79, CPython 3.12.3 (PyYAML, the locked renderer) and 3.14.7, the pinned SDK.

The replicas first started at `a3992e54` were stopped by the self-review above.

| Gate | Where | Result |
|---|---|---|
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the `firmware-boundary` step) | container, CPUs 64-67 | PASS, 655 s (36 % of 30 minutes): `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) …; 0 finding(s), 105 boundary, 79 pin and 4 figure controls, 0 misbehaved`; 79 pin control lines `[ok]`: the 34 hook plants, the 17 inherited-environment controls among them |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the `firmware-verilator` step) | container with the pinned Verilator 5.050 and the RV32 SDK, CPUs 72-75, `VERILATOR_JOBS=2` | PASS, 470 s (20 % of 40 minutes): `816 compiled sources of 916 recorded invocations (386, 94, 336) …; 0 finding(s), 6 boundary, 79 pin and 4 figure controls, 0 misbehaved` |
| `firmware-unit`'s steps (`unitjob.sh`) | container, CPUs 68-71 | every step rc 0, 1952 s (72 % of 45 minutes, beside the boundary and Verilator replicas; `round12/logs/ujob.outer`): the firmware gate's 845 verdict lines byte-identical to rounds 4 to 11 (sha256 `ad30597bedd62700f6947680059d962b0d97a664df4ad59cc7364448b1274ad3`, `round12/logs/fw-verdicts-head.txt`: 843 `[ok]`, `mutants: 471 of 471 caught`, `test_ctrl_firmware: PASS`, after `tsn-c-stack at 1a9f651c...`), so the gate, whose pin check now gives Git only the proof's own environment, builds and runs exactly as before; the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `fw_coverage.py --check` PASS (30 files), its table byte-identical to round 11's (sha256 `f54c317ff33d22106c82b17af5ebb885c98d4708d654fb549348c77910e75cc4`, `round12/logs/cov-head.txt`). The gate's log is 318,873 bytes, sha256 `1df273fc4d9e5c6db84cc66666e6cbcc21ba6d4a26b8487a212e94dd3cf911fa`, not copied |
| the docs job's 54 commands (`docsjob.sh`) | host, fresh clone at `adb93604`, `MAKEFLAGS=w` | 53 of 54 rc 0. `ci_events.py --check` OK, `--selftest` PASS, `ci_scope.py --selftest` PASS, `check_py_idiom.py` every ratchet held, `check_em_dash.py --base aca5e8af` 0 findings over 19 added lines, `docs_check.py` 0 findings across 202 pages, `check_submodule_docs.py` OK. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50 (two default-goal fixtures). It fails identically at `aca5e8af` and at dev `09c7231e` with `MAKEFLAGS=w` (host make 4.4.1 and make 4.3 alike), and passes 50 of 50 at the head without `MAKEFLAGS`. It is pre-existing and unrelated: no file it reads changed. Round 11's docs job ran without `MAKEFLAGS` |
| images (`images6.sh`) | host, pinned SDK, round 1's runtime archives, fresh clone at `adb93604` | 35 of 35 ELF files relinked; the manifest byte-identical to rounds 6 to 11 and to dev `aef7ac66`'s (sha256 `de8ae063d8046a72b90cf180b5d1dcf129c43400cd7f139a2ea26a897c86ebd0`, `round12/images-head.sha256`); every hash of the round-1 table holds |
| the 52 hook and inherited-environment controls and the clean proof (`pin_subset.py`) | host, CPython 3.12.3 and 3.14.7 | 52 of 52 on each, 0 misbehaved |
| the hook-rule campaign | host, CPython 3.12.3 and 3.14.7, CPUs 76-79 | 24 of 24 CAUGHT on each, H0 clean |
| every entry point (round 9's `entrypoints.py`) | host, fresh clone at `adb93604` | 17 entry points × 5 disguises, 0 not refused; the clone clean afterwards |
| the inherited-environment probe | host, clones at `aca5e8af` and `adb93604` | as tabled above |
| `act_ci.py --selftest` | not run: no workflow, `act_ci.py` or `ci_events.py` change this round, and no merge; round 8's run at `4cab445a` stands |

Memory: the service stayed under 1.4 GB (`MemoryPeak` 1,334,882,304 bytes, the containers outside its cgroup), the host 48 GB available.

### Open risks and questions (round 12)

1. **STOP, item 1.** The dev merge needs F-INT's ACMP core change in tsn-c-stack first (above). A ruling is needed on how: a tsn-c-stack PR, then a pin move here.
2. **Two in-model routes**, found this round: the forged tree object and the repository's own `core.fsmonitor` (above). Each needs a ruling, in this lane or its own Issue.
3. **`MAKEFLAGS=w` and `check_rtl_source_lists.py --selftest`:** 48 of 50 at dev `09c7231e`, `aca5e8af` and the head alike. If the hosted docs job runs with `MAKEFLAGS=w`, it fails on dev too. This is outside this lane.
4. **Optional or carried items:**
   - R584-9-S1 (the lint's `IndexError`) stays optional and not taken.
   - R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's retained RES-1 wording go to #495.
   - `firmware-unit` stays over 60 % of its 45 minutes, which is #716's scope.

## Round 13

Assignment: #697 comment [6116488747](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6116488747), the way on from the round-12 STOP. Five items:
1. move the pin of `third_party/tsn-c-stack` to `405dc683` (tag `milan-fpga-697-pin-405dc683`), re-recording what the pin feeds through its generators;
2. merge current dev with a merge commit;
3. retarget F-INT's 11 `pub-acmp-*` plants to `third_party/tsn-c-stack/src/acmp.c`;
4. images byte-identical to dev's at the merged dev, every shape;
5. keep round 12's threat model, environment allowlist and 79 pin controls.

STOP if any image differs, or if any F-INT plant cannot be retargeted.
Base of the round: `adb936049165dc82e8832e79329984108eb1480f`. New commits only, no rebase or amend; not pushed.
Status: REVIEW READY at the head below, posted as #697 comment [6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531) (its text: `round13/review-ready-round13.md`); every gate passes there (one pre-existing docs self-test failure under `MAKEFLAGS=w`, as on dev). Neither STOP condition holds: no image differs, and all 11 F-INT plants are retargeted and caught.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `c03e9c9c4` | Move the tsn-c-stack pin to 405dc683, the round-12 pin with F-INT's ACMP publish port, and point the docs and the submodule diagram at it | the core proof (below); `ctrl_build.py --stack-pin` (`tsn-c-stack at 405dc683…`); `submodule_boundaries.gen.py` (written, then `--check` and `--selftest`); `check_submodule_docs.py` and `--selftest`; `check_diagram_pngs.py` and `--selftest`; `docs_check.py`; the stack's own `scripts/check_boundary.py`; all rc 0 |
| `30744883f` | Merge dev c20c85bd, keeping the ACMP core's removal now that the pinned stack carries F-INT's publish port, and requiring publication-census beside firmware-boundary and firmware-verilator | dev's `acmp_mbx.c` compiled against the pinned headers (`-Wall -Wextra -Werror -pedantic`, rc 0); `ci_events.py --check` (1974 items) and `--selftest` (2766 arms), CPython 3.12.3; the diagram regenerated through its generator, `--check` rc 0 |
| `5425fb644` | Plant F-INT's eleven pub-acmp defects into the stack's acmp.c, where the ACMP core now lives | each plant's fixture once in the stack's `src/acmp.c`, each killer test and its words in the stack's `tests/test_acmp.cpp` or `test_acmp_mbx.cpp` (scratch `pub_plants.py`); pyflakes; `check_py_idiom.py`; then the full gates at this head (below) |
| `6382dc88a` | Say on the submodule page that the tsn-c-stack pin is kept reachable by its tag, not by main | `check_submodule_docs.py`, `check_doc_style.py` (which first refused one 23-word paragraph, so it is two), `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --check`, `check_em_dash.py --base adb93604`, all rc 0 |
| `8aaa2da74` | Hold dev's publication census, which names the firmware only in its docstring, as a builder whose compiles are none of the firmware's | found by the `firmware-boundary` replica (below); pyflakes, `check_py_idiom.py`, a scratch reading of the builder census; then every gate at this head |

One-line subjects, no body, no trailers, configured identity. The merge's parents are `c03e9c9c4` and dev `c20c85bddd4ec5a054be42b55fc291a3b4c7f7d8` (the dev tip when fetched, PR #722's merge; it holds F-INT's `09c7231ec`).

Head: `8aaa2da74e3d5ee569fed420debc2b69c6749d44` (four commits and one merge commit on `adb93604`; `git diff --stat c20c85bd HEAD` is the lane's whole change against dev). Every gate below ran at this head unless it says otherwise.

### Item 1: the pin

**The pin is `405dc68310a18f669049ffc10cc23eef7300dcff`**, the tag `milan-fpga-697-pin-405dc683` (a lightweight tag on the commit; `git ls-remote` gives the same SHA), the head of tsn-c-stack PR #22 (closed; its content merged to `main` as `1ba27354` through PR #23). It is `1a9f651c` plus four commits: `2dcbe91` (the publish port), `f3dc2ae`, `bc68ad8` and `405dc68`. `git diff --stat 1a9f651c 405dc683`: 22 files, 1082 insertions, 31 deletions; the cores' part is `include/acmp.h` +30 and `src/acmp.c` +37. Not `main`: `git diff 405dc683 1ba27354 -- src include` is `src/adp.c` (+6 −2, tsn-c-stack PR #19's discard change), which would change the firmware.

**The proof that its cores are the code dev builds** (`pin-proof.txt`, round 13 section; `pin-text-diff-405dc683.txt`, 92,010 bytes):

| File (dev `c20c85bd` `sw/firmware/ctrl/…` against the stack's `src/` or `include/`) | Raw tokens, comments and whitespace dropped, `(kind, spelling, line)` |
|---|---|
| `adp/adp.c` | SAME 1736 / 1736 |
| `adp/adp.h` | SAME 497 / 497 |
| `acmp/acmp.c` | SAME 7849 / 7849 (round 1: 7586; F-INT's port is the difference) |
| `acmp/acmp.h` | SAME 1175 / 1175 (round 1: 1137) |
| `maap/maap.c` | SAME 2064 / 2064 |
| `maap/maap.h` | SAME 394 / 394 |
| `wire/wire.h` | SAME 202 / 202 |

The seven files are the same bytes at dev `09c7231ec` (F-INT's merge) and at `c20c85bd`. The textual diff is comment and SPDX lines only. Each core compiled from each side's flat copy with the image flags (the pinned SDK's GCC 14.3.0, `ctrl_build.RV32_FLAGS` less `-fstack-usage`, `ctrl_image.IMAGE_FLAGS`, `fw_rv32.includes`), once `-DNDEBUG` and once `-UNDEBUG`: six of six object pairs BYTE-EQUAL (`adp.c` `a69f577a…`/`76ee7907…`, `acmp.c` `317e7037…` both, `maap.c` `0ec9b61b…`/`0a6132f0…`).

**Re-recorded through the generators** (`c03e9c9c4`, then again in the merge with dev's lwSRP pin):
- the gitlink (`third_party/tsn-c-stack`, `git ls-files --stage`: `160000 405dc683… 0`);
- `docs/reference/SUBMODULES.md:27` (the pin row) and `:249`, `:294` (the licence and quality-workflow links);
- the submodule diagram, `docs/diagrams/submodule_boundaries.{drawio,svg,png}` and its `PNG_MANIFEST.json` entry, written by `submodule_boundaries.gen.py` (the SVG's `pin 405dc68310a1` and `pin 08ee86e812a0`), `--check` `OK (6 exact gitlinks, decoded PNG)`;
- the pinned links into the stack: `sw/firmware/ctrl/README.md:65-68`, `:78`, `:239`, `:248`, `:261`; `sw/firmware/ctrl/maap/README.md:19`; `sw/firmware/gtest/README.md:246-247`, `:291`, `:299`; `docs/design/MAILBOX_SPLIT.md:114`, `:330`, `:527`. Every linked path exists at `405dc683` (`git cat-file -e`), and `docs/PORTING.md` still has `## Ownership and dispatch`;
- the boundary: the stack's own `scripts/check_boundary.py` at the pin (`compiler dependencies and object symbols pass`), and both boundary jobs (below);
- `SUBMODULES.md:240-243` (`6382dc88a`): the pin is not on tsn-c-stack's `main`, which merges by squash; its tag keeps it reachable; that `main` also changes `src/adp.c`.

At `c03e9c9c4` alone, before the merge, the stack's core calls a `publish` port that only dev's adapter sets (`acmp_mbx.c` `m->ports.publish = port_publish;`, which arrives with the merge). So that commit is not a firmware state anyone should build: its firmware gates were not run there, and the evidence is at the merge's descendants.

### Item 2: the merge

`git merge --no-ff c20c85bd` on `c03e9c9c4` stopped in 13 conflicts, the same files as round 12's trial:

| Conflict | Resolution |
|---|---|
| modify/delete `sw/firmware/ctrl/acmp/acmp.c`, `acmp/acmp.h`, `test/acmp_fake.hpp`, `test/test_acmp.cpp` | the deletion kept (`git rm`). Dev's `acmp.c`/`acmp.h` are token for token the pinned stack's (above). Dev's `acmp_fake.hpp` is the stack's `tests/acmp_fake.hpp` token for token (2648 tokens; the lines differ in comments). Dev's `test_acmp.cpp` has 69 tests, every name of which is among the stack's 79 |
| `.github/workflows/rtl-fast.yml` | the aggregate needs and checks all eight: `publication-census` (F-INT's) and `firmware-unit`, `firmware-boundary`, `firmware-verilator` (`rtl-fast.yml:487`, `:509-512`) |
| `scripts/ci_events.py` | the aggregate's step environment holds both sides' result names (`ci_events.py:594`); both sides' job constants kept (`:1263`, `:1265`, `:1268`) |
| `docs/testing/CI_WORKFLOWS.md` | a documentation-only change skips `publication-census`, `firmware-unit`, `firmware-boundary` and `firmware-verilator` (`:118`) |
| `tb/verilator/mbx/Makefile` | `.PHONY` names dev's `census` and this lane's `stack-pin` (`:71`) |
| `docs/reference/SUBMODULES.md` | dev's lwSRP pin `08ee86e8` and this lane's tsn-c-stack row (`:26-27`) |
| `docs/diagrams/submodule_boundaries.{drawio,svg,png}`, `PNG_MANIFEST.json` | regenerated by its generator from both gitlinks |

Not conflicted and taken as merged: dev's adapter `acmp/acmp_mbx.{c,h}` with its `publish` wiring, the lwSRP gitlink `08ee86e8` (its checkout updated with `git submodule update`), F-INT's `publication-census` job, and the rest of dev. Dev's `acmp_mbx.c` compiles against the pinned headers (`gcc -std=c11 -Wall -Wextra -Werror -pedantic -fsyntax-only`, rc 0); in round 12, against `1a9f651c`, it failed with `'struct acmp_ports' has no member named 'publish'`.

No reference to the removed paths is left outside the stack (`git grep` of `acmp/acmp.[ch]`, `test/test_acmp.cpp`, `test/acmp_fake`), except `ctrl_build.py:458-459`'s `LEGACY` map, which reads revisions from before the move, and the 11 plants (item 3).

### Item 3: F-INT's eleven plants

`5425fb644` names `ACMP_C` (`ctrl_mutant.py:14`, `tsn-c-stack/src/acmp.c`) for each, `ctrl_mutants.py:588`, `:593`, `:598`, `:601`, `:605`, `:608`, `:614`, `:632`, `:635`, `:638`, `:642`, imported at `:29`. Nothing else in a plant changed: its fixture, defect, arm, killer tests and their words are dev's. Each fixture occurs once in the stack's `src/acmp.c` (the campaign's `plant` refuses any other count), and each killer test and its words are in the stack's `tests/test_acmp.cpp` or this repository's `test_acmp_mbx.cpp`. The three adapter plants (`pub-acmp-adapter-*`, `acmp/acmp_mbx.c`) stay this repository's. Whether each is caught by name is in the campaign (below).

### Self-review after `6382dc88`: dev's publication census and the boundary's builder census

The `firmware-boundary` replica at `6382dc88` built every known builder (rc 0 each) and then refused, rc 2 after 701 s:

`REFUSED: sw/mailbox/publication_census.py names the firmware's tree and is a program, and is neither a known builder (ctrl_configs.BUILDERS) nor listed as one that runs under another (PART_OF), compiles none of the firmware's (OUTSIDE) or compiles only in a suite (SUITES)`

The census is F-INT's (dev `09c7231e`). It names `sw/firmware/ctrl/app/ctrl_app_aecp.c` once, in its docstring (`publication_census.py:90`), and runs only sv2v, Yosys and the builder's generator (`census_elab.run`), no C compiler. This lane's cross-check finds builders by text and refuses any program it cannot place, so the merge made the gate refuse by name, as it should.

`8aaa2da74` ("Hold dev's publication census, which names the firmware only in its docstring, as a builder whose compiles are none of the firmware's") lists it in `OUTSIDE` with that reason (`ctrl_configs.py:164-165`). With it, a scratch reading of `ctrl_configs.builder_texts()` finds 33 modules by text: none is unplaced but the four non-programs that compile in the capture (`ctrl_arms.py`, `srp_arms.py`, `nvm_bench.py`, `fw_gtest.py`, as before), and no `OUTSIDE` entry is stale. The `--only verilator` run leaves this cross-check to the boundary run (`ctrl_configs.held`), which is why only `firmware-boundary` saw it.

### Item 4: the images, byte for byte against dev

Every RV32 image at every shipped shape, linked in fresh clones at dev `c20c85bd` and at the head with the same pinned SDK and round 1's runtime archives (scratch `images6.sh`, unchanged since round 6: `ctrl_image.py` at each of the five shapes; `ctrl_srp_image.py` at each, one and two interfaces, with SRP, without it and with AECP). 35 of 35 ELF hashes are identical. The two manifests are the same bytes, sha256 `8b1292dbe318603b3ed2354c0b58c2721ab3f27094589153d946af0783b39095`, at `5425fb64` and again at `6382dc88`. All 35 differ from round 12's (`de8ae063…`, at `adb93604`), as dev's F-INT and lwSRP `08ee86e8` changed the firmware; this lane's head builds dev's exactly.

| Image (shape) | dev `c20c85bd` sha256 | head sha256 (`6382dc88`; `8aaa2da7` changes no source the images build) | |
|---|---|---|---|
| `ctrl_image/head/endstation_arty_4x4` | `8c27ee19b7a4f0a6…` | `8c27ee19b7a4f0a6…` | same |
| `ctrl_image/head/endstation_arty_8ch` | `b7976d5cc2e0bc88…` | `b7976d5cc2e0bc88…` | same |
| `ctrl_image/head/endstation_arty_current` | `b119b2b56911120e…` | `b119b2b56911120e…` | same |
| `ctrl_image/head/endstation_ax7101_1x1_tdm8` | `5a4086ce0245a5e2…` | `5a4086ce0245a5e2…` | same |
| `ctrl_image/head/endstation_ax7101_8x8` | `acb380ee815698bc…` | `acb380ee815698bc…` | same |
| `srp_image/endstation_arty_4x4-if1-aecp` | `82e5ce706c7736fa…` | `82e5ce706c7736fa…` | same |
| `srp_image/endstation_arty_4x4-if1-nosrp` | `b25d258237bf6aa4…` | `b25d258237bf6aa4…` | same |
| `srp_image/endstation_arty_4x4-if1-srp` | `228c4d2d4da86158…` | `228c4d2d4da86158…` | same |
| `srp_image/endstation_arty_4x4-if2-aecp` | `a2dd25cfe83a2469…` | `a2dd25cfe83a2469…` | same |
| `srp_image/endstation_arty_4x4-if2-nosrp` | `77419321adfeed90…` | `77419321adfeed90…` | same |
| `srp_image/endstation_arty_4x4-if2-srp` | `d11e73701465dc12…` | `d11e73701465dc12…` | same |
| `srp_image/endstation_arty_8ch-if1-aecp` | `c2799ea46a854c45…` | `c2799ea46a854c45…` | same |
| `srp_image/endstation_arty_8ch-if1-nosrp` | `b23e71ad89fe5f7d…` | `b23e71ad89fe5f7d…` | same |
| `srp_image/endstation_arty_8ch-if1-srp` | `fed8b54f96ec1c60…` | `fed8b54f96ec1c60…` | same |
| `srp_image/endstation_arty_8ch-if2-aecp` | `57ad658eff2ddd75…` | `57ad658eff2ddd75…` | same |
| `srp_image/endstation_arty_8ch-if2-nosrp` | `f47dc12d5a6bbf98…` | `f47dc12d5a6bbf98…` | same |
| `srp_image/endstation_arty_8ch-if2-srp` | `8da5b37b2527b7b6…` | `8da5b37b2527b7b6…` | same |
| `srp_image/endstation_arty_current-if1-aecp` | `7f2bac9275054548…` | `7f2bac9275054548…` | same |
| `srp_image/endstation_arty_current-if1-nosrp` | `f0f462ae82deb1f9…` | `f0f462ae82deb1f9…` | same |
| `srp_image/endstation_arty_current-if1-srp` | `7c8ecec43b7a6f82…` | `7c8ecec43b7a6f82…` | same |
| `srp_image/endstation_arty_current-if2-aecp` | `31dd11a7820b681d…` | `31dd11a7820b681d…` | same |
| `srp_image/endstation_arty_current-if2-nosrp` | `3f40b9150068f56b…` | `3f40b9150068f56b…` | same |
| `srp_image/endstation_arty_current-if2-srp` | `0ca8e6a97eafb7f6…` | `0ca8e6a97eafb7f6…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if1-aecp` | `74a12209e0301a9a…` | `74a12209e0301a9a…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if1-nosrp` | `a2bea49e78da57f9…` | `a2bea49e78da57f9…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if1-srp` | `db0fb58e7ebfec18…` | `db0fb58e7ebfec18…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if2-aecp` | `d3fc02d6916278dc…` | `d3fc02d6916278dc…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if2-nosrp` | `bf7e37a793f2a5cc…` | `bf7e37a793f2a5cc…` | same |
| `srp_image/endstation_ax7101_1x1_tdm8-if2-srp` | `e052ed2b10e1ae3a…` | `e052ed2b10e1ae3a…` | same |
| `srp_image/endstation_ax7101_8x8-if1-aecp` | `1721078bbde9510b…` | `1721078bbde9510b…` | same |
| `srp_image/endstation_ax7101_8x8-if1-nosrp` | `7dd3d0843ef5f97f…` | `7dd3d0843ef5f97f…` | same |
| `srp_image/endstation_ax7101_8x8-if1-srp` | `b9bf08715abcd58e…` | `b9bf08715abcd58e…` | same |
| `srp_image/endstation_ax7101_8x8-if2-aecp` | `fbcf4230d2a5087f…` | `fbcf4230d2a5087f…` | same |
| `srp_image/endstation_ax7101_8x8-if2-nosrp` | `104552602a5e5fb9…` | `104552602a5e5fb9…` | same |
| `srp_image/endstation_ax7101_8x8-if2-srp` | `3fc8b8ab4ba24e7d…` | `3fc8b8ab4ba24e7d…` | same |

`ctrl_image.py --base c20c85bd` at `8aaa2da7`: `+0` in every section at both shapes (`text 34,088`, `bss 13,248`, total 48,084; and `text 34,092`, `bss 23,600`, total 58,440).

### Item 5: what round 12 left

The threat-model texts, `ctrl_build.GIT_ENVIRONMENT`, `ctrl_pin.py` and `ctrl_pin_env.py` are unchanged (`git diff adb93604 HEAD -- sw/firmware/ctrl/test/ctrl_build.py sw/firmware/ctrl/test/ctrl_pin.py sw/firmware/ctrl/test/ctrl_pin_env.py` is empty). Each boundary job runs the 79 pin controls at the head, 0 misbehaved. The controls clone the stack at the new pin, so `pin~1` is now `bc68ad8f…`: `GIT_INDEX_FILE` gives `tsn-c-stack at bc68ad8f… is not the pinned 405dc683…`. Separately:
- the 52 hook and inherited-environment controls and the clean proof (`pin_subset.py`), at `8aaa2da7`: 52 of 52 on CPython 3.12.3 and on 3.14.7;
- the hook-rule campaign (`hook_mutants.py`, four disposable clones at `8aaa2da7`): H0 clean and H1 to H24 CAUGHT, 24 of 24 on each interpreter, every escape count as in round 12 (H5 19, H15 25, H16 34, H22 17, H23 11), each clone restored;
- every entry point (`entrypoints.py`, a clone at `8aaa2da7`): 17 × 5 disguises, 85 of 85 refused, naming `405dc683`; the clone clean afterwards.

### The campaigns, against dev

`firmware-unit`'s steps in fresh clones, dev `c20c85bd` and the head, the same CI-parity container and CPU count. Every verdict line of the firmware gate (`[ok]`/`[ESCAPED]`/…), compared line by line (scratch `compare13.py`):
- 915 lines on each side, every one `[ok]`, the same labels in the same order;
- the ctrl campaign `mutants: 506 of 506 caught` on each (round 12's 471, plus dev's 35); the same 506 names, no verdict different; the AECP and SRP campaigns and both lwSRP pin arms `[ok]` line for line;
- 35 lines differ, each `[ok] mutant <name> (<arms>): N check(s) failed`, only in N: the `acmp-*` and `pub-acmp-*` plants, N at the head never lower (+90 in all). The stack's `test_acmp.cpp` holds 79 tests where dev's held 69, so a plant fails more of them;
- the head's gate prints `tsn-c-stack at 405dc68310a18f669049ffc10cc23eef7300dcff` first.
- 60 arms on each side (dev's `srpcmp` is the 60th), every arm's test tally equal but `acmp` (105 tests at the head, 95 at dev) and `adp` (34 and 26; 34 at round 12's head too): the stack's core suites are larger than dev's copies, and no arm runs fewer.

F-INT's eleven core plants, at the head: `pub-acmp-after-the-response` (16 checks failed), `-skipped-at-the-end-of-an-entry` (51), `-talker-for-the-stream` (7), `-stream-held-past-settlement` (1), `-every-sink-every-entry` (26), `-port-unguarded` (1), `-reset-forgets-the-port` (3), `-started-after-the-response` (1), `-started-after-the-report` (4), `-started-from-bound` (9), `-started-move-skipped` (5): each `[ok]`, its named killer failing on its words. Control: at the merge `30744883` alone, the campaign's own `plant` cannot apply any of the 11 (`FileNotFoundError` on `work/ctrl/acmp/acmp.c`); at the head it applies all 11 (scratch `plant_probe.py`).

### Coverage

`fw_coverage.py --check` PASS (30 files) at dev and at the head, every file at 100 % of lines and branches. The 30 rows are equal, with dev's core rows read at the stack's paths:

| File | dev `c20c85bd` | head |
|---|---|---|
| `acmp.c` (`sw/firmware/ctrl/acmp/` → `third_party/tsn-c-stack/src/`) | 767/767 lines, 362/362 branches | 767/767, 362/362 |
| `adp.c` | 204/206, 95/102 | 204/206, 95/102 |
| `maap.c` | 209/209, 140/140 | 209/209, 140/140 |
| `wire.h` (`…/wire/` → `…/include/`) | 10/10, 2/2 | 10/10, 2/2 |

The head's table (its 30 rows, sha256 `8fcdce6d…2265c70`, scratch `cov-head.txt`) differs from round 12's in five rows, each dev's own: `acmp_mbx.c` 79/79, `maap_mbx.c` 99/99, `mbx.c` 243/243, `srp_mbx.c` 539/539 and `acmp.c` 767/767 (742 in round 12; the port's 25 lines). The coverage self-test catches 29 of 29 planted cases at the head (dev 28 of 28; the lane's stack case is the 29th).

### Gates at the round-13 head

Containers: the CI-parity image (Ubuntu 24.04.5, its CPython 3.12.3, GCC 13.3, GNU make 4.3 under `MAKEFLAGS=w`, static GoogleTest 1.14.0, clang 18, cmake 3.28), four CPUs each on disjoint sets of the service's 64-79, fresh clones; up to four ran at once beside other lanes' Yosys and Verilator work on the host. Host: CPython 3.12.3 (PyYAML, the locked renderer) and 3.14.7, GNU make 4.3, the pinned SDK. The service's memory peaked at 3.5 GB.

| Gate | Where | Result |
|---|---|---|
| `firmware-boundary`'s step (`ctrl_boundary.py --require-rv32 --selftest --without verilator`) | container, `8aaa2da7` | PASS, 699 s (39 % of 30 minutes): `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own) …; 0 finding(s), 105 boundary, 79 pin and 4 figure controls, 0 misbehaved`. At `6382dc88` it refused dev's census by name (above), rc 2 after 701 s |
| `firmware-verilator`'s step (`--only verilator`, the pinned Verilator 5.050, `VERILATOR_JOBS=2`) | container, `8aaa2da7` | PASS, 471 s (20 % of 40): `829 compiled sources of 930 (386, 94, 349) …; 0 finding(s), 6 boundary, 79 pin and 4 figure controls, 0 misbehaved` (round 12: 816 of 916; dev's bench grew). At `6382dc88`: PASS, 517 s, the same counts |
| `firmware-unit`'s steps (`unitjob.sh`) | container, `8aaa2da7` | every step rc 0, 2104 s (78 % of 45 minutes): `tsn-c-stack at 405dc683…`, 60 arms, `mutants: 506 of 506 caught`, `test_ctrl_firmware: PASS`; the store `OK across 5 shape(s), 435 tests`; the coverage self-test 29 of 29; `firmware coverage: PASS (30 files)`. Its 915 verdict lines (sha256 `861dcd9f7e1703b205cb36dc277da69d234dae1b4c684ff8aef91b628f0937ef`) and coverage rows are byte-identical to the run at `6382dc88` (2210 s) |
| the same at dev `c20c85bd` | container | every step rc 0, 2170 s: `mutants: 506 of 506 caught`, 915 verdict lines all `[ok]` (sha256 `dd3b4ac6…eae23`), coverage 30 files; compared above |
| the docs job's 54 commands (`docsjob.sh`) | host, a clone with only the builder's three submodules (no tsn-c-stack, no lwSRP, as hosted), make 4.3, `MAKEFLAGS=w`, `8aaa2da7` | 53 of 54 rc 0: `ci_events.py --check` (1974 items) and `--selftest` (2766 arms), `ci_scope.py --selftest`, `check_py_idiom.py` (every ratchet held), `check_em_dash.py --base adb93604` (0 over 2217 added lines, dev's included), `docs_check.py` (0 findings, 203 pages), `check_submodule_docs.py`, `submodule_boundaries.gen.py --check` and `--selftest`, `check_diagram_pngs.py` and `--selftest` (28 mutation controls) among them. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50, the same two fixtures at dev `c20c85bd` with `MAKEFLAGS=w`; 50 of 50 at the head without it (round 12's finding, unchanged) |
| `check_em_dash.py --base $(git merge-base origin/dev HEAD)` (`c20c85bd`, as hosted) | host | 0 findings over 401 added lines in 12 pages |
| `act_ci.py --selftest --worktree <clone>` (the copy installed 0555 outside the tree, sha256 `797f123b…d22d1`, the tree's) | host, CPython 3.12.3 with PyYAML, a clone at `8aaa2da7` (and at `6382dc88`) | PASS, 446 arms, line for line round 8's |
| images (`images6.sh`) | host, the pinned SDK, round 1's runtime archives, `8aaa2da7` (and `6382dc88`, `5425fb64`) | 35 of 35 identical to dev `c20c85bd` (above) |
| `ctrl_image.py --base c20c85bd` | host, `8aaa2da7` | `+0` in every section at both shapes |
| the 52 hook and inherited-environment controls (`pin_subset.py`) | host, `8aaa2da7`, CPython 3.12.3 and 3.14.7 | 52 of 52 on each |
| the hook-rule campaign (`hook_mutants.py`) | host, four clones at `8aaa2da7` | 24 of 24 CAUGHT on each interpreter, H0 clean |
| every entry point (`entrypoints.py`) | host, `8aaa2da7` | 85 of 85 refused |
| `ctrl_build.py --stack-pin`, the stack's `scripts/check_boundary.py`, `check_submodule_docs.py --selftest`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check` | host, the lane | rc 0 each |

Not run: the stack's own CMake suite with `ctest` (the README's three commands) as a separate step. The local run was refused by this session's permission settings, and it was not retried another way. The stack's core tests run inside the firmware gate's arms (`adp` 34, `acmp` 105 tests, among others), and its CMake build with gcc and clang runs as a builder of the boundary job.

### Open risks and questions (round 13)

1. **Intermediate commits.** `c03e9c9c4` (the pin alone) does not build working firmware: the stack's core calls `ports->publish` unguarded, and only the merge's adapter sets it. The merge `30744883f` alone cannot apply the 11 plants. Each is a step of the assignment's order; the head is where every gate passes.
2. **Round 12's two in-model routes** (a forged tree object in the stack's object store; the repository's own `core.fsmonitor`) remain published, not fixed, awaiting a ruling.
3. **`MAKEFLAGS=w` and `check_rtl_source_lists.py --selftest`:** 48 of 50 at dev `c20c85bd` and at the head alike; outside this lane.
4. **`firmware-unit`'s headroom:** 2104 s in the replica (dev's own 2170 s), over 60 % of 45 minutes; #716's scope. PR #724 (#716) touches the same CI files; whichever merges second resolves.
5. **Carried:** R584-9-S1 stays optional and not taken; R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's RES-1 wording go to #495.
