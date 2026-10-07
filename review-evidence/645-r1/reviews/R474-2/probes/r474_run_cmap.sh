#!/bin/bash
# R474-2: build and run chmap_capture in one planted tree; log + rc beside it.
# usage: r474_run_cmap.sh TREE VERILATOR
T=$1; V=$2; D=$T/tb/verilator/chmap_capture
make -C $D build VERILATOR=$V VERILATOR_JOBS=8 > $T/cmap_build.log 2>&1; echo $? > $T/cmap_build.rc
timeout 600 $D/obj_dir/Vchmap_wrap > $T/cmap_run.log 2>&1; echo $? > $T/cmap_run.rc
