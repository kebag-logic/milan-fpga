# [A683j] #665 lane S2b round 8: 16 KiB two-way fetch L1, firmware and mailbox-DMA round for 8x8 (HANDOFF)

**Status: STOP** (2026-10-29) with the figures. At 100 MHz the last AECP and SRP records still miss T_svc at 8x8, 14.47 to 16.39 ms, with both repository drafts staged or not. By the assignment, the next question is scope (a 1x1-only split for Mark II), and it goes to the owner. At 1x1 this branch brings every row the CPU decides within T_svc except arm A's last SRP record (10.41 ms); with both drafts staged every one fits.

- Branch `665-s2b-cycles`, local, not pushed. Head `59038a1d7c8ec65417fc74d7fb64804d7075e3fe`: ten commits on round 7's `17d32e81cbf75976a6b1e7bbcdf9864a9d1cd097`, whose commits stay.
  - Lane base `origin/dev-soft-core` `e76a755a`, checked as an ancestor. The PR targets `dev-soft-core` (now `1a635a4c`, with S2 merged as `6660a1a0`).
- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked). No git command changed a submodule of the lane (each was checked to be its own top level with its own origin before use). Both drafts live in scratch clones (`donor/`, round 7's TSN stack draft reused).
- Assignment: issuecomment-6492443864 (`ASSIGNMENT-A10-6492443864.md`). TAKEN: issuecomment-6492614894 (`TAKEN-COMMENT.md`). STOP: issuecomment-6495801236 (`STOP-COMMENT.md`).
- CPU and memory:
  - every heavy job ran as its own transient unit, MemoryMax 4 to 16 GB: on this session's 16-31, then on 32-47 and 0-15 while `cpu_ranges.py` showed them free;
  - the full sweep as four shard units (`native-shards.py`, MemoryMax 10 GB each) on 0-15, started at 39 GB MemAvailable; MemAvailable stayed above 30 GB.
- Vivado, under `$VIVADO_LOCK`, exclusive, one at a time, each started above 37 GB MemAvailable, all before the sweep started: the split CPU's route at 100 MHz (2 minutes), the xvlog gate, the mover's route.

## Contents

1. Outcome against the assignment
2. Changes (file:line, reason)
3. New checks, planted defects and failing words
4. Method
5. Measurement before and after
6. Gates
7. Findings, conflicts, decisions needed
8. Run history

## 1. Outcome against the assignment

| Item | Outcome |
|---|---|
| 1. The fetch L1 becomes 16 KiB two-way, 64-byte lines, LRU, one refill at a time; data cache and RV32IM kept; all-fabric cacheless RV32I | `6ba67356`: `CTRL_FETCH_L1 = (128, 2)`. The generator's PLRU is exact LRU at two ways, and its default is one refill slot. The option test kills five other geometries; the all-fabric CPU keeps exactly `--xlen=32` |
| NFR-SCOUT-01 amended in `FR_NFR.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `SPLIT_CONTROL_MEMORY.md`; `docs/history` untouched | `7ac3e52e`, the owner's text in each; SPLIT_CONTROL_MEMORY section 9's sentence moved to the past tense, section 13 states the new one |
| The BRAM cost against the 224 KB budget | Section 5: the CPU's own memory, outside the firmware allocation: +3 RAMB36 (11.5 to 14.5 tiles). No image's plan changes (35.0 / 38.5 / 48.5 / 55.0 of 56 / 56 / 56 / 57.5). The ledger is 124: 2.5 over 121.5 (section 7) |
| 2a. `ctrl_mem` copy and fill word-wise and bulk | `c7690363`: eight words a turn and the rest by its bits; already word-wise before. Six planted defects; coverage 100 % |
| 2b. DMA for `mbx_rx_take` and `mbx_tx_send` | `cf5ae260`, `caddc237`, `39aba024`: `KL_mbx_dma`, the record mover, on the split hart's mailbox host port, mastering the CPU's coherent DMA port. The mailbox contract is unchanged (no `gen_mailbox.py` change; its `--check --crosscheck --selftest` and the census pass). Own bench, 17 planted defects |
| 2c. lwSRP's receive path: a donor change and the parent adapter change, not pushed | `donor/lwsrp-reclaim-and-parse.patch`: two exact changes, three tests, six plants; lwSRP's suite and scenarios pass. The parent's side is the pin in two places (`receipts/variants/`). No adapter source change is needed (section 7) |
| 3. The TSN stack's wire-halves draft measured staged | Round 7's draft (`6532c3b0`), staged by gitlink with the hot list's runtime entry removed |
| Re-measure every composed row at 100 MHz, both points, both arms, before and after | Section 5: before (round 7, with and without the stack draft), the fetch L1 alone, after, after with both drafts; 20 legs, 0 refusals |
| The I$ refills per window | Section 5 |
| The split CPU's out-of-context route at 100 MHz: timing and area | Section 5: closes, CPU WNS +0.659 / WHS +0.031 ns, bus +2.660 / +0.072 ns, no routing errors |
| Gates: round 7's, the full sweep (4 shard units), the census, `gen_mailbox.py --check --crosscheck --selftest` | Section 6 |
| STOP with the figures; if the 8x8 AECP or SRP row misses, the scope question goes to the owner | Both miss; section 7 |

## 2. Changes

`6ba67356` Give the split CPU a 16 KiB two-way fetch L1:

| file:line | Change | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:2894-2899` | `CTRL_FETCH_L1 = (128, 2)`: 128 sets of two ways of the generator's 64-byte line; its comment states the generator's PLRU (LRU at two ways) and its one refill slot | Owner decision 2026-10-29, item 1 |
| `sw/builder/test_soc_options.py:23-27` | `SPLIT_FETCH_L1` restated as `--fetch-l1 --fetch-l1-sets=128 --fetch-l1-ways=2` | The test restates the geometry on purpose |
| `test_soc_options.py:265-269`, `:286` | Five geometry controls; the summary line names the cache | Section 3 |

`c7690363` Copy and fill aligned memory eight words a turn and the rest by its bits:

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/plat/ctrl_mem.c:7-20` | The header states the bulk turns and why: most calls on the record paths fill or copy a few tens of aligned bytes | Item 2a |
| `ctrl_mem.c:65-73` | `load_half`, `store_half`, at an even address only | The halfword step |
| `ctrl_mem.c:89-136` | `forward`'s aligned path: eight words a turn, then the rest under 32 bytes by its bits (four words, two, one, a halfword, a byte), each step leaving both pointers aligned; it returns there | Was four-word turns, a word loop and a byte loop |
| `ctrl_mem.c:233-277` | `memset`: eight words a turn, then the same bit steps | Same |
| `sw/firmware/ctrl/test/ctrl_mutants.py:436-449` | Six planted defects | Section 3 |

`cf5ae260` Add the split placement's record mover:

| file:line | Change | Reason |
|---|---|---|
| `hdl/milan/mailbox/KL_mbx_dma.sv` (new) | `KL_mbx_dma`, between `KL_mbx_wb` and `KL_mbx`. It masters the CPU's coherent DMA port: AXI4, 32-bit, INCR bursts of at most 16 beats inside one 64-byte line. Receive: a chunk's ring reads into a 16-word buffer, then one write burst whose last beat's strobes stop at the length. Transmit: a read burst, each beat written to the ring with the lanes past the length zero. Each host request holds its fields through its answer, as `KL_mbx_wb`'s do. While a move runs it owns the port: a CPU access is held and made after it, and a CPU access's answer cycle keeps the CPU's fields. A start off a word or while busy, and an error response, set ERR until the next accepted start | Item 2b. The harness reads a request's fields at its answer, so holding them leaves S2's observer and grader unchanged |
| `tb/verilator/mbx/dma_main.cpp` (new) | The mover's bench, checks D1 to D9 | Section 3 |
| `tb/verilator/mbx/dma_mutants.py` (new) | 17 planted defects, built with the Makefile's own recipe | Section 3 |
| `tb/verilator/mbx/Makefile` | `run-dma`, `dma-mutants` (in `make`), `print-dma-vflags`, `clean`; the header lines in `7ac3e52e` | The suite runs it |

`caddc237` Put the record mover on the split placement's mailbox host port and the CPU's DMA bus:

| file:line | Change | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:2635` | `KL_mbx_dma.sv` in `_CTRL_MAILBOX_SOURCES` | The split placement compiles it |
| `milan_soc.py:2646-2653` | `CTRL_MBX_DMA_REGISTERS`: RING, MEM, CMD, STATUS and their fields | The register map in one place; `plat/mbx_dma.h` restates it |
| `milan_soc.py:2656-2708` | `CtrlMailboxDma`: the four CSRs, the AXI master, the instance. START comes the cycle after CMD's write, when CSRStorage holds the new word | Glue only; the logic is SystemVerilog (CONTRIBUTING 1) |
| `milan_soc.py:2711-2720` | `add_ctrl_mailbox_dma`: its own CSR bank at a given location, its master on `soc.dma_bus`; refused without a DMA bus | |
| `milan_soc.py:2739-2763` | `CtrlMailbox` takes the mover: `KL_mbx_wb`'s host port to its CPU side, `KL_mbx`'s to its mailbox side | |
| `milan_soc.py:2802` | `add_ctrl_mailbox` pins the mover's bank at `n_locs - 3`, below the mailbox's | A new CSR bank must not move an old one |
| `tb/verilator/ctrl_service_budget/split_soc.py:19-24`, `:77-81`, `:102`, `:169-201`, `:237-245` | The harness's test SoC. It reads the fixture's mover address from `ctrl_build.SPLIT_RV32_FLAGS`, refused unless it is the bank `n_locs - 3`. `StimulusMailbox` goes through the mover, and the host-port pads are on `KL_mbx`'s side | The harness measures the product's mailbox path, and its observer sees the mover's accesses with the CPU's |

`39aba024` Move each mailbox record's payload with the record mover in the split image:

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/plat/mbx_dma.h` (new) | The registers and `mbx_dma_move()`: RING, MEM, CMD writes, then STATUS polled until BUSY clears; true unless ERR | |
| `sw/firmware/ctrl/mbx/mbx.c:32-34` | `mbx_dma.h` under `CTRL_MBX_DMA_BASE` | |
| `mbx.c:310-330` | `mbx_rx_take`: the mover copies the payload; a move that ends in ERR resynchronises the ring, as an untrusted record does | |
| `mbx.c:353-374` | `tx_payload()`: the word loops, unchanged, out of `mbx_tx_send` | |
| `mbx.c:393-406` | `mbx_tx_send`: the mover for a frame on a word, ERR leaving the record uncommitted (`MBX_STATUS_BAD`, TX_HEAD and SEQ unchanged). A frame off a word, and every other build, keep the loops | The host suites' branches are unchanged |
| `sw/firmware/ctrl/test/ctrl_build.py:78-83` | `SPLIT_MBX_DMA_BASE` (bank `n_locs - 3` of the 64 KiB CSR window, `0xF000E800`) and `-DCTRL_MBX_DMA_BASE` in `SPLIT_RV32_FLAGS` only | The split image only |

`b7c30969` Give the record mover its own Yosys row and module-matrix entry, explain its planted-defect driver, and keep it within the idiom gates:

| file:line | Change | Reason (the gate's words) |
|---|---|---|
| `syn/yosys/run.sh:309-310` | The mover's own row | Each mailbox adapter has one |
| `docs/traceability/MODULE_MATRIX.md`, `hdl/milan/mailbox/README-tests.md` | Through `docs/traceability/gen_module_matrix.py`, the generator | `STALE (run gen_module_matrix.py)` |
| `scripts/measure_test_evidence_readers.py:70-73` | `dma_mutants.py`'s disposition | `UNEXPLAINED` |
| `tb/verilator/mbx/dma_mutants.py` | No host timeout on the bench's run | `4 wall-clock-dependent suite file(s) > ratchet 3` |
| `hdl/milan/mailbox/KL_mbx_dma.sv` | No byte unit in the AWSIZE, ARSIZE and WSTRB comments | `NAMING RATCHET: FAIL (3 new, 0 stripped)` |
| `tb/verilator/mbx/dma_main.cpp` | One declarator a declaration | `multi-declarator declaration 4 > ratchet 0` |
| `sw/litex/milan_soc.py:2668`, `:2670` | Docstrings | `undocumented public function 1 > ratchet 0` |

`d8188521` Record the mailbox driver's and the memory primitives' coverage at their new sizes:

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/gtest/coverage.ratchet:21`, `:23` | `mbx.c` 265/265 lines, 110/110 branches; `ctrl_mem.c` 167/167 and 80/80 | Written by `fw_coverage.py --write`, its generator |

`4e037d33` Plant the bulk copy's lost word as one stored over its neighbour:

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/test/ctrl_mutants.py:437` | `mem-copy-bulk-drops-a-word` stores the eighth word over the seventh | Dropping the store left `w7` unused, so the planted copy did not compile under the driver's `-Werror` and was counted escaped (`mutants: 545 of 546 caught` at `b7c30969`) |

`7ac3e52e` Record the fetch L1 in NFR-SCOUT-01 and the ledger, the mover and the primitives in their pages, and the rows:

| file:line | Change | Reason |
|---|---|---|
| `docs/reference/FR_NFR.md:322`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:62` | NFR-SCOUT-01, the owner's text | Item 1 |
| `docs/design/MARK_II_AREA_PLAN.md:383`, `:872`, `:895-898`, `:908-909`, `:941` | The core row's text, the ledger row (+3, 124), its paragraph, the ceiling lines | Item 1's BRAM cost |
| `docs/design/SPLIT_CONTROL_MEMORY.md:26` | Contents entry through `scripts/gen_toc.py --write`, then described | Generated navigation through its generator |
| `SPLIT_CONTROL_MEMORY.md:380-382` | Section 9's requirement sentence in the past tense, pointing at section 13 | It records round 4's amendment |
| `SPLIT_CONTROL_MEMORY.md:763-921` | Section 13: the fetch L1, its route, the primitives, the mover, lwSRP's draft, the rows, the refills, what holds the 8x8 rows, what is left | Durable record |
| `docs/design/MAILBOX_SPLIT.md:252-262`, `:1137-1140` | The mover on the host port; the switch-on build's sources and banks | The contract page |
| `sw/firmware/ctrl/README.md:49`, `:661-671` | `mbx_dma.h`; the split flags' `CTRL_MBX_DMA_BASE`; the bulk steps | |
| `tb/verilator/ctrl_service_budget/README.md:98`, `:101-102`, `:802`, `:965` | The DMA port's one master, the mover in the test SoC, the pointer to section 13 | |
| `tb/verilator/mbx/README.md:4`, `:25-34`; `Makefile:19-22` | The fifth target | |

`59038a1d` Name the record mover's first register CFG, keeping a retired host-plane name out of the tree:

| file:line | Change | Reason (the gate's words) |
|---|---|---|
| `sw/firmware/ctrl/plat/mbx_dma.h:12`, `:35`, `:39`, `:59` | RING to CFG: `MBX_DMA_REG_CFG`, `MBX_DMA_CFG_MASK_LSB` | `check_baremetal_only.py --check` at `7ac3e52e`: `[H] retired target host-plane surface 'DMA_RING': '#define MBX_DMA_RING_MASK_LSB 16u' (#259: no dormant target driver/memory-ring contract)` |
| `sw/litex/milan_soc.py:2647`, `:2653`, `:2674`, `:2688` | The CSR `cfg`, `CTRL_MBX_DMA_REGISTERS` | So the generated CSR names carry no `dma_ring` either |

The split image at `59038a1d` is byte-identical to the measured legs' at both points, and the harness's `backlog` group at 1x1 arm A reproduces `M100-A1` exactly (`receipts/measure/final-head-check.md`).

## 3. New checks, planted defects and failing words

| Check | Planted defect | Failing words |
|---|---|---|
| `test_soc_options.py` `_split_cache` (split CPU exactly `... --fetch-l1-sets=128 --fetch-l1-ways=2 ...`) | `CTRL_FETCH_L1` `(256, 2)`, `(128, 3)`, `(128, 1)`, `(64, 2)`, `(64, 1)` | `killed: a larger cache`, `a third way`, `one way`, `a smaller cache`, `the 4 KiB direct-mapped cache it replaces` |
| `CtrlMem.W1MemcpyEveryAlignmentAndLength` | `mem-copy-bulk-drops-a-word` (the eighth word stored over the seventh), `mem-copy-rest-halfword-dropped`, `mem-copy-rest-byte-dropped` | `W1 memcpy byte` |
| `CtrlMem.W3MemsetEveryAlignmentLengthAndValue` | `mem-set-bulk-drops-a-word`, `mem-set-rest-steps-overlap`, `mem-set-rest-halfword-dropped` | `W3 memset byte` |
| `dma_main.cpp` D1 | `tail-strobe-full`; `ring-index-unwrapped` | `D1 no byte outside [addr, addr + len) is written`; `D1 memory holds the record's bytes in ring order` |
| D2 | `tx-lanes-unmasked` | `D2 the ring holds the record's words, the lanes past len zero` |
| D3 | `burst-crosses-line`; `wlast-early` | `D3 a burst stays inside one 64-byte line`; `D3 WLAST marks a burst's last beat only` |
| D4 | `cpu-request-dropped`; `ack-misrouted` | `D4 a CPU access is answered`; `D4 a CPU access held for a transfer completes after it` |
| D5 | `misaligned-accepted`; `busy-start-accepted` | `D5 a start off a word sets ERR`; `D5 a start while a transfer runs sets ERR` |
| D6 | `bresp-ignored`; `rresp-error-written`; `err-not-cleared` | `D6 a write error response sets ERR`; `D6 no ring word is written from an errored beat or after it`; `D6 the next accepted start clears ERR` |
| D7 | `zero-length-runs` | `D7 a length of 0 runs no transfer` |
| D8 | `reset-keeps-state` | `D8 a reset leaves the mover idle` |
| D9 | `hold-address-moves`; `hold-data-moves`; `single-beat-bursts` | `D9 a request's address holds through its answer`; `D9 a write's data holds through its answer`; `D9 a line's sixteen ring reads end within 32 cycles` |

The bench is checked against a driver's word loop written from the contract, never against the RTL: a model of `KL_mbx`'s host port (one request a cycle, the answer the cycle after, a partial write strobe refused), an AXI4 memory with seeded random stalls on every channel and a one-line error range, and an AXI monitor (A3.2.1 stability, INCR, four-byte beats, WLAST, one burst in flight, the line rule). 360,473 checks: every word of a line, every length to 96 bytes and the largest frame, across the ring's wrap, at 0 % and 30 % stalls.

The bench caught two defects of the first draft before it was committed:
- a CPU access answered in the cycle a move starts showed the mover's address (fixed: the CPU's answer cycle keeps its fields);
- back-to-back ring requests left the harness's observer reading the next request's address at an answer (fixed: each request is held through its answer, at half the port's rate).

The lwSRP draft's tests and plants are in `donor/README.md`. Every defect in the table was caught in its driver at the head (section 6): the memory ones in the firmware self-test's shard 1, the mover's in the mailbox suite's `dma-mutants`, the option test's in `test_soc_options.py`.

## 4. Method

- **The harness:** S2's, the four backlog groups, at 1x1/1if and 8x8/2if, arms A and B (`--variant answering-ports`), `--record-budget-findings`, from clean clones, with round 6's profiling variant (`receipts/variants/harness-profile-cumulative.patch`, which also carries `CSB_CPU_HZ`), `CSB_CPU_HZ=100000000`; the bus stays 100 MHz.
- **The legs** (`receipts/measure/`, labels in each `label.txt`):
  - before: round 7's `N100` (its head `ee45d131`) and `W100` (with the TSN stack draft), from round 7's receipts;
  - `I100`: `6ba67356`, the fetch L1 alone on round 7's firmware;
  - `M100`: `39aba024`, this branch's firmware, mover and fetch L1. Its firmware, RTL and harness are the head's: since then only gate plumbing (a Yosys row, a test-evidence disposition, comments, declarations, docstrings), the coverage ratchet, one planted defect's text and Markdown changed;
  - `D100`: `M100` with both drafts staged (`receipts/variants/parent-with-donors-gitlinks.patch`, `parent-with-lwsrp-donor-pin.patch`, `parent-with-donor-hot-list.patch`).
- **The analysis** (`scripts/`): `table6.py` (rows; refills per window), `prof.py` (window breakdown), `holders7.py` (module families), `logcmp.py` (behaviour with the timing removed), `memcalls.py` (the primitives' call shapes in a round 7 trace).
- **Out of context:** the CPU and its memory with round 5's `ooc_soc.py`/`ooc_route.sh` recipe at 10/10 ns; the mover with `dma_ooc.sh` (the mailbox's recipe).

## 5. Measurement before and after

Every composed row, worst instance over the four groups, ms, arm A / arm B, bold over T_svc (`receipts/rows/rows-1x1.md`, `rows-8x8.md`; SPLIT_CONTROL_MEMORY section 13):

| 1x1/1if: row | before | with the stack's change | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 6.62 / 6.76 | 6.06 / 6.37 | 5.66 / 5.43 | 5.09 / 5.02 | 4.41 / 4.55 |
| ADP record, last | 4.94 / 5.06 | 4.27 / 4.50 | 4.02 / 3.88 | 3.77 / 3.56 | 3.22 / 3.24 |
| MAAP record, last | 4.93 / 5.09 | 4.31 / 4.54 | 4.06 / 3.92 | 3.81 / 3.60 | 3.25 / 3.27 |
| AECP record, last | **13.45** / **14.37** | **12.95** / **13.44** | **10.52** / **10.42** | 9.56 / 9.93 | 8.64 / 9.00 |
| SRP record, last | **15.30** / **14.84** | **14.28** / **13.91** | **11.03** / **10.71** | **10.41** / 9.91 | 9.11 / 9.26 |
| ACMP command behind a full ring | 5.44 / 5.40 | 4.89 / 4.86 | 4.19 / 4.14 | 3.91 / 3.69 | 3.44 / 3.44 |
| ENTITY_AVAILABLE behind a full ADP ring | 3.63 / 3.86 | 3.18 / 3.42 | 3.04 / 2.97 | 2.88 / 2.72 | 2.46 / 2.48 |
| The owed row, the commands behind it, the owed window's last AECP record | miss | miss | miss | miss | miss |

| 8x8/2if: row | before | with the stack's change | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | **10.69** / **10.70** | **10.51** / **10.59** | 9.10 / 9.10 | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 8.13 / 8.14 | 8.01 / 8.06 | 6.91 / 6.91 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 8.12 / 8.13 | 8.00 / 8.04 | 6.89 / 6.89 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | **19.26** / **19.73** | **19.11** / **20.39** | **15.88** / **16.16** | **14.92** / **15.89** | **14.47** / **15.22** |
| SRP record, last | **21.76** / **21.07** | **21.30** / **20.86** | **16.89** / **16.64** | **16.30** / **16.39** | **15.81** / **15.19** |
| ACMP command behind a full ring | 9.85 / 9.86 | 9.66 / 9.73 | 8.42 / 8.42 | 7.87 / 8.29 | 7.98 / 7.63 |
| ENTITY_AVAILABLE behind a full ADP ring | 5.45 / 5.34 | 5.24 / 5.43 | 4.52 / 4.42 | 4.23 / 4.32 | 4.24 / 4.38 |
| The owed row, the commands behind it, the owed window's last AECP record | miss | miss | miss | miss | miss |

The first records, an event behind 15 others and the refilling bucket fit everywhere.

**I$ refills per window** (`receipts/rows/irefills-*.md`): the line refills of the work passes overlapping each group's composed window, and their wait, ms, arm A / arm B:

| Window | before | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|
| 1x1 `backlog` | 5,551 (4.90) / 5,539 (4.90) | 1,514 (1.34) / 1,497 (1.33) | 1,493 (1.32) / 1,488 (1.32) | 1,539 (1.36) / 1,529 (1.36) |
| 1x1 `backlog-adp` | 10,053 (8.92) / 9,766 (8.63) | 4,100 (3.63) / 3,877 (3.43) | 4,203 (3.71) / 4,176 (3.69) | 3,734 (3.30) / 3,697 (3.28) |
| 1x1 `backlog-adp-refill` | 11,698 (10.38) / 10,463 (9.25) | 4,216 (3.73) / 3,865 (3.42) | 4,488 (3.97) / 4,121 (3.64) | 3,995 (3.53) / 3,714 (3.29) |
| 1x1 `backlog-owed` | 11,629 (10.32) / 11,627 (10.28) | 3,856 (3.42) / 3,791 (3.36) | 4,049 (3.57) / 4,052 (3.58) | 3,642 (3.21) / 3,616 (3.22) |
| 8x8 `backlog` | 9,029 (8.04) / 9,087 (8.08) | 3,620 (3.27) / 3,569 (3.22) | 3,922 (3.48) / 3,936 (3.49) | 3,972 (3.55) / 4,021 (3.59) |
| 8x8 `backlog-adp` | 10,686 (9.53) / 10,380 (9.26) | 4,124 (3.73) / 4,000 (3.62) | 4,464 (4.01) / 4,376 (3.89) | 4,409 (3.96) / 4,473 (4.00) |
| 8x8 `backlog-adp-refill` | 11,626 (10.35) / 10,906 (9.71) | 4,314 (3.90) / 4,018 (3.63) | 4,642 (4.18) / 4,383 (3.90) | 4,522 (4.06) / 4,409 (3.94) |
| 8x8 `backlog-owed` | 12,331 (11.01) / 12,592 (11.25) | 3,847 (3.49) / 3,770 (3.42) | 4,170 (3.75) / 4,195 (3.73) | 4,002 (3.61) / 4,244 (3.79) |

**What each change took** (`receipts/profile/`):
- the fetch L1: 60 to 70 % of the refills of every window, 3.4 to 7.0 ms of wait; the rows fell 3.0 to 5.0 ms;
- the mover: `mbx_tx_send` 0.98 to 1.03 ms of an 8x8 window to 0.40 to 0.45, `mbx_rx_take` 0.85 to 0.93 to 0.65 to 0.71; the driver's instructions halved;
- the primitives: `memset` 15 % fewer instructions at 8x8, `forward` 6 % fewer; their time is mostly the data cache's refills;
- lwSRP's draft: `mrp_reclaim` 0.68 to 0.75 ms of an 8x8 SRP window to 0.18; lwSRP's share 3.6 to 3.7 ms to 3.2 to 3.4.

**The route** (`receipts/area/cpu16k2-ooc-10ns/`; Vivado 2026.1, `AreaOptimized_high`, `xc7a100t-fgg484-2`, the split CPU and its firmware memory from the 1x1 image, cpu_clk and litex_clk at 10 ns, asynchronous):

| Split CPU | CPU WNS / WHS, ns | Bus WNS / WHS, ns | LUT | FF | DSP | The CPU's RAMB36 / RAMB18 (tiles) | Design tiles |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4 KiB direct-mapped fetch L1 (round 5's 100 MHz route) | +0.952 / +0.041 | +2.440 / +0.070 | 3,902 | 6,828 | 4 | 6 / 11 (11.5) | 54.5 |
| 16 KiB two-way fetch L1 | +0.659 / +0.031 | +2.660 / +0.072 | 3,948 | 6,879 | 4 | 9 / 11 (14.5) | 58.0 |

No routing errors (10,668 nets fully routed). The CPU netlist alone: 3,785 LUTs, 6,443 FFs. Its worst path is the generator's memory bridge into its read pipe, 8.93 ns, 84 % route (was the branch redirect at 9.0 ns). The netlist is `VexiiRiscvLitex_a2b3af48835516899a4f0ca5650d3edf` with the product's region list (`netlist.json`). The image's rom and sram took 43.5 tiles here and 43.0 in round 5's route: round 7's image, not this round's change.

**The mover out of context** (`receipts/area/dma-ooc/`, 10 ns): 395 LUTs, 700 FFs, 64 F7 muxes, no block RAM, WNS +4.086 / WHS +0.216 ns. Yosys 0.66 maps it to 2,302 generic cells.

**The images** (`receipts/images/images.md`, round 7's head against this one): rom +40 to +56 bytes, sram unchanged; planned tiles 35.0 / 38.5 / 48.5 / 55.0 at both, within 56 / 56 / 56 / 57.5.

**Behaviour** (`receipts/behaviour/`, 16 group logs a pair, both points and arms):
- `I100` against `M100` (the mover and the primitives): identical in every part;
- round 7 against `I100`: only MAAP's clock-seeded addresses at 1x1, as round 7 found;
- `M100` against `D100` (both drafts): identical but for four transmit records' cross-channel `SEQ` in 8x8 arm A's `backlog-owed`, which follows the sends' timing; every egress frame is identical;
- round 7's stack leg against `D100`: MAAP's addresses, and at 8x8 the periodic ADP advertisement round 7 also saw in a run that ends at another time.

## 6. Gates

Every gate ran on a clean clone (`scripts/clone.sh`), its log in `receipts/gates/` with host paths replaced (`receipts/gates/stale/` keeps the superseded runs). "Since" says what changed after a gate's head.

| Gate | Command | Where | Result | Receipt |
|---|---|---|---|---|
| Firmware self-test, shards 0, 2, 3 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard k/4 --jobs 4` | `b7c30969` (since: the coverage ratchet, shard 1's planted defect's text, Markdown, the RING-to-CFG rename; the split images are byte-identical) | rc 0, `test_ctrl_firmware: PASS` each; shard 0 `[ok] arm hot`, `named plants not caught: none`; no `ESCAPED` | `selftest-shard0.log`, `selftest-shard2.log`, `selftest-shard3.log` |
| Firmware self-test, shard 1 (the control campaign, the six new memory plants) | same, `--shard 1/4` | `4e037d33` | rc 0, `mutants: 546 of 546 caught`, `test_ctrl_firmware: PASS` | `selftest-shard1.log` |
| same | same | `b7c30969` | rc 1, `mutants: 545 of 546 caught`: `mem-copy-bulk-drops-a-word` did not compile under `-Werror` (`w7` unused). Fixed in `4e037d33` | `stale/selftest-shard1-b7c3.log` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check` | final head | rc 0, `firmware coverage: PASS (32 files)`; `mbx.c` 265/265 lines and 110/110 branches, `ctrl_mem.c` 167/167 and 80/80 | `final-fw_coverage_check.log`, `fw_coverage_write.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | `b7c30969` | rc 0, `RV32 build self-test: 25 checks PASS` | `fw_rv32_selftest.log` |
| Mailbox generator | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck --selftest` | `b7c30969` (no mailbox change since) | rc 0, `selftest: 0 arm(s) failed` | `gen_mailbox.log` |
| rtl-fast `publication-census` | `python3 sw/mailbox/publication_census.py --check --selftest --jobs 4`, the pinned sv2v v0.0.12 and Yosys 0.66 named by `SV2V`/`YOSYS` | `b7c30969` (no RTL change since) | rc 0, `RESULT: PASS`; `mutations: 0 of 31 rule(s) no arm proves`. A first run found sv2v v0.0.13 on the unit's PATH and refused, as it must | `publication_census.log`, `stale/publication_census-unpinned-sv2v.log` |
| The mailbox suite (the mover's bench and plants with it) | `make -C tb/verilator/mbx` | in the sweep (shard 3, `b7c30969`) and in the boundary's Verilator step at the final head | rc 0: Wishbone 402, cosim 32, two interfaces 404 / 449 / model 389, `mbx mutants: 6 of 6 caught`, the mover's 360,473 checks, `mbx record mover mutants: 17 of 17 caught` | sweep shard 3 `mbx.log` (`receipts/sweep/`) |
| RTL lint ratchet | `python3 scripts/lint_rtl.py --check` | `4e037d33` (no RTL change since) | rc 0, `LINT GATE: PASS (89 violation(s) <= ratchet 89 ...)` | `lint_rtl_head.log` |
| Vivado front-end | `python3 scripts/xvlog_gate.py --check`, under the lock | `b7c30969` | rc 0, `xvlog gate: PASS (0 finding(s) == ratchet; 0 hdl/, 0 pinned processors)` | `xvlog_check.log` |
| Yosys, the mover's row | `syn/yosys/run.sh --top KL_mbx_dma --top KL_mbx_wb` | `b7c30969` | rc 0, `[PASS] KL_mbx_dma cells=2302`, `[PASS] KL_mbx_wb cells=5`; the tied-input and tap-purity checks PASS | `yosys-KL_mbx_dma-KL_mbx_wb.log` |
| CPU option test | `python3 sw/builder/test_soc_options.py` | final head (the docs runner) and `4e037d33` | rc 0, 16 killed split-CPU controls, `RESULT: PASS` | `docs/soc_options.log`, `soc_options_head.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `d8188521` (since: a planted defect's text, Markdown, the rename) | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: the historical Arty report, as in rounds 3 to 7 (1,955 s) | `builder_require_rv32.log` |
| rtl-fast `firmware-boundary` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | final head | **rc 2**: it refuses S2's harness files; the `REFUSED` line is byte-identical to rounds 5 to 7 (md5 `079f75e5...`) | `final-ctrl_boundary_without_verilator.log` |
| same | same | `7ac3e52e` + S2's `e0e1b464` (in `dev-soft-core`) | rc 0, `ctrl_boundary: PASS` | `ctrl_boundary_with_S2_e0e1b464.log` |
| rtl-fast `firmware-verilator` | `... --only verilator` | final head | rc 0, `ctrl_boundary: PASS` (the mailbox suite among its builders: exit 0) | `final-ctrl_boundary_only_verilator.log` |
| The split link script's test | `python3 sw/litex/test_ctrl_memory.py` | `b7c30969` | rc 0 | `test_ctrl_memory.log` |
| Linked images at four points | `scripts/images.py` (`ctrl_srp_image.py --with-aecp --layout split`), round 7's head against `d8188521` | `d8188521` (and byte-identical at the final head, two points) | rc 0; planned tiles unchanged, 0 over a cap | `images-four-points.log`, `receipts/images/` |
| Docs workflow, bare-metal scope, idiom gates, `ci_events`, harness self-test, CPU option test, `behave` (96 gates) | `scripts/docs_gates.sh` (`gates_s2b3.py`) | final head | `hdl_reference` refused at first only because its scratch output survived the earlier pass (`output directory is not empty`); rerun on a clean scratch rc 0. All 96 rc 0, tree clean: `docs_check: 0 finding(s)`, `check_em_dash: 0 finding(s) over 1813 added line(s)`, `TOC gate: OK`, `baremetal-only: OK (0 findings across 1441 ...)`, the harness `self-test: 0 failures`, C++ and Python idioms within their ratchets, `behave` 14 features, 406 scenarios, 1,977 steps passed | `docs/`, `stale/docs-final-hdl_reference-scratch-collision.log` |
| same | same | `7ac3e52e` | 1 of 96 nonzero: `baremetal_check` (`retired target host-plane surface 'DMA_RING'`). Fixed in `59038a1d` | `stale/docs-7ac3/` |
| Naming, test evidence, C++/Python idioms, module matrix (in the docs runner too) | `measure_naming.py --check`, `measure_test_evidence.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `gen_module_matrix.py --check` | before `b7c30969` | the findings in section 2's `b7c30969` row; fixed there | |
| S2's harness | `run.py --point 1x1/8x8 --groups <the four backlog groups> --record-budget-findings`, both arms | `I100`, `M100`, `D100`: 12 legs | rc 0 each, `4 groups graded, 0 refusals`; the misses are the measurement | `receipts/measure/` |
| same, at the final head | `--groups backlog`, 1x1 arm A | final head | rc 0; identical to `M100-A1` | `receipts/measure/final-head-check.md` |
| The full sweep, 4 shard units | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4` with the pinned Verilator 5.050, sv2v v0.0.12 and tsn-gen `deca300c`, MemoryMax 10 GB each | `b7c30969` (since: Markdown, the coverage ratchet, a planted defect's text, a Makefile comment, the RING-to-CFG rename in glue and firmware macros) | rc 0 at every shard: 64 / 64 suites (15 + 17 + 16 + 16), **2,551,847 checks, 0 in-suite failures, 0 timed out**; `python3 scripts/suite_tally.py <union> --quiet --expect-suite-root tb/verilator` rc 0 | `receipts/sweep/` |
| lwSRP's draft | its suite (`cmake`, `ctest`, `unit_tests`), `behave`, `scripts/lwsrp_plants.py` | the draft | 26,690 passes, rc 0; 3 scenarios; 6 of 6 plants caught | `receipts/donor/` |

Not run here: the CI command table's checker (`scripts/ci_tool_inventory.py --check`), which needs the CI image's checksum-pinned shell parser (section 7).

## 7. Findings, conflicts, decisions needed

- **Decision (owner): scope.** At 100 MHz, on the 16 KiB two-way fetch L1, with every lever named so far taken (the drafts staged), the 8x8 last AECP and SRP records still miss T_svc: 14.47 to 15.81 ms (arm A / B worst 14.47 / 15.22 and 15.81 / 15.19). The assignment sends the next question, a 1x1-only split for Mark II, to the owner. At 1x1 every row the CPU decides fits with the drafts; without them, arm A's last SRP record misses by 0.41 ms.
- **What holds the 8x8 rows** (`receipts/profile/holders-D.md`): each window over T_svc runs 266,000 to 311,000 instructions, waits 3.0 to 4.0 ms on instruction refills and has a data-cache refill outstanding for 2.5 to 3.7 ms. By family: lwSRP 2.4 to 3.5 ms, ACMP's core 2.3 to 2.6, the memory primitives 2.0 to 2.5, AECP 1.1 to 2.0, the SRP adapter 1.4 to 2.0, the mailbox driver 1.3 to 1.7. No function holds 1.3 ms.
- **Decision (owner or manager): the ledger.** The 16 KiB two-way cache adds 3 tiles: 124 after the conditional release (2.5 over 121.5), 125 with every bank in block RAM, 126 at the full 56-tile allocation. "If these trades still exceed 121.5, the manager must commission further redesign" (MARK_II_AREA_PLAN).
- **Decision: the two drafts.** lwSRP's (`donor/`) and the TSN stack's (round 7's) each need their repository's review, then a pin move: lwSRP's gitlink with `ctrl_arms.LWSRP_REV` (the image builder refuses any other), the stack's with the hot list's runtime entry removed.
- **Finding: no adapter change for lwSRP's draft.** The SRP adapter's reclaim flag still saves the call, and `mrp_reclaim`'s contract is unchanged. Dropping the flag would simplify the adapter, not speed it, and remove its own tests and planted defect. So the parent's part is the pin alone, and the assignment's "parent adapter change" is that.
- **Finding: the model was optimistic.** Round 6's fetch-cache model predicted the 16 KiB two-way refill counts well. Measured, the rows came out 0.8 to 1.6 ms above its figures (1x1 AECP 10.52 against 8.96; 8x8 SRP 16.89 against 16.09): the rest of each window did not stay as the model held it.
- **Finding: the profiling variant's write-back column.** With the mover running, the variant's data-cache write-back occupancy reads the whole window (`receipts/profile/`). It is an observer artefact: the windows got shorter. That column is not used here.
- **Risk: the CI command table.** `ci/image/command-table.json` records each literal CI command form. It does not yet record the mailbox suite's new `--Mdir obj_dma` Verilator form. Its checker (`scripts/ci_tool_inventory.py --check`) refuses this host (`REFUSED: CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`), so neither the check nor a regeneration ran here. The hosted image workflow will say whether the entry is needed.
- **The firmware-boundary step's refusal** is S2's pre-existing one (this lane's base lacks `e0e1b464`, which `dev-soft-core` has); its `REFUSED` line is byte-identical to rounds 5 to 7 (md5 `079f75e5…`), and with that commit applied the step's result is in section 6.
- **Lane conflicts:** S1 (PR #795) edits the harness's `KL_mbx` instance and moves the mailbox contract to 2.3. This lane puts the mover in front of that instance (`split_soc.StimulusMailbox`, `milan_soc.CtrlMailbox`). Whichever merges second rebases.
- Round 7's open items stand: the three rows no CPU lever moves (the 60 ms egress hold, `ACMP_OWED_MAX`, with tsn-c-stack #26), and the overlap with S1 and S2c.

## 8. Run history

- 2026-10-29 10:02 CET start; 10:1x TAKEN (issuecomment-6492614894).
- 10:16-10:18 the 16 KiB two-way CPU's route at 100 MHz under the lock.
- 10:1x-10:3x the fetch-L1-only legs (two lost a netlist-generation race between parallel builds and were rerun); `ctrl_mem`; the mover, its bench and plants.
- 10:4x-10:5x the mover in the SoCs and the firmware; the interim legs; the lwSRP draft, cgreen 1.6.5 built in scratch, its tests and plants.
- 11:0x the gate fixes; xvlog under the lock; the mover's route under the lock; the drafts' legs (the first two refused: the image builder reads lwSRP's pin from `ctrl_arms.LWSRP_REV` too).
- 11:1x the firmware self-test's shards; the full sweep as four shard units on 0-15 at `b7c30969`.
- 11:3x shard 1's escaped plant (`-Werror`), fixed in `4e037d33`; coverage ratchet; images; census (first with the wrong sv2v on PATH, rerun with the pinned one).
- 11:4x docs (`7ac3e52e`); the docs runner, the builder and the boundary steps at the head.
- 12:09 the docs runner at `7ac3e52e`: the bare-metal scope gate refused `DMA_RING`; renamed in `59038a1d`; the images and one harness group at that head checked against the legs; the docs runner, both boundary steps and coverage rerun there.
- 12:45 the sweep's last shard; the tally over the union rc 0.
- 12:5x STOP posted: issuecomment-6495801236.
