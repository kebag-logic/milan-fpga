[A683j] TAKEN

Branch: `665-s2b-cycles` (local, not pushed), on round 7's head `17d32e81cbf75976a6b1e7bbcdf9864a9d1cd097`, whose commits stay. The lane base is `origin/dev-soft-core` `e76a755a`: checked as an ancestor, not dev. The PR targets `dev-soft-core`.

Authoritative references:
- the round-8 assignment and the owner's decision of 2026-10-29 10:01, issuecomment-6492443864;
- round 7's STOP, issuecomment-6491998804;
- NFR-SCOUT-01 (`docs/reference/FR_NFR.md`), the owner's 224 KB firmware memory limit (F5, #640), `docs/design/SPLIT_CONTROL_MEMORY.md` sections 7, 9 and 12, `docs/design/MARK_II_AREA_PLAN.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`;
- the mailbox contract (`sw/mailbox/mailbox.yaml`, `hdl/milan/mailbox/`), S2's harness (`tb/verilator/ctrl_service_budget/`) with round 6's labelled profiling variant;
- `sw/firmware/ctrl/mem/`, `sw/firmware/ctrl/mbx/`, `sw/firmware/ctrl/srp/`, and the pinned `third_party/lwSRP` and `third_party/tsn-c-stack`.

Interpreted scope:
1. **Fetch L1: 16 KiB, two-way, 64-byte lines, LRU, one refill at a time.** `milan_soc.CTRL_FETCH_L1` becomes 128 sets of 2 ways (the pinned generator's PLRU, which is exact LRU at two ways; its default of one refill slot). The 8 KiB coherent data cache and RV32M stay. The all-fabric CPU keeps exactly `--xlen=32`. `test_soc_options.py`'s controls follow, with planted defects for the old geometry. NFR-SCOUT-01 is amended with the owner's text in the four named documents, and `docs/history` is not touched. The block RAM cost goes into the area ledger and against the 224 KB limit.
2. (a) **`ctrl_mem`'s copy and fill:** word-wise, and in bulk where alignment allows. The byte semantics, overlap rules and return values stay exact, with new host tests and planted defects.
   (b) **Mailbox DMA:** a new SystemVerilog block on the split placement's mailbox path, `KL_mbx_dma`, between `KL_mbx_wb` and `KL_mbx`'s host port.
   - It moves a record's payload between a ring and the firmware's memory through the CPU's coherent DMA port, in AXI4 bursts.
   - Its control registers are its own uncached window beside the mailbox's, so the mailbox contract does not change and `gen_mailbox.py` regenerates nothing.
   - The hart's own mailbox accesses wait while it holds the port.
   - It has a self-checking Verilator bench, lint and the xvlog gate.
   - `mbx_rx_take` and `mbx_tx_send` use it in the split build, keeping each record's header words, counters, doorbells, lane order and zero padding as they are now. Any other build keeps the word loop.
   - The harness's test SoC gets the same block, so its host-port observers see every access.

   (c) **lwSRP's receive path:** a donor patch for kebag-logic/lwSRP and the parent adapter change, measured staged and pushed nowhere.
3. **The tsn-c-stack wire-halves donor** from round 7 is staged in scratch clones for the measurement, as round 7 did. The branch keeps the pin.
4. **Re-measure** every composed row at 100 MHz, both points (1x1/1if, 8x8/2if), both arms, the four backlog groups, before (round 7's legs) and after, with and without the stack donor, with the I$ refills per window. Then the split CPU's out-of-context route at 100 MHz with the new cache: timing and area, under the host lock, one route at a time.

Validation plan:
- the firmware self-test (`--require-rv32 --self-test`, four shards) with every firmware mutant driver;
- `fw_coverage.py --check` and `fw_rv32_selftest.py --require-rv32`;
- S2's harness at both points and its self-test;
- `test_builder.py --require-rv32` and `test_soc_options.py`;
- `gen_mailbox.py --check --crosscheck --selftest` and the publication census;
- the new block's bench, `lint_rtl.py --check` and `xvlog_gate.py --check`;
- rtl-fast's `firmware-boundary` and `firmware-verilator`;
- the linked images at four points;
- the docs, idiom and bare-metal gates, and `cd tests && behave`;
- the full sweep as four shard units, because RTL changes;
- the out-of-context route.

Blockers: none.

STOP with the figures. If the 8x8 AECP or SRP row still misses, the scope question (a 1x1-only split for Mark II) goes to the owner.
