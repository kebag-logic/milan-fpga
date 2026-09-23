#!/usr/bin/env bash
# Old tests against new RTL: the base (fbc1f715) testbench directories of
# srp_encoder, srp_decoder and srp_top planted into copies of the head tree.
# Only checks that encode the deliberately changed LeaveAll behaviour should
# fail; anything else would be an unannounced behaviour change.
# Usage: 08_old_tests_new_rtl.sh <scratch> <verilator>
set -uo pipefail
scratch=$1; vl=$2; here=$(cd "$(dirname "$0")" && pwd)
for s in srp_encoder srp_decoder srp_top; do
  t="$scratch/oldtb-$s"; rm -rf "$t"; cp -a "$scratch/head" "$t"
  rm -rf "$t/tb/$s"; cp -a "$scratch/base/tb/$s" "$t/tb/$s"
  "$here/01_run_suites.sh" "$t" "$vl" "$t/logs" "$s"
  grep -E '^FAIL' "$t/logs/$s.log" | sed 's/^/    /'
done
