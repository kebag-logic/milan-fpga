[A558]

## Contents

- **[Status](#status)** -- Local evidence and branch target.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and reviewers.
- **[Description](#description)** -- Behavior and integration.
- **[Authoritative references](#authoritative-references)** -- Requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Prerequisites.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Round 1](#round-1)** -- Earlier evidence and review status.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Remaining proof.
- **[Definition of Done](#definition-of-done)** -- Implementation and merge bar.

## Status

REVIEW READY: round 2 implementation and authorized local gates pass; independent re-review pending.
`665-f2-maap` -> `dev`. Head: `938497af1dffd8a87edebf3ab93663914bf85e5e`.
Both round-1 reviews were NEGATIVE; corrected-head independent review is required.

## Linked Issue / roles

Relates to #665.

Executor: [A558].
Internal cleared-context reviewer: [R528].
External reviewer: [R529].

Assignment: #665 comments 6026720272 and 6029239721.
Reports: PR #687 comments 6029234761 and 6028867882; packets under
`review-evidence/665f2-r1/reviews/` on `665f2-review-evidence`.

## Description

Adds a static MAAP core per interface with INITIAL/PROBE/DEFEND transitions,
complete PDUs, seeded randomization, three probe retransmissions, conflict
priority, release and retry. Deferred output retains its original timer obligation.
Ports reject synchronous reentry. The adapter uses the FC MAAP channel, indexed
link state and tagged timers.

Round 2 fixes two behavior defects: the explicit composition enables MAAP RX
interrupts alongside ADP and events, and a valid range supplied with Begin! while
the port is down survives until the next PortOperational!. Standing tests cover
actual idle wait/wake at one and two interfaces, fixed-seed restart, all six
MAC-priority octets, CSR direction and complete write ordering, and stalled output
on interface 1. Eight review defects and four generic predicate defects extend
the controller campaign, with credit to R528-1 and R529-1.

The differential now observes software timer deadlines and parent frame completion
cycles. It grades strict 500 < T < 600 ms core intervals, the parent's 500..627 ms
delta, and four core PROBEs starting immediately versus three delayed parent
PROBEs. Five new controls reject 1/500/600 ms core intervals and falsified parent
bounds/counts. All previous eleven cases remain; the README lists every #686 delta.

`maap_csr_allocation` programs existing AAF/CRF destinations and the talker window,
closing admission before changes and restoring it after all destination writes.
Its integration dependency is mandatory: clearing `MAAP_CTRL[0]` disables
`KL_maap`, so `KL_pp_maap_shim` never answers ALLOC_DA ok and `talker_active`
never asserts. Before this output is used, feed the processor's MAAP face from
the firmware allocation, or move ACMP onto the core through F3. This is a #664
decision 3 default-flip condition; F2 records it without changing that wiring.

## Authoritative references

- IEEE 1722-2016 B.2; B.3.2/Table B.7 and note a; B.3.3/Table B.8;
  B.3.4.1/.2; B.3.5.1 through B.3.5.9; B.3.6.1 through B.3.6.7; B.4.
- `docs/reference/FR_NFR.md`: NFR-SCOUT-02/03/08 and H-MAAP.
- `docs/design/MAILBOX_SPLIT.md` and `sw/mailbox/mailbox.yaml`.
- `sw/firmware/ctrl/maap/README.md`: API, work bounds and proof limits.
- #678: no synchronous callbacks into protocol cores.
- #686 and comment 6029233665: parent deviations, including probe count.
- #664 decision 3: placement/default-flip obligations.

## How to get into the same state

Provide host C/C++ compilers, test libraries, the repository-pinned simulator
and a bare-metal RV32I compiler. CHECK_ROOT must be disk-backed scratch outside
the source and output packet. PINNED_VERILATOR must select version 5.050;
RV32_CC selects the bare-metal compiler for this pre-#679 head.

```sh
git checkout 665-f2-maap
test "$(git rev-parse HEAD)" = 938497af1dffd8a87edebf3ab93663914bf85e5e
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
export TMPDIR="${CHECK_ROOT:?}"
export VERILATOR="${PINNED_VERILATOR:?}"
export CTRL_RV32_CC="${RV32_CC:?}"
export VERILATOR_JOBS=2
export PYTHONDONTWRITEBYTECODE=1
```

Use the pinned Markdown and HDL parser requirements for documentation gates.
Keep dependencies, exports and generated files in scratch. Limit simulation builds
to two concurrently, make to eight jobs, and campaign workers to four.

## How to validate

Run each mutation partition separately, with INDEX from 0 through 3:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard INDEX 4
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/mbx -j1 VBUILD_JOBS=8
python3 sw/builder/test_builder.py --require-rv32
```

Run mailbox and builder commands in an isolated checkout to retain generated
files in scratch. Run the complete builder/static bank and documentation workflow
commands from CONTRIBUTING and #664 comment 6014810929. Use
`db9aa8c9b135b34ff3d070a979dee70440b37cc6` for this stacked lane's diff checks.
The handoff records bounded foreground partitions of the original builder
function sequence and long bare-metal profile, with complete/disjoint fixture
coverage and unchanged assertions in SDK and compiler-absent modes.

Expected: zero gate exits, 192 controller defects caught by named checks,
16 differential controls caught, and 100% line/branch coverage at the ratchet.
The F2 suite executes 74 cases: 36 core/CSR, 12 mailbox at one interface, 13 at
two, one debug and 12 differential. All 17 coverage files pass; the three MAAP C
files have no exclusions. Measured: 192 controller defects and 16 differential
controls caught; all 93 builder/documentation bank entries returned zero.
HANDOFF.md records exact commands, partition audits and evidence hashes.
Vendor analysis is SKIPPED without its analyzer; historical placement calibration
is NOT RUN without its report. Neither supplies physical proof.

## Round 1

Earlier head: `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`.
Recorded evidence: 66 F2 executions, 180 controller defects caught, 11 differential
controls caught, 17 files at the coverage ratchet and the 93-entry builder/docs
bank with zero exits. The vendor and calibration limits were the same.
Full original tables and receipt hashes remain in HANDOFF.md's Round 1 section.

R528-1 and R529-1 then identified the missing wake interrupt, lost down-link
preference, differential timing gap, escaped restart/priority/CSR/poll defects
and missing integration dependency. Their negative reviews supersede the earlier
review-ready status; old evidence is not a corrected-head verdict.

## Known limitations / out of scope

H-MAAP charges 100 ns per ordered mailbox access on a monotonic host clock.
New wake cases measure 4,700 ns from original RX_HEAD publication; the interface-1
stall measures 5,004,400 ns including its 5 ms stall. Callback bound: 48 accesses;
standalone pass bounds: 616/664 at one/two interfaces. The service limit is 10 ms
against the shared 50 ms ceiling. Target CPU time, bus arbitration, wire departure,
media quiescence, NVM overlap and bench acceptance remain integration obligations.

RV32 validation covers `-DNDEBUG` freestanding objects. The host debug assertion
does not prove target debug linkage, a linked image or whole-program stack usage.
#679's ilp32d SDK path is absent while PR #683 remains open.

No RTL, register definitions, shipping image, placement default or submodule pin
changes. The platform supplies ordered CSR access, exclusive stream-window
ownership and quiescence before first ownership transfer. The allocation-to-ACMP
dependency above must be resolved before this output is used.

PRs #683 and #685 remain open at final handoff. Under assignment item 9, the
manager runs the merge round if #683 remains open at handoff, retaining both SDK
builds and MAAP arms/partitions and rerunning the whole firmware gate set.
Publication, independent re-review, hosted/local-replica evidence, candidate-merge
validation and post-merge containment remain pending.

## Definition of Done

- [x] Linked Issue implementation acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes, with the stated unavailable-tool/calibration limits
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
