#!/usr/bin/env bash
# Round-2 out-of-tree proofs at head c5afc0a4: router equivalence (base 08ae0013
# against head) at five shapes and its mutants; the occupancy induction at three
# shapes and its mutants. One line per run in rc.txt; three runs at a time.
P=<data>/tmp/pp181-a635/r2/proofs; cd $P
SKIP="pend_after_w base_w gnt_found_w gnt_src_w"
S1="-set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1"
export EQUIV_SKIP="pend_after_w base_w gnt_found_w gnt_src_w"   # the router's changed nets
job() {   # job <name> <command...>
  local n=$1; shift; local t0=$SECONDS rc=0
  timeout 7200 "$@" > "$n.out" 2>&1 || rc=$?
  echo "$n rc=$rc ($((SECONDS - t0))s)" >> rc.txt
}
export -f job; export SKIP S1 P
: > rc.txt
{
  for n in 1 5 8 16 29; do
    echo "job router-$n ./equiv.sh router-$n $P/src/base_KL_pp_event_router.sv $P/src/head_KL_pp_event_router.sv KL_pp_event_router 2 \"\" -- -set N_SRC_P $n"
  done
  for m in R1-base-always-ptr R2-presented-not-removed R3-load-ignores-ack R4-select-reloads-always R5-no-grant-clears; do
    echo "job m-$m ./equiv.sh m-$m $P/src/base_KL_pp_event_router.sv $P/mutants/$m.sv KL_pp_event_router 2 \"\" -- -set N_SRC_P 8"
  done
  echo "job inv-head-1x1 ./inv.sh head-1x1 $P/src/head_KL_aecp_notify.sv \$S1"
  for m in N1-pop-keeps-set N2-push-unseen N3-pop-one-late N4-cleared-beside-push N5-not-busy N6-reset-set N7-pop-clears; do
    echo "job inv-m-$m ./inv.sh m-$m $P/mutants/$m.sv \$S1"
  done
  echo "job inv-head-default ./inv.sh head-default $P/src/head_KL_aecp_notify.sv"
  echo "job inv-head-2if-ident ./inv.sh head-2if-ident $P/src/head_KL_aecp_notify.sv -set N_IF_P 2 -set EN_IDENTIFY_NOTIF_P 1"
} > jobs.txt
xargs -d '\n' -P 3 -I{} bash -c '{}' < jobs.txt
echo DONE >> rc.txt
