[A560]

## Contents

- **[Status](#status)** -- Validation state.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and review roles.
- **[Description](#description)** -- Resulting behavior.
- **[Round 2](#round-2)** -- Accepted findings and evidence.
- **[Authoritative references](#authoritative-references)** -- Applicable contracts.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Dependencies.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Remaining integration.
- **[Definition of Done](#definition-of-done)** -- Review and merge bar.

## Status

STOP: local validation incomplete. `665-f4-srp` -> `dev`.
Head: `42a0371affceb2a07a734449d706be01fa5abc9a`. No push or PR update was performed.
The required builder contract function exceeded two 550-second foreground windows.
The other 99 builder functions completed; the missing function is not counted as passed.
The existing optional resource-calibration arm also lacked its external report.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`.
Internal reviewer: `[R532]`.
External reviewer: `[R533]`.
Both round-1 reviews were negative. Re-review remains required.

## Description

Provide per-interface MSRP and MVRP through the bare-metal mailbox, using the exact lwSRP dependency and entity-sized static pools. Startup declares every output, Class A Domain and its VLAN. The binding port reconciles Listener declarations, and licence output follows admission, registration and committed VLAN membership. Refused output retains its bytes and interface until commit.

## Round 2

Merged the assigned dev head `d51b373a` with `--no-ff` and pinned the integrated lwSRP port `23d9a817`. The merged compiler, assertion and reentry checks remain mandatory.

MSRP IN/rLv now leaves immediately under Milan v1.2 4.2.7.2.2. MVRP retains the generic Registrar behavior; Lv received in LV retains the original LeaveTime deadline. D1 now agrees with the processor. D2 retains the Listener declaration subtype on withdrawal.

Link events preserve short down/up interruptions. Reset restores the default Domain, revokes old licences and fences the affected interface's published receive prefix. Shared StreamID declarations combine all eligible bindings, including different destinations and VIDs. Failed recreation releases partial participants and retries without starving the other interface.

The adapter has 41 cases at each interface count. Named plants discriminate both Ethernet overhead terms, the 75% boundary, immediate withdrawals, stale input, shared declarations, retry and strict Ready-to-ReadyFailed licence continuity. The upstream note 4/5 tests and reversals are on local branch `f4-applicant-notes`, head `495520f`; the assigned parent pin is unchanged pending dependency review.

Linked composition spans 53,856 bytes for the one-interface 1x1 shape and 94,576 bytes for the two-interface 8x8 shape. These totals include static pools, alignment and an explicit 8192-byte stack reservation. The corresponding merged-base totals are 19,200 and 19,696 bytes. Both shapes and both interface counts are recorded separately. These are linked size fixtures with observed licence outputs, not booted images or routed resource measurements.

S1's LeaveAll type/port regression exists in the integrated dependency. S2's optional generic callback concern remains for upstream disposition; this adapter uses retained attribute values and does not depend on an extra Join indication. The integration role must carry the notes to dependency PR #12 because this assignment permits public posts only on #665. S3's recreation failure is guarded and tested. TICK documentation now distinguishes centiseconds from NOW_MS.

## Authoritative references

- Issue #665 assignment comments 6030279477 and 6033558691; acceptance addition 6030870481.
- R532-1 and R533-1 in `review-evidence/665f4-r1/reviews/` on `665f4-review-evidence`.
- `REQUIREMENTS.md` section 1; `docs/design/MAILBOX_SPLIT.md`.
- `docs/reference/FR_NFR.md`: NFR-SCOUT-02, NFR-SCOUT-03 and NFR-SCOUT-08.
- Milan v1.2 4.2.7.2.2, 4.3.2, 5.5.2.7 and Table 4.3.
- IEEE 802.1Q-2018 Tables 10-3/10-4, 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- Issue #608, #678, #679 and processor issue #134.

## How to get into the same state

After the integration role publishes the parent commits:

```sh
git switch 665-f4-srp
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
export TMPDIR="$SCRATCH"
export MILAN_RV32_CC="$SDK/bin/riscv32-linux-gcc"
export VERILATOR="$PINNED_VERILATOR"
export VERILATOR_JOBS=2
```

Use the CI-pinned SDK distribution and pinned HDL compiler version 5.050. Firmware code targets RV32I/ILP32. Keep build output on disk, compiler workers bounded, and at most two HDL builds active.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$SCRATCH/firmware"
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
make -C tb/verilator/mbx
python3 sw/mailbox/gen_mailbox.py --check
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/ci_events.py --selftest
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
```

Require zero exits, all named plants rejected and the 100% ratchet with no new exclusions. HANDOFF.md, ROUND2-GATES.md and ROUND2-TESTS.md contain the complete command, coverage and defect tables. The builder contract still needs a complete run within an approved execution arrangement. It is the reason this handoff is STOP.

For linked size, run `ctrl_image_runtime.py` from the provisioned runtime sources, then `ctrl_image.py` for both entity shapes and interface counts. Repeat with `--without-srp --ctrl-source "$BASE_CTRL"` for each exported base. Runtime provenance and binary hashes are retained separately; the measurement scripts leave the shipping build untouched.

## Known limitations / out of scope

- ACMP application wiring, live MAAP allocation input and connected fabric licence output remain integration work; F3 is absent from the assigned base.
- The latency figures are a conditional host service envelope, with one shared 10 ms budget. Target scheduling and wire timing still require release evidence.
- The reserved stack size is not a whole call-chain proof.
- No RTL, non-mailbox register, default all-fabric configuration or shipping-image change is included.
- Hosted gates, dependency publication/review, candidate-merge validation and physical release work are not claimed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are fully satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
