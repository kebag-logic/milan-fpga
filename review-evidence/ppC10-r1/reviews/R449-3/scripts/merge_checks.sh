#!/usr/bin/env bash
# R449-3: round-3b merge checks, read-only against the review clone.
#  1. replay the merge (git merge-tree) and compare the replay with the head
#  2. the PR's RTL diff against main, and the merge's RTL diff against b6f17f2
#     compared with P1's RTL diff
#  3. the top's sorted non-blank line multiset, main vs merge
#  4. the text at every cited line into a file both sides changed, and every
#     KL_pp_nvm_port.sv citation
# usage: merge_checks.sh <clone>
set -u
cd "$1" || exit 2
H=39298e03aa53d5f82c7485b8d12d2b69a47b0d55
echo "== 1. merge replay (b6f17f2 + c4cb84f)"
out=$(git merge-tree --write-tree --name-only b6f17f2 c4cb84f); echo "$out" | sed 's/^/   /'
t=$(echo "$out" | head -1)
echo "   replay tree vs head, files differing: $(git diff --name-only "$t" $H | tr '\n' ' ')"
git diff "$t" $H | sed 's/^/   /'
echo "== 2. RTL sides"
echo "   c4cb84f..head hdl files: $(git diff --name-only c4cb84f $H -- hdl | tr '\n' ' ')"
if diff <(git diff b6f17f2 $H -- hdl | grep '^[+-]' | grep -v '^+++\|^---') \
        <(git diff f4167536 c4cb84f -- hdl | grep '^[+-]' | grep -v '^+++\|^---') >/dev/null; then
  echo "   merge's hdl diff vs b6f17f2 == P1's hdl diff (f4167536..c4cb84f): EQUAL"
else echo "   merge's hdl diff vs b6f17f2 != P1's hdl diff: DIFFERENT"; fi
echo "== 3. protocol_processor_top.sv sorted non-blank line multiset, c4cb84f vs head"
f=hdl/top/protocol_processor_top.sv
diff <(git show c4cb84f:$f | grep -v '^\s*$' | sort) <(git show $H:$f | grep -v '^\s*$' | sort) | sed 's/^/   /'
echo "== 4. cited lines at the head"
show() { echo "   $1:$2"; git show "$H:$1" | sed -n "${2/-/,}p" | sed 's/^/      | /'; }
show hdl/aecp/KL_aecp_nvm_writer.sv 549-552
show hdl/top/protocol_processor_top.sv 2731-2731
show hdl/packet_engine/KL_pp_nvm_port.sv 244-255
show hdl/packet_engine/KL_pp_nvm_port.sv 350-354
show hdl/packet_engine/KL_pp_nvm_port.sv 446-449
show hdl/packet_engine/KL_pp_nvm_port.sv 376-376
show hdl/packet_engine/KL_pp_nvm_port.sv 390-390
show hdl/packet_engine/KL_pp_nvm_port.sv 196-200
show hdl/acmp/KL_pp_acmp_listener.sv 344-347
show hdl/aecp/KL_aecp_notify.sv 557-557
show hdl/packet_engine/KL_pp_originator.sv 194-194
show hdl/packet_engine/KL_pp_rx_validator.sv 383-383
echo "   every explicit citation into those files in the tree:"
git grep -nE '(protocol_processor_top\.sv|KL_pp_nvm_port\.sv|KL_aecp_nvm_writer\.sv)`?:[0-9]+' $H -- . | sed "s/^$H://; s/^/      /"
