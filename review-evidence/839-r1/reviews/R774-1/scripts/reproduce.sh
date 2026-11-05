#!/bin/sh
# Reproduce this round's probes. usage: reproduce.sh <clean clone at 992c3d7b with submodules> <work dir> <verilator>
# Builds seven copies (head, base RTL, mutant without the MAAP/AAF/CRF hold, each with and without the
# early-enable probe leg, plus byte-dump legs), runs `make bootsa` in each concurrently, prints the tallies.
set -eu
clone=$1; work=$2; vl=$3; here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work/logs"
mk() { mkdir -p "$work/$1"; (cd "$clone" && tar -cf - .) | tar -xf - -C "$work/$1"; }
for n in head base noxtra headearly noxtraearly headdump basedump; do mk $n; done
for n in base basedump; do git -C "$clone" show 604899c08ff1cd1830e1dd08b733109ef852400c:hdl/milan/milan_datapath.sv > "$work/$n/hdl/milan/milan_datapath.sv"; done
for n in noxtra noxtraearly; do python3 -I "$here/plant_noxtra.py" "$work/$n/hdl/milan/milan_datapath.sv"; done
for n in headearly noxtraearly; do python3 -I "$here/plant_early_enable.py" "$work/$n/tb/verilator/milan_dp/sim_boot_sa.cpp"; done
for n in headdump basedump; do python3 -I "$here/plant_dump.py" "$work/$n/tb/verilator/milan_dp/sim_boot_sa.cpp"; done
for n in head base noxtra headearly noxtraearly headdump basedump; do
  (cd "$work/$n/tb/verilator/milan_dp" && make bootsa VERILATOR="$vl" VERILATOR_JOBS=2 > "$work/logs/bootsa_$n.log" 2>&1; echo $? > "$work/logs/bootsa_$n.rc") &
done
wait
for n in head base noxtra headearly noxtraearly headdump basedump; do echo "$n rc=$(cat "$work/logs/bootsa_$n.rc") $(grep -E '== bootsa: checks' "$work/logs/bootsa_$n.log")"; done
# expected: head 0/40, base 9 failures, noxtra 0 failures (survivor), headearly 0, noxtraearly 4 failures
