#!/bin/sh
# Reproduce the hosted `elaborate` / `docs-check` failure of PR #555's head:
# sw/builder/test_builder.py gate 1b (test_baremetal_profile_contract) pins the
# pre-#387 render_recentre_p_w initializer. Runs the gate compiler-absent (the
# hosted docs-check step) on three disposable shared clones of <repo>:
#   base  = dev 57456af9 (expected rc 0)
#   head  = e68c1b1a     (expected rc 1, the pin assertion)
#   probe = head with ONLY the pin and its ADP mutant re-pointed at
#           media_rebase_p_w (a reviewer probe, not a proposed fix)
# Usage: probe_builder_render_pin.sh <repo-with-submodules> <work-dir> <out-dir>
set -u
REPO=$1; WORK=$2; OUT=$3
mkdir -p "$WORK" "$OUT"
mk() {  # mk <name> <commit>
  rm -rf "$WORK/$1"
  git clone -q --shared --no-checkout "$REPO" "$WORK/$1"
  git -C "$WORK/$1" checkout -q "$2"
  for s in gptp-processor protocol-processor third_party/verilog-axis; do
    git -C "$WORK/$1" -c protocol.file.allow=always submodule update --init -q \
      --reference "$REPO/.git/modules/$s" "$s"
  done
}
gate() {  # gate <name>
  ( cd "$WORK/$1" && git rev-parse HEAD && git diff --stat &&
    timeout 600 python3 sw/builder/test_firmware_compiler.py --absent \
      --audit "$WORK/$1.jsonl" ) > "$OUT/builder-gate1b-$1.log" 2>&1
  echo "rc=$?" >> "$OUT/builder-gate1b-$1.log"
  echo "$1: $(tail -1 "$OUT/builder-gate1b-$1.log")"
}
mk base 57456af96b3127b9d309a995bbbd35a6113ce52d; gate base
mk head e68c1b1ac08c8b1e12a28e281b266d06f881e402; gate head
mk probe e68c1b1ac08c8b1e12a28e281b266d06f881e402
python3 - "$WORK/probe/sw/builder/test_builder.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
edits = [
 ('            "gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load "\n'
  '            "| src_recentre_p_r",\n',
  '            "media_rebase_p_w | src_recentre_p_r",\n'),
 ('        "       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\\n"\n'
  '        "       | src_recentre_p_r;",\n'
  '        "       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\\n"\n'
  '        "       | src_recentre_p_r | cfg_adp_enable;",\n',
  '        "       media_rebase_p_w\\n"\n'
  '        "       | src_recentre_p_r;",\n'
  '        "       media_rebase_p_w\\n"\n'
  '        "       | src_recentre_p_r | cfg_adp_enable;",\n'),
]
for old, new in edits:
    assert s.count(old) == 1, old
    s = s.replace(old, new)
open(p, "w").write(s)
PY
git -C "$WORK/probe" diff > "$OUT/builder-probe.patch"
gate probe
