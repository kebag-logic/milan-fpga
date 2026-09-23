#!/bin/sh
# Build and run the disposable probe variants from the exact-head export.
# Usage: 31_run_probes.sh <clone> <export-root> <step: build|run>
# VERILATOR must be set. Builds run one at a time (each at -j 8); runs are 5
# single-threaded simulations in parallel (limit is 8 jobs).
set -eu
clone=$1
exp=$2
step=$3
: "${VERILATOR:?}"
BASE=ede8d48ecd7c7f589a14b957951f040d92c99c70
here=$(cd "$(dirname "$0")" && pwd)
pdir="$exp/tb/verilator/media_grid_align_probe"
case "$step" in
  build)
    python3 -I -B "$here/30_make_probe.py" "$exp"
    mkdir -p "$exp/base_hdl"
    git -C "$clone" show "$BASE:hdl/ieee1722/crf/KL_media_grid_align.sv" > "$exp/base_hdl/KL_media_grid_align.sv"
    git -C "$clone" show "$BASE:hdl/ieee1722/aaf/KL_chan_map_capture.sv" > "$exp/base_hdl/KL_chan_map_capture.sv"
    echo "base aligner blob: $(git hash-object --no-filters "$exp/base_hdl/KL_media_grid_align.sv") (tree says $(git -C "$clone" rev-parse "$BASE:hdl/ieee1722/crf/KL_media_grid_align.sv"))"
    echo "base capture blob: $(git hash-object --no-filters "$exp/base_hdl/KL_chan_map_capture.sv") (tree says $(git -C "$clone" rev-parse "$BASE:hdl/ieee1722/aaf/KL_chan_map_capture.sv"))"
    cd "$pdir"
    rm -rf obj_*
    printf '%s\n' \
      "head||" \
      "k8|+define+PROBE_KEEPOFF=8|" \
      "k12|+define+PROBE_KEEPOFF=12|" \
      "k24|+define+PROBE_KEEPOFF=24|" \
      "base||base" \
    | xargs -P 1 -I{} sh -c '
        v=$(echo "{}" | cut -d"|" -f1); d=$(echo "{}" | cut -d"|" -f2); b=$(echo "{}" | cut -d"|" -f3)
        if [ "$b" = base ]; then
          make build VERILATOR="$VERILATOR" MDIR=obj_$v DEFS="$d" \
            AL=../../../base_hdl/KL_media_grid_align.sv CAP=../../../base_hdl/KL_chan_map_capture.sv > build_$v.log 2>&1
        else
          make build VERILATOR="$VERILATOR" MDIR=obj_$v DEFS="$d" > build_$v.log 2>&1
        fi && echo "built $v" || { echo "BUILD FAILED $v"; tail -20 build_$v.log; }'
    ;;
  run)
    cd "$pdir"
    for v in head k8 k12 k24 base; do echo "$v"; done | xargs -P 5 -I{} sh -c \
      './obj_{}/Vprobe > run_{}.log 2>&1; echo "ran {} rc=$?"'
    ;;
  *) echo "unknown step"; exit 2;;
esac
