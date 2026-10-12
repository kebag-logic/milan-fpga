# HANDOFF — lane 697c, [A583]

Issue: [kebag-logic/milan-fpga#697](https://github.com/kebag-logic/milan-fpga/issues/697), assignment comments 6091228902 (round 1), 6092628778 (round 2), 6093389868 (round 2b), 6094873968 (round 3), 6096148471 (round 4), 6097800045 (round 5), 6102039501 (round 6), 6104711137 (round 7), 6105928035 (round 8), 6107732413 (round 9), 6112358746 (round 10), 6113306444 (round 11), 6114400461 (round 12), 6116488747 (round 13) and 6117713386 (round 14).
Branch: `697-consume` from dev `8b61b70902f3ebf118e56967277e2686731081bd`, pushed as PR #705; PR #705 shows round 13's head `8aaa2da7`.
Head: `a8fe548a083239efc799a79c540b2be63e9d13e7` (round 14: four commits on `8aaa2da7`, PR #705's head; not pushed).
Status: round 14 REVIEW READY at `a8fe548a0`, comment [6118316100](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118316100) (its text: `round14/review-ready-round14.md`) (every object the proof reads hashed against its id; `core.fsmonitor=false`; the alternates control; see [Round 14](#round-14)); round 13 REVIEW READY at `8aaa2da74`, comment [6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531) (its text: `round13/review-ready-round13.md`) (pin `405dc683`, dev `c20c85bd` merged, F-INT's plants retargeted, images identical to dev's; see [Round 13](#round-13)); round 12 STOP at `adb936049` (item 1, the dev merge; items 2 and 3 done), comment [6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316) (its text: `round12/stop-round12.md`) (see [Round 12](#round-12)); round 11 REVIEW READY at `aca5e8afc`, comment [6114209149](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114209149) (its text: `round11/review-ready-round11.md`) (see [Round 11](#round-11)); round 10 REVIEW READY at `be607527e`, comment [6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) (its text: `round10/review-ready-round10.md`) (see [Round 10](HANDOFF-rounds-7-10.md#round-10)); round 9 REVIEW READY at `feed95bbb`, comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179) (see [Round 9](HANDOFF-rounds-7-10.md#round-9)); round 8 REVIEW READY at `4cab445aa`, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`) (see [Round 8](HANDOFF-rounds-7-10.md#round-8)); round 7 REVIEW READY at `8436dfc0b`, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (see [Round 7](HANDOFF-rounds-7-10.md#round-7)); round 6 REVIEW READY at `5b4f6fbeb`, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`) (see [Round 6](HANDOFF-rounds-2-6.md#round-6)); round 5 REVIEW READY at `92b5be188`, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (see [Round 5](HANDOFF-rounds-2-6.md#round-5)); round 4's REVIEW READY was comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937); round 3's was comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057), round 2b's 6094033396, round 2's 6093383132. Round 1: TAKEN 6091267846, REVIEW READY 6092168627; the pin was confirmed in 6092176555.
PR body: `PR-BODY.md` in this directory (round 2 to 14 sections added, round 5's residue and round 14's R585-12-RS1 to RS4 and R584-11-RES-1 applied; no PR edit made).

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

## Rounds 7 to 10

Moved verbatim to [`HANDOFF-rounds-7-10.md`](HANDOFF-rounds-7-10.md) in round 14 (its sections: [Round 7](HANDOFF-rounds-7-10.md#round-7), [Round 8](HANDOFF-rounds-7-10.md#round-8), [Round 9](HANDOFF-rounds-7-10.md#round-9), [Round 10](HANDOFF-rounds-7-10.md#round-10)), so this file stays under 200 KB.

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

## Round 14

Assignment: #697 comment [6117713386](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117713386), answering [R584-11](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6117711037) and [R585-12](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6117666847), both NEGATIVE at `8aaa2da7` on one MINOR (R584-11-F1 = R585-12-F1: the pin proof accepts an edited core source under a forged `src/` tree object, a route the round-12 ruling puts inside the model). Items:
1. every object the proof reads is checked against its id, failing closed (the pinned commit, every tree it walks, every blob it compares); a standing control plants R585-12's forged subtree (`forge_probe.py` F1), refused by name before any build; F0 and F2 keep their verdicts;
2. R585-12-S1: the helper passes `-c core.fsmonitor=false`, with a standing control;
3. R585-12-S2 (optional): the alternates control independent of an inherited `objects/info/alternates`;
4. the PR-body residue (R585-12-RS1 to RS4, R584-11-RES-1), here in `PR-BODY.md`; R584-11-S1 optional.

The 79 pin controls and the environment controls still hold, and the images stay byte-identical.
Base of the round: `8aaa2da74e3d5ee569fed420debc2b69c6749d44` (PR #705's head). New commits only, no rebase or amend; not pushed.
Status: REVIEW READY at the head below, posted as #697 comment [6118316100](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118316100) (its text: `round14/review-ready-round14.md`; see [Gates](#gates-at-the-round-14-head)); every item done, the optional S2 taken, R584-11-S1 not taken.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `d89898db3` | Hash every object the pin proof reads against its id, so a forged src/ tree or pinned commit in the stack's store is refused by its place, with standing controls for both and a forged blob | the new walk against round 13's `ls-tree -r -t` listing of the pin (scratch `tree_equiv.py`: 89 entries, 11 trees, equal, CPython 3.12.3 and 3.14.7); the census (0 findings; it runs the proof under its hook); the 17 inherited-environment controls and the 3 new ones (scratch `store_subset.py`, 20 of 20 `[ok]`); R585-12's `forge_probe.py` (F0, F1, F2 refused); pyflakes; `check_py_idiom.py` |
| `b62c1981c` | Give every Git command of the pin proof core.fsmonitor=false, so no repository's own configuration starts a program while the pin is decided, with standing controls for the superproject's and the stack's | census 0 findings; `store_subset.py` 22 of 22; pyflakes; `check_py_idiom.py` |
| `4a35f2f44` | Empty the alternates file in the pin control whose clone's store no longer holds the pin, so a stack initialised with --reference cannot lend it the objects | `store_subset.py --reference` (the stack cloned with `--reference`, as R585-12's setup): 1 of 22 `[ESCAPED]` at `b62c1981` (R585-12's receipt reproduced), 0 of 22 here; pyflakes |
| `a8fe548a0` | Forge the object-store controls' objects as new files, so no loose file a hard link shares with another store is written | `store_subset.py` 22 of 22, with and without `--reference`; pyflakes; `check_py_idiom.py`; then every gate below at this head |

One-line subjects, no body, no trailers, configured identity.

Head: `a8fe548a083239efc799a79c540b2be63e9d13e7` (four commits on `8aaa2da7`; `git diff --stat 8aaa2da7 HEAD`: six files under `sw/firmware/ctrl`, 280 insertions, 42 deletions). No firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin changes.

### Item 1: every object the proof reads, checked against its id

What the proof reads from the stack's object store, and how each is now checked:
- **the pinned commit**: read raw (`git cat-file commit <pin>`), hashed here as Git hashes an object (`commit <length>\0<bytes>`, with the repository's object format) and compared with the pin;
- **every tree under it**: the root tree the verified commit names, then each subtree a verified tree names, each read raw (`git cat-file tree <id>`), hashed (`tree <length>\0<bytes>`) and compared with its id, then parsed here (mode, name, id), never listed by Git;
- **no blob**: each file and symbolic link of the checkout is hashed from its own bytes, as before, and compared with the blob id its verified tree records, so no blob object is read and none can stand in for one.

Git checks neither path itself: it checks the hash of the object a command is given (which is why round 13's F2 was refused), but not of a tree below it that `ls-tree -r` walks (F1), and not of anything `cat-file` prints. Mutant M1 below shows the second: with the hash comparison removed, both the forged tree and the forged commit are accepted. So the check is what refuses both, and a forged or corrupt object is refused by its place in the pin before any build:

```text
REFUSED: tsn-c-stack's object store holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40, not to its id, so nothing under it can be compared
```

A read failure keeps round 13's words (`cannot read the pinned tree of <stack>: the pinned commit (commit 405dc683): fatal: ...`), which the alternates control reads.

Changes (file:line at the head):
- `sw/firmware/ctrl/test/ctrl_build.py:432` `KINDS`; `:435-446` `stored` (one object read raw, hashed, compared, refused by its place); `:449-468` `pinned_tree` (the walk); `:471-493` `stack_pin` (calls `pinned_tree` where it called `ls-tree -r -t`; its docstring states the check).
- `ctrl_build.py:197-205` `GitRun.raw` and `:375-389` the helper: Git's output is captured as bytes and decoded here (UTF-8, `surrogateescape`, as before); the bytes are kept for the raw reads. Text mode's newline translation is gone, which changes no answer the proof reads (Git prints no carriage return in them).
- `sw/firmware/ctrl/test/ctrl_pin.py:56-64` THE THREAT MODEL states the check in place of the two open routes; `:125-130` THE CONTROLS names `ctrl_pin_store.py`; `:191-198` the census's vocabulary gains the builtin `bytes` and the attributes `append`, `decode`, `hex`, `partition`, `pop` and `raw`; `:248` the hook plants' tree anchor moves to `want = pinned_tree(stack, pin, algorithm)`; `:980` `pin_controls` runs the new controls; `:991` cleans their directory.
- `sw/firmware/ctrl/test/ctrl_pin_store.py` (new, 167 lines): `loose` (`:46-58`, the clone fetched into a new repository with `fetch.unpackLimit` above its object count, so every object is loose, none packed, none in another store; refused by name otherwise), `forge` (`:61-69`, the victim's loose file replaced by a new file holding the source object's bytes), the three object-store controls (`:72-95`) and `store_arms` (`:113-167`).
- `sw/firmware/ctrl/test/ctrl_pin_env.py:79-91` `Scene.remade` and `Scene.edited_src`, shared by `swapped` (its behaviour unchanged) and the new controls.
- `sw/firmware/ctrl/test/ctrl_configs.py:75` `GATE` holds `ctrl_pin_store.py`, a module of the boundary gate, never a builder.
- `sw/firmware/ctrl/README.md:172-173` (the check), `:209` (84 pin controls, the figure the self-test checks), `:230-235` (the five new controls).

The standing controls (`ctrl_pin_store.store_arms`, after the 17 inherited-environment ones):

| Control | Verdict at the head | With M1 (no hash compared) |
|---|---|---|
| a source edited, the pinned `src/` tree's object replaced by a tree holding the edit (R585-12's F1) | `[ok]` `... forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to 832cc534 ...` | `[ESCAPED]` accepted `405dc683…` |
| a source edited, the pinned commit's object replaced by a commit whose tree holds the edit | `[ok]` `... the pinned commit (commit 405dc683) hashes to 3abf5e27 ...` | `[ESCAPED]` accepted `405dc683…` |
| a source edited, its pinned blob's object replaced by the edit's | `[ok]` `tsn-c-stack differs from the pinned 405dc683: src/adp.c` | `[ok]` (no blob is read) |

The reviewers' own probes, run unmodified against the head (`logs/forge-probe-head.txt`, `logs/model-routes-head.txt`):

| Probe | At `8aaa2da7` (their receipts) | At the head |
|---|---|---|
| R585-12 `forge_probe.py` F0, edit only | REFUSED `src/adp.c` | REFUSED `tsn-c-stack differs from the pinned 405dc683: src/adp.c` |
| F1, forged `src/` tree | **ACCEPTED** `405dc683…` | **REFUSED** `... the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40, not to its id ...` (`git fsck`: `9b48fa40…: hash-path mismatch`) |
| F2, forged pinned commit | REFUSED `cannot read the pinned tree ... hash mismatch 405dc683…` (Git's own check) | REFUSED `... the pinned commit (commit 405dc683) hashes to 55f2ca0d, not to its id ...` (the proof's check) |
| F3, the clone's own `core.fsmonitor` | ACCEPTED, 0 runs | ACCEPTED, 0 runs |
| R584-11 `model_routes.sh`, clean / edit | exit 0 / exit 2 `src/adp.c` | exit 0 / exit 2 `src/adp.c` |
| route 1, forged `src/` tree | **exit 0** | **exit 2** `... the pinned src/ tree (tree 5c8c189a) hashes to 7ebe40ef ...` |
| route 2, the clone's own `core.fsmonitor` | exit 0, 0 recorder lines | exit 0, 0 recorder lines |

**"By name", read publicly.** The refusal names the forged object by its place in the pin (`the pinned src/ tree`) and its id. It cannot name the edited file under a forged tree: the only listing of that tree the store gives is the forged one, which lists the edit as pinned. So R584-11's verification ("route 1 ends in exit 2 naming `src/adp.c`") is met as exit 2 naming the forged `src/` tree that holds it; R585-12's ("F1 refused by name") and the assignment's ("refuse it by name before any build") as written.

Every entry point (round 13's sweep, extended: scratch `entrypoints14.py`, a full clone at the head, `logs/entrypoints14.log`): the 17 entry points that pin the stack (the pin check, both firmware gates' forms, coverage, both image builders, the boundary, the MAAP differential's two modes, the three AECP tools, five mailbox bench targets), each under 7 states (round 13's five, plus the pinned `include/` tree's object and the pinned commit's object forged to hide an edit of `include/adp.h`): **119 of 119 refused**, the two new states each by the forged object's place (`the pinned include/ tree (tree 0042e213)`, `the pinned commit (commit 405dc683)`), before any build.

The walk gives exactly what `ls-tree -r -t` gave for the pin (`tree_equiv.py`): 89 entries, 11 of them trees, every mode, type and blob id equal, on CPython 3.12.3 and 3.14.7. A tree recorded with a non-canonical mode (`100664`, which `ls-tree` would print as `100644`) would now be refused by name rather than read as canonical; the pinned trees hold none.

### Item 2: the helper starts no program the configuration names

- `ctrl_build.py:385`: every Git command of the pin proof is `git -c core.fsmonitor=false -C <dir> ...`. The command line's setting outranks every configuration file, so neither the superproject's own `.git/config` (read when `stack_gitlink` runs `ls-files --stage` on its index) nor the stack's starts a program. Docstrings: the helper (`:378-382`), THE THREAT MODEL; README `:175`.
- Standing controls (`ctrl_pin_store.py:98-110`): a scratch superproject whose index's gitlink is the pin and whose own configuration names a recorder as `core.fsmonitor`, its gitlink read by `stack_gitlink` (`[ok]` `accepted 405dc683…`, the recorder never ran); and the stack clone's own configuration naming the recorder beside an edit (`[ok]`, refused by `src/adp.c`'s name, never ran).
- R585-12's superproject probe, reproduced on disposable clones (scratch `super_fsmonitor.sh`, `logs/super-fsmonitor.txt`): the pin check started the recorder **2 times at `8aaa2da7`, 0 at the head**, the verdict `405dc683…` at both.
- Mutant M2 (the setting removed from the helper): the superproject control `[ESCAPED]`: `Git ran a program a repository's own configuration names`. The stack's control holds with or without the setting, since the proof reads no index of the stack; it stands against a later index read.
- The setting also neutralises `core.fsmonitor` given through an inherited environment. That is why, in the hook-rule campaign, the mutants that let the caller's environment reach Git again (H22, H23) now escape 11 and 9 controls where round 13 counted 17 and 11: the six (H22) and two (H23) `core.fsmonitor` controls among them hold anyway. Both mutants are still caught.

### Item 3: the alternates control

`ctrl_pin_env.py:145-151` `unstored` also deletes the clone's `objects/info/alternates`, which a clone of a stack initialised with `--reference` inherits, so the store holds none of the pin's objects whatever it borrowed. With the stack cloned by `--reference` (R585-12's setup), the control was `[ESCAPED] ... tsn-c-stack at 405dc683…` at `b62c1981` and is `[ok] cannot read the pinned tree ... the pinned commit (commit 405dc683): fatal: ...` from `4a35f2f4` (`logs/s2-reference-c2.log`, `logs/s2-reference-c3.log`). The new object-store controls build their own store and pass with and without it. README `:225`.

### Item 4: the PR-body residue

Applied in `PR-BODY.md`, exactly as the reviews give them:
- R585-12-RS1 and R584-11-RES-1: ", not pushed" deleted from round 13's status line; round 14's status line says neither.
- R585-12-RS2: the Definition of Done reads "(all met locally; pin `405dc683` set by #697 comment 6116488747 under the rule of comment 6092176555)".
- R585-12-RS3: the five links of the fourth "Authoritative references" bullet name `8aaa2da74e3d5ee569fed420debc2b69c6749d44`, the published head (the control firmware page changes again in round 14; its link can move to the round-14 head once that is published).
- R585-12-RS4: "The hosted `firmware-boundary` job needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image."

R584-11-S1 (the pin-only commit `c03e9c9c` builds no working firmware) is not taken: it would need a history rewrite, which the round forbids; a squash merge leaves no such commit on `dev`.

### Self-review: an evidence script wrote into the lane's object store

The extended entry-point sweep ran in a full clone made by a plain local clone (round 13's `mkclone13.sh`), whose loose object files are hard links to the lane's own submodule store. Its two forged-object states overwrote the clone's loose files in place, so for less than two minutes (the sweep's last two states, ending at 04:44:33 UTC) the lane's `405dc683` commit object and `include/` tree object held forged bytes, until the sweep's own restore wrote them back. The image build at the head found it: it refused the lane's submodule by the forged commit's name, the new check doing its job.

Restored and checked: `git fsck --full` on the lane's submodule is clean, the pin check passes, and the two files are back at mode 0444 (all 85 loose objects). Every replica that overlapped the window was discarded and rerun on fresh clones; the sweep now replaces each file (a new inode) and was rerun, the lane's files keeping their inode, mode and bytes. The in-tree controls never wrote into a shared file (their clone is `--no-hardlinks`, then fetched into a new repository); `a8fe548a` makes `forge` replace the file anyway.

### The images

Every RV32 image at every shipped shape, linked at the head with the pinned SDK and round 1's runtime archives (scratch `images6.sh`, unchanged), against dev `c20c85bd`'s manifest from round 13 (the same script and archives). The manifests are byte-equal (sha256 `8b1292db…`, as round 13's head).

| Image (shape) | dev `c20c85bd` sha256 | head `a8fe548a` sha256 | |
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

35 of 35 identical


### Gates at the round-14 head

Every gate the change touches ran at `a8fe548a083239efc799a79c540b2be63e9d13e7`, in fresh clones (scratch `mkclone13.sh`, every submodule from the lane's checkout). The replica is the runner's Ubuntu 24.04 (CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0 static, cmake 3.28, clang 18, `MAKEFLAGS=w`), four CPUs each, the pinned RV32 SDK, the pinned Verilator 5.050; the three ran at once. Logs: `round14/logs/` in this directory.

| Gate | Where | Result |
|---|---|---|
| `firmware-boundary`'s step, `ctrl_boundary.py --require-rv32 --selftest --without verilator` (`boundaryjob.sh`) | replica, CPUs 64-67 | **PASS in 750 s**: 2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own), 0 findings, **105 boundary, 84 pin and 4 figure controls, 0 misbehaved** (`bjob-head.log`; the five new controls at its lines 208-212; the four figure controls read the README's 84) |
| `firmware-verilator`'s step, `--only verilator` (`vgate8.sh`) | replica, CPUs 72-75 | **PASS in 518 s**: 829 of 930, 0 findings, **6, 84 and 4, 0 misbehaved**; the bench (62 s), the MAAP differential's self-test (162 s) and the AECP wire comparison `--every` (216 s) each exit 0 (`vjob-head.log`) |
| `firmware-unit`'s steps (`unitjob.sh`) | replica, CPUs 68-71 | **every step rc 0, 2197 s in all** (`ujob-head.outer`): `tally_selftest.py` 3 s; `fw_rv32_selftest.py --require-rv32` 6 s; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` 1891 s, `tsn-c-stack at 405dc683…`, **`mutants: 506 of 506 caught`**, 915 verdict lines `[ok]`, 0 escaped, `test_ctrl_firmware: PASS`, every verdict line equal to round 13's at `8aaa2da7` once its time is dropped (its log, 348900 bytes, is kept out of this directory: sha256 `9e07907455b897f66ebbc8d43a3a987bdeda8d0b3f6fc027b29e619aa887cc93`); `test_ctrl_nvm.py` 77 s, `OK across 5 shape(s), 435 tests`; `fw_coverage.py --selftest` `29 of 29 planted cases`; `fw_coverage.py --check` 219 s, `firmware coverage: PASS (30 files)`, every row 100 % and equal to round 13's |
| the 35 RV32 images (`images6.sh`) | host, the pinned SDK, round 1's runtime archives | 35 of 35 identical to dev `c20c85bd` (above) |
| the docs job's 54 commands (`docsjob.sh`) | host, a clone with the job's three submodules, CPython 3.12.3 with PyYAML and the pinned renderer, `MAKEFLAGS=w` | 53 of 54 rc 0 (`docsjob-head.log`): `check_em_dash.py --base c20c85bd` (the merge base with live dev) 0 findings over 409 added lines in 12 pages; `docs_check.py` 0 findings across 203 pages; `check_py_idiom.py` every ratchet held (`long module: 10 <= 10`, `over-long line: 0 <= 0`); `check_hygiene.py --check` PASS; `ci_events.py --check` (1974 items) and `--selftest`; `gen_toc.py --check` and `--verify-anchors`; `DOC_MAP.gen.py --check`; `submodule_boundaries.gen.py --check` and `--selftest`; `check_submodule_docs.py` and `--selftest`. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50 under `MAKEFLAGS=w`, as at dev; 50 of 50 without it (`srclists-nomf-head.log`) |
| the hook-rule campaign (`hook_mutants.py`) | host, four clones at the head | H0 clean; **H1 to H24 CAUGHT, 24 of 24 on CPython 3.12.3 and on 3.14.7**; escapes H5 19, H15 25, H16 34, H22 11, H23 9 (item 2 explains H22 and H23), each clone restored (`hook-mutants-*.log`) |
| the clean proof and the 34 hook plants (`pin_subset.py hook`) | host, a clone at the head | 35 of 35 `[ok]` on CPython 3.12.3 and 3.14.7 (`hook-subset-head-*.log`) |
| the 17 inherited-environment and 5 new controls (`store_subset.py`) | host, the head; and from a stack cloned with `--reference` | 22 of 22 `[ok]` each way (`c4-store-subset*.log`) |
| the round-14 mutants (`store_mutants.py`) | host, a clone at the head | M0 0 of 22; M1 (no hash compared) 2 escape, the forged tree and the forged commit; M2 (no `core.fsmonitor=false`) 1 escapes, the superproject (`store-mutants-head.log`) |
| R585-12's `forge_probe.py`, R584-11's `model_routes.sh`, R585-12's superproject probe (`super_fsmonitor.sh`) | host, clones at the head (and `8aaa2da7`) | as in items 1 and 2 (`forge-probe-head.txt`, `model-routes-head.txt`, `super-fsmonitor.txt`) |
| every entry point (`entrypoints14.py`) | host, a full clone at the head | 17 × 7 states, 119 of 119 refused (`entrypoints14.log`) |
| the walk against `ls-tree -r -t` (`tree_equiv.py`) | host, the head | 89 entries, 11 trees, equal on CPython 3.12.3 and 3.14.7 (`tree-equiv-head.txt`) |
| `ctrl_build.py --stack-pin`; `git fsck --full` of the lane's submodule | host, the lane | `tsn-c-stack at 405dc683…`, rc 0; fsck rc 0 |

Not run: act (no workflow, act manifest or CI file changes this round; round 13's act self-test stands for those files) and the stack's own CMake suite with `ctest` as a separate step (the boundary step above runs the stack's own boundary gate, with gcc and clang, as one of its builders). Hosted CI cannot run: the head is not pushed.


### Open risks and questions (round 14)

1. **"By name"** is read as naming the forged object by its place and id (above). If the manager wants the edited file named too, that needs the checkout's own tree ids computed from disk, a larger change.
2. **Git 2.36 or later** reads `core.fsmonitor=false` as off. Earlier Git took the setting as a hook path, and would start a program named `false`; the hosted runner's Git and this host's (2.56.0) are well past it.
3. **Dev moved** to `c6bd08c6` (PR #707, gPTP; 16 commits after `c20c85bd`). This round merges nothing. `git merge-tree` of the head with it conflicts only in the generated submodule diagram (`docs/diagrams/submodule_boundaries.{drawio,png}`, `PNG_MANIFEST.json`), which its generator remakes.
4. **The self-review above**: the evidence scripts that forge objects must never run in a hard-linked clone; the published `entrypoints14.py` replaces files.
5. **Carried:** `check_rtl_source_lists.py --selftest` fails 2 of 50 under `MAKEFLAGS=w`, as at dev; `firmware-unit`'s headroom stays #716's; R584-9-S1 stays optional; R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's wording go to #495.
