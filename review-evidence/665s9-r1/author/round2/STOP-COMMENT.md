[A760d] STOP

Head: `72f596b8f375407a4b8ac6d15868b7f975c18850` on `665-s9-split-image` (local, not pushed): four commits added on `ad2ed0e3`, nothing else changed. The mailbox contract, the register map, the mailbox minor, VERSION, the firmware and the shape geometry are unchanged.

**Why STOP: the ruling's item 5. The floor still misses after both cuts.**
- The integrated split route was re-run with the cuts from one new synthesis checkpoint, through all three of #818's directives:
  - `ExtraTimingOpt`: slow WNS **+0.021 ns**, the best, 0.009 under the +0.030 floor. WHS is +0.036 at the fast corners, which meets the floor;
  - `ExtraPostPlacementOpt` (the recipe's): +0.000 ns. Fast-corner WHS is +0.019, a 50 MHz datapath path in the TDM render's FIFO;
  - `AltSpreadLogic_high`: -0.003 ns, 4 endpoints below 0 and 16 under the floor.
- Both cuts did what they were for: no path from LiteX's bus bridge reaches `KL_mbx/reg_rdata_r`, and none from `u_rx/head_r` reaches a ring.
- The paths left under the floor are all inside `KL_mbx`, at the 100 MHz bus clock:
  - `ExtraTimingOpt`: `u_rx/ch_r` to the reset pins of the new ring write registers (`wr_addr_o` and `wr_data_o`), +0.021, 17 levels. This is the free-space and drain decision zeroing them. Also `u_rx/ch_r` to `u_rx/field_r`'s reset, +0.025, 21 levels, the frame clean-up after the verdict;
  - `AltSpreadLogic_high`: `u_rx/ch_r` to RX_DROP's enable, -0.003, 22 levels, the verdict. All 16 endpoints under the floor are that counter's enables;
  - `ExtraPostPlacementOpt`: `rd_off_r` to `reg_rdata_r`, +0.000, 19 levels, 74 % routing. The generated if-chain is built as a priority multiplexer.
- **The next cut** (no contract change):
  - (a) register the ring write port's address and data without the write decision; only the enable needs it. No cost;
  - (b) register the receive block's verdict a cycle before it acts. One mailbox clock per received frame;
  - (c) generate the register read multiplexer as an AND-OR of its one-hot window selects, which the disjoint address map allows. No added cycle.
  - (a) and (b) close the `KL_mbx_rx` paths and (c) the read multiplexer. The three are one round.

**Done: items 1 to 4 apart from the floor.**
- **Item 1.**
  - The register read is decoded from an offset registered at its request, through its own copy of the window decodes. The bound-talker read-back is read at an address registered then.
  - The cut was needed there because round 1's worst register read path that missed the read-back was itself +0.022 ns.
  - Added cycles per access, mailbox clock: register read +1 (two after the request); ring read 0; write 0. S2's harness measures host-port latency of 1 to 2 clocks, where the fixture recorded 1 to 1.
  - GM_LO's snapshot is taken in the same cycle as its word.
  - S2's harness against round 1's tallies:
    - 1x1/1if: 36 T_svc misses (36/141 probes, 15/81 paths), against 34 (13/81). The two new ones are `acmp.entity_available.if0` at 10.434 ms and `acmp.get_tx_state.if0` at 11.185 ms, against T_svc 10 ms;
    - round 1's head, run again for its per-probe values, gives exactly its 34. There the two were 8.723 and 9.454 ms. Each is still served in one pass, but that pass now makes 10 more mailbox accesses and about 86,000 more CPU cycles (+1.7 ms). That is work moving into the pass as the loop's timing shifts, not the 10 ns per read. 64 of the 81 paths move by under 0.05 ms;
    - 8x8/2if: 63 (63/182, 31/129), the same as round 1.
- **Item 2.** The ring write port and the published head are registered, so a head is published a cycle after the commit, once its last header word is in the ring.
  - The suite counts, every clock of every check, a ring word written while that cycle's head covers it (H0).
  - The mutant that publishes the head one cycle early fails H0 alone, with 150 such words. No check through the host port sees it.
- **Item 3.**
  - The contract outputs are unchanged (`gen_mailbox.py --check`, 0 findings).
  - The all-fabric exports equal the base's, 21 of 21 files at 1x1 and 8x8. The all-fabric image reads no mailbox source.
- **Item 4, apart from the floor.**
  - The `KL_mbx` suite passes through both adapters at one and two interfaces, with its co-simulation.
  - Its mutant table catches 225 of 225, 18 of them new: each cut undone or misplaced, and a twin arm for each read-side decode.
  - The split boots to ready at 1x1 and 8x8.
  - The new tests also pass on the base RTL, so they grade the contract, not this implementation.
  - Two existing tests changed with the read-side decode:
    - a face window's refusals are graded in its second request. Its first answer was 3 cycles inside the 64-cycle wait bound through AXI4-Lite, and the extra register-read clock overran it at two interfaces. Every label and expected value stays, except one status tag;
    - seven existing arms have unique fixtures or the check that now sees them. Each read-side reach they lost has a twin arm.
- **The route's figures.**
  - 29,302 LUT, 39,229 FF, 72 block RAM tiles: 8,738 LUT under the M9 bar, so D7's (b) is not triggered.
  - The bound-talker term, out of context, is 474 LUT / 89 FF at one interface and 707 / 154 at two. Round 1 measured 285 / 87 and 682 / 159.
  - The cuts add the read side's bound decode and six flip-flops; the rest is the recipe's spread. D7 (a) closes it as measured, now 174 LUT over its target.

**Gates at `72f596b8`, on clean clones, all rc 0:**
- **The workflows.**
  - Every `run:` step of every job a ready pull request to `dev-soft-core` triggers (docs, elaborate, rtl-fast with the firmware jobs incl. firmware-boundary and firmware-verilator, rtl): 69 job instances, 497 steps rc 0, none failed or missing.
  - 110 steps did not run, each with its reason: APT resolution, tool builds into `/opt`, the GitHub API, the schedule-only physical gPTP job, and the hosted sweep workers' suite step, which the sweep below covers.
  - docs.yml on its own verifier: 88 steps rc 0, 7 not run with a reason, 0 bad.
- **The full sweep as four native shards:** 65 of 65 suites, 2,192,919 checks, 0 in-suite failures. The shard holding capture_coherence ran on 4 CPUs. No preflight failure.
- **Firmware:**
  - `test_ctrl_firmware.py --require-rv32 --self-test` and its mutant campaigns, in four shards: PASS each, 570 of 570 control mutants caught;
  - `fw_coverage.py --check`: PASS, 35 files;
  - `ctrl_boundary.py`, both halves: PASS.
- **Lane gates:**
  - `test_builder.py --require-rv32`;
  - `cd tests && behave`: 508 scenarios passed;
  - `git diff --check 1d6bf555 72f596b8`;
  - the `KL_mbx` suite and its 225 mutants.
- **Gates whose inputs the later commits leave unchanged:**
  - S2's harness at 1x1/1if and 8x8/2if, and the split boots at 1x1 and 8x8, ran at `3ba76ae7`;
  - the out-of-context term and the all-fabric compare ran at `1e1fd9ef`.
- **One retry.** The elaborate job holding the standalone LiteX simulations stopped `test_soc_timing_cuts` at its 900 s wall clock beside the sweep (result unknown, not a failure). It passed 8 of 8 on its second attempt, and its aggregator and manifest re-ran after it.
