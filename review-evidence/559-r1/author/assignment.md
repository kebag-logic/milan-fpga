[A10] Ready. Executor [A307]; reviewers [R324] internal and [R325] external. The branch is `559-capture-copy` from dev `a3d795ae`.

**Decision (acceptance 1): measurement route.**
- Measure with a cycle-accurate simulation of the product SoC: the board's cacheless RV32I VexiiRiscv variant and bus, as the board build configures them, running the product firmware built for the 8x8 shape.
  - `sw/litex/milan_sim.py` uses NaxRiscv today, so it is not the product CPU as it stands.
  - Read the elapsed cycles from the firmware, bracketing the copy under the hold. Include the record walk (`nvm_rec_after`) in the figure, not only the bytes.
- If the simulation cannot carry the product CPU in this lane, STOP and report what blocks it on this issue. The silicon route is then my call.

**Decision (acceptance 2): order of remedies.**
- The bar is a worst-case capture copy at 8x8 of at most half the hold (25 ms at 50 ms). Measure the worst case over repeated captures, with controller traffic running against the PP during the copy.
  1. If the bar is met, the result is "50 ms is enough", with the measured figure and margin.
  2. If it is not met, make the copy cheaper in the firmware and measure again. Keep the builder gate's census green, and state any change to the census lists.
  3. A resized hold comes last. It needs its own argument for the longest delay a held request then sees.

Scope:
1. The measurement harness or configuration, committed and runnable, with its command recorded. Also give the 1x1 figure from the same harness.
2. The remedy chosen under the order above.
3. `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and UNRESOLVED 6 carry the measured figures and replace the model. Say which model factor the measurement retires.

