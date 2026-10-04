#!/bin/bash
# Wave 1: head suites in the clone, and the unit-level and OOC probes in copies.
. "$(dirname "$0")/env.sh"
cd "$CLONE"
# 1. the timed notify leg at head ([UNB] incl.), clean build
run notify_head make -C tb/verilator/milan_dp notify VERILATOR="$VERILATOR" VERILATOR_JOBS=6
# 2. the crf_rx suite at head: unit, discontinuity, talker_step, receiver mutants
run crfrx_head make -C tb/verilator/crf_rx all VERILATOR="$VERILATOR"
# 3. crf_rx unit against the BASE KL_crf_rx (the lane's unit checks must fail)
mkcopy crfrx_base
git -C "$CLONE" show $BASE_SHA:hdl/ieee1722/crf/KL_crf_rx.sv > $SCR/crfrx_base/hdl/ieee1722/crf/KL_crf_rx.sv
run crfrx_unit_base make -C $SCR/crfrx_base/tb/verilator/crf_rx unit VERILATOR="$VERILATOR"
# 4. probe P6: the fall counts an unlock even when NOT locked
mkcopy crfrx_p6
python3 "$PKT/scripts/plant.py" $SCR/crfrx_p6/hdl/ieee1722/crf/KL_crf_rx.sv \
  "      if (w_bind_fall_w && locked_o) begin" "      if (w_bind_fall_w) begin" \
  && run crfrx_unit_p6 make -C $SCR/crfrx_p6/tb/verilator/crf_rx unit VERILATOR="$VERILATOR"
# 5. probe P7: the fall drops lock and pushes but scores no unlock (CRF counts like a rebind)
mkcopy crfrx_p7
python3 "$PKT/scripts/plant.py" $SCR/crfrx_p7/hdl/ieee1722/crf/KL_crf_rx.sv \
  "        cnt_unlocked_o <= cnt_unlocked_o + 32'd1;
        dirty_p_o      <= 1'b1;
      end

      //! not-bound -> bound" "        dirty_p_o      <= 1'b1;
      end

      //! not-bound -> bound" \
  && run crfrx_unit_p7 make -C $SCR/crfrx_p7/tb/verilator/crf_rx unit VERILATOR="$VERILATOR"
wait
