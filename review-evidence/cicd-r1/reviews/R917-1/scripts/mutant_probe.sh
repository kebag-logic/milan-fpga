#!/bin/bash
# mutant_probe.sh OUTDIR CPUS SCRATCH
# Reviewer-planted mutants and probe-omission controls, run at the base and the
# head tree copies under SCRATCH (SCRATCH/base, SCRATCH/head), each through the
# suite's own Makefile target with an RTL override; no tracked file is edited.
#   P1 crf_rx  : FRAMES/UNSUPPORTED counter pegs at 255 (the old 8-bit law)
#                -> must fail the same [G1] check names at base and head.
#   P2 maap    : the PROBE draw folds the current LFSR state instead of the next
#                -> base and head must report the same failures.
#   P3 control : head crf_rx unit build with tout_r dropped from probes.vlt and
#                pdu_count_o/fmt_err_o downgraded to public_flat_rd (a copy of
#                the suite dir); the reviewer's probe_check.py must flag it.
set -u
OUT=$1 CPUS=$2 S=$3
HERE=$(cd "$(dirname "$0")" && pwd)
export VERILATOR="$HERE/vwrap.sh" VW_JOBS=2 VERILATOR_JOBS=2 MAKEFLAGS='-j1 --no-print-directory'
mkdir -p "$OUT"
for t in base head; do
  T=$S/$t
  sed 's/fmt_err_o <= fmt_err_o + 32'"'"'d1;/fmt_err_o <= (fmt_err_o == 32'"'"'d255) ? fmt_err_o : fmt_err_o + 32'"'"'d1;/' \
    "$T/hdl/ieee1722/crf/KL_crf_rx.sv" > "$OUT/$t.p1_KL_crf_rx.sv"
  cmp -s "$T/hdl/ieee1722/crf/KL_crf_rx.sv" "$OUT/$t.p1_KL_crf_rx.sv" && echo "P1 anchor missing ($t)"
  taskset -c "$CPUS" make -s -C "$T/tb/verilator/crf_rx" unit-build RX_RTL="$OUT/$t.p1_KL_crf_rx.sv" \
    UNIT_MDIR="$OUT/$t.p1_obj" > "$OUT/$t.p1.build.log" 2>&1
  echo "build rc=$?" >> "$OUT/$t.p1.build.log"
  taskset -c "$CPUS" "$OUT/$t.p1_obj/Vcrf_rx_sim" > "$OUT/$t.p1.run.log" 2>&1
  echo "run rc=$?" >> "$OUT/$t.p1.run.log"

  sed 's/probe_fold(lfsr_next_w)}/probe_fold(lfsr_r)}/' \
    "$T/hdl/ieee1722/maap/KL_maap.sv" > "$OUT/$t.p2_KL_maap.sv"
  cmp -s "$T/hdl/ieee1722/maap/KL_maap.sv" "$OUT/$t.p2_KL_maap.sv" && echo "P2 anchor missing ($t)"
  taskset -c "$CPUS" make -s -C "$T/tb/verilator/maap" build MAAP_RTL="$OUT/$t.p2_KL_maap.sv" \
    MDIR="$OUT/$t.p2_obj" > "$OUT/$t.p2.build.log" 2>&1
  echo "build rc=$?" >> "$OUT/$t.p2.build.log"
  taskset -c "$CPUS" "$OUT/$t.p2_obj/VKL_maap_sim" > "$OUT/$t.p2.run.log" 2>&1
  echo "run rc=$?" >> "$OUT/$t.p2.run.log"
done

# P3: a copy of the head suite directory with a weakened probes list
C=$S/p3_head
mkdir -p "$C/tb/verilator"
rsync -a --exclude='obj_*' "$S/head/tb/verilator/crf_rx" "$C/tb/verilator/"
ln -sfn "$S/head/hdl" "$C/hdl"
ln -sfn "$S/head/tb/common" "$C/tb/common"
sed -e '/-var "tout_r"/d' -e 's/^public_flat_rw/public_flat_rd/' "$S/head/tb/verilator/crf_rx/probes.vlt" \
  > "$C/tb/verilator/crf_rx/probes.vlt"
diff "$S/head/tb/verilator/crf_rx/probes.vlt" "$C/tb/verilator/crf_rx/probes.vlt" > "$OUT/p3.probes.diff"
taskset -c "$CPUS" make -s -C "$C/tb/verilator/crf_rx" unit-build UNIT_MDIR="$OUT/p3_obj" > "$OUT/p3.build.log" 2>&1
echo "build rc=$?" >> "$OUT/p3.build.log"
python3 -I "$HERE/probe_check.py" "$OUT/p3_obj" "$C/tb/verilator/crf_rx/sim_main.cpp" > "$OUT/p3.probe_check.txt" 2>&1
echo "probe_check rc=$?" >> "$OUT/p3.probe_check.txt"
taskset -c "$CPUS" "$OUT/p3_obj/Vcrf_rx_sim" > "$OUT/p3.run.log" 2>&1
echo "run rc=$?" >> "$OUT/p3.run.log"
taskset -c "$CPUS" "$S/head/tb/verilator/crf_rx/obj_dir/Vcrf_rx_sim" > "$OUT/head.clean.run.log" 2>&1
echo "run rc=$?" >> "$OUT/head.clean.run.log"
echo done > "$OUT/DONE"
