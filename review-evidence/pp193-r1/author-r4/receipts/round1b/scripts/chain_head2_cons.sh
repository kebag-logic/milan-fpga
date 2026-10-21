#!/usr/bin/env bash
# the scratch parent's gitlink at the final head (commit 3 changes only
# tb/pp_top/gsi_mutants.py and tb/pp_top/README.md): the consumer gates that
# read processor source text other than RTL
S=<scratch>
P=$S/parent
PP=$P/protocol-processor
H=$(cat $S/head2.sha)
[ "$(git -C $P rev-parse --show-toplevel)" = "$P" ] || exit 3
[ "$(git -C $PP rev-parse --show-toplevel)" = "$PP" ] || exit 3
git -C $PP clean -fdXq || exit 4
git -C $PP fetch -q <lane> "$H" || exit 4
git -C $PP checkout -q "$H" || exit 5
[ "$(git -C $PP rev-parse HEAD)" = "$H" ] || exit 6
[ -z "$(git -C $PP status --porcelain --ignored)" ] || exit 6
git -C $P add protocol-processor || exit 7
git -C $P commit -q -m "scratch: protocol-processor gitlink at head ${H:0:8}" || exit 7
bash $S/scripts/run_consumers.sh $S/rec/head2-cons cpp_idiom py_idiom rtl_source_lists pp_srcs port_contracts measure_naming measure_test_evidence docs_check sh_idiom hygiene sv_idiom submodule_docs baremetal_only soc_sources todo_ownership lint_rtl bdd
echo done > $S/rec/HEAD2-CONS.done
