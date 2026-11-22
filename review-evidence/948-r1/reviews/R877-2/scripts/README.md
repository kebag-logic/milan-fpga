# Reviewer probes, round R877-2 (#948 / PR #959)

All probes run on disposable copies of the head tree, never on the review clone.
Verilator: the scoped 5.050 wrapper (`verilator --version` prints `Verilator 5.050 2026-07-01 rev v5.050`).

- `plant_tap_bubbles.py <tree>`: puts tap-side bubbles inside every frame. In `sim_depkt.cpp`, 0-3 stall
  cycles before 60% of beats, each either tvalid low or tvalid high with `s_tready_i` low; the enqueue pulse
  is scheduled from the cycle the eighth beat is accepted. In `sim_fanout.cpp`, 0-3 cycles of tvalid low
  before 60% of beats, through the real parser and monitor (the wrap ties the tap's tready high).
  Then `make -C <tree>/tb/verilator/avtp_rxmon VERILATOR=<5.050> fanout` and `... depkt`.
- `widen_ddrop_pend.py <tree>`: widens the monitor's per-input DEPKT drop accumulator from 3 to 6 bits
  (applied on top of the bubble plant), to test the cause of `[FO10]`'s lost drop counts.
- Attribution at round 1: in a bubble-planted copy, restore `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv` and
  `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` from `4ceba3d4` (`git show 4ceba3d4:<path> > <path>`), then
  run `make fanout`. Only the `[FO10]` lines are graded. Round 2's tests fail there by design.
- `verify_clone.sh <clone> <head> <tree>`: head, tree, index == HEAD tree (mode, blob, path), worktree ==
  index, untracked count, and the submodule gitlinks.
