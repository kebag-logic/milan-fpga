# Reviewer scripts (R449-1)

All scripts work on scratch copies only; none edits a checkout. Tools come from PATH or
from `VERILATOR` / `XVLOG`; this review used Verilator 5.050 (pinned), Yosys 0.66, sv2v
0.0.13 and Vivado/xvlog 2026.1 on one 16-CPU host shared with other work.

| Script | What it does |
|---|---|
| `yosys_fault.sh` | copies a processor tree, plants one fault (`inst`, `port`, `param`, `fatal`, `drop`, `bogus`, `allv`, `newmod`, `killonce`, `rcone`) and runs that tree's `syn/yosys/run.sh`; writes `gate.log` and `rc` |
| `fault_batch_one.sh` | one line of `receipts/faults/jobs.txt` (name, allocator, tree, kind, modules) through `yosys_fault.sh`; run as `xargs -P 6 -L 1 fault_batch_one.sh < jobs.txt` with `PACKET` set |
| `nvm_bound_probe.sh` | item 2: `tb/nvm_port/elab_bounds.sh` and sv2v + yosys `chparam` at 65527/65528 over five variants of `KL_pp_nvm_port.sv` (pristine, `$error`, `$warning`, a bound derived from `dev_len_o` and `HDR_LEN_C`, `HDR_LEN_C` = 10) |
| `xvlog_all.sh` | item 3: `xvlog -sv`, packages first, one module file per invocation, over every `.sv` under `hdl/` |
| `ooc_netlist.tcl` | item 3: sources the in-tree `syn/ooc/protocol_processor_ooc.tcl` for a given tree and writes the netlist (`write_verilog -mode design`) |
| `own_arm.sh` | item 4: plants one `gen_ucode.py` patch in a scratch copy and runs `tb/pp_top`'s `aecp-dispatch` target |
