#!/bin/sh
# R474-3 commands, as run (each long job was started with scripts/bg.sh and
# waited on in the foreground). Set these before running:
#   CLONE    a detached checkout of 2525eae9567865a8bc741901914bdf5a1caf2c26
#   PACKET   this packet directory; SCRATCH=$PACKET/scratch; L=$PACKET/receipts
#   V        the pinned Verilator 5.050 wrapper
set -eu
export PYTHONDONTWRITEBYTECODE=1 VERILATOR="$V"
cd "$CLONE"
# A: capture suite at head (RTL leg + netlist leg)
make -C tb/verilator/chmap_capture run VERILATOR="$V" VERILATOR_JOBS=4 MDIR="$SCRATCH/cc_head" NETDIR="$SCRATCH/net_head"
# B, E: the lane's twelve planted controls
python3 -B tb/verilator/follow_ring/mutants.py --mdir "$SCRATCH/mut_cap" --jobs 3 --select SINGLE-DROP HELD-DUP STARVED-HELD-DUP
python3 -B tb/verilator/follow_ring/mutants.py --mdir "$SCRATCH/mut_fr" --jobs 4 --select NO-ARM NO-RECOVERY HIGH-ARM QUIET-ARM NO-SETTLE RENDER-ONLY EARLY W1 OVERSHOOT
# C: follow_ring integration (b8, pullin, small pulls, settle control)
make -C tb/verilator/follow_ring run VERILATOR="$V" VERILATOR_JOBS=4 SWEEP_JOBS=4 MDIR="$SCRATCH/fr_head"
# D: reviewer probes in a disposable copy (hdl and tb/common symlinked to the clone)
T="$SCRATCH/probe/tree"; mkdir -p "$T/tb/verilator"
ln -sfn "$CLONE/hdl" "$T/hdl"; ln -sfn "$CLONE/tb/common" "$T/tb/common"
cp -r tb/verilator/chmap_capture "$T/tb/verilator/"
python3 -I -B "$PACKET/scripts/r474_probe.py" tb/verilator/chmap_capture/sim_main.cpp \
  "$PACKET/scripts/r474_probe.cpp" "$T/tb/verilator/chmap_capture/sim_main.cpp"
sed "s/&& q_fed_r\[pop_pair_w\] && (pop_cnt_w == '0) && !pop_hold_w;/\&\& q_fed_r[pop_pair_w] \&\& (pop_cnt_w == '0);/" \
  hdl/ieee1722/aaf/KL_chan_map_capture.sv > "$SCRATCH/probe/KL_chan_map_capture_prefix.sv"
make -C "$T/tb/verilator/chmap_capture" build VERILATOR="$V" VERILATOR_JOBS=4 MDIR="$SCRATCH/probe/obj_head"
make -C "$T/tb/verilator/chmap_capture" build VERILATOR="$V" VERILATOR_JOBS=4 MDIR="$SCRATCH/probe/obj_prefix" \
  CMAP_SRC="$SCRATCH/probe/KL_chan_map_capture_prefix.sv"
(cd "$T/tb/verilator/chmap_capture" && "$SCRATCH/probe/obj_head/Vchmap_wrap") > "$L/D_probe_head.run.log"
(cd "$T/tb/verilator/chmap_capture" && "$SCRATCH/probe/obj_prefix/Vchmap_wrap") > "$L/D_probe_prefix.run.log" || true
# F: other suites that compile the capture
make -C tb/verilator/capture_coherence run VERILATOR="$V" MDIR="$SCRATCH/cc_coh"
cp -r tb/verilator/media_grid_align "$T/tb/verilator/"; make -C "$T/tb/verilator/media_grid_align" run VERILATOR="$V"
# G: source and docs gates (read-only)
python3 -I -B scripts/check_doc_style.py
python3 -I -B scripts/docs_check.py
python3 -I -B scripts/check_em_dash.py --base fea346e76c2a57ed5cd131af8fc68dfeff57f877 || true  # renderer absent: cannot judge
VERILATOR="$V" python3 -B scripts/lint_rtl.py --check
# H: merge audit
for m in 701b8332b 2525eae95; do git merge-tree --write-tree "$m^1" "$m^2" | head -1; git rev-parse "$m^{tree}"; done
# Z: restoration check
python3 -I -B "$PACKET/scripts/verify_checkout.py" "$CLONE" 2525eae9567865a8bc741901914bdf5a1caf2c26 a0545d5d4f4e098464fbd6a6a7a21fb4c735a423
