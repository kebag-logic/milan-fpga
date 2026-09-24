#!/usr/bin/env bash
# Build one milan_dp leg with the Makefile's OWN recipe (read from `make -n run`,
# not copied), into an out-of-tree Mdir, with optional extra Verilator flags
# appended before the output name. The run is a separate step.
#   leg.sh <sim|nxn|nxn8|notify> <mdir-root> [extra verilator args...]
# JOBS (default 8) bounds the C++ compile.
set -euo pipefail
leg=$1; root=$2; shift 2
jobs=${JOBS:-8}
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
cd $LANES/542-notify-pointer/tb/verilator/milan_dp
make --no-print-directory VERILATOR="$V" ltn_rom.hex ucode.hex gptp_ucode.hex >/dev/null
line=$(make --no-print-directory -n VERILATOR="$V" VERILATOR_JOBS="$jobs" run \
       | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' \
       | grep -E -- "-o Vmilan_dp_${leg}\$")
[ "$(printf '%s\n' "$line" | wc -l)" = 1 ] || { echo "leg.sh: no unique recipe for $leg" >&2; exit 2; }
if printf '%s' "$line" | grep -q -- '--Mdir obj_'; then
    line=${line/--Mdir obj_/--Mdir $root/obj_}
else
    line=${line/"$V "/"$V --Mdir $root/obj_dir "}
fi
extra=""
for a in "$@"; do extra+=" $(printf '%q' "$a")"; done
line=${line/ -o Vmilan_dp_${leg}/$extra -o Vmilan_dp_${leg}}
mkdir -p "$root"
printf '%s\n' "$line" > "$root/${leg}.cmd"
echo "leg.sh: sim_nxn.cpp blob $(git hash-object sim_nxn.cpp) at HEAD $(git rev-parse HEAD)" | tee "$root/${leg}.src"
git diff --quiet HEAD -- . || echo "leg.sh: WARNING the milan_dp tree differs from HEAD" | tee -a "$root/${leg}.src"
eval "$line"
