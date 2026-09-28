#!/bin/sh
# Run a command in <clone> under the pins-only environment from setup_pins_env.sh.
# Usage: pins_env.sh <clone> <work root> <command...>
set -eu
clone=$1; work=$2; shift 2
export HOME="$work/pins-home" TMPDIR="$work/tmp"
export PATH="$work/pins-venv/bin:$work/pins-tools/bin:/usr/bin:/bin"
unset PYTHONPATH MILAN_LITEX_PYTHON VIRTUAL_ENV
cd "$clone"
exec "$@"
