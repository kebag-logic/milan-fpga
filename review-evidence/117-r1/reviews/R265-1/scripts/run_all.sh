#!/usr/bin/env bash
# Reproduce every R265-1 receipt from public inputs only.
#
# usage: scripts/run_all.sh <repo-clone at 0abf147f> <workdir>
#   The public evidence commit 160debeba11231e2fd38fde26c01c467039603ba
#   (branch 117-review-evidence) is fetched into <workdir>, extracted, and
#   every reviewer script runs over it. Receipts are written to ./receipts.
set -euo pipefail

repo=$1
work=$2
here=$(cd "$(dirname "$0")/.." && pwd)
ev_commit=160debeba11231e2fd38fde26c01c467039603ba
head=0abf147f726721f4a323ee6a32095a02363fe2dc
base=ede8d48ecd7c7f589a14b957951f040d92c99c70

mkdir -p "$work" "$here/receipts"
if [ ! -d "$work/evid.git" ]; then
  git init -q --bare "$work/evid.git"
  git -C "$work/evid.git" fetch -q --depth=1 https://github.com/kebag-logic/milan-fpga.git "$ev_commit"
fi
rm -rf "$work/ev"
mkdir -p "$work/ev"
git -C "$work/evid.git" archive "$ev_commit" review-evidence/117-r1 | tar -x -C "$work/ev"
ev=$work/ev/review-evidence/117-r1

test "$(git -C "$repo" rev-parse HEAD)" = "$head"
s=$here/scripts
r=$here/receipts
python3 "$s/verify_evidence_manifests.py" "$ev" > "$r/evidence_manifest_verify.txt"
python3 "$s/check_doc_hashes.py" "$repo/docs/findings/117_GPTP_SILICON_EVIDENCE.md" "$ev" > "$r/doc_hash_map.txt"
python3 "$s/step2.py" "$ev/bench-a200" > "$r/step2.txt"
python3 "$s/steady.py" "$ev/bench-a200" > "$r/steady.txt"
python3 "$s/step3.py" "$ev/bench-a202" > "$r/step3.txt"
python3 "$s/step3_ctl.py" "$ev/bench-a202" > "$r/step3_ctl.txt"
python3 "$s/probe_details.py" "$ev/bench-a202" > "$r/probe_details.txt"
python3 "$s/phc_steps.py" "$ev/bench-a202" > "$r/phc_steps.txt"
python3 "$s/census_cmp.py" "$ev/bench-a202/bench/census-start.jsonl" "$ev/bench-a202/bench/final/census-end.jsonl" > "$r/census_a202.txt" || true
python3 "$s/census_cmp.py" "$ev/bench-a200/bench/census-start.jsonl" "$ev/bench-a200/bench/final/census-final.jsonl" > "$r/census_a200.txt" || true
python3 "$s/peer_fw_hash.py" "$ev/bench-a200/bench/peer-aem-1.jsonl" > "$r/peer_fw_hash.txt"
python3 "$s/check_anchors.py" "$repo" docs/findings/117_GPTP_SILICON_EVIDENCE.md \
  docs/design/GM_LOSS_RECOVERY.md docs/findings/README.md > "$r/anchors.txt"
"$s/rerun_packet_analysis.sh" "$ev" "$work/rerun" > "$r/packet_analysis_rerun.txt"

# Bare-metal-only gate at base, first commit and head, in a disposable clone.
rm -rf "$work/basechk"
git clone -q --shared --no-checkout "$repo" "$work/basechk"
for rev in "$base" c3eb95fa9ac86a3f20b45f94057d6c011127db08 "$head"; do
  git -C "$work/basechk" checkout -q --detach "$rev"
  echo "== $rev"
  rc=0
  out=$(cd "$work/basechk" && python3 scripts/check_baremetal_only.py --check 2>&1) || rc=$?
  printf '%s\n' "$out" | tail -4
  echo "rc=$rc"
done > "$r/baremetal_only_by_rev.txt"
echo "receipts written to $r"
