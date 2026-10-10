#!/usr/bin/env bash
# Local replica of .github/workflows/rtl-fast.yml jobs changes, verilator-lint
# and bdd-conformance at the checked-out head (yosys-elaboration and
# firmware-unit are recorded separately). Usage:
# rtl_fast_other_replica.sh <repo> <venv-bin> <verilator-dir> <logdir>
set -u
repo=$1; vbin=$2; vdir=$3; logs=$4
py="$vbin/python"
mkdir -p "$logs"
cd "$repo" || exit 2
n=0; fails=0
step() {
  n=$((n + 1))
  local log; log=$(printf '%s/%02d.log' "$logs" "$n")
  "$@" > "$log" 2>&1
  local rc=$?
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  printf 'rc=%d  %s\n' "$rc" "$*"
}
step "$py" scripts/ci_scope.py --selftest
step "$vdir/verilator" --version
step env PATH="$vdir:$PATH" "$py" scripts/lint_rtl.py --check --self-test
step "$py" scripts/pp_srcs.py --check --selftest
pushd tests > /dev/null || exit 2
step "$vbin/behave" --no-capture -f plain
popd > /dev/null || exit 2
echo "steps: $n  failing: $fails"
[ "$fails" -eq 0 ]
