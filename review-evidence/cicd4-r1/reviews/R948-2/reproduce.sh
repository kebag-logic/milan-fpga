#!/usr/bin/env bash
set -euo pipefail
repo=${1:?Usage: reproduce.sh /path/to/isolated-exact-head-clone}
here=$(cd -- "$(dirname -- "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
git -C "$repo" fetch --no-recurse-submodules --no-tags origin 9141378262c3331229a56c23d2c2fbb14cd87b48
git -C "$repo" fetch --no-recurse-submodules --no-tags origin 6be24f180ccc2c0ddda4b5d3ffa40ba09d7885e3
python3 "$here/verify_packet.py" "$repo" > "$here/packet-verification.json"
python3 "$here/run_checks.py" "$repo"
python3 "$here/compare_evidence.py" "$repo" > "$here/evidence-comparison.log" 2>&1
python3 "$here/verify_tree.py" "$repo" > "$here/tree-integrity.json"
