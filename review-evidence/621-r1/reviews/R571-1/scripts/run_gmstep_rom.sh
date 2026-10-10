#!/usr/bin/env bash
# run_gmstep_rom.sh <model-dir> <rom-dir> <log> : runs a built gmstep model with
# the gPTP ROM image found in <rom-dir> (the engine loads gptp_ucode.hex from
# the working directory at elaboration time).
set -u
mdir=$(realpath "$1"); cd "$2" || exit 2
"$mdir/Vmilan_dp_gmstep" "$mdir/aemi.bin" 0 > "$3" 2>&1
echo $? > "${3%.log}.rc"
