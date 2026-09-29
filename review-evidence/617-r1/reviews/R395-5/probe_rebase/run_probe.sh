#!/bin/sh
# R395-5 composition probe: the #602 PHC-only re-base fired into the #617
# datapath leg while the aligner acquires and holds the CRF lock.
# Usage: run_probe.sh <repo> <packet-dir> <verilator-bin-dir>
# Builds an UNTRACKED copy of tb/verilator/capture_coherence's dp recipe in
# <repo>/tb/verilator/zz_r395_probe (removed at the end), once against the
# composed milan_datapath.sv and once per planted coupling (datapath copies
# under <packet>/scratch), and runs sim_dp_rebase.cpp against each.
set -u
REPO=$1; PK=$2; VBIN=$3
export PATH="$VBIN:$PATH"
OUT=$PK/receipts
PD=$REPO/tb/verilator/zz_r395_probe
SRC_DP=$REPO/hdl/milan/milan_datapath.sv
MUT=$PK/scratch/probe_mutants
rm -rf "$PD" "$MUT"; mkdir -p "$PD" "$MUT"
cp "$REPO/tb/verilator/capture_coherence/Makefile" "$REPO/tb/verilator/capture_coherence/coherence_bench.hpp" "$PD/"
cp "$PK/probe_rebase/sim_dp_rebase.cpp" "$PD/sim_dp.cpp"

# Planted couplings of the re-base into the paths this PR binds. Each sed must
# change exactly one line; the script refuses otherwise.
plant() {  # name, instance header (literal), port line (literal), sed expression
  name=$1; header=$2; port=$3; expr=$4
  line=$(awk -v h="$header" -v p="$port" 'index($0, h) {on=1} on && $0 == p {print NR; exit}' "$SRC_DP")
  [ -n "$line" ] || { echo "plant $name: no '$port' after '$header'"; exit 2; }
  sed "${line}${expr}" "$SRC_DP" > "$MUT/$name.sv"
  n=$(diff "$SRC_DP" "$MUT/$name.sv" | grep -c '^>')
  [ "$n" = 1 ] || { echo "plant $name: changed $n lines"; exit 2; }
  { echo "== $name (line $line)"; diff "$SRC_DP" "$MUT/$name.sv"; } >> "$OUT/probe_rebase_plants.txt"
}
: > "$OUT/probe_rebase_plants.txt"
# P1: the re-base restarts the capture walk (an extra media tick into the crossbar)
plant P1_crossbar_tick ') chan_map_capture (' '    .tick_i (media_tick_p),' 's/(media_tick_p)/(media_tick_p | media_rebase_p_w)/'
# P2: the re-base resets the media NCO (the grid restarts its period)
plant P2_nco_reset ') media_nco (' '    .rst_n        (axis_resetn),' 's/(axis_resetn)/(axis_resetn \&\& !media_rebase_p_w)/'
# P3: the re-base resets the grid aligner (re-engagement mid-lock)
plant P3_aligner_reset ') media_grid_align (' '    .rst_n      (axis_resetn),' 's/(axis_resetn)/(axis_resetn \&\& !media_rebase_p_w)/'

cd "$PD" || exit 2
: > "$OUT/probe_rebase_summary.txt"
for v in clean P1_crossbar_tick P2_nco_reset P3_aligner_reset; do
  if [ "$v" = clean ]; then dp=$SRC_DP; else dp=$MUT/$v.sv; fi
  log=$OUT/probe_rebase_$v.log
  { echo "variant $v  DP_SRC=$(basename "$dp")  head $(git -C "$REPO" rev-parse HEAD)"; } > "$log"
  MAKEFLAGS= taskset -c 0-7 make -s --no-print-directory dp-build DP_SRC="$dp" DP_MDIR="obj_$v" >> "$log" 2>&1
  brc=$?
  echo "build rc=$brc" >> "$log"
  if [ $brc -ne 0 ]; then
    printf '%-20s build_rc=%s\n' "$v" "$brc" >> "$OUT/probe_rebase_summary.txt"; continue
  fi
  taskset -c 0-7 timeout 3000 "./obj_$v/Vcoherence_dp" >> "$log" 2>&1
  rc=$?
  echo "run rc=$rc" >> "$log"
  printf '%-20s build_rc=0 run_rc=%s  %s\n' "$v" "$rc" "$(grep -E '^(RESULT|capture_coherence_dp).*' "$log" | tail -1)" >> "$OUT/probe_rebase_summary.txt"
done
cd "$REPO" && rm -rf "$PD"
cat "$OUT/probe_rebase_summary.txt"
