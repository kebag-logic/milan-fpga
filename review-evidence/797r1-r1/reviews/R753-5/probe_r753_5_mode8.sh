#!/usr/bin/env bash
# Disposable probe for review round R753-5 of PR #825 (#797): add one SRP
# drive to the sweep harness - a poll answered, then a provisioning STRMW_CTRL
# write left unanswered - and run it against the exact-head RTL and against
# the RTL with the STRMW_CTRL clear of srp_fresh_r removed (p4_noprov).
# Usage: probe_r753_5_mode8.sh <packet-dir> <verilator-shim-dir>
# Needs probe_r753_5.sh to have extracted p0_head and p4_noprov first.
set -u
PKT=$1; export PATH="$2:$PATH"
patch_sweep() {
  python3 -I - "$1" <<'EOF'
import sys
p = sys.argv[1]; t = open(p).read()
a = "for (int srpmode = 0; srpmode < 8; srpmode++)"
b = "if (srpmode == 7) answer_srp();"
assert t.count(a) == 1 and t.count(b) == 1
t = t.replace(a, "for (int srpmode = 0; srpmode < 9; srpmode++)")
t = t.replace(b, b + "\n    if (srpmode == 8) { srp_ans = answer_srp(); wr(0x810, @aaf_ctrl@u); srpw = t->o_srp_ctx_we; }")
open(p, "w").write(t); print(p, "patched: mode 8 = poll answered, then STRMW_CTRL write unanswered")
EOF
}
for n in p0_head p4_noprov; do
  d=$PKT/scratch/m8_$n; rm -rf "$d"; mkdir -p "$d"
  cp -a "$PKT/scratch/$n/hdl" "$PKT/scratch/$n/configs" "$PKT/scratch/$n/docs" "$PKT/scratch/$n/scripts" "$d/"
  patch_sweep "$d/scripts/register_read_sweep.py"
  (cd "$d" && python3 -I scripts/register_read_sweep.py --work "$d/work" > "$PKT/receipts/m8_$n.log" 2>&1; echo $? > "$PKT/receipts/m8_$n.rc") &
done
wait
for n in p0_head p4_noprov; do printf 'm8_%s rc=%s\n' "$n" "$(cat "$PKT/receipts/m8_$n.rc")"; done
