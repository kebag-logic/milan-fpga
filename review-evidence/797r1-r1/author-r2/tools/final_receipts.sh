#!/bin/sh
# Rerun both reviewers' simulations and plants, the probes and the SoC check on the lane's committed head.
# Usage: final_receipts.sh <lane> <receipts> <tools> <scratch> <venv python> <r753 scripts> <r754 scripts> <export>
L=$1; O=$2; T=$3; W=$4; PY=$5; R3=$6; R4=$7; EXP=$8
cd "$L" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
S=$W/sim; rm -rf "$S"; mkdir -p "$S/r753" "$S/r754/sim" "$S/r754/receipts" "$O/sim" "$O/plants" "$O/behave" "$O/export"
sh "$R3/build_oracle.sh" "$L" "$S/r753" /usr/bin/verilator "$S/r753/oracle_raw.txt" > "$O/sim/r753_build.log" 2>&1; echo $? > "$O/sim/r753_build.rc"
python3 -I "$R3/compare_oracle.py" docs/reference/REGISTER_MAP.md "$S/r753/oracle_raw.txt" > "$O/sim/r753_oracle_compare.txt" 2>&1; echo $? > "$O/sim/r753_oracle_compare.rc"
cp "$S/r753/oracle_raw.txt" "$O/sim/r753_oracle_raw.txt"
S4=$S/r754
python3 -I "$R4/gen_wrapper.py" "$L/hdl/common/csr/milan_csr.sv" "$S4/sim/tb_top.sv" "$S4/sim/portmap.json" > "$O/sim/r754_wrapper.log" 2>&1
python3 -I -c "
import json,sys
m=json.load(open(sys.argv[1]));hs={'i_lctx_wr_rdy','i_tctx_wr_rdy','i_lctx_rd_valid','i_tctx_rd_valid','i_lctx_snap_ok','i_tctx_snap_ok','i_ptp_tod_valid','i_pp_ack'}
open(sys.argv[2],'w').write(''.join(f'{n} {p} {w} {int(n in hs)}\n' for n,(p,w) in m['inputs'].items()))" "$S4/sim/portmap.json" "$S4/sim/ports.txt"
ib=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['in_bits'])" "$S4/sim/portmap.json")
ob=$(python3 -I -c "import json,sys;print(json.load(open(sys.argv[1]))['out_bits'])" "$S4/sim/portmap.json")
verilator --cc --exe --build -j 8 -O2 -Wno-fatal -Wno-lint -Wno-style --top-module tb_top -I"$L/hdl/common/csr" -I"$L/configs/generated/endstation_ax7101_1x1_tdm8" -CFLAGS "-DIN_BITS=$ib -DOUT_BITS=$ob -O2" --Mdir "$S4/sim/obj" "$S4/sim/tb_top.sv" "$L/hdl/common/csr/milan_csr.sv" "$R4/sim_main.cpp" > "$O/sim/r754_build.log" 2>&1; echo $? > "$O/sim/r754_build.rc"
for m in reset word input directed; do "$S4/sim/obj/Vtb_top" $m "$S4/sim/ports.txt" > "$S4/receipts/sim_$m.txt"; done
"$S4/sim/obj/Vtb_top" bit "$S4/sim/ports.txt" > "$S4/sim/sim_bit.txt"
python3 -I "$R4/compare_page.py" docs/reference/REGISTER_MAP.md "$S4/receipts" "$S4/sim/sim_bit.txt" "$S4/sim/portmap.json" > "$O/sim/r754_compare_page.txt" 2>&1; echo $? > "$O/sim/r754_compare_page.rc"
python3 -I "$R4/attrib.py" docs/reference/REGISTER_MAP.md "$S4/receipts" "$S4/sim/sim_bit.txt" "$S4/sim/portmap.json" "$R4" > "$O/sim/r754_attribution.txt" 2>&1; echo $? > "$O/sim/r754_attribution.rc"
cp "$S4/receipts/sim_reset.txt" "$O/sim/r754_sim_reset.txt"; cp "$S4/receipts/sim_directed.txt" "$O/sim/r754_sim_directed.txt"
P=$W/plants; rm -rf "$P"; mkdir -p "$P/r753" "$P/r754" "$P/wp"
"$PY" -B "$R3/plant_probes.py" "$L" "$P/r753" 8 > "$O/plants/r753_plant_probes.txt" 2>&1; echo $? > "$O/plants/r753_plant_probes.rc"
"$PY" -B "$T/r754_mutants_paths.py" "$L" "$P/r754" "$PY" > "$O/plants/r754_mutants.tsv" 2>&1; echo $? > "$O/plants/r754_mutants.rc"
"$PY" -B "$R3/write_probe.py" "$L" "$P/wp" > "$O/plants/r753_write_probe.txt" 2>&1; echo $? > "$O/plants/r753_write_probe.rc"
python3 -I "$T/note_as_paragraph_probe.py" "$L" > "$O/plants/r753_note_as_paragraph.txt" 2>&1; echo $? > "$O/plants/r753_note_as_paragraph.rc"
python3 -I "$R3/row_audit.py" docs/reference/REGISTER_MAP.md > "$O/plants/r753_row_audit.txt" 2>&1; echo $? > "$O/plants/r753_row_audit.rc"
"$PY" -B "$T/memory_map_plant.py" "$L" "$PY" > "$O/plants/memory_map_plants.txt" 2>&1; echo $? > "$O/plants/memory_map_plants.rc"
cat docs/reference/REGISTER_MAP.md docs/design/CSR_REGISTER_NOTES.md scripts/register_descriptions.json > "$W/new_both.txt"
git show 1e80128f:docs/reference/REGISTER_MAP.md > "$W/old_page.md"
python3 -I "$T/survival.py" "$W/old_page.md" "$W/new_both.txt" > "$O/survival.txt" 2>&1; echo $? > "$O/survival.rc"
"$PY" -B scripts/gen_register_reference.py --check --soc-from "$EXP" > "$O/export/soc_from_check.txt" 2>&1; echo $? > "$O/export/soc_from_check.rc"
cp "$EXP/csr.csv" "$EXP/aem_desc.json" "$O/export/"
(cd tests && $WORKSPACE_HOME/.local/bin/behave --no-capture -f plain features/counters_contract_milan.feature > "$O/behave/counters_contract_milan.txt" 2>&1; echo $? > "$O/behave/counters_contract_milan.rc")
git status --short > "$O/lane_status_after.txt"
echo DONE
