#!/bin/bash
# Usage: run_sweep.sh <repo> <packet> : builds the shipping and 2x2 milan_csr and compares each page row.
R=$1; P=$2; V=${VERILATOR:-verilator}; O=$P/receipts/sweep; S=$P/scratch/sweep
mkdir -p "$S" "$O"; python3 -I "$P/tools/gen_sweep.py" "$R" "$S/sweep.cpp.in"
build() { # name listeners lsn0row shape
  local n=$1 l=$2 row=$3 shape=$4 d=$S/$1
  mkdir -p "$d"; sed "s/N_L/$l/g" "$S/sweep.cpp.in" > "$d/sweep.cpp"
  ( cd "$d" && "$V" --cc --exe --build -j 8 --public-flat-rw +incdir+"$R/configs/generated/$shape" +incdir+"$R/hdl/common/csr" \
      -Wno-fatal -Wno-lint -Wno-UNOPTFLAT -GNUM_QUEUES=5 -GADDR_WIDTH=16 -GN_LISTENERS_P=$l -GN_TALKERS_P=$l -GSRP_LSN0_ROW_P=$row \
      -GGPTP_PLANE_EN_P=1 -GMILAN_CLK_FREQ_HZ_P=50000000 -GCHMAP_RDBK_P=3 -GPPS_P=0 -GPPS_WIDTH_CYC_P=50000 \
      --top-module milan_csr "$R/hdl/common/csr/milan_csr.sv" sweep.cpp -CFLAGS "-std=c++17 -O1" -o sim ) > "$O/build_$n.log" 2>&1
  echo $? > "$O/build_$n.rc"
  "$d/obj_dir/sim" > "$S/$n.log" 2> "$O/run_$n.err"; echo $? > "$O/run_$n.rc"
  sha256sum "$S/$n.log" | cut -d' ' -f1 > "$O/sweep_$n.sha256"
  python3 -I "$P/tools/compare_sweep.py" "$R/docs/reference/REGISTER_MAP.md" "$S/$n.log" "$l" > "$O/compare_$n.txt" 2>&1; echo $? > "$O/compare_$n.rc"
}
build ship 1 2 endstation_ax7101_1x1_tdm8 &
build 2x2 2 4 endstation_arty_4x4 &
wait
