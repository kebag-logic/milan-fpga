set -euo pipefail
echo "<tools>/pinned-verilator-5.050" >> "$GITHUB_PATH"
<tools>/pinned-verilator-5.050/verilator --version
<tools>/pinned-verilator-5.050/verilator --version | grep -F "${VERILATOR_VERSION#v}"
