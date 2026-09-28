# R367-3 probe commands (portable)

Prerequisites: a disposable copy `$TREE` of the candidate at `6b2ebd1c435136966f84ffc16d28a80c7d6b9387` (with git metadata and the submodules at their gitlinks), a second copy `$OLD` of the same tree with `tb/verilator/milan_dp/sim_main.cpp` replaced by `git show 471892a9bcc2d26fdcfc19db01949ecea83c5e0f:tb/verilator/milan_dp/sim_main.cpp` (the round-2 harness), and Verilator 5.050 first on `PATH` (identity in `receipts/tool_identity.txt`). `$PKT` is this packet. All commands ran in the foreground.

| Receipt | Command |
|---|---|
| `receipts/summary.tsv`, `receipts/O*.log`, `receipts/OH*.log`, `receipts/G*.log` | `python3 $PKT/probe_r367_3.py $TREE $OLD $PKT/scratch $PKT/receipts` |
| `receipts/feed/feed_sweep.tsv`, `receipts/feed/feed_NN.log` | `python3 $PKT/probe_r367_2.py $TREE $PKT/scratch $PKT/receipts/feed --feed-sweep` (the round-2 script, unchanged) |
| `receipts/executor_controls_subset.log` | from `$TREE/tb/verilator/milan_dp`: `python3 $PKT/run_executor_controls_r367_3.py $TREE` (the candidate's own runner and `CONTROLS`, restricted to the five option-off controls and the coincident control) |
| `receipts/gmstep_mutants_default.log` | from `$TREE/tb/verilator/milan_dp`: `python3 gmstep_mutants.py` (the default sweep) |
| `receipts/TC_clean.log`, `receipts/togglecount_harness.patch` | `sh $PKT/togglecount_r367_3.sh <third disposable copy> $PKT/scratch $PKT/receipts` |
| `receipts/tkdiag_make.log` | `make -C $TREE/tb/verilator/tkdiag` (the pinned include root is redacted to `$PINNED_VERILATOR_ROOT`) |
| `receipts/gate_*.log`, `receipts/gates_summary.txt` | in `$TREE`: `python3 scripts/<gate>.py [args]` for each gate listed in `gates_summary.txt`; `check_em_dash` and `gen_toc` ran under a Python 3.14.7 environment that has the pinned Markdown renderer (the default interpreter lacks it and refuses with rc 2); `git diff --check 6d5ebd73..6b2ebd1c` |
| `receipts/stale_scan_hits.txt` | `python3 $PKT/stale_scan_r367_2.py <review clone>` (classified in `receipts/stale_scan_classification.md`) |
| `receipts/hosted_snapshot.json` | `gh api repos/kebag-logic/milan-fpga/commits/6b2ebd1c435136966f84ffc16d28a80c7d6b9387/check-runs?per_page=100` (read-only; 2026-09-28 02:27 UTC) |
| `receipts/clone_integrity_before.txt`, `receipts/clone_integrity_after.txt` | index, worktree, per-blob SHA-1 and mode, submodule and gitlink comparison of the review clone before and after all probes |

## Probe plants

All plants go through the suite's own `DP_SRC` / `MCR_SRC` make variables; no tracked file of either tree is edited.

| Name | Leg | Harness | Plant |
|---|---|---|---|
| O0 | option-off | head | none |
| O1 | option-off | head | restart term plus `\| eff_ptp_adjust_w` (adjtime, same cycle) |
| O2 | option-off | head | restart term plus `\| cfg_ptp_cmd_load` (settime) |
| O3 | option-off | head | restart term plus `\| media_rebase_p_w` (both) |
| O4 | option-off | head | restart engine resets `tgt_r` and `mr_o` to all ones (event-relative witness) |
| O5-O8 | option-off | head | a reviewer-written 20-bit down-counter loaded by `eff_ptp_adjust_w`; the restart term plus `\| (r367_dly_r == 20'd1)`, so the adjtime requests a restart 16, 256, 4096 or 65536 cycles later |
| OH0, OH5, OH6 | option-off | round 2 (`471892a9`) | none; the 16-cycle and 256-cycle plants of O5 and O6 |
| G0 | gmstep | head | none |
| G1 | gmstep | head | restart term plus `\| media_rebase_p_w` |
| G2 | gmstep | head | restart term gated `& ~media_rebase_p_w` (coincident suppression) |
| G3 | gmstep | head | selected-CRF `mr` propagation removed |
| G4 | gmstep | head | restart term plus `\| cfg_ptp_cmd_load` |
| TC | option-off | head plus the witness patch | none; prints the number of talker-0 `mr` level changes between the adjtime and the settime baseline |
