#!/bin/bash
# cand_boot.sh CLONE OUT SHAPE: the split boot simulation on a fix candidate's clone (S9's environment).
export PATH=<home>/br-milan-rv32/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=<scratch>/fg4/tmp MAKEFLAGS="-j8 --no-print-directory"
cd "$1" && echo "HEAD $(git rev-parse --short=8 HEAD)" && <home>/litex-milan/venv/bin/python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$2" --shape "$3"
