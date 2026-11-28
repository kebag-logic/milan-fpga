#!/bin/sh
# Run the validation kit and the RV32 gate of a tsn-c-stack clone, each with its own log and return-code file.
# Usage: TOOLS=<pinned toolchain directory> run_gates.sh <clone> <work>
# The kit runs four groups at once, so --jobs 4 keeps it near 16 parallel jobs; the RV32 gate was started with
# --jobs 4 once the kit's two builds had finished.
set -u
clone=$1; work=$2
. "$(dirname "$0")/env.sh"
mkdir -p "$work"
cd "$clone" || exit 2
python3 scripts/validate.py --work "$work/build-validation" --jobs 4 > "$work/validate.log" 2>&1; echo $? > "$work/validate.rc"
python3 scripts/baremetal.py --work "$work/build-rv32" --jobs 4 > "$work/baremetal.log" 2>&1; echo $? > "$work/baremetal.rc"
