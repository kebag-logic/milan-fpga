# Public scope snapshot

Issue: https://github.com/kebag-logic/milan-fpga/issues/679

[A10] Found by #665 lane FT (A547; confirmed by review R506-1). Pre-existing at dev `423ac5d9`.

The ctrl firmware's `rv32` arm (`sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32`) fails against the CI-pinned SDK from `scripts/ci_rv32_sdk.py`. That SDK is `ilp32d` and has no `gnu/stubs-ilp32.h` for `-mabi=ilp32`. The arm passes with the host toolchain. The `firmware-unit` job skips it by name, so CI does not build the ctrl firmware for RV32.

**Acceptance:**
1. The ctrl firmware builds for the shipping core's ABI with the CI-pinned SDK: either it builds freestanding (no glibc stubs, matching bare metal), or the pinned SDK gains the matching multilib.
2. The `rv32` arm runs in the hosted job, not skipped by name.
3. The same check applies to `ctrl_nvm`'s RV32 arm.

Relates to #665.


https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923

[A10] **Lane for #679.** Executor [A557], branch `679-rv32-sdk` from dev `6714181d`. Reviewers [R526] (internal) and [R527] (external).

1. Make the ctrl and ctrl_nvm firmware RV32 builds work with the CI-pinned SDK (`scripts/ci_rv32_sdk.py`, `ilp32d`). Preferred: build them freestanding for the shipping core's ABI (no glibc stubs, matching bare metal: `-ffreestanding -nostdlib` with the project's own minimal runtime). Alternative: pin an SDK with the matching multilib. State which, and why.
2. The `rv32` arm runs in `firmware-unit`, no longer skipped by name, on hosted and act. Show the hosted log.
3. No firmware behaviour change. The images' sizes are reported before and after, and the bss/stack bounds still hold.

**Gates:** firmware-unit, both firmware campaigns with `--require-rv32`, the builder bank, `scripts/ci_scope.py --selftest` and the docs gates.

**Output:** HANDOFF.md and PR-BODY.md ("Closes #679"). Then post REVIEW READY with the head on #679. Do not push.

Do not edit or delete any existing comment.


https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702

[A10] **Ruling on [A557] STOP (6022346110): proceed to review; the manager runs the missing gates.**

1. **Builder gate 1b** exceeded the session's 580 s foreground limit, which is not a gate failure. The merge-train candidate's builder bank runs all 48 commands with no foreground limit. It decides.
2. **Hosted and act evidence** come from the PR, which the manager opens now.
3. **Linked-image sizes.** No linked ctrl or ctrl_nvm image exists until SoC integration (after F2 to F5). For this PR, acceptance item 3 is met by the object sizes and static frames you report, with that limit stated. The linked-image size and stack bounds become an acceptance item of the integration lane.

The PR body is updated from "blocked" accordingly. Reviews start at `0a004a8c`.

Do not edit or delete any existing comment.


PR: https://github.com/kebag-logic/milan-fpga/pull/683

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

REVIEW READY under the manager ruling 6022358702: local implementation committed at `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe`; builder gate 1b, hosted and act results come from the merge-train candidate and this PR. `679-rv32-sdk` -> `dev`.

Both firmware suites pass with RV32 required, including all five store shapes and 434 store tests. The ctrl campaign catches all 76 mutants; that run preceded the final ISA-attribute check, which the final positive suites and build self-test exercise. The 15 new RV32 controls pass. Coverage remains 100 percent adjusted lines and branches for all 14 files at the unchanged ratchet. The store campaign catches all 106 mutants using the original driver with reusable physical worker directories. The builder bank does not have a complete passing verdict. No hosted or act success is claimed.

## Linked Issue / roles

Closes #679
Relates to #665

Executor: `[A557]`
Internal cleared-context reviewer: `[R526]`
External reviewer: `[R527]`

## Description

The ctrl RV32 arm previously reached the pinned ILP32D SDK's hosted libc headers while compiling for ILP32, failing on the missing ILP32 glibc stub. Both validation arms now isolate freestanding compiler headers and the existing memory/formatter declarations, retaining RV32I and ILP32. Both reject unexpected runtime symbols, wrong architecture or ABI, and non-static frame reports.

The workflow installs the same pinned SDK before both firmware suites and requires their RV32 arms. The canonical CI contract checks that ordering and rejects removal of either required-RV32 flag. A new self-test plants header, ISA, ABI, heap, unknown-service and stack-protection defects.

Ctrl object totals remain text/data/BSS 11520/0/170 bytes. Store text falls by 240 bytes per shape after disabling SDK-injected stack protection in validation objects; data, BSS, static buffers and largest static frames remain unchanged. The largest static frame is 112 bytes for ctrl and 128 bytes for each store shape. These are object and frame measurements, not linked-image sizes or whole-program stack bounds.

## Authoritative references

- [Assignment on #679](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923)
- [Firmware integration contract #665](https://github.com/kebag-logic/milan-fpga/issues/665)
- [Product ownership and verification requirements](REQUIREMENTS.md)
- [Firmware test harness and RV32 evidence limits](sw/firmware/gtest/README.md#rv32-object-builds)
- [CI workflow policy](docs/testing/CI_WORKFLOWS.md)
- [Shipping bare-metal build](sw/firmware/milan_baremetal/Makefile)

## How to get into the same state

Use the publisher's branch once publication is authorized; this session did not push it. The local branch starts at `6714181d0c8a16e2983f85b724f4d688f5111835` and adds one commit.

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

Expected: every required command exits zero, all 76 ctrl and 106 store mutants are caught, both RV32 arms run, all five shapes pass, and the existing coverage ratchet holds. The handoff records the full documentation gate table. The standard store command exceeded the foreground limit; `nvm_foreground.py` retained its original driver and all grading while reusing one physical mutant directory per worker, completing in 392.3 seconds. The builder gate still needs an execution arrangement that can finish within the session's foreground limit. After an authorized publication, run the trusted validation-base act runner before inspecting hosted results, following the CI policy, and attach the firmware-unit hosted log.

## Known limitations / out of scope

- This implements freestanding object compilation with the existing pinned SDK. It does not add a linked `-nostdlib` image or runtime implementation. The assignment's linked-image and whole-stack evidence remains unfulfilled.
- Hosted and supported act execution require publication and a PR, which this session forbids. Their verdicts remain pending.
- Builder gate 1b timed out twice at 580 seconds. The other 99 functions returned successfully, with area calibration explicitly not run without a route report. Partial results do not clear the builder bank.
- Firmware behavior sources, shipping-image inputs and RTL are unchanged. There is no hardware or bench evidence.
- The existing coverage exclusions are unchanged, including the ADP premise recorded under #678. Optional private-dependency validation remains separate.

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

