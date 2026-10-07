[A560]

## Contents

- **[Status](#status)** -- Local implementation and validation status.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and independent reviewers.
- **[Description](#description)** -- SRP behavior and dependency changes.
- **[Authoritative references](#authoritative-references)** -- Requirements and protocol clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Exact branch, dependency and environment.
- **[How to validate](#how-to-validate)** -- Reproducible gates and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Integration and release evidence still owed.
- **[Definition of Done](#definition-of-done)** -- Remaining merge obligations.

## Status

Local F4 implementation is ready for independent review; assigned gates pass, with the builder’s existing optional gate 11 calibration arm skipped because its external utilization report is absent. `665-f4-srp` -> `dev`.
Head: `50d492c12789e1d80bf11f547e7fe53e02b4bdb9`.
No remote PR or review verdict has been created.

## Linked Issue / roles

Relates to #665.

Executor: `[A560]`
Internal cleared-context reviewer: `[R532]`
External reviewer: `[R533]`

## Description

Add per-interface MSRP/MVRP on the bare-metal mailbox using the exact lwSRP submodule pin. Startup declares every output as Advertise or Failed, announces the Class A Domain and joins its VLAN. The binding port declares Listeners for matching registered Talkers. VLAN output commits before Talker permission or Listener Ready. A withdrawal received in LV after LeaveAll stops the Talker at the original five-second deadline.

Allocation uses an entity-sized static pool. The adapter retains refused output unchanged, drains earlier timer events before new SRP input, isolates link resets by interface, and rejects synchronous reentry. Host tests cover both interface counts and every shipped entity shape. Firmware CI now fetches the dependency and requires the shared freestanding RV32 checks and control mutation campaign.

The local upstream stack adds Apache-2.0 licensing and fixes timer ownership, wire encoding, receive validation, transactional/segmented output, bounded storage, registration replacement and Listener redeclaration. The final pin is `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da` on local branch `zephyr-api-docs`. Upstream publication and review precede parent publication.

## Authoritative references

- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477), #608, #678 and #679; protocol-processor #134.
- `REQUIREMENTS.md` section 1; `docs/reference/FR_NFR.md` NFR-SCOUT-02/03/08 and H-SRP.
- `docs/design/MAILBOX_SPLIT.md`; `sw/firmware/ctrl/srp/README.md`.
- IEEE 802.1Q-2018 Tables 10-3/10-4, clauses 10.7.11, 35.1.2.2, 35.2.2.7.2 and 35.2.6.
- Milan v1.2 Table 4.3, 4.3.2 and 5.5.2.7.

## How to get into the same state

After the manager publishes the parent and upstream prerequisite commits:

```sh
git fetch origin 665-f4-srp
git switch 665-f4-srp
git rev-parse HEAD
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
python3 scripts/ci_rv32_sdk.py --destination "${SDK}"
export MILAN_RV32_CC="${SDK}/bin/riscv32-linux-gcc"
export TMPDIR="${SCRATCH}"
export PYTHONDONTWRITEBYTECODE=1
export PYTHON_CPU_COUNT=4
export VERILATOR_JOBS=2
```

`SDK` and `SCRATCH` name caller-selected disk directories. Put pinned Verilator 5.050 on `PATH` and export `VERILATOR` to that entrypoint. The SDK distribution is ilp32d; the cacheless core objects are RV32I/ILP32, freestanding, as specified by #679. The SDK archive SHA-256 is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`.

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/mbx -j1
python3 sw/mailbox/gen_mailbox.py --check
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
python3 scripts/check_doc_paths.py
python3 scripts/gen_toc.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_hygiene.py --check
python3 scripts/lint_rtl.py --check
```

Expected: every applicable command returns zero. Use a build wrapper that limits generated C++ child builds to eight jobs and at most two simultaneous Verilator builds. The handoff records the bounded scratch replicas and batch commands used locally.

Passing evidence includes 30 adapter, three debug, four timing and five wire-differential cases at each interface count; ten entity-shape runs; ten SRP RV32 builds; 43 SRP and 97 existing firmware mutations; 17 shared RV32 controls; and 434 saved-state tests. The adapter has 359/359 lines and 342/342 branch arcs, with no exclusions. All 15 measured firmware files remain at 100% after existing exclusions. The original processor suites pass 1,219 and 2,200 checks, with storage-shape runs also passing. Every local upstream fix branch passes cgreen and behave. All 15 added upstream regression cases reject their planted source defects. The builder bank completes all 100 original functions; gate 11 calibration is explicitly not covered.

## Known limitations / out of scope

- F3 is absent from the assigned FC base. Its application binding wiring, actual licence output and dynamic MAAP allocation composition remain integration work under #665.
- Host timing assumes 100 ns per mailbox access, one aggregate 1 ms CPU/preemption allowance and 100 ns observation uncertainty. Target and wire timing must validate these assumptions; object stack frames do not prove a call-chain bound.
- The selected processor wire differential documents two normative differences: delayed Lv deregistration under Table 10-4, and retaining a valid Listener subtype on withdrawal under 35.2.2.7.2. It is not an exhaustive walk of every processor state.
- The full repository RTL/synthesis merge bar and protected hosted contexts remain integration evidence to obtain before validation.
- The private dependency must become fetchable before hosted CI and merge. The manager still owns FC/dev integration, upstream publication, independent reviews and candidate-merge validation.
- No RTL, register map, default all-fabric build or shipping image changes are included.

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
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
