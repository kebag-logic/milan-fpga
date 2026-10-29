#!/bin/sh
# Reviewer run: the platform image and the size fixture at the four points, and the ledger's refusals.
# usage: r733_images.sh CHECKOUT OUT RUNTIME_DIR CSR_CSV PYTHON
set -u
R=$1; OUT=$2; RT=$3; CSV=$4; PY=$5
mkdir -p "$OUT"
cd "$R" || exit 2
plat() {  # name config interfaces [ledger]
  name=$1; cfg=$2; nif=$3; shift 3
  "$PY" -B sw/firmware/ctrl/test/ctrl_plat_image.py --config "configs/$cfg.yaml" --interfaces "$nif" \
    --csr-csv "$CSV" --output "$OUT/$name" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" "$@" \
    > "$OUT/$name.log" 2>&1
  echo "$name rc=$?"
}
fix() {
  name=$1; cfg=$2; nif=$3; shift 3
  "$PY" -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$cfg.yaml" --interfaces "$nif" --with-aecp \
    --layout split --output "$OUT/$name" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" "$@" \
    > "$OUT/$name.log" 2>&1
  echo "$name rc=$?"
}
plat plat-1x1-if1 endstation_ax7101_1x1_tdm8 1
plat plat-1x1-if2 endstation_ax7101_1x1_tdm8 2
plat plat-8x8-if1 endstation_ax7101_8x8 1
plat plat-8x8-if2-ledgered endstation_ax7101_8x8 2 --ledgered-point platform-8x8-two-interfaces
fix fix-1x1-if1 endstation_ax7101_1x1_tdm8 1
fix fix-1x1-if2 endstation_ax7101_1x1_tdm8 2
fix fix-8x8-if1 endstation_ax7101_8x8 1
fix fix-8x8-if2-ledgered endstation_ax7101_8x8 2 --ledgered-point 8x8-two-interfaces
# the refusals: each must exit 2
plat REFUSE-plat-8x8-if2-no-override endstation_ax7101_8x8 2
plat REFUSE-plat-8x8-if2-fixture-override endstation_ax7101_8x8 2 --ledgered-point 8x8-two-interfaces
plat REFUSE-plat-override-1x1-if1 endstation_ax7101_1x1_tdm8 1 --ledgered-point platform-8x8-two-interfaces
plat REFUSE-plat-override-1x1-if2 endstation_ax7101_1x1_tdm8 2 --ledgered-point platform-8x8-two-interfaces
plat REFUSE-plat-override-8x8-if1 endstation_ax7101_8x8 1 --ledgered-point platform-8x8-two-interfaces
fix REFUSE-fix-8x8-if2-platform-override endstation_ax7101_8x8 2 --ledgered-point platform-8x8-two-interfaces
