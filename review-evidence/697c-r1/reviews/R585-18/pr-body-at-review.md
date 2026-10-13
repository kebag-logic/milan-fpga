[A583]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Round 18](#round-18)
- [Round 19](#round-19)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

**REVIEW READY locally at `97e713168470bfae2685521fa557dc462b782b32`**, following merge `95ca54cb` of dev `d5858bbe` (M8a, PR #721). The scope extension in #697 comment 6137497435 is implemented: the reset-entry compile is a fifth mandatory capture, the other programs have explicit classifications, and five new boundary controls pass. All 65 linked images equal dev byte for byte; the pin is unchanged. Both boundary sides, all 915 firmware verdicts, 30-file coverage, the pin/entry-point/hook/configuration campaigns and the required documentation gates pass locally. This head is unpushed and still needs independent review and protected hosted evidence. Earlier reports below describe their named heads.

`697-consume` -> `dev`. REVIEW READY: [issue #697 comment 6138131373](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6138131373). Earlier implementation and review history is recorded in #697 and #705; the current merge and continuation evidence is in Round 19 below. The Round 18 section retains the exact review-requested timing and pushed-head corrections.

## Linked Issue / roles

Relates to #697

Executor: `[A583]`
Internal cleared-context reviewer: `[R584]`
External reviewer: `[R585]`

## Description

milan-fpga now takes its ADP, ACMP and MAAP cores and the wire layer from the
[tsn-c-stack](https://github.com/kebag-logic/tsn-c-stack) submodule at
`third_party/tsn-c-stack`, and no longer holds copies. No firmware behaviour
changes: all 65 linked RV32 variants are byte-identical to dev `d5858bbe`.

| Piece | Change |
|---|---|
| Submodule | `third_party/tsn-c-stack` pinned at `405dc68310a18f669049ffc10cc23eef7300dcff` (round 13; round 1's `1a9f651c` plus F-INT's ACMP `publish` port, tsn-c-stack PR #22, kept by the tag `milan-fpga-697-pin-405dc683`), whose cores are dev's code token for token and line for line. `.gitmodules`, `scripts/act_ci.py` `TRUSTED_SUBMODULES` (with four new refusal arms), the submodule map, its diagram and `THIRD_PARTY.md` (MIT). |
| Copies removed | `git rm` of `adp.{c,h}`, `acmp.{c,h}`, `maap.{c,h}`, `wire/wire.h` and the core-test copies `test_acmp.cpp`, `acmp_fake.hpp`, `test_adp_reentry.cpp`, `test_maap_debug.cpp`; the core cases of `test_adp.cpp` and `test_maap.cpp` go too, their adapter and CSR cases stay. |
| Build | `ctrl_build.py` names the cores `tsn-c-stack/src/*.c` in the same link order and includes only the stack's `include/`; the arms build the stack's own core tests into the same binaries under the same tally labels (`fw_gtest_label.cpp` for a binary whose test files name no label). The `mbx` bench Makefile, the SRP arms, the MAAP differential and both image fixtures build from the stack. |
| Evidence readers | `ctrl_image.py --base` and `ctrl_srp_image.py --ctrl-source` measure a pre-move tree with its own cores and a later one with its recorded stack. |
| Coverage | `fw_coverage.py` measures the stack's `src/` and `include/` (never its tests or examples), with a new planted case; the ratchet is regenerated through its generator. Current candidate and dev coverage tables agree at 30 files under the same compiler; all lines and branches pass after the unchanged exclusions. |
| Mutation tables | Core plants name the stack's files; 43 plants whose anchor was a comment the stack removed take the stack's own re-anchored text; every planted program is token-identical to dev's. Two killers take the stack's words, see below. |
| Boundary | New `ctrl_boundary.py`, judging exactly the sources a capture of the firmware's builders' compiler invocations recorded as compiled (`ctrl_capture.py`, round 5), each by the compiler's own dependency output for that invocation (`-M` and `-H` with its own arguments, directory and environment, round 7), every file a compile read classified by where it lives. A compile of a firmware source (the saved-state store's and the images' own included) reads no stack file outside `include/`, and no firmware file includes one in any compile; a compile of a stack source reads, through its own `#include` lines, only the stack's files and the C implementation's headers, and no stack file includes anything else; the stack's tests reach nothing of this repository outside the submodule; no file under `sw/firmware` is named as a stack source or header; and the stack's own `scripts/check_boundary.py` runs. |
| Pin check | One shared check, `ctrl_build.stack_pin` (`ctrl_build.py --stack-pin` for the Makefile), proves the stack's content: every file of its sources, headers, tests, examples, scripts and CMake files must hash to the gitlink's tree, with nothing added, read from the files rather than the index. The host test (with coverage), the boundary gate, the MAAP differential in both modes, the mailbox bench and both image fixtures with the submodule as their stack run it first; in a Makefile, every target whose recipe builds against the stack has it as a prerequisite (`ctrl_pin.py`, round 3). |
| CI | `firmware-unit`, #716's three mutation jobs (round 18) and the Verilator shards fetch the submodule; two new required jobs judge the boundary: `firmware-boundary` (round 8) runs every known builder but the Verilator ones by its builds under the gate's own capture, and `firmware-verilator` (round 6) the Verilator ones; `firmware-unit` runs its suites with no capture; `scripts/ci_events.py` pins all of it. |
| Docs | A "TSN stack submodule" section in `sw/firmware/ctrl/README.md` (what it provides, what it must not depend on, its tests, MIT inside this CERN-OHL-W platform), and every reference to the old paths; `README.md`, `QUICKSTART.md` and `CONTRIBUTING.md` initialise the submodule wherever every Verilator suite runs. Links into the stack use pinned URLs, since the docs gates run without submodules. |

Two killers changed words, not kills: the stack's two A29 tests now assert the
admission and withdrawal counts first, so `acmp-admit-ignores-another-talker`
and `acmp-reset-forgets-the-admitted` fail the same tests on the stack's words.
Its own table uses those words.

## Round 18

This historical section retains the review-requested corrections. Its references to earlier round sections refer to the public issue history and the archived handoff. Current results follow in Round 19.

[R584-15](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6126637070) and [R585-16](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6126287004) were POSITIVE at `5b4ea551`. #716 then merged as dev `dc4d06cb` ([PR #724](https://github.com/kebag-logic/milan-fpga/pull/724)): it splits `firmware-unit` into four required firmware jobs. The [assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6130298041) merges it with both sides standing and no other change. `git merge --no-ff` of dev `dc4d06cb` on `5b4ea551` stopped in the four conflicts the assignment names, and is committed as `ddbd7fd7`; one commit follows, `27ee16b5`. No rebase, amend, push or PR edit.

| File | Resolution |
|---|---|
| `.github/workflows/rtl-fast.yml` | Dev's file, with this lane's changes. All four firmware jobs fetch `third_party/tsn-c-stack`, since each builds the firmware whose ADP, ACMP and MAAP cores it holds. `firmware-boundary` and `firmware-verilator` follow dev's four jobs unchanged. The aggregate's `needs`, environment and loop are dev's list plus this lane's two. Parsed, every other job equals both parents'; dev's four equal dev's but for the fetch line |
| `scripts/ci_events.py` | Both constant blocks; the aggregate's inherited environment is the union. `RV32_REQUIRED_STEPS` keeps this lane's entries, takes `firmware-unit`'s step name from `FIRMWARE_PHASE_STEPS` and gains each mutation job with its phase step. Every missing-compiler control dev planted is still planted, and `firmware-boundary`'s too. Dev's census, budget rows and their arms merged as dev wrote them. The three new jobs' contract fetch derives from `firmware-unit`'s, so it requires tsn-c-stack |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py` | Dev's phase dispatch with this lane's `--build-only` and `BUILT` verdict. `--build-only` refuses `--self-test`, and `--shard` requires it, so the two never combine. The stack pin check stays in `main` before the first build, so every phase runs it |
| `docs/testing/CI_WORKFLOWS.md` | The docs-only skip names all six jobs. Three lines of the firmware bullet that the split made false now read: each of the four jobs initializes tsn-c-stack, none runs a capture, and the budgets are #716's table (this lane's single-job budget lines are gone). One line says the aggregate also requires the two boundary jobs |

One semantic conflict, which Git could not see. The boundary gate finds by text every program that names the firmware's tree, and refuses one that its registry does not classify. Dev's new `test_ctrl_firmware_shards.py` is such a program. At the merge, `firmware-boundary`'s step built every builder, then refused it by name (rc 2). `27ee16b5` lists it in `ctrl_configs.OUTSIDE` as a program whose compiles are none of the firmware's, as round 13 did for dev's publication census. That is measured, not assumed: under the gate's own capture it ran with no compile recorded. `ctrl_configs.py` is loaded only by the boundary gate's modules. No firmware, image input or pin changes.

Planted controls of the resolution: each choice undone alone is refused by `ci_events.py --check`, 15 of 15. These are each firmware job's fetch without tsn-c-stack, a boundary or mutation job dropped from the aggregate's `needs` or its loop, `firmware-unit` without `--shard 0/4`, a job removed, `--require-rv32` dropped and a budget row dropped. With the stack edited, each `--shard i/4` form refuses naming the file before any build. With the pin line taken out of `main`, none refuses.

| Job | Timeout | Hosted maximum | Of the timeout | Replica, head / dev beside it |
|---|---|---|---|---|
| `firmware-unit` | 45 min | 703 s (#716) | 26.0 % | 589 / 590 s |
| `firmware-control-mutants` | 45 min | 841 s (#716) | 31.1 % | 888 / 860 s (at the merge `ddbd7fd7`; 763 s alone at the head) |
| `firmware-aecp-mutants` | 45 min | 260 s (#716) | 9.6 % | 183 / 182 s |
| `firmware-srp-mutants` | 45 min | 625 s (#716) | 23.1 % | 571 / 569 s |
| `firmware-boundary` | 30 min | 834 s (this lane, at `5b4ea551`) | 46.3 % | step 691 s |
| `firmware-verilator` | 40 min | 737 s (this lane, at `8aaa2da7`) | 30.7 % | step 488 s |

#716's figures are from its ten hosted runs at `f41e4f2d`. This lane's are from its four hosted runs that ran both boundary jobs. Each job ran beside dev's in the replica (the control job at the merge `ddbd7fd7`, whose control-gate code the head does not change), and the ratios (0.998 to 1.033) show this lane adds no material time to #716's jobs. Scaling #716's maxima by them gives at most 32.2 %; #716's own calibration formula gives at most 36.7 %. Every job is within 60 %.

At the head, in the runner's Ubuntu 24.04 replica on four CPUs: `firmware-boundary`'s step PASS in 691 s (105, 106 and 4 controls, 0 misbehaved). `firmware-verilator`'s PASS in 488 s (6, 106 and 4). The four firmware jobs' commands each end `test_ctrl_firmware: PASS`, and their 915 verdict lines, every one `[ok]`, equal round 17's single run line for line. Coverage is 100 % in 30 files with every row unchanged; the store passes 435 tests. 35 of 35 RV32 images are byte-identical to dev `dc4d06cb`'s, and `ctrl_image.py --base dc4d06cb` gives `+0` in every section. The CI contract: 2169 items, 3064 self-test arms, the firmware census preserved; the shard proof: 916 invocations, each in exactly one shard. The act self-test passes, 446 arms. Every entry point that pins the stack (21, the four shard forms new) under twelve states is refused by name before any build: 252 of 252. The hook-rule campaign catches 24 of 24 on CPython 3.12.3 and 3.14. 106 pin controls, 0 misbehaved, on Git 2.56.0 and upstream 2.43.0. The round-17 mutants and the earlier reviewers' probes print what they printed at `5b4ea551`. The docs job: 53 of 54, the `MAKEFLAGS=w` source-list self-test failing 2 of 50 as at dev `dc4d06cb`.

Residue: R584-15-RES-1 is applied in the Round 17 section's item (d), as its exact fix states. R585-16-RES-1 is carried, not applied, since round 18 allows no other change. Its exact fix: in `sw/firmware/ctrl/README.md:181`, "and no key that names a program, a promisor remote or its transport." becomes "and no key that has Git start a program or declares a promisor remote or its transport while the pin is decided (a remote's or a submodule's `url` may name any transport, but no command of the proof contacts a remote)."; in `ctrl_build.py:199`, "None names a program or a store." becomes "None has Git start a program or fetch while the pin is decided."; in `ctrl_build.py:551-552`, "and no key of it names a program, a promisor remote or its transport." becomes "and no key of it has Git start a program, or declares a promisor remote or its transport, while the pin is decided.". R584-15-S1 and R585-16-S1 are optional and not taken.

Open, for the manager:
- (a) `27ee16b5` is the one change beyond the four conflicts; it touches no firmware, image input or pin, which is why it was not taken as a STOP;
- (b) R585-16-RES-1 waits for a round that allows a text change;
- (c) #716's hosted acceptance at the new head, ten consecutive runs, is the manager's; the head was pushed after this section was prepared, and its hosted runs are the manager's to accept;
- (d) `check_rtl_source_lists.py --selftest` fails 2 of 50 under `MAKEFLAGS=w`, at dev `dc4d06cb` too.

## Round 19

Relates to #697. Head `97e713168470bfae2685521fa557dc462b782b32` follows merge `95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62`, whose parents are `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` and dev `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` (M8a, PR #721). No rebase or amend.

The sole textual merge conflict was `sw/firmware/ctrl/test/ctrl_srp_image.py`. The resolution preserves dev's split memory planner, firmware-owned reset entry, linker and `--layout`, together with the lane's `--stack-source`, `source_tree` pin check, legacy-source handling and stack source selection. No linked-image check was removed or duplicated. Every other dev change is inherited unchanged.

The boundary then refused three newly discovered programs. The [scope extension](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6137497435) authorizes their classification and the reset-entry capture. The continuation changes are:

| File:line | Result |
|---|---|
| `sw/firmware/ctrl/test/ctrl_configs.py:121` | `test_ctrl_memory.py --build-only` is the fifth mandatory firmware capture; its shared probe module is PART_OF that builder at line 140. |
| `sw/firmware/ctrl/test/ctrl_configs.py:150` | `ctrl_memory.py` is OUTSIDE because it reads ELF data and plans banks without compiling. |
| `sw/firmware/ctrl/test/ctrl_configs.py:151` | `milan_soc.py` is OUTSIDE for this control firmware: it reads a prelinked control ELF at line 2765, marks the ROM initialized at line 2774 and excludes shipping software in control-mailbox mode at line 4217. Its separate BIOS/milan_baremetal path builds other firmware; the reason names that distinction explicitly. |
| `sw/litex/ctrl_memory_probe.py:19`, `sw/litex/test_ctrl_memory.py:951` | The unchanged probe/link helper is shared by the full suite and a build-only entry point. Build-only requires RV32, links the existing reset entry, and runs no tests or CPU generation. The extraction keeps the existing module-size ratchet. |
| `sw/firmware/ctrl/test/ctrl_plants.py:193` | Each program's unclassified copy is refused; dropping the fifth capture is refused; a private stack include in the reset entry is caught through that capture. |
| `.github/workflows/rtl-fast.yml:499`, `scripts/ci_events.py:2450` | The existing boundary dependency step adds the pinned LiteX Python imports, and the CI contract holds that exact command. |
| `docs/testing/CI_WORKFLOWS.md:76`, `sw/firmware/ctrl/README.md:126` | Describe the fifth capture, classification reasons, dependencies and revised 101-defect firmware boundary population. |

The compiler census finds the reset source only in the fifth capture: zero occurrences in each old capture, exactly one in the added capture. Its baseline dependencies are the reset source and the compiler's own predefinition header. The forbidden-header plant is caught by name. The no-RV32 control exits 2 before compiling. The probe and link function have identical ASTs before/after extraction, and their compile argument sets match.

| Validation at the continuation head | Result |
|---|---|
| Linked images, every shape/composition | 65/65 ELFs equal dev by direct bytes, size and SHA-256: five standalone, 30 flat runtime, 30 split runtime |
| Firmware boundary, five fresh captures | 2824 sources / 3052 invocations; zero findings; 110 boundary, 106 pin and four figure controls, zero misbehavior |
| Verilator boundary, autonomous capture | 829 sources / 926 invocations; zero findings; six boundary, 106 pin and four figure controls, zero misbehavior |
| Firmware execution and mutations | 915 passing verdicts: 60 arms, 506 control, 76 AECP, 198/73 SRP and two lwSRP pin controls |
| Store execution | 435 tests across five shapes; RV32 builds pass |
| Coverage | 30 files, 100% lines/branches after unchanged exclusions; candidate and dev have identical normalized rows under the same compiler; 29/29 reader controls pass |
| M8a memory test | Zero failures, 44/44 mutants caught |
| Harness, SDK and image checks | Listener 18/18 defects caught; RV32 17 checks, SDK 25 tests and linked-image 33 checks pass |
| Entry points and shard pin-first controls | 252/252 named refusals; all four firmware forms lose the pin refusal only under the control deleting the check |
| Pin, hook and configuration campaigns | 106 pin/four figure controls per environment; Python 3.12.3 and 3.14.7, Git 2.43.0 and 2.56.0; H0 clean/H1–H24 caught; all 21 N/P variant outcomes retain Round 18's results |
| Earlier review probes | Eight unchanged scripts on each Git retain expected outcomes, including subsection-less and empty-subsection keys with RAN=0 |
| CI contract and documentation gates | 2169 checks, 3064 self-test arms, 16 extra workflow plants and all 54 documentation/source-list/evidence commands pass |
| Disposable runner self-test | 446 arms pass inside the disposable boundary |

The image manifests on both sides hash to `96f55deba3b69b224fb838b746f559b3c944b552c694cef3211470d8b11db584`. The handoff retains every per-shape before/after size and hash. The tsn-c-stack pin remains `405dc68310a18f669049ffc10cc23eef7300dcff`; the lwSRP pin is unchanged. The seven dev core files are unchanged from the selected pin's retained source/token comparison. Comments differ as already documented; source-file byte equality is not claimed. The continuation changes no production firmware, image input or gitlink.

The boundary's measured local phases total 800.64 seconds; adding the measured pinned-package installation gives 836.57 seconds, 46.5% of its unchanged 30-minute timeout, below the 1080-second 60% ceiling. This is a sum of bounded local commands, not a new hosted job measurement. Round 18's hosted maximum remains 834 seconds. Verilator boundary took 472.53 seconds locally, 19.7% of its 40-minute timeout. The four earlier firmware jobs and their hosted budget evidence are unchanged.

Control and SRP campaigns were partitioned into disjoint slices of the unchanged tables and functions for the command limit; no mutation was omitted or duplicated. The candidate and dev coverage rows agree under GCC 16.2.1. The older GCC 13.3 report counts `srp_mbx.c` as 539 lines, versus 540 now, all covered. Of 915 firmware verdict lines, 914 are identical to Round 18; `acmp-unbound-record-not-zero` remains caught and reports 35 failed checks rather than 32 under the newer native compiler/test environment.

Supplementary store `--self-test` attempts reached the 570-second command limit; no complete 109-mutant store pass is claimed. Round 18's required store command omits that option and passes all 435 tests. Initial environment/size-gate attempts were corrected before the final passing runs: build-only avoids unnecessary CPU generation, extracting the unchanged probe satisfies the existing size ratchet, and the disposable runner's stubs use its fixed PATH. No gate or acceptance condition was weakened.

R584-16-RES-1 and RES-2 are applied exactly in the Round 18 section: pushed-head wording and the control-job timing's merge-versus-head labels. R585-17-RES-1 is the same pushed-head correction. Other residue remains carried.

No hosted run or PR-head act replica is claimed for this unpushed commit. The offline self-test ran only inside a disposable container. The previous positive reviews cover `27ee16b5`; the new head needs independent review and protected hosted contexts. No hardware work, push, PR edit or merge was performed.
## Authoritative references

- [Round 19 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6134939296), [M8a PR #721](https://github.com/kebag-logic/milan-fpga/pull/721), and the two positive reviews of the previous head ([R584-16](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6131676792), [R585-17](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6131790196)).

- [#697](https://github.com/kebag-logic/milan-fpga/issues/697) acceptance 1 to 5, the [pin ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092176555), owner decisions [6074086970](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970), [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506) and [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062), the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902), the [round 13 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6116488747), the [round 14 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6117713386), the [round 15 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6118625227) the [round 16 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6119960001) the [round 17 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6121496568) and the [round 18 assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6130298041); #716 and its merged change, [PR #724](https://github.com/kebag-logic/milan-fpga/pull/724).
- F5: [#700](https://github.com/kebag-logic/milan-fpga/pull/700), [AECP core and adapters](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/sw/firmware/ctrl/aecp/README.md).
- tsn-c-stack at the pin ([PR #22](https://github.com/kebag-logic/tsn-c-stack/pull/22), tag `milan-fpga-697-pin-405dc683`): [README](https://github.com/kebag-logic/tsn-c-stack/blob/405dc68310a18f669049ffc10cc23eef7300dcff/README.md), [import record](https://github.com/kebag-logic/tsn-c-stack/blob/405dc68310a18f669049ffc10cc23eef7300dcff/docs/IMPORT.md), [porting guide](https://github.com/kebag-logic/tsn-c-stack/blob/405dc68310a18f669049ffc10cc23eef7300dcff/docs/PORTING.md), [boundary gate](https://github.com/kebag-logic/tsn-c-stack/blob/405dc68310a18f669049ffc10cc23eef7300dcff/scripts/check_boundary.py).
- [Control firmware](https://github.com/kebag-logic/milan-fpga/blob/27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c/sw/firmware/ctrl/README.md), [firmware harness](https://github.com/kebag-logic/milan-fpga/blob/27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c/sw/firmware/gtest/README.md), [submodule map](https://github.com/kebag-logic/milan-fpga/blob/27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c/docs/reference/SUBMODULES.md), [CI workflow policy](https://github.com/kebag-logic/milan-fpga/blob/27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c/docs/testing/CI_WORKFLOWS.md), [mailbox bench](https://github.com/kebag-logic/milan-fpga/blob/27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c/tb/verilator/mbx/README.md).

## How to get into the same state

Round 19 is not published. These commands require a local checkout already containing the merge commit; a remote fetch currently supplies the preceding head.

```sh
git checkout --detach 95ca54cb9454d967b5534b4c3cc32c4c7e2e6a62
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 scripts/ci_rv32_sdk.py --destination <new SDK directory>
export MILAN_RV32_CC=<new SDK directory>/bin/riscv32-linux-gcc
```

The firmware gates need GoogleTest and GoogleMock 1.14.0, PyYAML, the pinned
RV32 SDK, CMake and Clang (the stack's own boundary gate), and the pinned
Verilator 5.050 for the two local Verilator gates.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --build-only --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --build-only --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_image.py --base d5858bbee328cf8d2c39a99ec14203f5d0ddd123
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
make -C tb/verilator/mbx
python3 sw/firmware/ctrl/test/aecp_wire.py --every --output <scratch directory> --verilator <Verilator 5.050>
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/firmware/ctrl/test/ctrl_build.py --stack-pin
python3 scripts/act_ci.py --selftest  # inside a disposable container or the CI job only, never on the host
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --firmware-census
python3 scripts/check_submodule_docs.py
python3 scripts/docs_check.py
```

For the image bytes, link both fixtures at dev and at this head with the same
SDK and runtime archives and compare the ELF hashes: `ctrl_image.py --shape
<shape> --out <dir>` for each shipped shape, and `ctrl_srp_image.py --config
<config> --interfaces <1|2> [--without-srp | --with-aecp] --output <dir> --libc <libc.a>
--compiler-runtime <libcompiler_rt.a>` for each shipped config. The `--with-aecp`
composition links compiler-rt's `__umoddi3`, so its runtime archives must be built
with `-fno-stack-protector` (the pinned SDK defaults to `-fstack-protector-strong`).

Expected result / pass criteria:

These are the success conditions to meet after resolving the Round 19 boundary integration. At the current head the boundary command exits 2; the full bar is incomplete.

- the firmware gate prints `tsn-c-stack at 405dc68310a18f669049ffc10cc23eef7300dcff`, all 60 arms `[ok]`, `mutants: 506 of 506 caught`, every AECP defect `[ok]` (76), every SRP defect `[ok]` (198 at two interfaces, 73 in the one-interface subset), both lwSRP pin arms `[ok]` and `test_ctrl_firmware: PASS`;
- coverage: `29 of 29 planted cases`, then `firmware coverage: PASS (30 files)`, every file at 100 %; the store: `OK across 5 shape(s), 435 tests`;
- each `--build-only`: every binary `built, not run (--build-only)` and `test_ctrl_firmware: BUILT`, `saved-state store gate (#665 F1): BUILT across 5 shape(s), nothing run (--build-only)`, `firmware coverage: BUILT (...)`; with `--self-test` (or the coverage gate's `--check`) each is refused, rc 2;
- boundary, the first form (every known builder, give it `VERILATOR`) or the second (the `firmware-boundary` job's), each running every known builder it judges by its builds under its own capture first: `no capture given: running every known builder the run judges under one`, one line per builder, `capture: ... every known builder held: ...`, `1 compile(s) failed, each with its dependency pass, and compiled nothing: ...` (the RV32 self-test's planted header defect), every control `[ok]`, then `<N> compiled sources of <M> recorded invocations (... the firmware's, ... the stack's, ... test equipment's and builders' own), each judged by what its dependency output lists, host and RV32, every Makefile builder's pin prerequisites and the pin proof's census; 0 finding(s), 105 boundary, 106 pin and 4 figure controls, 0 misbehaved` and `ctrl_boundary: PASS` for the second, in about 11 minutes on four CPUs over 2822 compiled sources of 3053 invocations (the first plants the Verilator run's five controls too; `--only verilator`: 6 boundary, 106 pin and 4 figure controls, V1 to V3 and the MAAP differential's replay among them, in about 8 minutes on four CPUs with its builders; it needs `gptp-processor` initialised, for the end-station builder, and refuses without it); a capture made by an earlier recorder is refused: `a recorder that lists no dependencies made it: capture again`;
- the four `--shard` runs: each prints the shard proof's five `PASS` lines and `tsn-c-stack at 405dc68310a18f669049ffc10cc23eef7300dcff` before any build, then its phase: `--shard 0/4` the 60 arms `[ok]`, `--shard 1/4` `mutants: 506 of 506 caught`, `--shard 2/4` the AECP defects, `--shard 3/4` both SRP campaigns and both lwSRP pin arms; each ends `test_ctrl_firmware: PASS`. Together they print the default run's verdict lines; `test_ctrl_firmware_shards.py`: `916 live invocations in exactly one shard; shard sizes [60, 507, 77, 272]`; `--firmware-census`: `"preserved": true`;
- `--base dc4d06cb`: `+0` in every section at both shapes;
- the MAAP differential prints `tsn-c-stack at 405dc68310a18f669049ffc10cc23eef7300dcff` first, then `16/16 caught`; the bench prints the same line before its firmware build, then its six tallies with 0 failures and `mbx mutants: 5 of 5 caught`, and `make -C tb/verilator/mbx run-if2` alone prints it before compiling; the AECP wire comparison prints the same line, then `wire comparison PASS: 1 ingress paths, 142 observations` and, with `--every`, `wire comparison PASS: 2 ingress paths, 294 observations`; the pin check alone prints the same line;
- the pin controls: the clean clone `accepted 405dc683...`; the stack checks, tools and bench targets each refused by name, among them the stack's `LICENSE` edited, a symbolic link standing in for `src/adp.c`, `scripts/check_boundary.py` made executable, and `src/adp.c` edited under a replacement of the pinned `src/` tree, under a replacement commit for the pin, and beside a graft file (each `tsn-c-stack differs from the pinned 405dc683: src/adp.c`), and under a clean filter given through attributes (`tsn-c-stack's repository holds configuration outside the pin proof's allowlist: filter.pin-control.clean (local)`); the pin proof as the checkout holds it `the pin check's verdict, no refusal`; and the 34 audit hook controls, each the hook's refusal (`ctrl_build.py:<n> starts git (subprocess.Popen) while the pin proof runs, not by the helper`, `... asks for compile in the pin proof ...` and the like) at a line of its plant, or, for the nine that cannot name one, for the program, the setting, the variable, a key or value that is not a plain `str`, or the plant's own filename; the 17 inherited-environment controls, each the verdict the clone itself earns (`tsn-c-stack differs from the pinned 405dc683: src/adp.c`, `... is not the pinned ...`, `cannot read the pinned tree ...`, the pinned clone with every variable at once `tsn-c-stack at 405dc683...`) with no program the configuration names run, and the hook's judge refusing `fork_exec` entries that give a key twice; the twenty-seven object-store, attribute and configuration controls: the pinned `src/` tree's object and the pinned commit's forged beside an edit, each `tsn-c-stack's object store holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to …` or `… the pinned commit (commit 405dc683) hashes to …`, the edited source's blob forged and a line-ending conversion through attributes (each `… differs from the pinned 405dc683: src/adp.c`), seven states of a superproject's own configuration, its gitlink read, each `the superproject's repository holds configuration that has Git start a program or fetch while the gitlink is read: <its keys, each with its scope>` (a recorder named as `core.fsmonitor`; a sparse partial clone lacking the tree that holds the gitlink, its upload-pack a recorder that serves it, and the same over ssh through `core.sshCommand`; that sparse superproject beside a promisor remote declared by `remote.promisor` or `remote.partialCloneFilter` without a subsection, or by `remote "".promisor`, reached through a recorder by an `ext::` URL rewrite, each naming that one key; an included file and the work tree's own configuration each naming a recorder as `core.fsmonitor`), a superproject configured as `actions/checkout` and `git submodule update --init` leave it (`accepted 405dc683...`), a clean clone with a key of every allowlisted family (`accepted 405dc683...`), and fourteen states of the stack's own configuration, `submodule "".active` (an empty subsection) among them, each `tsn-c-stack's repository holds configuration outside the pin proof's allowlist: <its keys, each with its scope>`, no recorder ever run; the four figure controls each `gives the ... as <n+1>, where the self-test has <n>`;
- act self-test `selftest: PASS`; the rest exit 0;
- all 65 image hashes equal between dev and the head, including flat and split runtime layouts.

Local evidence at the head (CI-parity Ubuntu 24.04 container with gcc 13.3 and
GoogleTest 1.14.0 for the firmware gates) belongs to the earlier named rounds; it is not a pass for Round 19. The
detailed tables (image hashes, coverage before and after, campaign counts,
plant equivalence, pin proof) are in
[`review-evidence/697c-r1/author/HANDOFF.md`](https://github.com/kebag-logic/milan-fpga/blob/ec6854f6fefbfa2954d6907d5cf457afac92377c/review-evidence/697c-r1/author/HANDOFF.md)
at `ec6854f6`. Round 2's, round 2b's, round 3's and round 4's evidence is not published yet; until it is, their REVIEW READY comments ([6093383132](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093383132), [6094033396](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6094033396), [6095730057](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6095730057) and [6097154937](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6097154937)) carry their results.

## Known limitations / out of scope

- Round 19 classifies `milan_soc.py` OUTSIDE using the registry's control-firmware scope: it loads the existing control ELF; its separate BIOS/milan_baremetal path compiles no control-stack source. This does not claim that the whole program compiles nothing. The full memory test needs the patched elaboration environment; its boundary build-only mode needs the pinned Python imports and RV32 compiler.

- The pin holds milan-fpga's code, not byte-identical files: every tsn-c-stack commit carries the MIT SPDX line, and from `18d7378` its comments are reduced; #697 comment 6092176555 confirms that reading. Round 13's pin `405dc683` is not on tsn-c-stack's `main`, which merges by squash; the tag `milan-fpga-697-pin-405dc683` keeps it reachable. Moving to tsn-c-stack main (the ADP change of tsn-c-stack #19 and the YAML generator, #703) is a later PR.
- The lwSRP pin check (`ctrl_arms.lwsrp_pin`) still reads `git status`; R584-1-S1 marks that part optional, and lwSRP is not #697's submodule.
- act has not run: this PR changes `scripts/act_ci.py`'s trusted manifest, so the first act run needs the audited-install bootstrap by an independent reviewer.
- The hosted `firmware-boundary` job needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image.
- The MAAP differential runs in CI in `firmware-verilator` (round 6), under the boundary's capture. The mailbox bench also runs in CI as the `mbx` Verilator suite.
- The AECP wire comparison runs in CI in `firmware-verilator` at both references (`--every`); its two-interface reference is the processor revision `c9f74b68`, taken from the processor submodule's objects, not the submodule's gitlink.
- The repository's runtime builder (`ctrl_image_runtime.py`, unchanged here) compiles compiler-rt with the pinned SDK's default stack protector, so its archives cannot link `ctrl_srp_image.py --with-aecp`; the AECP images were compared with `-fno-stack-protector` archives at dev and here alike.
- Rounds 3 to 6: the boundary self-test judged every shape, contract and language. At `d1b22e80`, measured on a hosted runner: the step ran more than 12 min and the job exceeded 45 min (job 114173809799). Round 4 runs each preprocessing once and judged the same configurations in 74 to 86 s here, on four pinned CPUs of a shared host where `d1b22e80` took 807 s; on a hosted runner at `e07b3054` the step took 93 s (job 114206016568). Round 5's step took 101 to 106 s on four idle pinned CPUs, where `e07b3054`'s took 80 to 82 s on the same CPUs; on a hosted runner at `92b5be18` it took 113 s (job 114282060753). A preprocessing is reused only for the same unit and arguments with every file it read byte-identical and no file added or removed that it could look up by name; judging every control with and without reuse gave the same findings, 0 of 60 differing.
- R584-3-S1's multi-word literal is closed by construction in round 5 (the capture records the flag the compiler is given); its force-included SRP header named as a constant, and a pin recipe that ignores its exit status, are optional and not addressed; the bench arms of the pin self-test already catch the last.
- `firmware-boundary` has no Verilator; `firmware-verilator` judges the mailbox bench, the MAAP differential and the AECP wire comparison (`--only verilator`). The two jobs split the builders, never an invocation: each recorded compile is judged whole in the job that ran it, and only a run given both captures also tries a mode only one records beside one only the other does (no compile combines them; that run passes locally with 105 and 20 controls). A Verilator cache miss adds its source build to `firmware-verilator`, as it does to `verilator-lint`.
- The image builders run in the boundary step at `ctrl_image.SHAPES`, and the gate judges exactly the compiles they make there; `ctrl_srp_image.py` is given no runtime archives there, so it compiles every object and must stop exactly at its link.
- A compiler a Python builder starts by a path is recorded by the audit hook, and one a Makefile builder's recipe names is read from make's dry run; one a shell runs by a path (a script's, or a command a builder runs through a shell), one a compiled helper runs by a path, and one a Python builder started with `-I` or `-E` runs by a path would not be, and none exists (README, beside the bypass sentence). An exec-level guard (`LD_PRELOAD`) was weighed and not taken: it would load into the store suite's ASan binary, which refuses a preloaded library.
- Round 7: a compile is judged by where the files it read live. A builder's own file outside the checkout (a source it writes or copies, a mutant's tree) is held only by the `#include` lines of the firmware and stack files it reads, not by its own; the firmware the images compile is the checkout's.
- Round 7: a mode reaches only the compiles a builder gives it. Rounds 3 to 6 explored every combination of the modes, shapes and contracts any builder gave, a superset of what any builder compiles; round 7 judges exactly the recorded compiles, as the assignment's population rule says, so a defect under a mode no builder gives the file it is in is not found.
- R585-2-S2 (an explicit `--stack` for `aecp_arms.py` still builds the submodule's `tests/`) is optional and not addressed; the default invocation pins the stack it builds.

- A capture given must have been made in the checkout judged: a builder run of it that ran in another checkout refuses the gate (round 7), since that checkout's files are none of this one's. Hosted, no capture is given: each boundary job makes its own.
- An expansion is reused only while every file and directory it reported is unchanged and every argument is plain; a file a compile reads that the report does not show (a specs file, a plugin) makes its argument non-plain, so it is never reused. The dependency pass is never reused: it runs for every compiled source.
- Round 7 reads the assignment in eight places of its own (the Round 7 section): command-line reads into stack compiles judged as the builder's, the C implementation's headers as the compiler's baseline and the RV32 builds' freestanding C library, test equipment held only through the firmware and stack files it reads, the include tree judged in every compile, stack tests admitted the host's libraries, failed compiles named rather than refused, POSIX headers admitted on the host, and modes not explored across units. Each is a decision the manager may confirm or reverse.
- Round 8 (superseded in round 18: #716 splits the job into four, merged here): `firmware-unit` runs no capture, and is over 60 % of its 45 minutes on its suites alone: dev's own job took 1963 s hosted at `8b61b709` and 1484 to 2462 s on other branches' twenty most recent runs; a longer timeout or sharded campaigns would meet 60 %, and neither is taken here.
- Round 8: the boundary judges the builds, not the suites, so the campaigns' compiles of planted copies leave its capture; measured against round 7's capture of the suites, they add no fact a rule can refuse. `ctrl_configs.SUITES` lists the four modules that compile only inside a suite.
- Round 8: `firmware-boundary`'s 30-minute timeout is chosen for a new job (38 % locally); its hosted figures at `4cab445a` are in the manager's ruling on #697 ([6107349992](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107349992)).
- Round 12: the pin proof's threat model ([ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6114400461)) is the state it reads: the checkout's files and modes, Git's object store, refs, configuration and attributes, and the environment the proof inherits. Its own modules are reviewed source, outside the model; the audit hook is defence in depth against such code. The hook sees launches through the interpreter's audited interfaces only: not `ctypes` or an extension module, and on the runner's CPython 3.12.3 not `_posixsubprocess.fork_exec`, which `subprocess` calls just after raising its own event from Python (CPython 3.14 audits `fork_exec` itself). What Git itself starts, and code above the helper in `ctrl_build.py`, are outside it too.
- Round 12 (both closed in round 14; round 15 holds the whole configuration class to an allowlist): within that model two routes were open: a forged tree object in the stack's object store (Git reads subtrees for `ls-tree -r` without checking their hash), and a program the repository's own configuration names (`core.fsmonitor`), which Git starts when the decision reads the index.
- Round 14: every object the proof reads is hashed against its id, so a forged or corrupt one is refused by its place in the pin and its id, not by the file it would hide. Passing a forged object would take a second preimage of a pinned id under the stack's object format (SHA-1). Objects fetched from a remote are checked on transfer, so the route needs write access to the local object store.
- Round 14: Git 2.36 or later reads `core.fsmonitor=false` as off; earlier Git took the setting as a hook path.
- Round 15: the configuration guarantee is the allowlist (`ctrl_build.STACK_CONFIG`), read through Git itself (`git config --list --show-scope`), so what is judged is what that Git reads; a key it lists in a scope other than the repository's own, its work tree's or the helper's command line is refused. `GIT_NO_LAZY_FETCH=1` is defence in depth: honoured from Git 2.45.0 and by Gits patched for CVE-2024-32465, ignored by an older unpatched Git, where the allowlist refuses every promisor key first.
- Round 16: the superproject's own configuration is held by the keys it may not hold (`ctrl_build.SUPERPROJECT_REFUSED`: a promisor remote, its transport and `core.fsmonitor`), refused by name before the gitlink is read from its index; from round 17 each is judged by its section and variable, whatever its subsection, so the superproject declares no promisor remote in any key spelling Git reads. Its other keys are not judged (an allowlist would refuse `actions/checkout`'s `http.<url>.extraheader`); 28 of them that name a program, in a plain and a sparse superproject, start nothing while the gitlink is read, on Git 2.56.0 and upstream 2.43.0 (round 16's scratch probe). The stack's own configuration is held by its allowlist (round 15). `GIT_NO_LAZY_FETCH=1` and `core.fsmonitor=false` are defence in depth; where a Git does not honour `GIT_NO_LAZY_FETCH` (an upstream release before 2.45.0 other than the CVE-2024-32465 maintenance releases, such as 2.43.0 or 2.44.0), these two checks are what holds.
- Round 17: one parser (`ctrl_build.parsed_key`) splits both repositories' keys into section, subsection and variable as Git's own `parse_config_key` does. The stack's allowlist lists no family with an empty subsection, so a key such as `submodule "".active` is refused by its name, failing closed; Git writes none.
- Round 12: Git is given only the proof's own environment, and, under a capture, the builders' names (`CTRL_CAPTURE_FROM`) the capture's audit hook adds to every start, which Git does not read.
- Round 11 (its limit statement superseded by round 12's threat model): the pin proof's guarantee is its audit hook's (`ctrl_build.audited`), over launches through the interpreter's audited interfaces.
- Round 11: the hook judges while the proof runs, that is, while a function of `stack_gitlink`, `stack_pin` or `main` that `ctrl_build.py` defines runs in any thread, or while one of the two modules' top level runs. A function of the two modules that starts a process at another time is not judged: the build functions, `run`, and `ctrl_pin.py`'s tool runs. Replacing the decision's code is refused, but a gate that called another function bound in `stack_pin`'s name would not be running the decision; every gate imports `stack_pin` by name when it loads.
- Round 11: an import of a module already loaded raises no audit event, so `import importlib`, `__import__` and `pkgutil.importlib` on their own are refused by the lint, not at run time; anything they reach that starts a process or runs dynamic code in the proof is refused by the hook.
- Round 11 (closed in round 12): the helper's environment was the caller's with the two settings, so a Git variable the caller set (`GIT_DIR`, `GIT_INDEX_FILE`, `GIT_CONFIG_*`) reached Git; round 12's probe shows `GIT_INDEX_FILE` and `GIT_DIR` making the pin check accept a stack that is not the gitlink's at `aca5e8af`.
- Round 10 (superseded by round 11's hook): the census holds references, not processes. A function of another module that starts a process is not a facility it knows: `ctrl_build.py`'s build functions and `run`, and `ctrl_pin.py`'s tool runs, start processes through `fw_gtest.run`, and the census refuses them only where the pin decision would reach them (round 9's text census, which a computed or dashed name passed, is gone). It reads the modules as written, so code elsewhere that rebinds their names at run time, or a route of Python's own to an object that none of the refused names opens, is not seen.
- Round 10: the decision's vocabulary is fixed, so a change to `stack_gitlink`, `stack_pin`, `main` or what they reach that uses a new name fails the census until the name is added to `ctrl_pin.VOCABULARY`, `BUILTINS` or `ATTRIBUTES`. The helper and its environment are held by the module-wide rule, the environment check and the replacement controls, not by the vocabulary.
- Round 9: a graft rewrites only a commit's parents, which the pin proof never reads; its control shows a graft carries no altered stack past the proof, and the helper's graft setting is held by the census's environment check.
- Round 9: the pin check compares the submodule's whole checkout but its `.git`, so a file left inside it (a build directory made there) refuses every gate by name until it is removed.
- Round 9: the figure check reads the four sentences of the firmware README that give the self-test's population; a figure written elsewhere is not checked.

## Definition of Done

- [x] Linked Issue implementation acceptance criteria are satisfied locally (pin `405dc683` set by #697 comment 6116488747 under the rule of comment 6092176555; Round 19 classification scope is stated explicitly)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (Round 19 continuation; the supplementary store mutation attempts are not counted as passes)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](https://github.com/kebag-logic/milan-fpga/blob/5b4f6fbebf1f620cc20d90eb16012306f5e8e4e1/CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done



