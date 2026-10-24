echo "<scratch>/optverilator/bin" >> "$GITHUB_PATH"
<scratch>/optverilator/bin/verilator --version
<scratch>/optverilator/bin/verilator --version | grep -F "${VERILATOR_VERSION#v}"
PATH="<scratch>/optverilator/bin:$PATH" \
  python3 scripts/lint_rtl.py --check --self-test --jobs "$CI_CAMPAIGN_JOBS"
