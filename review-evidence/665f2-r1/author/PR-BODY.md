[A558]

## Contents

- **[Status](#status)** -- Local evidence and branch target.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and independent reviewers.
- **[Description](#description)** -- Protocol behavior and integration.
- **[Authoritative references](#authoritative-references)** -- Requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Source and prerequisites.
- **[How to validate](#how-to-validate)** -- Reproducible gates and expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Remaining integration proof.
- **[Definition of Done](#definition-of-done)** -- Implementation and merge requirements.

## Status

REVIEW READY: implementation and authorized local gates pass; independent review pending.
`665-f2-maap` -> `dev`. Head: `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`.

## Linked Issue / roles

Relates to #665.

Executor: [A558].
Internal cleared-context reviewer: [R528].
External reviewer: [R529].

Assignment: #665 comment 6026720272; resumed on FC round 2, comment 6026839422.

## Description

Adds a static, per-interface MAAP core with INITIAL/PROBE/DEFEND transitions,
complete PDUs, seeded randomization, three probe retransmissions, conflict
priority, release and retry. Deferred output retains its original timer obligation.
Synchronous reentry asserts in debug builds and is counted and ignored in release builds.

The mailbox adapter uses the FC MAAP channel, indexed link state and tagged timers.
The explicit `ctrl_app_start_maap` composition supplies the allocation callback.
`maap_csr_allocation` programs the existing AAF and CRF destination registers and
indexed stream window, closing admission before allocation loss or updates.
The ordinary startup and shipping all-fabric policy remain unchanged.

Host coverage includes every receive/state/priority cell, one and two interfaces,
all supported output counts, stalled rings, timer wrap and the complete allocation
callback path. The parent differential checks shared stimulus against Annex B
and explicitly records the known #686 deviations.

## Authoritative references

- IEEE 1722-2016 B.2; B.3.2/Table B.7; B.3.3/Table B.8; B.3.4.1/.2;
  B.3.5.1 through B.3.5.9; B.3.6.1 through B.3.6.7; B.4.
- `docs/reference/FR_NFR.md`: NFR-SCOUT-02/03/08 and H-MAAP.
- `docs/design/MAILBOX_SPLIT.md` and `sw/mailbox/mailbox.yaml`.
- `sw/firmware/ctrl/maap/README.md`: API, work bounds and proof limits.
- #678: ports must not call a protocol core synchronously.

## How to get into the same state

Use this branch with its pinned submodules initialized.
The environment must provide the repository-pinned simulator, host C/C++ compilers,
test libraries, a freestanding RV32I compiler and the documented gate dependencies.
Set TMPDIR to disk-backed scratch and VERILATOR to the pinned executable.
Set CTRL_RV32_CC to the selected bare-metal compiler when the default SDK lacks ILP32 headers.
Use at most two simulation builds and four campaign workers.

```sh
git checkout 665-f2-maap
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
export VERILATOR_JOBS=2
```

## How to validate

Run each mutation partition separately, with INDEX from 0 through 7:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard INDEX 8
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/tally_selftest.py
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/mbx -j1 VBUILD_JOBS=8
python3 sw/builder/test_builder.py --require-rv32
```

Run the complete [builder and documentation command bank](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6014810929)
from CONTRIBUTING and the documentation workflow, using the resumed base for diff checks. Keep generated build products in scratch.
The recorded run splits long campaigns and the builder's original test-function
sequence into bounded foreground invocations. Its long bare-metal profile also
partitions independent case lists, preserving every original assertion; the receipt
manifest checks complete, disjoint case coverage in SDK and absent-compiler modes.

Expected: all commands exit zero; 100% line and branch coverage for all three
new portable C files with no exclusions; every planted defect fails its named test.
Measured: 66 new test cases, 180 controller defects caught and 11 differential
defects caught. All 17 coverage files meet the ratchet. All 93 builder/documentation bank entries completed with zero exits, using bounded
partitions where needed. The vendor analyzer and historical placement calibration remain
explicitly unavailable; the latter requires its earlier report.

## Known limitations / out of scope

H-MAAP establishes mailbox-access bounds and monotonic model-time checks under
an explicit 100 ns transaction assumption. The callback bound is 48 accesses;
the standalone pass bound is 616 at one interface and 664 at two.
The project service limit is 10 ms against the shared 50 ms ceiling.
Target CPU time, bus arbitration, wire departure, media quiescence, NVM overlap
and bench acceptance remain later placement-integration obligations.

No RTL, register definitions, shipping image or placement defaults change.
The platform supplies the ordered datapath CSR operations and exclusive ownership
of the stream window. Existing media must be quiescent before first ownership transfer.
The parent fabric's Annex B deviations remain #686.
Independent reviews, hosted checks, candidate-merge validation and integration
into dev remain pending. This lane neither pushes nor merges.

## Definition of Done

- [x] Linked Issue implementation acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
