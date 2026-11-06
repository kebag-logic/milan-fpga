#!/usr/bin/env bash
# Regenerate the documentation audit in disposable trees and compare it byte for byte
# with the published head.
# Usage: regen_probe.sh <repo> <head> <merge-commit> <scratch-dir>
set -u
repo=$1 head=$2 merge=$3 scratch=$4
mkdir -p "$scratch"
gen=scripts/docs_inventory.py
audit=docs/DOCUMENTATION_AUDIT.md
data=scripts/docs_inventory.json
want_audit=$(git -C "$repo" show "$head:$audit" | sha256sum | cut -d' ' -f1)
want_data=$(git -C "$repo" show "$head:$data" | sha256sum | cut -d' ' -f1)
echo "head audit sha256 $want_audit"
echo "head data  sha256 $want_data"

compare() {
    local tree=$1 label=$2 got_a got_d
    got_a=$(sha256sum "$tree/$audit" | cut -d' ' -f1)
    got_d=$(sha256sum "$tree/$data" | cut -d' ' -f1)
    [ "$got_a" = "$want_audit" ] && echo "$label audit: BYTE-IDENTICAL" || echo "$label audit: DIFFERS $got_a"
    [ "$got_d" = "$want_data" ] && echo "$label data: BYTE-IDENTICAL" || echo "$label data: DIFFERS $got_d"
}

checkout() {
    local dir=$1 rev=$2
    rm -rf "$dir"
    git clone -q --no-hardlinks --no-checkout "$repo" "$dir"
    git -C "$dir" -c advice.detachedHead=false checkout -q --detach "$rev"
}

echo "== A: head, Git population, submodules not populated"
a=$scratch/regen-head
checkout "$a" "$head"
(cd "$a" && python3 -I $gen --check; echo "check rc=$?")
(cd "$a" && python3 -I $gen --write; echo "write rc=$?")
compare "$a" A
echo "porcelain lines after write: $(git -C "$a" status --porcelain | wc -l)"
(cd "$a" && python3 -I $gen --check; echo "check-after-write rc=$?")

echo "== B: head, no Git metadata (filesystem walk)"
b=$scratch/regen-archive
rm -rf "$b"; mkdir -p "$b"
git -C "$repo" archive "$head" | tar -x -C "$b"
(cd "$b" && python3 -I $gen --check; echo "check rc=$?")
(cd "$b" && python3 -I $gen --write; echo "write rc=$?")
compare "$b" B

echo "== C: merge commit before the regeneration commit"
c=$scratch/regen-merge
checkout "$c" "$merge"
(cd "$c" && python3 -I $gen --check 2>&1 | tail -3; echo "check rc=${PIPESTATUS[0]}")
(cd "$c" && python3 -I $gen --write; echo "write rc=$?")
compare "$c" C
echo "files changed by write at the merge commit:"
git -C "$c" status --porcelain

echo "== D: negative controls on a head copy; each must exit 1"
d=$scratch/regen-neg
checkout "$d" "$head"
(cd "$d" && printf 'one more line\n' >> docs/testing/TESTING.md && python3 -I $gen --check >/dev/null 2>&1; echo "extra TESTING.md line rc=$?"; git checkout -q -- docs/testing/TESTING.md)
(cd "$d" && sed -i 's/| 92,369 |\*\*/| 92,368 |**/; s/\*\*92,369\*\*/**92,368**/' $audit && python3 -I $gen --check >/dev/null 2>&1; echo "edited total rc=$?"; git checkout -q -- $audit)
(cd "$d" && sed -i '0,/73,640/s//73,641/' $audit && python3 -I $gen --check >/dev/null 2>&1; echo "edited current-lines rc=$?"; git checkout -q -- $audit)
(cd "$d" && python3 -I $gen --check; echo "restored rc=$?")

echo "== E: generator self-test on the head copy"
(cd "$a" && git checkout -q -- . && python3 -I $gen --selftest 2>&1 | tail -3; echo "selftest rc=${PIPESTATUS[0]}")
