#!/usr/bin/env bash
# R357-1 on-disk mutants run through the real gate entry point.
# Usage: probe_emitter_mutants.sh <pristine-head-copy> <scratch-dir> <receipt-dir>
# Each mutant gets its own disposable copy of the head tree; the gate is run
# as CI runs it (docs.yml: check_entity_shape.py --self-test) and, for RTL and
# census mutants, also without --self-test. KILLED = nonzero exit.
set -u
src=$(cd "$1" && pwd); scratch=$2; out=$3
mkdir -p "$scratch" "$out"

mutate() {  # name file python-replacement-expr
  local name=$1 file=$2 old=$3 new=$4 dir="$scratch/mut_$1"
  rm -rf "$dir"; cp -a "$src" "$dir"
  python3 - "$dir/$file" "$old" "$new" <<'EOF'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode('unicode_escape'), sys.argv[3].encode().decode('unicode_escape')
t = open(p).read()
assert t.count(old) == 1, (p, old, t.count(old))
open(p, 'w').write(t.replace(old, new))
EOF
}

run_one() {  # name mode(plain|--self-test)
  local name=$1 mode=$2 dir="$scratch/mut_$1" rc
  [ "$mode" = plain ] && mode=""
  ( cd "$dir" && timeout 1200 python3 scripts/check_entity_shape.py $mode ) \
      > "$out/mutant_${name}${mode:+_selftest}.log" 2>&1
  rc=$?
  echo "$name ${mode:-plain} rc=$rc $([ $rc -ne 0 ] && echo KILLED || echo SURVIVED)"
}

B=sw/builder/endstation_builder.py
mutate emit_cross $B "{int(dc['CONTROL'])}" "{int(dc['AUDIO_UNIT'])}"
mutate emit_literal $B "{int(dc['CONTROL'])}" "1"
mutate census_zero $B '"CLOCK_DOMAIN": 1, "CONTROL": 1,' '"CLOCK_DOMAIN": 1, "CONTROL": 0,'
mutate rom_two_controls avdecc/aem_assemble.py \
  '    descs.append((CONTROL, 0, d_control_identify(names["control_identify"])))\n' \
  '    descs.append((CONTROL, 0, d_control_identify(names["control_identify"])))\n    descs.append((CONTROL, 1, d_control_identify(names["control_identify"])))\n'
mutate rtl_h1_unbound hdl/milan/KL_pp_shadow.sv '      .N_CONTROL_P    (N_CONTROL_P),\n' ''
mutate rtl_h0_literal hdl/milan/milan_datapath.sv '.N_CONTROL_P         (AEM_N_CONTROL_C)' '.N_CONTROL_P         (1)'

{
  printf '%s\n' "emit_cross --self-test" "emit_cross plain" "emit_literal --self-test" \
    "emit_literal plain" "census_zero plain" "rom_two_controls plain" "rtl_h1_unbound plain" \
    "rtl_h0_literal plain"
} | xargs -P 8 -L 1 bash -c "$(declare -f run_one); scratch='$scratch'; out='$out'; run_one \"\$0\" \"\${1:-}\"" \
  | sort | tee "$out/emitter_mutants_summary.txt"
