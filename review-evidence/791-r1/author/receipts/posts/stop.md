[A765] STOP

Head: `03447eaa087ba0687362a7372f4a00bd40c6fd46` on `791-split-region-decode` (local, not pushed). It is two commits on `dev-soft-core` `1d6bf555`, which has not moved.

**Why STOP: the build host's root file system went read-only during the gate pass.**

- Between 08:22 and 08:26 local time the kernel remounted the root file system read-only (an emergency remount). That file system holds the CPU generator's netlist cache and its build tool's home.
- Since then no new CPU netlist can be generated. So the remaining required runs cannot build: the split boot simulation at 8x8, and S2's harness at 1x1/1if and 8x8/2if.
- Running them against a relocated copy of the generator tree was not authorized, so it was not done.
- The lane's handoff cannot be written to its output directory either.
- Needs: the host's root file system restored, then those runs and the remaining gates at this head.

**The change, option (a).**
- `add_ctrl_memory` hands the CPU generator each control region as its aligned power-of-two pieces (`ctrl_memory.decode_pieces` and `cpu_regions`, `milan_soc.exact_cpu_decode`):
  - `rom`'s 224 KiB at 0 becomes 128 KiB at 0, 64 KiB at 0x2_0000 and 32 KiB at 0x3_0000;
  - `sram` is split the same way at 0x1000_0000.
- Each piece's mask compare is exact, and together the pieces are exactly [origin, origin + 224 KiB).
- The SoC's bus regions, its decoder, `csr.csv`, `regions.ld` and `CtrlMemory` are unchanged. The all-fabric SoC never calls `add_ctrl_memory`.
- Why (a) over (b):
  - (a) is exact by construction and carries no generator patch.
  - (b) would be a generator patch carried on every re-pin.
  - (b) would also need the netlist cache invalidated, because the cache is keyed by LiteX's hash of the region list and arguments, not by the generator's source.
  - A range compare costs more logic than a mask compare.
- (a)'s one dependency, LiteX naming the netlist through the CPU's own naming step, is guarded: a finalize that never calls it is refused by name.
- S2's `CpuPatches` now records the SoC's whole regions before the split. Its default arm refuses a list that is not its own power-of-two cover, instead of widening it. `as-built` is the single-mask control.

**Evidence so far, each on a clean clone of this head unless stated:**
- **The CPU-simulation test**, `tb/verilator/ctrl_region_decode`: self-test PASS.
  - The shipping decode passes all 15 checks. These fetch and load at the last word of `rom` and `sram`, and at each seam between pieces. They also fetch and load one word past each end, which must fault before the bus: cause 5 or cause 1, with `mtval` that address. Two DECODE checks read the netlist's own fetch and load decode at every 32-bit address and require it to equal the SoC's regions.
  - The single-mask mutant fails exactly four named checks: `rom: a load at each seam of its decode pieces reads its word from memory` (`0x0001fffc: trap cause 5; 0x0002fffc: trap cause 5`), the seam fetch, and both DECODE checks (`first difference 0x00008000, refused inside the regions`).
  - `rom`'s last word, 0x3_7ffc, has bit 15 clear, so the single mask admits it. The fault is at every address with bit 15 set.
  - The power-of-two cover mutant fails the four past-the-end checks and both DECODE checks.
  - The test's single-mask CPU netlist matches line for line the CPU of #878's Arty image that did not boot, and its cover netlist is that lane's booting diagnostic's own.
- **The product split export's CPU at 1x1 and 8x8**, one netlist for both, at `eb26f22d` (this head changes only text since): its fetch and load decode admit exactly the SoC's regions at every 32-bit address. No Arty split config exists on this branch.
- **The split boot simulation at 1x1**: ready at 84.425 ms, trace 18 of 18 equal, PASS.
- **All-fabric.**
  - The AX7101 1x1 and 8x8 exports' CPU netlists are byte-identical to the base's: the same name, the same bytes and the same generator rows.
  - Their top Verilog and `soc.h` differ from the base's. The differences inspected, at 1x1, are in comments: timestamps, and the order of the module-hierarchy comment block. A comparison with comments set aside did not run, so the top is not yet shown identical.
  - The three Arty configs' exports are refused by LiteX's PLL search at base and head alike, after the CPU names its netlist. That name is the same at both sides.
- **`test_ctrl_memory.py`**, with its new CPU decode arm and six mutants, all caught, passed before the arm moved into its helper module. Its re-run at this head stalled in the SoC-build arm on the degraded host and is not counted.
- **The workflow replay so far**: docs `wire-accountability`, `docs-check-no-git`, `docs-gates-1` and `ci-fail-fast` succeeded. The rest has not run.
- **The full sweep** is running in four shard units at this head. Its verdict has not been read.

**Not done:** the split boot at 8x8; S2's harness at both points; the rest of the workflow replay, which holds the firmware, builder and behave gates; the sweep's verdict; REVIEW READY.

**Found, not fixed (a candidate issue):**
- Under the old cover decode, a speculative instruction-cache refill of the line past `rom`'s end was answered `err` by `CtrlMemory`'s hole. The refill never completed, and the CPU stopped.
- Whether a refill into the hole inside a region, past the image's banks, stalls the same way was not measured.
