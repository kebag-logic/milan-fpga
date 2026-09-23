#!/usr/bin/env bash
# Regenerate the R265-2 receipts.
# usage: scripts/run_all.sh <clone-at-f547a49b> <workdir>
# The clone must carry commit 160debeba11231e2fd38fde26c01c467039603ba (the
# pre-redaction archive, still served by the public repository); the pinned
# archive 32aec661 is fetched from the public branch into <workdir>.
set -euo pipefail
clone=$(cd "$1" && pwd)
work=$2
here=$(cd "$(dirname "$0")/.." && pwd)
pin=32aec66197ba78ee431c27383bb958e5728c270a
pre=160debeba11231e2fd38fde26c01c467039603ba
head=f547a49bee5966a901d1e11981eb4dc94d038711
mkdir -p "$work" "$here/receipts"
export PYTHONDONTWRITEBYTECODE=1
if [ ! -d "$work/ev.git" ]; then
  git init -q --bare "$work/ev.git"
  git --git-dir="$work/ev.git" fetch -q --no-tags \
    https://github.com/kebag-logic/milan-fpga.git \
    117-review-evidence:refs/remotes/ev/117-review-evidence
fi
rm -rf "$work/ev32" "$work/ev160" "$work/anc" "$work/prtree"
mkdir -p "$work/ev32" "$work/ev160" "$work/prtree"
git --git-dir="$work/ev.git" archive "$pin" review-evidence/117-r1 | tar -x -C "$work/ev32"
git -C "$clone" archive "$pre" review-evidence/117-r1 | tar -x -C "$work/ev160"
for c in 55b2338378693a7a17b30162a1374802666c6252 6b14c6c024c99f9bb79633a1c8177fe677ffc000 \
         204879ff2893a16ea73c5c1a9cd262c947f5855a; do
  mkdir -p "$work/anc/$c"
  git --git-dir="$work/ev.git" archive "$c" review-evidence | tar -x -C "$work/anc/$c"
done
for f in docs/findings/117_GPTP_SILICON_EVIDENCE.md docs/findings/README.md docs/design/GM_LOSS_RECOVERY.md; do
  mkdir -p "$work/prtree/$(dirname "$f")"
  git -C "$clone" show "$head:$f" > "$work/prtree/$f"
done
A=$work/ev32/review-evidence/117-r1
cd "$here"
python3 scripts/verify_archive.py "$A" "$work/ev160/review-evidence/117-r1" > receipts/archive-verify.txt || true
python3 scripts/page_hashes.py "$work/prtree/docs/findings/117_GPTP_SILICON_EVIDENCE.md" "$A" > receipts/page-hashes.txt || true
python3 scripts/scan_identity.py "$work/ev160/review-evidence/117-r1" "$A" "$clone" \
  "$work"/anc/* "$work/prtree" 2>&1 | sed "s#$work/##g" > receipts/identity-scan.txt || true
python3 scripts/step2.py "$A/bench-a200" > receipts/step2-rederived.txt
python3 scripts/step3.py "$A/bench-a202" > receipts/step3-rederived.txt
python3 scripts/step3b.py "$A/bench-a202" > receipts/step3b-rederived.txt
python3 scripts/step3c.py "$A/bench-a202" > receipts/step3c-rederived.txt
python3 scripts/step3_ctl.py "$A/bench-a202" > receipts/step3-controller-rederived.txt
python3 scripts/misc_checks.py "$A" > receipts/misc-checks.txt
{ python3 scripts/restore_verify.py "$clone" "$head" 27e6488d3da9669f787662d49e40f2263995dcb7 || true; git -C "$clone" submodule status; } > receipts/restore-verify.txt
python3 scripts/announce_fields.py "$A/bench-a200" > receipts/announce-fields.txt
python3 scripts/console_census.py "$A" > receipts/console-census.txt
