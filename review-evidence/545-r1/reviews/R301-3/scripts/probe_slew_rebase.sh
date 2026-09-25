#!/usr/bin/env bash
# Disposable probe (not a shipped control): the slew discard also drops the
# window baseline (an unconditional re-base on every slew-marked window).
# Builds a mutated copy of the servo in scratch through the suite Makefile
# (SERVO_RTL/UNIT_MDIR/PHC_MDIR overridden) and runs the unit harness and the
# full slew suite. Reports each harness verdict; the tree is not modified.
set -u
R=${1:?repo}; W=${2:?scratch}
mkdir -p "$W"
python3 - "$R" "$W" <<'PY'
import sys, pathlib
r, w = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
s = (r / "hdl/ieee1722/crf/KL_mmcm_drp_servo.sv").read_text()
a = "if (slew_hit_w) disc_run_r <= '0;"
assert s.count(a) == 1
(w / "probe_rebase.sv").write_text(s.replace(a, "if (slew_hit_w) begin disc_run_r <= '0; win_valid_r <= 1'b0; end"))
PY
M="make --no-print-directory -s -C $R/tb/verilator/mmcm_servo SERVO_RTL=$W/probe_rebase.sv VERILATOR=${VERILATOR:-verilator}"
$M unit-build UNIT_MDIR=$W/obj_unit >/dev/null 2>&1 & p1=$!
$M phc_step_build PHC_MDIR=$W/obj_phc >/dev/null 2>&1 & p2=$!
wait $p1; b1=$?; wait $p2; b2=$?
echo "build rc unit=$b1 phc=$b2"
( cd "$R/tb/verilator/mmcm_servo" && "$W/obj_unit/Vservo_sim" > "$W/unit.out" 2>&1; echo "unit rc=$?" ) &
( cd "$R/tb/verilator/mmcm_servo" && "$W/obj_phc/Vphc_step" +slew_suite > "$W/slew.out" 2>&1; echo "slew_suite rc=$?" ) &
wait
echo "--- unit failures:"; grep -E '\[FAIL\]|checks,' "$W/unit.out"
echo "--- slew suite failures:"; grep -E '\[FAIL\]|checks:|RESULT' "$W/slew.out"
