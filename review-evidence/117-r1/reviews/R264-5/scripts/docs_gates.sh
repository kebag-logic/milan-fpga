#!/usr/bin/env bash
# Focused documentation gates at the exact head (run from the checkout root).
set -u
export PYTHONDONTWRITEBYTECODE=1
base=${1:-ede8d48ecd7c7f589a14b957951f040d92c99c70}
for cmd in "scripts/docs_check.py" "scripts/check_em_dash.py --base $base" "scripts/check_doc_style.py" \
           "scripts/check_gptp_docs.py" "scripts/check_gptp_docs.py --with-submodule" \
           "scripts/check_baremetal_only.py --check" "docs/DOC_MAP.gen.py --check" \
           "scripts/check_feature_status.py --self-test" "scripts/gen_toc.py" "scripts/gen_toc.py --verify-anchors"; do
  echo "=== python3 $cmd"
  out=$(timeout 300 python3 $cmd 2>&1); rc=$?
  printf '%s\n' "$out" | tail -3
  echo "rc=$rc"
done
