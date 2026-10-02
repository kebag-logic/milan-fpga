#!/bin/sh
# R421-4 fault probe: put the lane's two microprogram entry points back at
# round 3's words 2000/2016 (main's READ_DESCRIPTOR overlays now live there) and
# show that every layer that grades the relocation fails: tb/ucpu N6/N7 (bench
# constants), check_upc_map.py and tb/pp_top ID1/NP3 (engine constants).
# Usage: relocation_probe.sh CLONE WORK OUT   (verilator on PATH: the pinned 5.050)
set -u
CLONE=$1; W=$2; OUT=$3; HEAD=95a78c099ee5aa914521975355adc1dfef99d01c
rm -rf "$W"; mkdir -p "$W/u" "$W/e"
git -C "$CLONE" archive $HEAD | tar -x -C "$W/u"; git -C "$CLONE" archive $HEAD | tar -x -C "$W/e"
sed -i 's/E_IDNOTIF = 464; /E_IDNOTIF = 2000;/; s/E_SINFOUNS = 480; /E_SINFOUNS = 2016;/' "$W/u/tb/ucpu/sim_main.cpp"
(cd "$W/u/tb/ucpu" && make > "$W/ucpu_stale.log" 2>&1); echo "ucpu stale rc=$?"
sed -i "s/UPC_IDNOTIF_C  = 11'd464; /UPC_IDNOTIF_C  = 11'd2000;/; s/UPC_SINFOUNS_C = 11'd480; /UPC_SINFOUNS_C = 11'd2016;/" "$W/e/hdl/aecp/KL_aecp_engine.sv"
(cd "$W/e" && python3 scripts/check_upc_map.py) > "$W/upc_stale.log" 2>&1; echo "check_upc_map stale rc=$?"
(cd "$W/e/tb/pp_top" && make identify-build gsi-build > "$W/eng_build.log" 2>&1 && { ./obj_idn/Vpp_top_idn > "$W/eng_idn.log" 2>&1; echo "idn rc=$?"; ./obj_dir/Vpp_top_sim --notify-only > "$W/eng_np.log" 2>&1; echo "notify-only rc=$?"; })
{ echo "== tb/ucpu with E_IDNOTIF/E_SINFOUNS at 2000/2016 (round 3's addresses)"; grep -E '^FAIL|checks:' "$W/ucpu_stale.log"
  echo "== check_upc_map with the engine's UPC constants at 2000/2016"; cat "$W/upc_stale.log"
  echo "== pp_top identify build, engine at 2000/2016"; grep -E '^FAIL: ID1|^ID:|^\[build' "$W/eng_idn.log"
  echo "== pp_top --notify-only, engine at 2000/2016"; grep -E '^FAIL|^[A-Z]+:|^\[build' "$W/eng_np.log"; } > "$OUT"
