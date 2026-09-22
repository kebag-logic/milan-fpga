#!/bin/sh
# R239: build-variant probes through the suite's OWN recipe (make mux-sva-build
# with the campaign's override variables), in the scratch export only.
#   noassert-flag  MUX_SVA_ASSERT empty: is 5.050 default-on, as the guide says?
#   bind-omitted   the bind replaced by an empty file: must the harness refuse?
#   bind-warning   a bind with a width-truncating connection: must -Wall fail it?
#   bind-instpath  a bind naming an instance path: accepted or refused by 5.050?
set -u
V=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
S=$VALIDATION_STORAGE/r239-372-r1-work/src/tb/verilator/ptp_ts
P=$VALIDATION_STORAGE/r239-372-r1-work/probes
R=$WORKSPACE_HOME/milan-fpga-management/2026-09-22/372-r1-r239/raw
BIND=$S/../../common/sva/axis_mux_rr_2in_1out_bind.sv
mkdir -p "$P/variants"
: > "$P/variants/empty_bind.sv"
sed 's/\.owner_none_i(state == IDLE)/.owner_none_i(state)/' "$BIND" > "$P/variants/warn_bind.sv"
sed 's/^bind axis_mux_rr_2in_1out /bind axis_mux_rr_2in_1out.u_nothing /' "$BIND" > "$P/variants/instpath_bind.sv"
diff "$BIND" "$P/variants/warn_bind.sv" > "$R/variant-warn_bind.diff"
diff "$BIND" "$P/variants/instpath_bind.sv" > "$R/variant-instpath_bind.diff"
build() { # name width bind assertflag
  make --no-print-directory -C "$S" mux-sva-build VERILATOR="$V" MUX_SVA_WIDTH="$2" \
    MUX_SVA_OBJ="$P/variants/$1" MUX_SVA_BIND="$3" MUX_SVA_ASSERT="$4" > "$R/variant-$1-build.log" 2>&1
  echo "variant $1 build exit=$?" | tee -a "$R/variant-summary.txt"
}
: > "$R/variant-summary.txt"
build noassert-flag 8 "$BIND" ""
build bind-omitted 8 "$P/variants/empty_bind.sv" --assert
build bind-warning 8 "$P/variants/warn_bind.sv" --assert
build bind-instpath 8 "$P/variants/instpath_bind.sv" --assert
for v in noassert-flag bind-omitted; do
  if [ -x "$P/variants/$v/Vmux_sva" ]; then
    "$P/variants/$v/Vmux_sva" > "$R/variant-$v-positive.log" 2>&1
    echo "variant $v positive run exit=$?" | tee -a "$R/variant-summary.txt"
    "$P/variants/$v/Vmux_sva" +verilator+error+limit+1000 +scenario=single_beats +stimulus_fault=s1_flip_tdata \
      > "$R/variant-$v-fault.log" 2>&1
    echo "variant $v s1_flip_tdata run exit=$?" | tee -a "$R/variant-summary.txt"
  fi
done
