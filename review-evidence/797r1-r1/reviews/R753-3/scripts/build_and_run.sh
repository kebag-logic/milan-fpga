#!/bin/sh
# build_and_run.sh <repo-root> <packet> <label> <L> <T> <LSN0_ROW> <config-dir>
R=$1; P=$2; L=$3; NL=$4; NT=$5; ROW=$6; CFG=$7
V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
O=$P/scratch/$L; mkdir -p $O
python3 -I $P/scripts/gen_sweep.py $R $O/main.cpp $NL || exit 3
$V --cc --exe --build -j 8 -O1 -Wno-fatal -Wno-lint -Wno-style --public-flat-rw --top-module milan_csr \
  -GN_LISTENERS_P=$NL -GN_TALKERS_P=$NT -GSRP_LSN0_ROW_P=$ROW -GCHMAP_RDBK_P=3 \
  -I$R/hdl/common/csr -I$CFG -CFLAGS "-O1" --Mdir $O/obj $R/hdl/common/csr/milan_csr.sv $O/main.cpp > $O/build.log 2>&1 || { tail -30 $O/build.log; exit 4; }
$O/obj/Vmilan_csr > $O/sweep.log 2> $O/directed.log || exit 5
wc -l $O/sweep.log
