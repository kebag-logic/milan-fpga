#!/usr/bin/env bash
# Parent identity evidence for the gPTP plane at the CURRENT scratch-parent
# gitlink. Usage: parent_evidence.sh <label>
#  1. the parent's own gate, verbatim:
#       syn/yosys/run.sh --mode elaborate --no-structural --top KL_gptp_shadow
#  2. the same staged sv2v input and the same Yosys program, plus a
#     per-module stat and an RTLIL dump of the hierarchical netlist
#  3. the same program followed by flatten; opt; opt_clean (the tie-off
#     propagated), with stat and an RTLIL dump
#  4. the three generated ROM images, their sha256, and the bundle digest
#     result_cache.py computes
set -u
label="$1"
P=$VALIDATION_STORAGE/g35-a599/parent
S=$VALIDATION_STORAGE/g35-a599
OUT=$S/parent-$label
rm -rf "$OUT"; mkdir -p "$OUT/results" "$OUT/work"
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
cd "$P" || exit 2
[ "$(git -C "$P/gptp-processor" rev-parse --show-toplevel)" = "$P/gptp-processor" ] || { echo "submodule toplevel mismatch" >&2; exit 2; }
{
  echo "parent HEAD $(git -C "$P" rev-parse HEAD)"
  echo "gitlink     $(git -C "$P" rev-parse :gptp-processor)"
  echo "submodule   $(git -C "$P/gptp-processor" rev-parse HEAD)"
  echo "yosys       $(yosys -V)"
  echo "sv2v        $(sv2v --version)"
  git -C "$P" status --short
} > "$OUT/identity.txt" 2>&1

# 1. the parent's gate, verbatim
syn/yosys/run.sh --mode elaborate --no-structural --top KL_gptp_shadow \
  --results "$OUT/results" > "$OUT/gate.log" 2>&1
echo $? > "$OUT/gate.rc"

# 2./3. the same input and program, with dumps
W=$OUT/work
mapfile -t rec < <(syn/yosys/run.sh --emit KL_gptp_shadow)
flags=(); srcs=()
for l in "${rec[@]}"; do
  case "$l" in
    define=*) flags+=("-D${l#define=}") ;;
    incdir=*) flags+=("-I" "${l#incdir=}") ;;
    src=*)    srcs+=("${l#src=}") ;;
  esac
done
sv2v --top=KL_gptp_shadow "${flags[@]}" "${srcs[@]}" > "$W/KL_gptp_shadow.v" 2> "$W/sv2v.err"
echo $? > "$OUT/sv2v.rc"
python3 syn/yosys/enforce_elaboration.py "$W/KL_gptp_shadow.v"
echo $? > "$OUT/enforce.rc"
# ROMs into the yosys working directory, exactly as run.sh generates them
python3 protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o "$W/ltn_rom.hex" >/dev/null
python3 protocol-processor/hdl/aecp/ucode/gen_ucode.py -o "$W/ucode.hex" >/dev/null
python3 gptp-processor/hdl/ucode/gen_gptp_ucode.py -o "$W/gptp_ucode.hex" >/dev/null
( cd "$W" && sha256sum ltn_rom.hex ucode.hex gptp_ucode.hex ) > "$OUT/rom_sha256.txt"
python3 syn/yosys/result_cache.py rom-digest --rom-dir "$W" > "$OUT/rom_bundle_digest.txt"
echo $? > "$OUT/rom_bundle.rc"
base="read_verilog KL_gptp_shadow.v; hierarchy -check -top KL_gptp_shadow; proc; opt_clean; check -assert; stat -top KL_gptp_shadow"
( cd "$W" && yosys -q -p "$base; tee -q -o hier.stat.txt stat; tee -q -o hier.stat.json stat -json; write_rtlil hier.il" ) > "$OUT/hier.log" 2>&1
echo $? > "$OUT/hier.rc"
( cd "$W" && yosys -q -p "$base; flatten; opt; opt_clean; tee -q -o flat.stat.txt stat; tee -q -o flat.stat.json stat -json; write_rtlil flat.il" ) > "$OUT/flat.log" 2>&1
echo $? > "$OUT/flat.rc"
( cd "$W" && sha256sum KL_gptp_shadow.v hier.il flat.il ) > "$OUT/netlist_sha256.txt"
for f in gate sv2v enforce rom_bundle hier flat; do echo "$f rc=$(cat "$OUT/$f.rc")"; done
