# The 1x1/2if leg: a scratch harness point

Measured on a scratch tree whose firmware (`sw/firmware/ctrl/gptp/*`, `mbx/mbx.c`, `test/ctrl_aecp_image.c`), contract
(`sw/mailbox/mailbox.yaml`) and testbench (`tb/verilator/ctrl_service_budget/sim_main.cpp`, `gptp_group.py`) are
byte-identical to commit `36f6d5a8`. It adds one line to `tb/verilator/ctrl_service_budget/run.py`'s `POINTS`, which
is not committed:

    '1x1-2if': ('endstation_ax7101_1x1_tdm8', 2)

Committing that point also needs `shape_costs.BUILT`, the firmware's shape table and the flip check to carry
1x1/2if, which is out of scope this round. The leg was graded with the harness of that tree. At that tree the share
was 1 ms (the gptp family still entered it), and no pass exceeded even that: "0 of 205 work passes over the per-pass
share 1.000 ms". The cycle figures (`cost-1x1-2if-scratch.txt`) come from the PASS lines' per-module counts, which
grading does not change.

Command: `run.py --point 1x1-2if --groups gptp-slave --with-gptp --record-budget-findings --record-share-findings`.
