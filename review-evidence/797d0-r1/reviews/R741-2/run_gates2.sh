#!/usr/bin/env bash
# Run the PR's listed validation commands plus the docs-job neighbours, concurrently, one log and rc per command.
# Usage: run_gates2.sh CLONE PYTHON OUTDIR
set -u
clone=$1; py=$2; out=$3; mkdir -p "$out"
cmds=(
 "scripts/docs_inventory.py --check"
 "scripts/docs_inventory.py --selftest"
 "scripts/docs_check.py"
 "scripts/check_doc_style.py"
 "scripts/check_em_dash.py --base 1e80128f0a467b58bf884b7d9bf62e013a2fb141"
 "scripts/check_doc_paths.py"
 "scripts/gen_toc.py --verify-anchors"
 "scripts/gen_toc.py --check"
 "scripts/check_baremetal_only.py --check"
 "scripts/check_baremetal_only.py --selftest"
 "scripts/ci_gate_workflows.py --check"
 "scripts/ci_events.py --check"
 "scripts/ci_events.py --selftest"
 "scripts/check_archive.py"
 "scripts/check_feature_status.py"
)
i=0
for c in "${cmds[@]}"; do
  i=$((i+1)); n=$(printf '%02d' $i)
  ( cd "$clone" && echo "$ $c" > "$out/$n.log" && timeout 900 "$py" -I $c >> "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) &
done
wait
for f in "$out"/*.rc; do n=$(basename "$f" .rc); printf '%s\trc=%s\t%s\n' "$n" "$(cat "$f")" "$(head -1 "$out/$n.log" | cut -c3-)"; done
