# HANDOFF — lane 697c, [A583]

Current: Round 20 is review ready locally at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`; see the final section.

Issue: [kebag-logic/milan-fpga#697](https://github.com/kebag-logic/milan-fpga/issues/697), assignment comments 6091228902 (round 1), 6092628778 (round 2), 6093389868 (round 2b), 6094873968 (round 3), 6096148471 (round 4), 6097800045 (round 5), 6102039501 (round 6), 6104711137 (round 7), 6105928035 (round 8), 6107732413 (round 9), 6112358746 (round 10), 6113306444 (round 11), 6114400461 (round 12), 6116488747 (round 13), 6117713386 (round 14), 6118625227 (round 15), 6119960001 (round 16), 6121496568 (round 17) and 6130298041 (round 18).
Branch: `697-consume` from dev `8b61b70902f3ebf118e56967277e2686731081bd`; PR #705 held `27ee16b5` at this round's assignment. Round 19 is local only.
Round 18 head: `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` (round 18: a merge of dev `dc4d06cb` on `5b4ea551`, PR #705's head, as `ddbd7fd7`, then one commit; not pushed).
Historical status: round 18 REVIEW READY at `27ee16b52`, comment [6131138314](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6131138314) (its text: `round18/review-ready-round18.md`) (dev `dc4d06cb` merged, #716's four firmware jobs beside the two TSN stack boundary jobs, each firmware job fetching tsn-c-stack; dev's shard proof held by the boundary gate's registry; images identical to dev `dc4d06cb`'s; every job within 60 % of its timeout; see [Round 18](#round-18)); round 17 REVIEW READY at `5b4ea5516`, comment [6122601380](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6122601380) (its text: `round17/review-ready-round17.md`) (one parser reads both repositories' configuration keys; the superproject's promisor, transport and fsmonitor keys refused by section and variable whatever their subsection; dev `c6bd08c6` merged, images identical to its; see [Round 17](#round-17)); round 16 REVIEW READY at `516a69be9`, comment [6120798872](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6120798872) (its text: `round16/review-ready-round16.md`) (the superproject's own configuration may not name a promisor remote, its transport or an fsmonitor, each refused by name before the gitlink is read; see [Round 16](#round-16)); round 15 REVIEW READY at `44eef11f8`, comment [6119366539](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119366539) (its text: `round15/review-ready-round15.md`) (the stack's own configuration held to an allowlist of Git's own bookkeeping, the configuration guarantee; `GIT_NO_LAZY_FETCH=1`; see [Round 15](#round-15)); round 14 REVIEW READY at `a8fe548a0`, comment [6118316100](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118316100) (its text: `round14/review-ready-round14.md`) (every object the proof reads hashed against its id; `core.fsmonitor=false`; the alternates control; see [Round 14](#round-14)); round 13 REVIEW READY at `8aaa2da74`, comment [6117226531](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117226531) (its text: `round13/review-ready-round13.md`) (pin `405dc683`, dev `c20c85bd` merged, F-INT's plants retargeted, images identical to dev's; see [Round 13](HANDOFF-rounds-11-13.md#round-13)); round 12 STOP at `adb936049` (item 1, the dev merge; items 2 and 3 done), comment [6115091316](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6115091316) (its text: `round12/stop-round12.md`) (see [Round 12](HANDOFF-rounds-11-13.md#round-12)); round 11 REVIEW READY at `aca5e8afc`, comment [6114209149](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114209149) (its text: `round11/review-ready-round11.md`) (see [Round 11](HANDOFF-rounds-11-13.md#round-11)); round 10 REVIEW READY at `be607527e`, comment [6113121913](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6113121913) (its text: `round10/review-ready-round10.md`) (see [Round 10](HANDOFF-rounds-7-10.md#round-10)); round 9 REVIEW READY at `feed95bbb`, comment [6108314179](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6108314179) (see [Round 9](HANDOFF-rounds-7-10.md#round-9)); round 8 REVIEW READY at `4cab445aa`, comment [6106923767](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6106923767) (its text: `round8/review-ready-round8.md`) (see [Round 8](HANDOFF-rounds-7-10.md#round-8)); round 7 REVIEW READY at `8436dfc0b`, comment [6105602289](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105602289) (see [Round 7](HANDOFF-rounds-7-10.md#round-7)); round 6 REVIEW READY at `5b4f6fbeb`, comment [6103486693](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6103486693) (its text: `round6/review-ready-round6.md`) (see [Round 6](HANDOFF-rounds-2-6.md#round-6)); round 5 REVIEW READY at `92b5be188`, comment [6100754030](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6100754030) (see [Round 5](HANDOFF-rounds-2-6.md#round-5)); round 4's REVIEW READY was comment [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937); round 3's was comment [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057), round 2b's 6094033396, round 2's 6093383132. Round 1: TAKEN 6091267846, REVIEW READY 6092168627; the pin was confirmed in 6092176555.
PR body: `PR-BODY.md` in this directory (round 2 to 17 sections added, round 5's residue, round 14's R585-12-RS1 to RS4 and R584-11-RES-1, round 15's R584-12-RES-1 / R585-13-RES-1, round 16's R585-14-RES-1 / R584-13-RES-1 and R584-13-RES-2, round 17's R584-14-RES-1, R585-15-RES-1 and R585-15-RES-2 applied, and round 18's R584-15-RES-1 applied and R585-16-RES-1 carried; no PR edit made).

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

## Rounds 14 to 18

Preserved in [HANDOFF-rounds-14-18.md](HANDOFF-rounds-14-18.md), including every gate, image, coverage, mutation and pin receipt from those rounds.

## Round 19

Assignment: [issue #697 comment 6134939296](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6134939296). Starting head: `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c`. Fetched dev and merge second parent: `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` (M8a, PR #721). Current head: `95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62`.

**STOP: the required boundary gate refuses the merged tree.** Its registry does not classify three M8a programs: `sw/litex/ctrl_memory.py`, `sw/litex/milan_soc.py`, and `sw/litex/test_ctrl_memory.py`. The gate exits 2 at `ctrl_configs.held`, before boundary self-tests or the final include judgement. The four builder captures all exited 0. The complete refusal is in `round19/logs/boundary.log`.

The assignment says **"No other change."** The merge is complete, but making this gate pass requires an additional registry/capture integration decision outside the sole conflicted file. No such change was made. In particular, `test_ctrl_memory.py:540` compiles the firmware reset entry, so classifying all three as compiling no firmware would be inaccurate. No firmware byte difference or pin change was found. This STOP reports the validation/scope conflict, not an image-difference finding.

The Round 19 STOP comment text is `round19/stop-round19.md`; its returned URL is retained in `round19/stop-comment-url.txt` when posted. No TAKEN was repeated. No push or PR edit was made.

### Resume and merge

The interrupted session left an unfinished merge, with `MERGE_HEAD` and `FETCH_HEAD` both `d5858bbe`, and one unmerged index entry. Its working file already contained the combined resolution. This session verified origin as the assigned HTTPS repository, starting HEAD as `27ee16b5`, and fetched dev again, obtaining exactly `d5858bbe`. The original `8b61b709` is an ancestor. The inherited working-file resolution was retained, checked, staged and committed; nothing was rebased or amended.

| Commit | Parents | Subject |
|---|---|---|
| `95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62` | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c`, `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` | Merge dev d5858bbe preserving split memory and pinned stack consumption |

Configured identity, one-line subject, no body or trailers. The working tree is clean. Images and captures started on the resolved working tree and were judged against the same bytes committed at this head. The boundary judgement itself ran after the commit.

### Resolution and every changed file

Only `sw/firmware/ctrl/test/ctrl_srp_image.py` required conflict resolution:

- `:8` retains the split placement/reset description; `:11` retains the stack-source description.
- `:23` and `:41` retain the stack imports, legacy-source compatibility and pin check, with no change to `source_tree`.
- `:29` imports dev's memory planner.
- `:80` retains dev's `link()` exactly, including its generated regions, reset entry and split linker script.
- `:103` retains `--stack-source`; `:107` retains dev's `--layout`.
- `:122` and `:128` retain the lane's stack-aware source selection before building.
- `:148`, `:153`, `:155`, `:159`, `:173` and `:177` retain the object, ABI, unresolved-symbol, heap, composition and section checks.
- `:151` uses dev's `link()`; `:194` retains dev's split plan or flat span report.

`round19/resolution-vs-lane.diff`, `resolution-vs-dev.diff` and `remerge-resolution.diff` retain the exact diffs. AST comparison confirms every dev function unchanged after undoing exactly the stack-source CLI argument and the two lane substitutions in `main`; `source_tree` equals the lane parent's. Every other dev change retains exactly its added and removed lines. The file set differing from dev remains the lane's same 72 files. `round19/resolution-check.txt` records the comparison.

All other changes below are inherited from dev. No additional change was made:

