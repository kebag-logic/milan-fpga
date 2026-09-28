# R367-2 probe commands (portable)

The prerequisites are a disposable copy of the candidate at `471892a9bcc2d26fdcfc19db01949ecea83c5e0f`, with git metadata and the submodules at their gitlinks, and the pinned Verilator 5.050 on `PATH`. Set `$TREE` to that copy and `$PKT` to this packet.

| Receipt | Command |
|---|---|
| `receipts_gmstep_clean_d0.log` | `make -C $TREE/tb/verilator/milan_dp gmstep-build`, then `./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0` from that directory |
| `receipts/summary.tsv`, `receipts/O*.log`, `receipts/G*.log` | `python3 $PKT/probe_r367_2.py $TREE $PKT/scratch $PKT/receipts` |
| `receipts/feed/feed_sweep.tsv`, `receipts/feed/feed_NN.log` | `python3 $PKT/probe_r367_2.py $TREE $PKT/scratch $PKT/receipts/feed --feed-sweep` |
| `receipts/gmstep_mutants_default.log` | `python3 gmstep_mutants.py` in `$TREE/tb/verilator/milan_dp` |
| `receipts/tkdiag_make.log` | `make -C $TREE/tb/verilator/tkdiag` |
| `receipts/stale_scan_hits.txt` | `python3 $PKT/stale_scan_r367_2.py <clean clone>` (classified in `receipts/stale_scan_classification.md`) |
| `receipts/gate_*.log` | `python3 scripts/<gate>.py [--check]` in `$TREE` for `docs_check`, `check_doc_paths`, `check_doc_style`, `check_cpp_idiom`, `check_py_idiom` and `check_hygiene` |
| `receipts/hosted_snapshot.json` | `gh api repos/kebag-logic/milan-fpga/commits/<head>/check-runs?per_page=100` (read-only) |
| `receipts/clone_integrity.txt` | index, worktree, submodule and gitlink comparison of the review clone after all probes |

Probe mutants, planted by `probe_r367_2.py` through the suite's own `DP_SRC` and `MCR_SRC` variables:

| Name | Leg | Plant |
|---|---|---|
| O1 | option-off | the restart term plus `\| eff_ptp_adjust_w` (adjtime only) |
| O2 | option-off | the restart term plus `\| cfg_ptp_cmd_load` (settime only) |
| O3 | option-off | the restart term plus `\| media_rebase_p_w` (both causes) |
| O4 | option-off | the restart engine resets `tgt_r` and `mr_o` to all ones. This is the event-relative witness: the pre-event level is 1, and no event changes it |
| G1 | gmstep | the re-base term is restored |
| G2 | gmstep | the restart term is gated by `& ~media_rebase_p_w` (coincident suppression) |
| G3 | gmstep | selected-CRF `mr` propagation is removed |
| G4 | gmstep | the restart term plus `\| cfg_ptp_cmd_load` (settime only) |
