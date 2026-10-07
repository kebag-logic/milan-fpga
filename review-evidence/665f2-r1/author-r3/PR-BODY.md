[A558]

## Contents

- **[Status](#status)** -- Local evidence and branch target.
- **[Linked Issue / roles](#linked-issue--roles)** -- Assignment and reviewers.
- **[Description](#description)** -- Behavior and integration.
- **[Authoritative references](#authoritative-references)** -- Requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Prerequisites.
- **[How to validate](#how-to-validate)** -- Commands and expected results.
- **[Round 3](#round-3)** -- Dev merge, SDK preservation and link-bounce regression.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Remaining proof.
- **[Definition of Done](#definition-of-done)** -- Implementation and merge bar.

## Status

Round 3 local gates pass; ready for independent review and manager publication.
`665-f2-maap` -> `dev`. Head: `8b78a8fd36864246336c71c061ac4f21d629952f`.
193 controller defects and 16 differential controls caught; all 17 files meet
100% line/branch coverage after the existing exclusions. The 93-entry builder/docs
bank exits zero with the explicit physical-tool/calibration limits below.
The branch has not been pushed. Prior positive delta reviews cover `938497af`;
this new head still needs independent review.

## Linked Issue / roles

Relates to #665.

Executor: [A558].
Internal cleared-context reviewer: [R528].
External reviewer: [R529].

Assignments: #665 comments 6026720272, 6029239721 and 6029938743.
R528-2 and R529-2 positive delta reviews: PR #687 comments 6029935831 and
6029833929. Earlier negative findings and corrected-head evidence remain in
HANDOFF.md's historical Round 1 and Round 2 sections.

## Description

Adds a static MAAP core per interface with INITIAL/PROBE/DEFEND transitions,
complete PDUs, seeded randomization, three probe retransmissions, conflict
priority, release and retry. Deferred output retains its original timer obligation.
Ports reject synchronous reentry. The adapter uses the FC MAAP channel, indexed
link state and tagged timers.

The explicit composition enables MAAP RX interrupts alongside ADP and events.
A valid range supplied with Begin! while down survives until the next operational
port and is consumed once. Tests cover actual idle wait/wake at one and two
interfaces, restart and link-bounce draws, all six priority octets, CSR direction
and complete destination-before-enable ordering, plus stalled output on interface 1.

The differential observes software timer deadlines and parent frame completion
cycles. It grades strict 500 < T < 600 ms core intervals, the parent's 500..627 ms
delta, and four core PROBEs starting immediately versus three delayed parent
PROBEs. Controls reject 1/500/600 ms core intervals and falsified parent bounds/counts.
All twelve cases remain; the README lists every #686 delta.

`maap_csr_allocation` programs existing AAF/CRF destinations and the talker window,
closing admission before changes and restoring it after all destination writes.
Its integration dependency is mandatory: clearing `MAAP_CTRL[0]` disables
`KL_maap`, so `KL_pp_maap_shim` never answers ALLOC_DA ok and `talker_active`
never asserts. Before this output is used, feed the processor's MAAP face from
firmware allocation, or move ACMP onto the core through F3. This is a #664
decision-3 default-flip condition; F2 documents it without changing that wiring.

## Authoritative references

- IEEE 1722-2016 B.2; B.3.2/Table B.7 and note a; B.3.3/Table B.8;
  B.3.4.1/.2; B.3.5.1 through B.3.5.9; B.3.6.1 through B.3.6.7; B.4.
- `docs/reference/FR_NFR.md`: NFR-SCOUT-02/03/08 and H-MAAP.
- `docs/design/MAILBOX_SPLIT.md` and `sw/mailbox/mailbox.yaml`.
- `sw/firmware/ctrl/maap/README.md`: API, work bounds and proof limits.
- #678: no synchronous callbacks into protocol cores.
- #679: shared freestanding RV32 SDK and object/runtime checks.
- #686 and comment 6029233665: parent deviations, including probe count.
- #664 decision 3: placement/default-flip obligations.

## How to get into the same state

Use the published objects for this head when available. Provide host C/C++
compilers and test libraries, pinned Markdown/HDL parser dependencies, version
5.050 of the simulator, and the repository-pinned RV32 SDK. CHECK_ROOT is
disk-backed scratch outside the lane and this packet. Run recipe and mailbox
builds in an isolated checkout so generated files remain in scratch.

```sh
git checkout 665-f2-maap
test "$(git rev-parse HEAD)" = 8b78a8fd36864246336c71c061ac4f21d629952f
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
export TMPDIR="${CHECK_ROOT:?}"
export VERILATOR="${PINNED_VERILATOR:?}"
export VERILATOR_JOBS=2
export MAKEFLAGS=-j8
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/ci_rv32_sdk.py --destination "$CHECK_ROOT/rv32-sdk"
export MILAN_RV32_CC="$CHECK_ROOT/rv32-sdk/bin/riscv32-linux-gcc"
```

The shared override replaces the controller-only override. The ilp32d SDK emits
RV32I/ILP32 freestanding release objects through isolated headers; no hosted
library is linked. Limit simultaneous simulation builds to two, make workers
to eight and campaign/coverage workers to four.

## How to validate

Run each mutation partition separately with INDEX from 0 through 3. Together
they execute all 193 controls; every shard also executes all positive arms.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard INDEX 4 --build-dir "$CHECK_ROOT/ctrl-INDEX"
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/mbx -j1 VBUILD_JOBS=8
python3 sw/builder/test_builder.py --require-rv32
```

Run the complete builder/static bank and documentation workflow commands from
CONTRIBUTING and #664 comment 6014810929, using
`910f338dbd050f4efd2d96991ddcf928a583d55f` for diff checks. HANDOFF.md records
every command, exit, evidence hash and the bounded foreground partitions of the
original long builder/profile functions. The audit proves complete/disjoint
fixture coverage with unchanged assertions in SDK and compiler-absent modes.

Measured: all final commands exit zero; 193/193 controller defects, 16/16
differential controls, 17/17 RV32 build self-test checks, 434 saved-state tests
across five shapes and 100% line/branch coverage for all 17 files after existing
exclusions. F2 executes 75 cases: 37 core/CSR, 12 mailbox at one interface, 13 at
two, one debug and 12 differential. The three MAAP C files have no exclusions;
the ratchet and exclusion files are unchanged. Listener/tally and coverage checker
self-tests also pass. The mailbox suite passes both bus/interface configurations,
co-simulation and all five quick controls. The inherited dev AAF startup gate
passes 34,020 checks and catches all eight controls.

All 93 builder/documentation bank entries exit zero. Vendor analysis is SKIPPED
without its analyzer; historical placement calibration is NOT RUN without its
report. Compiler-absent profile runs intentionally skip compile-only claims,
which the SDK profile runs separately measure. No skip supplies physical proof.

## Round 3

Assignment: #665 comment 6029938743. Merge commit
`5901ab0869e0674bb18bbb4df60757f2711e5cd4` has ordered parents
`938497af1dffd8a87edebf3ab93663914bf85e5e` and
`910f338dbd050f4efd2d96991ddcf928a583d55f`. No rebase or amend was used.
Conflict resolution retains #679's isolated-header, ELF ABI/ISA, static-frame
and runtime dependency checks alongside every MAAP source, arm, mutation partition
and named obligation. No check was dropped or re-graded.

`a71b8c8072c28c3511254484de5dda4e57e91d3f` adds
`MaapCore.LinkBounceDrawsAfterSuppliedRange`: Begin! with a supplied range,
then operational up/down/up, with a fresh in-pool draw and complete probe after
the bounce. `r2-saved-range-never-consumed` compiles and fails its exact fresh-range
assertion. The README now counts ten arms plus optional `lwsrp`.

`8b78a8fd36864246336c71c061ac4f21d629952f` fixes the integration failure exposed
by isolated SDK headers: assertion include and use are both debug-only. Release
behavior is unchanged, and the host debug assertion and its planted defect still
run. Superseded failures and corrected-head results are separated in HANDOFF.md.

## Known limitations / out of scope

H-MAAP charges 100 ns per ordered mailbox access on a monotonic host clock.
Wake cases measure 4,700 ns from RX_HEAD publication; the interface-1 stall
measures 5,004,400 ns including its 5 ms stall. Callback bound: 48 accesses;
standalone pass bounds: 616/664 at one/two interfaces. The service limit is 10 ms
against the shared 50 ms ceiling. Target CPU time, bus arbitration, wire departure,
media quiescence, NVM overlap and bench acceptance remain integration obligations.

RV32 validation covers `-DNDEBUG` freestanding objects. Host debug assertions
do not prove target debug linkage, a linked image or whole-program stack usage.
The controller's largest static frame is 112 bytes; saved-state is 128 bytes.
#679's ilp32d SDK path is included, with strict object/runtime checks intact.

No new F2 RTL, register-definition, shipping-image, placement-default or submodule-pin
change. The authorized dev merge imports existing dev history; FC remains stacked.
The platform supplies ordered CSR access, exclusive stream-window ownership and
quiescence before first ownership transfer. The allocation-to-ACMP dependency
above must be resolved before this output is used.

The manager performs the later trivial dev merge after FC #685 lands. Publication,
independent review of this head, hosted/local-replica evidence, candidate-merge
validation and post-merge containment remain pending. Positive R528-2/R529-2
verdicts cover the preceding head and do not approve this delta.

The service recorded a cumulative memory peak of 11,011,305,472 bytes, above the
requested 9 GB ceiling; its initial value was not captured. Concurrency was reduced,
and later current samples were below the ceiling. This run does not establish
compliance with that memory limit. The disk free-space floor was preserved.

## Definition of Done

- [x] Lane implementation acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification passes with the stated unavailable physical checks
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at the current head
- [ ] External review is positive at the current head
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING
- [x] Documentation is updated where needed
- [ ] Post-merge containment is checked before the Issue moves to Done
