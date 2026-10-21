#!/usr/bin/env bash
# usage: chain_final.sh A|B. Final head 324ac9a7, two runners side by side,
# each campaign driver at --jobs 2, each runner in its own clean clone.
# A: the gates that read the docs and READMEs (the head-gates records at
#    65d39b0c stand for the others: 324ac9a7 changes only tb/srp_top/README.md
#    and one required tag in tb/srp_top/mutants.py), then srp_top, acmp,
#    dispatch, gsi, elab_mutants, name_wr in final-pp-c.
# B: d3, notify, aecp, ctr, name_state in final-pp-c2.
S=<scratch>/r3
case $1 in
  A) bash $S/scripts/run_gates.sh $S/final-pp $S/rec/final-gates lint_hdl gen_matrix make_check
     bash $S/scripts/run_camps.sh $S/final-pp-c $S/rec/final-camps 2 srp_top acmp dispatch gsi elab_mutants name_wr
     echo done > $S/rec/final-A.done ;;
  B) bash $S/scripts/run_camps.sh $S/final-pp-c2 $S/rec/final-camps2 2 d3 notify aecp ctr name_state
     echo done > $S/rec/final-B.done ;;
esac
