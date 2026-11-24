set -euo pipefail
echo "$VALIDATION_TOOLS/pinned-verilator-5.050" >> "$GITHUB_PATH"
$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version
$VALIDATION_TOOLS/pinned-verilator-5.050/verilator --version | grep -F "${VERILATOR_VERSION#v}"
PATH="$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH" \
  python3 scripts/lint_rtl.py --check --self-test --jobs "$CI_CAMPAIGN_JOBS"

