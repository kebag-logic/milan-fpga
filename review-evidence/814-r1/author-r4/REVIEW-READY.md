[A703d] REVIEW READY
Commit: 4ee2aa9654196a00876dedade4b2e987c9c06e64 (branch 814-soc-timing-cut; two commits on top of 8b28ebaf, no rebase; not pushed)

Changed:
- `sw/litex/milan_soc.py:2430-2469`, `RegisteredRefresher`. LiteDRAM's ZQCS timer now leaves reset one cycle after the rest (`ResetInserter` on `refresher.zqcs_timer`, released by a `started` flip-flop). The registered request delays every refresh sequence's end by one cycle, and the timer's pulse now keeps its phase against it. On an idle controller every DFI command, precharge-all, REFRESH and ZQCS, is LiteDRAM's own exactly one cycle later. Before, the board's tREFI 782 and ZQCS period 10^8 (gcd 2) meant an idle controller never issued ZQCS. The docstring says what holds idle and under traffic. This is ruling item 1, option (a); R755 F-2 and R756 F-1.
- `sw/litex/test_soc_timing_cuts.py`, now 23 checks:
  - Z4: a 6-cycle ZQCS period, gcd 2 with tREFI. The staged DFI commands equal LiteDRAM's one cycle later through two ZQCS, the second after the timer re-phases.
  - Z5: the planted stage without the delay fails Z4.
  - F6: the flash stage's outputs stalled at random, the PHY's command READY also behind LiteSPI's own `LiteSPICSControl` at the shipping cs_delay.
  - D5 and D6: LiteDRAM's aw and ar READY random under back-to-back writes, then reads beside writes. In F6 and D6, each registered READY must hold beats, the transfers must be the issued ones in order, and VALID and payload must hold until taken.
  - F7 and D7: planted lossy registered-READY stages on SPI tx, SPI rx, and aw and ar must fail.
  - S-1: F2's planted path starts at the bridge's own registers.
  - Two harness fixes. The model PHY's memory holds only the image; it was 4 Mi words, about 4.5 GB and 100 s a flash simulation. Each build clears migen's tracer registry, which kept every SoC alive.
- `docs/testing/TESTING.md:736-756`: the new arms, and that the DRAM arms grade transfers, not read data.

Validation (all rc 0, run at the head unless a commit is named):
1. `cd sw/litex && PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py`: 23 checks, `RESULT: PASS`. 585 s CPU, 88 MB peak.
2. R756-1's `mutate_timing_cuts.py`, all ten mutants: 10 KILLED, including `axi_lossy_ready`, `spi_tx_lossy_ready` and `spi_rx_lossy_ready`, which survived at 8b28ebaf. My drop-held mutants for R755's F-1 (aw and ar, SPI tx, SPI rx) and the done-pulse-delayed ZQCS alternative: 4 KILLED.
3. route-1x1 at the three directives, run in parallel, at 0d4a899f. 0d4a899f..head changes only the test and TESTING.md.
   - #818's gate at PR #820's 50e5d08d gives rc 0, `RESULT: PASS`, and selects ExtraTimingOpt at +0.406 ns: Slow +0.406 / +0.099, Fast +1.583 / +0.036.
   - ExtraPostPlacementOpt is at +0.322 / +0.031 and AltSpreadLogic_high at +0.126 / +0.035, so every directive meets the floor at every corner. No STOP.
   - Resources against the record: LUT -119, FF +320, slices +31; RAMB and DSP unchanged. The fall is 0.034 ns, with no WARNING.
   - F1 +1.723 to +2.721 ns and F2 +1.392 to +1.607 ns at the three directives, each more than 1 ns from the worst path. F3 is not among the 5,000 worst.
   - The gate's controls: shipping alone rc 0; without a set rc 2; a comparison directory alone rc 2. #818's self-tests: 312 arms and 500 fuzz cases PASS, and 236 of 236 mutants fail.
4. `scripts/run_litex_sims.sh --selftest`: 10 of 10. The aggregate: 8 of 8, none timed out.
5. rtl-fast, replayed at the head against live dev 56df0894: `success; failed jobs: none`, all 12 jobs and 56 steps.
6. The docs workflow gates: 44 steps, 0 failed (`gate_42` not run, by AGENTS.md section 5), including `gate_39`, the Python idiom ratchet. Builder leg 1 on the LiteX interpreter, the 5 markdown gates on CPython 3.12.3, and the no-git step's two gates: all rc 0.
7. `python3 sw/builder/test_builder.py`: `ALL GATES PASS EXCEPT 2 NOT RUN`, the same two as dev's bank on this host.
8. The full sweep, which TESTING.md changing makes necessary: 4 shard units, 64 of 64 PASS (14, 17, 17, 16). Each preflight cancellation self-test passed.

Acceptance criteria:
- Met under the round-3 ruling and the round-4 ruling. The re-routed set meets the build floor at every corner on its best directive under #818. F1 to F3 are each more than 1 ns from the worst path. The cuts keep their bus contracts, now graded under backpressure as well.
- The ZQCS decision is LiteDRAM's own, one cycle later.
- The record is not re-recorded (issuecomment-6525285974).

Open risks/questions:
- The test's runtime is about 585 s CPU against the aggregate's 900 s member limit (about 405 s before). Most of it is the refresh DFI simulations.
- The DRAM harness's model PHY setup does not land write data: the DFI write burst leaves masked, with and without the stage. So the DRAM arms grade transfers and responses, not read data. This predates this round.
- The flash stage has not been on hardware. The real PHY cannot be elaborated in migen simulation, so the arm uses LiteSPI's own `LiteSPICSControl` for its chip-select hold.
- The selected directive is now ExtraTimingOpt. Its worst path is a milan-domain reset net into LiteEth MAC status registers, outside F1 to F4.
- The CPU booking had only three free 16-CPU ranges. The sweep's four shards took 12 CPUs each (16-27, 96-107, 108-119, 28-31 plus 120-127), with no core shared.
