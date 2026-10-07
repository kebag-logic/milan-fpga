[A558]

## Contents

- **[Status](#status)** — Local evidence and branch target.
- **[Linked Issue / roles](#linked-issue--roles)** — Assignment and reviewers.
- **[Description](#description)** — Behavior and integration.
- **[Authoritative references](#authoritative-references)** — Requirements and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Setup.
- **[How to validate](#how-to-validate)** — Commands and expected results.
- **[Round 4](#round-4)** — Final merge, debug build and linked sizes.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — Remaining proof.
- **[Definition of Done](#definition-of-done)** — Implementation and merge bar.

## Status

Round 4: Local validation passed; ready for independent review and manager publication.
`665-f2-maap` -> `dev`. Head: `5968967e19411428b71dde5c4712d4a8fa528cfb`.
The authorized dev merge includes FC and #677. This head is not pushed.
196 controller defects and sixteen differential controls caught; all seventeen
coverage files meet 100% lines/branches after the existing exclusions.
The 93-entry builder/documentation bank passes with the explicit unavailable
physical checks below. Independent reviews and publication remain pending.

## Linked Issue / roles

Relates to #665.

Executor: [A558]. Internal cleared-context reviewer: [R528]. External reviewer: [R529].

Round 4 assignment: #665 comment 6033552374. Linked-size acceptance addition:
comment 6030870481. Earlier assignments: comments 6026720272, 6029239721 and
6029938743. R528-3-F1 and R529-3-F1 are addressed; R528-3-S1 now has target
debug compile evidence. Earlier verdicts do not approve this head.

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

Use the published objects for this head after manager publication. Provide host
C/C++ compilers, GoogleTest/GoogleMock, pinned Markdown/parser dependencies,
Verilator 5.050 and the repository-pinned RV32 SDK. CHECK_ROOT is disk-backed
scratch outside the lane and evidence packet. Run generator/build recipes in
an isolated checkout so generated files stay outside the implementation tree.

```sh
git checkout 665-f2-maap
test "$(git rev-parse HEAD)" = 5968967e19411428b71dde5c4712d4a8fa528cfb
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis
export TMPDIR="${CHECK_ROOT:?}"
export VERILATOR="${PINNED_VERILATOR:?}"
export VERILATOR_JOBS=2
export MAKEFLAGS=-j8
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/ci_rv32_sdk.py --destination "$CHECK_ROOT/rv32-sdk"
export MILAN_RV32_CC="$CHECK_ROOT/rv32-sdk/bin/riscv32-linux-gcc"
```

Before any Git command inside a submodule, verify its reported top-level directory
is that submodule. Limit simultaneous simulation builds to two, make workers to
eight and campaign/coverage workers to four. The isolated SDK headers support
RV32I/ILP32 object checks without linking hosted libraries.

## How to validate

Run each controller partition separately, INDEX 0 through 7. Together they grade
all 196 controls; every partition also runs every positive arm.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2 --mutation-shard INDEX 8 --build-dir "$CHECK_ROOT/ctrl-INDEX"
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/firmware/ctrl/test/maap_differential.py --self-test
python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 2
python3 sw/firmware/gtest/tally_selftest.py --mutants
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2
make -C tb/verilator/mbx -j1 VBUILD_JOBS=8
python3 sw/builder/test_builder.py --require-rv32
```

Run the builder/static and documentation bank from CONTRIBUTING and #664 comment
6014810929, using `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` as the diff base.
HANDOFF.md gives each command, bounded foreground partitions, test/defect mapping,
coverage table and gate table. Portable partition drivers and a complete/disjoint
case audit retain the original assertions and graders. NVM partitions likewise
retain the original named-test grader. Logs remain in scratch; the packet records
sizes and hashes.

Expected results: each final gate exits 0; 196/196 controller defects, including
96 MAAP defects, and sixteen differential controls caught; seventeen RV32 checks;
435 saved-state tests across five shapes; 109 inherited NVM mutants caught;
seventeen coverage files meet the ratchet.
F2 runs 75 baseline cases: 37 core/CSR, twelve mailbox at one interface, thirteen
at two, one debug and twelve differential. The three MAAP C files have no
exclusions. The merge imports higher ADP/NVM coverage obligations without lowering
a threshold or adding exclusions. Both ADP reentry arms run 122 cases.

Mailbox passes both bus/interface configurations, real firmware co-simulation
and five quick controls. The 93-entry builder/documentation bank exits 0. Vendor
analysis is SKIPPED without its analyzer; historical placement calibration is
NOT RUN without its report. Compiler-absent profile runs skip compiled claims,
which SDK profile runs separately measure. No skip supplies physical proof.

## Round 4

Merge `d4bc335c20ad764fdcda7ebef6a6cd64dc60af93` has ordered parents
`8b78a8fd36864246336c71c061ac4f21d629952f` and
`d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`. Conflict resolution preserves both
catalogs, normal/coverage arms, mutation partitions and the assertion allowance.
The merged 196 definitions are exactly the union of the prior 193 and dev's 100,
with unchanged seams, named tests and failure needles. No check meaning changed
or required a relaxed verdict. No rebase or amend was used.
The regular RV32 arm retains F2's release profile. Dev's assertion-enabled profile
was also checked by running the same ABI/ISA, dependency and frame checks on all
twelve controller/MMIO objects with `-DNDEBUG` removed; it passes. This preserves
both build profiles' evidence without treating release as a debug-runtime proof.

The MAAP README now selects the compiler with `MILAN_RV32_CC`. The retired
controller-only variable has no matches under `sw`, `docs` or `scripts`.
Debug `maap.c` compiles with the pinned SDK and passes RV32I/ILP32 inspection.
Its undefined assertion handler remains a target debug-link obligation; the header
only declares it. The regular object gate and linked size measurement use
`-DNDEBUG`. The final documentation-only commit corrects the inherited harness
sentence about this distinction. Executable inputs match the tested `24be55fc`
tree. Documentation checks, image/debug measurements and the full coverage check
were rerun at the final head. Receipt heads are explicit in HANDOFF.md.

The linked measurement uses actual controller, ADP/MAAP, loop, MMIO and CSR
allocation code with real RV32I memory routines and libgcc. Bare-metal GCC 15.2.0,
`-Os`, static linking and section garbage collection are used. Entity and boot
constants come from the normal generators. There are no unresolved references,
heap calls, runtime stubs or hosted components.

| Shape / image | text | rodata | data | bss | Total before stack |
|---|---:|---:|---:|---:|---:|
| Shipping AX 1x1 TDM8, dev | 8,356 | 176 | 0 | 2,156 | 10,688 |
| Shipping AX 1x1 TDM8, F2 | 14,284 | 200 | 0 | 3,296 | 17,780 |
| Largest shipped AX 8x8, dev | 8,356 | 176 | 0 | 2,156 | 10,688 |
| Largest shipped AX 8x8, F2 | 14,284 | 200 | 0 | 3,296 | 17,780 |
| Maximum accepted 15-listener / 16-AAF-talker + CRF entity, F2 | 14,284 | 200 | 0 | 3,296 | 17,780 |
| F2 delta from dev, each shape | +5,928 | +24 | 0 | +1,140 | +7,092 |
| Maximum entity with two-interface mailbox, dev | 8,748 | 176 | 0 | 2,248 | 11,172 |
| Maximum entity with two-interface mailbox, F2 | 15,004 | 200 | 0 | 4,448 | 19,652 |
| Two-interface F2 delta | +6,256 | +24 | 0 | +2,200 | +8,480 |

All five shipped shapes produce the same section sizes. Generated source counts
change the MAAP range without allocating per-stream storage. The capacity fixture
has seventeen talker sources and fills 32 MRP attributes; an invalid 33-attribute
shape is refused by the unchanged generator.
The first measurements use the shipping one-interface mailbox; the additional
two-interface variant is produced by the mailbox generator and measured above.

Static `ctrl_app`: 3,184 bytes versus dev's 2,076. Its MAAP adapter is 1,104
bytes, including a 960-byte per-interface queue. Both retain 204 bytes of pool
control, 1,748 bytes of loop state and 124 bytes of ADP state. The CSR allocation
context adds 32 bytes. ADP/MAAP never allocate from the pool; the unused minimum
valid arena is 32 bytes. Contained sizes must not be added twice. The packet
includes the complete target-size table and reproducible measurement helper.
At two interfaces, `ctrl_app` is 4,336 bytes (dev 2,168), with 216 bytes of ADP,
2,168 bytes of MAAP and two contained 960-byte queues. Other pool sizes are unchanged.

A separate 4 KiB stack reserve gives 21,876 bytes of F2 sections, below the
approximately 128 KiB planning budget. The entry and linker layout are sizing
scaffolding, not board startup or a shipping image. Later composition and routed
resource acceptance remain default-flip work.
The two-interface maximum totals 23,748 bytes with the same separate stack reserve.

## Known limitations / out of scope

H-MAAP charges 100 ns per ordered mailbox access on a monotonic host clock.
Wake cases measure 4,700 ns from RX_HEAD publication; the interface-1 stall
measures 5,004,400 ns including its 5 ms stall. Callback bound: 48 accesses;
standalone pass bounds: 616/664 at one/two interfaces. The service limit is
10 ms against the shared 50 ms ceiling. Target execution, bus arbitration,
wire departure, media quiescence, NVM overlap and bench acceptance remain
integration obligations. Static frames are not a whole-program stack proof.

The linked size excludes later F1/F3/F4/F5 composition and board runtime work.
No F2 RTL, register definition, shipping image, default all-fabric build or
submodule pin change exists against the authorized dev. The platform supplies
ordered CSR access, exclusive stream-window ownership and quiescence before
ownership transfer. Allocation-to-ACMP wiring remains a mandatory dependency.

No push, PR edit or merge to dev was performed. Publication, current-head reviews,
trusted local replication and protected hosted checks, candidate-merge validation
and post-merge containment remain pending. This is author evidence, not a review
verdict or a clean-lens ledger.

The service's cumulative memory peak was observed at 10,640,736,256 bytes;
its initial peak was not captured. This run cannot establish compliance with
the requested 9 GB bound. Reduced-concurrency current samples remained below
that bound, and the disk free-space floor was maintained.

## Definition of Done

- [x] Lane implementation acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification passes with the stated unavailable physical checks
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive at this head
- [ ] External review is positive at this head
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING
- [x] Documentation is updated where needed
- [ ] Post-merge containment is checked before the Issue moves to Done
