[A557]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

REVIEW READY: round-2 local validation passes at `04e1435a218908d2b12b4053e5dab2c2dcac2ebf`. `679-rv32-sdk` -> `dev`.

Both full campaigns pass: 76 ctrl and 106 store mutants caught, with five store shapes and 434 tests. All local firmware-unit commands pass with RV32 required. The 17 RV32 controls pass, including both new same-name static-definition controls. Removing either binding restriction makes its control fail. The reviewer probe rejects both masked dependencies, while separate global and weak definition controls pass. Coverage remains 100 percent adjusted lines and branches for all 14 files at the unchanged ratchet. Documentation and CI contract gates pass.

Independent corrected-head re-review and manager-owned publication and merge-candidate validation remain pending.

## Linked Issue / roles

Closes #679
Relates to #665

Executor: `[A557]`
Internal cleared-context reviewer: `[R526]`
External reviewer: `[R527]`

## Description

The ctrl RV32 arm previously reached the pinned ILP32D SDK's hosted libc headers while compiling for ILP32, failing on the missing ILP32 glibc stub. Both validation arms now isolate freestanding compiler headers and the existing memory/formatter declarations, retaining RV32I and ILP32. Both reject unexpected runtime symbols, wrong architecture or ABI, and non-static frame reports. The runtime check matches undefined names across compiled objects using only global or weak definitions. A same-name local definition cannot hide an unresolved external dependency; both real arms have a compiled regression control for this case.

The workflow installs the same pinned SDK before both firmware suites and requires their RV32 arms. The canonical CI contract checks that ordering and rejects removal of either required-RV32 flag. The self-test plants header, ISA, ABI, heap, unknown-service, local-binding and stack-protection defects. All 15 original controls remain.

Ctrl object totals remain text/data/BSS 11520/0/170 bytes. Store text falls by 240 bytes per shape after disabling SDK-injected stack protection in validation objects; data, BSS, static buffers and largest static frames remain unchanged. The largest static frame is 112 bytes for ctrl and 128 bytes for each store shape. These are object and frame measurements, not linked-image sizes or whole-program stack bounds.

## Authoritative references

- [Round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022780134)
- [Scope ruling](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702)
- [Assignment on #679](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923)
- [Firmware integration contract #665](https://github.com/kebag-logic/milan-fpga/issues/665)
- [Product ownership and verification requirements](REQUIREMENTS.md)
- [Firmware test harness and RV32 evidence limits](sw/firmware/gtest/README.md#rv32-object-builds)
- [CI workflow policy](docs/testing/CI_WORKFLOWS.md)
- [Shipping bare-metal build](sw/firmware/milan_baremetal/Makefile)

## How to get into the same state

Use the publisher's branch once publication is authorized; this session did not push it. The local branch starts at `6714181d0c8a16e2983f85b724f4d688f5111835` and adds two commits. Round 2 adds one commit on `0a004a8c`, without rewriting history.

```sh
git switch 679-rv32-sdk
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# Set SCRATCH to an existing disk-backed directory with sufficient free space.
export TMPDIR="$SCRATCH"
export PYTHONDONTWRITEBYTECODE=1
export PYTHON_CPU_COUNT=4
export VERILATOR_JOBS=2
export MAKEFLAGS=-j8
python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/sdk"
export MILAN_RV32_CC="$SCRATCH/sdk/bin/riscv32-linux-gcc"
```

Provide the distribution's host test libraries, matching compiler/coverage utilities, the repository's documentation dependencies and the documented builder elaboration environment. The SDK archive and installer are unchanged.

## How to validate

Run from the checkout, retaining each command's exit code and complete log.

```sh
python3 scripts/ci_rv32_sdk_selftest.py
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_scope.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/check_em_dash.py --base 6714181d
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
```

Expected: every required command exits zero, all 76 ctrl and 106 store mutants are caught, all 17 RV32 controls pass, both RV32 arms run, all five shapes pass, and the existing coverage ratchet holds. The handoff records every local gate. The bounded store execution calls the original full driver with one reusable physical mutant directory per worker; inventory, flags, cache keys, generated inputs and failure oracles remain unchanged.

After publication, the manager runs the trusted validation-base workflow replica before inspecting hosted results, following the CI policy, and retains the corrected-head firmware-unit log. The broader builder and merge-candidate bar follows the public scope ruling.

## Known limitations / out of scope

- These are freestanding object builds with the unchanged pinned SDK. The scope ruling accepts object sizes and individual static frames here. Linked images, runtime compatibility and whole-program stack bounds belong to integration.
- The local firmware-unit commands use the pinned SDK selector and capped worker counts. They do not constitute hosted or supported workflow-replica evidence for the new unpublished head.
- Hosted firmware-unit job 112422842862 passed at the previous head. Its log is historical evidence; the corrected head requires fresh published-head checks.
- The manager owns the broader builder/source receipts and final current-dev merge-candidate validation under the scope ruling. Earlier partial builder receipts do not count as a complete passing bank.
- Firmware behavior sources, shipping-image inputs and RTL are unchanged. There is no hardware or bench evidence.
- Coverage exclusions remain unchanged, including the ADP premise under #678. Optional private-dependency validation remains separate.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
