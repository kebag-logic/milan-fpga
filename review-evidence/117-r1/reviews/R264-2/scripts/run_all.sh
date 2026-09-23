#!/usr/bin/env bash
# Regenerate every R264-2 receipt from public sources.
# usage: run_all.sh CLONE_AT_HEAD WORKDIR OUTDIR
#   CLONE_AT_HEAD: a clean clone of kebag-logic/milan-fpga at f547a49b (read only)
#   WORKDIR:       disposable scratch (receives the fetched and extracted archives)
#   OUTDIR:        receipts directory
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
clone=$(cd "$1" && pwd)
mkdir -p "$2" "$3"
work=$(cd "$2" && pwd) out=$(cd "$3" && pwd)
here=$(cd "$(dirname "$0")" && pwd)
url=https://github.com/kebag-logic/milan-fpga.git
pinned=32aec66197ba78ee431c27383bb958e5728c270a   # archive the page pins (redacted)
prior=160debeba11231e2fd38fde26c01c467039603ba    # its pre-rewrite predecessor (token recovery only)
mkdir -p "$work" "$out"
cd "$work"
[ -d evidence.git ] || git init -q --bare evidence.git
git -C evidence.git fetch -q "$url" "$pinned" "$prior"
rm -rf ev32 ev160 && mkdir ev32 ev160
git -C evidence.git archive "$pinned" review-evidence/117-r1 | tar -x -C ev32
git -C evidence.git archive "$prior" review-evidence/117-r1 | tar -x -C ev160
P=ev32/review-evidence/117-r1 O=ev160/review-evidence/117-r1
page="$clone/docs/findings/117_GPTP_SILICON_EVIDENCE.md"
python3 "$here/redaction_tokens.py" "$O" "$P" "$P/MANIFEST.json" tokens.hex > "$out/redaction_runs.txt"
python3 "$here/identity_sweep.py" "$clone" "$O" "$P" > "$out/identity_sweep_archive.txt"
python3 "$here/confirm_hits.py" "$clone" "$O" "$P" > "$out/identity_hits_located.txt"
python3 "$here/pcap_token_counts.py" "$clone" "$O" "$P" > "$out/token_counts_orig_vs_pub.txt"
python3 "$here/token_in_tree.py" "$clone" "$O" "$P" "$clone/.git" f547a49bee5966a901d1e11981eb4dc94d038711 > "$out/tokens_in_pr_tree.txt"
python3 "$here/encoded_forms_sweep.py" "$clone" "$O" "$P" > "$out/encoded_forms_sweep.txt"
python3 "$here/pcap_name_fields.py" "$P" > "$out/pcap_name_fields_published.txt"
python3 "$here/verify_page_hashes.py" "$page" "$P" > "$out/page_hash_resolution.txt"
python3 "$here/rederive_step2.py" "$P/bench-a200/bench" > "$out/rederive_step2.txt"
python3 "$here/rederive_step3.py" "$P/bench-a202/bench" > "$out/rederive_step3.txt"
python3 "$here/rederive_step3_extra.py" "$P" > "$out/rederive_step3_extra.txt"
python3 "$here/verify_reach_row.py" "$P/bench-a202/bench" > "$out/verify_reach_row.txt"
python3 "$here/verify_phc_steps.py" "$P/bench-a202/bench" > "$out/verify_phc_steps.txt"
python3 "$here/verify_dark_window_hostrecs.py" "$P/bench-a202/bench" > "$out/verify_dark_window_hostrecs.txt"
python3 "$here/verify_census_daemons.py" "$P" > "$out/verify_census_daemons.txt"
echo "run_all: done"
