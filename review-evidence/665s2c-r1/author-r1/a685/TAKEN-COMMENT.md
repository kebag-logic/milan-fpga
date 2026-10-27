[A685] TAKEN

Branch: `665-s2c-icache`, from S2's head `cd3525c3ddcbdb5d78bf8fccdab354c468926997` (PR #792, round 2), on `dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. The PR targets `dev-soft-core`. Not pushed; the manager pushes.

Authoritative references: the S2c assignment (issuecomment-6421463860); S2's result (issuecomment-6413711129) and PR #792; decisions D3 and D4 (issuecomment-6409738976); the branch policy (issuecomment-6409455089); the owner's all-fabric clarification (issuecomment-6410301079); #791; `docs/reference/FR_NFR.md` 3.4.1 (T_svc = 10 ms); `docs/design/SPLIT_CONTROL_MEMORY.md` (the 56-tile ledger); `docs/design/MARK_II_AREA_PLAN.md` (the tile ledger); the product's cacheless VexiiRiscv patch series (`sw/litex/patches/0004`, `0005`).

Interpreted scope:
- In `sw/litex/milan_soc.py`, only the split placement's CPU (`--ctrl-mailbox`) gains a VexiiRiscv instruction cache, through the pinned generator's own options (`--fetch-l1`, `--fetch-l1-sets`, `--fetch-l1-ways`; the line is fixed at 64 B at generator `235753e2`).
  - No data cache: an LSU L1 leaves the product's non-coherent fabric (patch 0005 covers only the no-LSU-L1 shape) and needs coherency with the DMA port. I will state the measured reason with the chosen parameters.
  - The all-fabric CPU arguments, and so its netlist and export, stay byte-identical.
  - The cache adds no region and changes no region's size or flags. Where the cache's region decode meets the non-power-of-two `rom`/`sram` decode (#791), I fix it in the split CPU's region list and state how.
- S2's harness gains a test-only cache-size override and observes the cache's refill bus, so it can measure the same groups with and without the cache.
  - At both points (1x1 with one interface, 8x8 with two): worst pass, composed maximum, every backlog row, fan-out and cycles per path, against S2's no-cache tables, at 4 KB, 8 KB and more sizes if the curve needs them.
- A labelled hybrid-XIP arm (test code only): the image's code executes from the QSPI flash window behind the cache. It reports whether the T_svc paths hold, and how much block RAM that frees.
- The cache's block RAM, LUT and FF from Yosys and from a Vivado out-of-context run, against the 56-tile ledger and the area plan.
- Firmware behaviour and tests and the mailbox contract stay unchanged.

Validation plan:
- S2's harness at both points without and with the cache, its self-test and its controls (the `as-built` control rerun with the cache);
- Yosys, and Vivado out of context under the host lock, queued behind any release build;
- `test_builder.py --require-rv32`;
- the all-fabric export digest for every shipped config, base against head, byte-identical;
- the docs gates; `cd tests && behave`; the four-shard Verilator sweep.

All rc 0, foreground, unpiped.

Blockers: none. I STOP if the cache needs a generator version change, an all-fabric change or a timing-closure change to the shipping clocks.
