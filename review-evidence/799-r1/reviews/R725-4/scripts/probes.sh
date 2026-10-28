#!/bin/sh
# Usage: probes.sh <probe-root-with-committed-base>
# Each probe copies the base tree, plants one defect, runs the gate that claims
# to catch it, and records the rc. Expected: every planted defect is refused.
set -u
root=$1
probe() {
  name=$1; shift; mut=$1; shift
  d="$root/$name"; rm -rf "$d"; cp -a "$root/base" "$d"
  (cd "$d" && sh -c "$mut") >/dev/null 2>&1
  (cd "$d" && git diff --stat | tail -1)
  for gate in "$@"; do
    (cd "$d" && sh -c "$gate") > "$d.$(echo "$gate" | tr -c 'a-z0-9' _ | cut -c1-40).log" 2>&1
    echo "$name | $gate | rc=$?"
  done
}
SS='python3 scripts/suite_shards.py --selftest'
CK='python3 scripts/ci_gate_workflows.py --check'
probe p0_control 'true' "$SS" "$CK"
probe p1_table18_unregenerated "sed -i 's/^WORKER_OVERHEAD_SECONDS = (122,) \* 19/WORKER_OVERHEAD_SECONDS = (122,) * 18/' scripts/suite_shards.py" "$SS" "$CK"
probe p2_handedit_total20 "sed -i 's/^          - 19$/          - 20/' .github/workflows/rtl.yml" "$SS" "$CK"
probe p3_figure_over_bound "sed -i 's/\"milan_dp\": (1429, /\"milan_dp\": (1499, /' scripts/suite_shards.py" "$SS"
probe p4_regular_timeout_46 "sed -i 's/matrix.shard == 18 \&\& 60 || 45/matrix.shard == 18 \&\& 60 || 46/' .github/workflows/rtl.yml" "$CK"
probe p5_seventeen_workers_regenerated "sed -i 's/^WORKER_OVERHEAD_SECONDS = (122,) \* 19/WORKER_OVERHEAD_SECONDS = (122,) * 17/' scripts/suite_shards.py && python3 scripts/ci_gate_workflows.py" "$CK" "$SS"
probe p6_eighteen_workers_regenerated "sed -i 's/^WORKER_OVERHEAD_SECONDS = (122,) \* 19/WORKER_OVERHEAD_SECONDS = (122,) * 18/' scripts/suite_shards.py && python3 scripts/ci_gate_workflows.py" "$CK" "$SS"
probe p7_allowance_100 "sed -i 's/^WORKER_OVERHEAD_SECONDS = (122,) \* 19/WORKER_OVERHEAD_SECONDS = (100,) * 19/' scripts/suite_shards.py" "$SS"
