#!/bin/sh
# Elaborate milan_datapath (Verilator --cc, no C++ compile) at a given shape
# include dir, with the milan_dp suite's own flag set and source list.
# Usage (from tb/verilator/milan_dp): elab_shape.sh <shape_incdir> <mdir> <N_STREAMS>
set -eu
shape=$1; mdir=$2; n=$3
srcs=$(make -s print-srcs)
flags=$(make -s print-dp-vflags | sed 's/--exe --build -j [0-9]*//; s/-CFLAGS "[^"]*"//')
eval verilator +incdir+"$shape" $flags --Mdir "$mdir" -GN_STREAMS="$n" $srcs
