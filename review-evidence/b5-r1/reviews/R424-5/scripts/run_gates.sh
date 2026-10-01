#!/usr/bin/env bash
# Run the documentation gates that apply to a docs-only change, in the pinned
# Markdown environment, from the review clone at the exact head.
# Usage: run_gates.sh <clone> <python-with-pinned-markdown-lock> <base-sha>
set -uo pipefail
clone=$1 py=$2 base=$3
cd "$clone"
echo "head: $(git rev-parse HEAD) tree: $(git rev-parse HEAD^{tree})"
echo "python: $("$py" -c 'import sys,cmarkgfm,html5lib; print(sys.version.split()[0], "cmarkgfm", cmarkgfm.__version__ if hasattr(cmarkgfm,"__version__") else "?", "html5lib", html5lib.__version__)')"
run() { local out; out=$("$@" 2>&1); local rc=$?; echo "rc=$rc :: $*"; printf '%s\n' "$out" | tail -n 4 | sed 's/^/    /'; }
run "$py" -B scripts/docs_check.py
run "$py" -B scripts/check_doc_style.py
run "$py" -B scripts/check_doc_style.py --selftest
run "$py" -B scripts/gen_toc.py --check
run "$py" -B scripts/gen_toc.py --verify-anchors
run "$py" -B scripts/gen_toc.py --selftest
run "$py" -B scripts/check_em_dash.py --base "$base"
run "$py" -B scripts/check_em_dash.py --selftest
run "$py" -B scripts/check_doc_paths.py
run "$py" -B scripts/check_feature_status.py
run "$py" -B scripts/check_feature_status.py --self-test
run "$py" -B scripts/check_baremetal_only.py --check
run "$py" -B scripts/ci_scope.py --selftest
run git diff --check "$base" HEAD
run git diff --check e216dfe4f0cab7b0c7352d7973acb4d33c157f70 HEAD
echo "status after: $(git status --porcelain | wc -l) changed path(s)"
