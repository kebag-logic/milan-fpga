#!/usr/bin/env bash
# Reproduce the ROM digest ledger at the reviewed head with the repository
# tool, compare it with the committed ledger, and probe that the 0922e434 rows
# are load-bearing for the OOC path. Restores the tracked ledger afterwards.
# Usage: rom_ledger_probe.sh <clone> <packet>
set -u
CLONE="$1"; PKT="$2"
R="$PKT/receipts"; S="$PKT/scratch/ooc_tmp"
mkdir -p "$R" "$S"
cd "$CLONE" || exit 2
LEDGER=syn/yosys/rom_digests.tsv
PP_NEW=0922e43408f891fc0b84a84691df86b4fd0f1c0d
PP_OLD=990f96526bb89356c963a260ebbdcf2a77e6623a

git cat-file -p "HEAD:$LEDGER" > "$S/ledger.head"

echo "== 1. record mode at the pin =="
( cd syn/yosys && OOC_TMP="$S" ./ooc.sh --record-rom-digests ); echo "record rc=$?"
if cmp -s "$LEDGER" "$S/ledger.head"; then echo "RERECORD_IDENTICAL_TO_HEAD yes"; else echo "RERECORD_IDENTICAL_TO_HEAD NO"; diff "$S/ledger.head" "$LEDGER"; fi

echo "== 2. new rows equal old-pin rows =="
for img in ltn_rom.hex ucode.hex; do
  n=$(awk -v p=$PP_NEW -v i=$img '$1==p && $2==i {print $3}' "$S/ledger.head")
  o=$(awk -v p=$PP_OLD -v i=$img '$1==p && $2==i {print $3}' "$S/ledger.head")
  echo "$img new=$n old=$o $([ -n "$n" ] && [ "$n" = "$o" ] && echo MATCH || echo DIFFER)"
done
echo "rows_for_new_pin=$(grep -c "^$PP_NEW	" "$S/ledger.head")"
echo "committed_ledger_diff_vs_base:"; git diff 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD -- "$LEDGER" | grep '^[-+][^-+]'

echo "== 3. generated images hashed directly =="
for f in ltn_rom.hex ucode.hex gptp_ucode.hex; do sha256sum "$S/$f"; done

echo "== 4. negative probe: ledger without the new-pin rows must refuse =="
grep -v "^$PP_NEW	" "$S/ledger.head" > "$LEDGER"
( cd syn/yosys && OOC_TMP="$S" ./ooc.sh KL_pp_shadow ) > "$S/neg.out" 2>&1; echo "neg rc=$?"
grep -m1 FATAL "$S/neg.out"

echo "== 5. negative probe: a wrong new-pin digest must refuse =="
sed "s/^\($PP_NEW	ucode.hex	\).*/\1$(printf '0%.0s' $(seq 64))/" "$S/ledger.head" > "$LEDGER"
( cd syn/yosys && OOC_TMP="$S" ./ooc.sh KL_pp_shadow ) > "$S/neg2.out" 2>&1; echo "neg2 rc=$?"
grep -m1 FATAL "$S/neg2.out"

echo "== restore =="
git checkout -- "$LEDGER"
git diff --quiet HEAD -- "$LEDGER" && echo "LEDGER_RESTORED yes"
