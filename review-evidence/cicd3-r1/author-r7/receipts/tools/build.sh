#!/bin/bash
# build.sh TREE CPUS: in r7/wt/TREE, `make clean`, then ci-prepare and both gPTP builds, pinned to CPUS, through the
# shared ccache (OBJCACHE=ccache, the host's one cache_dir). Records each runtime and build input's sha256.
set -u
T=$1; C=$2; R=/data-2/milan/tmp/cicd-a839/r7; W=$R/wt/$T; O=$R/meas/build-$T
. $R/bin/env.sh
export VERILATOR_JOBS=4 MAKEFLAGS='-j1 --no-print-directory' OBJCACHE=ccache
mkdir -p "$O"; cd "$W/tb/verilator/milan_dp" || exit 99
git -C "$W" rev-parse HEAD > "$O/head"
make -s clean > /dev/null 2>&1
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" \
  make -s ci-prepare build-gptp build-gptp-lat > "$O/out" 2>&1
echo "rc=$?" >> "$O/time"
{ sha256sum ucode.hex ltn_rom.hex gptp_ucode.hex gptp_lat_ucode.hex obj_gptp/Vmilan_dp_gptp obj_gptplat/Vmilan_dp_gptplat
  for d in obj_gptp obj_gptplat; do
    printf '%s  %s/{*.cpp,*.h} (Verilator output, sorted)\n' "$(cd $d && cat $(ls *.cpp *.h | sort) | sha256sum | cut -d' ' -f1)" "$d"
  done; } > "$O/sha256"
echo "$T build: $(head -1 "$O/time") $(tail -1 "$O/time")" >> $R/meas/progress
