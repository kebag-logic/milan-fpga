#!/usr/bin/env bash
# Regenerate the R265-3 receipts.
# Usage: run_all.sh <clone at 8016f7ac> <evidence git dir holding 117-review-evidence and the superseded chains> <out-dir> [private-values.json] [issue-117-comments.txt]
# The optional private-values file (the reference peer's original ENTITY field values, hex) is
# never published; without it the identity sweep covers the deny-listed stems only.
set -u
clone=$(cd "$1" && pwd) ev=$(cd "$2" && pwd) secret=${4:-} comments=${5:-}
mkdir -p "$3" && out=$(cd "$3" && pwd)
[ -n "$secret" ] && secret=$(cd "$(dirname "$secret")" && pwd)/$(basename "$secret")
[ -n "$comments" ] && comments=$(cd "$(dirname "$comments")" && pwd)/$(basename "$comments")
here=$(cd "$(dirname "$0")" && pwd)
base=ede8d48ecd7c7f589a14b957951f040d92c99c70
head=8016f7ac843b0ae6764dc4ec0140cda5ac7d6cc1
pin=74ac94e8eb331202f39d66cc006bc2640481e6da
tip=4165beb89afe217931bc52a8aaf800303e7bee1b
sup1=32aec66197ba78ee431c27383bb958e5728c270a
sup2=160debeba11231e2fd38fde26c01c467039603ba
mkdir -p "$out/gates" "$out/work"
work=$out/work
git --git-dir="$ev" archive "$pin" review-evidence | tar -x -C "$work"
root=$work/review-evidence/117-r1
git -C "$clone" show "$head:docs/findings/117_GPTP_SILICON_EVIDENCE.md" >"$work/page.md"
sec=(); [ -n "$secret" ] && sec=(--secret-json "$secret")
python3 "$here/archive_manifest_check.py" "$root" "$work/page.md" >"$out/archive_manifest_check_pin.txt"
for pk in bench-a200 bench-a202; do
  (cd "$root/$pk" && echo "$pk sha256sum -c: FAILED=$(sha256sum -c MANIFEST.sha256 2>/dev/null | grep -c ': FAILED$') OK=$(sha256sum -c MANIFEST.sha256 2>/dev/null | grep -c ': OK$') total=$(grep -c . MANIFEST.sha256)")
done >"$out/sha256sum_c_pin.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$ev" "${sec[@]}" --label "evidence branch history" --range "$base..$tip" --commit-msgs "$base..$tip" >"$out/identity_sweep_evidence_history.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$ev" "${sec[@]}" --label "pin tree" --tree "$pin:review-evidence" >"$out/identity_sweep_pin_tree.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$clone/.git" "${sec[@]}" --label "PR history" --range "$base..$head" --commit-msgs "$base..$head" >"$out/identity_sweep_pr_history.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$clone/.git" "${sec[@]}" --label "PR full tree" --tree "$head" >"$out/identity_sweep_pr_tree.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$ev" "${sec[@]}" --label "CONTROL superseded chain" --range "$base..$sup1" --commit-msgs "$base..$sup1" >"$out/identity_sweep_control_superseded.txt"
python3 "$here/identity_sweep.py" --repo "$clone" --git-dir "$ev" "${sec[@]}" --label "CONTROL pre-rewrite chain" --range "$base..$sup2" --commit-msgs "$base..$sup2" >"$out/identity_sweep_control_prerewrite.txt"
python3 "$here/scrub_rules_sweep.py" "$clone" "$ev" "evidence branch history" "$base..$tip" >"$out/scrub_rules_evidence_history.txt"
python3 "$here/scrub_rules_sweep.py" "$clone" "$clone/.git" "PR history" "$base..$head" >"$out/scrub_rules_pr_history.txt"
python3 "$here/pcap_name_fields.py" $(find "$root" -name '*.pcap' | sort) >"$out/pcap_name_fields_pin.txt"
python3 "$here/switch_addressing.py" "$root" 3cc0c6fe0210 >"$out/switch_addressing.txt"
python3 "$here/superseded_links.py" "$clone/.git" "$ev" "$base" "$head" "$tip" "$sup1" "$sup2" >"$out/superseded_links.txt"
python3 "$here/archive_simple_claims.py" "$root" >"$out/archive_simple_claims.txt"
for pair in "bench-a200/bench/census-start.jsonl bench-a200/bench/final/census-final.jsonl" \
            "bench-a202/bench/census-start.jsonl bench-a202/bench/final/census-end.jsonl"; do
  set -- $pair; echo "== $1 vs $2"; python3 "$here/census_acmp_diff.py" "$root/$1" "$root/$2"
done >"$out/census_acmp_diff.txt"
python3 "$here/step2_rederive.py" "$root" >"$out/step2_rederive.txt"
python3 "$here/step3_rederive.py" "$root" >"$out/step3_rederive.txt"
python3 "$here/step3_acmp.py" "$root" >"$out/step3_acmp.txt"
python3 "$here/step3_tucnt.py" "$root" >"$out/step3_tucnt.txt"
python3 "$here/step3_holdover_episodes.py" "$root" >"$out/step3_holdover_episodes.txt"
python3 "$here/intra_page_anchors.py" "$work/page.md" | sed "s#^$work/##" >"$out/intra_page_anchors.txt"
python3 - "$root/MANIFEST.json" >"$out/tool_redaction_flags_pin.txt" <<'PY'
import json, sys
for e in json.load(open(sys.argv[1])):
    if "/tools/" in e["file"] and e["original_sha256"] != e["published_sha256"]:
        print(e["file"], "original", e["original_sha256"][:8], "path_redacted", e.get("path_redacted"),
              "identity_redacted", e.get("identity_redacted", False))
PY
[ -n "$comments" ] && "$here/external_hash_claims.sh" "$clone" "$root" "$comments" >"$out/external_hash_claims.txt"
"$here/doc_gates.sh" "$clone" "$out/gates" "$base" >"$out/gates/SUMMARY.txt"
"$here/restore_verify.sh" "$clone" "$head" fe7079365e3d61364b7d6602a6e3abab20c1d222 >"$out/restore_verify.txt"
