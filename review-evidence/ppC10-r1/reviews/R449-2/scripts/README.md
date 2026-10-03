# Reviewer scripts (R449-2)

All scripts work on scratch copies only, and none edits a checkout. Tools come from PATH or
from `VERILATOR`. This review used Verilator 5.050 (pinned), Yosys 0.66 and sv2v 0.0.13 on
one 16-CPU host shared with other work.

| Script | What it does |
|---|---|
| `yosys_fault.sh`, `fault_batch_one.sh` | R449-1's fault planter and batch line, byte-identical to round 1 (unchanged probes). `receipts/faults/jobs.txt` lists the 21 cases |
| `nvm_bound_probe.sh` | R449-1's item-2 probe, byte-identical. Its `derived` edit targets round 1's literal text, so at this head that variant cannot apply and its row repeats `pristine` |
| `summarize_faults.sh` | turns `<dir>/<case>/{rc,gate.log}` into the round-1 SUMMARY table format |
| `census_probe.sh`, `census_batch_one.sh` | add one module under `hdl/top/` with a given header form (split, `automatic`, comments, `macromodule`, attribute on the header line or the line before, `automatic` plus an all.v syntax fault), optionally name it in `tops`, then run the tree's `syn/yosys/run.sh` |
| `elab_mutants.sh` | mutants of `KL_pp_nvm_port`'s `MAX_PAYLOAD_P` guard against `tb/nvm_port/elab_bounds.sh`. A `-noyosys` case runs with sv2v and yosys removed from PATH (symlink farm) |
| `port_netlist.sh` | `KL_pp_nvm_port`'s sv2v + yosys netlist at two revisions and two `MAX_PAYLOAD_P` values; prints the hashes and compares them |
| `parent_gate3_mutants.sh` | the parent's `check_rtl_source_lists.py` and `--selftest` on a c8 + p2 + c10 parent tree: six refusal-disabling checker mutants and three data plants |
