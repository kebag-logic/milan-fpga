#!/usr/bin/env bash
# Disposable mutation probes for the C8 waiver pass-through and the L6/L10 cleanup.
# Usage: mutate_gate36b.sh <pristine-probe-tree> <work-dir> <receipt-dir>
# Each mutant is a fresh copy of the pristine tree with one python substitution;
# run_gate36b.py must FAIL (rc != 0) for the mutant to count as killed.
set -u
src=$1; work=$2; out=$3; mkdir -p "$work" "$out"; here=$(cd "$(dirname "$0")" && pwd)
mutant() {  # id file old new
  local id=$1 f=$2 old=$3 new=$4 d="$work/$1"
  rm -rf "$d"; cp -a "$src" "$d"
  python3 - "$d/$f" "$old" "$new" <<'PY' || { echo "$id APPLY-FAILED" > "$out/mut_$id.rc"; return; }
import sys; p, o, n = sys.argv[1:]
s = open(p).read(); assert s.count(o) == 1, f"{o!r} occurs {s.count(o)} times"; open(p, "w").write(s.replace(o, n))
PY
  ( timeout 1200 python3 "$here/run_gate36b.py" "$d" > "$out/mut_$id.log" 2>&1; echo $? > "$out/mut_$id.rc" ) &
}
mutant M1_builder_lint_off sw/builder/endstation_builder.py "        576)" "        576, lint=False)"
mutant M2_soc_lint_off sw/litex/milan_soc.py "identity_from_overlay(ovl)), 576)" "identity_from_overlay(ovl)), 576, lint=False)"
mutant M3_specs_drop_waiver avdecc/aem_specs.py 'lint_waivers=list(ovl.get("model_lint_waivers", [])),' 'lint_waivers=[],'
mutant M4_loader_drop_waiver sw/builder/endstation_builder.py 'model_lint_waivers=list(cfg.get("model_lint_waivers") or []),' 'model_lint_waivers=[],'
mutant M5_doc_drop_waiver avdecc/gen_aemi_image.py '**({"lint_waivers": M["LINT_WAIVERS"]} if M.get("LINT_WAIVERS") else {}),' ''
mutant M6_waiver_narrow configs/endstation_ax7101_8x8.yaml '    last: 7' '    last: 6'
wait
for f in "$out"/mut_*.rc; do id=$(basename "$f" .rc); rc=$(cat "$f"); case $rc in 0) v=SURVIVED;; *APPLY*) v=INVALID;; *) v=KILLED;; esac; echo "$id rc=$rc $v"; done
