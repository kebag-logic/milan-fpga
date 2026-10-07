#!/usr/bin/env bash
# Export both AX7101 configurations at base and head in ONE tree path, then compare.
# Usage: run_ax_compare.sh PYTHON TREE VEX_DATA_DIR WORK_DIR MODE BASE_SHA HEAD_SHA
# The tree is switched base -> head with `git checkout` (same path, so no path
# string can differ); every artifact population is snapshotted after each export.
set -u
py=$1 tree=$2 vex=$3 work=$4 mode=$5 base=$6 head=$7
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
fail=0
for phase in base head; do
  sha=$base; [ "$phase" = head ] && sha=$head
  git -C "$tree" checkout -q --detach "$sha" || exit 3
  [ "$(git -C "$tree" rev-parse HEAD)" = "$sha" ] || exit 3
  [ -z "$(git -C "$tree" status --porcelain --untracked-files=no)" ] || exit 4
  git -C "$tree" status --porcelain --untracked-files=no >"$work/status-before-$phase.txt"
  for cfg in ax7101_1x1_tdm8 ax7101_8x8; do
    tag=$phase-$mode-$cfg
    # Reset generated directories to their tracked state so no stale file survives.
    git -C "$tree" clean -qfdx -- configs/generated sw/builder/out && \
      git -C "$tree" checkout -q -- configs/generated || exit 5
    out=$work/export-$cfg
    "$py" "$here/export_ax.py" "$tree" "$cfg" "$out" "$vex" "$work/$tag.json" "$mode" \
      >"$work/$tag.log" 2>&1
    rc=$?; echo "$rc" >"$work/$tag.rc"; echo "$tag rc=$rc"
    [ "$rc" = 0 ] || fail=1
    snap=$work/snap/$tag; rm -rf "$snap"; mkdir -p "$snap"
    cp -a "$out" "$snap/export"
    cp -a "$tree/sw/builder/out/endstation_$cfg" "$snap/builder"
    cp -a "$tree/configs/generated/endstation_$cfg" "$snap/shape"
    # A tracked generated file that the export rewrote differently would show here.
    git -C "$tree" status --porcelain --untracked-files=no >"$work/status-after-$tag.txt"
    [ -s "$work/status-after-$tag.txt" ] && { echo "tracked file changed by $tag"; fail=1; }
  done
done
for cfg in ax7101_1x1_tdm8 ax7101_8x8; do
  "$py" "$here/compare_manifests.py" "$work/base-$mode-$cfg.json" "$work/head-$mode-$cfg.json" \
    >"$work/compare-$mode-$cfg.txt" 2>&1
  rc=$?; echo "$rc" >"$work/compare-$mode-$cfg.rc"; echo "compare $mode $cfg rc=$rc"
  [ "$rc" = 0 ] || fail=1
done
exit $fail
