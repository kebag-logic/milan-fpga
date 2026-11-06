#!/usr/bin/env bash
# literal_guard_mutants.sh CHECKOUT BOOT: the two literal edits R738-4-F3 names, each against --placement-controls, reverted after.
set -u
ck=$1; boot=$2; cd "$ck"
one() { # name file sed-expression
  sed -i "$3" "$2"; git diff --stat -- "$2" | tail -1
  python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$boot" --placement-controls 2>&1 | grep -E 'WRONG|ESCAPED|placement controls:' | cut -c1-170
  echo "$1: control rc ${PIPESTATUS[0]}"
  git checkout -q -- "$2"
}
one guard-call-removed tb/verilator/ctrl_split_boot/boot_soc.py "/^    refuse_deviation(build_dir \/ 'csr.csv', flash_map)$/d"
one deviations-return-empty tb/verilator/ctrl_service_budget/split_soc.py '/^def map_deviations/,/^    return out$/s/^    return out$/    return []/'
git status --porcelain | wc -l
