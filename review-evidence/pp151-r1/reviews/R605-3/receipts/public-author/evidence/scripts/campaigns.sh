#!/usr/bin/env bash
# campaigns.sh <label> <jobs-per-campaign> <max-concurrent> [name ...]
# Runs every campaign that builds a changed file, in the lane, each recorded by rec.sh.
set -u
label=$1 J=$2 K=$3; shift 3
L=<lane>
R=<scratch>/scripts/rec.sh
O=<scratch>/rec/$label/camp; mkdir -p "$O"
V=<tools>/pinned-verilator-5.050/verilator
declare -A C=(
  [srp_top]="python3 -B tb/srp_top/mutants.py --output $O/srp_top --jobs $J"
  [adp_engine]="python3 -B tb/adp_engine/mutants.py --output $O/adp_engine --jobs $J"
  [aecp]="python3 -B tb/pp_top/aecp_mutants.py --output $O/aecp --jobs $J"
  [aecp_dispatch]="python3 -B tb/pp_top/aecp_dispatch_mutants.py --output $O/aecp_dispatch --verilator $V --jobs $J"
  [ctr]="python3 -B tb/pp_top/ctr_mutants.py --output $O/ctr --jobs $J"
  [acmp]="python3 -B tb/pp_top/acmp_mutants.py --output $O/acmp --verilator $V --jobs $J"
  [d3]="python3 -B tb/pp_top/d3_mutants.py --output $O/d3 --verilator $V --jobs $J"
  [gsi]="python3 -B tb/pp_top/gsi_mutants.py --output $O/gsi --verilator $V --jobs $J"
  [notify]="python3 -B tb/pp_top/notify_mutants.py --output $O/notify --verilator $V --jobs $J"
  [name_wr]="python3 -B tb/pp_top/name_wr_mutant.py --output $O/name_wr"
  [name_state]="python3 -B tb/name_state/mutants.py --verilator $V --jobs 2 --output $O/name_state"
  [maap]="python3 -B tb/maap/mutants.py --output $O/maap --jobs $J"
  [srp_admission]="python3 -B tb/srp_admission/mutants.py --output $O/srp_admission --jobs $J"
  [desc_mem_guard]="python3 -B tb/desc_mem_guard/mutate.py --output $O/desc_mem_guard"
  [nvm_figures]="make -C tb/nvm_port figures"
)
names=("$@"); [ ${#names[@]} -gt 0 ] || names=(srp_top adp_engine aecp aecp_dispatch ctr acmp d3 gsi notify name_wr name_state maap srp_admission desc_mem_guard nvm_figures)
for n in "${names[@]}"; do
  [ -n "${C[$n]:-}" ] || { echo "unknown campaign $n"; exit 2; }
  while [ "$(jobs -rp | wc -l)" -ge "$K" ]; do wait -n; done
  echo "$(date +%T) start $n"
  # shellcheck disable=SC2086
  $R "$label" "camp_$n" host "$L" ${C[$n]} &
done
wait
echo "$(date +%T) all done"
for n in "${names[@]}"; do echo "$n rc=$(cat <scratch>/rec/$label/camp_$n.rc) secs=$(cat <scratch>/rec/$label/camp_$n.secs)"; done
