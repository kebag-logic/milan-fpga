#!/usr/bin/env bash
# Regenerate this packet's receipts.
# usage: run_all.sh CLONE EVID_GITDIR OUT [TOKENS_JSON] [ORIGINAL_ROOT]
#   CLONE        review clone at dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba (docs gates, probes, links)
#   EVID_GITDIR  a clone of branch 117-review-evidence (tip 7626fb2b850e1e9c707ea247cab211b1e6833e0e)
#   OUT          output directory for receipts
#   TOKENS_JSON  optional private {"class": ["token", ...]} file for the identity sweep and probe P8
#                (never published); without it the sweep applies the repository's scrub rules only
#   ORIGINAL_ROOT optional pre-redaction archive root; only structure counts are printed from it
# Local paths in outputs are replaced by <clone> and <packet>.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
CLONE=$(cd "$1" && pwd); EVID=$(cd "$2" && pwd); OUT=$3; TOK=${4:-}; ORIG=${5:-}
HERE=$(cd "$(dirname "$0")" && pwd); PACKET=$(dirname "$HERE")
BASE=ede8d48ecd7c7f589a14b957951f040d92c99c70
HEAD=dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba
PIN=db842315015dda3d68c9687973c4803bb25ceefb
TIP=7626fb2b850e1e9c707ea247cab211b1e6833e0e
mkdir -p "$OUT"
[ "$(git -C "$CLONE" rev-parse HEAD)" = "$HEAD" ] || { echo "clone is not at $HEAD" >&2; exit 2; }
PINDIR=$(mktemp -d)
trap 'rm -rf "$PINDIR"' EXIT
git -C "$EVID" archive "$PIN" review-evidence/117-r1 | tar -x -C "$PINDIR"
ROOT=$PINDIR/review-evidence/117-r1
scrub() { sed -e "s|$CLONE|<clone>|g" -e "s|$PACKET|<packet>|g" -e "s|$PINDIR|<pin>|g"; }

python3 "$HERE/page_hashes_vs_manifest.py" "$CLONE/docs/findings/117_GPTP_SILICON_EVIDENCE.md" "$ROOT" | scrub > "$OUT/page_hashes_vs_manifest.txt"
python3 "$HERE/step3_rederive.py" "$ROOT" --json "$OUT/step3_rederive.json" | scrub > "$OUT/step3_rederive.txt"
python3 "$HERE/step2_rederive.py" "$ROOT" | scrub > "$OUT/step2_rederive.txt"
python3 "$HERE/b1_b3_check.py" "$ROOT" ${ORIG:+"$ORIG"} | scrub > "$OUT/b1_b3_check.txt"
python3 "$HERE/hostname_census.py" "$ROOT" | scrub > "$OUT/hostname_census_pin.txt"
python3 "$HERE/peer_view.py" "$ROOT" | scrub > "$OUT/peer_view.txt"
python3 "$HERE/archive_claims.py" "$ROOT" "$CLONE" "$OUT/step3_rederive.json" | scrub > "$OUT/archive_claims.txt"
"$HERE/pr_links.sh" "$CLONE" | scrub > "$OUT/pr_commits_archive_links.txt"
python3 "$HERE/page_links.py" "$CLONE" | scrub > "$OUT/page_links.txt"
{
  for c in "python3 scripts/docs_check.py" "python3 scripts/check_baremetal_only.py --check" \
           "python3 scripts/check_em_dash.py --base $BASE" "python3 scripts/gen_toc.py --check" \
           "python3 scripts/gen_toc.py --verify-anchors" "python3 scripts/check_doc_style.py" \
           "python3 scripts/check_doc_paths.py" "python3 scripts/check_gptp_docs.py" \
           "python3 scripts/check_feature_status.py" "python3 scripts/check_archive.py" \
           "python3 scripts/check_solution_docs.py" "python3 scripts/check_hygiene.py --check" \
           "python3 scripts/check_todo_ownership.py" "git diff --check $BASE..HEAD"; do
    echo "\$ $c"; (cd "$CLONE" && $c 2>&1 | tail -15); echo "rc=${PIPESTATUS[0]}"; echo
  done
} | scrub > "$OUT/docs_gates_at_head.txt"
if [ -n "$TOK" ]; then
  python3 "$HERE/identity_sweep.py" "$CLONE" "$TOK" \
    "pin=$EVID:$PIN:review-evidence" "branch-history=$EVID:$BASE..$TIP:review-evidence" \
    "pr-page=$CLONE:$BASE..$HEAD:docs/findings/117_GPTP_SILICON_EVIDENCE.md" \
    "pr-design=$CLONE:$BASE..$HEAD:docs/design/GM_LOSS_RECOVERY.md" \
    "pr-index=$CLONE:$BASE..$HEAD:docs/findings/README.md" | scrub > "$OUT/identity_sweep_targets.txt"
fi
python3 "$HERE/gate_probes.py" "$CLONE" ${TOK:+"$TOK"} | scrub > "$OUT/gate_probes.txt"
git -C "$CLONE" diff --quiet && [ -z "$(git -C "$CLONE" status --porcelain --ignored --untracked-files=all)" ] \
  || { echo "clone not clean after probes" >&2; exit 3; }
echo "receipts written to $OUT"
