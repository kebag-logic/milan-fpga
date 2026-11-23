#!/usr/bin/env bash
# docs_steps.sh CLONE OUT JOB/ID...: docs_steps.py in the docs workflow's environment (round 1's docs_wf.sh).
. <scratch>/bin/env.sh
export PATH=<scratch>/venv-md/bin:$PATH:<tools>/sv2v-v0.0.12
export VERILATOR=<tools>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory"
exec <scratch>/venv-md/bin/python -B "$(dirname "$0")/docs_steps.py" "$@"
