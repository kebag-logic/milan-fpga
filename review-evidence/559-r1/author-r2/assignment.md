[A10] Round 2 for PR #564 at `32076148`. Executor [A309]. Both reviews are NEGATIVE:
- [R324]: https://github.com/kebag-logic/milan-fpga/pull/564#issuecomment-5831082266
- [R325]: https://github.com/kebag-logic/milan-fpga/pull/564#issuecomment-5831008258

**Decision (the clock: R324 F2, R325 F1).**
- The bare-metal build contract governs (`BAREMETAL_FIRMWARE.md:43`). The 8x8 figure of record is measured with a 50 MHz CPU, with rising edges aligned to sys as the board PLL aligns them.
- The 8x8 config's 100 MHz line is Linux-era. Reconciling it is #565, not this PR. Leave the yaml alone and add an explicit clock override to the harness.
- Section 18 restores "hold sizing uses the writer's actual clock". It must not say that the 50 MHz assumption is retired.

**Decision (the remedy).**
- The hold stays 50 ms. The margin is stated against the guaranteed floor of 49 ms (R324 F4).
- The reviewers measured about 24.30 ms at 8x8, 50 MHz, aligned edges. That is about 2.0x the floor, and half the floor (24.5 ms) is met by less than 1%. So "enough" holds only while the copy and the clock stay as measured. That condition becomes a gate:
  - A check that runs on hosted runners, with no compiler and no simulation, recomputes each shape's capture-copy census (closed-record bytes and records) from the generated tables, and the shape's CPU clock.
  - It fails when either differs from the measured-for values that `measurements.json` records.
  - Any change that grows the copy, or that changes the clock, therefore forces a new measurement.
- STOP condition: if the 8x8 maximum at 50 MHz with aligned edges, taken over both arms, exceeds 24.5 ms, stop and report it here. The remedy then becomes a cheaper copy, and that is my call.

Scope:
1. **Measurement (R324 F1 and F5, R325 F2).**
   - Run both shapes at 50 MHz with aligned edges, 16 captures, traffic ON and OFF. Also record the 8x8 at 100 MHz as a labelled non-contract point.
   - The published maximum is the maximum over every arm.
   - The harness grades the no-traffic arm's timing, not only its counters. A planted grading change that ignores the OFF arm's timing must fail.
   - The docs state, with numbers, that the offered READ_DESCRIPTOR load does not measurably lengthen the copy.
2. **The gate above.** Give it a named failing control for each input: bytes, records and clock.
3. **Docs (R325 F3, R324 F3, R325 S1).**
   - `TESTING.md` and `tb/verilator/README.md` name the harness as an out-of-sweep, environment-dependent measurement. They give its prerequisites (the LiteX tree, the CPU netlist and the pinned RV32 SDK) and state the exception to the "every directory needs a Makefile" rule.
   - The README names every substituted model: clocks and phase, the DDR PHY model, MAC transport and flash.
   - Section 18 and UNRESOLVED 6 carry the figures, the 49 ms floor and the #565 pointer.
