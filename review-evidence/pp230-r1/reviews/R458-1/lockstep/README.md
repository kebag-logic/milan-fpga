# R458-1 review probes for milan-fpga #230 / processor PR #154

Reviewer-owned, disposable. Nothing here is proposed for the repository.

Inputs: two `git archive` extractions of the processor, base `c4cb84ff` and head `65324390`
(`<base_tree>`, `<head_tree>`), and Verilator 5.050 (`VERILATOR=<path>`).

| Script | What it does |
|---|---|
| `gen_top_lockstep.py <base_tree> <head_tree> <out>` | renames the eight SRP modules of each tree (`_ref`, `_new`) and writes a `KL_srp_top` with the head's exact header that runs both, drives its outputs from the head copy, compares all 51 outputs and 24 internal signals every cycle after the first reset, and counts timer-arm FIFO boundary events |
| `build_top_lockstep.sh <base_tree> <head_tree> <work>` | builds the committed `tb/srp_top` harness (unchanged stimulus; its `u_dut.` peeks re-pointed at the head copy) against that lockstep top, with `--x-initial unique --x-assign unique`; run `LS_SEED=<n> <work>/obj_dir/Vsrp_top_sim` |
| `rand_init.cpp` | sets `randReset(2)` and the seed from `LS_SEED`, so every unreset variable starts random and different in the two copies without touching the bench's argv |
| `ls_fsm.sv`, `ls_fsm_main.cpp` | module-level random lockstep of base and head `KL_srp_talker_fsm`, `KL_srp_listener_fsm` and `KL_srp_admission` at N contexts: pooled stream_id/DA/VLAN values so events match records, re-declarations with new TSpec, settles and teardowns, random ticks, back-pressure, expiries and mid-run resets; every output compared every cycle |
| `build_fsm_lockstep.sh <ref_dir> <new_dir> <head_tree> <N> <work>` | builds `ls_fsm` at N; run `<work>/obj_dir/Vls_fsm <cycles> <seed>` (exit 1 on any mismatch) |
| `probes.py <base_tree> <head_tree> <work> <verilator>` | 17 one-edit faults in the head's new storage paths; for each, the committed suites that build the edited file and the two lockstep benches above |
| `verilator-jcap.sh` | caps a bench Makefile's `verilator --build -j` at 2 (`VERILATOR_REAL=<pinned tool>`) |
| `../vivado/srp_map.tcl` | out-of-context synthesis of `KL_srp_top` alone, to read how each SRP memory maps; not the #638 recipe |

Receipts are in `../receipts/`; paths there are rewritten to `$PACKET`, `$HOME` and `$TOOLS`.
