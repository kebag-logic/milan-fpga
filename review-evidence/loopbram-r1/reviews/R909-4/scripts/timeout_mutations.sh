#!/usr/bin/env bash
# Disposable mutation probes of the loopback suites' provisional figures and
# timeout arms. Usage: timeout_mutations.sh <repo> <scratch-dir>
# Each probe exports the repo's HEAD into a fresh copy, applies one sed edit,
# and runs the planner selftest and the runner evidence contract on the copy.
set -u
repo=$1; scratch=$2
run() { # name file sed-expr
  local name=$1 file=$2 expr=$3 d="$scratch/mut-$1"
  rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive HEAD scripts tb/verilator .github | tar -x -C "$d"
  sed -i "$expr" "$d/$file"
  if cmp -s "$d/$file" <(git -C "$repo" show "HEAD:$file"); then
    echo "$name: PLANT-NOT-APPLIED"; return; fi
  python3 -I "$d/scripts/suite_shards.py" --selftest > "$d/shards.log" 2>&1; local s=$?
  python3 -I -c "import sys; sys.path.insert(0, sys.argv[1]); import measure_test_evidence as m; p = m.runner_contract(open(sys.argv[2]).read()); print(p); sys.exit(1 if p else 0)" \
      "$d/scripts" "$d/scripts/run_all_suites.sh" > "$d/runner.log" 2>&1; local r=$?
  echo "$name: suite_shards-selftest rc=$s runner_contract rc=$r :: $(grep -m1 -i 'provisional\|FAIL' "$d/shards.log" | head -c 200)"
}
run control          scripts/suite_shards.py   's/^$/&/'
run fig-299          scripts/suite_shards.py   's/"input_loopback": 300,/"input_loopback": 299,/'
run fig-dp-1800      scripts/suite_shards.py   's/"input_loopback_dp": 300,/"input_loopback_dp": 1800,/'
run arm-removed      scripts/run_all_suites.sh '/^    input_loopback)    printf/d'
run arm-dp-301       scripts/run_all_suites.sh 's/input_loopback_dp) printf .%s\\n. "${SUITE_TIMEOUT:-300}"/input_loopback_dp) printf '"'"'%s\\n'"'"' "${SUITE_TIMEOUT:-301}"/'
run unprovisional    scripts/suite_shards.py   's/frozenset({"input_loopback", "input_loopback_dp", "reboot_ctrl"})/frozenset({"reboot_ctrl"})/'
