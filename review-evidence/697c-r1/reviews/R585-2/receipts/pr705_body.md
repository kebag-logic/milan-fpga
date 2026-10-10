[A583]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2](#round-2)** — What R584-1 and R585-1 asked for, and how each gap is closed by construction.
- **[Round 2b](#round-2b)** — The merge of dev after F5 (AECP), and how the boundary, the pin check and the mode derivation cover what F5 added.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at the merge head `386b8e69` (dev `aef7ac66` merged in) — firmware gate PASS (59 arms; 471/471 control, 74/74 AECP, 169/169 and 68/68 SRP, 2/2 lwSRP pin plants caught, every verdict equal to dev's); coverage 30 files at 100 %, the same raw counts as dev; 35 of 35 RV32 images byte-identical to dev; boundary gate PASS in every configuration the builders compile, 36 boundary and 15 pin controls — `697-consume` -> `dev`. Hosted runs and act have not run yet.

## Linked Issue / roles

Relates to #697

Executor: `[A583]`
Internal cleared-context reviewer: `[R584]`
External reviewer: `[R585]`

## Description

milan-fpga now takes its ADP, ACMP and MAAP cores and the wire layer from the
[tsn-c-stack](https://github.com/kebag-logic/tsn-c-stack) submodule at
`third_party/tsn-c-stack`, and no longer holds copies. No firmware behaviour
changes: both linked RV32 images are byte-identical at every shape.

| Piece | Change |
|---|---|
| Submodule | `third_party/tsn-c-stack` pinned at `1a9f651cdf7846b8e10ac246a6ef6916960fbb92`, the newest tsn-c-stack commit whose cores are milan-fpga's code token for token and line for line. `.gitmodules`, `scripts/act_ci.py` `TRUSTED_SUBMODULES` (with four new refusal arms), the submodule map, its diagram and `THIRD_PARTY.md` (MIT). |
| Copies removed | `git rm` of `adp.{c,h}`, `acmp.{c,h}`, `maap.{c,h}`, `wire/wire.h` and the core-test copies `test_acmp.cpp`, `acmp_fake.hpp`, `test_adp_reentry.cpp`, `test_maap_debug.cpp`; the core cases of `test_adp.cpp` and `test_maap.cpp` go too, their adapter and CSR cases stay. |
| Build | `ctrl_build.py` names the cores `tsn-c-stack/src/*.c` in the same link order and includes only the stack's `include/`; the arms build the stack's own core tests into the same binaries under the same tally labels (`fw_gtest_label.cpp` for a binary whose test files name no label). The `mbx` bench Makefile, the SRP arms, the MAAP differential and both image fixtures build from the stack. |
| Evidence readers | `ctrl_image.py --base` and `ctrl_srp_image.py --ctrl-source` measure a pre-move tree with its own cores and a later one with its recorded stack. |
| Coverage | `fw_coverage.py` measures the stack's `src/` and `include/` (never its tests or examples), with a new planted case; the ratchet is regenerated: same counts on the new paths, and `srp_mbx.c` moves from a stale 515 to the 514 lines dev already measures. |
| Mutation tables | Core plants name the stack's files; 43 plants whose anchor was a comment the stack removed take the stack's own re-anchored text; every planted program is token-identical to dev's. Two killers take the stack's words, see below. |
| Boundary | New `ctrl_boundary.py`, judging every configuration the firmware's builders compile (the modes are read from the builders' own `-D`/`-U` flags, and every combination of those a unit tests is preprocessed, on the host and for RV32): the stack's sources and headers depend only on the stack's public headers and the C library; the stack's tests reach nothing of this repository outside the submodule; the firmware and image code reach only the stack's `include/`; no file under `sw/firmware` is named as a stack source or header; and the stack's own `scripts/check_boundary.py` runs. |
| Pin check | One shared check, `ctrl_build.stack_pin` (`ctrl_build.py --stack-pin` for the Makefile), proves the stack's content: every file of its sources, headers, tests, examples, scripts and CMake files must hash to the gitlink's tree, with nothing added, read from the files rather than the index. The host test (with coverage), the boundary gate, the MAAP differential in both modes, the mailbox bench and both image fixtures with the submodule as their stack run it first. |
| CI | `firmware-unit` and the Verilator shards fetch the submodule; `firmware-unit` gains the boundary step; `scripts/ci_events.py` pins all three. |
| Docs | A "TSN stack submodule" section in `sw/firmware/ctrl/README.md` (what it provides, what it must not depend on, its tests, MIT inside this CERN-OHL-W platform), and every reference to the old paths; `README.md`, `QUICKSTART.md` and `CONTRIBUTING.md` initialise the submodule wherever every Verilator suite runs. Links into the stack use pinned URLs, since the docs gates run without submodules. |

Two killers changed words, not kills: the stack's two A29 tests now assert the
admission and withdrawal counts first, so `acmp-admit-ignores-another-talker`
and `acmp-reset-forgets-the-admitted` fail the same tests on the stack's words.
Its own table uses those words.

## Round 2

[R584-1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092573026) and
[R585-1](https://github.com/kebag-logic/milan-fpga/pull/705#issuecomment-6092623741) were NEGATIVE on
MINOR gaps in the boundary and pin gates. Round 2
([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092628778)) adds three
commits on `60e7b57c` and changes no firmware source, test, mutation table or build flag.

| Finding | Closed by |
|---|---|
| R585-1-F1: the boundary was judged in one configuration | The gate reads the build modes from the builders themselves (every `-D`/`-U` flag literal in `ctrl_build.py`, `ctrl_arms.py`, `srp_arms.py`, both image fixtures, the MAAP differential and the bench's Makefile), never from a list of its own. GCC's `-dU` reports the macros each unit's preprocessing tests; the gate preprocesses every combination of their modes, with every other mode defined, until none is new. Both directions run on the host and for RV32. A finding names its configuration, e.g. `host [-DCTRL_REENTRY_ASSERT]: ...`. R585-1's three escaped probes are each refused by name. |
| R585-1-F2 = R584-1-F1: two gates built an unpinned stack | The MAAP differential (both modes; new `--stack`, default the submodule) and the mailbox bench (a phony `stack-pin` prerequisite of its firmware library) run the same `stack_pin` first. Planted controls: the bench accepts a pinned clone; the bench and both differential modes refuse an edited one before building. |
| R584-1-S1: the pin trusted `git status` | `stack_pin` hashes every file of `src/`, `include/`, `tests/`, `examples/`, `scripts/`, `cmake/` and `CMakeLists.txt` and compares it with the gitlink's tree; added files are refused; the index is never read. An `assume-unchanged` edit, an edited script or CMake file and an added header are refused. |
| R584-1-S2: the stack's tests were outside the boundary | The stack's `tests/*.cpp` and `*.hpp` are preprocessed as C++ with the arms' test include path in every configuration; a dependency inside this repository outside the submodule is refused. The real-path `#include "mbx_hal.h"` plant in `tests/test_maap_debug.cpp` fails the gate by name. |
| R585-1 residue | R1 to R4 in this body; R5 in the five `adp.c` coverage rows of `sw/firmware/gtest/README.md`. |

At round 2's head the boundary self-test plants 25 defects refused by name, 3 passing controls and 12 pin
controls, all as expected. A real-path run in a disposable clone, editing the clone's own submodule, is
refused by the bench, both differential modes, the host test, the pin check (an `assume-unchanged` edit) and
the boundary gate (an edited script), each by name. The images (25 of 25), coverage (22 files, same counts), the firmware gate's
verdicts and the MAAP and bench tallies are unchanged from round 1.

## Round 2b

F5 (#700, the AECP core under `sw/firmware/ctrl/aecp/`) merged into dev as `aef7ac66` and conflicted
with this branch. Round 2b ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6093389868))
merges dev in as one merge commit, `386b8e69`, with no rebase. AECP is not part of tsn-c-stack: it stays
this firmware's, and every F5 source, test, coverage row and mutation entry is kept.

| What | Resolution |
|---|---|
| Conflicts | `sw/firmware/ctrl/README.md` keeps both layout rows; `ctrl_srp_image.py` keeps the stack's `source_tree` and F5's `--with-aecp` composition, with the cores from the stack. |
| F5's builders | `aecp_arms.py` and `aecp_wire.py` named the removed `wire/`: they now take the stack's `include/`, the application arm builds the cores from the stack, and the AECP tests find `acmp_fake.hpp` in the stack's `tests/` (token-identical to dev's copy). |
| Pin check | `aecp_arms.py`, `aecp_mutants.py` and `aecp_wire.py` take `--stack` (the submodule by default) and run the shared pin check first when run alone; in the firmware gate they run after its pin check. Three pin controls refuse an edited clone in each. |
| Boundary units | The firmware's units are every directory of `sw/firmware/ctrl` but `host/` and `test/`, and every C source under `test/`: F5's core, adapters, application bridge and AECP image are judged (51 units, 34 before). The include path adds every firmware directory, and the entity generators' headers (`aecp_entity_gen.h` among them) are generated, not stood in for. |
| Mode derivation | The builders are found, not listed: every Python module and Makefile of the checkout that names `sw/firmware/ctrl` or `ctrl_build`. F5's `AECP_TEST_APP`, `AECP_TEST_MAILBOX` and `AECP_TEST_NVM` come from `aecp_arms.py` with nothing added to the gate; names the C implementation reserves (the runtime builder's `_LIBC`) are not modes. |
| Controls | Eight new boundary controls, each refused by name: a stack include under F5's `AECP_TEST_APP`; a mode written only in a new builder file; the stack including `aecp.h`; a stack test including `aecp_mbx.h`; the AECP core, its application bridge and the AECP image's SRP composition reaching the stack outside `include/`; a copy named `aecp/acmp.h`. |

The merge alone did not pass: F5's arms could not build, and the round-2 boundary gate refused
`app/ctrl_app_aecp.c` for RV32. So the merge commit carries the resolution, and every gate passes at it.
Real-path probes in a disposable clone: an edited `src/acmp.c` is refused by the three AECP tools, the AECP
image and the firmware gate, and three boundary plants fail the gate by name.

## Authoritative references

- [#697](https://github.com/kebag-logic/milan-fpga/issues/697) acceptance 1 to 5, the [pin ruling](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6092176555), owner decisions [6074086970](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970), [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506) and [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062), and the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902).
- F5: [#700](https://github.com/kebag-logic/milan-fpga/pull/700), [AECP core and adapters](../sw/firmware/ctrl/aecp/README.md).
- tsn-c-stack at the pin: [README](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/README.md), [import record](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/docs/IMPORT.md), [porting guide](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/docs/PORTING.md), [boundary gate](https://github.com/kebag-logic/tsn-c-stack/blob/1a9f651cdf7846b8e10ac246a6ef6916960fbb92/scripts/check_boundary.py).
- [Control firmware](../sw/firmware/ctrl/README.md), [firmware harness](../sw/firmware/gtest/README.md), [submodule map](../docs/reference/SUBMODULES.md), [CI workflow policy](../docs/testing/CI_WORKFLOWS.md).

## How to get into the same state

```sh
git fetch origin 697-consume
git checkout 697-consume
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
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/ctrl/test/ctrl_image.py --base aef7ac66605c4404900ce04cbaaeff88e41bb880
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
make -C tb/verilator/mbx
python3 sw/firmware/ctrl/test/aecp_wire.py --reference protocol-processor --interfaces 1 --output <scratch directory> --verilator <Verilator 5.050>
python3 sw/firmware/ctrl/test/ctrl_build.py --stack-pin
python3 scripts/act_ci.py --selftest  # inside a disposable container or the CI job only, never on the host
python3 scripts/ci_events.py --check
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

- the firmware gate prints `tsn-c-stack at 1a9f651cdf7846b8e10ac246a6ef6916960fbb92`, all 59 arms `[ok]`, `mutants: 471 of 471 caught`, every AECP defect `[ok]` (74), every SRP defect `[ok]` (169 at two interfaces, 68 in the one-interface subset), both lwSRP pin arms `[ok]` and `test_ctrl_firmware: PASS`;
- coverage: `29 of 29 planted cases`, then `firmware coverage: PASS (30 files)`, every file at 100 %;
- boundary: `51 firmware units ... 18 build modes (376 preprocessings); 0 finding(s), 36 boundary and 15 pin controls, 0 misbehaved` and `ctrl_boundary: PASS`;
- `--base aef7ac66`: `+0` in every section at both shapes;
- the MAAP differential prints `tsn-c-stack at 1a9f651cdf7846b8e10ac246a6ef6916960fbb92` first, then `16/16 caught`; the bench prints the same line before its firmware build, then its six tallies with 0 failures and `mbx mutants: 5 of 5 caught`; the AECP wire comparison prints the same line, then `wire comparison PASS: 1 ingress paths, 142 observations`; the pin check alone prints the same line;
- act self-test `selftest: PASS`; the rest exit 0;
- all 35 image hashes equal between dev and the head.

Local evidence at the head (CI-parity Ubuntu 24.04 container with gcc 13.3 and
GoogleTest 1.14.0 for the firmware gates): all of the above hold. The
detailed tables (image hashes, coverage before and after, campaign counts,
plant equivalence, pin proof) are in
[`review-evidence/697c-r1/author/HANDOFF.md`](https://github.com/kebag-logic/milan-fpga/blob/ec6854f6fefbfa2954d6907d5cf457afac92377c/review-evidence/697c-r1/author/HANDOFF.md)
at `ec6854f6`; round 2's and round 2b's are in the lane packet's HANDOFF.

## Known limitations / out of scope

- The pin is the newest tsn-c-stack commit with milan-fpga's code, not byte-identical files: every tsn-c-stack commit carries the MIT SPDX line, and from `18d7378` its comments are reduced; #697 comment 6092176555 confirms the pin on that reading. Moving to tsn-c-stack main (the ADP change of tsn-c-stack #19 and the YAML generator, #703) is a later PR.
- The lwSRP pin check (`ctrl_arms.lwsrp_pin`) still reads `git status`; R584-1-S1 marks that part optional, and lwSRP is not #697's submodule.
- act has not run: this PR changes `scripts/act_ci.py`'s trusted manifest, so the first act run needs the audited-install bootstrap by an independent reviewer.
- The hosted `firmware-unit` step needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image, not yet observed on this PR.
- The MAAP differential is a local gate, not in CI. The mailbox bench runs in CI as the `mbx` Verilator suite.
- The AECP wire comparison is a local gate; its two-interface reference is the processor revision `c9f74b68`, not the pinned submodule.
- The repository's runtime builder (`ctrl_image_runtime.py`, unchanged here) compiles compiler-rt with the pinned SDK's default stack protector, so its archives cannot link `ctrl_srp_image.py --with-aecp`; the AECP images were compared with `-fno-stack-protector` archives at dev and here alike.
- The boundary self-test takes about four and a half minutes in `firmware-unit`, beside the firmware gate's own campaigns.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (all met locally; pin confirmed in #697 comment 6092176555)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