| File:line | Inherited change |
|---|---|
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:192` | Split-memory architecture reference |
| `docs/README.md:79` | Memory document entry |
| `docs/design/AREA_BUDGET.md:232` | M8a memory/area accounting |
| `docs/design/MAILBOX_SPLIT.md:1139` | Split memory integration contract |
| `docs/design/MARK_II_AREA_PLAN.md:42` | Plan and memory ledger |
| `docs/design/SPLIT_CONTROL_MEMORY.md:1` | Memory map, refusal rules, fit and reproduction |
| `docs/litex/LITEX_SOC.md:8` | Memory documentation link |
| `docs/testing/CI_WORKFLOWS.md:172` | M8a validation population |
| `docs/testing/TESTING.md:700` | Split-memory tests |
| `scripts/check_py_idiom.py:175` | Dev's idiom accounting |
| `scripts/ci_scope.py:65` | Split-memory CI scope |
| `scripts/run_litex_sims.sh:101` | Memory test in the simulation inventory |
| `sw/firmware/ctrl/README.md:616` | Split image fixture documentation |
| `sw/firmware/ctrl/plat/ctrl_split.ld:1` | Firmware split-memory linker script |
| `sw/firmware/ctrl/plat/ctrl_split_start.S:1` | Firmware reset entry |
| `sw/litex/ctrl_memory.py:1` | Map, ELF reader, planner and refusals |
| `sw/litex/milan_soc.py:44` | Banked control memory and SoC integration |
| `sw/litex/test_ctrl_memory.py:1` | Memory, link, SoC and mutation checks |
| `syn/ooc/ctrl_memory_ooc.py:1` | Out-of-context mapping recipe |

### Pin and source proof

The tsn-c-stack gitlink remains `405dc68310a18f669049ffc10cc23eef7300dcff`; its own top-level directory and HTTPS origin were verified before operations. Its checkout is clean. The lwSRP gitlink remains `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`.

`pin-proof.txt` and `pin-text-diff-405dc683.txt` retain the selected pin's proof. The seven dev core files have no change in `c20c85bd..d5858bbe`, so that proof applies unchanged; `round19/pin-proof-continuity.txt` records the empty diff. Source files differ in comments, as previously recorded; byte equality is claimed for the linked images, not the source text.

### Images: before and after, every shape

65 of 65 linked ELFs match dev `d5858bbe` by SHA-256 **and direct byte comparison**:

- five standalone images, one for every `configs/endstation_*.yaml` shape;
- 30 flat runtime images: five shapes, one/two interfaces, no SRP/SRP/full AECP;
- 30 split runtime images over the same combinations.

The same pinned RV32 compiler and existing runtime archives were used on both sides. Runtime-less compositions used the same inputs as the preceding round. The baseline is a new detached dev worktree with its own initialized dependencies. The first baseline attempt stopped because its gPTP dependency was not initialized; after initializing it and the other required dependencies, the full run succeeded. That setup failure is not an image verdict.

The manifest SHA-256 is `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584` on both sides. Every image build returned 0. ELFs, objects, captures, generated headers and exports stay in scratch. `round19/images-head.json` and `images-dev.json` retain each ELF's size and digest. The full before/after table follows:

| Image / shape / interfaces / composition | Bytes | Before: dev d5858bbe SHA-256 | After: resolved merge SHA-256 |
|---|---:|---|---|
| `ctrl_image/head/endstation_arty_4x4/ctrl_app.elf` | 50752 | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` |
| `ctrl_image/head/endstation_arty_8ch/ctrl_app.elf` | 50752 | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` |
| `ctrl_image/head/endstation_arty_current/ctrl_app.elf` | 50744 | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` |
| `ctrl_image/head/endstation_ax7101_1x1_tdm8/ctrl_app.elf` | 50768 | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` |
| `ctrl_image/head/endstation_ax7101_8x8/ctrl_app.elf` | 50776 | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` |
| `flat-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 68836 | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` |
| `flat-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35312 | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` |
| `flat-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 127148 | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` |
| `flat-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70364 | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` |
| `flat-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36184 | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` |
| `flat-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 128676 | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` |
| `flat-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 68836 | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` |
| `flat-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35312 | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` |
| `flat-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 132900 | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` |
| `flat-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70364 | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` |
| `flat-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36184 | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` |
| `flat-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 134428 | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` |
| `flat-endstation_arty_current-if1-srp/ctrl_app.elf` | 68412 | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` |
| `flat-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35312 | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` |
| `flat-endstation_arty_current-if1-aecp/ctrl_app.elf` | 121416 | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` |
| `flat-endstation_arty_current-if2-srp/ctrl_app.elf` | 69900 | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` |
| `flat-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36184 | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` |
| `flat-endstation_arty_current-if2-aecp/ctrl_app.elf` | 122912 | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 68764 | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` |
| `flat-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35312 | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 123612 | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` |
| `flat-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70188 | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` |
| `flat-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36184 | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` |
| `flat-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125044 | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` |
| `flat-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 68868 | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` |
| `flat-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35312 | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` |
| `flat-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 137332 | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` |
| `flat-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70372 | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` |
| `flat-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36184 | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` |
| `flat-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 138836 | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` |
| `split-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 69144 | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` |
| `split-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35624 | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` |
| `split-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 129740 | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` |
| `split-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70672 | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` |
| `split-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36496 | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` |
| `split-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 129740 | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` |
| `split-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 69144 | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` |
| `split-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35624 | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` |
| `split-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 133836 | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` |
| `split-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70672 | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` |
| `split-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36496 | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` |
| `split-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 137932 | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` |
| `split-endstation_arty_current-if1-srp/ctrl_app.elf` | 68720 | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` |
| `split-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35624 | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` |
| `split-endstation_arty_current-if1-aecp/ctrl_app.elf` | 125560 | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` |
| `split-endstation_arty_current-if2-srp/ctrl_app.elf` | 70208 | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` |
| `split-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36496 | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` |
| `split-endstation_arty_current-if2-aecp/ctrl_app.elf` | 125560 | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` |
| `split-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 69072 | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` |
| `split-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35624 | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` |
| `split-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 125588 | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` |
| `split-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70496 | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` |
| `split-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36496 | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` |
| `split-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125588 | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` |
| `split-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 69176 | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` |
| `split-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35624 | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` |
| `split-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 138268 | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` |
| `split-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70680 | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` |
| `split-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36496 | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` |
| `split-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 142364 | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` |

### Gate results and planted controls

CPython 3.12.3 was used for boundary captures, pin controls, image self-tests and documentation gates. The image matrices used the host interpreter and the same pinned RV32 compiler on both sides. M8a's test used the existing LiteX environment. Native compiles used the host compiler; these are not hosted CI timing measurements. No Verilator or Vivado build ran in this stopped round. The service's measured memory peak was 4,817,895,424 bytes, below 9 GB.

| Gate | Result | Planted control / limit |
|---|---|---|
| Four firmware builder captures | rc 0 each: RV32 9.07 s, control 381.31 s, store 101.10 s, coverage builds 282.82 s | RV32 self-test runs its own negative probes; the three build-only forms build but do not execute the suites |
| Boundary judgement, with those four captures | **rc 2**, 34.71 s; the three programs named above | Registry is fail-closed. Boundary defect controls and final dependency verdict are NOT RUN because `held()` refuses first |
| Pin control runner | rc 0; 106 controls, 0 misbehaved; census 0, figures 0 | Existing pin, configuration, environment, hook, object-store and Makefile controls; all four figure plants caught |
| `ctrl_image_selftest.py --require-rv32` | rc 0; 33 checks | Arithmetic/leaf, foreign instructions/headers/ABI, unresolved weak symbol and incompatible runtime controls |
| `test_ctrl_memory.py` | rc 0; 0 failures | 44/44 mutants caught; malformed images, budget, overlap, staging, reset, bank access and SoC refusal controls |
| `run_litex_sims.sh --selftest` | rc 0 | Failure, missing/unlisted member, masked result, skip, explicit interpreter refusal and timeout controls |
| `ci_events.py --check` | rc 0; 2169 contract items | Self-test below checks the contract's defect arms |
| `ci_events.py --selftest` | rc 0; 3064 arms | Existing workflow/event/firmware/aggregate controls |
| Round 18 documentation command list | **54/54 rc 0**, 169.62 s | Its paired self-tests include source-list, evidence-reader, scope, diagram, docs, hygiene and idiom controls; full command/result list in `round19/logs/docs.log` |
| All image variants | rc 0; 65/65 equal | Linked-image checks run within each build; direct baseline equality is the independent comparison |
| `git diff --check`, cached diff check | rc 0 | No whitespace errors |

The source-list self-test passes here with `MAKEFLAGS` unset. The historical failure under `MAKEFLAGS=w` was not rerun and is not declared fixed. No hosted CI or PR-head act replica was run because this head was not pushed. No author review verdict is claimed.

### Coverage and mutation tables

| Population | Prior round 18 evidence | Round 19 result |
|---|---|---|
| Firmware coverage | 30 files, 100%; table retained in earlier handoffs | Coverage **builds** pass; coverage measurement NOT RUN after the boundary/scope STOP; no new percentage claimed |
| Control firmware mutations | 506/506 caught | NOT RUN; no new kill count claimed |
| All four firmware phase verdicts | 915 `[ok]` verdict lines | NOT RUN as suites; build-only capture passed |
| SRP / AECP campaigns | Prior complete phase evidence in Round 18 | NOT RUN; no new kill count claimed |
| Pin controls | 106/106 expected verdicts | 106/106, 0 misbehaved |
| Boundary controls | 105 firmware, 6 Verilator, all correct | NOT RUN: registry refusal before controls; Verilator side not started |
| Pin figure controls | 4/4 caught | 4/4 caught |
| Image self-test | 33 checks | 33 checks PASS |
| M8a memory mutations | Inherited suite | 44/44 caught, listed below |

