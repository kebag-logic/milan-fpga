#!/bin/sh
# Byte identity of the generated ROMs and the preprocessed engine sources at two
# exported trees. Usage: rom_identity.sh BASE_TREE HEAD_TREE OUT_DIR VERILATOR
set -eu
base=$1; head=$2; out=$3; vl=$4
mkdir -p "$out"
for side in base head; do
  eval tree=\$$side
  ( cd "$tree/hdl/aecp/ucode" && python3 -B gen_ucode.py -o "$out/$side.ucode.hex" )
  ( cd "$tree/hdl/acmp/rom" && python3 -B gen_ltn_rom.py -o "$out/$side.ltn_rom.hex" )
done
sha256sum "$out"/base.ucode.hex "$out"/head.ucode.hex "$out"/base.ltn_rom.hex "$out"/head.ltn_rom.hex \
  | sed "s#$out/##"
cmp "$out/base.ucode.hex" "$out/head.ucode.hex" && echo "ucode.hex: base == head"
cmp "$out/base.ltn_rom.hex" "$out/head.ltn_rom.hex" && echo "ltn_rom.hex: base == head"
# every .sv / .svh under hdl/ identical, byte for byte
( cd "$base" && find hdl -name '*.sv' -o -name '*.svh' | LC_ALL=C sort | xargs sha256sum ) > "$out/base.sv.sha256"
( cd "$head" && find hdl -name '*.sv' -o -name '*.svh' | LC_ALL=C sort | xargs sha256sum ) > "$out/head.sv.sha256"
cmp "$out/base.sv.sha256" "$out/head.sv.sha256" && echo "hdl .sv/.svh: $(wc -l < "$out/head.sv.sha256") files identical"
# preprocessed engine (every define and include resolved) at base and head
for side in base head; do
  eval tree=\$$side
  ( cd "$tree" && "$vl" -E -P --bbox-unsup hdl/common/pp_pkg.sv hdl/aecp/ucpu_pkg.sv \
      hdl/aecp/KL_aecp_engine.sv > "$out/$side.engine.E.sv" 2> "$out/$side.engine.E.err" ) || true
done
sha256sum "$out"/base.engine.E.sv "$out"/head.engine.E.sv | sed "s#$out/##"
cmp "$out/base.engine.E.sv" "$out/head.engine.E.sv" && echo "preprocessed engine: base == head"
