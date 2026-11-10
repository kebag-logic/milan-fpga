#!/bin/bash
# Usage: mbx_variant.sh <clone> <variant-dir-with-gen/> <log> <verilator> : the mbx suite's run-if2 leg on a pre-generated layout.
C=$1; V=$2; L=$3; VER=$4
make -C "$C/tb/verilator/mbx" -o if2-gen run-if2 IF2="$V" VERILATOR="$VER" VBUILD_JOBS=3 > "$L" 2>&1; echo $? > "$L.rc"
