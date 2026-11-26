#!/usr/bin/env bash
# Build and run a reviewer probe (the head bench plus CASES_CPP) against a tree under review.
# Usage: build_probe.sh TREE WORKDIR VERILATOR CASES_CPP
set -euo pipefail
tree=$1; work=$2; verilator=$3; cases=$4
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work"
# the head's bench, everything before its main(), then the probe's cases and main()
awk '/^int main\(int argc, char \*\*argv\)/{exit} {print}' "$tree/tb/verilator/usbnet/sim_main.cpp" > "$work/sim_probe.cpp"
cat "$cases" >> "$work/sim_probe.cpp"
rtl=$tree/hdl/usbnet
"$verilator" --cc --exe --build -j 4 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-PROCASSINIT \
  -Werror-UNDRIVEN -Werror-MULTIDRIVEN -CFLAGS "-std=c++17 -O2" --top-module KL_usbnet_tap \
  -GCLK_HZ_P=1000000 -GRATE_BPS_P=800000 -GBURST_OCTETS_P=3200 -GHOST_TIMEOUT_MS_P=3 --Mdir "$work/obj" \
  "$rtl/KL_usbnet_pkg.sv" "$rtl/KL_usbnet_rx_copy.sv" "$rtl/KL_usbnet_tx_inject.sv" "$rtl/KL_usbnet_tx_arb.sv" \
  "$rtl/KL_usbnet_tap.sv" "$work/sim_probe.cpp" -o Vprobe > "$work/build.log" 2>&1
set +e
"$work/obj/Vprobe"
echo "probe rc=$?"
