#!/usr/bin/env bash
# docs_steps.sh CLONE OUT JOB/ID...: docs_steps.py in the docs workflow's environment (round 1's docs_wf.sh).
. /data-2/milan/tmp/963-a819/bin/env.sh
export PATH=/data-2/milan/tmp/963-a819/venv-md/bin:$PATH:$VALIDATION_TOOLS/sv2v-v0.0.12
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory"
exec /data-2/milan/tmp/963-a819/venv-md/bin/python -B "$(dirname "$0")/docs_steps.py" "$@"
