#!/bin/sh
# Option-parsing edge probes for --current-retention.
#   sh probe_options.sh HEAD_CHECKER BASE_CHECKER FIXTURE_REPO
# FIXTURE_REPO: probe_matrix.py's rv-two-commit-no-later repository (main checked out).
H=$1; B=$2; cd "$3" || exit 2
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null LC_ALL=C
for args in "--no-fetch --base --current-retention main pr" \
            "--base --no-fetch main pr" \
            "--no-fetch --base main pr --current-retention --current-retention" \
            "--current-retention --selftest" \
            "--no-fetch --current-retention --base main" \
            "--no-fetch --base main pr --current-retention"; do
  echo "== head: $args"; python3 -B -I "$H" $args 2>&1 | head -3; echo "rc=$(python3 -B -I "$H" $args >/dev/null 2>&1; echo $?)"
done
echo "== base: --no-fetch --base --current-retention main pr"
python3 -B -I "$B" --no-fetch --base --current-retention main pr 2>&1 | head -1
echo "rc=$(python3 -B -I "$B" --no-fetch --base --current-retention main pr >/dev/null 2>&1; echo $?)"
