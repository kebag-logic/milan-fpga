#!/bin/sh
# Undo each generator change of this round in an export of the head and run the
# workflow's --check: a stale page must fail it (rc 1). Usage: generator_mutants.sh <lane> <scratch>
L=$1; W=$2
PATH=/tmp/797-a711-wd/bin:$PATH
printf 'mutant\trc\tlast line\n'
for m in baseline no_selection no_fold no_slot_name old_srp_words old_fresh_words old_chmap_words; do
  rm -rf "$W/$m"; mkdir -p "$W/$m"
  git -C "$L" archive HEAD | tar -x -C "$W/$m"
  cd "$W/$m" || exit 2
  case $m in
    no_selection) sed -i 's/^        chosen = selection(st)$/        chosen = None/' scripts/register_sv.py ;;
    no_fold) sed -i 's/conditions(named(term, model.wording))/conditions(term)/' scripts/register_page.py ;;
    no_slot_name) sed -i 's/^            if start.unknown and node\[2\]\[0\] == "bin"/            if False and node[2][0] == "bin"/' scripts/register_fields.py ;;
    old_srp_words) sed -i 's/"`STRM_SEL\[9\]` is 1"/"`STRM_SEL[9]` selects the listener row at index 0"/' scripts/register_descriptions.json ;;
    old_fresh_words) sed -i 's/the SRP table answered a poll since the last `STRM_SEL`\/`STRMW_CTRL` write/the SRP table answered since the last selection/' scripts/register_descriptions.json ;;
    old_chmap_words) python3 -c "
import json,sys
p='scripts/register_descriptions.json'; d=json.load(open(p))
d['condition_words']['cmrd_valid_r']=['a channel-map readback has completed','no channel-map readback has completed']
open(p,'w').write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')" ;;
  esac
  changed=$(git -C "$L" diff --no-index --stat "$L/scripts" "$W/$m/scripts" 2>/dev/null | tail -1)
  python3 scripts/gen_register_reference.py --check > "$W/$m.log" 2>&1
  rc=$?
  printf '%s\t%s\t%s | %s\n' "$m" "$rc" "$(tail -1 "$W/$m.log" | cut -c1-160)" "${changed:-no change}"
  cd /
done
