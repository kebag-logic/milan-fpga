# Reviewer probes, round 2 (portable)

All probes need `verilator` (5.050) on PATH. `<tree>` is an extraction of the
exact head (`git archive 762fbd6 | tar -x -C <tree>`); nothing is written
outside the work directory given.

1. `python3 -I extra_mutants_r2.py <tree> <work> 8`
   Round-1 mutants X1-X15 unchanged, plus Y1-Y7 for the round-2 delta. Each is
   built against the repository parser harness and against the independent
   random-chain probe `fu_walk_diff.cpp`; every harness FAIL line is printed.
   Receipt: `receipts/extra_mutants_r2.log`.
2. `sh build_diff.sh <tree>/hdl <obj>` then `<obj>/Vdiff 300000`
   Random-chain reference probe at head. Receipt: `receipts/diff_head.log`.
3. Build `fu_latch_demo.cpp` against `KL_gptp_rx_parser` exactly as
   `build_diff.sh` builds its probe (`-o Vdemo`), then run it. The two
   round-1 demonstrator frames A and B. Receipt: `receipts/latch_demo_head.log`.
4. Head harness on base RTL: build `tb/verilator/parser/sim_main.cpp` against
   the parser RTL of `3e3a4e7` with the suite's own Verilator flags.
   Receipt: `receipts/head_harness_on_base_rtl.log`.
