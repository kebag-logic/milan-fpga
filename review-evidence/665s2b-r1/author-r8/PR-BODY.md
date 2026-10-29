[A683j]

## Contents

- **[Status](#status)** — STOP: the 16 KiB two-way fetch L1, the bulk memory primitives and the mailbox's record mover, with every composed row after them at 100 MHz. `665-s2b-cycles` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, the decisions needed, and the measurement's variants.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

STOP at `59038a1d7c8ec65417fc74d7fb64804d7075e3fe`: ten commits on round 7's `17d32e81`. RTL changed: the split CPU's fetch L1 and a new mailbox-path block, `KL_mbx_dma`. The mailbox contract, the tsn-c-stack pin and the lwSRP pin are unchanged.

- **The fetch L1 is 16 KiB, two-way, LRU, one refill at a time** (the owner's decision of 2026-10-29). NFR-SCOUT-01 is amended in the four documents that state it. Out of context at 100 MHz the split CPU closes (CPU WNS +0.659 ns, bus +2.660 ns). Its block RAM grows from 11.5 to 14.5 tiles, which is CPU memory outside the 224 KB firmware allocation, so no image's plan changes. The area ledger goes to 124, 2.5 over its ceiling.
- **The memory primitives** copy and fill aligned memory eight words a turn and the rest by its bits.
- **The record mover** sits on the split hart's mailbox host port and moves each record's payload between its ring and memory through the CPU's coherent DMA port, in AXI4 bursts inside one 64-byte line. It adds nothing to the mailbox contract: the same ring words in the same order, the header words, counters and doorbells the driver's, and its own CSR bank. The split image's driver uses it for every received payload and every transmitted payload on a word.
- **lwSRP's receive path** has a draft change for lwSRP's own review, two exact changes measured staged here. The TSN stack's wire-halves draft from round 7 is staged with it.
- **After, at 100 MHz:**
  - at 1x1 every row the CPU decides fits but arm A's last SRP record (10.41 ms); with both drafts staged every one fits;
  - at 8x8 the last ACMP record now fits, and the last AECP and SRP records still miss, 14.47 to 16.39 ms.
  - Instruction refills per window fell by 60 to 70 %.
- **Gates:** see "How to validate" for each one's result and head, the full sweep among them (64 / 64 suites, 0 failures). Every gate the diff touches is rc 0, except rtl-fast's firmware-boundary step. That step gives the known refusal of S2's harness files, byte-identical to rounds 5 to 7, and passes with S2's `e0e1b464`, which is in `dev-soft-core`.

## Linked Issue / roles

Relates to #665

Executor: `[A683j]`
Internal cleared-context reviewer: to be named
External reviewer: to be named

## Description

| Commit | Piece | What and why |
|---|---|---|
| `6ba67356` | `sw/litex/milan_soc.py`, `sw/builder/test_soc_options.py` | `CTRL_FETCH_L1 = (128, 2)`: 16 KiB two-way of the generator's 64-byte line. The generator's PLRU is exact LRU at two ways, and its default is one refill. The option test restates the geometry and kills five others; the all-fabric CPU keeps exactly `--xlen=32`. |
| `c7690363` | `sw/firmware/ctrl/plat/ctrl_mem.c`, `ctrl_mutants.py` | Aligned `memcpy`/`memmove` upwards and `memset`: eight words a turn, then the rest under 32 bytes by its bits (four words, two, one, a halfword, a byte), each step leaving both pointers aligned. Six planted defects. |
| `cf5ae260` | `hdl/milan/mailbox/KL_mbx_dma.sv`, `tb/verilator/mbx/` | The record mover and its bench. Each host request holds its fields through its answer, as `KL_mbx_wb`'s do. A CPU access during a move is held and made after it; an error response or a refused start sets ERR. The bench checks the mover against a driver's word loop written from the contract, with a model of `KL_mbx`'s port and a stalling, erring AXI4 memory (360,473 checks). 17 planted defects; `make` runs them. |
| `caddc237` | `milan_soc.py`, `tb/verilator/ctrl_service_budget/split_soc.py` | `CtrlMailboxDma` (glue: four CSRs, the AXI master, the instance) between `KL_mbx_wb` and `KL_mbx`, its bank pinned below the mailbox's, its master on the CPU's DMA bus. The CPU budget harness's test SoC has the same mover; its host-port observer is on `KL_mbx`'s side. |
| `39aba024` | `sw/firmware/ctrl/plat/mbx_dma.h`, `mbx/mbx.c`, `test/ctrl_build.py` | In the split image (`CTRL_MBX_DMA_BASE`, in `SPLIT_RV32_FLAGS` only) `mbx_rx_take` and `mbx_tx_send` move the payload with the mover: three register writes and a status poll. A transmit frame off a word, and every other build, keep the word loops the host suites run. |
| `b7c30969` | `syn/yosys/run.sh`, the module matrix, the test-evidence readers, comments, declarations, docstrings | The mover's own Yosys row; the matrix through its generator; the idiom gates' findings on the new files. |
| `d8188521` | `sw/firmware/gtest/coverage.ratchet` | The two changed files at their new sizes, 100 % lines and branches, through `fw_coverage.py --write`. |
| `4e037d33` | `ctrl_mutants.py` | The bulk copy's lost word planted so the copy compiles under the driver's `-Werror`. |
| `7ac3e52e` | `FR_NFR.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `SPLIT_CONTROL_MEMORY.md` (section 13), `MAILBOX_SPLIT.md`, READMEs | NFR-SCOUT-01's new text; the ledger's row; the measurement. |
| `59038a1d` | `plat/mbx_dma.h`, `milan_soc.py` | The mover's first register is CFG: the bare-metal scope gate refuses the retired host-plane name `DMA_RING`. The split images are byte-identical, and the harness reproduces the measured leg exactly. |

**Every composed row at 100 MHz** (worst instance over the four backlog groups, ms, arm A / arm B, bold over T_svc; "before" is round 7's head):

| Row | 1x1 before | 1x1 after | 1x1 after, both drafts | 8x8 before | 8x8 after | 8x8 after, both drafts |
|---|---:|---:|---:|---:|---:|---:|
| ACMP record, last | 6.62 / 6.76 | 5.09 / 5.02 | 4.41 / 4.55 | **10.69** / **10.70** | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 4.94 / 5.06 | 3.77 / 3.56 | 3.22 / 3.24 | 8.13 / 8.14 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 4.93 / 5.09 | 3.81 / 3.60 | 3.25 / 3.27 | 8.12 / 8.13 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | **13.45** / **14.37** | 9.56 / 9.93 | 8.64 / 9.00 | **19.26** / **19.73** | **14.92** / **15.89** | **14.47** / **15.22** |
| SRP record, last | **15.30** / **14.84** | **10.41** / 9.91 | 9.11 / 9.26 | **21.76** / **21.07** | **16.30** / **16.39** | **15.81** / **15.19** |
| ACMP command behind a full ring | 5.44 / 5.40 | 3.91 / 3.69 | 3.44 / 3.44 | 9.85 / 9.86 | 7.87 / 8.29 | 7.98 / 7.63 |
| ENTITY_AVAILABLE behind a full ADP ring | 3.63 / 3.86 | 2.88 / 2.72 | 2.46 / 2.48 | 5.45 / 5.34 | 4.23 / 4.32 | 4.24 / 4.38 |
| The owed row, the commands behind it, the owed window's last AECP record | miss | miss | miss | miss | miss | miss |

The fetch L1 alone, and the refills per window, are in [SPLIT_CONTROL_MEMORY section 13](../docs/design/SPLIT_CONTROL_MEMORY.md#13-the-larger-fetch-l1-and-the-record-mover). Behaviour with the timing removed is unchanged: the mover and the primitives give identical egress and register sequences at both points and arms.

## Authoritative references

- NFR-SCOUT-01 and NFR-SCOUT-03 ([`docs/reference/FR_NFR.md`](../docs/reference/FR_NFR.md#34-fabric-scale-out-and-future-ports)), as amended by the owner on 2026-10-29 (#665).
- [`docs/design/SPLIT_CONTROL_MEMORY.md`](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 7, 9, 12 and 13; [`MARK_II_AREA_PLAN.md`](../docs/design/MARK_II_AREA_PLAN.md)'s block RAM ledger; [`MAILBOX_SPLIT.md`](../docs/design/MAILBOX_SPLIT.md) "Bus adapters and the hard core".
- The mailbox contract ([`sw/mailbox/mailbox.yaml`](../sw/mailbox/mailbox.yaml)); AMBA AXI4 (IHI0022H) A3.2.1 and the INCR burst rules for the mover's DMA port.
- IEEE 802.1Q-2018 Table 10-3 note 11 and 35.2.2.7.2, for lwSRP's draft.
- [CONTRIBUTING.md](../CONTRIBUTING.md) section 1 (SystemVerilog only for new HDL) and section 3 (a self-checking Verilator harness for every functional RTL change).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2b-cycles
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The split image and the harness need the pinned RV32 SDK and the product LiteX environment, as for S2's harness ([`tb/verilator/ctrl_service_budget/README.md`](../tb/verilator/ctrl_service_budget/README.md)).

## How to validate

```sh
python3 sw/builder/test_soc_options.py
make -C tb/verilator/mbx run-dma dma-mutants
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
syn/yosys/run.sh --top KL_mbx_dma
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest
python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
python3 sw/builder/test_builder.py --require-rv32
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --groups backlog,backlog-adp,backlog-adp-refill,backlog-owed --record-budget-findings
bash scripts/run_all_suites.sh suite-logs --wait
(cd tests && behave)
```

Expected result / pass criteria, as run for this PR (the head each ran at; the code at each is the final head's, or what changed since is named):

- `test_soc_options.py`: `RESULT: PASS`, 16 killed split-CPU controls (final head).
- The mover's bench: `checks: 360473   failures: 0`; `mbx record mover mutants: 17 of 17 caught` (in the sweep and in the firmware-verilator step).
- `lint_rtl.py --check`: `LINT GATE: PASS (89 violation(s) <= ratchet 89 ...)`. `xvlog_gate.py --check`: `PASS (0 finding(s) == ratchet ...)`. Yosys: `[PASS] KL_mbx_dma cells=2302`. No RTL changed after these ran.
- The firmware self-test, all four shards `test_ctrl_firmware: PASS`: shard 1 at `4e037d33` with `mutants: 546 of 546 caught`; shards 0, 2 and 3 at `b7c30969`. Since then: the coverage ratchet, one planted defect's text, Markdown, and a register rename that leaves the split images byte-identical.
- `fw_coverage.py --check`: `firmware coverage: PASS (32 files)`, 100 % on `mbx.c` and `ctrl_mem.c` (final head). `fw_rv32_selftest.py`: `25 checks PASS`.
- `gen_mailbox.py --check --crosscheck --selftest`: `selftest: 0 arm(s) failed`. The census, with the pinned sv2v v0.0.12 and Yosys 0.66: `RESULT: PASS`.
- `test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 1 NOT RUN`, the historical Arty report as in rounds 3 to 7.
- The harness self-test: `self-test: 0 failures`. The harness at both points and arms: `4 groups graded, 0 refusals`; the T_svc misses are the measurement above.
- The full sweep, as four shard units at `b7c30969`: 64 / 64 suites, 2,551,847 checks, 0 in-suite failures, 0 timed out; the tally over the union rc 0. Since then: Markdown, the ratchet, one planted defect's text, a Makefile comment and the register rename.
- The docs workflow's gates, the bare-metal scope gate, the idiom gates and `behave` (14 features, 406 scenarios, 1,977 steps), 96 in all: rc 0 at the final head.
- rtl-fast's firmware-boundary step (`ctrl_boundary.py --require-rv32 --selftest --without verilator`) gives rc 2. It refuses S2's harness files, with the `REFUSED` line byte-identical to rounds 5 to 7. With S2's `e0e1b464` (in `dev-soft-core`) applied it passes. The firmware-verilator step passes at the final head.

## Known limitations / out of scope

- **Scope (the owner's question).** At 8x8 the last AECP and SRP records still miss T_svc at 100 MHz, 14.47 to 16.39 ms, with every lever named so far taken. No function holds 1.3 ms of those windows: the work is spread over lwSRP, ACMP's core, the memory primitives, AECP, the SRP adapter and the mailbox driver.
- **The ledger** is 124 tiles after the conditional release, 2.5 over the 121.5-tile ceiling; 125 with every bank in block RAM, 126 at the full 56-tile allocation.
- **Two drafts outside this branch:** lwSRP's (two exact changes, three tests, six planted defects; lwSRP's suite and scenarios pass) and the TSN stack's from round 7. Each needs its repository's review, then a pin move: lwSRP's gitlink with `ctrl_arms.LWSRP_REV`, the stack's with the hot list's runtime entry removed. The SRP adapter needs no change.
- **The measurement uses labelled variants:** round 6's profiling variant (which sets the CPU clock), and the drafts staged in scratch clones.
- **The CI command table** does not yet record the mailbox suite's new Verilator build form. Its checker needs the CI image's checksum-pinned shell parser and did not run here.
- The three rows no CPU lever moves (the 60 ms egress hold, `ACMP_OWED_MAX`, the command behind the owed input) are unchanged.

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
