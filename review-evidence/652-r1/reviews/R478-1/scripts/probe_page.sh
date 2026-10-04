#!/bin/sh
# One planted edit in the design page of a fresh scratch worktree, then the
# record-space gate. Prints PAGE <name> rc=<rc> and the section 4.2 findings.
# Usage: probe_page.sh <packet> <name> <old> <new>
P=$1; name=$2; old=$3; new=$4
W=$P/scratch/page-$name
git -C "$P/scratch/head" worktree remove --force "$W" 2>/dev/null; rm -rf "$W"
git -C "$P/scratch/head" worktree add -q --detach "$W" HEAD
python3 "$P/scripts/plant.py" "$W/docs/design/SAVED_STATE_FASTCONNECT.md" "$old" "$new" || exit 3
(cd "$W" && python3 scripts/check_nvm_record_space.py --quiet) > "$P/receipts/page_$name.log" 2>&1
rc=$?
echo "PAGE $name rc=$rc :: $(grep -m3 'section 4.2' "$P/receipts/page_$name.log" | tr '\n' ' ' | cut -c1-300)"
