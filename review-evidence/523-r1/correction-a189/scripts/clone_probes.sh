#!/usr/bin/env bash
# Run R256's two real-tree probes, unmodified, against a DISPOSABLE local clone
# (both scripts edit, then `git checkout`/`git clean`, the tree they are given,
# so they must never touch a lane). The clone's gPTP processor and axis
# submodules are cloned from the checkout's own submodule checkouts at their pins.
# Usage: clone_probes.sh CHECKOUT PACKET
set -u
repo="$1"; packet="$2"
r256="$packet/scratch/review-probes/review-evidence/523-r1/reviews/R256-2/scripts"
clone="$packet/scratch/clone"
tools=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin
rm -rf "$clone"
git clone -q --no-hardlinks "$repo" "$clone" || exit 3
git -C "$clone" checkout -q --detach "$(git -C "$repo" rev-parse HEAD)" || exit 3
for sub in gptp-processor third_party/verilog-axis; do
  git -C "$clone" config "submodule.$sub.url" "$repo/$sub"
  git -C "$clone" -c protocol.file.allow=always submodule update -q --init "$sub" || exit 3
done
git -C "$clone" submodule status
python3 "$packet/scripts/rcpt.py" 45-R256-refusal-scope --cwd "$clone" \
  --env "PATH=$tools:$PATH" --env "VERILATOR=$tools/verilator" --env VERILATOR_JOBS=8 --env "TMPDIR=$packet/scratch/probe-tmp" -- \
  bash "$r256/probe_refusal_scope.sh" "$clone"
python3 "$packet/scripts/rcpt.py" 46-R256-dependency-pins --cwd "$clone" \
  --env "PATH=$tools:$PATH" --env "VERILATOR=$tools/verilator" --env VERILATOR_JOBS=8 --env "TMPDIR=$packet/scratch/probe-tmp" -- \
  bash "$r256/probe_dependency_pins.sh" "$clone"
cp "$packet/scratch/refusal-scope-results.tsv" "$packet/receipts/probes/R256-refusal-scope.tsv" 2>/dev/null || true
