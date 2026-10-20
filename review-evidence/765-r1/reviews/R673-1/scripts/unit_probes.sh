#!/bin/bash
# Reviewer mutant probes on the crf_rx counter harness and the avtp_rxmon N=4 harness.
# Usage: unit_probes.sh TREE OUTDIR   (TREE = a clean checkout of the head under review)
set -u
T=$1; O=$2; H=$(dirname "$0"); mkdir -p "$O"
CRF=$T/hdl/ieee1722/crf/KL_crf_rx.sv
RXM=$T/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv
run_crf() { # name file
  make -s -C "$T/tb/verilator/crf_rx" unit-build RX_RTL="$2" UNIT_MDIR="$O/obj_$1" > "$O/$1.build.log" 2>&1 || { echo "$1 BUILD-FAIL" >> "$O/SUMMARY.txt"; return; }
  (cd "$T/tb/verilator/crf_rx" && "$O/obj_$1/Vcrf_rx_sim") > "$O/$1.log" 2>&1; rc=$?
  echo "$1 rc=$rc failed: $(grep -E '\[(FAIL|fail)\]|FAIL ' "$O/$1.log" | head -8 | tr '\n' '|')" >> "$O/SUMMARY.txt"
}
run_nx() { # name file
  make -s -C "$T/tb/verilator/avtp_rxmon" nx-build RXMON_SRC="$2" NX_MDIR="$O/obj_$1" > "$O/$1.build.log" 2>&1 || { echo "$1 BUILD-FAIL" >> "$O/SUMMARY.txt"; return; }
  (cd "$T/tb/verilator/avtp_rxmon" && "$O/obj_$1/Vavtp_rxmon_nx_sim") > "$O/$1.log" 2>&1; rc=$?
  echo "$1 rc=$rc failed: $(grep -E '\[(FAIL|fail)\]|FAIL ' "$O/$1.log" | head -8 | tr '\n' '|')" >> "$O/SUMMARY.txt"
}
: > "$O/SUMMARY.txt"
# crf: a format reject drops the established lock
python3 -I "$H/plant.py" "$CRF" "$O/crf_lockdrop.sv" "          settle_r  <= '0;\n        end else begin\n          //! SEQ_NUM_MISMATCH" "          settle_r  <= '0;\n          locked_o  <= 1'b0;\n        end else begin\n          //! SEQ_NUM_MISMATCH" >/dev/null && run_crf crf_lockdrop "$O/crf_lockdrop.sv" &
# crf: a format reject advances the sequence cursor
python3 -I "$H/plant.py" "$CRF" "$O/crf_seqadv.sv" "          settle_r  <= '0;\n        end else begin\n          //! SEQ_NUM_MISMATCH" "          settle_r  <= '0;\n          exp_seq_r <= seq_i + 8'd1;\n          have_seq_r <= 1'b1;\n        end else begin\n          //! SEQ_NUM_MISMATCH" >/dev/null && run_crf crf_seqadv "$O/crf_seqadv.sv" &
# crf: clean control through the same recipe
run_crf crf_clean "$CRF" &
# avtp: the zero-count term dropped
python3 -I "$H/plant.py" "$RXM" "$O/rxm_nozero.sv" "                  (p_cpf_w     != 10'd0)       &&\n" "" >/dev/null && run_nx rxm_nozero "$O/rxm_nozero.sv" &
# avtp: the compare reads the current format's samples_per_frame field instead of its channel count
python3 -I "$H/plant.py" "$RXM" "$O/rxm_spf.sv" "fmt_r[31:22];   //! channels_per_frame" "fmt_r[21:12];   //! channels_per_frame" >/dev/null && run_nx rxm_spf "$O/rxm_spf.sv" &
# avtp: subtype term dropped (an AAF-shaped PDU of another subtype accepted)
python3 -I "$H/plant.py" "$RXM" "$O/rxm_nosubtype.sv" "  wire fmt_ok_w = (cur_w.subtype == f_subtype_w) &&" "  wire fmt_ok_w = 1'b1 &&" >/dev/null && run_nx rxm_nosubtype "$O/rxm_nosubtype.sv" &
run_nx rxm_clean "$RXM" &
wait
sort "$O/SUMMARY.txt"
