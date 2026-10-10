#!/usr/bin/env bash
# Apply a normal-diff plant to a scratch copy of KL_maap.sv (no checkout edit),
# then build and run the unit and real-datapath MAAP harnesses against it.
# Usage: reapply_plant.sh <tree> <patch> <workdir> <receipts-dir> <verilator>
set -u
T=$1; PATCHF=$2; W=$3; O=$4; V=$5
mkdir -p "$W" "$O"
patch -o "$W/KL_maap.sv" "$T/hdl/ieee1722/maap/KL_maap.sv" "$PATCHF" > "$O/patch.log" 2>&1; echo $? > "$O/patch.rc"
diff "$T/hdl/ieee1722/maap/KL_maap.sv" "$W/KL_maap.sv" > "$O/applied.diff"
python3 -I - "$T" "$W/KL_maap.sv" > "$O/equals_campaign_mutant.log" <<'PY'
import sys, pathlib
t, plant = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).read_text()
src = (t / "hdl/ieee1722/maap/KL_maap.sv").read_text()
a, b = "port_operational_i && !port_operational_r", "!port_operational_i && port_operational_r"
print("anchor count", src.count(a), "; plant equals mutants.py m5_restart_on_link_loss:", src.replace(a, b) == plant)
PY
M=$T/tb/verilator/maap
( make -C "$M" build MAAP_RTL="$W/KL_maap.sv" MDIR="$W/obj" VERILATOR="$V" VERILATOR_JOBS=4 > "$O/unit_build.log" 2>&1 && (cd "$W/obj" && ./VKL_maap_sim) > "$O/unit_run.log" 2>&1; echo $? > "$O/unit.rc" ) &
( make -C "$M" integration-build MAAP_RTL="$W/KL_maap.sv" DP_MDIR="$W/int" VERILATOR="$V" > "$O/int_build.log" 2>&1 && (cd "$W/int" && ./maap_integration) > "$O/int_run.log" 2>&1; echo $? > "$O/int.rc" ) &
wait
