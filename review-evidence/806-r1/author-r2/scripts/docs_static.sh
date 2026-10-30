#!/usr/bin/env bash
# #806 round 2: the static gates the wording commit touches (CHANGELOG.md, docs/design/AREA_BUDGET.md,
# docs/reference/SUBMODULES.md), one at a time in a clean clone at <rev>; each line of table.txt is "<rc> <seconds>s <name>: <command>".
# usage: docs_static.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/806-a701b; C=$X/clone-static-${rev:0:8}; O=$X/r/static-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"
git rev-parse HEAD > "$O/head.txt"; git submodule status > "$O/submodules.txt"
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table.txt"; }
run doc_style python3 scripts/check_doc_style.py
MD=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3   # the pinned Markdown renderer (tools/markdown/requirements.txt)
run toc_selftest $MD scripts/gen_toc.py --selftest
run toc_anchors $MD scripts/gen_toc.py --verify-anchors
run toc_check $MD scripts/gen_toc.py --check
run check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run submodule_docs python3 scripts/check_submodule_docs.py
run gptp_docs python3 scripts/check_gptp_docs.py --with-submodule
run gptp_docs_plain python3 scripts/check_gptp_docs.py
run hygiene python3 scripts/check_hygiene.py --check
run todo_ownership python3 scripts/check_todo_ownership.py
run feature_status python3 scripts/check_feature_status.py
run docs_check python3 scripts/docs_check.py
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo STATIC-DONE >> "$O/table.txt"
