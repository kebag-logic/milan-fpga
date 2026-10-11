#!/bin/bash
# Disguise the REAL tsn-c-stack submodule of a milan-fpga checkout five ways (include/adp.h edited to
# ADP_ADVERTISE_MS 9000u under a replacement tree, a replacement commit, a graft file and an attribute clean
# filter; and a script made executable), run a sample of entry points on their default stack, and require
# each to exit non-zero naming the changed path, before any build. Every disguise is undone and the clean
# pin re-checked after each. Usage: entry_points_probe.sh <checkout> <scratch> <rv32-cc> <verilator>
set -u
R=$(cd "$1" && pwd); S=$2; export MILAN_RV32_CC=$3; export VERILATOR=$4
STK=$R/third_party/tsn-c-stack; GD=$(git -C "$STK" rev-parse --absolute-git-dir)
PIN=$(git -C "$R" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
T=$R/sw/firmware/ctrl/test; G=$R/sw/firmware/gtest
mkdir -p "$S"; ORIG=$S/adp.h.orig; cp "$STK/include/adp.h" "$ORIG"
nor() { env GIT_NO_REPLACE_OBJECTS=1 git -C "$STK" "$@"; }
edit() { sed -i 's/#define ADP_ADVERTISE_MS 5000u/#define ADP_ADVERTISE_MS 9000u/' "$STK/include/adp.h"; }
undo() {
  for r in $(git -C "$STK" replace -l); do git -C "$STK" replace -d "$r" >/dev/null; done
  rm -f "$GD/info/grafts" "$GD/info/attributes"; git -C "$STK" config --unset filter.probe.clean || true
  cp "$ORIG" "$STK/include/adp.h"; chmod 644 "$STK/scripts/check_boundary.py"
}
newtree() {  # the pinned include/ tree with adp.h replaced by the edited blob; echo old new
  local blob old new; blob=$(git -C "$STK" hash-object -w --no-filters include/adp.h); old=$(nor rev-parse "$PIN:include")
  new=$(nor ls-tree "$old" | sed "s/[0-9a-f]\{40\}\tadp.h$/$blob\tadp.h/" | git -C "$STK" mktree); echo "$old $new"
}
d_replace_tree() { edit; read -r old new < <(newtree); git -C "$STK" replace "$old" "$new"; }
d_replace_commit() {
  edit; local old new root nroot c; read -r old new < <(newtree); root=$(nor rev-parse "$PIN^{tree}")
  nroot=$(nor ls-tree "$root" | sed "s/[0-9a-f]\{40\}\tinclude$/$new\tinclude/" | git -C "$STK" mktree)
  c=$(nor cat-file commit "$PIN" | sed "1s/$root/$nroot/" | git -C "$STK" hash-object -t commit -w --stdin)
  git -C "$STK" replace "$PIN" "$c"
}
d_graft() { edit; echo "$PIN" > "$GD/info/grafts"; }
d_filter() {
  local size; size=$(stat -c %s "$ORIG"); edit
  printf '%s\n' "$(sed 's/9000u/5000u/' "$STK/include/adp.h")" > /dev/null
  git -C "$STK" config filter.probe.clean "sed s/ADP_ADVERTISE_MS\\ 9000u/ADP_ADVERTISE_MS\\ 5000u/"
  echo "include/adp.h filter=probe" > "$GD/info/attributes"
  [ "$(git -C "$STK" hash-object include/adp.h)" = "$(nor rev-parse "$PIN:include/adp.h")" ] \
    && echo "  (filter turns the edit back into the pinned blob: yes)" || echo "  (filter check: NO)"
}
d_mode() { chmod 755 "$STK/scripts/check_boundary.py"; }
run() {  # name, expected path, command...
  local name=$1 want=$2; shift 2; local out rc
  out=$(cd "$S" && timeout 300 "$@" 2>&1); rc=$?
  local said; said=$(printf '%s\n' "$out" | grep -E "REFUSED|differs from the pinned" | tail -1 | cut -c1-160)
  if [ $rc -ne 0 ] && printf '%s' "$said" | grep -q "$want"; then echo "  [refused] $name: rc=$rc: $said"
  else echo "  [ESCAPED] $name: rc=$rc: ${said:-$(printf '%s\n' "$out" | tail -1 | cut -c1-160)}"; fi
}
for d in d_replace_tree d_replace_commit d_graft d_filter d_mode; do
  want=include/adp.h; [ $d = d_mode ] && want=scripts/check_boundary.py
  echo "== $d"; $d
  echo "  git status --short in the submodule: $(git -C "$STK" status --short | tr '\n' ' ')"
  run "ctrl_build.py --stack-pin" "$want" python3 -B "$T/ctrl_build.py" --stack-pin
  run "make stack-pin" "$want" make --no-print-directory -C "$R/tb/verilator/mbx" stack-pin
  run "make obj_fw/libctrlfw.a" "$want" make --no-print-directory -C "$R/tb/verilator/mbx" obj_fw/libctrlfw.a
  run "test_ctrl_firmware.py --build-only" "$want" python3 -B "$T/test_ctrl_firmware.py" --build-only --build-dir "$S/b-$d"
  run "fw_coverage.py --build-only" "$want" python3 -B "$G/fw_coverage.py" --build-only --keep "$S/c-$d"
  run "maap_differential.py" "$want" python3 -B "$T/maap_differential.py"
  run "aecp_arms.py --app" "$want" python3 -B "$T/aecp_arms.py" --app --output "$S/a-$d"
  run "ctrl_image.py" "$want" python3 -B "$T/ctrl_image.py"
  run "ctrl_boundary.py" "$want" python3 -B "$T/ctrl_boundary.py" --require-rv32
  undo
  echo "  undone: $(python3 -B "$T/ctrl_build.py" --stack-pin)"
done
