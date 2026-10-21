#!/usr/bin/env bash
# final head 7b424cdf (commit 5 changes only tb/srp_top/README.md): the
# processor gates that read it, then the scratch parent's gitlink at it and the
# parent consumer gates that read processor text other than RTL
S=<scratch>/r2
P=$S/parent
PP=$P/protocol-processor
LANE=<lane>
H=7b424cdfe111a426f00517ff471246b4b9650726
rm -rf $S/final-pp
git clone -q $LANE $S/final-pp && git -C $S/final-pp checkout -q $H || exit 2
[ -z "$(git -C $S/final-pp status --porcelain --ignored)" ] || exit 2
bash $S/scripts/run_gates.sh $S/final-pp $S/rec/final-gates lint_hdl gen_matrix make_check
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP fetch -q $LANE '+refs/heads/*:refs/remotes/lane/*' || exit 4
git -C $PP clean -fdxq || exit 4
git -C $PP checkout -q "$H" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$H" ] || exit 6
[ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
git -C $P add protocol-processor || exit 7
git -C $P commit -q -m "scratch: protocol-processor gitlink at final head ${H:0:8}" || exit 7
bash $S/scripts/run_consumers.sh $S/rec/final-cons cpp_idiom py_idiom rtl_source_lists pp_srcs port_contracts measure_naming measure_test_evidence docs_check sh_idiom hygiene sv_idiom submodule_docs baremetal_only soc_sources todo_ownership lint_rtl bdd
echo done > $S/rec/FINAL.done
