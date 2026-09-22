#!/usr/bin/env bash
# The docs-check job's pre-submodule steps (.github/workflows/docs.yml:51-123)
# that this host can run, executed at the exact head in the Git scratch clone
# whose submodules are NOT initialized. Not run here: the HDL-reference build
# (pinned pyslang wheel not installed; no install allowed) and gen_wavedrom
# (wavedrom module not installed). Scratch only; the clone must stay clean.
set -uo pipefail
S=${SCRATCH:-/tmp/r222-478-r2-scratch}
D="$S/git-nosub"
BASE=$(git -C "$D" merge-base HEAD 88e9276b2a220c716f64a843f7e1eb8f9265e896)
echo "head=$(git -C "$D" rev-parse HEAD) em-dash base (merge-base with 88e9276b)=$BASE"
echo "submodules: $(git -C "$D" submodule status | cut -c1 | tr -d '\n') (all '-' = uninitialized)"
fail=0
step() { # <cmd...>
  local out rc
  out=$(cd "$D" && "$@" 2>&1); rc=$?
  [ $rc -eq 0 ] || fail=$((fail+1))
  printf 'exit %-3s %s\n' "$rc" "$*"
  printf '%s\n' "$out" | tail -2 | sed 's/^/        | /'
}
step python3 scripts/docs_check.py
step python3 scripts/check_em_dash.py --base "$BASE"
step python3 scripts/check_doc_style.py
step python3 scripts/check_doc_style.py --selftest
step python3 scripts/check_gptp_docs.py
step python3 scripts/check_gptp_docs.py --selftest
step python3 docs/DOC_MAP.gen.py --check
step python3 docs/DOC_MAP.gen.py --selftest
step python3 docs/diagrams/timesync_chain.gen.py --check
step python3 docs/diagrams/timesync_chain.gen.py --selftest
step python3 scripts/check_solution_docs.py
step python3 scripts/check_solution_docs.py --selftest
step python3 docs/diagrams/submodule_boundaries.gen.py --check
step python3 docs/diagrams/submodule_boundaries.gen.py --selftest
step python3 scripts/check_submodule_docs.py
step python3 scripts/check_submodule_docs.py --selftest
step python3 scripts/check_diagram_pngs.py
step python3 scripts/check_diagram_pngs.py --selftest
step python3 scripts/check_feature_status.py --self-test
step python3 docs/traceability/gen_module_matrix.py --check
echo "non-zero steps: $fail"
echo "clone status lines after run: $(git -C "$D" status --porcelain --untracked-files=all | wc -l)"
git -C "$D" status --porcelain --untracked-files=all | head
