#!/usr/bin/env bash
# Disposable reach probes of the documentation gates over the lines this PR
# added. Works ONLY in a throwaway clone (argv[1]) made with
# `git clone --shared` of the review clone; each probe starts from a clean
# checkout of the exact head, mutates one thing, commits it (the em-dash gate
# judges HEAD), runs the relevant gates and records each exit status.
set -u
work=$1; head=$2; base=$3
cd "$work" || exit 2
export PYTHONDONTWRITEBYTECODE=1
gates() {
  for g in "scripts/docs_check.py" "scripts/check_em_dash.py --base $base" \
           "scripts/check_feature_status.py" "scripts/check_gptp_docs.py" \
           "scripts/check_doc_style.py" "scripts/gen_toc.py --check" \
           "scripts/gen_toc.py --verify-anchors" "scripts/check_doc_paths.py"; do
    out=$(python3 -B $g 2>&1); rc=$?
    printf '  %-45s exit=%s  %s\n' "$g" "$rc" "$(printf '%s' "$out" | grep -v '^\s*$' | tail -n1 | cut -c1-110)"
  done
}
probe() {
  name=$1; shift
  git checkout -q --detach "$head" && git reset -q --hard "$head"
  echo "== $name"
  python3 -B - "$@" <<'PY' || { echo "  PATCH REFUSED"; return; }
import sys
path, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(path, encoding="utf-8").read()
n = t.count(old)
if n < 1: sys.exit(f"anchor absent in {path}")
open(path, "w", encoding="utf-8").write(t.replace(old, new, 1))
print(f"  patched {path} (first of {n})")
PY
  git -c user.name=probe -c user.email=probe@invalid commit -q -am "probe $name"
  gates
}
echo "== control (exact head, no mutation)"; git checkout -q --detach "$head"; gates
probe "D1 delete the AS-13 traceability row" docs/traceability/ieee8021as.md \
  "| AS-13 | 8.3, 10.2.4.8, 14.6.9 | \`delayAsymmetry\` not modelled, so zero | None; decision on #511 | [Plane record](../design/GPTP_PLANE.md#propagation-asymmetry-is-not-modelled) | Excluded |
" ""
probe "D2 break one cross-page fragment" docs/reference/FR_NFR.md \
  "GPTP_PLANE.md#propagation-asymmetry-is-not-modelled" "GPTP_PLANE.md#propagation-asymmetry-is-not-modeled"
probe "D3 plant U+2014 in an added line" docs/design/GPTP_PLANE.md \
  "Revisit when a profile adds a second cabled port." "Revisit when a profile adds a second cabled port $(printf '\342\200\224') or later."
probe "D4 over-claim a served MVU command" docs/reference/MILAN_FEATURE_STATUS.md \
  "- \`GET_MILAN_INFO\`
<!-- milan-feature-fact:served_mvu_operations:end -->" "- \`GET_MILAN_INFO\`
- \`GET_SYSTEM_UNIQUE_ID\`
<!-- milan-feature-fact:served_mvu_operations:end -->"
probe "D5 restore FR-MVU-02 to MUST" docs/reference/FR_NFR.md \
  "the parent owns any integration seam. | S | T |" "the parent owns any integration seam. | M | T |"
git checkout -q --detach "$head" && git reset -q --hard "$head"
echo "== end: $(git rev-parse HEAD) clean=$(git status --porcelain | wc -l)"
