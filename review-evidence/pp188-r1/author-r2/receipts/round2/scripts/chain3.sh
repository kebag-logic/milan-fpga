#!/usr/bin/env bash
# Round 2, head only (the base consumer and OOC records stand): stage the
# round-2 head as the scratch parent's gitlink and run every consumer gate,
# then the OOC gates (ooc_selftest there, beside its ledger row).
set -u
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
HEAD_SHA=$(cat $S/head2.sha)
GATES="cpp_idiom py_idiom rtl_source_lists pp_srcs port_contracts measure_naming
measure_test_evidence docs_check sh_idiom hygiene sv_idiom submodule_docs
baremetal_only lint_rtl bdd yosys_elaborate test_builder xvlog pp_shadow
nvm_cosim_lint nvm_cosim_quick milan_dp_render milan_dp"
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP clean -fdXq || exit 4
git -C $PP fetch -q <lane> 188-189-listener || exit 4
git -C $PP checkout -q "$HEAD_SHA" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$HEAD_SHA" ] || exit 6
[ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
git -C $P add protocol-processor || exit 7
bash $S/scripts/run_consumers.sh $S/rec2/cons-head $GATES
bash $S/scripts/run_ooc.sh $S/rec2/ooc-head
echo done > $S/rec2/CHAIN.done
