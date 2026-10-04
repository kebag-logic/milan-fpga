# R462-3 commands, in the order run (paths relative to the packet root PKT)

V = the pinned Verilator 5.050 wrapper; `V --version` printed
`Verilator 5.050 2026-07-01 rev v5.050`.

1. `scripts/setup_trees.sh <clone> PKT`: scratch/head is a `git archive` of c725be1;
   scratch/mainrtl is the same, with main b0a74196's `protocol_processor_top.sv` and
   `KL_pp_acmp_listener.sv` (the only two hdl/ files main..head changes).
2. Concurrent, each through `scripts/bg.sh NAME DIR CMD` (log in receipts/NAME.log, rc in receipts/NAME.rc):
   - head-pp_top-run: `make run VERILATOR=V` in scratch/head/tb/pp_top (six builds)
   - head-acmp_listener / mainrtl-acmp_listener: `make run VERILATOR=V` in */tb/acmp_listener
   - mainrtl-aq: `make gsi-build VERILATOR=V && ./obj_dir/Vpp_top_sim --arm-queue-only` in scratch/mainrtl/tb/pp_top
   - probes: `python3 scripts/probe.py PKT V 4` (eight one-line plants; receipts/probes.json)
   - head-acmp-campaign: `scripts/campaign.sh scratch/head scratch/acmp-camp V 6`, which runs the
     committed `tb/pp_top/acmp_mutants.py --output ... --verilator V --jobs 6` unchanged, with
     TMPDIR under scratch/ (attempt 1 ran with the default /tmp and was interrupted from outside
     this review: receipts/head-acmp-campaign-attempt1-interrupted.log).
3. `scripts/lint_two.sh scratch/head V`: lint_hdl.sh's flags and file set, for the two changed tops.
4. Clone integrity: receipts/clone-integrity.txt (commands inline in REPORT.md).
5. Published Vivado reports (milan-fpga 28663f5a, review-evidence/pp639-r1/author-r1/vivado/)
   fetched read-only; extract in receipts/vivado-figures-extract.txt.
6. Hosted checks at the exact head, read-only: receipts/hosted-check-runs.txt.

Published receipts have the pinned toolchain's install prefix replaced by <PINNED_VERILATOR_ROOT>.
