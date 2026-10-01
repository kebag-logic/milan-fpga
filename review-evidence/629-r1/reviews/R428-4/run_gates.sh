#!/bin/sh
# Reviewer gate run for PR #631 at the exact head. Usage: run_gates.sh <clone> <md-venv> <outdir>
C="$1"; V="$2"; O="$3"
export PYTHONDONTWRITEBYTECODE=1
cd "$C" || exit 2
git rev-parse HEAD > "$O/head.txt"
"$V/bin/python" -m pip freeze --all > "$O/md_venv_freeze.txt" 2>&1
run() { n="$1"; shift; "$@" > "$O/$n.out" 2>&1; echo $? > "$O/$n.rc"; }
run docs_check            "$V/bin/python" scripts/docs_check.py
run check_doc_style       "$V/bin/python" scripts/check_doc_style.py
run gen_toc_check         "$V/bin/python" scripts/gen_toc.py --check
run gen_toc_verify_anchors "$V/bin/python" scripts/gen_toc.py --verify-anchors
run check_em_dash         "$V/bin/python" scripts/check_em_dash.py --base d4dd742679b902b2bc5eedf89d525066d59aafbb
run check_doc_paths       "$V/bin/python" scripts/check_doc_paths.py
run check_entity_shape    python3 scripts/check_entity_shape.py
run diff_check_worktree   git diff --check
run diff_check_base       git diff --check d4dd742679b902b2bc5eedf89d525066d59aafbb 1bdd68957dd1357645c500014002b1e5a115864c
run diff_check_round4     git diff --check a463a1deb9d63614e8bd2134ccd7b2cd541c72ed 1bdd68957dd1357645c500014002b1e5a115864c
git status --porcelain --ignored=matching > "$O/status_after.txt"