| M8a mutant | Result |
|---|---|
| `elf class weakened` (elf class) | Caught by checks arm |
| `elf machine off` (elf machine) | Caught by checks arm |
| `truncated fields read` (elf truncated) | Caught by checks arm |
| `truncated segments read` (elf truncated) | Caught by checks arm |
| `unterminated names read` (elf truncated) | Caught by checks arm |
| `load address read as the run address` (load address) | Caught by checks arm |
| `entry address off` (entry address) | Caught by checks arm |
| `entry bytes off` (entry bytes) | Caught by checks arm |
| `outside regions off` (outside regions) | Caught by checks arm |
| `entry bytes read the sections only` (entry bytes) | Caught by checks arm |
| `loads outside rom off` (loads outside rom) | Caught by checks arm |
| `load coverage off` (load coverage) | Caught by checks arm |
| `load coverage reads the first byte only` (load coverage) | Caught by checks arm |
| `a segment carries bytes below its start` (load coverage) | Caught by checks arm |
| `nobits in rom off` (nobits in rom) | Caught by checks arm |
| `writable in rom off` (writable in rom) | Caught by checks arm |
| `region overlap off` (regions) | Caught by checks arm |
| `address overlap off` (addresses) | Caught by checks arm |
| `load-address overlap off` (initial bytes) | Caught by checks arm |
| `budget off` (budget) | Caught by checks arm |
| `budget refuses exactly 56` (budget) | Caught by checks arm |
| `budget half a tile slack` (budget) | Caught by checks arm |
| `budget 1.5 tiles slack` (budget) | Caught by checks arm |
| `stage symbol off` (stage symbol) | Caught by checks arm |
| `stage size off` (stage size) | Caught by checks arm |
| `stage accepts a larger buffer` (stage size) | Caught by checks arm |
| `stage accepts a smaller buffer` (stage size) | Caught by checks arm |
| `banks smallest first` (bank order) | Caught by banks arm |
| `cpu origins off` (cpu origins) | Caught by checks arm |
| `cpu origins read the reset address only` (cpu origins) | Caught by checks arm |
| `rom left uninitialised for the Builder` (no BIOS build) | Caught by checks arm |
| `decode one bit short` (decode width) | Caught by sim arm |
| `hole compares one bit short` (hole width) | Caught by sim arm |
| `hole starts a word late` (hole start) | Caught by sim arm |
| `hole answers nothing` (hole answer) | Caught by sim arm |
| `err held a second cycle` (err pulse) | Caught by sim arm |
| `rom banks from the image start` (rom contents) | Caught by sim arm |
| `a writable rom` (read-only rom) | Caught by sim arm |
| `BIOS ROM built` (no BIOS memory) | Caught by soc arm |
| `BIOS SRAM built` (no BIOS memory) | Caught by soc arm |
| `control memory not added` (memory hookup) | Caught by soc arm |
| `main() staging check removed` (stage in main) | Caught by soc arm |
| `flag pairing off` (pairing) | Caught by soc arm |
| `shipping firmware linked` (no shipping firmware) | Caught by soc arm |

### Reproduce and unfinished bar

Set the same pinned compiler, `TMPDIR` to scratch and `PYTHONDONTWRITEBYTECODE=1`. Use CPython 3.12.3 with the required packages for the firmware/coverage captures. Each command below runs in the candidate root and exits 0 except the final boundary command, which reproduces the named rc-2 refusal:

```sh
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/rv32" -- python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/control" -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/store" -- python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/coverage" -- python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator \
  --capture "$CAP/rv32" --capture "$CAP/control" --capture "$CAP/store" --capture "$CAP/coverage"
```

Other measured checks:

```sh
python3 "$EVIDENCE/run_pin_controls.py" "$CANDIDATE" "$PIN_WORK"
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out "$IMAGE_CHECK"
python3 sw/litex/test_ctrl_memory.py
bash scripts/run_litex_sims.sh --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 "$EVIDENCE/images.py" "$CANDIDATE" "$AFTER" "$RUNTIME_ROOT"
python3 "$EVIDENCE/images.py" "$DEV" "$BEFORE" "$RUNTIME_ROOT"
```

Use the LiteX interpreter for `test_ctrl_memory.py`. `RUNTIME_ROOT` contains the existing `runtime/` and `runtime-freestanding/` archives. The documentation job's 54 individual commands and return codes are retained in `round19/logs/docs.log`; all have their separate receipts under `round19/logs/docs/`. Raw receipt sizes and SHA-256 values are in `round19/raw-log-inventory.json`; published text copies redact host paths. `round19/MANIFEST.sha256` identifies the published packet.

R584-16-RES-1 and RES-2 were applied exactly to the prepared PR body's Round 18 open item, timing cell, explanation and Status bullet. R585-17-RES-1 is the same pushed-head correction and is covered. Other carried residue is unchanged.

Unfinished: resolve the three-program registry/capture integration within an explicitly settled scope, then rerun the entire Round 18 bar, including firmware execution, coverage measurement, full mutation campaigns, both boundary sides, entry-point and hook/configuration campaigns and the disposable act self-test. Existing positive reviews cover `27ee16b5`; this merge has no new review approval. The present evidence is not REVIEW READY.


## Round 19 continuation

