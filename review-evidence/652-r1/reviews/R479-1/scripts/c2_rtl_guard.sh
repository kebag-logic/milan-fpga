#!/bin/sh
# Campaign 2: KL_nvm_backend's elaboration guard at base and head for
# N_NAME_P 0/1/99/128/129/235, and with N_NAME_MAX_C planted at 127/129 in a
# copy of the head source. Usage: c2_rtl_guard.sh <base tree> <head tree> <receipt dir>
B=$1; H=$2; R=$3; mkdir -p "$R"; S=$R/c2_scratch; mkdir -p "$S"
out=$R/c2_guard.tsv; : > "$out"
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
for cap in 127 129; do
  sed "s/N_NAME_MAX_C = 128;/N_NAME_MAX_C = $cap;/" "$H/hdl/milan/KL_nvm_backend.sv" > "$S/KL_nvm_backend.sv"
  for n in 127 128 129 130; do lint "head-cap$cap" "$S/KL_nvm_backend.sv" $n; done
done
rm -rf "$S"
echo done > "$R/c2.done"
