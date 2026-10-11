#!/usr/bin/env bash
# parent_gates.sh <label>: the scratch parent's Verilator lint and Yosys elaboration, recorded
set -u
label=$1
R=<scratch>/scripts/rec.sh; P=<scratch>/parent
$R "$label" lint_rtl pinned $P python3 -B scripts/lint_rtl.py --check --self-test --jobs 4
$R "$label" yosys_elab pinned $P syn/yosys/run.sh --mode elaborate
