#!/usr/bin/env bash
# Round 2 parent identity: point the scratch parent's gptp-processor gitlink
# (index only, never committed) at a pin, run the elaboration evidence and the
# ROM-ledger check, then restore the ledger. Usage: parent_r2.sh <label> <sha>
set -u
label="$1"; sha="$2"
S=$VALIDATION_STORAGE/g35-a599; P=$S/parent; SUB=$P/gptp-processor
O=$S/r2/romcheck-$label; mkdir -p "$O"
export TMPDIR=$S/tmp
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || { echo "parent toplevel mismatch"; exit 2; }
[ "$(git -C "$SUB" rev-parse --show-toplevel)" = "$SUB" ] || { echo "submodule toplevel mismatch"; exit 2; }
if ! git -C "$SUB" cat-file -e "$sha^{commit}" 2>/dev/null; then
  git -C "$SUB" fetch -q $LANES/g35-rx-err g35-rx-err || exit 2
fi
git -C "$SUB" checkout -q --detach "$sha" || exit 2
git -C "$P" update-index --cacheinfo "160000,$(git -C "$SUB" rev-parse HEAD),gptp-processor" || exit 2
echo "gitlink $(git -C "$P" rev-parse :gptp-processor) submodule $(git -C "$SUB" rev-parse HEAD)" > "$O/pin.txt"
"$S/bin/parent_evidence.sh" "$label" > "$O/evidence.out" 2>&1
cd "$P" || exit 2
syn/yosys/ooc.sh tcam > "$O/check-before-record.log" 2>&1; echo $? > "$O/check-before-record.rc"
syn/yosys/ooc.sh --record-rom-digests > "$O/record.log" 2>&1; echo $? > "$O/record.rc"
git diff -- syn/yosys/rom_digests.tsv > "$O/record.diff"
syn/yosys/ooc.sh tcam > "$O/check-after-record.log" 2>&1; echo $? > "$O/check-after-record.rc"
git checkout -q -- syn/yosys/rom_digests.tsv
git status --short > "$O/parent-status-after.txt"
cat "$O/pin.txt" "$O/evidence.out"
for f in check-before-record record check-after-record; do echo "$f rc=$(cat "$O/$f.rc")"; done
