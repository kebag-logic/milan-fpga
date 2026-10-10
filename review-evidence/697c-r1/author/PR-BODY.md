[A583]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally — firmware gate PASS (51 arms; 471/471 control, 169/169 and 68/68 SRP, 2/2 lwSRP pin plants caught); coverage 22 files at 100 %; 25 of 25 RV32 images byte-identical — `697-consume` -> `dev`. Hosted runs and act have not run yet.

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
| Boundary | New `ctrl_boundary.py`: the stack's sources and headers, under the firmware's own host and RV32 flags, depend only on the stack's public headers and the C library; the firmware and image code reach only the stack's `include/`; no file under `sw/firmware` is named as a stack source or header; and the stack's own `scripts/check_boundary.py` runs. Every gate first refuses a stack that is off its gitlink or modified. |
| CI | `firmware-unit` and the Verilator shards fetch the submodule; `firmware-unit` gains the boundary step; `scripts/ci_events.py` pins all three. |
| Docs | A "TSN stack submodule" section in `sw/firmware/ctrl/README.md` (what it provides, what it must not depend on, its tests, MIT inside this CERN-OHL-W platform), and every reference to the old paths; `README.md`, `QUICKSTART.md` and `CONTRIBUTING.md` initialise the submodule wherever every Verilator suite runs. Links into the stack use pinned URLs, since the docs gates run without submodules. |

Two killers changed words, not kills: the stack's two A29 tests now assert the
admission and withdrawal counts first, so `acmp-admit-ignores-another-talker`
and `acmp-reset-forgets-the-admitted` fail the same tests on the stack's words.
Its own table uses those words.

## Authoritative references

- [#697](https://github.com/kebag-logic/milan-fpga/issues/697) acceptance 1 to 5, owner decisions [6074086970](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074086970), [6074093506](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074093506) and [6074191062](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6074191062), and the [lane assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902).
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
python3 sw/firmware/ctrl/test/ctrl_image.py --base 8b61b70902f3ebf118e56967277e2686731081bd
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
make -C tb/verilator/mbx run-wb run-axil run-cosim run-if2
python3 scripts/act_ci.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/check_submodule_docs.py
python3 scripts/docs_check.py
```

For the image bytes, link both fixtures at dev and at this head with the same
SDK and runtime archives and compare the ELF hashes: `ctrl_image.py --shape
<shape> --out <dir>` for each shipped shape, and `ctrl_srp_image.py --config
<config> --interfaces <1|2> [--without-srp] --output <dir> --libc <libc.a>
--compiler-runtime <libcompiler_rt.a>` for each shipped config.

Expected result / pass criteria:

- the firmware gate prints `tsn-c-stack at 1a9f651cdf7846b8e10ac246a6ef6916960fbb92`, every arm `[ok]`, `mutants: 471 of 471 caught`, every SRP defect `[ok]` (169 at two interfaces, 68 in the one-interface subset), both lwSRP pin arms `[ok]` and `test_ctrl_firmware: PASS`;
- coverage: `29 of 29 planted cases`, then `firmware coverage: PASS (22 files)`, every file at 100 %;
- boundary: `0 finding(s), 15 boundary and 4 pin controls, 0 misbehaved` and `ctrl_boundary: PASS`;
- `--base 8b61b709`: `+0` in every section at both shapes;
- the MAAP differential `16/16 caught`; the bench's six tallies with 0 failures;
- act self-test `selftest: PASS`; the rest exit 0;
- all 25 image hashes equal between dev and the head.

Local evidence at the head (CI-parity Ubuntu 24.04 container with gcc 13.3 and
GoogleTest 1.14.0 for the firmware gates): all of the above hold. The
detailed tables (image hashes, coverage before and after, campaign counts,
plant equivalence, pin proof) are in the evidence comment.

## Known limitations / out of scope

- The pin is the newest tsn-c-stack commit with milan-fpga's code, not byte-identical files: every tsn-c-stack commit carries the MIT SPDX line, and from `18d7378` its comments are reduced. Moving to tsn-c-stack main (the ADP change of tsn-c-stack #19 and the YAML generator, #703) is a later PR.
- act has not run: this PR changes `scripts/act_ci.py`'s trusted manifest, so the first act run needs the audited-install bootstrap by an independent reviewer.
- The hosted `firmware-unit` step needs CMake and Clang for the stack's own gate; both ship on the hosted Ubuntu image, not yet observed on this PR.
- The MAAP differential and the mailbox bench are local gates, not in CI.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (all met locally; the pin reading awaits confirmation, see Known limitations)
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
