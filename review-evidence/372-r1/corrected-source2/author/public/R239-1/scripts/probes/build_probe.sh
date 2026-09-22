#!/bin/sh
# R239: build a probe driver against the REAL mux + REAL checker + REAL bind
# from the scratch export, with the Makefile's MUX_SVA_VFLAGS copied verbatim
# (tb/verilator/ptp_ts/Makefile:62-65 at 60c5225f). Usage:
#   build_probe.sh <probe.cpp> <objdir> <width> [<dut.sv>] [<bind.sv>] [<assert-flag>]
set -eu
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
SRC=$VALIDATION_STORAGE/r239-372-r1-work/src
CPP=$1; OBJ=$2; W=$3
DUT=${4:-$SRC/hdl/common/axis_mux_rr_2in_1out.sv}
BIND=${5:-$SRC/tb/common/sva/axis_mux_rr_2in_1out_bind.sv}
ASSERT=${6---assert}
cd "$SRC/tb/verilator/ptp_ts"
"$V" --cc --exe --build -j 8 $ASSERT \
  --top-module axis_mux_rr_2in_1out -GTDATA_WIDTH="$W" \
  -Wall -Wno-CASEINCOMPLETE \
  -CFLAGS "-std=c++17 -O2 -Wall -Wextra -DAXIS_MUX_TDATA_WIDTH=$W" \
  -Mdir "$OBJ" "$DUT" ../../common/sva/axis_stream_source_sva.sv ../../common/sva/axis_mux_rr_2in_1out_sva.sv "$BIND" \
  "$CPP" -o Vprobe
