echo "<tools>/pinned-verilator-5.050" >> "$GITHUB_PATH"
<tools>/pinned-verilator-5.050/verilator --version
<tools>/pinned-verilator-5.050/verilator --version | grep -F "${VERILATOR_VERSION#v}"
PATH="<tools>/pinned-verilator-5.050:$PATH" \
  python3 scripts/lint_rtl.py --check --self-test --jobs "$CI_CAMPAIGN_JOBS"
