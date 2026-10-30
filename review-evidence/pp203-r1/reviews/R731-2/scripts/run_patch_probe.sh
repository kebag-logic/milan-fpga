#!/bin/sh
# run_patch_probe.sh TREE PATCH SCRATCH VERILATOR : apply an unchanged probe patch to a copy of
# TREE (patch -p1, offsets allowed, no fuzz) and run tb/pp_top section RBT
set -u
W=$(mktemp -d -p "$3"); cp -a "$1"/. "$W"/; rm -rf "$W/tb/pp_top/obj_dir"
(cd "$W" && patch -p1 -F0 < "$2"); echo "apply rc=$?"
make -C "$W/tb/pp_top" reboot VERILATOR="$4"; echo "make rc=$?"
rm -rf "$W"
