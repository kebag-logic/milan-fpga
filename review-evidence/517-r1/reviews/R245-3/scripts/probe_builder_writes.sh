#!/bin/bash
# Does the builder, invoked exactly as sim_nxn.cpp:405-410 invokes it (from
# tb/verilator/milan_dp with ../../../configs/<cfg>.yaml and a private -o),
# write any tracked file? usage: probe_builder_writes.sh DISPOSABLE_TREE OUTDIR
# Whole-tree write-set audit via a timestamp marker, plus tracked-header
# sha256/mtime before and after. Positive control: the same builder from the
# repository root with configs/<cfg>.yaml must rewrite the tracked header.
set -u
T=$1 OUT=$2; mkdir -p "$OUT"; cd "$T" || exit 90
hdr() { git ls-files 'configs/generated/*' | xargs stat -c '%Y.%y %n' ; git ls-files 'configs/generated/*' | xargs sha256sum; }
for cfg in endstation_arty_4x4 endstation_ax7101_8x8 endstation_ax7101_1x1_tdm8; do
  hdr > "$OUT/$cfg.before"; sleep 1.1; touch "$OUT/marker"; sleep 1.1
  priv=$(mktemp -d); (cd tb/verilator/milan_dp && python3 ../../../sw/builder/endstation_builder.py "../../../configs/$cfg.yaml" -o "$priv/builder" > "$OUT/$cfg.suite-dir.log" 2>&1); rc=$?
  hdr > "$OUT/$cfg.after"
  changed=$(find "$T" -path "$T/.git" -prune -o -newer "$OUT/marker" -type f -print | grep -v -E '/__pycache__/' | sed "s#^$T/##")
  private_hdr=$(ls "$priv/builder/$cfg/gen/adp_shape_defaults.svh" 2>/dev/null)
  echo "SUITE-DIR $cfg exit=$rc tracked_changed=$(cmp -s "$OUT/$cfg.before" "$OUT/$cfg.after" && echo no || echo YES) files_written_in_tree=[${changed}] private_header=$([ -n "$private_hdr" ] && echo present || echo absent)"
  rm -rf "$priv"
done
# positive control: from the repository root, the tracked branch is taken
cfg=endstation_arty_4x4; hdr > "$OUT/control.before"; sleep 1.1; touch "$OUT/marker"; sleep 1.1
priv=$(mktemp -d); python3 sw/builder/endstation_builder.py "configs/$cfg.yaml" -o "$priv/builder" > "$OUT/control.log" 2>&1; rc=$?
hdr > "$OUT/control.after"
changed=$(find "$T" -path "$T/.git" -prune -o -newer "$OUT/marker" -type f -print | grep -v -E '/__pycache__/' | sed "s#^$T/##")
echo "REPO-ROOT-CONTROL $cfg exit=$rc tracked_mtime_changed=$(cmp -s "$OUT/control.before" "$OUT/control.after" && echo no || echo YES) files_written_in_tree=[${changed}]"
rm -rf "$priv"; git -C "$T" status --porcelain | head
