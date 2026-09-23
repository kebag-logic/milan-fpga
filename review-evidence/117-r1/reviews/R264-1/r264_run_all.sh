#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Regenerate the R264-1 receipts.
#   r264_run_all.sh <evidence_root> <review_clone> <out_dir>
# <evidence_root>: review-evidence/117-r1 extracted from commit
#   160debeba11231e2fd38fde26c01c467039603ba (branch 117-review-evidence).
# <review_clone>: a clean checkout of 0abf147f726721f4a323ee6a32095a02363fe2dc.
set -euo pipefail

if (( $# != 3 )); then
  echo "usage: $0 <evidence_root> <review_clone> <out_dir>" >&2
  exit 2
fi
readonly evidence=$1 clone=$2 out=$3
readonly here=$(cd "$(dirname "$0")" && pwd)
readonly page="$clone/docs/findings/117_GPTP_SILICON_EVIDENCE.md"
readonly a200="$evidence/bench-a200" a202="$evidence/bench-a202/bench"
mkdir -p "$out/gates"

python3 "$here/r264_packet_check.py" "$evidence" "$page" > "$out/packet-integrity.txt"
python3 "$here/r264_wire.py" step2 "$a200/bench/runA/tap-runA.pcap" "$a200/bench/runB/tap-runB.pcap" \
  "$a200/bench/runC/tap-runC.pcap" "$a200/bench/final/tap-final.pcap" > "$out/step2-a200.json"
for f in runA/tap-runA.pcap runB/tap-runB.pcap runC/tap-runC.pcap final/tap-final.pcap; do
  python3 "$here/r264_wire.py" crf "$a200/bench/$f"
done > "$out/crf-a200.json"
python3 "$here/r264_console.py" summary "$a200/identity/console-identity.txt" "$a200/bench/runA/console.txt" \
  "$a200/bench/runB/console.txt" "$a200/bench/final/console-final.txt" \
  "$a200/bench/console-memread-test.txt" > "$out/console-a200-summary.txt"
cycles=()
for n in 1 2 3 4 5 6; do cycles+=("$a202/cycle$n"); done
python3 "$here/r264_step3.py" "${cycles[@]}" > "$out/step3-cycles.jsonl"
python3 "$here/r264_step3.py" --robust "${cycles[@]}" > "$out/step3-cycles-robust.jsonl"
python3 "$here/r264_watch.py" "${cycles[@]}" > "$out/step3-watch.jsonl"
python3 "$here/r264_step3_console.py" "${cycles[@]}" > "$out/step3-console.jsonl"
python3 "$here/r264_compare_step3.py" "$page" "$out/step3-cycles.jsonl" "$out/step3-cycles-robust.jsonl" \
  > "$out/step3-vs-page.txt"
(cd "$clone" && { python3 scripts/check_baremetal_only.py --check; echo "rc=$?"; }) \
  > "$out/gates/rerun_check_baremetal_only.txt" 2>&1 || true
echo "receipts written to $out"
