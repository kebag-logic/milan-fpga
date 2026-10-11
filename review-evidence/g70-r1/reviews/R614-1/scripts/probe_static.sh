#!/bin/sh
# Planted controls for the `ooc clock order` gate, run through `make ooc`
# with a stub Vivado so no synthesis can start. Each arm is a fresh export
# of the exact head; the clone itself is never modified.
# Usage: probe_static.sh <clone> <scratch-dir> <receipts-dir>
CO=$1; S=$2; OUT=$3
mkdir -p "$S/stub" "$OUT"
cat > "$S/stub/vivado" <<'EOF'
#!/bin/sh
echo "STUB VIVADO REACHED: $*"
exit 3
EOF
chmod +x "$S/stub/vivado"
printf 'PATH="%s:$PATH"; export PATH\n' "$S/stub" > "$S/stub/settings64.sh"

arm() { # name, then a shell snippet applied inside the export
  name=$1; shift
  d="$S/arm_$name"; rm -rf "$d"; mkdir -p "$d"
  git -C "$CO" archive HEAD | tar -x -C "$d"
  ( cd "$d" && sh -c "$1" )
  ( cd "$d" && git -C "$CO" diff --no-index --stat -- "$CO/syn" "$d/syn" ) > "$OUT/arm_$name.plant" 2>&1
  ( cd "$d" && VIVADO_SETTINGS="$S/stub/settings64.sh" make ooc ) > "$OUT/arm_$name.log" 2>&1
  echo "$name rc=$? stub_reached=$(grep -c 'STUB VIVADO REACHED' "$OUT/arm_$name.log")" >> "$OUT/summary.txt"
}
: > "$OUT/summary.txt"
MOVE='f=syn/ooc/$0; grep -v "^read_xdc " $f > t; awk "{print} /-generic UCODE_HEX_P/ {print \"read_xdc \$SPEC/syn/ooc/ooc_clock.xdc\"}" t > $f; rm t'
arm positive ':'
arm engine_read_after "sh -c '$MOVE' engine_ooc.tcl"
arm ucpu_read_after "sh -c '$MOVE' ucpu_ooc.tcl"
arm main_order "git -C '$CO' show 5dce647:syn/ooc/engine_ooc.tcl > syn/ooc/engine_ooc.tcl; git -C '$CO' show 5dce647:syn/ooc/ucpu_ooc.tcl > syn/ooc/ucpu_ooc.tcl"
# Edge probes beyond the order rule (expected to escape the static gate).
arm pre_synth_override "sed -i 's|^synth_design|create_clock -period 5.000 -name clk [get_ports clk_i]\nsynth_design|' syn/ooc/ucpu_ooc.tcl"
arm foreign_xdc_same_name "sed -i 's|^read_xdc .*|read_xdc /nonexistent/ooc_clock.xdc|' syn/ooc/ucpu_ooc.tcl"
arm xdc_unused_in_synth "sed -i 's|^read_verilog|set_property USED_IN_SYNTHESIS false [get_files ooc_clock.xdc]\nread_verilog|' syn/ooc/ucpu_ooc.tcl"
cat "$OUT/summary.txt"
