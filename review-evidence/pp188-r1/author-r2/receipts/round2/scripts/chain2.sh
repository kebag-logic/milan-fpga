#!/usr/bin/env bash
# Round 2: after the base processor records finish in the submodule, run the
# scratch parent's consumer gates and OOC gates with the gitlink staged at the
# round-2 base, then at the round-2 head. ooc_selftest runs in the OOC pass,
# where the ROM-digest ledger row it needs is recorded (scratch tree only).
set -u
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
BASE=cb8bab044d98a89d8c4eb2b56bd81835e6fc5d48
HEAD_SHA=$(cat $S/head2.sha)
GATES="cpp_idiom py_idiom rtl_source_lists pp_srcs port_contracts measure_naming
measure_test_evidence docs_check sh_idiom hygiene sv_idiom submodule_docs
baremetal_only lint_rtl bdd yosys_elaborate test_builder xvlog pp_shadow
nvm_cosim_lint nvm_cosim_quick milan_dp_render milan_dp"
until [ -f $S/rec2/base-gates/ALL.done ] && [ -f $S/rec2/base-camps/ALL.done ]; do sleep 60; done
stage() {
  [ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
  [ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
  git -C $PP clean -fdXq || exit 4
  git -C $PP fetch -q <lane> 188-189-listener || exit 4
  git -C $PP checkout -q "$1" || exit 5
  [ "$(git -C $PP rev-parse HEAD)" = "$1" ] || exit 6
  [ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
  git -C $P add protocol-processor || exit 7
}
stage $BASE
bash $S/scripts/run_consumers.sh $S/rec2/cons-base $GATES
bash $S/scripts/run_ooc.sh $S/rec2/ooc-base
stage "$HEAD_SHA"
bash $S/scripts/run_consumers.sh $S/rec2/cons-head $GATES
bash $S/scripts/run_ooc.sh $S/rec2/ooc-head
echo done > $S/rec2/CHAIN.done
