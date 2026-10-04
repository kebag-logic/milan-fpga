#!/bin/sh
# Campaign 7: KL_nvm_backend's elaboration guard at base and head for N_NAME_P
# 0/1/99/128/129/235 under the pinned Verilator, and the nvm_backend suite at
# the head (the RTL the builder reads its capacity from).
# Usage: c7_rtl.sh <base tree> <head tree> <receipt dir>   (pinned verilator first on PATH)
B=$1; H=$2; R=$3; mkdir -p "$R"; S=$R/../../scratch/c7_vl; rm -rf "$S"; mkdir -p "$S"
verilator --version > "$R/c7_verilator.txt"; command -v verilator >> "$R/c7_verilator.txt"
out=$R/c7_guard.tsv; : > "$out"
lint() { # label src n
  d=$(mktemp -d "$S/vl.XXXX")
  verilator --lint-only -Wall --Mdir "$d" --top-module KL_nvm_backend "-GN_NAME_P=$3" "$2" > "$d/log" 2>&1
  rc=$?
  msg=$(grep -o 'KL_nvm_backend: N_NAME_P=[^"]*' "$d/log" | head -1)
  other=$(grep -c '%Error' "$d/log")
  printf '%s\t%s\trc=%s\terrors=%s\t%s\n' "$1" "$3" "$rc" "$other" "$msg" >> "$out"
}
for n in 0 1 99 128 129 235; do
  lint base "$B/hdl/milan/KL_nvm_backend.sv" $n
  lint head "$H/hdl/milan/KL_nvm_backend.sv" $n
done
(cd "$H" && grep -n 'N_NAME_MAX_C' hdl/milan/KL_nvm_backend.sv) > "$R/c7_capacity_decl.txt"
(cd "$H" && python3 -c "import sys; sys.path.insert(0,'sw/builder'); import endstation_builder as e; print(e.nvm_name_capacity())") \
  >> "$R/c7_capacity_decl.txt" 2>&1
(cd "$H" && make -C tb/verilator/nvm_backend -j8 > "$R/c7_nvm_backend.log" 2>&1; echo $? > "$R/c7_nvm_backend.rc")
(cd "$H" && git status --porcelain --ignored=no) > "$R/c7_status_after.txt"
echo done > "$R/c7.done"
