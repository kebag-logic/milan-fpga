#!/usr/bin/env bash
# Print the processor source lines behind the three round-2 documentation claims
# at the old pin b2db3a97 and the new pin 631eeb34. Usage: claim_sources.sh <clone>
set -u
pp="$1/protocol-processor"; E=hdl/aecp/KL_aecp_engine.sv; T=hdl/top/protocol_processor_top.sv
show() { echo "--- $1:$2 lines $3"; git -C "$pp" show "$1:$2" | sed -n "$3p"; }
echo "== claim 1: response-memory failure of a non-AEM command (A_ALLOC, A_WR)"
show b2db3a97 $E 3549,3585
show 631eeb34 $E 1743,1753
show 631eeb34 $E 3756,3810
echo "--- PR #140 commits (ancestor of merge 03c842a, not of its first parent)"
for c in 9f0299a a2d2a24; do
  git -C "$pp" merge-base --is-ancestor $c 03c842a && ! git -C "$pp" merge-base --is-ancestor $c 03c842a^1 \
    && echo "$c: introduced by merge 03c842a (PR #140): $(git -C "$pp" log -1 --format=%s $c | cut -c1-120)"
done
echo "== claim 2: deadline answer (refusal stands; an effect answers for itself)"
show 631eeb34 $E 1722,1738
echo "== claim 3: ADPDU index fallback and the D3 roll-back clear"
show 631eeb34 $T 228,233
show 631eeb34 $T 1852,1862
show 631eeb34 $E 1607,1610
show 631eeb34 $E 1912,1928
echo "--- parent binding"
git -C "$1" grep -n "o_adp_current_config  = adp_idx0\|current_cfg_i     (cfg_adp_current_config)" -- hdl
echo "== KL_pp_shadow #80 qualifier: processor references to its issue #80"
git -C "$pp" grep -n "manager ruling, processor #80\|the ruling on issue #80" -- docs | cut -c1-200
