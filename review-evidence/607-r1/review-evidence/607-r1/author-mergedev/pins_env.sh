#!/bin/sh
# Run one command in the lane under the pins-only environment built by setup_pins_env.sh:
# its own HOME (so no bench venv, SDK or cache is reachable), the venv first on PATH,
# the pinned sv2v, and no PYTHONPATH or interpreter override.
# Usage: pins_env.sh <lane> <work root> <command...>
set -eu
lane=$1
work=$2
shift 2
export HOME="$work/pins-home" TMPDIR="$work/tmp"
export PATH="$work/pins-venv/bin:$work/pins-tools/bin:/usr/bin:/bin"
unset PYTHONPATH MILAN_LITEX_PYTHON VIRTUAL_ENV
cd "$lane"
exec "$@"
