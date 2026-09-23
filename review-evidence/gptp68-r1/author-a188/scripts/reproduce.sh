#!/bin/sh
# Re-run every receipt of this lane against the lane checkout's CURRENT HEAD.
# Writes receipts/<name>.log and receipts/<name>.exit; never edits the lane.
# Order: identity, tree state, ROM parity, ROM word diff, ROM differential,
# slew model, #68 mutation evidence, then the full repository gate.
set -u
. $REVIEWS/gptp68-a188-packet/scripts/env.sh
R=$A188_PACKET/receipts
S=$A188_PACKET/scripts
cd "$A188_LANE" || exit 2
step() {  # name command...
  n=$1; shift
  { echo "# command: $*"; echo "# start: $(date -Is)"; } > "$R/$n.log"
  "$@" >> "$R/$n.log" 2>&1
  rc=$?
  { echo "# end: $(date -Is)"; echo "# exit: $rc"; } >> "$R/$n.log"
  echo "$rc" > "$R/$n.exit"
  echo "$n exit=$rc"
}
step identity sh -c 'command -v verilator; verilator --version; sha256sum $VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator; git rev-parse HEAD "HEAD^{tree}" c1b617435824929a790739ea8585c3fe1a328cc0; git merge-base HEAD c1b617435824929a790739ea8585c3fe1a328cc0; git log --oneline c1b617435824929a790739ea8585c3fe1a328cc0..HEAD; git status --porcelain; nproc'
step rom-parity-base env REF=c1b617435824929a790739ea8585c3fe1a328cc0 "$S/rom_parity.sh"
step rom-parity "$S/rom_parity.sh"
step rom-word-diff "$S/rom_word_diff.sh"
step base-harness-vs-new-rom "$S/base_harness_vs_new_rom.sh"
step rom-servo-differential python3 "$S/rom_servo_differential.py" --n 20000
step servo-slew-model python3 "$S/servo_slew_model.py"
step policy-mutation-evidence python3 "$S/policy_mutation_evidence.py"
"$S/full_gate.sh" full-gate-head; echo "full-gate-head exit=$(cat "$R/full-gate-head.exit")"
step tree-after sh -c 'git status --porcelain; git status --porcelain --ignored | head -50'
