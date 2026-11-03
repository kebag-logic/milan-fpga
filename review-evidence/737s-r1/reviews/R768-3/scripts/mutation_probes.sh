#!/usr/bin/env bash
# Disposable mutation probes of the round 3 delta. Usage: mutation_probes.sh CLONE SCRATCH RECEIPTS
# Each probe copies the whole clone (with .git, so submodule source lists resolve), applies one
# mutation, regenerates the workflows where the mutation is in the generator, and runs the
# self-test that should refuse it. m0 is the unmutated control. The clone itself is never written.
set -euo pipefail
clone=$1 scratch=$2 receipts=$3
mutate() { python3 -I - "$1" "$2" "$3" <<'PY'
import pathlib, sys
path, old, new = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = path.read_text(); assert text.count(old) == 1, (path, old); path.write_text(text.replace(old, new))
PY
}
declare -A file old new
file[m1]=scripts/ci_gate_workflows.py; old[m1]='worker["timeout-minutes"] = 45'; new[m1]='worker["timeout-minutes"] = 45 if leg in BUILDER_WORKERS[name] else 44'
file[m2]=scripts/ci_litex_legs.py;     old[m2]='"test_gptp_tx_timestamp": 462,'; new[m2]='"test_gptp_tx_timestamp": 1182,'
file[m3]=scripts/ci_gate_workflows.py; old[m3]='    return BUILDER_WORKERS[name][legs.pop()]'; new[m3]='    return BUILDER_WORKERS[name][0]'
file[m4]=scripts/ci_gate_workflows.py; old[m4]='HEAD_ONLY_AGGREGATES = {"elaborate"}'; new[m4]='HEAD_ONLY_AGGREGATES = set()'
file[m5]=scripts/ci_gate_workflows.py; old[m5]='AGGREGATE_TIMEOUT = 3'; new[m5]='AGGREGATE_TIMEOUT = 4'
for m in m0 m1 m2 m3 m4 m5; do
  rm -rf "$scratch/full-$m"; cp -a "$clone" "$scratch/full-$m"
  if [ "$m" != m0 ]; then mutate "$scratch/full-$m/${file[$m]}" "${old[$m]}" "${new[$m]}"; fi
  ( cd "$scratch/full-$m"
    if [ "$m" = m2 ]; then test=ci_litex_legs_selftest; else python3 scripts/ci_gate_workflows.py; test=ci_gate_workflows_selftest; fi
    set +e; python3 scripts/$test.py > "$receipts/probe-$m.log" 2>&1; echo "$m $test rc=$?" > "$receipts/probe-$m.rc" ) &
done
wait
cat "$receipts"/probe-m?.rc
rm -rf "$scratch"/full-m?
