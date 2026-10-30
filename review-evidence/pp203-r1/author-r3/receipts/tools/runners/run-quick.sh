#!/usr/bin/env bash
export PATH=<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TMPDIR=<runs>/tmp
G=<tools>/gate.sh
O=<runs>/gates
mkdir -p $O
$G $O make_check <work2> make check
$G $O lint_hdl_5052 <work2> bash scripts/lint_hdl.sh
verilator --version > $O/lint_hdl_5052.version
PATH=<tool>/pinned-verilator-5.050:$PATH $G $O lint_hdl_5050 <work2> bash scripts/lint_hdl.sh
PATH=<tool>/pinned-verilator-5.050:$PATH verilator --version > $O/lint_hdl_5050.version
$G $O reboot <work2>/tb/pp_top make reboot
PATH=<tool>/sv2v-v0.0.12:$PATH $G $O yosys_run <work2> ./syn/yosys/run.sh
PATH=<tool>/sv2v-v0.0.12:$PATH $G $O elab_guards <work2> python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
touch $O/quick.done
