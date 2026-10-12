#!/usr/bin/env bash
# Disposable mutation probes on a copy of the composed candidate tree.
# Usage: probes.sh <clean-candidate-export> <scratch-dir> <receipts-dir>
# Each probe copies the export, applies one edit with python, runs
# `scripts/ci_events.py --check`, and records rc and the last log lines.
# "expect" is the rc class the probe should produce (fail = nonzero).
set -u
src=$1 scratch=$2 out=$3
mkdir -p "$out" "$scratch"

probe() {  # name expect file python-edit-expression
  local name=$1 expect=$2 file=$3 edit=$4 dir="$scratch/probe-$1"
  rm -rf "$dir"; cp -a "$src" "$dir"
  python3 - "$dir/$file" "$edit" <<'EOF'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); old = p.read_text()
old_s, new_s = sys.argv[2].split("\x1f")
assert old.count(old_s) >= 1, f"anchor not found: {old_s!r}"
p.write_text(old.replace(old_s, new_s, 1))
EOF
  (cd "$dir" && python3 -B scripts/ci_events.py --check) > "$out/$name.log" 2>&1
  local rc=$?
  echo $rc > "$out/$name.rc"
  local got=pass; [ $rc -ne 0 ] && got=fail
  local verdict=MATCH; [ "$got" != "$expect" ] && verdict=MISMATCH
  printf '%-34s expect=%-4s got=%-4s rc=%s %s\n' "$name" "$expect" "$got" "$rc" "$verdict"
  rm -rf "$dir"
}

US=$'\x1f'
D=docs/testing/CI_WORKFLOWS.md
W=.github/workflows/rtl-fast.yml
probe P0_control_unchanged       pass $D "${US}"
probe P1_drop_aecp_budget_row    fail $D "| \`firmware-aecp-mutants\` | 45 min | 1890 s | 1620 s |
${US}"
probe P2_srp_budget_60min        fail $D "| \`firmware-srp-mutants\` | 45 min |${US}| \`firmware-srp-mutants\` | 60 min |"
probe P3_drop_dev_621_paragraph  pass $D "#621 split further. Its small-step phase took the gmstep leg from 48 s to${US}Removed."
probe P4_drop_srp_from_aggregate fail $W ", firmware-aecp-mutants, firmware-srp-mutants]${US}, firmware-aecp-mutants]"
