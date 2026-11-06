#!/usr/bin/env bash
# Portable regeneration proof. Usage: regen_proof.sh <source-clone> <scratch-dir>
# Works only in disposable clones under <scratch-dir>; the source clone receives one read-only --check.
set -u
SRC=$1; S=$2
H=cf4120f4cf6c711781b9e4aa24173691dcce0a95; M=19f4c0b4eeac7cbb48aee0b055298b104628c039; D=87e9d03aa2a4797957ac0124d0c7851a2eec234c
A=docs/DOCUMENTATION_AUDIT.md; J=scripts/docs_inventory.json
export PYTHONDONTWRITEBYTECODE=1 LC_ALL=C.UTF-8
rm -rf "$S/regen"; mkdir -p "$S/regen"
run() { echo "\$ $*"; "$@"; echo "rc=$?"; }
echo "## 1 review clone, read-only check, with its initialised submodules"
( cd "$SRC" && git rev-parse HEAD && run python3 scripts/docs_inventory.py --check && git status --porcelain | wc -l )
echo "## 2 fresh no-submodule clone at H: --check, --write, byte compare"
git clone -q --no-checkout --shared "$SRC" "$S/regen/h"
cd "$S/regen/h"; git checkout -q --detach $H; git rev-parse HEAD 'HEAD^{tree}'
run python3 scripts/docs_inventory.py --check
run python3 scripts/docs_inventory.py --write
echo "worktree-delta-after-write: $(git status --porcelain | wc -l)"
sha256sum $A $J
echo "H blob audit: $(git show $H:$A | sha256sum)"
echo "H blob json : $(git show $H:$J | sha256sum)"
cmp <(git show $H:$A) $A && echo AUDIT_BYTE_IDENTICAL
cmp <(git show $H:$J) $J && echo JSON_BYTE_IDENTICAL
run python3 scripts/docs_inventory.py --selftest | tail -4
echo "## 3 replay: generator run from the merge commit must reproduce H's audit, and M must be stale"
git clone -q --no-checkout --shared "$SRC" "$S/regen/m"
cd "$S/regen/m"; git checkout -q --detach $M; git rev-parse HEAD
echo "M audit == dev audit? $(git rev-parse $M:$A) $(git rev-parse $D:$A)"
run python3 scripts/docs_inventory.py --check | cut -c1-160
run python3 scripts/docs_inventory.py --write
cmp <(git show $H:$A) $A && echo REPLAY_FROM_MERGE_EQUALS_H_AUDIT
echo "paths changed by the replay: $(git status --porcelain)"
echo "## 4 fault controls in the disposable H clone: the gate must fail"
cd "$S/regen/h"
sed -i 's/| \*\*total\*\* | \*\*213\*\* | \*\*92,369\*\* |/| **total** | **213** | **92,368** |/' $A; run python3 scripts/docs_inventory.py --check | cut -c1-140; git checkout -q -- $A
printf 'x\n' >> docs/testing/TESTING.md; run python3 scripts/docs_inventory.py --check | cut -c1-140; git checkout -q -- docs/testing/TESTING.md
git show $M:$A > $A; run python3 scripts/docs_inventory.py --check | cut -c1-140; git checkout -q -- $A
run python3 scripts/docs_inventory.py --check
echo "final-clean-delta: $(git status --porcelain | wc -l)"
