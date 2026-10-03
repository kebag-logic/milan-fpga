#!/bin/sh
# Usage: check_citations.sh <repo>
# Locates frame_ok_w and the KL_acmp_nvm_shadow instance at each lane revision, the texts the
# round-3 README/banner edits cite, and runs the round-3 assignment grep.
set -u
r=$1
for c in ddb3119d 53e1474b f4167536 c066dd83 5960d8fc 6ca4ade8; do
  w=$(git -C "$r" show "$c:hdl/aecp/KL_aecp_nvm_writer.sv" | grep -n 'logic frame_ok_w' | cut -d: -f1)
  s=$(git -C "$r" show "$c:hdl/top/protocol_processor_top.sv" | grep -n '^  KL_acmp_nvm_shadow #(' | cut -d: -f1)
  echo "$c frame_ok_w_decl=$w (assign ends $((w+3))) shadow_instance=$s"
done
echo "--- head: writer 549-552"; git -C "$r" show 6ca4ade8:hdl/aecp/KL_aecp_nvm_writer.sv | sed -n 549,552p
echo "--- head: top 2730"; git -C "$r" show 6ca4ade8:hdl/top/protocol_processor_top.sv | sed -n 2730p
echo "--- head: nvm_port README 97-101"; git -C "$r" show 6ca4ade8:tb/nvm_port/README.md | sed -n 97,101p
echo "--- head: nvm_port README 'not cut by' / 'still owed'"; git -C "$r" show 6ca4ade8:tb/nvm_port/README.md | grep -n -e 'not cut by' -e 'still owed'
echo "--- head: R21 banner 4247-4256"; git -C "$r" show 6ca4ade8:tb/pp_top/sim_main.cpp | sed -n 4247,4256p
echo "--- head: aecp_name_wr_o port / D3N phase / writer nchg_i"
git -C "$r" show 6ca4ade8:hdl/top/protocol_processor_top.sv | grep -n 'output logic *aecp_name_wr_o'
git -C "$r" show 6ca4ade8:tb/pp_top/sim_main.cpp | grep -n 'D3NamePhase{'
git -C "$r" show 6ca4ade8:hdl/aecp/KL_aecp_nvm_writer.sv | sed -n 129,132p
echo "--- head: 07 5.1 who persists what"; git -C "$r" show 6ca4ade8:docs/architecture/07_memory_maps.md | sed -n 558,565p
echo "--- assignment grep: git grep -nE -i 'not implemented yet|map stage|later stage' -- hdl tb"
git -C "$r" grep -nE -i "not implemented yet|map stage|later stage" 6ca4ade8 -- hdl tb; echo "rc=$?"
echo "--- same grep at 5960d8fc"
git -C "$r" grep -nE -i "not implemented yet|map stage|later stage" 5960d8fc -- hdl tb; echo "rc=$?"
echo "--- line-number citations into tb/pp_top/sim_main.cpp anywhere in the head tree"
git -C "$r" grep -nE 'sim_main(\.cpp)?`?:[0-9]{3,}' 6ca4ade8; echo "rc=$?"
echo "--- __LINE__ in tb/pp_top"; git -C "$r" grep -n '__LINE__' 6ca4ade8 -- tb/pp_top; echo "rc=$?"
