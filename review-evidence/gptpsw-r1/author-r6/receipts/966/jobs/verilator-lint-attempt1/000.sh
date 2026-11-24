set -euo pipefail
echo "/opt/verilator/bin" >> "$GITHUB_PATH"
/opt/verilator/bin/verilator --version
/opt/verilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"
PATH="/opt/verilator/bin:$PATH" \
  python3 scripts/lint_rtl.py --check --self-test --jobs "$CI_CAMPAIGN_JOBS"