Authority: [issue #697 comment 6137497435](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6137497435). Resumed from clean merge `95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62`. The continuation commit is `97e713168470bfae2685521fa557dc462b782b32`, **Capture the split-memory reset-entry build in the stack boundary**. It uses the configured identity, one-line subject, no body or trailers. No TAKEN was repeated. The candidate is local and has not been pushed.

### Changes and classification evidence

| File:line | Change and evidence |
|---|---|
| `sw/firmware/ctrl/test/ctrl_configs.py:121` | Fifth firmware builder: `sw/litex/test_ctrl_memory.py --build-only`. Its own captured run is mandatory even if another builder compiled the same source. |
| `sw/firmware/ctrl/test/ctrl_configs.py:140` | The shared probe builder is PART_OF the memory test and must appear in its capture. |
| `sw/firmware/ctrl/test/ctrl_configs.py:150` | `ctrl_memory.py` is OUTSIDE: ELF parsing, region checks and bank planning, with no compiler launch. |
| `sw/firmware/ctrl/test/ctrl_configs.py:151` | `milan_soc.py` is OUTSIDE relative to the registry's control-firmware population. `milan_soc.py:2765` reads an existing control ELF; `:2774` marks its ROM initialized; `:4217` excludes shipping software when control-mailbox mode is selected. Its other path adds BIOS/milan_baremetal and calls Builder at `:4342`, so this classification does **not** assert that the entire program compiles nothing. Those optional builds compile no control-stack source. This is the explicit interpretation of “firmware” used for the ruling. |
| `sw/litex/ctrl_memory_probe.py:10` | Moves the existing probe and `link()` unchanged into a shared module. `probe-equality.txt` proves equal ASTs for PROBE and link against the merge parent. Compile flags, reset source and link inputs are unchanged. The extraction keeps the existing 1000-line module ratchet unchanged. |
| `sw/litex/test_ctrl_memory.py:951` | `--build-only` requires RV32, compiles and links the existing probe/reset entry, prints BUILT, runs no suite and plants no mutant. Full default execution still runs its seven arms and 44 mutants. |
| `sw/firmware/ctrl/test/ctrl_plants.py:193` | Three unclassified copies made from the three actual program texts are each refused by name. |
| `sw/firmware/ctrl/test/ctrl_plants.py:197` | Dropping the fifth builder's own run refuses it by name. |
| `sw/firmware/ctrl/test/ctrl_plants.py:200` | The reset entry is planted with a private stack-header include and replayed from the fifth capture; the compiler's dependencies expose it and the boundary refuses it by name. |
| `.github/workflows/rtl-fast.yml:499` | The existing boundary install step adds the pinned LiteX Python requirements. No new job or duplicate step. |
| `scripts/ci_events.py:2450` | The exact canonical dependency command is held by the CI contract. Removing the dependency addition in a disposable clone is caught. |
| `docs/testing/CI_WORKFLOWS.md:76` | Documents the fifth capture, pinned imports and absence of CPU generation in build-only. |
| `sw/firmware/ctrl/README.md:126` | Documents the fifth capture and both OUTSIDE reasons. `:159` updates the checked firmware defect count from 96 to 101; eight passing controls remain. |

`reset-capture-origins.json` shows zero reset-entry invocations in each of the four old captures and exactly one in the fifth, attributed to both the test and its shared probe builder. Its dependencies are the reset source and the compiler's own predefinition header. No forbidden baseline dependency was found, so the ruling's reset-coupling STOP condition does not occur. The planted include is caught through this added compile. The no-compiler control exits 2 before compiling; the baseline full link arm and build-only use the same distinct compile argument sets.

### Images and pin at the continuation head

The **65-row before/after image table above remains the complete table for this head**: every file was rebuilt again at `97e71316`, compared directly with dev `d5858bbe`, and has the same size and SHA-256 shown there. Five standalone, 30 flat runtime and 30 split runtime images cover every shipped shape, one/two interfaces and SRP/no-SRP/AECP composition. Both manifest files hash to `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584`; `round19-continuation/image-equality.json` records all 65 pairs.

The gitlinks remain tsn-c-stack `405dc68310a18f669049ffc10cc23eef7300dcff` and lwSRP `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The existing `pin-text-diff-405dc683.txt`, `pin-proof.txt` and `round19/pin-proof-continuity.txt` remain the source proof: seven core files have identical code and line positions; comments/SPDX differ as allowed by the recorded ruling. Source-text byte equality is not claimed. No production firmware, linker input, image generator or gitlink is changed by `95ca54cb..97e71316`.

### Gates and planted controls

Every final required gate below returned 0. Logs and command receipts are under `round19-continuation/logs/`; commands in the receipts use named environment paths, with no shell wrapper prefix.

| Gate | Result | Planted control / validation of the reader |
|---|---|---|
| Five fresh firmware captures plus boundary judgement | 2824 sources / 3052 invocations; 1623 firmware, 347 stack, 854 other; no findings. 110 boundary, 106 pin and four figure controls, none misbehaved | 101 defects, eight admitted controls and baseline; all five new controls above caught. Missing/empty/incomplete captures, bypass compilers, dependency substitutions, private headers, both directions and census controls retained |
| Verilator boundary, autonomous capture in a disposable candidate clone | 829 sources / 926 invocations; 386 firmware, 94 stack, 349 other; no findings. Six boundary, 106 pin and four figure controls, none misbehaved | Five Verilator defects and baseline, including the AECP capture loss, mode-specific source/include and MAAP C++ path controls |
| Firmware execution shard 0/4 | 60 arms pass; sharding proof passes | Missing/duplicate/new suite dispatch, invalid shards and failed-suite prevention of mutation runs |
| Control mutation slices | 506/506 caught | Every registered control mutant, unchanged names and tests |
| AECP shard 2/4 | 76/76 caught | Every registered AECP mutant |
| SRP two/one-interface slices and lwSRP pin arms | 198 + 73 + 2, all caught | Every registered two-interface defect and exact one-interface subset; edited-source and alternate-pin controls |
| Store execution with RV32 | 435 tests over five shapes; RV32 builds pass | Existing boot/write/power-loss, corruption, flash, timing and refusal tests; the additional store mutation runs are reported separately below |
| Coverage measurement, candidate and dev under the same compiler | 30 files; every line/branch after unchanged exclusions is 100%; identical normalized tables | Coverage reader 29/29 planted cases; exclusion mismatches, omitted files and compensating swaps refused |
| Listener and RV32 harness | Listener cases pass and 18/18 listener defects caught; RV32 17 checks pass; SDK 25 arms pass | Crashes/failures/disabled tests cannot become successful tallies; ABI, header, heap, unresolved symbol and stack-protector defects refused |
| Linked-image self-test | 33 checks pass | Heap/unresolved symbols, architecture/multilib mismatch and recursive helper controls |
| Full M8a memory test | Seven arms, zero failures; 44/44 mutants caught | Image validation, regions, banks, decode/hole behavior, staging, BIOS exclusion and SoC hookup plants |
| Entry-point campaign | 21 entry points x 12 disguises = 252/252 named refusals | Replacements, grafts, index flags, alternate stores, environment and configuration disguises before any build |
| Four firmware forms' pin-first control | Four refuse the edited header; deleting their shared pin check removes that named refusal in all four | Two-second negative controls establish ordering, not successful completion of a build |
| Pin matrix | 106 controls and four figure controls pass under CPython 3.12.3 / 3.14.7 and Git 2.43.0 / 2.56.0 | Forged object contents, config spellings, promisor/transport/fsmonitor, environment and audit-launch controls |
| Hook rule-removal campaign | H0 clean; H1–H24 caught on each Python; clones restored | Removing or weakening every tested rule lets a control escape or refuses the clean proof |
| Configuration campaign | 21 variants on each Git, same summary rows as Round 18; clones restored | N/P tables below; isolated removal of defense-in-depth settings is intentionally not caught because the primary check still holds |
| Earlier review probes | Eight unchanged scripts on each Git, all script exits 0 and expected outcomes retained | Clean/allowlisted cases accepted; planted forbidden cases refused with RAN=0; direct Git controls distinguish the two versions |
| CI contract | 2169 checks; 3064 self-test arms pass | 16 extra workflow plants caught, including removal of the fifth capture's pinned Python dependencies |
| Documentation/source-list/evidence gates | All 54 commands pass, plus final diff whitespace check | Their registered self-tests pass; exact commands and per-command logs retained, including source-list, source-list dependency, suite/source census, evidence reader, idiom and figures controls |
| Disposable runner self-test | 446 arms pass | No network; candidate and stub mounts read-only; no host socket or credentials; only the disposable job's scratch directory writable |

Native execution uses CPython 3.12.3, GCC/g++/gcov 16.2.1 and GoogleTest/GoogleMock 1.18.0. Full M8a elaboration uses the existing patched LiteX environment. These are local results, not new hosted results. The Verilator is pinned 5.050. No Vivado or hardware work ran. The service limit was 12 GiB; observed peak 9,520,967,680 bytes (8.87 GiB). No new output artifact exceeds 200,000 bytes; large artifacts remain in scratch and are represented by size and SHA-256.

### Runtime and job budget

The firmware-boundary job keeps its 30-minute timeout and 1080-second 60% ceiling. Fresh local phases took 9.85 s (RV32), 345.22 s (control), 94.23 s (store), 259.82 s (coverage), 0.97 s (memory), and 90.55 s (judgement/self-test). Their sum is 800.64 s. The pinned Python installation took 35.93 s, giving 836.57 s, 46.5% of the timeout, for those measured phases. This is a sum of local foreground runs, not an observed end-to-end hosted job. Round 18's existing hosted maximum is 834 s (46.3%); current hosted timing remains to be measured after publication. Verilator boundary took 472.53 s, 19.7% of 40 minutes. The four pre-existing firmware jobs and their recorded hosted budgets are unchanged.

Large campaigns were partitioned into disjoint slices using the unchanged campaign functions and tables to stay within the command limit. `mutation-populations.json` lists all names; there are no omissions or duplicates. `firmware-verdicts.txt` has 915 passing verdicts: 60 arms, 506 control, 76 AECP, 198/73 SRP, two lwSRP pin controls. Compared with Round 18, 914 full lines are identical; `acmp-unbound-record-not-zero` is caught with 35 failed checks instead of 32 under the newer native compiler/test environment. The caught population is unchanged.

### Coverage table

Candidate and dev were measured with the same compiler. The only difference from Round 18's older compiler report is `srp_mbx.c` 540/540 instead of 539/539; its source is unchanged. Raw fractions below are before exclusions; final percentages apply the unchanged exclusions.

| File | Lines | Branches | After exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 79/79 | 28/28 | 100% lines / 100% branches |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100% lines / 100% branches |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 | 100% lines / 100% branches |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 | 100% lines / 100% branches |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100% lines / 100% branches |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 | 100% lines / 100% branches |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100% lines / 100% branches |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100% lines / 100% branches |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100% lines / 100% branches |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 99/99 | 64/64 | 100% lines / 100% branches |
| `sw/firmware/ctrl/mbx/mbx.c` | 243/243 | 102/102 | 100% lines / 100% branches |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100% lines / 100% branches |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100% lines / 100% branches |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100% lines / 100% branches |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100% lines / 100% branches |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100% lines / 100% branches |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 540/540 | 486/486 | 100% lines / 100% branches |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100% lines / 100% branches |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100% lines / 100% branches |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100% lines / 100% branches |
| `third_party/tsn-c-stack/include/wire.h` | 10/10 | 2/2 | 100% lines / 100% branches |
| `third_party/tsn-c-stack/src/acmp.c` | 767/767 | 362/362 | 100% lines / 100% branches |
| `third_party/tsn-c-stack/src/adp.c` | 204/206 | 95/102 | 100% lines / 100% branches |
| `third_party/tsn-c-stack/src/maap.c` | 209/209 | 140/140 | 100% lines / 100% branches |

### Mutation tables

| Population | Count | Result |
|---|---:|---|
| Control slices | 127 / 127 / 127 / 125 | 506 caught |
| AECP | 76 | 76 caught |
| SRP, two interfaces | 99 / 99 | 198 caught |
| SRP, one interface | 37 / 36 | 73 caught |
| lwSRP pin | 2 | 2 caught |
| Memory | 44 | 44 caught; full named table retained above and in memory-full.log |
| Listener | 18 | 18 caught |
| Firmware boundary defects / admitted / baseline | 101 / 8 / 1 | All behaved as planted |
| Verilator boundary defects / baseline | 5 / 1 | All behaved as planted |
| Pin / figure | 106 / 4 | None misbehaved in each environment |
| CI workflow plants | 16 | 16 caught |

Configuration variants preserve Round 18's outcomes on both Git versions:

| Variant | Git 2.43.0 | Git 2.56.0 |
|---|---|---|
| N0 none | rc 0; 0 escaped | rc 0; 0 escaped |
| N1 the superproject check not called | rc 1; 7 escaped | rc 1; 7 escaped |
| N2 the superproject check after the index is read | rc 1; 5 escaped | rc 0; 0 escaped |
| N3 the superproject's local scope only | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 extensions.partialclone not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.promisor not refused | rc 1; 4 escaped | rc 1; 4 escaped |
| N4 remote.partialclonefilter not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.uploadpack not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.sshcommand not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.fsmonitor not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N5 the helper's own command-line setting refused in the superproject | rc 1; 0 escaped; clean proof refused | rc 1; 0 escaped; clean proof refused |
| N6 no HELPER_CONFIG | rc 0; 0 escaped | rc 0; 0 escaped |
| N7 no GIT_NO_LAZY_FETCH | rc 0; 0 escaped | rc 0; 0 escaped |
| N8 neither the superproject check nor GIT_NO_LAZY_FETCH | rc 1; 7 escaped | rc 1; 7 escaped |
| N9 neither the superproject check nor HELPER_CONFIG | rc 1; 7 escaped | rc 1; 7 escaped |
| P1 round 16's match: a remote key with a named subsection only | rc 1; 3 escaped | rc 1; 3 escaped |
| P2 a remote key with a subsection, named or empty, only | rc 1; 2 escaped | rc 1; 2 escaped |
| P3 a remote key with a named subsection or none only | rc 1; 1 escaped | rc 1; 1 escaped |
| P4 the stack's `*` family holding an empty subsection too | rc 1; 1 escaped | rc 1; 1 escaped |
| P5 parsed_key reading an empty subsection as none | rc 1; 1 escaped | rc 1; 1 escaped |
| P6 parsed_key reading no subsection as an empty one | rc 1; 51 escaped; clean proof refused | rc 1; 51 escaped; clean proof refused |

N0 is the baseline. N6 and N7 remove isolated defense-in-depth settings; the primary repository configuration check still prevents the forbidden behavior, so their zero escapes are expected and are not claimed as kills. N5/P6 over-refuse the clean proof. The other weakened checks are caught by escapes. H0–H24 per-rule evidence is in hook312.log and hook314.log; H0 is clean and H1–H24 are caught. Caller environment key names in those logs are redacted; raw sizes/hashes are retained.

### Reproduction and final limitations

Set `MILAN_RV32_CC` to the pinned compiler, `VERILATOR` to pinned 5.050, `VERILATOR_JOBS=2`, `PYTHONDONTWRITEBYTECODE=1`, and `TMPDIR` to disk scratch. `CAP`, `WORK`, `CANDIDATE`, `DEV`, `CLONE`, `EVIDENCE` and `LITEX_PY` below are caller-selected paths. Use CPython 3.12.3 for the firmware commands and an existing patched LiteX environment only for the full memory suite. No command is piped.

```sh
python3 -m pip install --quiet pyyaml -r sw/litex/litex_pins.txt
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/rv32" -- python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/control" -- python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/store" -- python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/coverage" -- python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/memory" -- python3 sw/litex/test_ctrl_memory.py --build-only
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator --capture "$CAP/rv32" --capture "$CAP/control" --capture "$CAP/store" --capture "$CAP/coverage" --capture "$CAP/memory"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" control 0 "$WORK/control-0"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" control 1 "$WORK/control-1"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" control 2 "$WORK/control-2"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" control 3 "$WORK/control-3"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" srp2 0 "$WORK/srp2-0"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" srp2 1 "$WORK/srp2-1"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" srp1 0 "$WORK/srp1-0"
python3 "$EVIDENCE/round19-continuation/scripts/campaign.py" srp1 1 "$WORK/srp1-1"
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 scripts/ci_rv32_sdk_selftest.py
python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32 --out "$WORK/image-selftest"
"$LITEX_PY" sw/litex/test_ctrl_memory.py
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_events.py --firmware-census
python3 "$EVIDENCE/round19/run_pin_controls.py" "$CANDIDATE" "$WORK/pins"
```

The remaining exact command receipts identify the earlier unchanged probe/campaign scripts and their disposable checkouts. The 54-command docs list is docs-final.log. The offline runner self-test was run only inside a disposable container; its receipt specifies the boundary. No candidate host-side orchestrator was executed.

Corrected attempts are retained without being presented as passes: the initial full memory capture lacked the CPU-generation environment; the final build-only capture needs only pinned Python imports and passes. The first size-gate run failed before the shared probe extraction; the unchanged ratchet now passes. The first disposable self-test placed stubs outside its fixed PATH; the corrected read-only stub location passes. A supplementary store `--self-test` run and two attempted slices each reached the 570-second command limit; **no complete 109-mutant store result is claimed**. Round 18's required store command omits `--self-test`; its 435-test execution and the store's coverage/build captures all pass. No gate was weakened to obtain a pass.

The registry's OUTSIDE meaning is explicitly limited to this control firmware; the separate BIOS build is disclosed above. The current head still needs independent review and protected hosted contexts after publication. Existing positive reviews cover `27ee16b5` only. No new review verdict is claimed, no PR comment/body was edited, and no push or merge was performed. The issue remains open. The new issue comment will report this head and this bounded evidence.

The prepared PR body follows the repository template and is below the publication size limit. Historical rounds 2–17 remain in the handoff archives and public issue history; the Round 18 residue section is preserved verbatim.

Final status: [A583] REVIEW READY posted as [issue #697 comment 6138131373](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6138131373) at `97e713168470bfae2685521fa557dc462b782b32`. No push. Work stopped after posting.



## Round 20

**REVIEW READY locally at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`**, on `697-consume`. The clean resumed head was `97e713168470bfae2685521fa557dc462b782b32`. Origin was verified as the assigned public repository. `git fetch origin dev` yielded `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`; its no-fast-forward merge is `a71b0e4149c26576499d05cacf2fa6fbfe27fb15`. There were no textual conflicts. The implementation is the single following commit, `d40e4e982`. Both subjects are one line with no body or trailers. No push, PR edit, rebase, amend, merge to dev or hardware operation was performed.

Authority: [Round 20 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6140933191), [composition review R584-18](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6139118335), #726 / PR #729, and #697 acceptance items 1–5 with its recorded pin rulings. This is implementation evidence; a new independent verdict and protected hosted contexts are still required.

### Changed files and classification

| File:line | Change and purpose |
|---|---|
| `tb/verilator/milan_dp/stream_counter_f5.py:40` | Adds --stack and build-only; shared pin verification runs before any staging or compilation. Build-only retains the same compile/link path and runs no tests or plants. |
| `sw/firmware/ctrl/test/ctrl_configs.py:122` | Registers both F5 shapes as the sixth mandatory independent capture. The Makefile classification states precisely that its firmware recipes delegate to that separately captured program. |
| `sw/firmware/ctrl/test/ctrl_plants.py:193` | Removing the F5 entry or its own capture is refused by name; neither can be covered accidentally by another builder. |
| `tb/verilator/milan_dp/Makefile:545` | Pins the aggregate run before compilation; counters, counters-f5 and counters-mutants each require stack-pin. F5 recipes forward STACK_DIR. |
| `sw/firmware/ctrl/test/ctrl_pin.py:695` | Census requires all three counter prerequisites, including the RTL-only counters entry. Four F5 dirty/off-pin arms cover direct execution and build-only. |
| `sw/firmware/ctrl/test/ctrl_pin_bench.py:11` | Moves the existing bench-control helper intact, then adds prerequisite-removal plants for the three counter entries; preserves the Python size ratchet. |
| `sw/firmware/ctrl/README.md:126` | Documents six captures, 103 boundary defects and 120 pin controls, including F5 and counter entry points. |
| `docs/testing/CI_WORKFLOWS.md:80` | Documents the mandatory two-shape F5 build-only capture in the existing firmware-boundary job; no workflow step is dropped or duplicated. |

F5 compiles the AECP core, mailbox adapter, mailbox/loop support and its test fixture against public stack headers. Its two independent runs recorded 30 compiler invocations containing 28 compiled sources, all rc 0. Both shape runs are attributed to F5 itself. The full boundary judges them along with the other five captures. The classification does not claim the Makefile compiles nothing: its own direct compiler recipes build RTL harnesses and its firmware build delegates to F5.

The assignment names `counters` and `counters-f5`; the actual Makefile also invokes F5 from `counters-mutants`. All three are pinned. `counters` is RTL-only, so an explicit census rule and a prerequisite-removal plant prevent its promised pin check becoming accidental. `run` is also pinned first so aggregate entry controls refuse before compiling. All these negative checks name the modified stack file rather than relying on a compiler failure.

R584-18-F1: the held-text probe reports zero program refusals; removing either F5 classification or its independent capture is caught. R584-18-F2: direct F5 and all counter entries reject a modified/off-pin stack before builds; poisoned-header controls never reach compilation; each prerequisite-removal plant fails the census. Four direct F5 arms plus the additional Makefile arms raise the shared pin population from 106 to 120. No production firmware, image input or pin changed after the merge.

### Dev changes inherited by the merge

Each row comes unchanged from fetched dev `e81ce82f`; the first changed line in the merge delta is named. The counter contract, RTL, fixture and behavior changes are PR #729's. The following implementation commit modifies only the eight files in the change table above.

| File:line | Source |
|---|---|
| `docs/README.md:93` | Inherited from dev `e81ce82f` |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/394_387_E1_SWITCH_CYCLES.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/667_TALKER_START_BENCH.md:4` | Inherited from dev `e81ce82f` |
| `docs/findings/B14_BENCH_5603C353.md:4` | Inherited from dev `e81ce82f` |
| `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:320` | Inherited from dev `e81ce82f` |
| `docs/reference/REGISTER_MAP.md:148` | Inherited from dev `e81ce82f` |
| `docs/testing/726_STREAM_COUNTERS.md:1` | Inherited from dev `e81ce82f` |
| `docs/testing/CI_WORKFLOWS.md:286` | Inherited from dev `e81ce82f` |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218` | Inherited from dev `e81ce82f` |
| `docs/testing/TESTING.md:513` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:182` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:27` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:32` | Inherited from dev `e81ce82f` |
| `hdl/ieee1722/crf/KL_crf_rx.sv:58` | Inherited from dev `e81ce82f` |
| `scripts/measure_test_evidence_readers.py:127` | Inherited from dev `e81ce82f` |
| `scripts/suite_shards.py:2` | Inherited from dev `e81ce82f` |
| `sw/firmware/ctrl/aecp/README.md:55` | Inherited from dev `e81ce82f` |
| `tb/tools/torture_campaign.py:68` | Inherited from dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_lockstep.cpp:9` | Inherited from dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_main_nx.cpp:16` | Inherited from dev `e81ce82f` |
| `tb/verilator/crf_rx/sim_main.cpp:98` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/Makefile:27` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/README.md:24` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:55` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_nxn.cpp:93` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.cpp:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.py:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.hpp:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.py:1` | Inherited from dev `e81ce82f` |
| `tb/verilator/tkdiag/sim_main.cpp:17` | Inherited from dev `e81ce82f` |
| `tests/features/counters_contract_milan.feature:42` | Inherited from dev `e81ce82f` |
| `tests/steps/counters_contract_steps.py:344` | Inherited from dev `e81ce82f` |
| `tests/steps/torture_plan_steps.py:298` | Inherited from dev `e81ce82f` |

### Images and pin proof

The chosen pin remains `405dc68310a18f669049ffc10cc23eef7300dcff`; lwSRP remains `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. The stack directory/top-level and its own public origin were checked before operations. No stack branch was modified or pushed.

`round20/pin-text-diff.txt` is the fresh complete seven-file diff against dev `e81ce82f`; `pin-tokens.log` proves identical non-comment tokens at identical line positions. `pin-continuity.txt` proves the seven dev inputs are unchanged since `c20c85bd`, so the retained six debug/release RV32 object equalities in `pin-proof.txt` still apply. The source files differ in comments and licence text under ruling 6092176555; source-text byte identity is not claimed. Linked-image byte identity is independently measured below.

All 65 fresh linked ELFs are equal by direct byte comparison, size and SHA-256: five standalone, 30 flat runtime and 30 split runtime variants, covering all five shipped shapes, both interface counts and all three compositions. Both complete manifests hash to `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584`. The standalone image comparison also reports +0 for every section at both default shapes. The 33 linked-image self-test controls pass.

| Image / shape / layout / composition | Dev bytes / head bytes | Dev SHA-256 | Head SHA-256 |
|---|---:|---|---|
| `ctrl_image/head/endstation_arty_4x4/ctrl_app.elf` | 50752 / 50752 | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` | `8c27ee19b7a4f0a6266834c43c50d8a397469c612fe86860ecc2296ae44ebb5e` |
| `ctrl_image/head/endstation_arty_8ch/ctrl_app.elf` | 50752 / 50752 | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` | `b7976d5cc2e0bc8889bbe471472e4817a6368df9a31d48ec8c2e8a1d63c23af7` |
| `ctrl_image/head/endstation_arty_current/ctrl_app.elf` | 50744 / 50744 | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` | `b119b2b56911120eeb424276525ca53d2e34340bf169bbb4a788efe65cb8a092` |
| `ctrl_image/head/endstation_ax7101_1x1_tdm8/ctrl_app.elf` | 50768 / 50768 | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` | `5a4086ce0245a5e2ad198aa0db56e62b982b7c4c6d177fe4929dca4da6b2dfff` |
| `ctrl_image/head/endstation_ax7101_8x8/ctrl_app.elf` | 50776 / 50776 | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` | `acb380ee815698bcd99f31920c09e55c3e93d44d7d09b4d1ae8f2d6a2a03c1bd` |
| `flat-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 68836 / 68836 | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` | `228c4d2d4da86158199c99b08a0b895661fec07eb56c9554fc2ad32ee0f276c4` |
| `flat-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` | `b25d258237bf6aa4005ce6a72ce0b36640c08a046e8e522c56e9759ead85d7a7` |
| `flat-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 127148 / 127148 | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` | `82e5ce706c7736fa6778c6477a5d43233415fac26efc851aaeb2776146ce34cf` |
| `flat-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70364 / 70364 | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` | `d11e73701465dc12654b1871f72a7b10f1ea2c6a2f69157f2b8ea9d5cd3d2d89` |
| `flat-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` | `77419321adfeed9057dbd7b67461dd807c78222422526ca822ea56b9ab39df03` |
| `flat-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 128676 / 128676 | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` | `a2dd25cfe83a2469fe03b63ab6804f44fa7c3f91134d338f4ddc642890c76288` |
| `flat-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 68836 / 68836 | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` | `fed8b54f96ec1c60797841de476947215550b234b3785442e88e96e1b8ed4be8` |
| `flat-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` | `b23e71ad89fe5f7d3e7d059ff8a4f9d48f6a69a71d6060ff166f088e8f7b0ca4` |
| `flat-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 132900 / 132900 | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` | `c2799ea46a854c45e54992800c3cdc93175a364193d41d37f2eefacb966d2118` |
| `flat-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70364 / 70364 | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` | `8da5b37b2527b7b6bf097126ac2c6f3ec39a705c7bdcb3095812d1417388bb0c` |
| `flat-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` | `f47dc12d5a6bbf98aabb6874b778d3867fbd0310998243b5f65046da42ced74c` |
| `flat-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 134428 / 134428 | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` | `57ad658eff2ddd7570fe64ef08afe51ccdacf23e1fcc98c2dfcf5893aed168c2` |
| `flat-endstation_arty_current-if1-srp/ctrl_app.elf` | 68412 / 68412 | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` | `7c8ecec43b7a6f829490d84ba46ef485265965188329ee4f412b8eae86d8d245` |
| `flat-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` | `f0f462ae82deb1f9613987c36f965fc05a94e3e727f49eb5c70d0a20becf45ae` |
| `flat-endstation_arty_current-if1-aecp/ctrl_app.elf` | 121416 / 121416 | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` | `7f2bac9275054548497234c7d8c5042c1525c822775f1391a394d7abb65ff4dc` |
| `flat-endstation_arty_current-if2-srp/ctrl_app.elf` | 69900 / 69900 | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` | `0ca8e6a97eafb7f628960c8fd7d6bf047887ecd16d4aa2728939793f8cc1aa0e` |
| `flat-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` | `3f40b9150068f56b9118493f9d7d21e1452137c504e826a8d10d86dc3c1d14df` |
| `flat-endstation_arty_current-if2-aecp/ctrl_app.elf` | 122912 / 122912 | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` | `31dd11a7820b681d494632ff41ec235bf563a9c5efa3d6cabc89821ae8389bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 68764 / 68764 | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` | `db0fb58e7ebfec18465210871c83e560c8f71f4149932775bf8423f5b7becb19` |
| `flat-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` | `a2bea49e78da57f9642592d753e71b7b67d928e0f3482f3fc5ea650694b69bba` |
| `flat-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 123612 / 123612 | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` | `74a12209e0301a9a7313861e6e944f972a3ba84374a147e476cf2f12814fdcda` |
| `flat-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70188 / 70188 | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` | `e052ed2b10e1ae3a65d0b4a0ab31b0d92e7bcd5379c525a4223c1a71f336ad47` |
| `flat-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` | `bf7e37a793f2a5cc12c171c4568359ac57464009da4931b6d00d8bb56d420ab3` |
| `flat-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125044 / 125044 | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` | `d3fc02d6916278dc6f43cc27e96920d68657dabe6f4cae7c3cfb26ee43e2ce14` |
| `flat-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 68868 / 68868 | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` | `b9bf08715abcd58e7b7a66781e1e27e9a6762d9560366f68df5c9b2b42487af4` |
| `flat-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35312 / 35312 | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` | `7dd3d0843ef5f97f2f0c58af62fb937561d9c4bb20c0defb33221c2412087f2f` |
| `flat-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 137332 / 137332 | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` | `1721078bbde9510b60ba82f4c4cf7cc0639709bc3b419c0aad1260eb407d5d99` |
| `flat-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70372 / 70372 | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` | `3fc8b8ab4ba24e7d89e0b932ddafa0cffc2f1b9762a17b4cbe0808165f0640aa` |
| `flat-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36184 / 36184 | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` | `104552602a5e5fb901f2a03058f8f0d498d3e6782c9b1ed2e79aeefb6359c04d` |
| `flat-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 138836 / 138836 | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` | `fbcf4230d2a5087f28659de75907f60a1f92304e747d3587eb1d40546c6e5e81` |
| `split-endstation_arty_4x4-if1-srp/ctrl_app.elf` | 69144 / 69144 | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` | `b63e6e61df8b020539f5676c824a9653c53422e534586372934bf06036d8072b` |
| `split-endstation_arty_4x4-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` | `1463ecabbae6d29453e7beaa48d5d87a2683df70bcf30b6ca196bb51093f4dc0` |
| `split-endstation_arty_4x4-if1-aecp/ctrl_app.elf` | 129740 / 129740 | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` | `bf536d4fca826822cc402bae4b6676ecb5ccb3087b2399c23b1bcbdcd1c96c09` |
| `split-endstation_arty_4x4-if2-srp/ctrl_app.elf` | 70672 / 70672 | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` | `78dcd5b43530f79482de5a860794f345a1e9b3284bf7d813cfe2441cda43c924` |
| `split-endstation_arty_4x4-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` | `05cc67f98e6a3b116e31758796b006d0d3359faef4d10988cce3a4ce80e6f6f1` |
| `split-endstation_arty_4x4-if2-aecp/ctrl_app.elf` | 129740 / 129740 | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` | `5b0fca5b8ba2780dec30679fb2d3e23f76ffccce2d9372d58f610c78787368b5` |
| `split-endstation_arty_8ch-if1-srp/ctrl_app.elf` | 69144 / 69144 | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` | `c3c00cb451fea423a03c6e3db549ef56d9ea2653b881567e65bdc71b2db267c3` |
| `split-endstation_arty_8ch-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` | `922a5273abcf495c9eb7738d6e189600056e05d74f944714aebe4d70b9f3e6ed` |
| `split-endstation_arty_8ch-if1-aecp/ctrl_app.elf` | 133836 / 133836 | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` | `4f7cb03c125fa28a46d2b0bd3543c71c769dee0c01bff4fd88d113cc65df02c0` |
| `split-endstation_arty_8ch-if2-srp/ctrl_app.elf` | 70672 / 70672 | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` | `cb658c5cc7e56ebf45bf868bf3a4e1b7a30bcd68946340af8051b9f44ec8017e` |
| `split-endstation_arty_8ch-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` | `9d0707575b07b5a28274601c0b8a67836e9b07b3f1da73640a477fd68c921c0d` |
| `split-endstation_arty_8ch-if2-aecp/ctrl_app.elf` | 137932 / 137932 | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` | `5e2f217ecae327bd2080066807017904485d9bfda4fa06085f8e7f24a44dd081` |
| `split-endstation_arty_current-if1-srp/ctrl_app.elf` | 68720 / 68720 | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` | `3e0bbb97b4d8cbe46f6e47d2a25997ddd081a014be4424399f46409c2a36667b` |
| `split-endstation_arty_current-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` | `6e2058af7af81fa722792273811f0ce0112090968663798322ae082dd7480b8a` |
| `split-endstation_arty_current-if1-aecp/ctrl_app.elf` | 125560 / 125560 | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` | `2ea3cfe7d7855ba6b0af93b9d01511f219f5ae6d72ccd367d165f93adb521b82` |
| `split-endstation_arty_current-if2-srp/ctrl_app.elf` | 70208 / 70208 | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` | `5126df88e5ca3ec3045dfef82d1627c41d21f707c6301d9da9011fe6be550171` |
| `split-endstation_arty_current-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` | `039953b2c8ba10f8b149d29a7e119e28f44859e52ba261d1991de0adcc93e574` |
| `split-endstation_arty_current-if2-aecp/ctrl_app.elf` | 125560 / 125560 | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` | `2b21101556ea642a82a2abf709d5f1060ff96101bcacfdba8cbe9de0e2ab7ad5` |
| `split-endstation_ax7101_1x1_tdm8-if1-srp/ctrl_app.elf` | 69072 / 69072 | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` | `98a4d3efbb0a736348536497e971a5d1de2c5ecfb3b36eedf1cba40d7cfe73af` |
| `split-endstation_ax7101_1x1_tdm8-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` | `699bfb5e60dd2c1c2eb75a0261c50a4148957541cd8d9de44e12d1684e9d8aeb` |
| `split-endstation_ax7101_1x1_tdm8-if1-aecp/ctrl_app.elf` | 125588 / 125588 | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` | `7b9abdfa85028610c96e38e07ea5159875bb92ada730e16dca7c8b1671866715` |
| `split-endstation_ax7101_1x1_tdm8-if2-srp/ctrl_app.elf` | 70496 / 70496 | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` | `b2f0a89354e41dcb4098915a3beab592ca3be1283a7467f9058f1829f5b8832e` |
| `split-endstation_ax7101_1x1_tdm8-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` | `cf66960c3ff7dc948dcea77455c30eb42bbccc7e6f1b7dbc60a7a04e2bf053aa` |
| `split-endstation_ax7101_1x1_tdm8-if2-aecp/ctrl_app.elf` | 125588 / 125588 | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` | `27dc78da865f00feed7f60f7e4fd56c55a75dfb518bb999e1c22200cc81201d2` |
| `split-endstation_ax7101_8x8-if1-srp/ctrl_app.elf` | 69176 / 69176 | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` | `894962e6880e272e6e6c4aaf19501ae1829a4023110d57c6b5f518b5f8b6ec17` |
| `split-endstation_ax7101_8x8-if1-nosrp/ctrl_app.elf` | 35624 / 35624 | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` | `9f3cd2b5abd3aa48e5874235baedb63577f5fa26f12e718ef9127033f540cea0` |
| `split-endstation_ax7101_8x8-if1-aecp/ctrl_app.elf` | 138268 / 138268 | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` | `dcd58b96a87d53d42b60c73031e3dd8db4927b7b76b409656aaa3173d09c16d7` |
| `split-endstation_ax7101_8x8-if2-srp/ctrl_app.elf` | 70680 / 70680 | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` | `27d72c579ac3e444993db59119237cc6992c8ce6d1a2e5f73cee2b3ab7b1bfe9` |
| `split-endstation_ax7101_8x8-if2-nosrp/ctrl_app.elf` | 36496 / 36496 | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` | `2a5f6bfe67506d516270656e2444dae12d302bd57e42e36da513fbbb5057bbac` |
| `split-endstation_ax7101_8x8-if2-aecp/ctrl_app.elf` | 142364 / 142364 | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` | `60190c0fa70a22c9c5d2ac93c4d906b38b9aff65358c708ee90d16f5fc85a464` |

### Gates and planted controls

Every final required command has rc 0. Negative plants intentionally return nonzero inside their enclosing self-checking command. `round20/receipts.json` records every exact argument vector and elapsed time; `logs/docs-head.log` lists all 54 documentation commands individually. Raw files too large for this packet are represented by size/SHA-256 in `raw-artifacts.json`, with verdict extracts where useful. No binary, toolchain, package or tree export is in the packet.

| Gate / population | Result | Planted control or independent comparison |
|---|---|---|
| Six compiler captures and firmware boundary | 2852 sources / 3082 invocations; no findings | 103 defects + 8 admitted controls + 1 baseline = 112; all expected, including F5 registry/capture deletion |
| Verilator boundary | 829 sources / 926 invocations; no findings | Five defects + baseline = 6; mailbox co-simulation, MAAP differential and both AECP wire shapes pass |
| Shared pin / census / figures | 120 / 4 controls, none misbehaved | Both Git 2.43/2.56 and CPython 3.12.3/3.14.7; dirty bytes, off-pin, object-store/configuration attacks and prerequisite removal |
| Entry points | 27 × 12 = 324 named refusals | Original 21 plus F5 shapes/build-only and all three counter targets; replacement/forged objects, attributes, transport configuration and mode changes |
| Hook rules | H0 clean; H1–H24 caught on both Python versions | Each audit-hook rule removed independently |
| Configuration variants | 21 per Git version, expected table below | Clean baseline; individual configuration checks weakened; no new escape or lost detection |
| Four shard entry forms | Four refuse edited header; four escape when pin line removed | Standalone driver pin-removal control |
| Earlier unchanged review probes | All eight scripts rc 0 on each Git | Spelling, sparse index, promisor transport and object-store probes; detailed retained logs |
| Firmware execution/mutations | All 915 verdicts pass | 60 arms, 506 control, 76 AECP, 198/73 SRP, two lwSRP pin controls |
| Store execution | 435 tests across five shapes | Existing failure/reset/order/boundary cases; coverage reader controls below; no 109-mutant campaign claimed |
| Memory | Full suite passes; 44 mutants caught | Existing reset, split-memory and initialization plants |
| Coverage | 30 files; identical normalized head/dev table | Same compiler; unchanged exclusions; 29/29 reader controls |
| Listener / SDK / RV32 / image readers | All pass | 18 listener mutants, 25 SDK tests, RV32 diagnostic plants and 33 image controls |
| CI event contract / firmware census | 2169 checks; 3064 self-test arms; preserved census | 16 additional workflow plants caught; shard proof 916 invocations in exactly one shard |
| Disposable runner | 446 self-test arms pass | Network disabled, read-only candidate, no socket or credential forwarding; never candidate host-side orchestration |
| Documentation/source-list/evidence/idioms | 54/54 commands pass at committed head | Their standing self-tests, missing-input and evidence-reader plants; no ratchet increased |
| #726 baselines and original defect controls | Both shapes, frames-only, MAKEFLAGS=-w pass | Both before variants fail only the required original TX/RX/CADENCE groups |
| #726 counter mutations | All 12 RTL shape/variant cases pass | Eleven named variants; egress-stall also at 8×8; every detection has a passing check-omission run |
| F5 | Both baselines and direct make target pass | late/rate/fixed-grid each detected, then passes with its named check omitted; build-only runs no tests |
| #726 behavior / campaign / scheduling | 406 scenarios, 1977 steps; self-tests pass | Counter laws and phase/cadence cases; torture campaign self-test and suite shard controls |

The six capture phases plus judgement total 836.79 seconds locally (46.5% of the existing 30-minute timeout, below its 1080-second 60% ceiling). This excludes dependency installation and is a sum of bounded foreground commands, not a new hosted timing. Verilator boundary took 511.49 seconds (21.3% of its 40-minute timeout). Prior hosted budget evidence remains historical; this head has no new hosted acceptance.

### Coverage table

Same GCC/gcov 16.2.1 and GoogleTest 1.18.0 on candidate and dev. Counts below are raw covered/total; percentages are after the unchanged documented exclusions. Every normalized row is identical on both sides.

| File | Dev/head lines | Dev/head branches | After exclusions |
|---|---:|---:|---|
| `sw/firmware/ctrl/acmp/acmp_mbx.c` | 79/79 | 28/28 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/acmp/acmp_nvm.c` | 38/38 | 10/10 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp.c` | 357/357 | 308/308 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_commands.c` | 424/424 | 362/362 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_image.c` | 77/77 | 80/80 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_maps.c` | 222/222 | 290/290 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_mbx.c` | 101/101 | 40/40 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_nvm.c` | 102/102 | 86/86 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/aecp/aecp_state.c` | 63/63 | 69/69 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app.c` | 42/43 | 40/44 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | 107/107 | 64/64 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/app/ctrl_app_srp.c` | 82/82 | 62/62 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 101/101 | 62/62 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 99/99 | 64/64 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/mbx/mbx.c` | 243/243 | 102/102 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl/srp/srp_mbx.c` | 540/540 | 486/486 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/199 | 106/110 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100.00% lines / 100.00% branches |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/include/wire.h` | 10/10 | 2/2 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/acmp.c` | 767/767 | 362/362 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/adp.c` | 204/206 | 95/102 | 100.00% lines / 100.00% branches |
| `third_party/tsn-c-stack/src/maap.c` | 209/209 | 140/140 | 100.00% lines / 100.00% branches |

### Mutation tables

The full 915 named results are in `round20/firmware-verdicts.txt`. Disjoint campaign populations are retained as JSON; no item is dropped or counted twice.

| Population | Count | Result |
|---|---:|---|
| Control slices | 127 / 127 / 127 / 125 | 506 caught |
| AECP | 76 | 76 caught |
| SRP two interfaces | 99 / 99 | 198 caught |
| SRP one interface | 37 / 36 | 73 caught |
| lwSRP pin | 2 | 2 caught |
| Memory | 44 | 44 caught |
| Listener | 18 | 18 caught |
| Boundary defects / admitted / baseline | 103 / 8 / 1 | All expected |
| Verilator boundary defects / baseline | 5 / 1 | All expected |
| Pin / figure | 120 / 4 | All expected in four environments |
| CI workflow plants | 16 | 16 caught |
| RTL counter mutants | 11 + egress-stall at second shape | 12 detected and 12 omission escapes |
| F5 counter mutants | 3 | 3 detected and 3 omission escapes |

| Configuration variant | Git 2.43 | Git 2.56 |
|---|---|---|
| N0 none | rc 0; 0 escaped | rc 0; 0 escaped |
| N1 the superproject check not called | rc 1; 7 escaped | rc 1; 7 escaped |
| N2 the superproject check after the index is read | rc 1; 5 escaped | rc 0; 0 escaped |
| N3 the superproject's local scope only | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 extensions.partialclone not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.promisor not refused | rc 1; 4 escaped | rc 1; 4 escaped |
| N4 remote.partialclonefilter not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N4 remote.uploadpack not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.sshcommand not refused | rc 1; 1 escaped | rc 1; 1 escaped |
| N4 core.fsmonitor not refused | rc 1; 2 escaped | rc 1; 2 escaped |
| N5 the helper's own command-line setting refused in the superproject | rc 1; 0 escaped; clean proof refused | rc 1; 0 escaped; clean proof refused |
| N6 no HELPER_CONFIG | rc 0; 0 escaped | rc 0; 0 escaped |
| N7 no GIT_NO_LAZY_FETCH | rc 0; 0 escaped | rc 0; 0 escaped |
| N8 neither the superproject check nor GIT_NO_LAZY_FETCH | rc 1; 7 escaped | rc 1; 7 escaped |
| N9 neither the superproject check nor HELPER_CONFIG | rc 1; 7 escaped | rc 1; 7 escaped |
| P1 round 16's match: a remote key with a named subsection only | rc 1; 3 escaped | rc 1; 3 escaped |
| P2 a remote key with a subsection, named or empty, only | rc 1; 2 escaped | rc 1; 2 escaped |
| P3 a remote key with a named subsection or none only | rc 1; 1 escaped | rc 1; 1 escaped |
| P4 the stack's `*` family holding an empty subsection too | rc 1; 1 escaped | rc 1; 1 escaped |
| P5 parsed_key reading an empty subsection as none | rc 1; 1 escaped | rc 1; 1 escaped |
| P6 parsed_key reading no subsection as an empty one | rc 1; 51 escaped; clean proof refused | rc 1; 51 escaped; clean proof refused |

N6/N7 remove isolated defense-in-depth settings while the primary check remains; their zero escapes are expected and are not kills. N2 retains its known Git-version difference. N5/P6 over-refuse the clean proof. P6 retains its 51 affected controls before its expected setup refusal; its original detections remain. H0–H24 and each #726 named group/omission result are retained in the gate logs.

### Reproduction, corrections and limits

Use CPython 3.12.3, the pinned RV32 SDK and Verilator 5.050, `VERILATOR_JOBS=2`, campaign `--jobs 4`, disk `TMPDIR` and the pinned Python requirements. `WORK`, `CAP`, `CANDIDATE`, `DEV`, `EVIDENCE` and `RUNTIME_ROOT` are caller-selected paths; the runtime root supplies the same `runtime` and `runtime-freestanding` archives. The retained Round 19 reproduction block applies with the sixth capture added and the dev reference changed to e81ce82f. Exact command receipts cover every additional campaign.

```sh
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/f5" -- python3 tb/verilator/milan_dp/stream_counter_f5.py --build-only --shape 1 --work "$WORK/f5-1"
python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$CAP/f5" -- python3 tb/verilator/milan_dp/stream_counter_f5.py --build-only --shape 8 --work "$WORK/f5-8"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator --capture "$CAP/rv32" --capture "$CAP/control" --capture "$CAP/store" --capture "$CAP/coverage" --capture "$CAP/memory" --capture "$CAP/f5"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 "$EVIDENCE/round20/scripts/held_text_probe.py" "$CANDIDATE"
python3 "$EVIDENCE/round20/scripts/images.py" "$CANDIDATE" "$WORK/images-head"
python3 "$EVIDENCE/round20/scripts/images.py" "$DEV" "$WORK/images-dev"
python3 sw/firmware/ctrl/test/ctrl_image.py --base e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c --out "$WORK/image-delta"
make -C tb/verilator/milan_dp counters-f5
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" tx-interval rx-interval tx-reset aaf-reset
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" crf-reset rx-saturation late rate
python3 "$EVIDENCE/round20/scripts/stream_group.py" "$WORK" tx-nodirty fixed-grid egress-stall egress-stall@8
```

Corrected attempts remain visible. The first documentation run caught the expanded pin module's size; extracting the existing bench helper fixed it without changing the ratchet. A clone-verification path typo was corrected before use. The first configuration run reused a disposable stack store previously unpacked for forged-object entry controls; cleanup raced automatic maintenance. Those setup failures are excluded, and both complete configuration tables come from fresh independent stores. No failing plant is counted as a successful mutation kill merely because its setup failed.

The service briefly exceeded the requested 9 GB working target: recorded peak 11,070,345,216 bytes, with no OOM event. Overlap was reduced and only this task's file cache was reclaimed. Subsequent monitored samples remained below the target. At most two simulation builds ran at once; no campaign used more than four workers. All runs were foreground commands below the ten-minute command limit; no hardware or Vivado run occurred.

R584-17-RES-1 and R585-18's corresponding pushed-head residue are applied to the prepared PR body's historical Round 19 statements. R584-17-RES-2's historical README citation is corrected to line 193, with the current line 196 called out. The earlier R585-16 prose residue remains explicitly quoted and carried as assigned. No existing issue/PR comment was edited, and the PR itself was not edited.

No coverage row, required mutation kill or #726 regression was lost. The historical supplementary 109-mutant store campaign is not claimed; the required store execution command passes. The full exhaustive repository sweep, Yosys/Vivado gates, protected hosted contexts and PR-head local replica are not claimed for this unpushed round. Independent review, publication and the later merge-validation bar remain the manager's work. The issue remains open. The prepared new issue comment reports this exact head and bounded local evidence; after posting REVIEW READY, work stops.


### Final inherited unit-suite supplement

The merge audit checked the changed unit fixtures directly in disposable checkouts, in addition to the parent-MAC counter campaign. All four command groups return rc 0:

| Command | Result / standing control |
|---|---|
| `make -C tb/verilator/tkdiag` | 99 checks, zero failures; five mutation checks pass |
| `make -C tb/verilator/avtp_rxmon` | Single/multiple-context tests pass; lockstep 36 checks at each shape; five mutation checks pass |
| `make -C tb/verilator/crf_rx run` | Counter, 2201-check discontinuity and connected-talker simulations pass |
| `make -C tb/verilator/crf_rx mutants` | Ten positive/negative checks pass; six receiver and two servo defects detected |

These legacy Makefiles spell build concurrency literally. A scratch launcher changes only `-j`'s value to 2 and forwards every remaining argument to the supplied pinned 5.050 executable. Its portable source is `round20/scripts/verilator-two.py`; set `PINNED_VERILATOR` to that executable and `VERILATOR` to the launcher. No source/expectation/timing flag changed. At most two builds ran together.

`round20/population-continuity.json` confirms every control/SRP population equals Round 19's, including each disjoint slice. `round20/verdict-continuity.json` confirms all 915 sorted verdict lines are identical, not just their count. The final packet contains 66 passing main command groups plus the seven separately recorded quick checks and the 54-command documentation list. The working tree remains clean at `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
