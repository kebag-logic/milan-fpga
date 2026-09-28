#!/bin/sh
# Markdown/documentation gates from .github/workflows/docs.yml, run in the pinned
# renderer environment (tools/markdown/requirements.txt, sha256 prefix 40cdefe08ebd).
# Usage: md_gates.sh <clone> <md venv> <base> <receipt dir>
set -u
clone=$1; venv=$2; base=$3; out=$4
cd "$clone"
PY="$venv/bin/python3"
for spec in "docs_check:scripts/docs_check.py" \
            "check_em_dash-base:scripts/check_em_dash.py --base $base" \
            "check_em_dash-selftest:scripts/check_em_dash.py --selftest" \
            "check_doc_style:scripts/check_doc_style.py" \
            "check_doc_style-selftest:scripts/check_doc_style.py --selftest" \
            "check_doc_paths:scripts/check_doc_paths.py" \
            "gen_toc-selftest:scripts/gen_toc.py --selftest" \
            "gen_toc-verify-anchors:scripts/gen_toc.py --verify-anchors" \
            "gen_toc-check:scripts/gen_toc.py --check" \
            "DOC_MAP-check:docs/DOC_MAP.gen.py --check" \
            "check_hygiene-check:scripts/check_hygiene.py --check" \
            "check_solution_docs:scripts/check_solution_docs.py"; do
  name=${spec%%:*}; cmd=${spec#*:}
  # shellcheck disable=SC2086
  "$PY" $cmd > "$out/md-$name.log" 2>&1
  echo "$name rc=$?"
done
git diff --check "$base" HEAD > "$out/md-git-diff-check.log" 2>&1; echo "git-diff-check rc=$?"
