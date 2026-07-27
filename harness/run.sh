#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# THE entry point. One command runs everything, unattended.
#
#   harness/run.sh                       # start, or CONTINUE the newest run
#   harness/run.sh --new                 # force a fresh run id
#   harness/run.sh --from validation     # resume at a phase
#   harness/run.sh --only es-4.7         # one item
#   harness/run.sh --dry-run             # every phase against the mock bench
#
# Never prompts, never reads stdin. Detach it however you like:
#
#   setsid nohup harness/run.sh > /dev/null 2>&1 &
#   systemd-run --user --unit=milan-campaign harness/run.sh
#
# INTERPRETER. Analysis needs numpy, which is not installed system-wide on the
# dev box. Resolution order:
#   1. $MILAN_HARNESS_PYTHON
#   2. [exec].python in the config (read by the harness itself)
#   3. a `.venv` beside this script
#   4. python3 on PATH
# Everything except THD+N runs fine on a bare python3 >= 3.11 (tomllib).

set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ -n "${MILAN_HARNESS_PYTHON:-}" ]; then
    PY="$MILAN_HARNESS_PYTHON"
elif [ -x "$HERE/.venv/bin/python3" ]; then
    PY="$HERE/.venv/bin/python3"
else
    PY=python3
fi

if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo "harness: need python >= 3.11 (tomllib is standard library there);" \
         "got $("$PY" -V 2>&1)" >&2
    exit 2
fi

# The package lives beside this script; keep it importable without installing.
PYTHONPATH="$HERE${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONPATH

exec "$PY" -m milanharness "$@"
