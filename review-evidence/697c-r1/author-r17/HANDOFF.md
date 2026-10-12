# HANDOFF — lane 697c, [A583]

Issue: [kebag-logic/milan-fpga#697](https://github.com/kebag-logic/milan-fpga/issues/697), assignment comments 6091228902 (round 1), 6092628778 (round 2), 6093389868 (round 2b), 6094873968 (round 3), 6096148471 (round 4), 6097800045 (round 5), 6102039501 (round 6), 6104711137 (round 7), 6105928035 (round 8), 6107732413 (round 9), 6112358746 (round 10), 6113306444 (round 11), 6114400461 (round 12), 6116488747 (round 13), 6117713386 (round 14), 6118625227 (round 15), 6119960001 (round 16) and 6121496568 (round 17).
Branch: `697-consume` from dev `8b61b70902f3ebf118e56967277e2686731081bd`, pushed as PR #705; PR #705 shows round 16's head `516a69be`.
Head: `5b4ea55160c5ee34263e24140f960c4f03d923bc` (round 17: `6e88cfb6` on `516a69be`, PR #705's head, then a merge of dev `c6bd08c6`; not pushed).
Status: round 17 REVIEW READY at `5b4ea5516`, comment [6122601380](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6122601380) (its text: `round17/review-ready-round17.md`) (one parser reads both repositories' configuration keys; the superproject's promisor, transport and fsmonitor keys refused by section and variable whatever their subsection; dev `c6bd08c6` merged, images identical to its; see [Round 17](#round-17)); round 16 REVIEW READY at `516a69be9`, comment [6120798872](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6120798872) (its text: `round16/review-ready-round16.md`) (the superproject's own configuration may not name a promisor remote, its transport or an fsmonitor, each refused by name before the gitlink is read; see [Round 16](#round-16)); round 15 REVIEW READY at `44eef11f8`, comment [6119366539](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119366539) (its text: `round15/review-ready-round15.md`) (the stack's own configuration held to an allowlist of Git's own bookkeeping, the configuration guarantee; `GIT_NO_LAZY_FETCH=1`; see [Round 15](#round-15)); round 14 REVIEW READY at `a8fe548a0`, comment [6118316100](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118316100) (its text: `round14/review-ready-round14.md`) (every object the proof reads hashed against its id; `core.fsmonitor=false`; the alternates control; see [Round 14](#round-14)); round 13 REVIEW READY at `8aaa2da74`, comment [6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531) (its text: `round13/review-ready-round13.md`) (pin `405dc683`, dev `c20c85bd` merged, F-INT's plants retargeted, images identical to dev's; see [Round 13](HANDOFF-rounds-11-13.md#round-13)); round 12 STOP at `adb936049` (item 1, the dev merge; items 2 and 3 done), comment [6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316) (its text: `round12/stop-round12.md`) (see [Round 12](HANDOFF-rounds-11-13.md#round-12)); round 11 REVIEW READY at `aca5e8afc`, comment [6114209149](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114209149) (its text: `round11/review-ready-round11.md`) (see [Round 11](HANDOFF-rounds-11-13.md#round-11)); round 10 REVIEW READY at `be607527e`, comment [6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) (its text: `round10/review-ready-round10.md`) (see [Round 10](HANDOFF-rounds-7-10.md#round-10)); round 9 REVIEW READY at `feed95bbb`, comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179) (see [Round 9](HANDOFF-rounds-7-10.md#round-9)); round 8 REVIEW READY at `4cab445aa`, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`) (see [Round 8](HANDOFF-rounds-7-10.md#round-8)); round 7 REVIEW READY at `8436dfc0b`, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (see [Round 7](HANDOFF-rounds-7-10.md#round-7)); round 6 REVIEW READY at `5b4f6fbeb`, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`) (see [Round 6](HANDOFF-rounds-2-6.md#round-6)); round 5 REVIEW READY at `92b5be188`, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (see [Round 5](HANDOFF-rounds-2-6.md#round-5)); round 4's REVIEW READY was comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937); round 3's was comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057), round 2b's 6094033396, round 2's 6093383132. Round 1: TAKEN 6091267846, REVIEW READY 6092168627; the pin was confirmed in 6092176555.
PR body: `PR-BODY.md` in this directory (round 2 to 17 sections added, round 5's residue, round 14's R585-12-RS1 to RS4 and R584-11-RES-1, round 15's R584-12-RES-1 / R585-13-RES-1, round 16's R585-14-RES-1 / R584-13-RES-1 and R584-13-RES-2, and round 17's R584-14-RES-1, R585-15-RES-1 and R585-15-RES-2 applied; no PR edit made).

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

## Rounds 11 to 13

Moved verbatim to [`HANDOFF-rounds-11-13.md`](HANDOFF-rounds-11-13.md) in round 16 (its sections: [Round 11](HANDOFF-rounds-11-13.md#round-11), [Round 12](HANDOFF-rounds-11-13.md#round-12), [Round 13](HANDOFF-rounds-11-13.md#round-13)), so this file stays under 200 KB.

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


## Round 15

Assignment: #697 comment [6118625227](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118625227), answering [R584-12](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6118601165) and [R585-13](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6118621917), both NEGATIVE at `a8fe548a` on one MINOR (R584-12-F1 = R585-13-F1: a partial-clone promisor transport, named in the stack repository's own configuration, is started by Git while the pin is decided, and the PR body called that class closed). Items:
1. a local configuration allowlist, read through the helper before the first object read, refusing by name every other key;
2. `GIT_NO_LAZY_FETCH=1` in the helper's environment, with the Git versions that honour it recorded, the hosted runner's included;
3. the reviewers' promisor probes refused by name with `RAN=0`; one control per refused key family and a clean allowlisted clone accepted; the 79 pin controls, the environment and object-id controls still hold;
4. README, docstring and PR body state the allowlist as the configuration guarantee; the PR-body sentence that called the class closed is fixed.

Base of the round: `a8fe548a083239efc799a79c540b2be63e9d13e7` (PR #705's head). New commits only, no rebase or amend; not pushed.
Status: REVIEW READY at the head below, posted as #697 comment [6119366539](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119366539) (its text: `round15/review-ready-round15.md`; see [Gates](#gates-at-the-round-15-head)); every item done, R584-12-S1 / R585-13-S2 resolved by item 1, R585-13-S1 and S3 not taken.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `44eef11f8` | Refuse by name, before any object is read, every key of the stack's own configuration outside an allowlist of Git's own bookkeeping, and give Git GIT_NO_LAZY_FETCH, with a standing control for each refused family | the store, environment and configuration controls (scratch `store_subset.py`, 36 of 36 `[ok]`); every pin control with the census and the figure check (R585-13's `run_pin_controls.py` on the worktree: 98 pin controls, 0 misbehaved, census 0, figures 0, 4 of 4 figure controls); pyflakes; `check_py_idiom.py` (every ratchet held, `long module: 10 <= 10`); `docs_check.py` 0; then, committed, `check_em_dash.py --base c20c85bd` 0 findings over 423 added lines |

One-line subject, no body, no trailers, configured identity.

Head: `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` (one commit on `a8fe548a`; `git diff --stat a8fe548a HEAD`: five files under `sw/firmware/ctrl`, 258 insertions, 52 deletions). No firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin changes.

### Item 1: the configuration allowlist

`ctrl_build.configured` (`sw/firmware/ctrl/test/ctrl_build.py:486-509`), called by `stack_pin` (`:525`) right after the checkout is found to be its own and before `rev-parse HEAD` and any object read:
- reads, through the helper, all the configuration Git reads for the proof's commands in the stack's repository: `git config --list --show-scope -z` (each entry `scope NUL key LF value NUL`, section and variable names lower-cased by Git, the same on Git 2.56.0 and 2.43.0);
- accepts a `local` or `worktree` key whose name, with any subsection read as `*`, is in `STACK_CONFIG` (`:199-202`), and the one `command` key the helper itself gives (`HELPER_CONFIG`, `:193`, now also the helper's `-c` argument, `:400`);
- refuses everything else by name and scope, all of it at once and sorted: `REFUSED: tsn-c-stack's repository holds configuration outside the pin proof's allowlist: core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)`. A system or global key cannot occur (the helper's environment reads neither file) and would be refused too.

The allowlist (`STACK_CONFIG`), exactly the assignment's list: `core.repositoryformatversion`, `core.filemode`, `core.bare`, `core.logallrefupdates`, `core.worktree`; `remote.*.url`, `remote.*.fetch`; `branch.*.remote`, `branch.*.merge`; and the submodule bookkeeping Git writes itself: `submodule.active`, `submodule.*.url`, `submodule.*.active`, `submodule.alternatelocation`, `submodule.alternateerrorstrategy`.

What Git actually writes into the stack's own configuration (scratch `init_flows.sh`, `round15/logs/init-flows-git256.txt` and `init-flows-git243.txt`; identical on Git 2.56.0 and on Ubuntu 24.04's 2.43.0):

| How the stack is initialised | Keys written |
|---|---|
| `git submodule update --init` (the workflows' step), `clone --recurse-submodules`, `submodule update --init --reference`, a superproject worktree's `submodule update --init` | the four `core.*`, `core.worktree`, `remote.origin.url`, `remote.origin.fetch` |
| `git clone --reference <repo> --recurse-submodules` of the superproject | the same, and `submodule.alternatelocation=superproject`, `submodule.alternateerrorstrategy=die` |
| the pin controls' clone (`clone --no-hardlinks`), the object-store controls' (`init`, `fetch`) | the four `core.*` (and `remote.origin.*` for the first) |
| the lane's own submodule (an older initialisation) | the above and `branch.main.remote`, `branch.main.merge` |

So every way a gate's stack is made holds only allowlisted keys, and a stack with any other key (a developer's `pull.rebase`, `gc.auto`, an extra remote option) is refused by that key's name until it is removed. `submodule.*.url`, `submodule.*.active` and `submodule.active` are what Git writes when a repository's own submodules are initialised; the stack at the pin has none.

### Item 2: `GIT_NO_LAZY_FETCH=1`

`ctrl_build.py:189-190`: `GIT_ENVIRONMENT` gains `"GIT_NO_LAZY_FETCH": "1"`; the audit hook's judge requires the helper's environment to be `GIT_ENVIRONMENT` key for key, so it now requires the variable too (the 34 hook controls and the census are unchanged and hold).

Which Git honours it:

| Git | Honours `GIT_NO_LAZY_FETCH` | Evidence |
|---|---|---|
| 2.56.0 (this host) | yes | R585-13's `lazy_fetch_env.sh`: the proof's environment and arguments start the transport 2 times, 0 with the variable (`round15/logs/lazy-fetch-env-git256.txt`) |
| Ubuntu 24.04 `1:2.43.0-1ubuntu7.3` (the replica's) | yes, by its `CVE-2024-32465.patch` ("disable lazy-fetching by default in builtin/upload-pack.c, promisor-remote.c") | the same script: 2, then 0 (`lazy-fetch-env-git243.txt`); with the variable Git warns `lazy fetching disabled; some objects may not be available` |
| upstream `v2.45.0` and later | yes | `environment.h` defines `GIT_NO_LAZY_FETCH`; the 2.45.0 release notes list `git --no-lazy-fetch` (`git-tags-no-lazy-fetch.txt`) |
| upstream `v2.43.4`, `v2.44.1` (the CVE-2024-32465 releases; 2.39.4 to 2.42.2 carry the same fix per the 2.43.4 notes) | yes | `promisor-remote.c` reads `GIT_NO_LAZY_FETCH` |
| upstream `v2.43.0`, `v2.44.0` | no | neither file names it |
| the hosted runner | 2.55.0, so yes by version (not executed there: nothing can run on the runner from this lane) | run 38205277457 (2026-10-12, `ubuntu-24.04` image `20261004.327.1`): every job's checkout prints `git version 2.55.0` |

Where a Git does not honour it, the allowlist is the guarantee: mutant M2 below removes the variable and no control escapes, and R584-12's lazy probes start no program on either Git with the allowlist alone (`layer-probe.txt`).

### Item 3: the controls

R584-12's `store_probe.py` and R585-13's `forge_probes.sh`, run unchanged (downloaded from the review-evidence branch, sha256 equal to their manifests) on disposable clones without hard links:

| Probe | At `a8fe548a` | At `44eef11f8` |
|---|---|---|
| R584-12 `lazy_uploadpack_fail` | REFUSED (`Could not read from remote repository`), `RAN=1` | REFUSED `... allowlist: extensions.partialclone (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`, `RAN=0` |
| `lazy_uploadpack_serve` | **ACCEPTED**, `RAN=1` | REFUSED by the same keys, `RAN=0` |
| `lazy_ssh` | REFUSED, `RAN=2` | REFUSED `... core.sshcommand (local), extensions.partialclone (local), remote.origin.promisor (local)`, `RAN=0` |
| `lazy_toctou` | **ACCEPTED**, `RAN=1`, then `src/adp.c planted: True` | REFUSED, `RAN=0`, `planted: False` |
| `stack_fsmonitor` | REFUSED `src/adp.c` | REFUSED `... allowlist: core.fsmonitor (local)` |
| the other 15 (clean, edit, forged objects, corrupt, missing, super_fsmonitor, core_worktree) | as R584-12 reports | unchanged verdicts, every `RAN=0` |
| R585-13 P13 (partial clone, `core.sshCommand` a recorder) | exit 2, recorder runs **2** | exit 2, refused by the three keys, runs **0** |
| P14 (the recorder serves the object and edits later) | **exit 0**, runs 2, later edit: **edited** | exit 2, runs 0, later edit: none |
| P0 to P12 | as R585-13 reports | unchanged (P11 now refused by `core.fsmonitor (local)`) |

Run at the head on CPython 3.14 and 3.12.3 (host Git 2.56.0), and in the Ubuntu 24.04 replica (Git 2.43.0, CPython 3.12.3): every lazy probe `RAN=0` (`store-probe-head-py314.txt`, `store-probe-head-py312.txt`, `store-probe-head-git243.txt`; `a8fe548a` on 2.43.0: serve and toctou ACCEPTED, `RAN=1`, `store-probe-old-git243.txt`). With one layer removed at a time (scratch `layer_probe.sh`): the allowlist alone and the variable alone each give `RAN=0` on both Gits.

The standing controls (`sw/firmware/ctrl/test/ctrl_pin_store.py`), after the 17 inherited-environment ones; 14 new, 98 pin controls in all:

| Control | Family | Verdict at the head |
|---|---|---|
| a key of each family of the allowlist, the pinned clone (`allowlisted`, `:183-199`, which refuses its own setup if a family is missing) | the allowlist | `accepted 405dc683…` |
| a partial clone whose promisor remote's upload-pack is a program, the pinned `src/` tree's object missing | promisor and transport (R584-12's lazy upload-pack) | `... extensions.partialclone (local), remote.origin.promisor (local), remote.origin.uploadpack (local)` |
| a partial clone reached over ssh by a program (`core.sshCommand`), the object missing | promisor and transport (R584-12's lazy ssh, R585-13's P13) | `... core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)` |
| `extensions.partialClone` alone, the object missing | `extensions.partialClone` | `... extensions.partialclone (local)` |
| `remote.<name>.promisor` alone, the object missing | `remote.*.promisor` | `... remote.origin.promisor (local)` |
| a program as `remote.<name>.uploadpack` | `remote.*.uploadpack` | `... remote.origin.uploadpack (local)` |
| a program as `core.sshCommand` | `core.sshCommand` | `... core.sshcommand (local)` |
| (existing) a program as `core.fsmonitor`, a source edited | `core.fsmonitor` | now `... core.fsmonitor (local)` (was refused by `src/adp.c`) |
| a directory of programs as `core.hooksPath` | `core.hooksPath` | `... core.hookspath (local)` |
| (existing, of the 79, `ctrl_pin.py`) a clean filter through attributes | filter | now `... filter.pin-control.clean (local)` (was refused by `src/adp.c`) |
| a program as `credential.helper` | credential | `... credential.helper (local)` |
| a program as each other key Git starts one for (`HELPERS`, `:209-210`) | other helpers | `... core.alternaterefscommand (local), core.askpass (local), core.editor (local), core.pager (local), diff.pin-control.textconv (local), gpg.program (local), uploadpack.packobjectshook (local)` |
| an included file (`include.path`) naming a program as `core.fsmonitor` | include | `... core.fsmonitor (local), include.path (local)` |
| a work tree's own configuration (`extensions.worktreeConfig`) naming one | the work tree's scope | `... core.fsmonitor (worktree), extensions.worktreeconfig (local)` |
| a key no Git defines, naming a program | anything a later Git adds | `... pin-control.program (local)` |
| a source's line endings made CRLF under the clone's `text` attribute, which Git converts back into the pinned blob (`converted`, `:119-130`) | attributes (no configuration) | `tsn-c-stack differs from the pinned 405dc683: src/adp.c` |

Each needle is the refusal's whole key list, so a key the allowlist let through would change it and the control would escape; every control also fails if a recorder ran.

Two existing controls changed their verdict's words, not their outcome, because the allowlist now refuses their state first:
- the stack's `core.fsmonitor` control is now refused by the key; it could not fail before (R584-12-S1, R585-13-S2), and it escapes under M1;
- the clean-filter control (one of the 79) is now refused by the filter's key. The property it held, that no file is hashed through Git, keeps a standing control: the line-ending conversion above needs no configuration, and it is the one control that escapes under M6.

The `GIT_ATTR_SOURCE` environment control (`ctrl_pin_env.py:189-198`) now gives its filter through `GIT_CONFIG_COUNT` with the attribute, instead of in the clone's own configuration, so its verdict stays the clone's own edit (`differs from the pinned`), and the every-variable control's pinned clone stays accepted.

Mutants of the head (scratch `config_mutants.py`, each on a disposable clone, then `pin_subset15.py`: the clean clone, the clean-filter control, the 17 inherited-environment and the 19 store controls, 38 in all; `round15/logs/config-mutants-a.log`, `-b.log`):

| Mutant | Escaped of 38 |
|---|---|
| M0 none | 0 |
| M1 the allowlist not checked (`configured(stack)` removed) | 14: every planted-key control and the clean-filter control (the lazy ones refused `cannot read the pinned tree`, Git honouring the variable) |
| M2 no `GIT_NO_LAZY_FETCH` | 0: the allowlist alone holds |
| M3 neither | 14, the two transport controls with `Git ran a program a repository's own configuration names` |
| M4 the allowlist reads `--local` only | 2: the include and the work-tree controls (their keys go unseen) |
| M5 the allowlist by section only | 10 |
| M6 each file hashed through Git (`git hash-object`, with its attributes) | 1: the line-ending conversion control (accepted) |
| M7 the allowlist checked after the objects are read | 4: the four controls with a missing object |

Every pin control together (R585-13's `run_pin_controls.py` at the worktree that became `44eef11f`): 98 pin controls, 0 misbehaved; census 0 findings; figure findings 0; figure controls 4, 0 misbehaved (`pin-controls-wt-2.log`).

### Item 4: the texts

- `sw/firmware/ctrl/README.md:170` (the environment with `GIT_NO_LAZY_FETCH=1`), `:175-182` (the allowlist as the configuration guarantee, the keys, the refused families, the variable and the Git versions), `:216` (98 pin controls), `:220` (the clean filter refused by its key), `:237-249` (the nineteen store controls).
- `ctrl_build.py:183-204` (the environment's and the allowlist's comments), `:487-494` (`configured`'s docstring), `:513-519` (`stack_pin`'s).
- `ctrl_pin.py:29` (THE HOOK's environment), `:59-68` (THE THREAT MODEL: the allowlist is the configuration guarantee), `:107-110` and `:133-134` (THE CONTROLS), `pin_controls`' docstring; `:201` the census's vocabulary gains `rpartition`.
- `ctrl_pin_store.py:1-50` (the module docstring), `ctrl_pin_env.py:25-30`.
- `PR-BODY.md`: the round-14 Status bullet and the Contents line no longer say no repository's own configuration starts a program; the Status, Contents and a Round 15 section state the allowlist as the guarantee.

### Residue and suggestions

- R584-12-RES-1 / R585-13-RES-1 applied as given: the five links of the fourth reference bullet name `a8fe548a…` (R585-13 asked the first only; R584-12 all five, which covers both). The control firmware page changes again in this round; its link can move to this round's head once that is published.
- R584-12-S1 / R585-13-S2 (the stack's `core.fsmonitor` control cannot fail): resolved by item 1; it escapes under M1.
- R585-13-S1 (a control forging the root tree) and R585-13-S3 (the read-failure wording): optional, not taken; R584-12's and R585-13's probes refuse a forged root tree at the head.

### The images

Every RV32 image at every shipped shape, linked at the head with the pinned SDK and round 1's runtime archives (scratch `images6.sh`, unchanged, 93 s on four CPUs), against dev `c20c85bd`'s manifest from round 13. The manifests are byte-equal (sha256 `8b1292dbe318603b3ed2354c0b58c2721ab3f27094589153d946af0783b39095`, as dev's and round 14's head); `ctrl_image.py` printed `tsn-c-stack at 405dc683…` first.

| Image (shape) | dev `c20c85bd` sha256 | head `44eef11f` sha256 | |
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

### Gates at the round-15 head

Every gate the change touches ran at `44eef11f8ee0d0f980eb68355c930efe2cce8cd8`, each in a fresh clone that shares no file with the lane (scratch `mkclone15.sh`: `clone --no-hardlinks`, each submodule fetched over `file://` from the lane's checkout). The replica is the runner's Ubuntu 24.04 (CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0 static, cmake 3.28, clang 18, Git 2.43.0, `MAKEFLAGS=w`), four CPUs each, the pinned RV32 SDK, the pinned Verilator 5.050; the three ran at once. Logs: `round15/logs/` in this directory.

| Gate | Where | Result |
|---|---|---|
| `firmware-boundary`'s step, `ctrl_boundary.py --require-rv32 --selftest --without verilator` (`boundaryjob.sh`) | replica, CPUs 64-67 | **PASS in 693 s**: 2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own), 0 findings, **105 boundary, 98 pin and 4 figure controls, 0 misbehaved** (`bjob-head.log`; the figure controls read the README's 98) |
| `firmware-verilator`'s step, `--only verilator` (`vgate8.sh`) | replica, CPUs 72-75 | **PASS in 495 s**: 829 of 930, 0 findings, **6, 98 and 4, 0 misbehaved**; the bench (61 s), the MAAP differential's self-test (151 s) and the AECP wire comparison `--every` (205 s) each exit 0 (`vjob-head.log`) |
| `firmware-unit`'s steps (`unitjob.sh`) | replica, CPUs 68-71 | **every step rc 0, 2100 s in all** (`ujob-head.outer`): `tally_selftest.py` 3 s; `fw_rv32_selftest.py --require-rv32` 7 s; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` 1788 s, `tsn-c-stack at 405dc683…`, **`mutants: 506 of 506 caught`**, 915 verdict lines `[ok]`, every one equal to round 14's once its time is dropped, `test_ctrl_firmware: PASS` (its log, 348900 bytes, is kept out of this directory: sha256 `1bc0bede4935e2ecca14ceb0dee180f4e5400ef847817746658d264810b26f5e`); `test_ctrl_nvm.py` 77 s, `OK across 5 shape(s), 435 tests`; `fw_coverage.py --selftest` `29 of 29 planted cases`; `fw_coverage.py --check` 225 s, `firmware coverage: PASS (30 files)`, every row 100 % and equal to round 14's |
| the 35 RV32 images (`images6.sh`) | host, the pinned SDK, round 1's runtime archives | 35 of 35 identical to dev `c20c85bd` (above) |
| the docs job's 54 commands (`docsjob.sh`) | host, a clone with the job's three submodules, CPython 3.12.3 with PyYAML and the pinned renderer, `MAKEFLAGS=w` | 53 of 54 rc 0 in 147 s (`docsjob-head.log`, `docs-head/`): `check_em_dash.py --base c20c85bd` 0 findings over 423 added lines in 12 pages; `docs_check.py` 0 findings across 203 pages; `check_py_idiom.py` every ratchet held (`long module: 10 <= 10`, `over-long line: 0 <= 0`); `check_hygiene.py --check` PASS; `ci_events.py --check` (1974 items) and `--selftest`; `gen_toc.py --check` and `--verify-anchors`. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50 under `MAKEFLAGS=w`, as at dev; 50 of 50 without it (`srclists-nomf-head.log`) |
| the hook-rule campaign (`hook_mutants.py`, unchanged) | host, four clones at the head | H0 clean; **H1 to H24 CAUGHT, 24 of 24 on CPython 3.12.3 and on 3.14** (`hook-mutants-*.log`). Escapes equal round 14's but H22 30 (11) and H23 13 (9): H22 lets the host's global configuration reach Git, whose keys (`credential.*.helper`, `user.*`) the allowlist refuses by scope, the clean proof included; under H23 the four controls whose variables give Git command-line keys (`core.fsmonitor`, a clean filter) are refused by those keys. H0 is the clean proof, the 34 hook plants and the 17 inherited-environment controls, 0 escaped, on both interpreters |
| the configuration, environment and store controls (`pin_subset15.py`) and the round-15 mutants (`config_mutants.py`) | host, a disposable clone | 38 of 38 `[ok]`; M0 to M7 as in item 3 (`config-mutants-a.log`, `-b.log`) |
| every pin control with the census and the figure check (R585-13's `run_pin_controls.py`) | host, CPython 3.14 | 98, 0 misbehaved; census 0; figures 0; 4 of 4 figure controls (`pin-controls-wt-2.log`) |
| R584-12's `store_probe.py`, R585-13's `forge_probes.sh` and `lazy_fetch_env.sh` | host (Git 2.56.0; CPython 3.14 and 3.12.3) and the replica (Git 2.43.0) | as in items 2 and 3 |
| every entry point (`entrypoints15.py`) | host, a full clone at the head | 17 entry points × 9 states (round 14's seven, the clean filter now refused by `filter.pc.clean (local)`, and two new: a partial clone over an ssh program with the pinned `include/` tree missing, a line-ending conversion of `include/adp.h`): **153 of 153 refused** by name before any build, the recorder never run (`entrypoints15.log`) |
| `ctrl_build.py --stack-pin`; `git fsck --full` of the lane's submodule | host, the lane | `tsn-c-stack at 405dc683…`, rc 0; fsck rc 0 (`lane-stack-fsck.txt`) |

Not run: act (no workflow, act manifest or CI file changes this round; round 13's act self-test stands for those files) and hosted CI (the head is not pushed).

Lane hygiene: the lane's checkout has 0 status entries, ignored files included. Bytecode caches left in it by round 14's runs (all from before this session) were removed; this round ran every probe, mutant and gate in scratch clones.

### Open risks and questions (round 15)

1. **The superproject's own configuration** is not under the allowlist: the assignment names the stack's, and `actions/checkout` writes keys into the superproject's (`http.<url>.extraheader`) that an allowlist would refuse. The proof reads only the superproject's index (`ls-files --stage`), with `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1`.
2. **A stack with any other key** in its own configuration (a developer's `pull.rebase`, `gc.auto`, an extra remote option) is refused by that key's name until it is removed. Every way the gates' stacks are made writes only allowlisted keys (item 1).
3. **The hosted runner's Git** (2.55.0) is read from run 38205277457's checkout logs; nothing was executed on the runner.
4. **Dev** is at `c6bd08c6` or later; this round merges nothing (round 14's note stands).
5. **Carried:** `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, as at dev; `firmware-unit`'s headroom (#716); R584-9-S1, R585-13-S1 and S3 optional; R584-8-RES-1, R585-8-RS1, R584-7-RES1 / R585-7-RS1 and R585-9's wording go to #495.

## Round 16

Assignment: #697 comment [6119960001](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119960001), answering [R585-14](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6119950198) (NEGATIVE at `44eef11f` on one MINOR, R585-14-F1: the superproject's own configuration, a partial clone with a promisor and a sparse index, makes an upstream Git older than 2.45 without the CVE-2024-32465 fix start a program while the gitlink is read, and the texts said that configuration was held) and [R584-13](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6119604125) (POSITIVE at `44eef11f`, two PR-body residue items). Option (a). Items:
1. before `stack_gitlink` reads the superproject's index, read its local and work-tree configuration through the helper and refuse by name `extensions.partialClone`, `remote.*.promisor`, `remote.*.partialclonefilter`, `remote.*.uploadpack`, `core.sshCommand` and `core.fsmonitor` (the last kept as a control); its other keys untouched, `actions/checkout`'s `http.<url>.extraheader` and the submodule entries passing;
2. R585-14's two probes end in the named refusal with `RAN=0` whatever the Git version; a standing control `[ok]` at the head and `ESCAPED` under its mutant; the 98 pin controls still hold;
3. `README.md:180-182`, `ctrl_build.py:191-192`, `ctrl_pin_store.py:44-48` and the PR body state what is held, for the stack's configuration (the allowlist) and the superproject's (these keys);
4. R584-13's RES-1 and RES-2 and R585-14's residue in PR-BODY.md.

Base of the round: `44eef11f8ee0d0f980eb68355c930efe2cce8cd8` (PR #705's head). New commits only, no rebase or amend; not pushed.
Status: REVIEW READY at the head below, posted as #697 comment [6120798872](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6120798872) (its text: `round16/review-ready-round16.md`; see [Gates](#gates-at-the-round-16-head)); every item done; R585-14-S1 to S3 and R584-13-S1 not taken.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `516a69be9` | Refuse by name, before the gitlink is read from its index, a promisor remote, its transport and an fsmonitor in the superproject's own configuration, with standing controls for a sparse partial-clone superproject and for actions/checkout's keys | the configuration, environment and store controls (scratch `pin_subset16.py`, 42 of 42 `[ok]` on Git 2.56.0 and on upstream 2.43.0); every pin control with the census and the figure check (R585-14's `r585_14_pin_controls.py` and `r585_14_census_figures.py` on the worktree: 102 pin controls, 0 misbehaved, census 0, figures 0, 4 of 4 figure controls); R585-14's two probes on the worktree (`RAN=0`, both Gits); pyflakes; `check_py_idiom.py` (every ratchet held, `long function: 9 <= 9`, `long module: 10 <= 10`); `docs_check.py` 0; `check_doc_style.py` OK; then, committed, `check_em_dash.py --base c20c85bd` 0 findings over 431 added lines, `gen_toc.py --check` and `--verify-anchors` OK |

One-line subject, no body, no trailers, configured identity.

Head: `516a69be9afba02670e37874294bd1f45ccb9316` (one commit on `44eef11f`; `git diff --stat 44eef11f HEAD`: four files under `sw/firmware/ctrl`, 194 insertions, 41 deletions). No firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin changes.

### Item 1: the superproject's keys

- `ctrl_build.configuration` (`sw/firmware/ctrl/test/ctrl_build.py:502-518`): the listing round 15's `configured` made, now a function of its own that both checks share: `git config --list --show-scope -z` through the helper, each entry as (scope, name with any subsection read as `*`, key, value). An included file's keys come in the including file's scope; listing reads no index and no object.
- `ctrl_build.configured` (`:521-532`): the stack's allowlist, unchanged in what it judges (round 15's 13 configuration controls and the allowlisted clone hold, and R585-14's stack probes print what its receipts print).
- `ctrl_build.superproject_configured` (`:535-545`), called by `stack_gitlink` (`:425`) before `ls-files --stage` (`:426`): refuses every entry whose name is in `SUPERPROJECT_REFUSED` (`:207-215`), in any scope but the helper's own `command`-scope `core.fsmonitor=false`, all at once, sorted, by name and scope (`SUPERPROJECT_KEYS`, `:216-217`): `REFUSED: the superproject's repository holds configuration that has Git start a program or fetch while the gitlink is read: extensions.partialclone (local), remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`. Since `GIT_ENVIRONMENT` reads no system or global file, the scopes that can occur are `local` (an included file's keys among them), `worktree` and the helper's `command`.
- `SUPERPROJECT_REFUSED`: `extensions.partialclone`, `remote.*.promisor`, `remote.*.partialclonefilter`, `remote.*.uploadpack`, `core.sshcommand`, `core.fsmonitor`, exactly the assignment's list. A promisor remote exists only through the first two, so without them Git fetches nothing however a Git version treats `GIT_NO_LAZY_FETCH`.
- Every caller of `stack_gitlink` gets the check: `stack_pin` (pin not given), `ctrl_pin.pin_controls`, and the controls' own `gitlink` read. The lane's and every scratch clone's superproject configuration hold none of the six keys (checked with `git config --list --show-scope`), and no workflow checks the superproject out with a filter or a sparse checkout (`actions/checkout@v4` without `filter:` or `sparse-checkout:`).
- What the superproject's other keys do while the gitlink is read (scratch `probes/super_other_keys.py`, `round16/logs/super-other-keys-git256.txt`, `-git243.txt`): 28 keys that name a program or reach one (`core.hooksPath` with five hooks, `credential.helper`, `core.askPass`, `core.pager`, `core.editor`, `sequence.editor`, a `textconv`, `diff.external`, a merge driver, a filter's `clean`, `smudge` and `process` with `core.attributesFile`, `gpg.program`, `core.alternateRefsCommand`, `uploadpack.packObjectsHook`, `core.gitProxy`, `protocol.ext.allow=always` with an `ext::` remote URL and an `ext::` `insteadOf`, `remote.<name>.vcs`, `submodule.recurse`, `core.untrackedCache`, `core.splitIndex`, `index.skipHash`, `gc.auto`, `maintenance.auto`, an `include.path` naming a pager), each naming the recorder: a plain superproject is read as `405dc683…`, a sparse one lacking the tree is refused `third_party/tsn-c-stack is not one stage-0 gitlink`, `RAN=0` in both, on Git 2.56.0 and on upstream 2.43.0. `ls-files` reads only Git's default configuration and recurses into submodules only when asked (`builtin/ls-files.c` at v2.43.0).

### Item 2: the controls

R585-14's packet fetched from `697c-review-evidence` (`52047a44`), its scripts run unchanged: all eight match the packet's `MANIFEST.sha256`; 13 of its receipts do not (their published text differs from the hashes listed), and they were read only as the reference outputs compared below (`round16/logs/r585-14-manifest-check.txt`). Upstream Git 2.43.0 built under scratch from `git-2.43.0.tar.xz` (kernel.org, sha256 `5446603e73d911781d259e565750dcd277a42836c8e392cac91cf137aa9b76ec`, the reviewer's receipt's; `NO_CURL`, `NO_PERL`, `NO_GETTEXT`, `-std=gnu17`). Logs: `round16/logs/`.

| Probe | `44eef11f`, Git 2.56.0 | `44eef11f`, upstream 2.43.0 | `516a69be`, Git 2.56.0 | `516a69be`, upstream 2.43.0 |
|---|---|---|---|---|
| `r585_14_superproject_sparse_gitlink_serve.sh` | REFUSED `not one stage-0 gitlink`, `RAN=0` | **`gitlink 405dc683…`, `RAN=1`** | REFUSED by `remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`, `RAN=0` | the same, `RAN=0` |
| `r585_14_superproject_sparse_gitlink.sh` | REFUSED, `RAN=0` | REFUSED, **`RAN=1`** | REFUSED by the same keys, `RAN=0` | the same, `RAN=0` |
| `r585_14_superproject_sparse.sh` | | | REFUSED by the same keys, `RAN=0` | the same, `RAN=0` |
| `r585_14_superproject.sh` | | | REFUSED by `core.fsmonitor (local), core.sshcommand (local), extensions.partialclone (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`, `RAN=0` | the same, `RAN=0` |
| `r585_14_probes.sh` (the stack's 17 states) | | | byte-identical to R585-14's receipt at `44eef11f` once paths are normalised | the same |

(A partial clone made by `git clone --filter` writes `remote.<name>.promisor` and `remote.<name>.partialclonefilter` and no `extensions.partialClone`; R585-14's probes are refused by those keys.)

The standing controls of the superproject (`sw/firmware/ctrl/test/ctrl_pin_store.py:290-318`, `superproject_controls`, run by `store_arms` at `:375`), each reading the gitlink as the proof reads the checkout's (`stack_gitlink`), each failing if any recorder ran:

| Control | Built by | Verdict at the head |
|---|---|---|
| (kept) the superproject's own configuration naming a recorder as `core.fsmonitor` | `superproject` (`:154-160`) | `... core.fsmonitor (local)` (was `accepted 405dc683…`, held by the helper's setting) |
| R585-14's shape: a sparse index whose sparse directory `third_party/` holds the gitlink without its tree (removed from the store, every object loose, no pack), a partial clone of an origin beside it, its upload-pack a recorder that then serves the tree (`SERVER`, `:85`) | `sparse_superproject` (`:182-208`), `served` (`:211-216`) | `... extensions.partialclone (local), remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)` |
| the same, the promisor remote reached over ssh by a recorder (`core.sshCommand`) | `sparse_superproject` | `... core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)` |
| an included file (`include.path`) and the work tree's own configuration (`extensions.worktreeConfig`) each naming a recorder as `core.fsmonitor` | `superproject_included` (`:174-179`) | `... core.fsmonitor (local), core.fsmonitor (worktree)` |
| the configuration `actions/checkout` and `git submodule update --init` leave: `remote.origin.url` and `fetch`, `gc.auto=0`, `http.https://github.com/.extraheader`, `submodule.third_party/tsn-c-stack.url` and `active` | `checked_out` (`:163-171`) | `accepted 405dc683…` |

`sparse_superproject` refuses its own setup unless the index holds `third_party/` as a sparse directory entry and the store holds no pack (so the tree is absent), or the control would prove nothing. Each needle is the refusal's whole key list. 102 pin controls in all, 0 misbehaved (`pin-controls-wt2.log`; and in both replica jobs).

Mutants of the head (scratch `super_mutants.py`, each alone on a disposable clone, then R585-14's `r585_14_pin_controls.py`, unchanged: all 102 pin controls; `super-mutants-git256.log`, `super-mutants-git243.log`):

| Mutant | Escaped of 102, Git 2.56.0 | Escaped of 102, upstream 2.43.0 |
|---|---|---|
| N0 none | 0 | 0 |
| N1 the superproject check not called | 4: the `core.fsmonitor` and include/work-tree controls accepted; both sparse controls `not one stage-0 gitlink` | 4: the same two accepted; both sparse controls **`Git ran a program a repository's own configuration names`** |
| N2 the check after the index is read | 0 (Git honours `GIT_NO_LAZY_FETCH`, so nothing is fetched, then the keys are refused) | **2**: both sparse controls, Git running the recorder |
| N3 the superproject's `local` scope only | 1: the include/work-tree control | 1 |
| N4 `extensions.partialclone` not refused | 2 | 2 |
| N4 `remote.*.promisor` not refused | 2 | 2 |
| N4 `remote.*.partialclonefilter` not refused | 1 | 1 |
| N4 `remote.*.uploadpack` not refused | 1 | 1 |
| N4 `core.sshcommand` not refused | 1 | 1 |
| N4 `core.fsmonitor` not refused | 2 | 2 |
| N5 the helper's own `command` setting refused in the superproject | the run fails before its first control: the pin controls' own gitlink read is refused (`core.fsmonitor (command)`) | the same |
| N6 no `HELPER_CONFIG` (`-c core.fsmonitor=false`) | 0: defence in depth | 0 |
| N7 no `GIT_NO_LAZY_FETCH` | 0: defence in depth | 0 |
| N8 neither the check nor `GIT_NO_LAZY_FETCH` | 4, both sparse controls with Git running the recorder | 4, as N1 |
| N9 neither the check nor `HELPER_CONFIG` | 4, the `core.fsmonitor` and include/work-tree controls with Git running the recorder | 4 |

So the standing control asked for holds on every Git: R585-14's sparse shape is `[ok]` at the head and `ESCAPED` without the check, on 2.56.0 by its words and on upstream 2.43.0 by the recorder running. `HELPER_CONFIG` no longer has a control that fails without it alone: the superproject's `core.fsmonitor` is now refused by name first, as the stack's was in round 15; it and `GIT_NO_LAZY_FETCH` are defence in depth, as R585-14-S2 notes (not taken).

### Item 3: the texts

- `sw/firmware/ctrl/README.md:179-186`: the allowlist is the guarantee for the stack; the superproject's configuration is listed the same way and the six keys refused by name, in its own file, an included one or its work tree's; those keys are the guarantee for the superproject (without a promisor remote Git fetches nothing; no fsmonitor is started); its other keys are not judged (`actions/checkout`'s `http.<url>.extraheader`, the submodule entries); `core.fsmonitor=false` is defence in depth behind both; where a Git does not honour `GIT_NO_LAZY_FETCH` (upstream 2.43.0, 2.44.0) the allowlist and the refused keys are the guarantee. `:220` 102 pin controls; `:241` twenty-three store and configuration controls; `:246-250` the five superproject controls (replacing the sentence that said the superproject's `core.fsmonitor` was accepted).
- `ctrl_build.py:182-189` (`GIT_ENVIRONMENT`'s comment), `:192-195` (`HELPER_CONFIG`: defence in depth behind both checks; was `:191-192`, "holds the superproject's configuration"), `:207-217` (`SUPERPROJECT_REFUSED`, `SUPERPROJECT_KEYS`), `:410` (the helper's docstring), `:421-423` (`stack_gitlink`), `:503-506`, `:522-527`, `:536-541` (the three docstrings).
- `ctrl_pin_store.py:24-65` (the module docstring; was `:44-48`, "core.fsmonitor=false, which holds the superproject's own configuration").
- `ctrl_pin.py:62-70` (THE THREAT MODEL: the superproject's keys), `:136` (THE CONTROLS); the module stays at 1000 lines (the idiom gate's `long module` limit).

### Item 4: the PR body's residue

- R585-14-RES-1 = R584-13-RES-1: the five links of the fourth reference bullet name `516a69be9afba02670e37874294bd1f45ccb9316`, the head the PR would merge at (the control firmware page changed in rounds 15 and 16; the other four moved with it for uniformity, as R584-13 allows). They resolve once the head is pushed.
- R584-13-RES-2: round 15's row 2 now reads "the CVE-2024-32465 maintenance releases read it too (checked: `v2.39.4`, `v2.42.2`, `v2.43.4`, `v2.44.1`)".
- Status, Contents, a Round 16 section, the round-14 row 2 and round-15 open item (a) (a note that round 16 refuses the keys), How to validate (102 pin controls; the five superproject controls' words) and Known limitations (the round-15 superproject sentence replaced by round 16's) state what is held.
- Not taken (optional): R585-14-S1 (compare the configuration controls' words for equality; every refusal names exactly its keys at the head), S2 (a control for each defence-in-depth layer alone), S3 (the words of a refusal when the stack's configuration cannot be parsed), R584-13-S1 (the file-system keys Git writes on other hosts), and the retained R585-13-S1 and S3.

### The images

Every RV32 image at every shipped shape, linked at the head with the pinned SDK and round 1's runtime archives (scratch `images6.sh`, unchanged, 95 s on four CPUs), against dev `c20c85bd`'s manifest from round 13. The manifests are byte-equal (sha256 `8b1292dbe318603b3ed2354c0b58c2721ab3f27094589153d946af0783b39095`, as dev's and round 15's head); `ctrl_image.py` printed `tsn-c-stack at 405dc683…` first.

| Image (shape) | dev `c20c85bd` sha256 | head `516a69be` sha256 | |
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

### Gates at the round-16 head

Every gate the change touches ran at `516a69be9afba02670e37874294bd1f45ccb9316`, each in a fresh clone that shares no file with the lane (scratch `mkclone16.sh`, round 15's: `clone --no-hardlinks`, each submodule fetched over `file://` from the lane's checkout). The replica is the runner's Ubuntu 24.04 (CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0 static, cmake 3.28, clang 18, Ubuntu's Git 2.43.0, `MAKEFLAGS=w`), four CPUs each, the pinned RV32 SDK, the pinned Verilator 5.050; the three ran at once. Logs: `round16/logs/` in this directory.

| Gate | Where | Result |
|---|---|---|
| `firmware-boundary`'s step, `ctrl_boundary.py --require-rv32 --selftest --without verilator` (`boundaryjob.sh`) | replica, CPUs 64-67 | **PASS in 696 s**: 2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own), 0 findings, **105 boundary, 102 pin and 4 figure controls, 0 misbehaved** (`bjob-head.log`; the figure controls read the README's 102) |
| `firmware-verilator`'s step, `--only verilator` (`vgate8.sh`) | replica, CPUs 72-75 | **PASS in 495 s**: 829 of 930, 0 findings, **6, 102 and 4, 0 misbehaved**; the bench (57 s), the MAAP differential's self-test (141 s) and the AECP wire comparison `--every` (208 s) each exit 0 (`vjob-head.log`) |
| `firmware-unit`'s steps (`unitjob.sh`) | replica, CPUs 68-71 | **every step rc 0, 2074 s in all** (`ujob-head.outer`): `tally_selftest.py` 3 s; `fw_rv32_selftest.py --require-rv32` 6 s; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` 1777 s, `tsn-c-stack at 405dc683…`, **`mutants: 506 of 506 caught`**, 915 verdict lines `[ok]`, every one equal to round 15's once its time is dropped, `test_ctrl_firmware: PASS` (its log, 348900 bytes, is kept out of this directory: sha256 `b76cf7f679e2076370e3662ceba6180592a00198f48d8f3fbfe1e390155cb57b`); `test_ctrl_nvm.py` 73 s, `OK across 5 shape(s), 435 tests`; `fw_coverage.py --selftest` `29 of 29 planted cases`; `fw_coverage.py --check` 214 s, `firmware coverage: PASS (30 files)`, every row 100 % and equal to round 15's (below) |
| the 35 RV32 images (`images6.sh`) | host, the pinned SDK, round 1's runtime archives | 35 of 35 identical to dev `c20c85bd` (above) |
| the docs job's 54 commands (`docsjob.sh`) | host, a clone with the job's three submodules, CPython 3.12.3 with PyYAML and the pinned renderer, `MAKEFLAGS=w` | 53 of 54 rc 0 in 165 s (`docsjob-head.log`, `docs-head/`): `check_em_dash.py --base c20c85bd` 0 findings over 431 added lines in 12 pages; `docs_check.py` 0 findings across 203 pages; `check_py_idiom.py` every ratchet held (`long function: 9 <= 9`, `long module: 10 <= 10`, `over-long line: 0 <= 0`); `check_hygiene.py --check` PASS; `ci_events.py --check` (1974 items) and `--selftest`; `gen_toc.py --check` and `--verify-anchors`. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50 under `MAKEFLAGS=w`, as at dev; 50 of 50 without it (`srclists-nomf-head.log`) |
| the hook-rule campaign (`hook_mutants.py`, unchanged) | host, four clones at the head | H0 clean; **H1 to H24 CAUGHT, 24 of 24 on CPython 3.12.3 and on 3.14**, every mutant's escape count equal to round 15's (`hook-mutants-*.log`) |
| every pin control with the census and the figure check (R585-14's `r585_14_pin_controls.py`, `r585_14_census_figures.py`) | host, CPython 3.14, Git 2.56.0 and upstream 2.43.0 | 102, 0 misbehaved; census 0; figures 0; 4 of 4 figure controls (`pin-controls-wt2.log`, `census-figures-wt2.log`; mutant N0 on each Git) |
| the configuration, environment and store controls (`pin_subset16.py`) and the round-16 mutants (`super_mutants.py`) | host, Git 2.56.0 and upstream 2.43.0 | 42 of 42 `[ok]` on each; N0 to N9 as in item 2 |
| R585-14's probes (all five scripts) and the other-keys probe (`super_other_keys.py`) | host, Git 2.56.0 and upstream 2.43.0 | as in items 1 and 2 |
| R584-12's `store_probe.py` (round 15's copy, unchanged) | host, Git 2.56.0 and upstream 2.43.0 | 20 states, every one `RAN=0` on both; every verdict equal to round 15's but `super_fsmonitor`, now `REFUSED ... core.fsmonitor (local)` (was ACCEPTED, held by the helper's setting) (`store-probe-head-py314.txt`, `store-probe-head-git243up.txt`) |
| every entry point (`entrypoints16.py`: round 15's with one state added) | host, a full clone at the head | 17 entry points × 10 states (round 15's nine, and the superproject itself a partial clone whose promisor remote is reached over an ssh recorder): **170 of 170 refused** by name before any build, the recorder never run (`entrypoints16.log`) |

The coverage at the head (`fw_coverage.py --check`, the replica), every row equal to round 15's and to dev's ratchet; the mutation campaigns' 915 verdict lines and `mutants: 506 of 506 caught` are equal to round 15's (the firmware gate's tables of rounds 1 to 13 stand):

| File | Lines (raw) | Branches (raw) | Lines after exclusions | Branches after exclusions |
|---|---|---|---|---|
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 79/79 | 28/28 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 99/99 | 64/64 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/mbx/mbx.c` | 243/243 | 102/102 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 539/539 | 486/486 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100.00 % | 100.00 % |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100.00 % | 100.00 % |
| `third_party/tsn-c-stack/include/wire.h` | 10/10 | 2/2 | 100.00 % | 100.00 % |
| `third_party/tsn-c-stack/src/acmp.c` | 767/767 | 362/362 | 100.00 % | 100.00 % |
| `third_party/tsn-c-stack/src/adp.c` | 204/206 | 95/102 | 100.00 % | 100.00 % |
| `third_party/tsn-c-stack/src/maap.c` | 209/209 | 140/140 | 100.00 % | 100.00 % |

Not run: act (no workflow, act manifest or CI file changes this round; round 13's act self-test stands for those files) and hosted CI (the head is not pushed).

Lane hygiene: R585-14's probes, run once against the lane's worktree before the commit, left three bytecode caches in it (`scripts/__pycache__`, `sw/firmware/ctrl/test/__pycache__`, `sw/firmware/gtest/__pycache__`, all from this session); they were removed, and every later probe, mutant and gate ran in scratch clones or with `-B`. At the end the lane's checkout has 0 status entries, ignored files included; `ctrl_build.py --stack-pin` in the lane prints `tsn-c-stack at 405dc683…`, rc 0, and `git fsck --full` of its submodule is rc 0 (`lane-stack-fsck.txt`).

### Open risks and questions (round 16)

1. **The superproject's other keys** are not judged, as the assignment says. Measured: none of 28 program-naming keys starts a program while the gitlink is read, on Git 2.56.0 and upstream 2.43.0; this is a scratch probe, not a standing control.
2. **`HELPER_CONFIG` and `GIT_NO_LAZY_FETCH`** are each defence in depth with no control that fails when one alone is removed (N6, N7 above; R585-14-S2).
3. **The hosted runner's Git** (2.55.0) is read from round 15's run 38205277457; nothing was executed on the runner.
4. **Dev** is at `c6bd08c6` or later; this round merges nothing.
5. **Carried:** `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, as at dev; `firmware-unit`'s headroom (#716); R584-9-S1, R585-13-S1 and S3, R585-14-S1 to S3 and R584-13-S1 optional; R584-8-RES-1 and the other retained residue for #495.

## Round 17

Assignment: #697 comment [6121496568](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6121496568), answering [R584-14](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6121475687) (NEGATIVE at `516a69be` on one MINOR, R584-14-F1: the superproject's refused keys match a remote's keys only with a named subsection, so a subsection-less `remote.promisor` or `remote.partialCloneFilter`, or an empty-subsection `remote "".promisor`, still declares a promisor remote, and on an upstream Git that ignores `GIT_NO_LAZY_FETCH` Git fetches or starts a program while the gitlink is read; one residue item, R584-14-RES-1) and [R585-15](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6121148300) (POSITIVE at `516a69be`, two residue items). Option (a); the second round in the superproject promisor class, so the class is ruled by construction. Items:
1. one key parser, judged by section and variable, for both repositories; the superproject refuses by (section, variable), the subsection never deciding; the refused pairs are round 16's; its other keys still pass;
2. standing controls for the subsection-less and empty-subsection spellings, each asserting the refusal by key name, `[ok]` at the head and `ESCAPED` under a mutant that matches named subsections only; R584-14's `superproject_spelling_probe.py`, unchanged, on upstream Git 2.43.0: S2, S3 and S6 to S9 REFUSED naming the key with `RAN=0`, S0 and S5 unchanged; every earlier pin control holding;
3. the texts state exactly what is held (the superproject declares no promisor remote in any key spelling Git reads, judged by section and variable; `GIT_NO_LAZY_FETCH=1` and `core.fsmonitor=false` defence in depth), without "on any Git" or "whatever a Git version makes of it"; R584-14-RES-1 at `README.md:186`, R585-15-RES-1 and RES-2 as their exact fixes state;
4. merge dev `c6bd08c6` (a merge commit), the generated submodule diagram only through its generator, STOP if another conflict touches firmware behaviour or an image input; images identical to dev `c6bd08c6`'s for every shape; round 16's bar re-run.

Base of the round: `516a69be9afba02670e37874294bd1f45ccb9316` (PR #705's head). New commits only, no rebase or amend; not pushed.
Status: REVIEW READY at the head below, posted as #697 comment [6122601380](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6122601380) (its text: `round17/review-ready-round17.md`; see [Gates](#gates-at-the-round-17-head)); every item done; R585-14-S1 to S3, R584-13-S1, R585-13-S1 and S3 not taken.

### Commits

| Commit | Subject | Validated before committing |
|---|---|---|
| `6e88cfb65` | Parse both repositories' configuration keys with one parser and refuse the superproject's promisor, transport and fsmonitor keys by section and variable whatever their subsection, with standing controls for the subsection-less and empty-subsection spellings | the configuration, environment and store controls (scratch `pin_subset17.py`, 46 of 46 `[ok]` on Git 2.56.0 and on upstream 2.43.0); every pin control with the census and the figure check (R584-14's `run_pin_controls.py`, unchanged: 106 pin controls, 0 misbehaved, census 0, figures 0, 4 of 4 figure controls, both Gits); R584-14's two spelling probes (both Gits, item 2); the round-17 mutants (item 2); pyflakes; `check_py_idiom.py` (every ratchet held, `long function: 9 <= 9`, `long module: 10 <= 10`); `docs_check.py` 0; `check_doc_style.py` OK; then, committed, `check_em_dash.py --base c20c85bd` 0 findings over 435 added lines, `gen_toc.py --check` and `--verify-anchors` OK |
| `5b4ea5516` | Merge dev c6bd08c6, regenerating the submodule boundary diagram from both sides' gitlinks | `submodule_boundaries.gen.py` (written, then `--check` `OK (6 exact gitlinks, decoded PNG)` and `--selftest`); `check_diagram_pngs.py` (`6 decoded, source-bound, review-pinned rasters`) and `--selftest` (28 mutation controls); `check_submodule_docs.py` (`6 exact gitlinks`) and `--selftest`; the merged tree differs from dev only in the lane's 72 files, and from the lane only in the six both sides changed (item 4) |

One-line subjects, no body, no trailers, configured identity.

Head: `5b4ea55160c5ee34263e24140f960c4f03d923bc` (tree `bfc159e4`; `6e88cfb6` on `516a69be`, then the merge of dev `c6bd08c6`). `git diff --stat 516a69be 6e88cfb6`: four files under `sw/firmware/ctrl`, 157 insertions, 92 deletions. No firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin changes.

### Item 1: one key parser

- `ctrl_build.parsed_key` (`sw/firmware/ctrl/test/ctrl_build.py:507-515`): a key as Git lists it, split as Git's own `parse_config_key` (`config.c` at v2.43.0) splits it: the section all before the first dot, the variable all after the last, the subsection, which may hold dots, all between: `None` where the key has none (`remote.promisor`), `""` where it is empty (`remote "".promisor`, listed `remote..promisor`), its name otherwise.
- `ctrl_build.configuration` (`:518-532`): every listed key parsed once, `(scope, section, subsection, variable, key, value)`; the one parser of both checks.
- `ctrl_build.superproject_configured` (`:560-572`), still called by `stack_gitlink` (`:430`) before `ls-files --stage`: refuses every key whose `section.variable` is in `SUPERPROJECT_REFUSED` (`:210-219`), whatever its subsection, in any scope but the helper's own `command`-scope setting. `SUPERPROJECT_REFUSED` is now the pairs `extensions.partialclone`, `remote.promisor`, `remote.partialclonefilter`, `remote.uploadpack`, `core.sshcommand`, `core.fsmonitor` (round 16's six, by section and variable). Git 2.43.0's `promisor-remote.c` (`promisor_remote_config`) reads `remote.promisor` and `remote.partialclonefilter` through `parse_config_key` and names the remote by the subsection whatever it is (`xmemdupz(name, namelen)`), so a missing or empty subsection declares a promisor remote named `""`; v2.51.0 reads them the same way. Every other superproject key still passes: the `actions/checkout` control (the remote, `gc.auto`, `http.https://github.com/.extraheader`, the stack's submodule entries) is `accepted 405dc683…`.
- The stack's allowlist (`ctrl_build.configured`, `:545-557`) uses the same parser: `ctrl_build.family` (`:535-542`) names a parsed key's family as `STACK_CONFIG` lists them, `section.variable` without a subsection, `section.*.variable` with a named one, and `section."".variable` with an empty one, which `STACK_CONFIG` (`:197-207`) never lists. The allowlist's verdicts are unchanged: round 16's code already refused an empty-subsection key (its name kept `..`, which no entry holds); round 15's 13 configuration controls, the allowlisted clone and R584-14's `stack_spelling_probe.py` print what they printed at `516a69be`.
- `ctrl_pin_store.allowlisted` (`ctrl_pin_store.py:282-295`), the control's own check that its clone holds a key of every family, now reads its keys with `parsed_key` and `family` too (it had a copy of the old split).
- The census holds: the decision's new names (`parsed_key`, `family`, `partition`, `rpartition`) are in the proof's vocabulary; 0 findings on every run.

### Item 2: the controls

R584-14's packet fetched from `697c-review-evidence` (`306d8e73`): all 42 files match its `MANIFEST.sha256`. Its scripts run unchanged with `-I -B` on disposable clones. Upstream Git 2.43.0 is round 16's build (`git-2.43.0.tar.xz`, sha256 `5446603e73d911781d259e565750dcd277a42836c8e392cac91cf137aa9b76ec`, R584-14's receipt's). Logs: `round17/logs/`.

R584-14's `superproject_spelling_probe.py`, unchanged:

| Case | `516a69be`, upstream 2.43.0 | `516a69be`, Git 2.56.0 | `5b4ea551`, upstream 2.43.0 | `5b4ea551`, Git 2.56.0 |
|---|---|---|---|---|
| S0 the head's own control (named remote) | REFUSED by its four keys, `RAN=0` | the same | the same | the same |
| S1 S0 with the check removed (the probe's own monkeypatch) | **ACCEPTED, `RAN=1`** | `not one stage-0 gitlink`, `RAN=0` | **ACCEPTED, `RAN=1`** | `not one stage-0 gitlink`, `RAN=0` |
| S2 `remote ""` url, promisor, uploadpack | `not one stage-0 gitlink`, `RAN=0` | the same | REFUSED `remote..promisor (local), remote..uploadpack (local)`, `RAN=0` | the same |
| S3 `remote.promisor`, `remote ""` url and uploadpack | `not one stage-0 gitlink`, `RAN=0` | the same | REFUSED `remote..uploadpack (local), remote.promisor (local)`, `RAN=0` | the same |
| S4 S2 with `extensions.partialclone` | REFUSED `extensions.partialclone (local)`, `RAN=0` | the same | REFUSED `extensions.partialclone (local), remote..promisor (local), remote..uploadpack (local)`, `RAN=0` | the same |
| S5 named remote | REFUSED `remote.origin.promisor (local), remote.origin.uploadpack (local)`, `RAN=0` | the same | the same | the same |
| S6 `remote.promisor`, `ext::` rewrite | **`not one stage-0 gitlink`, `RAN=1`** | `RAN=0` | REFUSED `remote.promisor (local)`, `RAN=0` | the same |
| S7 `remote.partialCloneFilter`, `ext::` rewrite | **`RAN=1`** | `RAN=0` | REFUSED `remote.partialclonefilter (local)`, `RAN=0` | the same |
| S8 `remote.promisor`, rewrite to the origin | **ACCEPTED `405dc683…` (Git fetched the tree)** | `not one stage-0 gitlink` | REFUSED `remote.promisor (local)`, `RAN=0` | the same |
| S9 `remote "".promisor`, `ext::` rewrite | **`RAN=1`** | `RAN=0` | REFUSED `remote..promisor (local)`, `RAN=0` | the same |

So S2, S3 and S6 to S9 end REFUSED naming the key with `RAN=0` on upstream 2.43.0 (and on 2.56.0), S0 and S5 keep their verdicts, and the `516a69be` columns reproduce R584-14's receipt. R584-14's `stack_spelling_probe.py` prints what its receipt prints on both Gits (T0 accepted; T1 and T2 refused by the allowlist naming their keys; `RAN=0`).

Standing controls, new (`sw/firmware/ctrl/test/ctrl_pin_store.py`):

| Control | Built by | Verdict at the head |
|---|---|---|
| R585-14's sparse superproject (the gitlink's tree missing from its store) beside a promisor remote declared by `remote.promisor`, no subsection, which Git names `""` and reaches through the recorder by `url."ext::<recorder>".insteadOf=` with `protocol.ext.allow=always` | `unnamed_promisor` (`:231-238`), `UNNAMED` (`:310-313`), `superproject_controls` (`:345-348`) | `... while the gitlink is read: remote.promisor (local)` |
| the same, `remote.partialCloneFilter=tree:0`, no subsection | the same | `... remote.partialclonefilter (local)` |
| the same, `remote "".promisor`, an empty subsection | the same | `... remote..promisor (local)` |
| the stack's own configuration holding `submodule "".active`, an allowlisted section and variable with an empty subsection | `store_arms` (`:411-413`) | `tsn-c-stack's repository holds configuration outside the pin proof's allowlist: submodule..active (local)` |

The superproject check refuses neither the rewrite nor `protocol.ext.allow`, so each new superproject control's refusal names its one promisor key, and each fails without the fix, since it asserts the refusal by key name: on Git 2.56.0 by its words, and on upstream 2.43.0, which ignores `GIT_NO_LAZY_FETCH`, with Git running the recorder (P1 below). The fourth control (not asked for; added so the allowlist's empty-subsection branch has a control that fails without it) holds the stack's side of the one parser. `store_arms`'s inner `unlisted` moved to module level (`:321-323`, beside `refused`) to keep the function under the idiom gate's 100-line limit. 106 pin controls in all, 0 misbehaved: on Git 2.56.0 and upstream 2.43.0 under CPython 3.14.7, on upstream 2.43.0 under CPython 3.12.3, and in both replica jobs (Ubuntu's Git 2.43.0).

Mutants of the head (scratch `super_mutants17.py`, each alone on a disposable clone, then R584-14's `run_pin_controls.py`, unchanged: all 106 pin controls, the census and the figure check; `super-mutants-head-git256.log`, `super-mutants-head-git243.log`; the same counts on `6e88cfb6` before the merge):

| Mutant | Escaped of 106, Git 2.56.0 | Escaped of 106, upstream 2.43.0 |
|---|---|---|
| N0 none | 0 | 0 |
| **P1 round 16's match: a remote key refused only with a named subsection** (the assignment's mutant) | **3: the three new superproject controls, each `not one stage-0 gitlink`** | **3: the same, Git running the recorder through the `ext::` rewrite** |
| P2 a remote key refused only with a subsection, named or empty | 2: `remote.promisor` and `remote.partialCloneFilter` | 2, the recorder run |
| P3 a remote key refused only with a named subsection or none | 1: `remote "".promisor` | 1, the recorder run |
| P4 the stack's `*` family holding an empty subsection too | 1: `submodule "".active` accepted | 1 |
| P5 `parsed_key` reading an empty subsection as none | 1: `submodule "".active` accepted (as `submodule.active`) | 1 |
| P6 `parsed_key` reading no subsection as an empty one | the run stops at the allowlisted control's setup (`holds no core.bare, …`), 51 controls already `ESCAPED` (the clean clone refused) | the same |
| N1 the superproject check not called | 7: the `core.fsmonitor` and include/work-tree controls accepted, the five sparse controls `not one stage-0 gitlink` | 7: the same two accepted, the five sparse controls with Git running the recorder |
| N2 the check after the index is read | 0 (Git honours `GIT_NO_LAZY_FETCH`, so nothing is fetched, then the keys are refused) | **5**: the five sparse controls, Git running the recorder |
| N3 the superproject's `local` scope only | 1: the include/work-tree control | 1 |
| N4 `extensions.partialclone` not refused | 2 | 2 |
| N4 `remote.promisor` not refused | 4: R585-14's two sparse controls by their words, the `remote.promisor` and `remote "".promisor` controls `not one stage-0 gitlink` | 4, the last two with the recorder run |
| N4 `remote.partialclonefilter` not refused | 2 | 2, the new one with the recorder run |
| N4 `remote.uploadpack` not refused | 1 | 1 |
| N4 `core.sshcommand` not refused | 1 | 1 |
| N4 `core.fsmonitor` not refused | 2 | 2 |
| N5 the helper's own `command` setting refused in the superproject | the run fails before its first control: the controls' own gitlink read is refused (`core.fsmonitor (command)`) | the same |
| N6 no `HELPER_CONFIG` (`-c core.fsmonitor=false`) | 0: defence in depth | 0 |
| N7 no `GIT_NO_LAZY_FETCH` | 0: defence in depth | 0 |
| N8 neither the check nor `GIT_NO_LAZY_FETCH` | 7, the five sparse controls with Git running the recorder | 7, as N1 |
| N9 neither the check nor `HELPER_CONFIG` | 7, the `core.fsmonitor` and include/work-tree controls with Git running the recorder | 7 |

Every earlier pin control holds (N0, and the 102 earlier controls `[ok]` in every run above).

Scratch-harness faults found and fixed while running these (none in the lane): a first mutant run named its work directories after the mutants, and an apostrophe in a path broke the mailbox bench's `make` recipes (`exit 2: no pin verdict`); the six `N4` mutants shared one work directory. A first hook-rule campaign ran four clones under one parent, and `hook_mutants.py` puts its scratch in the clone's parent (`<clone>/../work`), so the four runs shared it and reported rules NOT CAUGHT that are caught when run alone (H1 and H13 re-run alone at `516a69be` and at the head: CAUGHT at both, with and without `PYTHONDONTWRITEBYTECODE`). Those logs are kept as `hook-mutants-*.parallel-shared-work.txt`; the campaign was re-run with each clone under its own parent (below).

### Item 3: the texts

- `sw/firmware/ctrl/README.md:175` (one parser), `:178` (a key with an empty subsection is not in the allowlist), `:180` (the stack's refused promisor keys "with any subsection or none"), `:181` (what the allowlist holds: Git's own bookkeeping only, no key naming a program, a promisor remote or its transport; was "no key ... can have Git start a program, or fetch ..."), `:182-185` (the superproject: every key whose section and variable `SUPERPROJECT_REFUSED` lists, whatever its subsection; why the subsection never decides; "So the superproject declares no promisor remote in any key spelling Git reads, judged by section and variable, and names no fsmonitor"; was "without a promisor remote Git fetches nothing, so a tree its sparse index lacks is not fetched through a program"), `:187` (`core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1` defence in depth behind both checks), `:188` (R585-15-RES-1: "as Ubuntu 24.04's updated 2.43.0 package is (`2.43.0-1ubuntu7.3` checked; its release package `2.43.0-1ubuntu7` is not)"), `:189` (R584-14-RES-1: "(an upstream release before 2.45.0 other than the CVE-2024-32465 maintenance releases, such as 2.43.0 or 2.44.0)"; R585-15-RES-1's README:186 part, the same fact in other words, is replaced by it as the assignment directs), `:223` (106 pin controls), `:244` (Twenty-seven more), `:249` (Eight read the gitlink), `:252-253` (the three new superproject controls; each refused naming exactly the refused keys it planted), `:255` and `:259` (Fourteen, with `submodule "".active`).
- `ctrl_build.py:182-189` (`GIT_ENVIRONMENT`'s comment: `GIT_NO_LAZY_FETCH` defence in depth; R585-15-RES-1 "such as Ubuntu 24.04's updated 2.43.0"; what holds is that neither repository's configuration declares a promisor remote), `:197-203` (`STACK_CONFIG`'s families), `:210-217` (`SUPERPROJECT_REFUSED`, by section and variable), the docstrings of `parsed_key`, `configuration`, `family`, `configured` (was "... whatever a Git version makes of it") and `superproject_configured` (was "... whatever a Git version makes of GIT_NO_LAZY_FETCH").
- `ctrl_pin_store.py:3-78` (the module docstring: one parser; the superproject's keys by section and variable; eight superproject controls; the empty-subsection stack control; both settings defence in depth).
- `ctrl_pin.py:61-70` (THE THREAT MODEL: one parser; the superproject declares no promisor remote in any key spelling Git reads, judged by section and variable; the two settings defence in depth) and `:136` (R584-14's promisors among the controls); the module stays at 1000 lines.
- No "on any Git" or "whatever a Git version makes of it" remains in the tree or in the PR body.

### Item 4: the dev merge

`git fetch origin dev` gave `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc` (checked with `git rev-parse FETCH_HEAD`), and `git merge --no-ff` of it on `6e88cfb6` stopped in three conflicts. A trial merge in a scratch clone, before any change, gave the same three.

| Conflict | Resolution |
|---|---|
| `docs/diagrams/submodule_boundaries.drawio`, `submodule_boundaries.png` | remade by `docs/diagrams/submodule_boundaries.gen.py` from the merged index's gitlinks (tsn-c-stack `405dc683`, dev's gptp-processor `7dda9c3b`); the SVG, merged without conflict, is byte-equal to what the generator writes |
| `docs/diagrams/PNG_MANIFEST.json` | dev's file, then the generator's rewrite of the submodule diagram's entry; it differs from dev's in that entry only (a first resolution took the lane's file, which dropped dev's new `timesync_chain` entry; `check_diagram_pngs.py` refused it, and it was redone before the commit) |

Not conflicted and taken as merged: `docs/reference/SUBMODULES.md` (dev's gptp-processor pin `7dda9c3b` in the table and its four guide links, beside this lane's tsn-c-stack row), `docs/testing/CI_WORKFLOWS.md` (dev's text on the GM-step leg's move to its own suite, #621, beside this lane's), dev's gptp-processor gitlink (the lane's checkout updated with `git submodule update -- gptp-processor` after checking that submodule's top level and its origin `Mister-M-alt/FPGA-gPTP`), and the rest of dev: 40 files, none under `sw/`, `configs/`, `hdl/`, `third_party/`, `.github/` or a Makefile of the firmware (`syn/yosys/rom_digests.tsv` gains the gPTP microcode ROM of `7dda9c3b`). No conflict touched firmware behaviour or an image input. The merged tree differs from dev `c6bd08c6` in exactly the 72 files the lane changes from its source base `c20c85bd`, and from the lane only in the six both sides changed (the four diagram files, `SUBMODULES.md`, `CI_WORKFLOWS.md`).

### The images

Every RV32 image at every shipped shape, linked with the pinned SDK and round 1's runtime archives (scratch `images6.sh`, unchanged, 88 s at the head and 85 s at dev on four CPUs), at the head and at dev `c6bd08c6` (a clone of dev itself, its own cores in `sw/firmware/ctrl`). The manifests are byte-equal, sha256 `8b1292dbe318603b3ed2354c0b58c2721ab3f27094589153d946af0783b39095`, as dev `c20c85bd`'s and the heads of rounds 13 to 16 (`round17/logs/images-head-5b4ea551-elf.sha256`, `images-dev-c6bd08c6-elf.sha256`); `ctrl_image.py` printed `tsn-c-stack at 405dc683…` first at the head. `ctrl_image.py --base c6bd08c6f52632c6d33d834ce842ac3cf63f29cc` at the head: `+0` in every section at both shapes (`ctrl-image-base-c6bd08c6.log`).

| Image (shape) | dev `c6bd08c6` sha256 | head `5b4ea551` sha256 | |
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

### Gates at the round-17 head

Every gate the change touches ran at `5b4ea55160c5ee34263e24140f960c4f03d923bc`, each in a fresh clone that shares no file with the lane (scratch `mkclone17.sh`: `clone --no-hardlinks`, each submodule fetched over `file://` from the lane's checkout). The replica is the runner's Ubuntu 24.04 (CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0 static, cmake 3.28, clang 18, Ubuntu's Git 2.43.0, `MAKEFLAGS=w`), four CPUs each, the pinned RV32 SDK, the pinned Verilator 5.050; the three ran at once. Logs: `round17/logs/` in this directory.

| Gate | Where | Result |
|---|---|---|
| `firmware-boundary`'s step, `ctrl_boundary.py --require-rv32 --selftest --without verilator` (`boundaryjob.sh`) | replica, CPUs 64-67 | **PASS in 724 s**: 2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own), 0 findings, **105 boundary, 106 pin and 4 figure controls, 0 misbehaved** (`bjob-head.log`; the figure controls read the README's 106) |
| `firmware-verilator`'s step, `--only verilator` (`vgate8.sh`) | replica, CPUs 72-75 | **PASS in 503 s**: 829 of 930, 0 findings, **6, 106 and 4, 0 misbehaved**; the bench (61 s), the MAAP differential's self-test (148 s) and the AECP wire comparison `--every` (211 s) each exit 0 (`vjob-head.log`) |
| `firmware-unit`'s steps (`unitjob.sh`) | replica, CPUs 68-71 | **every step rc 0, 2153 s in all** (`ujob-head.outer`): `tally_selftest.py` 3 s; `fw_rv32_selftest.py --require-rv32` 7 s; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` 1847 s, `tsn-c-stack at 405dc683…`, **`mutants: 506 of 506 caught`**, 915 verdict lines `[ok]`, identical in order to round 16's, `test_ctrl_firmware: PASS` (its log, 348900 bytes, is kept out of this directory: sha256 `34ee0bc4dfaef34392b18b112a91212053aaa9f61d3ab30efa4846dc805023b5`); `test_ctrl_nvm.py` 80 s, `OK across 5 shape(s), 435 tests`; `fw_coverage.py --selftest` `29 of 29 planted cases`; `fw_coverage.py --check` 216 s, `firmware coverage: PASS (30 files)`, every row 100 % and identical to round 16's (the table of round 16 stands) |
| the 35 RV32 images (`images6.sh`) | host, the pinned SDK, round 1's runtime archives | 35 of 35 identical to dev `c6bd08c6` (above) |
| the docs job's 54 commands (`docsjob.sh`) | host, a clone with the job's three submodules, CPython 3.12.3 with PyYAML and the pinned renderer, `MAKEFLAGS=w` | 53 of 54 rc 0 in 164 s (`docsjob-head.log`, `docs-head/`): `check_em_dash.py --base c6bd08c6` 0 findings over 435 added lines in 12 pages; `docs_check.py` 0 findings across 204 pages; `check_py_idiom.py` every ratchet held (`long function: 9 <= 9`, `long module: 10 <= 10`, `over-long line: 0 <= 0`); `check_hygiene.py --check` PASS; `ci_events.py --check` (1974 items) and `--selftest`; `gen_toc.py --check` and `--verify-anchors`; `submodule_boundaries.gen.py --check` and `--selftest`; `check_diagram_pngs.py` and `--selftest`; `check_submodule_docs.py` and `--selftest`. The one failure is `check_rtl_source_lists.py --selftest`, 48 of 50 under `MAKEFLAGS=w`, the same two fixtures at dev `c6bd08c6` (`srclists-mfw-dev.log`); 50 of 50 at the head without it (`srclists-nomf-head.log`) |
| the hook-rule campaign (`hook_mutants.py`, unchanged) | host, four clones at the head, each under its own parent | H0 clean; **H1 to H24 CAUGHT, 24 of 24 on CPython 3.12.3 and on 3.14**, every mutant's verdict line and escape count equal to round 16's (`hook-mutants-*.log`) |
| every pin control with the census and the figure check (R584-14's `run_pin_controls.py`) | host | 106, 0 misbehaved; census 0; figures 0; 4 of 4 figure controls: CPython 3.14.7 with Git 2.56.0 and with upstream 2.43.0, CPython 3.12.3 with upstream 2.43.0 (`pin-controls-head-*.log`) |
| the round-17 mutants (`super_mutants17.py`) | host, Git 2.56.0 and upstream 2.43.0 | as in item 2 (`super-mutants-head-git*.log`) |
| R584-14's two probes, R585-14's five probe scripts, R584-12's `store_probe.py` (`probes17.sh`) | host, Git 2.56.0 and upstream 2.43.0 | R584-14's as in item 2; R585-14's and `store_probe.py`'s outputs identical to round 16's at `516a69be` once paths are normalised, `store_probe.py` 20 states every one `RAN=0` (`head-git*-*.txt`) |
| every entry point (`entrypoints17.py`: round 16's with two states added) | host, a full clone at the head | 17 entry points × 12 states (round 16's ten, and the superproject's `remote.promisor`, no subsection, and `remote "".promisor`, each over an `ext::` rewrite naming the recorder): **204 of 204 refused** by name before any build, the recorder never run (`entrypoints17.log`) |

Not run: act (no workflow, act manifest or CI file changes this round or in dev's merge; round 13's act self-test stands for those files) and hosted CI (the head is not pushed).

Lane hygiene: one bytecode cache appeared in the lane during the merge (`scripts/__pycache__/png_artifact.cpython-314.pyc`, written by a diagram self-test's child interpreter at 11:57 local, this session) and was removed; every probe, mutant and gate ran in scratch clones. At the end the lane's checkout has 0 status entries, ignored files included; `ctrl_build.py --stack-pin` in the lane prints `tsn-c-stack at 405dc683…`, rc 0, and `git fsck --full` of its submodule is rc 0 with no output (`lane-stack-fsck.txt`).

### Open risks and questions (round 17)

1. **The superproject's other keys** are not judged, as rounds 16 and 17 rule; round 16's measurement stands (none of 28 program-naming keys starts a program while the gitlink is read, on Git 2.56.0 and upstream 2.43.0; a scratch probe, not a standing control).
2. **The stack's empty-subsection families**: the allowlist lists none, so a key such as `submodule "".active` is refused by name. Git writes none; the round-15 allowlist refused them too. The fourth new control holds this, not asked for by the assignment.
3. **`HELPER_CONFIG` and `GIT_NO_LAZY_FETCH`** are each defence in depth with no control that fails when one alone is removed (N6, N7; R585-14-S2, optional, not taken).
4. **Not pushed**: no hosted run exists at the head; the replica is local evidence only.
5. **Carried:** `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, as at dev; `firmware-unit`'s headroom (#716; 2153 s here of its 45 minutes); R584-9-S1, R585-13-S1 and S3, R585-14-S1 to S3 and R584-13-S1 optional; R584-8-RES-1 and the other retained residue for #495.
