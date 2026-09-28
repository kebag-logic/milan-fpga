#!/usr/bin/env bash
# Reconstructed parent first-probe harness (kebag-logic/milan-fpga#606 class):
# processor talker at REV + parent KL_pp_maap_shim + the published fixed
# oracle reproduce_first_probe.cpp. Usage:
#   parent_first_probe.sh SRC_CLONE REV SHIM_SV ORACLE_CPP SCRATCH VERILATOR OUT_LOG
set -uo pipefail
src=$1; rev=$2; shim=$3; oracle=$4; scratch=$5; vl=$6; log=$7
here=$(cd "$(dirname "$0")" && pwd)
# guard: the log must be a new .txt file and the tool must be executable
case "$log" in *.txt) ;; *) echo "refuse: OUT_LOG must end in .txt"; exit 2;; esac
[ -e "$log" ] && { echo "refuse: OUT_LOG exists"; exit 2; }
[ -x "$vl" ] || { echo "refuse: VERILATOR not executable"; exit 2; }
t="$scratch/fp-$rev"; rm -rf "$t"; mkdir -p "$t/pp" "$t/b"
git -C "$src" archive HEAD | tar -x -C "$t/pp"          # head testbench/BFM
git -C "$src" show "$rev:hdl/acmp/KL_acmp_talker.sv" \
  | sed 's/^module KL_acmp_talker$/module KL_acmp_talker_core/; s/^endmodule : KL_acmp_talker$/endmodule : KL_acmp_talker_core/' \
  > "$t/b/KL_acmp_talker_core.sv"
cp "$here/first_probe_wrap.sv" "$shim" "$t/b/"; cp "$oracle" "$t/b/reproduce_first_probe.cpp"
{
  echo "talker rev $(git -C "$src" rev-parse "$rev")"
  sha256sum "$t/b/KL_acmp_talker_core.sv" "$t/b/$(basename "$shim")" "$t/b/reproduce_first_probe.cpp" "$t/b/first_probe_wrap.sv" | sed "s#$t/##"
  grep -c 'module KL_acmp_talker_core' "$t/b/KL_acmp_talker_core.sv" | sed 's/^/renamed module lines: /'
  cd "$t/b" && "$vl" --cc --exe --build -j 0 --top-module KL_acmp_talker -Wno-fatal -Wno-lint -Wno-style \
    -CFLAGS "-std=c++17 -O2 -I$t/pp/tb -I$t/pp/tb/acmp_talker" \
    "$t/pp/hdl/common/pp_pkg.sv" "$t/pp/hdl/srp/srp_pkg.sv" KL_acmp_talker_core.sv \
    "$(basename "$shim")" first_probe_wrap.sv reproduce_first_probe.cpp -o first_probe >build.log 2>&1
  echo "build rc=$?"; tail -3 build.log | grep -i error
  ./obj_dir/first_probe; echo "harness rc=$?"
} > "$log" 2>&1
cat "$log"; rm -rf "$t"
