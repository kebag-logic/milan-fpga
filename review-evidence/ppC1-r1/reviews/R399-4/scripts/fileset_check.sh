#!/usr/bin/env bash
# Read-only public re-derivation of the combined-edit parent file set named in the manager's
# comment 5890073527: PR #132's consolidated list + PR #133 section 4 crflic edit + the gitlink.
# Needs an authenticated `gh` (GET requests only). Usage: fileset_check.sh <packet-dir>
set -uo pipefail
pk=${1:?packet dir}
ref=79c36963660c10e4c1c11a744fb5bff41a552b8b
R=repos/kebag-logic/milan-fpga
raw() { gh api -H 'Accept: application/vnd.github.raw' "$R/contents/$1?ref=$ref"; }
echo "== live dev head now: $(gh api $R/branches/dev --jq .commit.sha)"
echo "== parent ref $ref; protocol-processor gitlink: $(gh api "$R/contents/protocol-processor?ref=$ref" --jq .sha)"

echo "== file names cited in PR #132 'Parent-visible for pin adoption: rounds 1-6, consolidated'"
awk '/^\*\*Parent-visible for pin adoption: rounds 1-6, consolidated\*\*/{f=1} /^\*\*Evidence at/{f=0} f' \
  "$pk/receipts/pr132-body.md" > "$pk/scratch/pr132-consolidated.md"
grep -oE '`[A-Za-z0-9_./-]+\.(sv|cpp|py|c|h|hpp)`' "$pk/scratch/pr132-consolidated.md" | sort | uniq -c

# Mapping of each named edit to its parent path (the 13 files of comment 5890073527) with a
# marker that must exist at the ref to show the edit target is that file.
while read -r path marker why; do
  f="$pk/scratch/$(echo "$path" | tr / _)"
  if raw "$path" > "$f" 2>/dev/null; then
    n=$(grep -c -E -- "$marker" "$f")
    echo "EXISTS blob $(git hash-object "$f") $path | marker /$marker/ x$n | $why"
  else echo "MISSING $path | $why"; fi
done <<'EOF'
hdl/milan/KL_pp_shadow.sv KL_protocol_processor_top|protocol_processor_top #132:ports/params/glue
scripts/measure_test_evidence.py DUT_READER_DISPOSITIONS #132:evidence-classifier
tb/verilator/milan_dp/sim_aclk.cpp start_the_boot_restore_walk #132:image-less-aclk-walk-wait
tb/verilator/milan_dp/sim_ax1x1gptp.cpp configure #132:ax1x1gptp-walk
tb/verilator/milan_dp/sim_crf_licence.cpp LeaveAll.MRPDUs #133-s4:crflic>=3
tb/verilator/milan_dp/sim_gmstep.cpp PP_CTRL|pp_ctrl #132:gmstep-walk
tb/verilator/milan_dp/sim_gptp.cpp PP_CTRL|pp_ctrl #132:gptp-walk
tb/verilator/milan_dp/sim_main.cpp PP_CTRL|pp_ctrl|restore #132:image-less-main/nolpf/ax1x1
tb/verilator/milan_dp/sim_nxn.cpp prove_read_descriptor_degrades_with_no_descriptor_memory #132:nxn-legs
tb/verilator/milan_dp_render/sim_tdm8_render.cpp T8 #132:render-T8-REMOVE
tb/verilator/nvm_cosim/cosim_cases.cpp B1|B4 #132:B1-B4-window
tb/verilator/nvm_cosim/cosim_top.sv KL_acmp_nvm_shadow #132:cosim_top-pins
tb/verilator/pp_shadow/sim_main.cpp K10|K12|M2|P3 #132:pp_shadow-phases
EOF
echo "== crflic lines at the ref (C1 section 4 edit target)"
sed -n '953p;956p' "$pk/scratch/tb_verilator_milan_dp_sim_crf_licence.cpp"
echo "== locate files the consolidated list names that are not in the 13 (search by basename)"
gh api "$R/git/trees/$ref?recursive=1" --jq '.tree[].path' > "$pk/scratch/parent-tree.txt"
for b in measure_test_evidence.py sim_tdm8_render.cpp cosim_cases.cpp sim_main.cpp KL_pp_nvm_mgr_arb.sv; do
  echo "$b -> $(grep -E "(^|/)$b\$" "$pk/scratch/parent-tree.txt" | tr '\n' ' ')"; done
echo "== consumer-set build files under tb/verilator/nvm_cosim, milan_dp_render (which cpp holds B1/T8)"
grep -E '^tb/verilator/(nvm_cosim|milan_dp_render)/[^/]+\.(cpp|c|sv|py)$' "$pk/scratch/parent-tree.txt"
echo "--- B1-B4 give-up window lives in cosim_cases.cpp (erase_fault_case), at the ref"
sed -n '480,500p' "$pk/scratch/tb_verilator_nvm_cosim_cosim_cases.cpp"
echo "--- T8 REMOVE lives in sim_tdm8_render.cpp, at the ref"
sed -n '2080,2090p' "$pk/scratch/tb_verilator_milan_dp_render_sim_tdm8_render.cpp"
echo "--- milan_dp/README.md at the ref: passages #132's list changes (retired [AECP] degrade arm, walk-starting harnesses)"
raw tb/verilator/milan_dp/README.md > "$pk/scratch/milan_dp_README.md"
echo "blob $(git hash-object "$pk/scratch/milan_dp_README.md") tb/verilator/milan_dp/README.md"
sed -n '633,637p;869,882p' "$pk/scratch/milan_dp_README.md"
