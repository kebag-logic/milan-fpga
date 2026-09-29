#!/usr/bin/env bash
# Read-only public check of the parent files the combined pin-adoption edits target, at a
# parent ref (default: milan-fpga dev 79c36963). Needs an authenticated `gh`.
set -uo pipefail
ref=${1:-79c36963660c10e4c1c11a744fb5bff41a552b8b}
R=repos/kebag-logic/milan-fpga
raw() { gh api -H 'Accept: application/vnd.github.raw' "$R/contents/$1?ref=$ref"; }
echo "parent ref $ref; protocol-processor gitlink: $(gh api "$R/contents/protocol-processor?ref=$ref" --jq .sha)"
t=$(mktemp -d)
for p in tb/verilator/milan_dp/sim_crf_licence.cpp tb/verilator/milan_dp/README.md \
         hdl/milan/KL_pp_shadow.sv tb/verilator/nvm_cosim/cosim_top.sv tb/verilator/milan_dp/sim_gmstep.cpp; do
  raw "$p" > "$t/$(basename $p)"; echo "blob $(git hash-object "$t/$(basename $p)") $p"
done
echo "--- C1 section 4: sim_crf_licence.cpp:953,956 and README :443, :528-530"
sed -n '953p;956p' "$t/sim_crf_licence.cpp"; sed -n '443p;528,530p' "$t/README.md"
echo "--- #132 list: new top ports connected in KL_pp_shadow.sv? (count of each name)"
for n in restore_closed_o restore_rb_o rs_cause_o restore_cause_o d3_unflushed_o NVM_RS_AGG_CYC_P NVM_RETRY_BACKOFF_CYC_P; do
  echo "$n $(grep -c "$n" "$t/KL_pp_shadow.sv")"; done
echo "--- #132 list: cosim_top.sv rs_agg_i / wr_chg / RETRY_BACKOFF_CYC_P"
for n in rs_agg_i wr_chg RETRY_BACKOFF_CYC_P; do echo "$n $(grep -c "$n" "$t/cosim_top.sv")"; done
echo "--- #132 list: sim_gmstep.cpp starts the restore walk (PP_CTRL[1])?"
grep -n -i -E 'restore|walk' "$t/sim_gmstep.cpp" | head -5 || true
echo "(no match above means the harness does not start the walk)"
rm -rf "$t"
