# Reviewer probes, R300-1 (#545 / PR #563)

All paths are relative to an exact-head extraction `TREE` of
`fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` with its pinned submodules
(`git archive` of the superproject and each submodule), and `VERILATOR`
is Verilator 5.050.

1. Servo suite and the author's slew mutants, unmodified recipe:
   `make -C TREE/tb/verilator/mmcm_servo VERILATOR=$VERILATOR`
   (receipt: `receipts/mmcm_servo_make.log`).
2. Reviewer mutants (one per invocation, builds at `-j 4`):
   `python3 scripts/reviewer_mutants.py TREE WORK <name> $VERILATOR`
   with `<name>` one of `clean_unit`, `step_dedupe_removed_unit`,
   `step_dedupe_removed_suite`, `mid_window_memory_removed`,
   `boundary_seed_dropped`, `open_seed_dropped`
   (receipts: `receipts/mutants/*.log`).
3. PHC application-latency probe (real `ptp_csr_sync` and
   `timestamp_counter`, transcribed shadow latch, alignment block and
   servo staging):
   `$VERILATOR --cc --exe --build -j 2 -Wno-fatal -Wno-lint -Wno-UNUSEDSIGNAL --top-module latency_wrap -Mdir OBJ TREE/hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv TREE/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv scripts/latency_probe/latency_wrap.sv scripts/latency_probe/sim_latency.cpp -o Vlat && OBJ/Vlat`
   Negative controls shorten `gptp_slew_tail_r` to 3 and 2 bits
   (receipts: `receipts/latency_probe.log`, `receipts/latency_probe_controls.log`).
