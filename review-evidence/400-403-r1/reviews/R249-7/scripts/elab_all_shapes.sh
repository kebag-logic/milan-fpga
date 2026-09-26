#!/usr/bin/env bash
# Lint-elaborates the composed milan_datapath under every shipped generated
# shape, gPTP plane off and on, using the milan_dp suite's own source list
# and warning flags. Usage: elab_all_shapes.sh <checkout> <logdir>
set -u
repo=$1; logs=$2; mkdir -p "$logs"
dp="$repo/tb/verilator/milan_dp"
srcs=$(make -s --no-print-directory -C "$dp" print-srcs) || exit 2
flags=$(make -s --no-print-directory -C "$dp" print-dp-vflags) || exit 2
# drop build-only switches and the -CFLAGS group; keep incdirs, warnings, -G
flags=$(printf '%s' "$flags" | sed -E 's/-CFLAGS "[^"]*"//; s/--cc|--exe|--build|-j [0-9]+//g; s/-GGPTP_PLANE_EN_P=[01]//')
export srcs flags dp logs
ls -d "$repo"/configs/generated/*/ | xargs -n1 basename | while read -r s; do
  for g in 0 1; do echo "$s $g"; done
done | xargs -P 8 -L1 bash -c '
  s=$0; g=$1
  cd "$dp" || exit 2
  # N_STREAMS from the shape: ADP_TALKER_SRC_C is N_STREAMS or N_STREAMS+1 (CRF)
  src=$(sed -nE "s/.*localparam int ADP_TALKER_SRC_C *= *([0-9]+);.*/\1/p" ../../../configs/generated/$s/gen/adp_shape_defaults.svh)
  n=$(( src > 1 ? src - 1 : 1 ))
  eval verilator --lint-only +incdir+../../../configs/generated/$s $flags -GGPTP_PLANE_EN_P=$g -GN_STREAMS=$n $srcs > "$logs/$s.gptp$g.log" 2>&1
  rc=$?; echo -e "$rc\t$s\tGPTP_PLANE_EN_P=$g\tN_STREAMS=$n"'
