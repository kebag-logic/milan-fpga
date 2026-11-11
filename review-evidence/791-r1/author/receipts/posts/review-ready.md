[A765] REVIEW READY
Commit: `03447eaa087ba0687362a7372f4a00bd40c6fd46` on `791-split-region-decode` (local, not pushed): two commits on `dev-soft-core` `1d6bf555`, which has not moved. This supersedes my STOP above: the build host's root file system was restored, and every run it blocked has now run.

Changed:
- **Option (a).** `add_ctrl_memory` hands the CPU generator each control region as its aligned power-of-two pieces (`ctrl_memory.decode_pieces` / `cpu_regions`, `milan_soc.exact_cpu_decode`). `rom` and `sram` become 128 + 64 + 32 KiB at their origins, so each mask compare is exact and their union is exactly [origin, origin + 224 KiB).
- The SoC's bus regions, decoder, `csr.csv`, `regions.ld` and `CtrlMemory` are unchanged. No generator or LiteX patch is carried.
- A finalize that never reaches the CPU's naming step is refused by name, so a re-pinned LiteX cannot silently restore the single mask.
- **Why not (b).** A range compare in the generator would be a patch carried on every re-pin. It would also need the netlist cache invalidated, because the cache key is LiteX's hash of the region list, not the generator's source.
- **New test.** `tb/verilator/ctrl_region_decode/` is the CPU-simulation test; its `decode.py` reads a netlist's fetch and load decode at every 32-bit address.
- **S2 harness.** `split_soc.CpuPatches` records the SoC's whole regions before the split. `cover` now refuses a list that is not its own power-of-two cover, instead of widening it; `as-built` is the single-mask control.
- **Memory test.** `test_ctrl_memory.py` gains a CPU decode arm, a split-export check and six mutants.
- **Docs.** `SPLIT_CONTROL_MEMORY.md` has a new section, the CPU's region decode, and the S2 and S3 harness READMEs are updated.

Validation, on clean clones of this head:
- **Region-decode test.** `run.py --self-test` passes:
  - the shipping decode passes 15 of 15 checks: fetch and load at the last word of each region and at each seam between pieces; fetch and load one word past each end, which must fault (cause 1 or 5, `mtval` that address) with no bus command; and the netlist decode at every address;
  - `single-mask` fails exactly its 4 checks: `rom`'s seam load and fetch (`0x0001fffc: trap cause 5; 0x0002fffc: trap cause 5`) and both DECODE checks (`first difference 0x00008000, refused inside the regions`);
  - `cover` fails exactly the 4 past-the-end checks and both DECODE checks.
- **Split boot to ready.** 1x1 at 84.425 ms and 8x8 at 184.695 ms; trace 18 of 18; rc 0.
- **S2's harness.** 1x1/1if: `18 groups graded, 0 refusals`. 8x8/2if: `17 groups graded, 0 refusals`. Both rc 0 with `--record-budget-findings`; its self-test reports 0 failures.
- **Generated decode.** The 1x1 and 8x8 split exports share one CPU netlist; its fetch and load decode equals the SoC's regions at every 32-bit address. There is no Arty split config on this branch.
- **All-fabric.** For every shipped config, base against head:
  - the CPU netlist (name, bytes, region list, arguments) and every builder output are identical;
  - the AX7101 top Verilog, `csr.csv` and `soc.h` are identical apart from LiteX's header comments;
  - the Arty exports are refused by LiteX's PLL search at the base and at this head alike.
- **`test_ctrl_memory.py`.** PASS: 173 ok, 0 FAIL, every new mutant caught.
- **Workflow replay.** Every `run:` step of docs, elaborate, rtl-fast and rtl that a pull request to `dev-soft-core` triggers, 69 job instances: `497 steps ran, 0 failed`. 110 steps did not run, each with its reason: APT resolution, source builds of tools already pinned, hosted-only API steps, and the sweep's shard steps.
- **Full sweep, four shards.** 64 of 65 suites passed. `gptp_shadow` failed with #833's `CLEANUP FAILED: owned descendants remain`; its 325 RTL checks and 9 controls passed. Its one re-run passed. 2,192,899 checks, 0 in-suite failures.
- **`git diff --check`** against the merge base: rc 0.

Acceptance criteria: all three Required items are met:
1. The decode is exact, by option (a), with the reasons above.
2. The test and its single-mask mutant fail a named check.
3. The all-fabric CPU netlist is byte-identical.

Open risks/questions:
- The region test's SoC is the split SoC without DDR3, as the Arty's is built. The AX7101 split CPU, which also has DDR3, is covered by the netlist decode check.
- Found, not fixed (candidate issue): under the old cover decode, an instruction-cache refill past `rom`'s end that the memory's err hole answered never completed. A refill into the hole inside a region was not measured.
