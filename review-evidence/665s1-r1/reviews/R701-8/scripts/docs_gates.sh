#!/bin/bash
# The docs workflow's check-mode gates that read files this delta changes (markdown, Python), at the head.
. "$(dirname "$0")/env.sh"
cd "$CHECKOUT" && echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain | wc -l)"
for g in "scripts/docs_check.py" "scripts/check_doc_paths.py" "scripts/check_doc_style.py" \
         "scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f" \
         "scripts/check_py_idiom.py" "scripts/check_hygiene.py --check" "scripts/check_baremetal_only.py --check" \
         "scripts/check_todo_ownership.py" "scripts/check_feature_status.py"; do
  out=$(/usr/bin/python3 -B $g 2>&1); rc=$?
  echo "== $g rc=$rc"; echo "$out" | tail -2
done
git diff --check e76a755afc0536453161e3cd33f6f4d2dcd7641f HEAD; echo "== git diff --check rc=$?"
