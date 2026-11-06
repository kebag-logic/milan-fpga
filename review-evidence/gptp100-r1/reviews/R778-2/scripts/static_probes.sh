#!/bin/sh
# Static probes for FPGA-gPTP PR #101 round 2 (head 84fd227).
# usage: static_probes.sh <clone at 84fd227> <out dir>
# Read-only on the clone except for the regenerated ROM images, which are
# compared with git diff and then restored with git checkout.
set -u
R=$1; O=$2; mkdir -p "$O"; cd "$R" || exit 2
H=84fd22781c95f7b7e65d7d18c99a5ed49a68e11c
run() { n=$1; shift; { echo "\$ $*"; "$@"; echo "rc=$?"; } > "$O/$n.log" 2>&1; }

run 01-head git rev-parse HEAD HEAD^{tree}
# 1. Replay the merge and compare it with the recorded merge 1615187.
run 02-merge-tree sh -c 'T=$(git merge-tree --write-tree 3e3f041 5184fb3 | head -1); echo auto-tree=$T; git diff --stat $T 1615187; git diff $T 1615187'
run 03-merge-msg git log -1 --format='%H %P%n%an <%ae>%n[%B]' 1615187
run 04-delta-stat sh -c 'git diff --stat 3e3f041 84fd227; echo ---post-merge; git diff --stat 1615187 84fd227; echo ---hdl-tb-vs-main; git diff --stat 5184fb3 84fd227 -- hdl tb'
run 05-hdl-tb-unchanged-by-merge sh -c 'for p in hdl/top hdl/ucpu hdl/common hdl/ucode tb/verilator/engine/mutants.py tb/verilator/engine/p100_mutants.py tb/verilator/engine/Makefile; do git diff --quiet 3e3f041 1615187 -- $p && echo "same-as-3e3f041 $p" || echo "DIFF $p"; done; for p in hdl/wire tb/verilator/parser scripts/check_docs.py scripts/check_docs_selftest.py; do git diff --quiet 5184fb3 84fd227 -- $p && echo "same-as-main $p" || echo "DIFF $p"; done'
# 2. Docs gate and source-evidence checker at head.
run 06-make-docs make docs
run 07-source-evidence python3 scripts/check_source_evidence.py
run 08-anchor-lines sh -c 'grep -o "\.\./hdl/[^)#]*#L[0-9]*" docs/SOURCE_EVIDENCE.md | sort -u | while read a; do f=${a#../}; f=${f%%#*}; l=${a##*#L}; printf "%s:%s: " "$f" "$l"; sed -n "${l}p" "$f"; done'
# 3. Help text and ROM images unchanged by the help edit.
run 09-help-head python3 -I hdl/ucode/gen_gptp_ucode.py --help
mkdir -p "$O/prev"; git show 1615187:hdl/ucode/gen_gptp_ucode.py > "$O/prev/gen_gptp_ucode.py"
run 10-help-merge python3 -I "$O/prev/gen_gptp_ucode.py" --help
run 11-help-diff sh -c "tail -n +2 '$O/09-help-head.log' > '$O/h1'; tail -n +2 '$O/10-help-merge.log' > '$O/h2'; diff '$O/h1' '$O/h2' && echo help-identical"
run 12-rom-regen sh -c 'make -C tb/verilator/engine -B gptp_ucode.hex >/dev/null && git diff --exit-code --stat && echo rom-matches-committed'
run 13-diff-check git diff --check 5184fb3 84fd227
run 14-status git status --porcelain
