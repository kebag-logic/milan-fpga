[A10] Needed by kebag-logic/milan-fpga#545. The owner step policy slews a locked offset of up to 100 µs at the 200 ppm clamp. The parent's CRF servo must discard the rate windows that overlap such a slew and stay LOCKED; see the manager decision at kebag-logic/milan-fpga#387 comment 5816509317. The indication has to come from this engine: it is the only place that knows it is slewing.

## Observed (pinned `e5dcea6e`)

- `hdl/top/KL_gptp_engine.sv:101-138`: the PHC face exports only `phc_addend_we_o`, `phc_addend_o`, `phc_step_we_o` and `phc_step_o`. There is no slew-active output.
- `hdl/top/KL_gptp_engine.sv:897`: a PHC write is either a step pulse or an addend pulse.
- `hdl/ucode/gen_gptp_ucode.py:828`: the `sv_slew` branch computes the PI trim and joins `sv_rate`. It publishes no persistent slew-active state.
- `docs/INTEGRATION.md:148,272`: `pub_flags_o[3]` stays asserted while slewing, and `pub_offset_o` is the pre-correction measurement.

None of these can stand for slew state. Ordinary frequency tracking uses the same addend path.

## Required (from the parent's analysis, milan-fpga #545 [A263] handoff)

1. Export a documented one-bit, registered, `clk_i`-synchronous **level**, `phc_slew_active_o`. It means "the PHC is undergoing the step policy's transient offset correction through the rate path".
2. Timing contract:
   - it asserts when the policy chooses to slew rather than step;
   - it stays asserted for the whole affected interval, including between consumed Sync pairs;
   - it clears when the policy correction has completed, while ordinary frequency tracking continues;
   - the behaviour on reset, asCapable loss, missing Sync, a replacement step, and a return to grandmaster duty is defined.
3. Tests: slew start and end on the policy's own decision, a step that does not assert it, ordinary tracking that does not assert it, and each defined edge case. A mutant that ties the level low, or clears it early, fails.
4. `docs/INTEGRATION.md` documents the port and the contract.
5. Parent consumer: the parent's `KL_gptp_shadow` instantiates `KL_gptp_engine`. The consumer check runs with the parent #545 branch that connects the new port.

