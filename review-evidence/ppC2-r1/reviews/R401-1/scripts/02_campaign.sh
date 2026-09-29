#!/bin/sh
# Re-run the PR's own MAAP mutation campaign on the scratch head export,
# with the pinned simulator first on PATH.
set -u
. "$(dirname "$0")/00_env.sh"
T="$PKT/scratch/head"
R="$PKT/receipts/campaign"
mkdir -p "$R"
PATH="$(dirname "$VLT"):$PATH" make -C "$T/tb/maap" mutants MUTANT_OUTPUT="$R" > "$R/campaign.log" 2>&1
echo "campaign rc=$?" | tee "$R/rc.txt"
