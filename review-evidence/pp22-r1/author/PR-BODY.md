[A546]

Relates to #22

Move the existing cancel declarations in `KL_pp_originator.sv` and verdict/FIFO declarations in `KL_pp_rx_validator.sv` above their first uses. The four declaration lines are unchanged; ports, parameters, registers and executable statements are preserved.

Validation at `2139f3dc10161b456dfbd51d2f73a63f9164e041`:

- All 46 derived processor source files pass analysis, with zero declaration-order or ignored-module errors; the base reproduces the two expected failures.
- Complete netlist statistics for both modules and the processor top are byte-identical to base.
- All 277 patch checks and 199 exact-text mutation arms plant successfully.
- All processor gates: passed; the 33 suites report 1,021,651 checks with zero failures at each revision, with identical complete records.
- Parent consumer set of 17 at dev `28f9666f`, with the supplied 148 adoption patch followed by the 22 budget patch: passed.

The adoption patch removes the two remaining budget entries and updates the section count to zero. The parent builder reports one calibration arm not run because its reference report is absent. Vendor synthesis and implementation were excluded by the assignment, so the original issue's synthesis-warning acceptance item remains unmeasured.
