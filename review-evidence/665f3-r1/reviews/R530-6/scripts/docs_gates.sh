#!/usr/bin/env bash
# The docs and idiom gates R530-6 ran, as finally invoked (receipts/docs_gates.log
# also keeps the first, mis-invoked attempts: no pinned-renderer python for
# check_em_dash, and a --check flag the idiom gates do not take).
# Usage: docs_gates.sh <clone> <python with tools/markdown/requirements.txt installed>
set -u
C=$1; V=$2; cd "$C" || exit 2
for c in "python3 scripts/docs_check.py" \
         "$V scripts/check_em_dash.py --base 13e715136b0b7c8d9763e0b730d9709f2c9f5932" \
         "$V scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df" \
         "python3 scripts/check_doc_style.py" "$V scripts/gen_toc.py --check" \
         "python3 scripts/check_py_idiom.py" "python3 scripts/check_cpp_idiom.py" \
         "python3 scripts/check_hygiene.py --check" "python3 scripts/check_baremetal_only.py --check"; do
  $c > /dev/null 2>&1; echo "rc=$? :: $c"
done
