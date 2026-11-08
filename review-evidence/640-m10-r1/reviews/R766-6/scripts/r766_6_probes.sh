#!/usr/bin/env bash
# Reproduce the round-6 delta probes on a clone of kebag-logic/milan-fpga.
# Usage: r766_6_probes.sh <clone-at-72816d26> <census-input-dir> <out-dir> [<venv-with-tools/markdown-requirements>]
# <census-input-dir> holds the published census tool and inputs from the
# evidence branch b6694157, review-evidence/640-m10-r1/author-r2/evidence/census/:
# census_coverage.py, basis_soc_hierarchy.txt, basis_csr.csv, basis_place_top_excerpt.rpt.
set -u
W=$1; C=$2; O=$3; V=${4:-}
H=72816d26a7e2a29db5bc198ff65056ee4c5790b4
B=503bc97cd4f24ad07596c17e7188f2024617972d
D=0a75aa774b89ac89351700f63dd8cbb89694af6c
P=d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73
mkdir -p "$O"
test "$(git -C "$W" rev-parse HEAD)" = "$H" || { echo "clone not at $H"; exit 2; }

# (1) the head's delta against dev equals round 5's delta against its base, line for line
git -C "$W" diff "$D" "$H" > "$O/dev_to_head.diff"
git -C "$W" diff "$B" "$P" > "$O/base_to_r5.diff"
for f in dev_to_head base_to_r5; do
  grep -E '^[+-]' "$O/$f.diff" | grep -vE '^(\+\+\+|---) ' > "$O/$f.lines"
done
cmp "$O/dev_to_head.lines" "$O/base_to_r5.lines" && echo "SAME added and removed lines" | tee "$O/delta_identity.txt"
git -C "$W" diff --stat "$D" "$H" | tee -a "$O/delta_identity.txt"

# (2) census coverage at the head, and its control against the round 1 page
( cd "$O" && python3 -I "$C/census_coverage.py" "$W" "$C/basis_soc_hierarchy.txt" "$C/basis_csr.csv" "$C/basis_place_top_excerpt.rpt" > census_coverage_head.out 2>&1; echo $? > census_coverage_head.rc )
CT=$O/control_r1; rm -rf "$CT"; mkdir -p "$CT/docs/design" "$CT/sw/litex"
git -C "$W" show 3f8ed303:docs/design/MARK_II_AREA_PLAN.md > "$CT/docs/design/MARK_II_AREA_PLAN.md"
cp "$W/sw/litex/milan_soc.py" "$CT/sw/litex/"
( cd "$O" && python3 -I "$C/census_coverage.py" "$CT" "$C/basis_soc_hierarchy.txt" "$C/basis_csr.csv" "$C/basis_place_top_excerpt.rpt" > census_coverage_control_r1.out 2>&1; echo $? > census_coverage_control_r1.rc )
echo "census head rc=$(cat "$O/census_coverage_head.rc") (want 0); control rc=$(cat "$O/census_coverage_control_r1.rc") (want 1)"

# (3) the docs.yml gates that read documentation pages
cd "$W"
export PYTHONDONTWRITEBYTECODE=1
[ -n "$V" ] && export PATH="$V/bin:$PATH"
run() { id=$1; shift; { echo "# head $H step $id: $*"; timeout 900 bash -c "$*"; } > "$O/$id.log" 2>&1; echo $? > "$O/$id.rc"; printf '%s rc=%s %s\n' "$id" "$(cat "$O/$id.rc")" "$(tail -1 "$O/$id.log" | cut -c1-150)"; }
run gate_7_docs_check "python3 scripts/docs_check.py"
run gate_9_doc_style "python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest && python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest"
run gate_15_feature_status "python3 scripts/check_feature_status.py && python3 scripts/check_feature_status.py --self-test"
run gate_16_traceability "python3 docs/traceability/gen_module_matrix.py --check"
run gate_43_doc_paths "python3 scripts/check_doc_paths.py"
run gate_44_archive "python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest"
run gate_45_toc "python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
run gate_46_inventory "python3 scripts/docs_inventory.py --check && python3 scripts/docs_inventory.py --selftest"
run em_dash_vs_0a75aa77 "python3 scripts/check_em_dash.py --base $D"
run em_dash_vs_503bc97c "python3 scripts/check_em_dash.py --base $B"
run diff_check_vs_dev "git diff --check $D HEAD && echo clean"
run diff_check_vs_base "git diff --check $B HEAD && echo clean"

# restore check
{ echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) write-tree $(git write-tree)"; git status --porcelain --ignored=matching; } > "$O/restore_check.txt"
cat "$O/restore_check.txt"
