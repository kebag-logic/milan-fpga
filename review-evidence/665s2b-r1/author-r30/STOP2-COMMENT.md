[A683zo] STOP

Head: `a4faefd46e6e41285077a0dbe90115ac416d0794` on `665-s2b-cycles`.
- It is one commit on the merge `187eeed8`: the size fixture's 8x8/2if entry at 58.5 RAMB36, as ruled on the first STOP (issuecomment-6831583372). Section 5 states it with that link, and says the cap is now fully used.
- `test_ctrl_memory.py` passes. The fixture links at all four points (38.5 / 41.0 / 51.5 / 58.5), and `fw_coverage.py --check` passes at this head.
- No rebase, force or amend; nothing pushed.

**Why STOP: at the merge, the firmware does not boot, because the mailbox's host port changed under this branch's record mover.**
- **The failure.** I launched the re-grade (both points, every arm) and the four cost controls. **No group booted.** Each one stops right after `nvm_store_boot`: the fixture's `main` returns, because `ctrl_loop_open` → `mbx_open` finds the mailbox's ID and CAPS reads failing `caps_match`. The CPU then sits at `_start`'s `j 5c`. I stopped the units after about 25 minutes.
- **It is the composition's, not either side's.** The split boot simulation (`tb/verilator/ctrl_split_boot/run.py`, 1x1) shows it:
  - `dev-soft-core` `0fb66211`: PASS.
  - PR #892's round 4 head `8bc1dfc0`: PASS.
  - this head: "Milan split: mailbox contract mismatch; entity disabled".
  - At round 29's head the same simulation passed.
- **The cause, in the RTL.**
  - `dev-soft-core`'s `3ba76ae7` (PR #889, #870) changed `KL_mbx`'s host port. Before, the comment read "the access completes, one cycle after host_req_i". Now it reads "1 cycle after host_req_i, 2 for a register read": `ack_r <= (host_req_i && !reg_rd_w) || rd_q_r`.
  - This branch's record mover, `hdl/milan/mailbox/KL_mbx_dma.sv`, sits on that port between `KL_mbx_wb` and `KL_mbx`, and exists only on this branch. It still routes the port's ack by the one-cycle rule: `ack_cpu_r <= cpu_issue_w` ("the host port's request last cycle was the CPU's") and `cpu_ack_o = host_ack_i && ack_cpu_r`.
  - So a CPU register read through the mover gets the wrong cycle's ack and data.
- **Why no gate saw it.** The mover's own bench (`tb/verilator/mbx` `run-dma`, `dma_main.cpp`) drives a model host port. The mailbox co-simulation has no mover. Neither tests this pairing. The pin move has no mover, and never ran the S2 harness or the split boot at the merge.
- **What it blocks.** The fix is a change to `KL_mbx_dma.sv`: track an outstanding register read until its ack, plus a bench case for a two-cycle register read and its plant. That is an RTL change, which this lane's brief forbids. It would also bring the RTL gates (the mailbox suites, CDC, Yosys, the full sweep) into the round. The re-grade, the four cost controls and the full pass cannot run until the composed tree boots.

Receipts are in the output directory's `receipts/resume-mover-ack/`: the three split boot logs, each group's log tail at this head, and the RTL and firmware excerpts.

**Asked:** a ruling on the mover's port contract at the merge. One option is that this lane makes the RTL change in `KL_mbx_dma.sv`, with its bench case, its plant and the RTL gates, and then finishes round 30's re-grade and full pass. The other is that the fix goes to another lane or to `dev-soft-core` first.
