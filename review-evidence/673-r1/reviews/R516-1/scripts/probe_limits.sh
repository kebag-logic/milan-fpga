#!/usr/bin/env bash
# Probe the live suite_timeout() of a run_all_suites.sh and the evidence
# checker's runner_contract() against base, head and mutated runner text.
# Usage: probe_limits.sh REPO BASE_SHA   (REPO checked out at the head under review)
set -u
REPO=$1 BASE=$2
fn=$(sed -n '/^suite_timeout() {/,/^}/p' "$REPO/scripts/run_all_suites.sh")
eval "$fn"
echo "== live suite_timeout at $(git -C "$REPO" rev-parse HEAD)"
for s in capture_coherence milan_dp_mclk milan_dp milan_dp_gptp milan_dp_render mmcm_servo pp_shadow aaf milan_dp_mclk_x; do
  unset SUITE_TIMEOUT; a=$(suite_timeout "$s")
  SUITE_TIMEOUT=; b=$(suite_timeout "$s")
  SUITE_TIMEOUT=77; c=$(suite_timeout "$s"); unset SUITE_TIMEOUT
  printf '%-18s unset=%s empty=%s override77=%s\n' "$s" "$a" "$b" "$c"
done
echo "== runner_contract verdicts"
PYTHONDONTWRITEBYTECODE=1 python3 - "$REPO" "$BASE" <<'EOF'
import subprocess, sys
repo, base = sys.argv[1], sys.argv[2]
sys.path.insert(0, f"{repo}/scripts")
from measure_test_evidence import runner_contract
head = open(f"{repo}/scripts/run_all_suites.sh").read()
old = subprocess.run(["git", "-C", repo, "show", f"{base}:scripts/run_all_suites.sh"],
                     capture_output=True, text=True, check=True).stdout
cases = [("head runner", head, False), ("base runner (pre-#673 limits)", old, True)]
for name, a, b in [
    ("mclk 3600->3000", "milan_dp_mclk)     printf '%s\\n' \"${SUITE_TIMEOUT:-3600}\"",
                        "milan_dp_mclk)     printf '%s\\n' \"${SUITE_TIMEOUT:-3000}\""),
    ("capture 2400->2399", "SUITE_TIMEOUT:-2400", "SUITE_TIMEOUT:-2399"),
    ("milan_dp 4800->5400", "milan_dp)          printf '%s\\n' \"${SUITE_TIMEOUT:-4800}\"",
                            "milan_dp)          printf '%s\\n' \"${SUITE_TIMEOUT:-5400}\""),
    ("mclk arm deleted", "    milan_dp_mclk)     printf '%s\\n' \"${SUITE_TIMEOUT:-3600}\" ;;\n", ""),
    ("override syntax := ", "${SUITE_TIMEOUT:-3600}", "${SUITE_TIMEOUT:=3600}"),
    ("arms reordered", "    milan_dp_gptp)     printf '%s\\n' \"${SUITE_TIMEOUT:-5400}\" ;;\n    milan_dp_mclk)     printf '%s\\n' \"${SUITE_TIMEOUT:-3600}\" ;;\n",
                       "    milan_dp_mclk)     printf '%s\\n' \"${SUITE_TIMEOUT:-3600}\" ;;\n    milan_dp_gptp)     printf '%s\\n' \"${SUITE_TIMEOUT:-5400}\" ;;\n"),
]:
    assert a in head, name
    cases.append((name, head.replace(a, b), True))
bad = 0
for name, text, expect_reject in cases:
    probs = runner_contract(text)
    ok = bool(probs) == expect_reject
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name}: {'rejected: ' + '; '.join(probs) if probs else 'accepted'}")
print(f"{len(cases) - bad}/{len(cases)} probe expectations met")
sys.exit(1 if bad else 0)
EOF
