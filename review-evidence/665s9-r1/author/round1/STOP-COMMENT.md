[A760] STOP

Head: `ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa` on `665-s9-split-image` (local, not pushed), on `dev-soft-core` `1d6bf555`: eight commits, added only. No HDL source, firmware, mailbox contract, ring, shape geometry or VERSION change.

**Why STOP: acceptance item 1 is not met, and closing it is outside this lane.**
- The integrated split route (shipping 1x1 through the split recipe, M0s recipe at `full-split`) misses the gate's +0.030 ns WNS floor at the slow corners in all three of #818's placement directives, from the same synthesis checkpoint:
  - `ExtraPostPlacementOpt` (the recipe's): -0.078 ns, 11 endpoints below 0;
  - `ExtraTimingOpt`: **+0.002 ns**, the best, 0.028 ns under the floor;
  - `AltSpreadLogic_high`: -0.061 ns, 8 endpoints below 0.
  - WHS meets 0 at every corner in every directive (+0.030 to +0.102 ns). The 50 MHz datapath clock has +1.359 to +1.377 ns.
- Every path under +0.030 ns is inside `KL_mbx`, at the 100 MHz bus clock `milansoc_crg_clkout0`:
  - the host's register read, from LiteX's AXI-Lite-to-Wishbone bridge state to `KL_mbx/reg_rdata_r` (13 to 21 logic levels, mostly routing). It runs through the bound-talker table's read-back (`rb_a_w`, `g_cmp[0].sr_r`, `bnd_eid_vld_w`);
  - the receive block's ring write, from `KL_mbx/u_rx/head_r` to the MAAP, AECP and SRP receive rings' block RAM ports.
- This lane may not edit `KL_mbx*` RTL, and a bus register stage on the mailbox window is a design change.
- **Decision needed**, one of:
  - (a) a mailbox timing change in a lane that owns `KL_mbx*` (register the host read data or the bound-talker read-back, and the receive ring write address), then S9 re-routes;
  - (b) a register stage on the mailbox's bus window in `milan_soc.py`, adding a cycle to every mailbox access, which the CPU service budget would re-measure;
  - (c) an owner exception to the floor at +0.002 ns.
- D7 (a) was ruled on area. The route is 8,763 LUT below the M9 bar, not within 300 LUT of it, so D7's (b) is not triggered on area; but the term's read-back is on this critical path.

**Done: items 2 to 6, and the measurements.**
- **Item 2.** The all-fabric endpoint is unchanged:
  - its exports at 1x1 and 8x8 equal the base's, 21 of 21 files each, apart from timestamps, paths and LiteX's comment-only hierarchy tree;
  - the builder's all-fabric outputs of the five shipped configs are byte-identical, 50 files, and no all-fabric manifest is written;
  - its route at this head passes the gate against `route-1x1` (exit 0): 52,272 LUT, 74 / 27 block RAM, WNS +0.245 / WHS +0.027 ns.
- **Item 3.** The ledger rows are in `docs/design/MARK_II_AREA_PLAN.md`, "M8a-2: the integrated split route", at the four points: text, rodata, data, BSS with lwSRP's pool, staging and the descriptor image counted once, stack, alignment; RAMB36/RAMB18 planned and as mapped; usable and unused bytes; the five largest BSS consumers, each with a reduction option.
  - As mapped, in tiles: 1x1, one interface, 37.5 (exactly so in the route); 1x1, two interfaces, 41.0; 8x8, one interface, 51.0; 8x8, two interfaces, 57.5 (ledgered at 59.0, owed to S14).
- **Item 4.** The whole image is 29,277 LUT, 39,060 FF, 12,767 slices and 56 / 32 block RAM (72 tiles): 8,763 LUT below 38,040 and 49.5 tiles below 121.5.
  - Reconciled owner by owner against the all-fabric route: the ledger's conditional total never credited the 26 tiles of DDR3 and processor memory-bridge buffers that D4 removes.
- **Item 5.** The bound-talker term, out of context: 285 LUT / 87 FF at one interface, within its 300 / 120 target; 682 / 159 at two.
  - In the route its storage maps as out of context (64 SRLs, 22 LUTRAMs, 87 FFs); its logic is not separable there. D7 (a)'s close-out row is in the ledger.
- **Item 6.** Gate 23p: both good images pass, and 12 planted images each fail by their kind:
  - from the SoC: ident, VERSION, mailbox minor, split datapath without `CTRL_SPLIT_P`, a split image with DDR3, an all-fabric image with the mailbox;
  - from the image's files: relinked firmware, a forged manifest, a removed manifest, an unbound bitstream, another bitstream, a renamed placement.
- **M8a-2 runs**, all passing:
  - DDR3, main RAM and the processor memory bridges are removed from the split, with no all-fabric change;
  - the split boots to ready at 1x1 and 8x8;
  - `check_nvm_capture.py` passes, and `nvm_split_target --point 8x8` passes with its controls caught;
  - `nvm_cosim`: 465 / 465;
  - `nvm_capture_cpu` 8x8 at 50 MHz, traffic on and off: 16 / 16 captures each, worst 13.86 ms, 0 mismatches.

**Gates at `ad2ed0e3`, on clean clones, all rc 0:**
- Every `run:` step of every job that a ready pull request to `dev-soft-core` triggers (docs, elaborate, rtl-fast with the firmware jobs incl. firmware-boundary and firmware-verilator, rtl): 69 job instances, 497 steps rc 0, none failed or missing. 110 steps did not run, each with its reason: APT resolution, tool builds into `/opt`, the GitHub API, the schedule-only physical gPTP job, and the 19 hosted sweep workers' suite step, which the sweep below covers.
- docs.yml on its own verifier: 88 steps rc 0, 7 not run with a reason, 0 bad.
- The full sweep as four native shards: 65 of 65 suites passed (15, 17, 17 and 16 per shard), 2,192,899 checks, 0 in-suite failures; the shard holding capture_coherence ran on 4 CPUs.
- The firmware self-test and its mutant campaigns (`test_ctrl_firmware.py --require-rv32 --self-test`, shards 0/4 to 3/4): PASS each, 570 of 570 control mutants caught; `fw_coverage.py --check`: PASS, 35 files; `ctrl_boundary.py` both halves: PASS.
- S2's harness: 1x1, one interface: 18 groups, 34 T_svc misses recorded; 8x8, two interfaces: 17 groups, 63 misses recorded. Both tallies equal the base's.
- `test_builder.py --require-rv32`; `cd tests && behave`: 508 scenarios passed; `git diff --check 1d6bf555 ad2ed0e3`; `test_ctrl_memory.py`; the split boot at 1x1 and 8x8.
- The elaborate job holding the standalone LiteX simulations passed on its fifth attempt. Two attempts saw `test_soc_timing_cuts` stopped at its 900 s wall clock on a loaded host (result unknown, not a failure). One lost its network connection. One was killed by a host reset. Run alone under the same load, the test passes at the base in 1,702 s and at this head in 1,774 s.
