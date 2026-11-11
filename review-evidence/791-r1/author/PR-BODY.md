[A765]

## Contents

- **[Status](#status)** — Green: every #791 item met, every gate passes; `791-split-region-decode` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — The exact region decode, why option (a), the test, and the harness change.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at head `03447eaa`: two commits on `dev-soft-core` `1d6bf555`. `791-split-region-decode` -> `dev-soft-core`.

- The split CPU's fetch and load decode is exact: [origin, origin + 224 KiB) for `rom` and for `sram`.
- The new CPU-simulation test and both of its planted decodes pass their self-test.
- The split simulation boots to ready at 1x1 (84.425 ms) and 8x8 (184.695 ms).
- The all-fabric CPU netlist is unchanged for every shipped config.
- Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers was replayed on clean clones of this head: 497 steps ran, 0 failed. 110 did not run, each with its reason: APT resolution, source builds of tools already pinned here, hosted-only API steps, and the sweep's shard steps.
- The full Verilator sweep ran as four shards: 64 of 65 suites passed. `gptp_shadow` failed once with #833's cleanup error, with its RTL checks and controls passing; its re-run passed.

## Linked Issue / roles

Closes #791
Relates to #665
Relates to #878

Executor: `[A765]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**The fault (#791).** The CPU generator checks each fetch and load against each region it is handed with one mask compare, `(address & ~(size - 1)) == origin`.
That compare is exact only for an aligned power of two.
For the 224 KiB `rom` at 0 it was `(address & 0xfffc8000) == 0`, which leaves out every address with bit 15 set, so no split image could boot (#878 saw it on the board).

**The fix: option (a).** `add_ctrl_memory` hands the generator each control region as its aligned power-of-two pieces:

| Region | Pieces |
|---|---|
| `rom`, 224 KiB at 0 | 128 KiB at 0, 64 KiB at 0x2_0000, 32 KiB at 0x3_0000 |
| `sram`, 224 KiB at 0x1000_0000 | the same pieces at 0x1000_0000 |

Each piece's compare is exact, and together the pieces are exactly the region.
Each piece keeps its region's mode and bus.
The SoC's bus regions, its decoder, `csr.csv`, `regions.ld` and `CtrlMemory` are unchanged.
The all-fabric SoC never calls `add_ctrl_memory`, and its CPU netlist is unchanged.

**Why (a) over (b), a range compare patched into the generator:**

- (a) is exact by construction and carries no generator or LiteX patch.
- (b) would be a generator patch carried on every re-pin.
- (b) would also need the netlist cache invalidated. The cache is keyed by LiteX's hash of the region list and arguments, not by the generator's source. So the split SoC's unchanged list would keep reusing the cached single-mask netlist.
- A range compare costs more logic than a mask compare.
- (a) has one dependency: LiteX names the netlist through the CPU's own naming step. It is guarded: a finalize that never calls that step is refused by name.

| File | Change |
|---|---|
| `sw/litex/ctrl_memory.py` | `decode_pieces`, `cpu_regions` |
| `sw/litex/milan_soc.py` | `exact_cpu_decode`, called by `add_ctrl_memory` |
| `tb/verilator/ctrl_region_decode/` | New: the CPU-simulation test, and `decode.py`, which reads a netlist's fetch and load decode at every 32-bit address |
| `tb/verilator/ctrl_service_budget/split_soc.py` | `CpuPatches` records the SoC's whole regions before the split. `cover` refuses a list that is not its own power-of-two cover, instead of widening it. `as-built` is the single-mask control |
| `sw/litex/ctrl_memory_decode.py`, `sw/litex/test_ctrl_memory.py` | The memory test's CPU decode arm, the split export's check and six mutants |
| `docs/design/SPLIT_CONTROL_MEMORY.md`, the S2 and S3 harness READMEs | The region decode and the harness arms |

**The test.**

- It fetches and loads at the last word of `rom` and `sram`, at each seam between pieces, and one word past each end.
- The test SoC's banks fill each region's power-of-two window. So there is memory past each end, and only the CPU's decode can refuse that access.
- A past-the-end access must fault before the bus: cause 5 for a load, cause 1 for a fetch, with `mtval` that address.
- Two DECODE checks require the netlist's fetch and load decode to equal the SoC's regions at every address.
- The single-mask mutant fails exactly four named checks:
  - `rom`'s seam load: `0x0001fffc: trap cause 5; 0x0002fffc: trap cause 5`;
  - `rom`'s seam fetch: `0x0001fffc: trap cause 1; 0x0002fffc: trap cause 1`;
  - both DECODE checks: `first difference 0x00008000, refused inside the regions`.
- `rom`'s last word, 0x3_7ffc, has bit 15 clear, so the single mask admits it.
- The power-of-two cover mutant fails the four past-the-end checks and both DECODE checks.
- The single-mask netlist is #878's as-built CPU, and the cover netlist that bring-up's booting diagnostic's CPU, each apart from its module name.

**The generated decode per split shape.** The 1x1 and 8x8 split exports elaborate one CPU netlist.
Its bus decoder has one exact compare per piece.
`decode.py` reads its fetch and load decode exact at every 32-bit address, DDR3, CLINT and PLIC included.
There is no Arty split configuration on this branch.

## Authoritative references

- #791 Required items 1 to 3.
- [Split control memory, the CPU's region decode](../docs/design/SPLIT_CONTROL_MEMORY.md#the-cpus-region-decode).
- #878's STOP: the fault on the board, and the scratch image given the regions' cover that booted.
- #833: the `gptp_shadow` lifecycle cleanup failure, re-run once and recorded.

## How to get into the same state

```sh
git fetch origin
git checkout 791-split-region-decode
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
```

Use the product LiteX tree, the pinned RV32 SDK and Verilator, as the [CPU budget harness](../tb/verilator/ctrl_service_budget/README.md#run-and-reproduce) does.

## How to validate

```sh
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode-self --self-test
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 sw/litex/test_ctrl_memory.py
```

Expected result / pass criteria:

- `ctrl_region_decode self-test: PASS`, with:
  - `SELF-TEST PASS none: fails 0 check(s), wants 0`
  - `SELF-TEST PASS single-mask: fails 4 check(s), wants 4`
  - `SELF-TEST PASS cover: fails 6 check(s), wants 6`
- Both split boots print `ctrl_split_boot: PASS (0 finding(s))`, ready at 84.425 ms (1x1) and 184.695 ms (8x8).
- Both budget runs exit 0:
  - 1x1, one interface: `18 groups graded, 0 refusals, 34 T_svc misses`;
  - 8x8, two interfaces: `17 groups graded, 0 refusals, 63 T_svc misses`.
- The S2 harness self-test prints `self-test: 0 failures`.
- `test_ctrl_memory: 0 failure(s)` and `RESULT: PASS`.

## Known limitations / out of scope

- The region test's SoC is the split SoC without DDR3, as the Arty's split image is built. The AX7101 split export also builds DDR3, and `decode.py` reads that netlist exact on its own.
- Stores are not graded: at the pinned generator the data port admits a store wherever it admits a load, whatever the region's mode. This predates the change.
- The out-of-context CPU figures in the split control memory document predate the fix, which changes only region compare terms.
- The all-fabric Arty exports on the builder's argv are refused by LiteX's PLL search, at the base as at this head, after the identical CPU netlist is named.
- Found, not fixed: under the old cover decode, an instruction-cache refill past `rom`'s end was answered `err` by `CtrlMemory`'s hole and never completed. A refill into the hole inside a region was not measured. This is a candidate issue.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
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
